#!/usr/bin/env python3
"""Small synthetic HTTP service for an isolated teaching lab.

There is no file serving, command execution, upload, database or user account.
Python's standard-library HTTP server is used only inside this training network.
"""

from __future__ import annotations

import json
import ctypes
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

INDEX = b"""<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SmartKEA | Laboratorio HTTP</title>
<style>body{color:#17233b;background:#f8fafc;font:18px/1.6 system-ui;max-width:50rem;margin:5rem auto;padding:1.5rem}a{color:#174ac5}code{background:#edf2ff;padding:.2em .4em;border-radius:.25em}</style>
<h1>Laboratorio HTTP de SmartKEA</h1>
<p>Servicio de aprendizaje con datos sinteticos. Explora las peticiones, las cabeceras,
los codigos de respuesta y los logs.</p>
<ul><li><a href="/health">/health</a></li><li><a href="/catalog.json">/catalog.json</a></li>
<li><a href="/robots.txt">/robots.txt</a></li></ul>
<p>Un archivo robots.txt orienta rastreadores: no sustituye un control de acceso.</p>
<p>Todos los objetivos de estas practicas pertenecen al laboratorio aislado.</p></html>"""


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


ROUTES = {
    "/": ("text/html; charset=utf-8", INDEX),
    "/health": ("application/json; charset=utf-8", json_bytes({
        "status": "ok", "service": "smartkea-lab-web", "synthetic": True,
    })),
    "/catalog.json": ("application/json; charset=utf-8", json_bytes({
        "synthetic": True,
        "items": [{"id": "LAB-001", "name": "Terminal de practicas", "available": True},
                  {"id": "LAB-002", "name": "Guia de evidencias", "available": True}],
    })),
    "/robots.txt": ("text/plain; charset=utf-8", b"User-agent: *\nDisallow: /training-only\n"),
}


class LabHTTPServer(ThreadingHTTPServer):
    """Limit simultaneous connections; a slow client cannot spawn unlimited threads."""

    daemon_threads = True
    request_queue_size = 16
    allow_reuse_address = True

    def __init__(self, server_address, handler_class):
        self.slots = threading.BoundedSemaphore(16)
        super().__init__(server_address, handler_class)

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()


class LabHandler(BaseHTTPRequestHandler):
    server_version = "SmartKEA-Lab/1.0"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def setup(self):
        self.request.settimeout(5)
        super().setup()

    def log_message(self, format, *args):
        # Request headers, credentials, body and query string are never logged.
        return

    def respond(self, status: int, content_type: str, body: bytes, *, head=False):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.send_header("Connection", "close")
        if status == 405:
            self.send_header("Allow", "GET, HEAD")
        self.end_headers()
        self.close_connection = True
        if not head:
            self.wfile.write(body)
        # json.dumps escapes control characters, preventing log-line injection.
        print(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event": "http_request", "client": self.client_address[0],
            "method": self.command, "path": self.safe_path(), "status": status,
            "synthetic_service": True,
        }, ensure_ascii=True), flush=True)

    def safe_path(self):
        try:
            return urlsplit(self.path).path[:512]
        except ValueError:
            return "[invalid-path]"

    def do_GET(self):
        resource = ROUTES.get(self.safe_path())
        if resource is None:
            return self.respond(404, "application/json; charset=utf-8", json_bytes({"error": "not_found", "synthetic": True}))
        content_type, body = resource
        return self.respond(200, content_type, body, head=self.command == "HEAD")

    def do_HEAD(self):
        resource = ROUTES.get(self.safe_path())
        if resource is None:
            return self.respond(404, "application/json; charset=utf-8", json_bytes({"error": "not_found", "synthetic": True}), head=True)
        return self.do_GET()

    def reject_method(self):
        return self.respond(405, "application/json; charset=utf-8", json_bytes({"error": "method_not_allowed"}))

    do_POST = reject_method
    do_PUT = reject_method
    do_PATCH = reject_method
    do_DELETE = reject_method
    do_CONNECT = reject_method
    do_TRACE = reject_method
    do_OPTIONS = reject_method


def main():
    if os.geteuid() == 0:
        raise SystemExit("Run the lab service as an unprivileged user (UID 10001 in Docker).")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
    libc.prctl.restype = ctypes.c_int
    if libc.prctl(38, 1, 0, 0, 0) != 0:  # Linux PR_SET_NO_NEW_PRIVS
        raise SystemExit("Could not enable no_new_privs; refusing to start.")
    address = os.environ.get("LAB_WEB_BIND", "0.0.0.0")
    port = int(os.environ.get("LAB_WEB_PORT", "8080"))
    if not 0 <= port <= 65535:
        raise SystemExit("LAB_WEB_PORT must be between 0 and 65535 (0 selects an ephemeral test port)")
    server = LabHTTPServer((address, port), LabHandler)
    print(json.dumps({"event": "ready", "service": "smartkea-lab-web", "port": server.server_port}), flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
