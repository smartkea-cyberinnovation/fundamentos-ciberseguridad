"""Offline regression coverage for manifest-driven, exact deployment tooling."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cloudflare


class ToolchainContractTests(unittest.TestCase):
    def fixture(self, version='4.158.0'):
        deps = {'wrangler': version}
        package = {'devDependencies': deps}
        lock = {'lockfileVersion': 3, 'packages': {
            '': {'devDependencies': dict(deps)},
            'node_modules/wrangler': {
                'version': version,
                'resolved': f'https://registry.npmjs.org/wrangler/-/wrangler-{version}.tgz',
                'integrity': 'sha512-synthetic-test-integrity'}}}
        return package, lock

    def write(self, directory, package, lock):
        (directory/'package.json').write_text(json.dumps(package))
        (directory/'package-lock.json').write_text(json.dumps(lock))

    def test_real_reviewed_lock_has_one_version_source(self):
        package = json.loads((cloudflare.TOOLING/'package.json').read_text())
        self.assertEqual(cloudflare.toolchain_version(), package['devDependencies']['wrangler'])
        self.assertFalse(hasattr(cloudflare, 'WRANGLER'))

    def test_exact_manifest_and_lock_updates_do_not_need_python_edits(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with patch.object(cloudflare, 'TOOLING', directory):
                for version in ('4.158.0', '4.159.1'):
                    self.write(directory, *self.fixture(version))
                    self.assertEqual(cloudflare.toolchain_version(), version)

    def test_ranges_prereleases_sources_and_extra_dependencies_are_rejected(self):
        package, lock = self.fixture()
        candidates = [{'wrangler': value} for value in ('^4.158.0', '~4.158.0', 'latest',
                      '4.158.0-beta', 'file:../other', '4.158.00', '4.158.0;echo bad')]
        candidates += [{'wrangler': '4.158.0', 'other': '1.0.0'}, None, ['wrangler']]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with patch.object(cloudflare, 'TOOLING', directory):
                for deps in candidates:
                    with self.subTest(dependencies=deps):
                        self.write(directory, {'devDependencies': deps}, lock)
                        with self.assertRaises(ValueError): cloudflare.toolchain_version()

    def test_mismatches_and_external_registry_fail_before_install(self):
        package, lock = self.fixture()
        variants = []
        for key, value in [('version', '4.154.0'), ('resolved', 'https://other.example/cli.tgz'),
                           ('integrity', None), ('integrity', '')]:
            candidate = deepcopy(lock)
            candidate['packages']['node_modules/wrangler'][key] = value
            variants.append(candidate)
        candidate = deepcopy(lock)
        candidate['packages']['']['devDependencies'] = {'wrangler': '4.154.0'}
        variants += [candidate, {'lockfileVersion': 2, 'packages': {}}, [],
                     {'lockfileVersion': 3, 'packages': {'': None, 'node_modules/wrangler': []}}]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with patch.object(cloudflare, 'TOOLING', directory), \
                 patch.object(cloudflare.shutil, 'which', return_value='/usr/bin/node'), \
                 patch.object(cloudflare, 'execute') as execute:
                for candidate in variants:
                    with self.subTest(lock=candidate):
                        self.write(directory, package, candidate)
                        with self.assertRaises(ValueError): cloudflare.install_tooling()
                execute.assert_not_called()

    def test_symlinked_lockfile_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write(directory, *self.fixture())
            (directory/'package-lock.json').rename(directory/'actual.json')
            (directory/'package-lock.json').symlink_to(directory/'actual.json')
            with patch.object(cloudflare, 'TOOLING', directory):
                with self.assertRaises(ValueError): cloudflare.toolchain_version()

    def test_installed_cli_version_is_checked_before_deployment(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write(directory, *self.fixture())
            cli = directory/'node_modules/wrangler'
            (cli/'bin').mkdir(parents=True)
            (cli/'package.json').write_text(json.dumps({'version': '4.154.0'}))
            (cli/'bin/wrangler.js').write_text('// synthetic fixture')
            with patch.object(cloudflare, 'TOOLING', directory), \
                 patch.object(cloudflare, 'WRANGLER_BIN', cli/'bin/wrangler.js'), \
                 patch.object(cloudflare.shutil, 'which', return_value='/usr/bin/node'), \
                 patch.object(cloudflare, 'execute') as execute:
                with self.assertRaisesRegex(ValueError, 'instalación'): cloudflare.run('deploy')
                self.assertEqual(execute.call_count, 1)
                self.assertIn('ci', execute.call_args.args[0])
                self.assertIn('--ignore-scripts', execute.call_args.args[0])


if __name__ == '__main__': unittest.main()
