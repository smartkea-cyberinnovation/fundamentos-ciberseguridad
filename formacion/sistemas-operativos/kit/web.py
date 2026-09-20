#!/usr/bin/env python3
"""Servicio web docente de rutas fijas. SOLO laboratorio; no servidor de produccion."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import sys

PAGE = '''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laboratorio de sistemas</title><style>
body{background:#fff;color:#172337;font:18px/1.65 system-ui;margin:4rem auto;padding:0 1.5rem;max-width:52rem}
article{border:1px solid #cdd7e5;border-radius:12px;padding:2rem;background:#f7f9fc}
a{color:#164f8b}code{background:#edf2f7;padding:.2rem .4rem}
</style><h1>Laboratorio de sistemas</h1><article><h2>Servicio docente operativo</h2>
<p>Este sitio utiliza datos ficticios y no recibe credenciales ni archivos.</p>
<p>Comprueba <a href="/healthz">el estado JSON</a>, revisa las cabeceras y relaciona cada respuesta con su log.</p>
<p>GET y HEAD son las operaciones admitidas. Una ruta inexistente devuelve 404.</p>
</article></html>'''.encode('utf-8')


class Handler(BaseHTTPRequestHandler):
    server_version = 'OSLab/1.1'
    sys_version = ''

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, format, *args):
        # No registrar cabeceras, query strings, rutas arbitrarias ni IP personales.
        pass

    def respond(self, head=False, denied=False):
        route = self.path.split('?', 1)[0]
        if denied:
            status, mime, content = 405, 'application/json', b'{"error":"method_not_allowed"}\n'
        elif route == '/':
            status, mime, content = 200, 'text/html; charset=utf-8', PAGE
        elif route == '/healthz':
            status, mime, content = 200, 'application/json', b'{"status":"ok","synthetic":true}\n'
        else:
            status, mime, content = 404, 'application/json', b'{"error":"not_found"}\n'
        self.send_response(status)
        for name, value in [('Content-Type', mime), ('Content-Length', str(len(content))),
                            ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'),
                            ('Referrer-Policy', 'no-referrer'),
                            ('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")]:
            self.send_header(name, value)
        if denied: self.send_header('Allow', 'GET, HEAD')
        self.end_headers()
        if not head: self.wfile.write(content)
        print(json.dumps({'event':'http_response', 'route':route if route in ('/', '/healthz') else 'other', 'status':status}), flush=True)

    def do_GET(self): self.respond()
    def do_HEAD(self): self.respond(head=True)
    def do_POST(self): self.respond(denied=True)
    def do_PUT(self): self.respond(denied=True)
    def do_DELETE(self): self.respond(denied=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['127.0.0.1', '0.0.0.0'], default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535: parser.error('Puerto entre 1024 y 65535')
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        try: server.serve_forever()
        except KeyboardInterrupt: pass


if __name__ == '__main__': main()
