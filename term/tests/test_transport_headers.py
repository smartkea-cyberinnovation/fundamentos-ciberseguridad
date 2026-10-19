"""Keep the public course byte-verifiable without weakening its CSP."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('term_transport_builder', ROOT / 'term/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
spec = importlib.util.spec_from_file_location('term_transport_adapter', ROOT / 'campus/term_integration.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class TransportHeadersTests(unittest.TestCase):
    def test_no_transform_retains_revalidation_and_strict_csp(self):
        for lab in ({'url':'','allowedOrigins':[],'embed':False},
                    {'url':'https://term.example.org/','allowedOrigins':['https://term.example.org'],'embed':True}):
            with self.subTest(embed=lab['embed']):
                headers = builder.headers(lab)
                self.assertIn('Cache-Control: public, no-cache, no-transform', headers)
                self.assertIn("script-src 'self'", headers)
                self.assertNotIn('unsafe-inline', headers)
                self.assertNotIn('cloudflareinsights.com', headers)
                self.assertIn("frame-ancestors 'none'", headers)

    def test_campus_policy_is_unchanged_and_term_is_scoped(self):
        original = "/*\n  Cache-Control: no-cache\n  X-Content-Type-Options: nosniff\n"
        from unittest.mock import patch
        with patch.object(Path, 'read_text', return_value=builder.headers({'allowedOrigins':[], 'embed':False})):
            merged = adapter.merged_headers(original, '/introduccion-ciberseguridad/')
        prefix, term = merged.split('\n/fundamentos-ciberseguridad/term/*\n', 1)
        self.assertEqual(prefix, original.replace('/*\n', '/introduccion-ciberseguridad/*\n', 1))
        self.assertNotIn('no-transform', prefix)
        self.assertIn('Cache-Control: public, no-cache, no-transform', term)
