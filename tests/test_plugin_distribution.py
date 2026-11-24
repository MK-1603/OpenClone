"""Test suite verifying OpenClone Universal AI Coding-Tool Plugin Distribution.

Validates:
- Antigravity native plugin manifest, skills, agents, rules
- Claude Code plugin manifest and marketplace catalog
- OpenAI Codex portable plugin manifest and marketplace catalog
- Cursor MCP and rule configurations
- Generic MCP server configuration
- Zero-clone policy integrity: all manifest asset paths resolve cleanly
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PluginDistributionTests(unittest.TestCase):
    def test_antigravity_root_plugin_manifest(self):
        p = ROOT / "plugin.json"
        self.assertTrue(p.is_file(), "Root plugin.json must exist for direct GitHub URL installation")
        data = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "openclone")
        self.assertIn("displayName", data)
        self.assertIn("version", data)
        self.assertIn("skills", data)
        self.assertIn("agents", data)
        self.assertIn("rules", data)
        self.assertIn("mcpServers", data)

        # Verify referenced skills exist
        for s in data["skills"]:
            skill_path = ROOT / s
            self.assertTrue(skill_path.is_dir(), f"Skill directory {s} must exist")
            self.assertTrue((skill_path / "SKILL.md").is_file(), f"{s}/SKILL.md must exist")

        # Verify referenced agents exist
        for a in data["agents"]:
            self.assertTrue((ROOT / a).is_file(), f"Agent file {a} must exist")

        # Verify referenced rules exist
        for r in data["rules"]:
            self.assertTrue((ROOT / r).is_file(), f"Rule file {r} must exist")

    def test_claude_code_marketplace_and_plugin(self):
        mkt = ROOT / ".claude-plugin" / "marketplace.json"
        self.assertTrue(mkt.is_file(), ".claude-plugin/marketplace.json must exist")
        mkt_data = json.loads(mkt.read_text(encoding="utf-8"))
        self.assertEqual(mkt_data.get("name"), "openclone-marketplace")
        self.assertTrue(len(mkt_data.get("plugins", [])) > 0)
        plugin_entry = mkt_data["plugins"][0]
        self.assertEqual(plugin_entry.get("name"), "openclone")

        # Verify plugin.json inside adapter
        p_json = ROOT / "adapters" / "claude-code" / ".claude-plugin" / "plugin.json"
        self.assertTrue(p_json.is_file())
        p_data = json.loads(p_json.read_text(encoding="utf-8"))
        self.assertEqual(p_data.get("name"), "openclone")
        self.assertIn("skills", p_data)

    def test_codex_marketplace_and_plugin(self):
        mkt = ROOT / ".agents" / "plugins" / "marketplace.json"
        self.assertTrue(mkt.is_file(), ".agents/plugins/marketplace.json must exist")
        mkt_data = json.loads(mkt.read_text(encoding="utf-8"))
        self.assertEqual(mkt_data.get("name"), "openclone")
        self.assertTrue(len(mkt_data.get("plugins", [])) > 0)

        # Verify codex adapter plugin.json
        p_json = ROOT / "adapters" / "codex" / "plugin.json"
        self.assertTrue(p_json.is_file())
        p_data = json.loads(p_json.read_text(encoding="utf-8"))
        self.assertEqual(p_data.get("name"), "openclone-engineering")
        self.assertIn("skills", p_data)

    def test_cursor_and_generic_mcp_config(self):
        cursor_mcp = ROOT / "adapters" / "cursor" / ".cursor" / "mcp.json"
        self.assertTrue(cursor_mcp.is_file())
        json.loads(cursor_mcp.read_text(encoding="utf-8"))

        generic_mcp = ROOT / "adapters" / "generic-mcp" / "README.md"
        self.assertTrue(generic_mcp.is_file())

    def test_zero_clone_installation_doc_exists(self):
        doc = ROOT / "docs" / "universal-installation.md"
        self.assertTrue(doc.is_file())
        content = doc.read_text(encoding="utf-8")
        self.assertIn("agy plugin install https://github.com/MK-1603/OpenClone", content)
        self.assertIn("/plugin marketplace add MK-1603/OpenClone", content)
        self.assertIn("codex plugin marketplace add MK-1603/OpenClone", content)


if __name__ == "__main__":
    unittest.main()
