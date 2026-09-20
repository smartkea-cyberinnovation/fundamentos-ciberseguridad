"""Bounded tests for the reference validator; no host administration or networking."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("reference_validation", ROOT / "validar.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ReferenceValidationTests(unittest.TestCase):
    def setUp(self):
        self.risk = validator.read_json(ROOT / "riesgo-ejemplo.json")
        self.areas = validator.read_json(ROOT / "catalogo.json")["areas"]

    def test_complete_reference(self):
        result = validator.validate_reference(ROOT)
        self.assertEqual(result["proposed_units"], 108)
        self.assertEqual(result["glossary_entries"], 110)

    def test_exact_risk_example(self):
        result = validator.validate_risk(self.risk)
        self.assertEqual(validator.Decimal(result["target"]), validator.Decimal("13440"))

    def test_rejects_total_instead_of_incremental_benefit(self):
        self.risk["incremental_decision"]["expected_annual_reduction_from_current"] = "34560"
        with self.assertRaises(ValueError):
            validator.validate_risk(self.risk)

    def test_rejects_impossible_reduction(self):
        self.risk["target"]["frequency_reduction_from_inherent"] = "1.2"
        with self.assertRaises(ValueError):
            validator.validate_risk(self.risk)

    def test_rejects_non_finite_input(self):
        self.risk["inherent"]["frequency"] = "Infinity"
        with self.assertRaises(ValueError):
            validator.validate_risk(self.risk)

    def test_rejects_bad_sensitivity(self):
        self.risk["sensitivity"]["target_loss_bounds"][0] = "3361"
        with self.assertRaises(ValueError):
            validator.validate_risk(self.risk)

    def test_acyclic_prerequisites(self):
        validator.validate_graph(self.areas)

    def test_rejects_cycle(self):
        graph = copy.deepcopy(self.areas)
        graph[0]["prerequisites"] = ["A02"]
        with self.assertRaises(ValueError):
            validator.validate_graph(graph)

    def test_rejects_unknown_prerequisite(self):
        graph = copy.deepcopy(self.areas)
        graph[0]["prerequisites"] = ["A99"]
        with self.assertRaises(ValueError):
            validator.validate_graph(graph)

    def test_rejects_duplicate_identifiers(self):
        with self.assertRaises(ValueError):
            validator.require_unique(["A01", "A01"], "area IDs")


if __name__ == "__main__":
    unittest.main()
