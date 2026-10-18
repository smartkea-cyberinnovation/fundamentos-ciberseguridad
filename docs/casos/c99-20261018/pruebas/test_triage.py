"""Pruebas sobre datos sintéticos; no ejecutan una webshell."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'herramientas'))
from triage_offline import decode_literal, analyze_bytes, MAX_BYTES

class TriageTests(unittest.TestCase):
    def test_hex_octal(self):
        self.assertEqual(decode_literal(r'"\x48\157\154\141"'), 'Hola')
    def test_single_quotes(self):
        self.assertEqual(decode_literal(r"'\x48'"), r'\x48')
    def test_escaped_backslash_not_decoded_twice(self):
        self.assertEqual(decode_literal(r'"\\x48"'), r'\x48')
    def test_invalid(self):
        with self.assertRaises(ValueError): decode_literal('abc')
    def test_octal_wrap(self):
        self.assertEqual(decode_literal(r'"\777"'), '\xff')
    def test_plain_marker(self):
        a=analyze_bytes(b'<?php $x="https://svgflow.digital/sz/log.php";')
        self.assertEqual(a['hits'][0]['kind'], 'callback_literal')
        self.assertFalse(a['sample_executed'])
    def test_encoded_marker(self):
        x='https://svgflow.digital/sz/log.php'
        fixture='<?php $x="'+''.join('\\x%02x'%ord(c) for c in x)+'";'
        self.assertTrue(analyze_bytes(fixture.encode())['hits'])
    def test_comments(self):
        a=analyze_bytes(b'<?php /* "https://svgflow.digital/sz/log.php" */ $x="normal";')
        self.assertFalse(a['hits'])
    def test_unknown_is_not_clean_verdict(self):
        a=analyze_bytes(b'<?php $a="hello";')
        self.assertIsNone(a['known_sample']); self.assertNotIn('safe', a)
    def test_limit(self):
        with self.assertRaises(ValueError): analyze_bytes(b'X'*(MAX_BYTES+1))

if __name__ == '__main__': unittest.main(verbosity=2)
