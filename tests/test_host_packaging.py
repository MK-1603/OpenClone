"""Unit tests verifying global host directory packaging and manifest validity."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class HostPackagingTests(unittest.TestCase):
    def setUp(self):
        self.hosts_dir = ROOT / "global" / "hosts"

    def test_hosts_directory_exists(self):
        self.assertTrue(self.hosts_dir.is_dir())

    def test_antigravity_packaging(self):
        agy_dir = self.hosts_dir / "antigravity"
        self.assertTrue(agy_dir.is_dir())
        manifest = agy_dir / ".antigravity-plugin" / "plugin.json"
        self.assertTrue(manifest.is_file())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertIn("openclone", data.get("name", ""))

    def test_claude_code_packaging(self):
        cc_dir = self.hosts_dir / "claude-code"
        self.assertTrue(cc_dir.is_dir())
        mkt = cc_dir / "marketplace.json"
        self.assertTrue(mkt.is_file())
        data = json.loads(mkt.read_text(encoding="utf-8"))
        self.assertIn("name", data)

    def test_codex_packaging(self):
        codex_dir = self.hosts_dir / "codex"
        self.assertTrue(codex_dir.is_dir())
        p_json = codex_dir / "plugin.json"
        m_json = codex_dir / "mcp.json"
        self.assertTrue(p_json.is_file())
        self.assertTrue(m_json.is_file())
        json.loads(p_json.read_text(encoding="utf-8"))
        json.loads(m_json.read_text(encoding="utf-8"))

    def test_vscode_packaging(self):
        vscode_dir = self.hosts_dir / "vscode"
        self.assertTrue(vscode_dir.is_dir())
        m_json = vscode_dir / "mcp.json"
        self.assertTrue(m_json.is_file())
        json.loads(m_json.read_text(encoding="utf-8"))

    def test_chatgpt_packaging(self):
        chatgpt_dir = self.hosts_dir / "chatgpt"
        self.assertTrue(chatgpt_dir.is_dir())
        inst = chatgpt_dir / "custom-gpt-instructions.md"
        openapi = chatgpt_dir / "openapi.json"
        self.assertTrue(inst.is_file())
        self.assertTrue(openapi.is_file())
        json.loads(openapi.read_text(encoding="utf-8"))

    def test_generic_mcp_packaging(self):
        gm_dir = self.hosts_dir / "generic-mcp"
        self.assertTrue(gm_dir.is_dir())
        m_json = gm_dir / "mcp.json"
        self.assertTrue(m_json.is_file())
        json.loads(m_json.read_text(encoding="utf-8"))
