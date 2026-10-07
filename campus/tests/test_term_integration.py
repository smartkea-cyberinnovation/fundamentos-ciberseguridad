"""The new course must not weaken campus policy or capture unrelated routes."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cloudflare
from publication import PUBLIC_BASE_PATH
from term_integration import TERM_BASE,merged_headers,redirects


class TermIntegrationTests(unittest.TestCase):
    def test_routes_only_cover_requested_educational_paths(self):
        routes=cloudflare.check_config()['routes']
        self.assertEqual([r['pattern'] for r in routes],[
            'smartkea.com/introduccion-ciberseguridad/*',
            'smartkea.com/fundamentos-ciberseguridad/term/*',
            'smartkea.com/fundamentos-ciberseguridad/term'])
        self.assertIn('term',cloudflare.check_config()['build']['watch_dir'])

    def test_redirect_stays_inside_term(self):
        self.assertEqual(redirects(),'/fundamentos-ciberseguridad/term /fundamentos-ciberseguridad/term/ 308\n')


if __name__=='__main__':unittest.main()
