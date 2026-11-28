"""Tests for Agent Client Protocol (ACP) Interoperability Adapter."""
import unittest
from pathlib import Path

from src.openclone.integrations.acp import ACPAdapter


class TestACPInteroperability(unittest.TestCase):
    """Test ACP protocol initialization, session lifecycle, and prompt handling."""

    def setUp(self):
        self.adapter = ACPAdapter()

    def test_acp_initialize(self):
        resp = self.adapter.handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {},
        })
        self.assertIn("result", resp)
        res = resp["result"]
        self.assertEqual(res["server"]["name"], "openclone-acp-adapter")
        self.assertTrue(res["capabilities"]["governedExecution"])

    def test_acp_session_lifecycle(self):
        # Create session
        create_resp = self.adapter.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "session/create",
            "params": {"workspace_root": "."},
        })
        self.assertIn("result", create_resp)
        session_id = create_resp["result"]["session_id"]
        self.assertTrue(session_id.startswith("acp-"))

        # Status
        status_resp = self.adapter.handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "session/status",
            "params": {"session_id": session_id},
        })
        self.assertEqual(status_resp["result"]["status"], "READY")

        # Cancel
        cancel_resp = self.adapter.handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "session/cancel",
            "params": {"session_id": session_id},
        })
        self.assertTrue(cancel_resp["result"]["cancelled"])

    def test_acp_prompt_execution(self):
        resp = self.adapter.handle_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "session/prompt",
            "params": {
                "text": "Add unit test for ACP adapter",
                "mode": "Fast",
            },
        })
        self.assertIn("result", resp)
        res = resp["result"]
        self.assertIn(res["status"], ("COMPLETED", "SUCCESS", "DELIVERED"))
        self.assertGreaterEqual(res["tests_passed"], 0)


if __name__ == "__main__":
    unittest.main()
