"""Offline contracts that prevent runner drift and duplicate release work."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ReleaseWorkflowTests(unittest.TestCase):
    def test_reviewed_release_runner_is_not_a_moving_alias(self):
        for name in ('campus', 'os-study', 'term', 'cloudflare', 'workers-clean-build'):
            text = (ROOT/f'.github/workflows/{name}.yml').read_text()
            runners = re.findall(r'^\s*runs-on:\s*(\S+)', text, re.M)
            with self.subTest(workflow=name):
                self.assertTrue(runners)
                self.assertEqual(set(runners), {'ubuntu-24.04'})

    def test_term_validates_toolchain_changes_on_push_and_pr(self):
        text = (ROOT/'.github/workflows/term.yml').read_text()
        self.assertEqual(text.count("'campus/tooling/**'"), 2)
        self.assertEqual(text.count("'campus/cloudflare.py'"), 2)
        self.assertIn('--attempts 60', text)
        self.assertIn('needs: [course, labs]', text)
        self.assertIn("github.ref == 'refs/heads/main'", text)

    def test_campus_compiles_catalogs_once_before_js_consumers(self):
        text = (ROOT/'.github/workflows/campus.yml').read_text()
        self.assertEqual(text.count('python3 campus/build.py'), 1)
        self.assertLess(text.index('python3 campus/build.py'), text.index('node --test'))
        for evidence in ('campus/qa/build.json', 'campus/qa/release.json', 'browser_routes.py'):
            self.assertIn(evidence, text)


if __name__ == '__main__': unittest.main()
