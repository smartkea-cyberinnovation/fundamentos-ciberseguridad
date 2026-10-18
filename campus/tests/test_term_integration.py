"""The new course must not weaken campus policy or capture unrelated routes."""
from pathlib import Path
from fnmatch import fnmatchcase
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
            'smartkea.com/fundamentos-ciberseguridad/term*',
            'www.smartkea.com/fundamentos-ciberseguridad/term*'])
        self.assertIn('term/content',cloudflare.check_config()['build']['watch_dir'])

    def test_routes_match_query_strings_on_the_entry_without_a_slash(self):
        # Cloudflare matches the whole request URL, including its query string.
        patterns=[r['pattern'] for r in cloudflare.check_config()['routes']]
        for host in ('smartkea.com','www.smartkea.com'):
            for suffix in ('','?ref=course','/','/?ref=course','/manual.html'):
                url=host+'/fundamentos-ciberseguridad/term'+suffix
                with self.subTest(url=url):
                    self.assertTrue(any(fnmatchcase(url,p) for p in patterns))
            for path in ('/','/contacto','/fundamentos-ciberseguridad/otro'):
                self.assertFalse(any(fnmatchcase(host+path,p) for p in patterns))

    def test_watcher_excludes_outputs_and_runtime_data(self):
        watched=[Path(p) for p in cloudflare.check_config()['build']['watch_dir']]
        for name in ('campus/qa/wrangler-local.log','campus/dist/course.json',
                     'campus/worker-dist/index.html','term/dist/course.json',
                     'term/.term-build-example/index.html','term/labs/workspace/note.txt',
                     'term/labs/secrets/token.json'):
            with self.subTest(path=name):
                self.assertFalse(any(Path(name).is_relative_to(root) for root in watched))

    def test_redirect_stays_inside_term(self):
        self.assertEqual(redirects(),'/fundamentos-ciberseguridad/term /fundamentos-ciberseguridad/term/ 308\n')


if __name__=='__main__':unittest.main()
