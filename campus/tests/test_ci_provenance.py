"""Generated CI reports are outputs, not untracked source inputs."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from provenance import source_commit

class CIProvenanceTests(unittest.TestCase):
    def test_real_campus_ignore_keeps_generated_reports_out_of_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);campus=root/'campus';campus.mkdir()
            (campus/'.gitignore').write_bytes((Path(__file__).resolve().parents[1]/'.gitignore').read_bytes())
            def git(*args):
                return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,text=True).stdout.strip()
            git('init','-q');git('add','.')
            git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture')
            qa=campus/'qa';qa.mkdir()
            (qa/'compiler.log').write_text('generated test result')
            (qa/'release.json').write_text('{}')
            self.assertEqual(git('status','--porcelain'),'')
            self.assertEqual(source_commit(root),git('rev-parse','HEAD'))

if __name__=='__main__':unittest.main()
