#!/usr/bin/env python3
"""Read-only HTTP acceptance of the campus at its real subpath; never runs labs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import time
import zipfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import urlopen
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from publication import PUBLIC_BASE_PATH, PUBLIC_URL
from provenance import source_commit
from operations import READINGS
from integral import READINGS as INTEGRAL_READINGS

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--origin', default='http://127.0.0.1:8789')
args = parser.parse_args()
origin = args.origin.rstrip('/')
base = origin + PUBLIC_BASE_PATH
expected_resources=[f'D{i:02}' for i in range(1,22)]+[item[0] for item in READINGS]+[item[0] for item in INTEGRAL_READINGS]
assert expected_resources == [f'D{i:02}' for i in range(1,41)], 'Keep the complete ordered public resource contract.'
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

# Exercise the added course through the same real Workers Static Assets runtime.
term_path='/fundamentos-ciberseguridad/term/'
term_base=origin+term_path
term_dist=Path(__file__).resolve().parents[2]/'term/dist'
expected_csp=next(line.split(': ',1)[1] for line in (term_dist/'_headers').read_text().splitlines()
                  if line.strip().startswith('Content-Security-Policy:'))
with urlopen(term_base,timeout=5) as response:
    assert response.status==200 and 'TERM' in response.read().decode()
    assert response.headers.get('Content-Security-Policy')==expected_csp, 'TERM must have its own single CSP.'
    assert response.headers.get('X-Content-Type-Options')=='nosniff'
with urlopen(origin+term_path.rstrip('/')+'?entry=check',timeout=5) as response:
    assert urlsplit(response.url).path==term_path and urlsplit(response.url).query=='entry=check'
with urlopen(term_base+'course.json',timeout=5) as response:
    term_bytes=response.read();term_data=json.loads(term_bytes)
    assert term_data['id']=='smartkea-term-linux' and len(term_data['modules'])==16
    term_lessons=[lesson for module in term_data['modules'] for lesson in module['lessons']]
    assert len(term_lessons)==48 and sum(len(lesson['quiz']) for lesson in term_lessons)==96
with urlopen(term_base+'build-info.json',timeout=5) as response:
    term_info=json.load(response)
    assert term_info['sourceCommit']==info['sourceCommit']
    assert term_info['sourceDirty'] is False, 'Generated staging files must not make a clean build dirty.'
    assert term_info['courseSha256']==hashlib.sha256(term_bytes).hexdigest()
with urlopen(term_base+'config.json',timeout=5) as response:
    assert json.load(response)==json.loads((term_dist/'config.json').read_text())
with urlopen(term_base+'manual.html',timeout=5) as response:
    manual=response.read().decode()
    assert manual.count('class="manual-lesson"')==48 and manual.count('class="manual-quiz"')==96
with urlopen(term_base+'downloads/labs.zip',timeout=5) as response:
    with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
        assert {'README.md','labs/compose.yaml','labs/scripts/ttyd-smoke.py'} <= set(archive.namelist())
try:
    urlopen(term_base+'missing-term-asset.js',timeout=5)
    raise AssertionError('A missing TERM asset must return 404.')
except HTTPError as error:
    assert error.code==404
    assert term_path in error.read().decode()
print(json.dumps({'status':'passed','runtime':origin,'publicBasePath':PUBLIC_BASE_PATH,
                  'checks':17,'sourceCommit':info['sourceCommit'], 'resources':len(expected_resources),
                  'termLessons':len(term_lessons),'termCourseSha256':term_info['courseSha256'],
                  'remoteDeployment':urlsplit(origin).hostname not in ('127.0.0.1','localhost')}))
