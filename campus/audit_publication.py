#!/usr/bin/env python3
"""Bounded public GET review of the campus. No credentials, scans or deployment.

Run explicitly: python3 campus/audit_publication.py --output campus/qa/publication.json
The report proves only the observations made at its timestamp, not account configuration.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import ssl
import urllib.error
import urllib.request

BASE = 'https://smartkea.com/introduccion-ciberseguridad/'
# Fixed allowlist. Never accept a caller-supplied URL or read a URL from downloaded content.
TARGETS = (('', 200, 'text/html'), ('build-info.json', 200, 'application/json'),
           ('course.json', 200, 'application/json'), ('course.en.json', 200, 'application/json'),
           ('assets/app.js', 200, 'javascript'), ('assets/styles.css', 200, 'text/css'),
           ('review-nonexistent-20260921.txt', 404, 'text/html'))
LIMIT = 8 * 1024 * 1024

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def inspect_body(name: str, body: bytes) -> dict:
    info = {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    if name in ('course.json', 'course.en.json'):
        data = json.loads(body)
        info.update(language=data.get('language'), version=data.get('version'),
                    modules=len(data.get('modules', [])),
                    labs=sum(len(m.get('labs', [])) for m in data.get('modules', [])),
                    resources=len(data.get('resources', [])), hours=data.get('hours'))
    elif name == 'build-info.json':
        data = json.loads(body)
        # Only public release identifiers, not arbitrary server response data.
        info['build'] = {k: data[k] for k in ('version','sourceCommit','modules','labs','hours','languages') if k in data}
    return info

def review() -> dict:
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    rows = []
    for name, expected, mime in TARGETS:
        row = {'path': name or '/', 'expectedStatus': expected}
        try:
            req = urllib.request.Request(BASE + name, headers={'User-Agent':'SmartKEA-Campus-ReadOnly-Review/1.0', 'Accept-Encoding':'identity'})
            try:
                response = opener.open(req, timeout=15)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                body = response.read(LIMIT + 1)
                if len(body) > LIMIT:
                    raise ValueError('Response exceeds bounded review limit')
                row['status'] = response.status
                row['contentType'] = response.headers.get('Content-Type','')
                row['protections'] = {k: response.headers.get(k,'') for k in
                    ('Content-Security-Policy','X-Content-Type-Options','Referrer-Policy')}
                row.update(inspect_body(name, body) if response.status == expected else {'bytes':len(body)})
                row['passed'] = response.status == expected and mime in row['contentType'].lower()
        except (OSError, ValueError, urllib.error.URLError) as error:
            row.update(passed=False, errorType=type(error).__name__)
        rows.append(row)
    return {'observedAt':dt.datetime.now(dt.timezone.utc).isoformat(), 'base':BASE,
            'scope':'Seven fixed public GETs; no login, no redirects followed, no account inspection.',
            'passed':all(r['passed'] for r in rows), 'observations':rows}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=review()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
