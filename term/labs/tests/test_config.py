"""Prevent accidental publication or privileged lab configuration in future edits."""
import json
import pathlib
import unittest
import yaml

LAB_DIR = pathlib.Path(__file__).resolve().parents[1]


class ConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose = yaml.safe_load((LAB_DIR / "compose.yaml").read_text())
        cls.stack = yaml.safe_load((LAB_DIR / "stack.yaml").read_text())

    def test_compose_is_unprivileged_and_internal(self):
        self.assertTrue(self.compose["networks"]["lab"]["internal"])
        for name, service in self.compose["services"].items():
            with self.subTest(service=name):
                self.assertEqual(service["user"], "10001:10001")
                self.assertTrue(service["read_only"])
                self.assertEqual(service["cap_drop"], ["ALL"])
                self.assertIn("no-new-privileges:true", service["security_opt"])
                self.assertGreater(service["pids_limit"], 0)
                self.assertNotIn("privileged", service)
                self.assertNotIn("network_mode", service)
                self.assertNotIn("devices", service)
                self.assertNotIn("docker.sock", json.dumps(service))
                self.assertEqual(service["networks"], ["lab"])

    def test_only_optin_loopback_ports(self):
        self.assertNotIn("ports", self.compose["services"]["web"])
        self.assertNotIn("ports", self.compose["services"]["toolbox"])
        for name, service in self.compose["services"].items():
            for port in service.get("ports", []):
                self.assertTrue(service.get("profiles"), name)
                self.assertTrue(port.startswith("127.0.0.1:"), port)
        self.assertEqual(self.compose["services"]["terminal"]["command"], ["--read-only"])
        self.assertEqual(self.compose["services"]["terminal-write"]["command"], ["--writable"])

    def test_tmpfs_options_are_single_strings(self):
        for service in self.compose["services"].values():
            for mount in service.get("tmpfs", []):
                self.assertTrue(mount.startswith("/"), mount)
                self.assertIn("noexec", mount)
                self.assertIn("size=", mount)

    def test_swarm_has_no_public_ports_or_builds(self):
        for name, service in self.stack["services"].items():
            with self.subTest(service=name):
                self.assertNotIn("ports", service)
                self.assertNotIn("build", service)
                self.assertNotIn("privileged", service)
                self.assertTrue(service["read_only"])
                self.assertEqual(service["cap_drop"], ["ALL"])
                self.assertIn("${LAB_", service["image"])
                self.assertIn(":?", service["image"])
                self.assertEqual(service["deploy"]["replicas"], 1)
                self.assertEqual(service["deploy"]["endpoint_mode"], "dnsrr")
                self.assertIn("LAB_STUDENT_ID", str(service["deploy"]["placement"]["constraints"]))

    def test_tunnel_secret_is_exclusive_to_connector(self):
        self.assertNotIn("secrets", self.stack["services"]["web"])
        self.assertNotIn("secrets", self.stack["services"]["terminal"])
        mounted = self.stack["services"]["cloudflared"]["secrets"]
        self.assertEqual(len(mounted), 1)
        self.assertEqual(mounted[0]["mode"], 0o400)
        self.assertTrue(self.stack["secrets"]["tunnel_credentials"]["external"])

    def test_tunnel_enforces_access_per_rule(self):
        for path in sorted((LAB_DIR / "config").glob("cloudflared*.yml")):
            with self.subTest(config=path.name):
                config = yaml.safe_load(path.read_text())
                self.assertEqual(config["ingress"][-1], {"service": "http_status:404"})
                for rule in config["ingress"][:-1]:
                    origin = rule["originRequest"]
                    self.assertTrue(origin["access"]["required"])
                    self.assertTrue(origin["access"]["audTag"])
                    self.assertEqual(origin["httpHostHeader"], rule["hostname"])
                    self.assertIs(origin["http2Origin"], False)
                    self.assertNotIn("noTLSVerify", origin)

    def test_explicit_public_inventory_has_no_runtime_files(self):
        inventory_path = LAB_DIR / "public-files.json"
        if not inventory_path.exists():
            self.skipTest("Public source archive intentionally omits the repository packaging inventory")
        inventory = json.loads(inventory_path.read_text())
        self.assertEqual(len(inventory), len(set(inventory)))
        self.assertNotIn("public-files.json", inventory)
        for relative in inventory:
            path = pathlib.PurePosixPath(relative)
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertTrue((LAB_DIR / relative).is_file(), relative)
            self.assertNotIn("__pycache__", path.parts)
            self.assertNotIn("workspace", path.parts)
            self.assertNotIn("evidence", path.parts)
            self.assertNotEqual(relative, ".env")


if __name__ == "__main__":
    unittest.main()
