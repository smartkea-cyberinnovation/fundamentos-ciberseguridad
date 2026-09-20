"""Offline regression for missing campus/dist on a fresh Workers checkout."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cloudflare

class WorkersBuildHookTests(unittest.TestCase):
    def test_hook_builds_only(self):
        config = cloudflare.check_config()
        self.assertEqual(config['build']['command'], 'python3 campus/cloudflare.py build')
        self.assertEqual(config['build']['cwd'], '.')
        self.assertNotIn('deploy', config['build']['command'])
        self.assertNotIn('npx', config['build']['command'])

    def check_invalid(self, mutate):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'wrangler.jsonc'
            config = cloudflare.check_config()
            mutate(config)
            path.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaises(ValueError):
                cloudflare.check_config(path)

    def test_missing_hook_rejected(self):
        self.check_invalid(lambda config: config.pop('build'))

    def test_recursive_hook_rejected(self):
        self.check_invalid(lambda config: config['build'].update(command='npx wrangler deploy'))

    def test_foreign_build_directory_rejected(self):
        self.check_invalid(lambda config: config['build'].update(cwd='src'))

    def test_apex_capture_rejected(self):
        self.check_invalid(lambda config: config.update(routes=[{'pattern':'smartkea.com/*','zone_name':'smartkea.com'}]))

    def test_extra_route_rejected(self):
        self.check_invalid(lambda config: config['routes'].append({'pattern':'smartkea.com/other/*','zone_name':'smartkea.com'}))

    def test_custom_domain_rejected(self):
        self.check_invalid(lambda config: config.update(routes=[{'pattern':'smartkea.com','custom_domain':True}]))

    def test_failed_compilation_never_validates_or_uploads(self):
        with patch.object(cloudflare, 'execute', side_effect=RuntimeError('build failed')) as execute:
            with patch.object(cloudflare, 'validate') as validate:
                with self.assertRaises(RuntimeError):
                    cloudflare.build_and_check()
                self.assertEqual(execute.call_count, 1)
                validate.assert_not_called()

if __name__ == '__main__':
    unittest.main()
