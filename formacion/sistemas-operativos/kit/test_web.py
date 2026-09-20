import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from web import Handler


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=3)

    def request(self, path, method='GET'):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        try:
            conn.request(method, path)
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally: conn.close()

    def test_home(self):
        status, headers, data = self.request('/')
        self.assertEqual(status, 200); self.assertIn(b'Laboratorio de sistemas', data)

    def test_health(self):
        status, headers, data = self.request('/healthz')
        self.assertEqual(status, 200); self.assertEqual(json.loads(data), {'status':'ok','synthetic':True})

    def test_head(self):
        status, headers, data = self.request('/healthz', 'HEAD')
        self.assertEqual(status, 200); self.assertEqual(data, b''); self.assertGreater(int(headers['Content-Length']), 0)

    def test_not_found(self):
        self.assertEqual(self.request('/no-existe')[0], 404)

    def test_no_file_serving(self):
        status, headers, data = self.request('/web.py')
        self.assertEqual(status, 404); self.assertNotIn(b'import', data)

    def test_post_denied(self):
        status, headers, data = self.request('/', 'POST')
        self.assertEqual(status, 405); self.assertEqual(headers['Allow'], 'GET, HEAD')

    def test_security_headers(self):
        status, headers, data = self.request('/')
        self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        self.assertEqual(headers['Cache-Control'], 'no-store')

    def test_no_query_reflection(self):
        status, headers, data = self.request('/?mensaje=secreto-ficticio')
        self.assertNotIn(b'secreto-ficticio', data)


if __name__ == '__main__': unittest.main()
