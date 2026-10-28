"""Offline tests for the public verifier, including an end-to-end fake transport."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('term_verify',ROOT/'verify_public.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
COMMIT='a'*40
HEADERS={'Content-Security-Policy':"default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
         'X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY',
         'Cache-Control':'public, no-cache, no-transform'}

class PublicTests(unittest.TestCase):
    def test_url_scope(self):
        self.assertTrue(v.allowed_url(v.BASE))
        self.assertTrue(v.allowed_url('https://smartkea.com'+v.PREFIX[:-1]))
        for url in ['http://www.smartkea.com'+v.PREFIX,'https://evil.test'+v.PREFIX,
                    v.BASE+'../secret',v.BASE+'%2e%2e/secret',v.BASE+'?token=test',
                    'https://user:pass@www.smartkea.com'+v.PREFIX,
                    'https://www.smartkea.com/contacto']:
            self.assertFalse(v.allowed_url(url),url)

    def manifest(self,extra=''):
        return (''.join('a'*64+'  '+p+'\n' for p in sorted(v.REQUIRED))+extra).encode()

    def test_manifest_rejects_unsafe_duplicate_or_incomplete_paths(self):
        self.assertEqual(set(v.parse_manifest(self.manifest())),v.REQUIRED)
        for extra in ['a'*64+'  ../outside\n','a'*64+'  /etc/passwd\n',
                      'a'*64+'  .env\n','a'*64+'  index.html\n',
                      'a'*64+'  _headers\n','a'*64+'  assets//app.js\n']:
            with self.assertRaises(ValueError):v.parse_manifest(self.manifest(extra))
        with self.assertRaises(ValueError):v.parse_manifest(b'')

    def release(self):
        course=json.loads((ROOT/'dist/course.json').read_bytes())
        course_body=json.dumps(course).encode()
        config=json.dumps({'lab':{'url':'','allowedOrigins':[],'embed':False}}).encode()
        info={'id':'smartkea-term-linux','sourceCommit':COMMIT,'sourceDirty':False,
              'courseSha256':v.sha(course_body),'modules':16,'lessons':48,'questions':96,
              'steps':194,'labConfigured':False}
        return info,course_body,config

    def test_metadata_matches_actual_bytes_counts_and_endpoint(self):
        info,course,config=self.release()
        self.assertEqual(v.verify_documents(info,course,config,COMMIT)['steps'],194)
        for field,value in [('sourceCommit','b'*40),('sourceDirty',True),
                            ('courseSha256','0'*64),('lessons',47),('labConfigured',True)]:
            with self.subTest(field=field),self.assertRaises(ValueError):
                v.verify_documents(dict(info,**{field:value}),course,config,COMMIT)

    def transport(self):
        info,course,config=self.release()
        files={name:b'asset' for name in v.REQUIRED}
        files.update({'course.json':course,'config.json':config,
                      'build-info.json':json.dumps(info).encode()})
        files['SHA256SUMS.txt']=''.join(v.sha(data)+'  '+name+'\n' for name,data in sorted(files.items())).encode()
        def reader(url):
            name=url.split(v.PREFIX,1)[1] if v.PREFIX in url else ''
            name=name or 'index.html'
            return {'status':200 if name in files else 404,'body':files.get(name,b'missing'),
                    'url':url,'headers':dict(HEADERS)}
        return files,reader

    def test_complete_verification_includes_both_entries_and_404(self):
        files,reader=self.transport();requests=[]
        def recorded(url):requests.append(url);return reader(url)
        self.assertEqual(v.check(COMMIT,recorded)['status'],'passed')
        self.assertIn('https://smartkea.com'+v.PREFIX[:-1],requests)
        self.assertIn(v.BASE+'__term_release_check_missing__',requests)
        self.assertEqual(requests.count(v.BASE+'build-info.json'),3)

    def test_tamper_fails_instead_of_claiming_deployment_success(self):
        files,reader=self.transport();files['assets/app.js']=b'tampered'
        with self.assertRaises(ValueError):v.check(COMMIT,reader)

    def test_soft_404_fails(self):
        _,reader=self.transport()
        def soft(url):
            result=reader(url)
            if result['status']==404:result['status']=200
            return result
        with self.assertRaises(ValueError):v.check(COMMIT,soft)

    def test_security_headers_accept_case_insensitive_names(self):
        v.verify_security_headers({k.upper(): val for k,val in HEADERS.items()})

    def test_csp_rejects_substring_matches_and_script_overrides(self):
        csp = HEADERS['Content-Security-Policy']
        cases = [csp.replace("default-src 'self'", "default-src 'self' https://external.example"),
                 csp.replace("script-src 'self'", "script-src *"),
                 csp.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'"),
                 csp + "; script-src-elem *", csp + "; script-src-attr 'unsafe-inline'",
                 csp + "; script-src *", csp + ", default-src *"]
        for policy in cases:
            with self.subTest(policy=policy), self.assertRaises(ValueError):
                v.verify_security_headers(dict(HEADERS, **{'Content-Security-Policy':policy}))

    def test_required_headers_cannot_disappear(self):
        for name in HEADERS:
            with self.subTest(name=name), self.assertRaises(ValueError):
                v.verify_security_headers({k:val for k,val in HEADERS.items() if k != name})
        for cache in ('public', 'public, no-cache', 'public, no-transform'):
            with self.subTest(cache=cache), self.assertRaises(ValueError):
                v.verify_security_headers(dict(HEADERS, **{'Cache-Control':cache}))

    def test_manual_entries_and_missing_routes_require_headers_too(self):
        for path in ('manual.html', '', '__term_release_check_missing__'):
            _,reader=self.transport()
            def weakened(url):
                response=reader(url)
                if url == v.BASE + path:
                    response['headers'].pop('Content-Security-Policy')
                return response
            with self.subTest(path=path), self.assertRaises(ValueError):
                v.check(COMMIT,weakened)

    def test_verification_records_all_four_entry_urls(self):
        _,reader=self.transport()
        result=v.check(COMMIT,reader)
        self.assertEqual(len(result['entries']),4)
        self.assertEqual({entry['requestedUrl'] for entry in result['entries']},
                         {'https://'+host+v.PREFIX[:-1]+slash for host in v.HOSTS for slash in ('','/')})
