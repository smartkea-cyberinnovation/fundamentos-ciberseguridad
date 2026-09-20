import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from check_release import validate
import build
class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build()
    def test_valid_bundle(self):
        out=validate(build.HERE/'dist',build.HERE/'pages-ready.zip')
        self.assertEqual(out['status'],'passed')
        self.assertEqual(out['labs'],96)
    def test_public_resource_ids_preserved(self):
        data=build.collect()
        self.assertEqual(data['resources'][0]['id'],'D01')
        self.assertIn('Laboratorio',data['resources'][0]['title'])
        self.assertEqual(data['resources'][19]['title'],'Cómo estudiar: teoría, práctica y evidencia')
    def test_tampered_bundle_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/'dist';shutil.copytree(build.HERE/'dist',target)
            (target/'index.html').write_text('tampered')
            with self.assertRaises(ValueError):validate(target,build.HERE/'pages-ready.zip')
    def test_missing_asset_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/'dist';shutil.copytree(build.HERE/'dist',target)
            (target/'assets/navigation.js').unlink()
            with self.assertRaises(ValueError):validate(target,build.HERE/'pages-ready.zip')
