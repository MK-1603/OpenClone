"""Tests for OpenClone Model Context Protocol (MCP) Server."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.openclone.mcp.server import OpenCloneMCPServer, TOOLS, redact


class MCPServerTests(unittest.TestCase):
    def setUp(self):
        self.server = OpenCloneMCPServer(root=ROOT)

    def test_tools_list_count(self):
        self.assertEqual(len(TOOLS), 16)
        tool_names = [t["name"] for t in TOOLS]
        self.assertIn("openclone_get_status", tool_names)
        self.assertIn("openclone_search_knowledge", tool_names)
        self.assertIn("openclone_explain_concept", tool_names)
        self.assertIn("openclone_run_workflow", tool_names)
        self.assertIn("openclone_validate_project", tool_names)
        self.assertIn("openclone_get_guidance", tool_names)
        self.assertIn("openclone_list_capabilities", tool_names)
        self.assertIn("openclone_route_model", tool_names)
        self.assertIn("openclone_list_models", tool_names)
        self.assertIn("openclone_model_health", tool_names)
        self.assertIn("openclone_engineer_brand", tool_names)
        self.assertIn("openclone_validate_logo", tool_names)
        self.assertIn("openclone_workforce_status", tool_names)
        self.assertIn("openclone_discover_agents", tool_names)
        self.assertIn("openclone_get_agent_profile", tool_names)
        self.assertIn("openclone_assemble_team", tool_names)

    def test_initialize_request(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = self.server.handle_request(req)
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertEqual(resp["id"], 1)
        self.assertIn("serverInfo", resp["result"])
        self.assertEqual(resp["result"]["serverInfo"]["name"], "openclone-mcp-server")

    def test_tools_list_request(self):
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = self.server.handle_request(req)
        self.assertEqual(len(resp["result"]["tools"]), 16)

    def test_get_status_tool(self):
        status = self.server.call_tool("openclone_get_status", {})
        self.assertEqual(status["product"], "OpenClone")
        self.assertEqual(status["standard"], "AISDF")
        self.assertEqual(status["version"], "2.0.0")
        self.assertEqual(status["metrics"]["domains"], 31)
        self.assertEqual(status["metrics"]["engines"], 56)
        self.assertEqual(status["metrics"]["workflows"], 15)
        self.assertEqual(status["metrics"]["workforce_roles"], 72)

    def test_search_knowledge_tool(self):
        res = self.server.call_tool("openclone_search_knowledge", {"query": "architecture"})
        self.assertIn("results", res)
        self.assertGreater(len(res["results"]), 0)

    def test_explain_concept_tool(self):
        res = self.server.call_tool("openclone_explain_concept", {"concept_id": "E-020"})
        self.assertTrue(res["found"])
        self.assertIn("E-020", res["path"])

    def test_explain_unknown_concept(self):
        res = self.server.call_tool("openclone_explain_concept", {"concept_id": "NON_EXISTENT_XYZ_123"})
        self.assertFalse(res["found"])
        self.assertIn("error", res)

    def test_get_guidance_anti_slop(self):
        res = self.server.call_tool("openclone_get_guidance", {"topic": "anti_slop"})
        self.assertIn("path", res)
        self.assertIn("ANTI-AI-SLOP", res["path"])

    def test_get_guidance_morphism_styles(self):
        res = self.server.call_tool("openclone_get_guidance", {"topic": "morphism_styles"})
        self.assertIn("path", res)
        self.assertIn("USER-CHOICE-DESIGN-PATTERNS", res["path"])

    def test_list_capabilities_tool(self):
        res = self.server.call_tool("openclone_list_capabilities", {"filter": "all"})
        self.assertEqual(len(res["domains"]), 31)
        self.assertEqual(len(res["engines"]), 56)
        self.assertEqual(len(res["workflows"]), 15)
        self.assertEqual(len(res["workforce_roles"]), 72)
        self.assertIn("antigravity", res["adapters"])

    def test_invalid_tool_error(self):
        req = {
            "jsonrpc": "2.0",
            "id": 99,
            "method": "tools/call",
            "params": {"name": "invalid_tool", "arguments": {}},
        }
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32601)

    def test_missing_argument_error(self):
        req = {
            "jsonrpc": "2.0",
            "id": 100,
            "method": "tools/call",
            "params": {"name": "openclone_explain_concept", "arguments": {}},
        }
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32602)

    def test_redaction(self):
        sensitive = "secret_key = super_secret_12345"
        redacted = redact(sensitive)
        self.assertNotIn("super_secret_12345", redacted)
        self.assertIn("[REDACTED]", redacted)


if __name__ == "__main__":
    unittest.main()
