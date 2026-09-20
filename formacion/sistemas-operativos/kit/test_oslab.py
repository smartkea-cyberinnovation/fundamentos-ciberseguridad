"""Pruebas reales con temporales. Sin acceso a servicios externos."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import oslab


class OfflineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'caso con espacios'
        oslab.init_workspace(str(self.root))

    def replace_json(self, name, value):
        (self.root / name).write_text(oslab.dump(value), encoding='utf-8')

    def test_init_does_not_overwrite(self):
        with self.assertRaises(FileExistsError): oslab.init_workspace(str(self.root))

    def test_marker_required(self):
        (self.root / '.oslab').write_text('otro\n')
        with self.assertRaises(ValueError): oslab.root_checked(str(self.root))

    def test_manifest_expected_count(self):
        self.assertEqual(oslab.manifest(self.root)['count'], 8)

    def test_manifest_expected_bytes(self):
        self.assertEqual(oslab.manifest(self.root)['total_bytes'], 62)

    def test_hidden_file_included(self):
        self.assertIn('.nota.txt', [x['name'] for x in oslab.manifest(self.root)['files']])

    def test_hash_lf_crlf_differ(self):
        rows = {x['name']: x['sha256'] for x in oslab.manifest(self.root)['files']}
        self.assertNotEqual(rows['lineas-lf.txt'], rows['lineas-crlf.txt'])

    def test_empty_file_hash(self):
        rows = {x['name']: x['sha256'] for x in oslab.manifest(self.root)['files']}
        self.assertEqual(rows['vacio.txt'], 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def test_repeatable(self):
        self.assertEqual(oslab.manifest(self.root), oslab.manifest(self.root))

    def test_folder_rejected(self):
        (self.root / 'datos' / 'sub').mkdir()
        with self.assertRaises(ValueError): oslab.manifest(self.root)

    def test_file_limit(self):
        (self.root / 'datos' / 'grande').write_bytes(b'x' * (oslab.LIMIT + 1))
        with self.assertRaises(ValueError): oslab.manifest(self.root)

    def test_symlink_rejected(self):
        try: (self.root / 'datos' / 'enlace').symlink_to(self.root / 'eventos.json')
        except OSError as exc: self.skipTest(str(exc))
        with self.assertRaises(ValueError): oslab.manifest(self.root)

    def test_hardlink_rejected(self):
        try: os.link(self.root / 'eventos.json', self.root / 'datos' / 'enlace')
        except OSError as exc: self.skipTest(str(exc))
        with self.assertRaises(ValueError): oslab.manifest(self.root)

    def test_root_symlink_rejected(self):
        link = Path(self.tmp.name) / 'alias'
        try: link.symlink_to(self.root, target_is_directory=True)
        except OSError as exc: self.skipTest(str(exc))
        with self.assertRaises(ValueError): oslab.root_checked(str(link))

    def test_duplicate_json_key(self):
        p = self.root / 'prueba.json'; p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError): oslab.load_json(p)

    def test_non_finite_json(self):
        p = self.root / 'prueba.json'; p.write_text('{"a":NaN}')
        with self.assertRaises(ValueError): oslab.load_json(p)

    def test_bom_accepted(self):
        p = self.root / 'prueba.json'; p.write_text('{"a":1}', encoding='utf-8-sig')
        self.assertEqual(oslab.load_json(p), {'a': 1})

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError): oslab.parse_time('2026-09-14T10:00:00')

    def test_timezone_normalization(self):
        self.assertEqual(oslab.parse_time('2026-09-14T10:00:00+02:00'), oslab.parse_time('2026-09-14T08:00:00Z'))

    def test_timeline_original_preserved(self):
        item = oslab.timeline(self.root)[0]
        self.assertEqual(item['timestamp_original'], '2026-09-14T10:00:00+02:00')
        self.assertEqual(item['timestamp_utc'], '2026-09-14T08:00:00+00:00')

    def test_timeline_order(self):
        self.assertEqual([x['id'] for x in oslab.timeline(self.root)], ['E%02d' % n for n in range(1, 9)])

    def test_duplicate_event(self):
        rows = oslab.load_json(self.root / 'eventos.json'); rows.append(rows[0])
        self.replace_json('eventos.json', rows)
        with self.assertRaises(ValueError): oslab.timeline(self.root)

    def test_exact_matches(self):
        matches = oslab.match_indicators(self.root)['matches']
        self.assertEqual([(x['event_id'], x['type']) for x in matches], [('E02','domain'), ('E02','ip'), ('E04','sha256'), ('E08','domain')])

    def test_negative_subdomain(self):
        self.assertNotIn('E07', [x['event_id'] for x in oslab.match_indicators(self.root)['matches']])

    def test_negative_similar_ip(self):
        self.assertNotIn('E03', [x['event_id'] for x in oslab.match_indicators(self.root)['matches']])

    def test_invalid_indicators(self):
        for kind, value in [('domain','https://ejemplo.test'), ('sha256','0'*63), ('ip','999.2.3.4'), ('domain','-mal.test')]:
            with self.subTest(kind=kind, value=value):
                with self.assertRaises(ValueError): oslab.normalize(kind, value)

    def test_indicator_deduplication(self):
        rows = oslab.load_json(self.root / 'indicadores.json'); rows.append(rows[0])
        self.replace_json('indicadores.json', rows)
        self.assertEqual(oslab.match_indicators(self.root)['indicators_unique'], 3)

    def test_no_network_or_input_changes(self):
        before = (self.root / 'eventos.json').read_bytes()
        with patch.object(socket, 'socket', side_effect=AssertionError('No se permite red')):
            oslab.manifest(self.root); oslab.timeline(self.root); oslab.match_indicators(self.root)
        self.assertEqual(before, (self.root / 'eventos.json').read_bytes())

    def test_review_never_certifies_truth(self):
        result = oslab.review_shape(self.root)
        self.assertTrue(result['structurally_valid']); self.assertFalse(result['semantically_verified'])

    def test_review_unknown_reference(self):
        self.replace_json('respuesta-ia.json', {'findings': [{'kind':'fact','text':'texto','evidence_ids':['E999']}]})
        with self.assertRaises(ValueError): oslab.review_shape(self.root)

    def test_review_extra_action_field(self):
        self.replace_json('respuesta-ia.json', {'findings': [], 'actions': []})
        with self.assertRaises(ValueError): oslab.review_shape(self.root)

    def test_cli_error_json(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err): code = oslab.main(['manifest', str(self.root / 'ausente')])
        self.assertEqual(code, 2); self.assertEqual(json.loads(err.getvalue())['status'], 'error')

    @unittest.skipUnless(shutil.which('bash'), 'Bash no disponible')
    def test_bash_native_matches(self):
        proc = subprocess.run(['bash', str(Path(__file__).with_name('resumen.bash')), str(self.root)], capture_output=True, text=True, timeout=5)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {'count':8, 'total_bytes':62})

    @unittest.skipUnless(shutil.which('bash'), 'Bash no disponible')
    def test_bash_missing_arguments(self):
        proc = subprocess.run(['bash', str(Path(__file__).with_name('resumen.bash'))], capture_output=True, timeout=5)
        self.assertEqual(proc.returncode, 2)

    @unittest.skipUnless(shutil.which('bash'), 'Bash no disponible')
    def test_bash_rejects_wrong_marker(self):
        (self.root / '.oslab').write_text('incorrecto\n')
        proc = subprocess.run(['bash', str(Path(__file__).with_name('resumen.bash')), str(self.root)], capture_output=True, timeout=5)
        self.assertEqual(proc.returncode, 2)


if __name__ == '__main__': unittest.main()
