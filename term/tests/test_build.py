import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('term_test_builder',HERE/'build.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)


class CourseTests(unittest.TestCase):
    def test_complete_curriculum_and_shell_syntax(self):
        course=builder.collect();lessons=[l for m in course['modules'] for l in m['lessons']]
        self.assertEqual(len(lessons),48)
        self.assertEqual(sum(len(l['quiz']) for l in lessons),96)
        failures=[]
        for lesson in lessons:
            for i,step in enumerate(lesson['steps']):
                result=subprocess.run([step['shell'],'-n'],input=step['command'],text=True,capture_output=True,timeout=5)
                if result.returncode:failures.append((lesson['id'],i,result.stderr))
        self.assertEqual(failures,[],str(failures))

    def test_endpoint_default_and_exact_origin_controls(self):
        self.assertEqual(builder.lab_config({}),{'url':'','allowedOrigins':[],'embed':False})
        valid={'TERM_LAB_URL':'https://term.example.org/','TERM_LAB_ALLOWED_ORIGINS':'https://term.example.org','TERM_LAB_EMBED':'1'}
        lab=builder.lab_config(valid);self.assertIn('frame-src https://term.example.org',builder.headers(lab))
        for url in ['http://term.example.org/','https://term.example.org.evil.test/','https://user:secret@term.example.org/','https://term.example.org/?args=sh','https://term.example.org/#x']:
            with self.subTest(url=url),self.assertRaises(ValueError):builder.lab_config(dict(valid,TERM_LAB_URL=url))
        for origin in ['https://*.example.org','https://smartkea.com','https://term.example.org/','https://term.example.org\nframe-src *']:
            with self.subTest(origin=origin),self.assertRaises(ValueError):builder.lab_config(dict(valid,TERM_LAB_ALLOWED_ORIGINS=origin))

    def test_public_lab_inventory_excludes_local_data(self):
        files=builder.public_lab_files()
        self.assertGreater(len(files),15)
        for name,path in files:
            self.assertNotIn('/secrets/',name);self.assertNotEqual(path.name,'.env');self.assertFalse(path.is_symlink())

    def test_renderer_escapes_content(self):
        source='# Demo\n\n<script>alert(1)</script>\n\n```sh\nprintf x\n```\n'
        result=builder.markdown_doc(source,'test.md')
        self.assertNotIn('<script>',result);self.assertIn('&lt;script&gt;',result)
        self.assertIn('<pre><code>printf x',result)

    def test_release_manifest_detects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'dist'
            with patch.dict('os.environ',{},clear=True):builder.build(dest)
            self.assertEqual(builder.validate(dest)['lessons'],48)
            (dest/'course.json').write_text('{}')
            with self.assertRaises(ValueError):builder.validate(dest)


if __name__=='__main__':unittest.main()
