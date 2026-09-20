"""Real temporary Git repositories: no user configuration or external network."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from provenance import source_commit
import build

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.git('init','-q')
        (self.root/'tracked.md').write_text('original')
        (self.root/'.gitignore').write_text('generated/\n')
        self.git('add','tracked.md','.gitignore')
        self.git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture')
    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.root,check=True,capture_output=True,text=True).stdout.strip()
    def test_clean_checkout_records_real_head(self):
        self.assertEqual(source_commit(self.root),self.git('rev-parse','HEAD'))
    def test_tracked_edit_has_no_source_commit(self):
        (self.root/'tracked.md').write_text('changed')
        self.assertIsNone(source_commit(self.root))
    def test_new_kit_input_has_no_source_commit(self):
        folder=self.root/'formacion/sistemas-operativos/kit';folder.mkdir(parents=True)
        (folder/'new.py').write_text('print("fixture")')
        self.assertIsNone(source_commit(self.root))
    def test_new_unicode_filename_has_no_source_commit(self):
        (self.root/'lección con espacios.md').write_text('fixture')
        self.assertIsNone(source_commit(self.root))
    def test_ignored_output_does_not_change_checkout(self):
        folder=self.root/'generated';folder.mkdir();(folder/'build.log').write_text('output')
        self.assertEqual(source_commit(self.root),self.git('rev-parse','HEAD'))
    def test_no_git_has_no_source_commit(self):
        shutil.rmtree(self.root/'.git')
        self.assertIsNone(source_commit(self.root))
    def test_ignored_laboratory_input_is_not_attributed(self):
        course=self.root/'formacion/sistemas-operativos';course.mkdir(parents=True)
        (course/'.gitignore').write_text('mi-laboratorio*/\n')
        self.git('add','.');self.git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','ignore fixture')
        local=course/'kit/mi-laboratorio-local';local.mkdir(parents=True)
        (local/'notes.md').write_text('private local fixture')
        self.assertEqual(self.git('status','--porcelain'),'')
        self.assertIsNone(source_commit(self.root))
    def test_ignored_lesson_input_is_not_attributed(self):
        course=self.root/'formacion/sistemas-operativos';course.mkdir(parents=True)
        (course/'.gitignore').write_text('lecciones/local*.md\n')
        self.git('add','.');self.git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','ignore fixture')
        local=course/'lecciones';local.mkdir();(local/'local.md').write_text('fixture')
        self.assertIsNone(source_commit(self.root))
    def test_build_checks_before_collecting_or_writing(self):
        order=[]
        with patch.object(build,'source_commit',side_effect=lambda root:order.append('provenance')):
            with patch.object(build,'collect',side_effect=lambda:(_ for _ in ()).throw(ValueError('stop before output'))):
                with self.assertRaises(ValueError):build.build()
        self.assertEqual(order,['provenance'])

if __name__=='__main__':unittest.main()
