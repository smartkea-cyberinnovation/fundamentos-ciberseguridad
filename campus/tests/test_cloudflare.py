"""Deployment contracts; all unit tests are offline and never publish."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cloudflare

class CloudflareTests(unittest.TestCase):
    def test_static_configuration(self):
        cfg=cloudflare.check_config()
        self.assertNotIn('main',cfg)
        self.assertNotIn('services',cfg)
        self.assertEqual(cfg['assets']['directory'],'./campus/worker-dist')
        self.assertEqual(cfg['routes'],cloudflare.PRODUCTION_ROUTES)
        self.assertTrue(cfg['workers_dev']);self.assertTrue(cfg['preview_urls'])
    def test_foreign_binding_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'wrangler.jsonc'; cfg=cloudflare.check_config()
            cfg['services']=[{'binding':'WORKER_SELF_REFERENCE','service':'frontend'}]
            path.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):cloudflare.check_config(path)
    def test_wrong_assets_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'wrangler.jsonc';cfg=cloudflare.check_config()
            cfg['assets']['directory']='.open-next/assets';path.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):cloudflare.check_config(path)
    def test_plan_never_builds_or_uploads(self):
        with patch.object(cloudflare,'execute') as execute:
            self.assertEqual(cloudflare.run('plan'),0);execute.assert_not_called()
    def test_production_command(self):
        args=cloudflare.wrangler_args('deploy')
        self.assertIn('deploy',args);self.assertNotIn('versions',args)
        self.assertIn('wrangler@4.132.0',args)
        self.assertEqual(args[-1],str(cloudflare.CONFIG))
    def test_preview_not_promoted(self):
        args=cloudflare.wrangler_args('preview')
        self.assertIn('versions',args);self.assertIn('upload',args);self.assertNotIn('deploy',args)
    def test_dry_run_cannot_upload(self):
        self.assertIn('--dry-run',cloudflare.wrangler_args('dry-run'))
    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):cloudflare.wrangler_args('exec arbitrary')
    def test_failed_config_prevents_wrangler(self):
        with patch.object(cloudflare,'check_config',side_effect=ValueError('bad configuration')):
            with patch.object(cloudflare,'execute') as execute:
                with self.assertRaises(ValueError):cloudflare.run('deploy')
                execute.assert_not_called()
    def test_build_only_no_npx(self):
        with patch.object(cloudflare,'build_and_check') as build:
            with patch.object(cloudflare,'execute') as execute:
                self.assertEqual(cloudflare.run('build'),0)
                build.assert_called_once();execute.assert_not_called()
    def test_wrapper_delegates_one_build_to_wrangler(self):
        with patch.object(cloudflare,'build_and_check') as build:
            with patch.object(cloudflare.shutil,'which',return_value='/usr/bin/npx'):
                with patch.object(cloudflare,'execute') as execute:
                    cloudflare.run('preview')
        build.assert_not_called();execute.assert_called_once()
        self.assertIn('versions',execute.call_args.args[0])
    def test_commands_never_use_shell(self):
        with patch.object(cloudflare.subprocess,'run') as run:
            cloudflare.execute(['python3','build.py'])
            self.assertIs(run.call_args.kwargs['shell'],False)
            self.assertTrue(run.call_args.kwargs['check'])
            self.assertEqual(run.call_args.kwargs['cwd'],cloudflare.ROOT)
    def test_new_resources_do_not_shift_old_links(self):
        import build
        data=build.collect();self.assertEqual(data['resources'][19]['id'],'D20')
        self.assertTrue(data['resources'][19]['title'].startswith('Cómo estudiar'))
        self.assertEqual(data['resources'][20]['id'],'D21')
        self.assertIn('despliegue',data['resources'][20]['title'])

if __name__=='__main__':unittest.main()
