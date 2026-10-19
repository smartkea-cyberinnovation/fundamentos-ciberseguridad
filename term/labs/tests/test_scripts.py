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


class HostWorkspaceTests(unittest.TestCase):
    """Exercise the native launcher's filesystem checks with a stub ttyd only."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name)
        self.base.chmod(0o755)
        self.home = self.base / "student-home"
        self.home.mkdir(mode=0o700)
        self.bin = self.base / "bin"
        self.bin.mkdir(mode=0o755)
        stub = self.bin / "ttyd"
        stub.write_text('#!/bin/sh\nif [ "$1" = --help ]; then printf "%s\\n" "--writable --check-origin"; else printf "%s\\n" "stub-terminal-invoked"; fi\n')
        stub.chmod(0o755)
        self.uid = 65534 if os.geteuid() == 0 else os.geteuid()
        self.gid = 65534 if os.geteuid() == 0 else os.getegid()
        if os.geteuid() == 0:
            os.chown(self.home, self.uid, self.gid)

    def run_host(self):
        options = {"user": self.uid, "group": self.gid, "extra_groups": []} if os.geteuid() == 0 else {}
        env = {**os.environ, "HOME": str(self.home), "PATH": str(self.bin) + os.pathsep + os.environ["PATH"]}
        try:
            return subprocess.run(["bash", str(SCRIPTS / "ttyd-host-start.sh"), "--read-only"],
                                  env=env, text=True, capture_output=True, timeout=5, check=False, **options)
        except PermissionError:
            self.skipTest("Runner cannot start a subprocess with an unprivileged UID")

    def test_owned_workspace_is_created_and_reused_with_private_permissions(self):
        workspace = self.home / "term-workspace"
        first = self.run_host()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("stub-terminal-invoked", first.stdout)
        self.assertEqual(workspace.stat().st_mode & 0o777, 0o700)
        workspace.chmod(0o755)
        again = self.run_host()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(workspace.stat().st_mode & 0o777, 0o700)

    def test_symlink_or_file_workspace_is_rejected_without_modifying_target(self):
        target = self.home / "keep-private"
        target.mkdir(mode=0o750)
        workspace = self.home / "term-workspace"
        workspace.symlink_to(target, target_is_directory=True)
        result = self.run_host()
        self.assertEqual(result.returncode, 73, result.stderr)
        self.assertNotIn("stub-terminal-invoked", result.stdout)
        self.assertEqual(target.stat().st_mode & 0o777, 0o750)
        workspace.unlink()
        workspace.write_text("keep this content")
        result = self.run_host()
        self.assertEqual(result.returncode, 73, result.stderr)
        self.assertEqual(workspace.read_text(), "keep this content")


if __name__ == "__main__":
    unittest.main()
