"""Tests for IDE Platform Adapters (Antigravity, VSCode, Cursor, JetBrains, Zed, Generic)."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.openclone.integrations.adapters.antigravity import AntigravityAdapter
from src.openclone.integrations.adapters.cursor import CursorAdapter
from src.openclone.integrations.adapters.generic import GenericPlatformAdapter
from src.openclone.integrations.adapters.jetbrains import JetBrainsAdapter
from src.openclone.integrations.adapters.vscode import VSCodeAdapter
from src.openclone.integrations.adapters.zed import ZedAdapter


class TestPlatformAdapters(unittest.TestCase):
    """Test connection, disconnection, and health checks across platform adapters."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_vscode_adapter_connect_and_disconnect(self):
        adapter = VSCodeAdapter()
        res = adapter.connect(self.temp_dir)
        self.assertEqual(res["status"], "CONNECTED")

        mcp_path = self.temp_dir / ".vscode" / "mcp.json"
        self.assertTrue(mcp_path.exists())
        content = json.loads(mcp_path.read_text(encoding="utf-8"))
        self.assertIn("openclone", content.get("servers", {}))

        health = adapter.health_check(self.temp_dir)
        self.assertEqual(health["status"], "PASS")

        # Disconnect
        d_res = adapter.disconnect(self.temp_dir)
        self.assertEqual(d_res["status"], "DISCONNECTED")
        self.assertFalse(mcp_path.exists())

    def test_cursor_adapter_connect_and_disconnect(self):
        adapter = CursorAdapter()
        res = adapter.connect(self.temp_dir)
        self.assertEqual(res["status"], "CONNECTED")

        mcp_path = self.temp_dir / ".cursor" / "mcp.json"
        self.assertTrue(mcp_path.exists())
        health = adapter.health_check(self.temp_dir)
        self.assertEqual(health["status"], "PASS")

        d_res = adapter.disconnect(self.temp_dir)
        self.assertEqual(d_res["status"], "DISCONNECTED")

    def test_jetbrains_adapter_connect_and_disconnect(self):
        adapter = JetBrainsAdapter()
        res = adapter.connect(self.temp_dir)
        self.assertEqual(res["status"], "CONNECTED")

        mcp_path = self.temp_dir / ".idea" / "mcp.json"
        self.assertTrue(mcp_path.exists())
        health = adapter.health_check(self.temp_dir)
        self.assertEqual(health["status"], "PASS")

        d_res = adapter.disconnect(self.temp_dir)
        self.assertEqual(d_res["status"], "DISCONNECTED")

    def test_zed_adapter_connect_and_disconnect(self):
        adapter = ZedAdapter()
        res = adapter.connect(self.temp_dir)
        self.assertEqual(res["status"], "CONNECTED")

        settings_path = self.temp_dir / ".zed" / "settings.json"
        self.assertTrue(settings_path.exists())
        health = adapter.health_check(self.temp_dir)
        self.assertEqual(health["status"], "PASS")

        d_res = adapter.disconnect(self.temp_dir)
        self.assertEqual(d_res["status"], "DISCONNECTED")

    def test_generic_adapter_connect_and_disconnect(self):
        adapter = GenericPlatformAdapter()
        res = adapter.connect(self.temp_dir)
        self.assertEqual(res["status"], "CONNECTED")

        mcp_path = self.temp_dir / ".openclone" / "mcp.json"
        self.assertTrue(mcp_path.exists())
        health = adapter.health_check(self.temp_dir)
        self.assertEqual(health["status"], "PASS")

        d_res = adapter.disconnect(self.temp_dir)
        self.assertEqual(d_res["status"], "DISCONNECTED")


if __name__ == "__main__":
    unittest.main()
