"""Regresiones defensivas: fixtures de texto; jamás invocan PHP ni la red."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'herramientas'))
from triage_offline import analyze_bytes, literals

IOC = b'https://svgflow.digital/sz/log.php'
ASSIGN = b'$x="' + IOC + b'";'

class LexerRegressionTests(unittest.TestCase):
    def test_line_comment_terminators(self):
        for comment in (b'//', b'#'):
            for end in (b'\r', b'\n', b'\r\n', b'?><?php '):
                with self.subTest(comment=comment, end=end):
                    report=analyze_bytes(b'<?php ' + comment + b' comment' + end + ASSIGN)
                    self.assertEqual(len(report['hits']),1)
    def test_html_before_php_ignored(self):
        self.assertFalse(analyze_bytes(b'<a href="'+IOC+b'">test</a>')['hits'])
    def test_html_between_blocks_ignored(self):
        report=analyze_bytes(b'<?php // end ?><a href="'+IOC+b'">x</a><?php '+ASSIGN)
        self.assertEqual(len(report['hits']),1)
    def test_hash_comment_closing_php_ignores_html(self):
        self.assertFalse(analyze_bytes(b'<?php # end ?><img src="'+IOC+b'">')['hits'])
    def test_real_quote_is_required(self):
        for ending in (b'"',b"'",b'`'):
            with self.subTest(ending=ending):
                report=analyze_bytes(b'<?php '+ASSIGN+ending)
                self.assertEqual(len(report['hits']),1)
                self.assertEqual(report['lexer_warnings'][0]['kind'],'unterminated_quoted_literal')
    def test_final_escaped_quote_not_a_close(self):
        raw=b'<?php '+ASSIGN+b' "bad\\"'
        report=analyze_bytes(raw)
        self.assertEqual(len(report['hits']),1)
        self.assertEqual(report['literal_count_reduced_lexer'],1)
        self.assertTrue(report['lexer_warnings'])
    def test_escaped_backslash_then_quote_does_close(self):
        self.assertEqual(len(list(literals('<?php "abc\\\\";'))),1)
    def test_php_end_in_string_does_not_leave_php(self):
        self.assertEqual(len(analyze_bytes(b'<?php $a="?>"; '+ASSIGN)['hits']),1)
    def test_php_end_in_block_comment_does_not_leave_php(self):
        self.assertEqual(len(analyze_bytes(b'<?php /* ?> */ '+ASSIGN)['hits']),1)
    def test_unterminated_block_comment_preserves_hash(self):
        raw=b'<?php '+ASSIGN+b' /* incomplete'
        report=analyze_bytes(raw)
        self.assertEqual(report['sha256'],hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(report['hits']),1)
        self.assertEqual(report['lexer_warnings'][0]['kind'],'unterminated_block_comment')
    def test_echo_short_tag(self):
        self.assertEqual(len(analyze_bytes(b'<?= "'+IOC+b'" ?>')['hits']),1)
    def test_uppercase_php_tag(self):
        self.assertEqual(len(analyze_bytes(b'<?PHP '+ASSIGN)['hits']),1)
    def test_backticks_are_not_executed_or_decoded(self):
        report=analyze_bytes(b'<?php `'+IOC+b'`;')
        self.assertFalse(report['hits']);self.assertFalse(report['sample_executed'])
    def test_heredoc_stops_with_explicit_warning(self):
        report=analyze_bytes(b'<?php '+ASSIGN+b' $z=<<<TXT\n'+IOC+b'\nTXT;')
        self.assertEqual(len(report['hits']),1)
        self.assertEqual(report['lexer_warnings'][0]['kind'],'unsupported_heredoc_or_nowdoc')
    def test_cli_writes_report_for_truncated_input(self):
        script=Path(__file__).resolve().parents[1]/'herramientas/triage_offline.py'
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'evidence.txt';dest=Path(folder)/'report.json'
            source.write_bytes(b'<?php '+ASSIGN+b' "')
            result=subprocess.run([sys.executable,str(script),str(source),'--out',str(dest)],capture_output=True,timeout=5)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(len(json.loads(dest.read_text())['hits']),1)
    def test_comment_ioc_ignored(self):
        report=analyze_bytes(b'<?php // "'+IOC+b'"\r$a="normal";')
        self.assertFalse(report['hits'])

    def test_many_short_comments_do_not_repeatedly_scan_the_remaining_input(self):
        class SearchBudgetText(str):
            # Count characters covered by str.find, including unsuccessful scans.
            # This catches quadratic tail rescans without a machine-speed timeout.
            scanned = 0
            def find(self, sub, start=0, end=None):
                end = len(self) if end is None else end
                result = super().find(sub, start, end)
                self.scanned += max(0, (result + len(sub) if result >= 0 else end) - start)
                if self.scanned > 4 * len(self):
                    raise AssertionError('Repeated scans exceed a linear input budget')
                return result
        source = SearchBudgetText('<?php ' + '// short comment\n' * 20000 + '"kept";')
        warnings = []
        self.assertEqual([value for _, value in literals(source, warnings)], ['"kept"'])
        self.assertEqual(warnings, [])

if __name__ == '__main__': unittest.main()
