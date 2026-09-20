#!/usr/bin/env python3
"""Vista previa local: solo loopback. Producción: Pages o servidor estático dedicado."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from build import CSP
class Handler(SimpleHTTPRequestHandler):
    server_version='CampusPreview'
    sys_version=''
    def end_headers(self):
        self.send_header('Content-Security-Policy',CSP)
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Cache-Control','no-cache')
        super().end_headers()
    def list_directory(self,path): self.send_error(404);return None
    def log_message(self,*args): pass
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8788);args=parser.parse_args()
    if not 1024<=args.port<=65535:parser.error('Puerto fuera de rango.')
    folder=Path(__file__).resolve().parent/'dist'
    if not (folder/'index.html').is_file():parser.error('Ejecuta primero python3 campus/build.py desde la raíz del repositorio.')
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(folder)))
    print(f'Vista previa local: http://127.0.0.1:{args.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
