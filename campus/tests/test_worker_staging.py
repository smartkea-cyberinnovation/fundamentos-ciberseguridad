"""Publication regressions: byte preservation, nested 404 and provenance."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build
from publication import PUBLIC_BASE_PATH, PUBLIC_URL
from stage_worker import stage, validate_staging


class WorkerStagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name)/'worker-dist'
        self.report = stage(self.output)
        self.campus = self.output/PUBLIC_BASE_PATH.strip('/')

    def test_public_content_bytes_preserved(self):
        for name in ('index.html','course.json','course.en.json','lectura.html','reading.en.html',
                     'assets/app.js','assets/styles.css','descargas/kit-laboratorio.zip'):
            self.assertEqual((build.HERE/'dist'/name).read_bytes(),(self.campus/name).read_bytes())
        self.assertFalse((self.output/'index.html').exists())
        self.assertFalse((self.output/'course.json').exists())

    def test_nested_404_and_headers(self):
        page = (self.campus/'404.html').read_text()
        self.assertIn('href="'+PUBLIC_BASE_PATH+'assets/styles.css"',page)
        self.assertIn(PUBLIC_BASE_PATH+'?lang=en#/temario',page)
        self.assertNotIn('href="/assets/',page)
        self.assertTrue((self.output/'_headers').is_file())
        self.assertFalse((self.campus/'_headers').exists())

    def test_metadata_keeps_source_and_adds_location(self):
        source = json.loads((build.HERE/'dist/build-info.json').read_text())
        info = json.loads((self.campus/'build-info.json').read_text())
        self.assertEqual(info['sourceCommit'],source['sourceCommit'])
        self.assertEqual(info['publicUrl'],PUBLIC_URL)
        self.assertEqual(info['publicBasePath'],PUBLIC_BASE_PATH)
        self.assertEqual(validate_staging(self.output)['status'],'passed')

    def test_changed_content_is_rejected(self):
        (self.campus/'course.json').write_text('{}')
        with self.assertRaises(ValueError):validate_staging(self.output)

    def test_unknown_output_is_not_removed(self):
        other = Path(self.temporary.name)/'other';other.mkdir()
        (other/'keep.txt').write_text('keep')
        with self.assertRaises(ValueError):stage(other)
        self.assertEqual((other/'keep.txt').read_text(),'keep')


if __name__ == '__main__':
    unittest.main()
