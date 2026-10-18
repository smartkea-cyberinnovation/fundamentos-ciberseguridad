import os
import pathlib
import subprocess
import tempfile
import unittest

LAB_DIR = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = LAB_DIR / "scripts"


def run_script(name, *args, timeout=10):
    return subprocess.run(["bash", str(SCRIPTS / name), *map(str, args)], text=True, capture_output=True, timeout=timeout, check=False)


class ScriptTests(unittest.TestCase):
    def test_all_bash_syntax(self):
        for script in sorted(SCRIPTS.glob("*.sh")):
            with self.subTest(script=script.name):
                result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_fixture_generation_and_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = pathlib.Path(tmp) / "evidence with spaces"
            generated = run_script("make-fixtures.sh", destination)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertEqual(destination.stat().st_mode & 0o777, 0o700)
            self.assertEqual(len((destination / "SHA256SUMS").read_text().splitlines()), 3)
            verified = run_script("verify-evidence.sh", destination)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            with (destination / "logs/access.log").open("a") as output:
                output.write("synthetic alteration\n")
            altered = run_script("verify-evidence.sh", destination)
            self.assertNotEqual(altered.returncode, 0)

    def test_generator_refuses_existing_or_symlink_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = pathlib.Path(tmp) / "existing"
            existing.mkdir()
            marker = existing / "keep.txt"
            marker.write_text("unchanged")
            self.assertEqual(run_script("make-fixtures.sh", existing).returncode, 73)
            linked = pathlib.Path(tmp) / "linked"
            linked.symlink_to(existing, target_is_directory=True)
            self.assertEqual(run_script("make-fixtures.sh", linked).returncode, 73)
            self.assertEqual(marker.read_text(), "unchanged")
            self.assertEqual(list(existing.iterdir()), [marker])

    def test_verifier_rejects_external_manifest_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = pathlib.Path(tmp) / "evidence"
            self.assertEqual(run_script("make-fixtures.sh", evidence).returncode, 0)
            (evidence / "SHA256SUMS").write_text("0" * 64 + "  /etc/passwd\n")
            result = run_script("verify-evidence.sh", evidence)
            self.assertEqual(result.returncode, 65, result.stderr)

    def test_verifier_rejects_symlink_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = pathlib.Path(tmp) / "evidence"
            self.assertEqual(run_script("make-fixtures.sh", evidence).returncode, 0)
            target = evidence / "logs/access.log"
            target.unlink()
            target.symlink_to("/etc/passwd")
            self.assertEqual(run_script("verify-evidence.sh", evidence).returncode, 65)

    def test_script_arguments_fail_before_network_or_docker(self):
        for name in ("diagnose.sh", "http-check.sh", "smoke.sh", "lock-images.sh"):
            with self.subTest(name=name):
                self.assertEqual(run_script(name, "unexpected").returncode, 64)
        self.assertEqual(run_script("swarm-limits.sh", "invalid;stack").returncode, 64)

    @unittest.skipUnless(os.geteuid() == 0, "root rejection is tested only when the runner is root")
    def test_terminal_launchers_reject_root(self):
        for name in ("ttyd-start.sh", "ttyd-host-start.sh"):
            with self.subTest(name=name):
                result = run_script(name)
                self.assertEqual(result.returncode, 77, result.stderr)
                self.assertIn("root", result.stderr)


if __name__ == "__main__":
    unittest.main()
