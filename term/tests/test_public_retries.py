"""Publication delays are retryable; byte/CSP/schema failures are not."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('term_verify_retries', ROOT/'verify_public.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
COMMIT = 'a'*40


class PublicRetryTests(unittest.TestCase):
    def test_delayed_commit_is_waited_for_without_claiming_early_success(self):
        checker = Mock(side_effect=[v.PublicationPending('old commit'),
                                   v.PublicationPending('old commit'),
                                   {'status': 'passed', 'checks': [{'path': 'index.html'}]}])
        sleep = Mock()
        result = v.verify_with_retries(COMMIT, 4, checker=checker, sleeper=sleep)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['verificationAttempts'], 3)
        self.assertEqual([x['status'] for x in result['attemptHistory']], ['waiting', 'waiting', 'passed'])
        self.assertEqual(sleep.call_count, 2)
        self.assertEqual(result['checks'], [{'path': 'index.html'}])

    def test_stale_commit_only_requests_metadata_and_records_observed_sha(self):
        reader = Mock(return_value={'status': 200, 'body': json.dumps({'sourceCommit': 'b'*40}).encode()})
        with self.assertRaisesRegex(v.PublicationPending, 'b'*40): v.check(COMMIT, reader)
        reader.assert_called_once_with(v.BASE+'build-info.json')

    def test_integrity_headers_and_schema_fail_immediately(self):
        for error in (ValueError('Public asset mismatch'), ValueError('Unexpected public CSP'),
                      KeyError('modules'), TypeError('invalid schema')):
            with self.subTest(error=error):
                checker = Mock(side_effect=error)
                sleep = Mock()
                result = v.verify_with_retries(COMMIT, 60, checker=checker, sleeper=sleep)
                self.assertEqual(result['status'], 'failed')
                self.assertFalse(result['retryable'])
                self.assertEqual(checker.call_count, 1)
                sleep.assert_not_called()

    def test_exhausted_wait_stays_failed_and_retains_each_attempt(self):
        checker = Mock(side_effect=v.PublicationPending('not yet published'))
        sleep = Mock()
        result = v.verify_with_retries(COMMIT, 3, checker=checker, sleeper=sleep)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(len(result['attemptHistory']), 3)
        self.assertEqual(sleep.call_count, 2)

    def test_network_failure_can_recover(self):
        result = v.verify_with_retries(COMMIT, 2,
            checker=Mock(side_effect=[OSError('network'), {'status': 'passed'}]), sleeper=Mock())
        self.assertEqual(result['status'], 'passed')

    def test_attempts_and_commit_are_bounded_before_network_access(self):
        checker = Mock()
        for commit, attempts in [(COMMIT, 0), (COMMIT, 61), ('main', 1), ('a'*39, 1)]:
            with self.assertRaises(ValueError): v.verify_with_retries(commit, attempts, checker=checker)
        checker.assert_not_called()

    def test_malformed_metadata_is_not_a_publication_delay(self):
        reader = Mock(return_value={'status': 200, 'body': b'[]'})
        with self.assertRaises(ValueError): v.check(COMMIT, reader)


if __name__ == '__main__': unittest.main()
