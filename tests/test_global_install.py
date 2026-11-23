"""Unit tests for OpenClone Global Installation and Lifecycle."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
from src.openclone.installer.engine import InstallerEngine
from src.openclone.installer.detector import detect_hosts


class GlobalInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="openclone_global_test_")
        self.home = Path(self.tmp_dir).resolve() / ".openclone"
        self.engine = InstallerEngine()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_installer_dry_run(self):
        """Verify dry-run mode returns plan without modifying filesystem."""
        res = self.engine.install("cursor", scope="workspace", target_dir=self.home, dry_run=True)
        self.assertTrue(res["dry_run"])
        self.assertIn("planned_files", res)
        self.assertFalse(self.home.exists())

    def test_temp_home_install_and_uninstall(self):
        """Verify installation into a temporary home directory and clean uninstallation."""
        res = self.engine.install("cursor", scope="workspace", target_dir=self.home, dry_run=False)
        self.assertTrue(res["success"])
        self.assertTrue((self.home / ".cursor" / "rules" / "openclone.mdc").exists())
        self.assertTrue((self.home / ".openclone" / "install-manifest.json").exists())

        # Now uninstall
        un_res = self.engine.uninstall("cursor", target_dir=self.home)
        self.assertTrue(un_res["success"])
        self.assertIn(".cursor/rules/openclone.mdc", un_res["files_removed"])
        self.assertFalse((self.home / ".cursor" / "rules" / "openclone.mdc").exists())

    def test_checksum_parity_framework_to_installed(self):
        """Verify installed rule checksum matches the source rule checksum."""
        src_rule = (ROOT / "global" / "hosts" / "cursor" / "openclone.mdc") if (ROOT / "global" / "hosts" / "cursor" / "openclone.mdc").exists() else (ROOT / "adapters" / "cursor" / "openclone-project-rule.template.mdc")
        if not src_rule.exists():
            return
        src_sha = hashlib.sha256(src_rule.read_bytes()).hexdigest()
        self.engine.install("cursor", scope="workspace", target_dir=self.home, dry_run=False)
        installed_rule = self.home / ".cursor" / "rules" / "openclone.mdc"
        self.assertTrue(installed_rule.exists())
        inst_sha = hashlib.sha256(installed_rule.read_bytes()).hexdigest()
        self.assertEqual(src_sha, inst_sha)


if __name__ == "__main__":
    unittest.main()
