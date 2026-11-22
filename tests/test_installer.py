"""Tests for OpenClone Global Plugin Installer and Host Management Engine."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from src.openclone.installer.detector import detect_hosts, HostDetectionResult
from src.openclone.installer.engine import InstallerEngine
from src.openclone.installer.manifest import InstallationManifest


class InstallerEngineTests(unittest.TestCase):
    """Test suite verifying installer engine, detector, transaction safety, and rollback."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="oc_installer_test_")
        self.workspace = Path(self.tmp_dir).resolve()
        self.engine = InstallerEngine()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_host_detection(self):
        """Verify host detection identifies supported hosts and formats results."""
        results = detect_hosts(self.workspace)
        self.assertIn("antigravity", results)
        self.assertIn("claude_code", results)
        self.assertIn("codex", results)
        self.assertIn("cursor", results)
        self.assertIn("generic_mcp", results)

        for hid, res in results.items():
            self.assertIsInstance(res, HostDetectionResult)
            self.assertGreaterEqual(res.confidence, 0.0)
            self.assertLessEqual(res.confidence, 1.0)
            self.assertIn("workspace", res.supported_scopes)

    def test_dry_run_install(self):
        """Verify dry run outputs planned files without writing to filesystem."""
        res = self.engine.install("cursor", scope="workspace", target_dir=self.workspace, dry_run=True)
        self.assertTrue(res["dry_run"])
        self.assertIn(".cursor/rules/aisdf.mdc", res["planned_files"])
        self.assertIn(".cursor/mcp.json", res["planned_files"])
        # Confirm files were NOT actually written
        self.assertFalse((self.workspace / ".cursor").exists())
        self.assertFalse((self.workspace / ".openclone").exists())

    def test_workspace_installation_transaction(self):
        """Verify clean workspace installation writes adapter files and manifests."""
        res = self.engine.install("cursor", scope="workspace", target_dir=self.workspace)
        self.assertTrue(res["success"])
        self.assertEqual(res["host_id"], "cursor")

        rule_file = self.workspace / ".cursor" / "rules" / "aisdf.mdc"
        mcp_file = self.workspace / ".cursor" / "mcp.json"
        manifest_file = self.workspace / ".openclone" / "install-manifest.json"

        self.assertTrue(rule_file.exists())
        self.assertTrue(mcp_file.exists())
        self.assertTrue(manifest_file.exists())

        # Verify manifest contents
        manifest = InstallationManifest.load(self.workspace)
        self.assertIn("cursor", manifest.hosts)
        rec = manifest.hosts["cursor"]
        self.assertEqual(rec.scope, "workspace")
        self.assertIn(".cursor/rules/aisdf.mdc", rec.installed_files)
        self.assertIn(".cursor/mcp.json", rec.installed_files)

    def test_preexisting_file_backup_and_uninstall_restore(self):
        """Verify pre-existing user files are safely backed up and restored on uninstall."""
        # 1. Simulate pre-existing user configuration
        mcp_dest = self.workspace / ".cursor" / "mcp.json"
        mcp_dest.parent.mkdir(parents=True, exist_ok=True)
        user_original_content = json.dumps({"custom_user_server": True})
        mcp_dest.write_text(user_original_content, encoding="utf-8")

        # 2. Install Cursor adapter
        res = self.engine.install("cursor", scope="workspace", target_dir=self.workspace)
        self.assertTrue(res["success"])
        self.assertEqual(res["backups_created"], 1)

        # Confirm new content replaced it
        new_content = mcp_dest.read_text(encoding="utf-8")
        self.assertIn("openclone", new_content)

        # 3. Uninstall Cursor adapter
        unres = self.engine.uninstall("cursor", target_dir=self.workspace)
        self.assertTrue(unres["success"])
        self.assertIn(".cursor/mcp.json", unres["backups_restored"])

        # Confirm original user content was restored!
        restored_content = mcp_dest.read_text(encoding="utf-8")
        self.assertEqual(restored_content, user_original_content)

        # Confirm non-backed up OpenClone file was cleanly removed
        self.assertFalse((self.workspace / ".cursor" / "rules" / "aisdf.mdc").exists())

    def test_integrity_verification(self):
        """Verify manifest detects physical file modification and tampering."""
        self.engine.install("claude_code", scope="workspace", target_dir=self.workspace)
        manifest = InstallationManifest.load(self.workspace)

        # Initially intact
        integ1 = manifest.verify_integrity(self.workspace, "claude_code")
        self.assertTrue(integ1["intact"])
        self.assertEqual(len(integ1["modified"]), 0)

        # Tamper with installed file
        mcp_path = self.workspace / ".mcp.json"
        mcp_path.write_text(mcp_path.read_text(encoding="utf-8") + "\n// tampered", encoding="utf-8")

        integ2 = manifest.verify_integrity(self.workspace, "claude_code")
        self.assertFalse(integ2["intact"])
        self.assertIn(".mcp.json", integ2["modified"])

    def test_security_boundary_containment(self):
        """Verify path traversal is rejected with PermissionError."""
        with self.assertRaises(PermissionError):
            self.engine._check_containment(self.workspace, self.workspace / ".." / "escaped.txt")

    def test_unsupported_host_error(self):
        """Verify unsupported host raises ValueError."""
        with self.assertRaises(ValueError):
            self.engine.install("unknown_host_xyz", target_dir=self.workspace)

    def test_doctor_diagnostics(self):
        """Verify doctor runs all checks and returns healthy status."""
        doc = self.engine.doctor(target_dir=self.workspace)
        self.assertIn("all_healthy", doc)
        self.assertIn("checks", doc)
        self.assertGreaterEqual(len(doc["checks"]), 4)


if __name__ == "__main__":
    unittest.main()
