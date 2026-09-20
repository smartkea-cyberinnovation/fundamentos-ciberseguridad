"""Local HTTP delivery checks. Not a rendered-browser or Cloudflare runtime test."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
from threading import Thread
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from serve import Handler
class DeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build();cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(build.HERE/'dist')))
        Thread(target=cls.server.serve_forever,daemon=True).start();cls.base=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
    def test_home_has_strict_headers(self):
        with urlopen(self.base,timeout=4) as r:
            self.assertEqual(r.status,200);self.assertIn("script-src 'self'",r.headers['Content-Security-Policy'])
            self.assertEqual(r.headers['X-Content-Type-Options'],'nosniff');self.assertEqual(r.headers['Referrer-Policy'],'no-referrer')
    def test_both_catalogues_available_over_http(self):
        for path,lang in [('course.json','es'),('course.en.json','en')]:
            with urlopen(self.base+'/'+path,timeout=4) as r:
                data=json.load(r);self.assertEqual(data['language'],lang);self.assertEqual(len(data['modules']),32)
    def test_both_reading_pages_available(self):
        for path,lang in [('lectura.html','es'),('reading.en.html','en')]:
            with urlopen(self.base+'/'+path,timeout=4) as r:
                html=r.read().decode();self.assertIn('lang="'+lang+'"',html);self.assertIn('id="M32"',html)
    def test_portable_script_is_javascript(self):
        with urlopen(self.base+'/assets/portable.js',timeout=4) as r:self.assertIn('javascript',r.headers['Content-Type'])
    def test_source_not_exposed(self):
        with self.assertRaises(HTTPError) as ctx:urlopen(self.base+'/build.py',timeout=4)
        self.assertEqual(ctx.exception.code,404)
    def test_unknown_path_not_successful_html(self):
        with self.assertRaises(HTTPError) as ctx:urlopen(self.base+'/missing.json',timeout=4)
        self.assertEqual(ctx.exception.code,404)
if __name__=='__main__':unittest.main()
