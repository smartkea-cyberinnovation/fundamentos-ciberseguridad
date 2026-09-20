import copy
import json
from pathlib import Path
import unittest
import generar


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.modules = json.loads(Path(generar.CATALOG).read_text(encoding='utf-8'))
        self.plan = generar.build(self.modules)

    def test_totals(self):
        self.assertEqual(self.plan['resumen'], {'sesiones': 240, 'laboratorios': 96, 'teoria_h': 168, 'practica_h': 312, 'total_h': 480})

    def test_unique_ids(self):
        for field in ('sesiones', 'laboratorios'):
            ids = [row['id'] for row in self.plan[field]]
            self.assertEqual(len(ids), len(set(ids)))

    def test_session_length(self):
        self.assertTrue(all(row['teoria_min'] + row['practica_min'] == 120 for row in self.plan['sesiones']))

    def test_lab_minutes(self):
        for lab in self.plan['laboratorios']:
            allocated = sum(part['minutos'] for row in self.plan['sesiones'] for part in row['laboratorios'] if part['id'] == lab['id'])
            self.assertEqual(allocated, lab['minutos'])

    def test_last_session(self):
        self.assertEqual(self.plan['sesiones'][-1]['laboratorios'], [{'id': 'L32C', 'minutos': 120}])

    def test_forward_dependency_rejected(self):
        changed = copy.deepcopy(self.modules)
        changed[0]['prerrequisitos'] = ['M32']
        with self.assertRaises(ValueError):
            generar.build(changed)

    def test_duplicate_module_rejected(self):
        changed = copy.deepcopy(self.modules)
        changed[1]['id'] = 'M01'
        with self.assertRaises(ValueError):
            generar.build(changed)

    def test_missing_module_rejected(self):
        with self.assertRaises(ValueError):
            generar.build(self.modules[:-1])


if __name__ == '__main__':
    unittest.main()
