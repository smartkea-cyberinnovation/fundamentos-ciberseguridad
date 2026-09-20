import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from release_inputs import KIT_FILES, public_kit_files
import build

class PublicKitTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name in KIT_FILES:(self.root/name).write_text('fixture')
    def test_only_declared_files(self):
        self.assertEqual({p.name for p in public_kit_files(self.root)},set(KIT_FILES))
    def test_local_workspace_is_excluded(self):
        local=self.root/'mi-laboratorio-local';local.mkdir();(local/'notes.md').write_text('private')
        (self.root/'.env.py').write_text('private')
        self.assertEqual(len(public_kit_files(self.root)),len(KIT_FILES))
    def test_missing_declared_file_fails(self):
        (self.root/KIT_FILES[0]).unlink()
        with self.assertRaises(ValueError):public_kit_files(self.root)
    def test_symlink_fails(self):
        name=KIT_FILES[0];(self.root/name).unlink();(self.root/name).symlink_to(self.root/KIT_FILES[1])
        with self.assertRaises(ValueError):public_kit_files(self.root)
    def test_oversized_file_fails(self):
        (self.root/KIT_FILES[0]).write_bytes(b'x'*1_000_001)
        with self.assertRaises(ValueError):public_kit_files(self.root)
    def test_generated_download_contains_exact_inventory(self):
        build.build()
        with zipfile.ZipFile(build.HERE/'dist/descargas/kit-laboratorio.zip') as archive:
            self.assertEqual(set(archive.namelist()),{'kit/'+x for x in KIT_FILES})

if __name__=='__main__':unittest.main()
