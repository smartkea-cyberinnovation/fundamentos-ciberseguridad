"""Network-level tests for the synthetic service, on ephemeral loopback ports."""
import http.client
import importlib.util
import json
import os
import pathlib
import select
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch

APP_PATH = pathlib.Path(__file__).resolve().parents[1] / "web" / "app.py"
spec = importlib.util.spec_from_file_location("smartkea_lab_app", APP_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.LabHTTPServer(("127.0.0.1", 0), app.LabHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, method="GET", headers=None, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        try:
            conn.request(method, path, headers=headers or {}, body=body)
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def test_health_contract(self):
        status, headers, body = self.request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"status": "ok", "service": "smartkea-lab-web", "synthetic": True})
        self.assertEqual(int(headers["Content-Length"]), len(body))

    def test_head_has_get_length_without_body(self):
        status, headers, body = self.request("/health", method="HEAD")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"")
        self.assertEqual(int(headers["Content-Length"]), len(app.ROUTES["/health"][1]))

    def test_unknown_head_has_no_body(self):
        status, _, body = self.request("/missing", method="HEAD")
        self.assertEqual(status, 404)
        self.assertEqual(body, b"")

    def test_no_filesystem_routes_or_query_reflection(self):
        for path in ("/../../etc/passwd", "/%2e%2e/etc/passwd", "/training-only", "/missing?payload=REFLECT_ME"):
            with self.subTest(path=path):
                status, _, body = self.request(path)
                self.assertEqual(status, 404)
                self.assertNotIn(b"root:", body)
                self.assertNotIn(b"REFLECT_ME", body)

    def test_mutation_methods_rejected(self):
        for method in ("POST", "PUT", "PATCH", "DELETE", "CONNECT", "TRACE", "OPTIONS"):
            with self.subTest(method=method):
                status, headers, body = self.request("/health", method=method, body=b"test-input")
                self.assertEqual(status, 405)
                self.assertEqual(headers["Allow"], "GET, HEAD")
                self.assertNotIn(b"test-input", body)

    def test_security_headers_and_fixed_routes(self):
        status, headers, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertNotIn(b"<script", body)
        self.assertEqual(self.request("/robots.txt")[2], b"User-agent: *\nDisallow: /training-only\n")

    def test_logs_do_not_include_query_or_authorization(self):
        records = []
        received = threading.Event()

        def capture(message, **kwargs):
            records.append(str(message))
            received.set()

        with patch("builtins.print", side_effect=capture):
            self.assertEqual(self.request("/health?token=PRIVATE_QUERY", headers={"Authorization": "Bearer PRIVATE_AUTH"})[0], 200)
            self.assertTrue(received.wait(timeout=2))
        text = "\n".join(records)
        self.assertNotIn("PRIVATE_QUERY", text)
        self.assertNotIn("PRIVATE_AUTH", text)
        record = json.loads(records[-1])
        self.assertEqual(record["path"], "/health")
        self.assertEqual(record["event"], "http_request")
        self.assertIs(record["synthetic_service"], True)

    def test_concurrent_connection_limit_is_finite(self):
        # Reserve every slot and confirm a further connection is refused promptly.
        reserved = []
        for _ in range(16):
            self.assertTrue(self.server.slots.acquire(blocking=False))
            reserved.append(True)
        try:
            self.assertFalse(self.server.slots.acquire(blocking=False))
            with self.assertRaises((http.client.RemoteDisconnected, ConnectionResetError)):
                self.request("/health")
        finally:
            for _ in reserved:
                self.server.slots.release()

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux no_new_privs deployment test")
    def test_real_process_starts_unprivileged_with_no_new_privs(self):
        options = {"user": 65534, "group": 65534, "extra_groups": []} if os.geteuid() == 0 else {}
        env = {**os.environ, "LAB_WEB_BIND": "127.0.0.1", "LAB_WEB_PORT": "0"}
        try:
            process = subprocess.Popen([sys.executable, str(APP_PATH)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd="/tmp", env=env, **options)
        except PermissionError:
            self.skipTest("Runner cannot switch to an unprivileged UID; execute this check on the dedicated Linux VM")
        try:
            readable, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(readable, "No startup event from lab server")
            line = process.stdout.readline()
            self.assertTrue(line, process.stderr.read() if process.poll() is not None else "Empty startup event")
            ready = json.loads(line)
            self.assertEqual(ready["event"], "ready")
            status = pathlib.Path(f"/proc/{process.pid}/status").read_text()
            self.assertRegex(status, r"NoNewPrivs:\s+1")
            self.assertNotRegex(status, r"Uid:\s+0\s")
            connection = http.client.HTTPConnection("127.0.0.1", ready["port"], timeout=2)
            try:
                connection.request("GET", "/health")
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                self.assertTrue(json.loads(response.read())["synthetic"])
            finally:
                connection.close()
        finally:
            process.terminate()
            process.communicate(timeout=3)


if __name__ == "__main__":
    unittest.main()
