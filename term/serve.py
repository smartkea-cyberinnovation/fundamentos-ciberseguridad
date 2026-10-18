#!/usr/bin/env python3
"""Loopback-only preview of the static TERM release, including production prefix."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json
import sys
import build


class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(build.HERE/'dist'),**kwargs)

    def translate_path(self,path):
        parsed=urlsplit(path)
        decoded=unquote(parsed.path)
        if decoded.startswith(build.PUBLIC_PATH):decoded=decoded[len(build.PUBLIC_PATH):]
        elif decoded.startswith('/'):decoded=decoded[1:]
        root=(build.HERE/'dist').resolve()
        candidate=(root/decoded).resolve()
        if not candidate.is_relative_to(root) or any(p.startswith('.') for p in Path(decoded).parts):
            return str(root/'__forbidden__')
        return str(candidate)

    def do_GET(self):
        url=urlsplit(self.path)
        if url.path==build.PUBLIC_PATH.rstrip('/'):
            self.send_response(308);self.send_header('Location',build.PUBLIC_PATH+('?' + url.query if url.query else ''));self.end_headers();return
        return super().do_GET()

    def list_directory(self,path):
        self.send_error(404);return None

    def end_headers(self):
        lab=json.loads((build.HERE/'dist/config.json').read_text())['lab']
        for line in build.headers(lab).splitlines()[1:]:
            if ':' in line:
                key,value=line.strip().split(':',1);self.send_header(key,value.strip())
        super().end_headers()

    def log_message(self,format,*args):
        # Local test URLs only. Avoid logging query parameters from shared links.
        print(f'{self.command} {urlsplit(self.path).path}',file=sys.stderr)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8791);args=parser.parse_args()
    build.validate()
    print(f'Preview: http://127.0.0.1:{args.port}{build.PUBLIC_PATH}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
