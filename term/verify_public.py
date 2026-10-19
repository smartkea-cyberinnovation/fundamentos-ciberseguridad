#!/usr/bin/env python3
"""Verify an already deployed TERM release using bounded, read-only HTTPS GETs.

No token, browser session, shell endpoint or external scanning is involved.
Only the two configured SmartKEA hosts and the TERM path are permitted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

PREFIX = '/fundamentos-ciberseguridad/term/'
BASE = 'https://www.smartkea.com' + PREFIX
HOSTS = {'smartkea.com', 'www.smartkea.com'}
MAX_BYTES = 3_000_000
REQUIRED = {'index.html','manual.html','course.json','config.json','build-info.json',
            'assets/app.js','assets/state.js','assets/styles.css','downloads/labs.zip'}


def allowed_url(url: str) -> bool:
    try:
        u = urlsplit(url)
        return (u.scheme == 'https' and u.hostname in HOSTS and u.port in (None,443)
                and not (u.username or u.password or u.query or u.fragment)
                and (u.path == PREFIX[:-1] or u.path.startswith(PREFIX))
                and not any(x in url for x in ('\\','\r','\n','\t',' '))
                and '%' not in u.path and '..' not in PurePosixPath(u.path).parts)
    except ValueError:
        return False


class ScopedRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError('Redirect outside the approved HTTPS TERM route.')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str) -> dict:
    if not allowed_url(url):
        raise ValueError('Only public HTTPS TERM assets may be checked.')
    req = Request(url, headers={'User-Agent':'SmartKEA-TERM-release-check/1.0',
                               'Cache-Control':'no-cache'})
    try:
        response = build_opener(ScopedRedirect()).open(req, timeout=15)
    except HTTPError as error:
        response = error
    with response:
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('Public response exceeds the verification limit.')
        return {'status':response.status, 'body':body, 'url':response.geturl(),
                'headers':dict(response.headers.items())}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_manifest(body: bytes) -> dict[str,str]:
    result = {}
    for line in body.decode('utf-8').splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  ([A-Za-z0-9_./-]+)',line)
        if not match:
            raise ValueError('Malformed public manifest.')
        digest, name = match.groups()
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or any(x.startswith('.') for x in p.parts) or p.as_posix()!=name or name in result:
            raise ValueError('Unsafe or repeated manifest path.')
        result[name]=digest
    if not REQUIRED <= result.keys() or '_headers' in result or 'SHA256SUMS.txt' in result:
        raise ValueError('Manifest does not describe the deployed public assets.')
    if len(result)>100:
        raise ValueError('Unexpected number of assets.')
    return result


def verify_documents(info: dict, course_body: bytes, config_body: bytes, expected: str) -> dict:
    course=json.loads(course_body);config=json.loads(config_body)
    lessons=[l for m in course['modules'] for l in m['lessons']]
    counts={'modules':len(course['modules']),'lessons':len(lessons),
            'questions':sum(len(l['quiz']) for l in lessons),
            'steps':sum(len(l['steps']) for l in lessons)}
    if info.get('id')!='smartkea-term-linux' or info.get('sourceCommit')!=expected or info.get('sourceDirty') is not False:
        raise ValueError('The public deployment is not the requested clean commit.')
    if info.get('courseSha256')!=sha(course_body):
        raise ValueError('Public course does not match its recorded hash.')
    if counts!={'modules':16,'lessons':48,'questions':96,'steps':194} or any(info.get(k)!=v for k,v in counts.items()):
        raise ValueError('Unexpected curriculum cardinality.')
    lab=config['lab']
    if info.get('labConfigured') is not bool(lab.get('url')):
        raise ValueError('Terminal configuration contradicts build metadata.')
    if not lab.get('url') and (lab.get('embed') or lab.get('allowedOrigins')):
        raise ValueError('An unconfigured terminal must remain disabled.')
    return counts


def check(expected: str, reader=fetch) -> dict:
    result={'checkedAt':datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'expectedCommit':expected,'baseUrl':BASE,'checks':[]}
    info_response=reader(BASE+'build-info.json')
    if info_response['status']!=200:
        raise ValueError('Build metadata is not available over HTTPS.')
    info=json.loads(info_response['body'])
    if info.get('sourceCommit')!=expected:
        raise ValueError('Waiting for requested commit to reach the public route.')
    manifest_response=reader(BASE+'SHA256SUMS.txt')
    if manifest_response['status']!=200:
        raise ValueError('Public manifest is unavailable.')
    manifest=parse_manifest(manifest_response['body'])
    bodies={}
    for name, digest in manifest.items():
        r=reader(BASE+name)
        if r['status'] not in ((200,404) if name=='404.html' else (200,)) or sha(r['body'])!=digest:
            raise ValueError('Public asset mismatch: '+name)
        if name=='index.html':
            headers={k.lower():v for k,v in r['headers'].items()}
            csp=headers.get('content-security-policy','')
            for directive in ("default-src 'self'","object-src 'none'","frame-ancestors 'none'"):
                if directive not in csp:
                    raise ValueError('Missing public security header: '+directive)
            if headers.get('x-content-type-options')!='nosniff':
                raise ValueError('Public nosniff header is missing.')
        bodies[name]=r['body']
        result['checks'].append({'path':name,'status':r['status'],'sha256':digest})
    result.update(verify_documents(info,bodies['course.json'],bodies['config.json'],expected))
    for host in sorted(HOSTS):
        for suffix in ('','/'):
            r=reader('https://'+host+PREFIX[:-1]+suffix)
            if r['status']!=200 or sha(r['body'])!=manifest['index.html']:
                raise ValueError('Course entry does not resolve on '+host+suffix)
    missing=reader(BASE+'__term_release_check_missing__')
    if missing['status']!=404:
        raise ValueError('A missing route must return HTTP 404, not a soft 200.')
    final=reader(BASE+'build-info.json')
    if final['status']!=200 or final['body']!=info_response['body']:
        raise ValueError('Deployment changed during verification; repeat the check.')
    result.update(status='passed',labConfigured=info['labConfigured'],
                  manifestSha256=sha(manifest_response['body']))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-commit',required=True)
    parser.add_argument('--attempts',type=int,default=1)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if not re.fullmatch(r'[a-f0-9]{40}',args.expected_commit) or not 1<=args.attempts<=12:
        parser.error('A full commit SHA and 1–12 attempts are required.')
    result={}
    for attempt in range(args.attempts):
        try:
            result=check(args.expected_commit);break
        except (ValueError,OSError,KeyError,TypeError) as error:
            result={'status':'failed','expectedCommit':args.expected_commit,
                    'checkedAt':datetime.now(timezone.utc).isoformat(timespec='seconds'),
                    'error':str(error),'attempt':attempt+1}
            print(json.dumps(result),file=sys.stderr)
            if attempt+1<args.attempts:time.sleep(10)
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text,end='')
    return 0 if result.get('status')=='passed' else 1


if __name__=='__main__':
    raise SystemExit(main())
