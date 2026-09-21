#!/usr/bin/env python3
"""Read-only HTTP acceptance of the campus at its real subpath; never runs labs."""
import argparse
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import urlopen
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from publication import PUBLIC_BASE_PATH, PUBLIC_URL
from provenance import source_commit
from operations import READINGS

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--origin', default='http://127.0.0.1:8789')
args = parser.parse_args()
origin = args.origin.rstrip('/')
base = origin + PUBLIC_BASE_PATH
expected_resources=[f'D{i:02}' for i in range(1,22)]+[item[0] for item in READINGS]
expected_version=json.loads((Path(__file__).resolve().parents[1]/'package.json').read_text())['version']
for attempt in range(80):
    try:
        with urlopen(base,timeout=2) as response:
            assert response.status==200
            assert 'Fundamentos' in response.read().decode()
            assert "script-src 'self'" in response.headers.get('Content-Security-Policy','')
            assert response.headers.get('X-Content-Type-Options')=='nosniff'
        break
    except (URLError,TimeoutError):
        if attempt==79:raise
        time.sleep(.25)
with urlopen(base+'course.json',timeout=5) as response:
    data=json.load(response)
    assert data['id']=='fundamentos-ciberseguridad'
    assert len(data['modules'])==32 and data['hours']==480
    assert [item['id'] for item in data['resources']]==expected_resources
    assert data['version']==expected_version
with urlopen(base+'course.en.json',timeout=5) as response:
    english=json.load(response);assert english['language']=='en'
    assert len(english['modules'])==32 and sum(len(module['labs']) for module in english['modules'])==96
    assert [item['id'] for item in english['resources']]==expected_resources
    assert english['version']==expected_version
with urlopen(base+'build-info.json',timeout=5) as response:
    info=json.load(response);assert info['version']==expected_version
    assert info['publicBasePath']==PUBLIC_BASE_PATH and info['publicUrl']==PUBLIC_URL
    expected=source_commit(Path(__file__).resolve().parents[2])
    assert info['sourceCommit']==expected, 'The runtime must match the current checkout provenance.'
    if urlsplit(origin).hostname not in ('127.0.0.1','localhost'):
        assert expected, 'Remote acceptance requires a clean, committed checkout.'
with urlopen(base+'assets/catalog.js',timeout=5) as response:
    assert 'javascript' in response.headers.get('Content-Type','')
for name in ('not-a-real-file-123456.json','nested/not-a-real-file.html'):
    try:
        urlopen(base+name,timeout=5)
        raise AssertionError('A missing path must return 404, not successful HTML.')
    except HTTPError as error:
        assert error.code==404
        page=error.read().decode()
        assert 'File not found.' in page
        for link in re.findall(r'(?:href|src)="([^"]+)"',page):
            path=urlsplit(link).path
            assert path.startswith(PUBLIC_BASE_PATH)
            with urlopen(origin+path,timeout=5) as asset:
                assert asset.status==200
                if path.endswith('.css'):assert 'text/css' in asset.headers.get('Content-Type','')
markers = [PUBLIC_BASE_PATH.lstrip('/')+'.campus-generated']
if urlsplit(origin).hostname in ('127.0.0.1','localhost') or urlsplit(origin).hostname.endswith('.workers.dev'):
    markers.append('.campus-worker-generated')
for name in markers:
    try:
        urlopen(origin+'/'+name,timeout=5)
        raise AssertionError('An internal generator marker must not be public.')
    except HTTPError as error:
        assert error.code==404
print(json.dumps({'status':'passed','runtime':origin,'publicBasePath':PUBLIC_BASE_PATH,
                  'checks':9,'sourceCommit':info['sourceCommit'], 'resources':len(expected_resources),
                  'remoteDeployment':urlsplit(origin).hostname not in ('127.0.0.1','localhost')}))
