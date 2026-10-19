"""C99 classroom case acceptance. Only synthetic data; no PHP or network execution."""
from __future__ import annotations

import copy
from datetime import timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / 'formacion/casos/c99-forense'
SCRIPT = CASE / 'herramientas/forense.py'
spec = importlib.util.spec_from_file_location('c99_classroom_forense', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
sys.path.insert(0, str(ROOT / 'campus'))
from operations import related_reading


class C99CaseTests(unittest.TestCase):
    def scenario(self):
        return json.loads((CASE / 'evidencias/escenario.json').read_text(encoding='utf-8'))

    def test_synthetic_dataset_is_explicit(self):
        data = self.scenario()
        self.assertIs(data['synthetic'], True)
        self.assertEqual(len(data['events']), 14)
        self.assertIn('packet capture', data['scope']['missing'])

    def test_timeline_order_and_equal_timestamps(self):
        result = helper.timeline(self.scenario())
        self.assertEqual([row['id'] for row in result['events']],
                         ['E01','E02','E03','E14','E04','E05','E06','E07','E08','E09','E10','E11','E12','E13'])
        self.assertEqual(result['equal_timestamps']['2026-10-01T09:01:00Z'], ['E04','E05'])
        e5 = next(row for row in result['events'] if row['id'] == 'E05')
        self.assertEqual(e5['time_original'], '2026-10-01T11:01:00+02:00')

    def test_timeline_does_not_mutate_input(self):
        data = self.scenario()
        before = copy.deepcopy(data)
        helper.timeline(data)
        self.assertEqual(data, before)

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            helper.parse_time('2026-10-01T09:00:00')

    def test_timezone_normalization(self):
        stamp = helper.parse_time('2026-10-01T11:01:00+02:00')
        self.assertEqual(stamp.hour, 9)
        self.assertEqual(stamp.tzinfo, timezone.utc)

    def test_duplicate_event_rejected(self):
        data = self.scenario()
        data['events'].append(copy.deepcopy(data['events'][0]))
        with self.assertRaises(ValueError):
            helper.timeline(data)

    def test_non_synthetic_data_rejected(self):
        for marker in (False, 'true', 1, None):
            with self.subTest(marker=marker):
                data = self.scenario()
                data['synthetic'] = marker
                with self.assertRaises(ValueError):
                    helper.timeline(data)

    def test_invalid_event_details_rejected(self):
        data = self.scenario()
        data['events'][0]['details'] = 'not an object'
        with self.assertRaises(ValueError):
            helper.timeline(data)

    def test_manifest_verifies_classroom_evidence(self):
        directory = CASE / 'evidencias'
        baseline = helper.manifest(directory)
        self.assertEqual(baseline['file_count'], 4)
        self.assertTrue(helper.verify(directory, baseline)['verified'])

    def test_changed_missing_and_extra_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.txt').write_text('alpha')
            (root / 'b.txt').write_text('beta')
            baseline = helper.manifest(root)
            (root / 'a.txt').write_text('changed')
            (root / 'b.txt').unlink()
            (root / 'c.txt').write_text('extra')
            result = helper.verify(root, baseline)
            self.assertFalse(result['verified'])
            self.assertEqual(result['changed'], ['a.txt'])
            self.assertEqual(result['missing'], ['b.txt'])
            self.assertEqual(result['extra'], ['c.txt'])

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'real.txt').write_text('real')
            try:
                (root / 'link.txt').symlink_to('real.txt')
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unavailable on this platform')
            with self.assertRaises(ValueError):
                helper.manifest(root)

    def test_manifest_path_traversal_rejected(self):
        baseline = helper.manifest(CASE / 'evidencias')
        baseline['files'][0]['path'] = '../outside.txt'
        with self.assertRaises(ValueError):
            helper.verify(CASE / 'evidencias', baseline)

    def test_duplicate_manifest_entry_rejected(self):
        baseline = helper.manifest(CASE / 'evidencias')
        baseline['files'].append(copy.deepcopy(baseline['files'][0]))
        with self.assertRaises(ValueError):
            helper.verify(CASE / 'evidencias', baseline)

    def test_oversized_input_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'large.txt'
            with path.open('wb') as stream:
                stream.truncate(helper.MAX_FILE_BYTES + 1)
            with self.assertRaises(ValueError):
                helper.read_regular(path)

    def test_cli_outputs_timeline_and_input_hash(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'timeline', str(CASE/'evidencias/escenario.json')],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['event_count'], 14)
        self.assertRegex(payload['input_sha256'], r'^[0-9a-f]{64}$')

    def test_cli_mismatch_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'evidence'
            root.mkdir()
            path = root / 'a.txt'
            path.write_text('first')
            baseline = Path(tmp) / 'manifest.json'
            baseline.write_text(json.dumps(helper.manifest(root)))
            path.write_text('second')
            result = subprocess.run([sys.executable, str(SCRIPT), 'verify', str(root), str(baseline)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(json.loads(result.stdout)['verified'])

    def test_self_check_has_twelve_valid_answers(self):
        data = json.loads((CASE/'preguntas.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['questions']), 12)
        self.assertEqual(len({q['id'] for q in data['questions']}), 12)
        for question in data['questions']:
            self.assertEqual(len(question['options']), 4)
            self.assertIn(question['correct_index'], range(4))
            self.assertTrue(question['explanation'])

    def test_guides_cover_all_ten_activities(self):
        for name in ('PRACTICA.md', 'PRACTICA.en.md'):
            raw = (CASE/name).read_text(encoding='utf-8')
            for index in range(1, 11):
                self.assertIn(f'## A{index:02}', raw)
        for name in ('DOCENTE.md','INFORME.md','FUENTES.md'):
            self.assertTrue((CASE/name).is_file())

    def test_bilingual_module_links_preserve_previous_readings(self):
        for mid in ('M27','M28','M29'):
            for language, filename in (('es','PRACTICA.md'),('en','PRACTICA.en.md')):
                raw = related_reading(mid, language)
                self.assertIn('#/recurso/D25', raw)
                self.assertIn('formacion/casos/c99-forense/'+filename, raw)
        self.assertNotIn('C99-DFIR', related_reading('M07', 'es'))

    def test_lab_configuration_is_ephemeral_and_restricted(self):
        raw = (CASE/'compose.laboratorio.yaml').read_text(encoding='utf-8')
        for marker in ('network_mode: none','read_only: true','10001:10001','no-new-privileges:true','cap_drop:','ALL'):
            self.assertIn(marker, raw)
        self.assertNotIn('ports:', raw)
        self.assertNotIn('docker.sock', raw)
        self.assertNotIn('privileged: true', raw)
        self.assertNotIn('volumes:', raw)

    def test_no_executable_php_or_secret_files_in_case(self):
        for path in CASE.rglob('*'):
            if path.is_file():
                self.assertNotEqual(path.suffix.lower(), '.php')
                self.assertNotIn(path.name, ('.env','id_rsa','id_ed25519'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
