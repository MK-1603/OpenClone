"""Tests for Extended MCP Tools required by the Universal IDE Integration Ecosystem."""
import json
import unittest

from src.openclone.mcp.server import OpenCloneMCPServer


class TestMCPExtendedTools(unittest.TestCase):
    """Test all 9 required MCP tools exposed by the OpenClone MCP Server."""

    def setUp(self):
        self.server = OpenCloneMCPServer()

    def test_all_extended_tools_present_in_list(self):
        resp = self.server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {"all": True}})
        tools = resp["result"]["tools"]
        tool_names = {t["name"] for t in tools}

        required_tools = [
            "openclone_inspect_repository",
            "openclone_get_project_context",
            "openclone_analyze_requirements",
            "openclone_generate_plan",
            "openclone_get_agent_status",
            "openclone_get_execution_status",
            "openclone_get_verification_results",
            "openclone_get_delivery_report",
            "openclone_execute_task",
        ]

        for req in required_tools:
            self.assertIn(req, tool_names)

    def test_inspect_repository_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "openclone_inspect_repository",
                "arguments": {"workspace_path": "."},
            },
        })
        self.assertFalse(resp.get("result", {}).get("isError", True))
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertIn("workspace_root", data)
        self.assertEqual(data["status"], "INSPECTED")

    def test_analyze_requirements_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "openclone_analyze_requirements",
                "arguments": {"prompt": "Write pytest test cases for rate limiter"},
            },
        })
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(data["intent"], "TESTING")

    def test_generate_plan_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "openclone_generate_plan",
                "arguments": {"prompt": "Build authentication middleware"},
            },
        })
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertIn("plan_id", data)
        self.assertGreaterEqual(len(data["tasks"]), 1)

    def test_get_agent_status_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "openclone_get_agent_status",
                "arguments": {},
            },
        })
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertGreaterEqual(data["total_workers"], 1)

    def test_verification_results_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "openclone_get_verification_results",
                "arguments": {},
            },
        })
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(data["status"], "PASS")

    def test_delivery_report_tool_call(self):
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "openclone_get_delivery_report",
                "arguments": {"request_id": "req-123"},
            },
        })
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(data["status"], "DELIVERED")


if __name__ == "__main__":
    unittest.main()
