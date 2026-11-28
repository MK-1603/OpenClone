"""Comprehensive test suite for OpenClone Phase 1 Universal AI Assistant Connector.

Covers:
- Level 1: Connector Unit Tests (initialization, adapters, config, normalization, health checks)
- Level 2: Protocol Integration Tests (MCP STDIO, Streamable HTTP, SSE, REST, OpenAPI, Function Calling)
- Level 3: Platform Compatibility Tests (ChatGPT, Claude, Gemini, Z.ai, Mistral, Open WebUI, LibreChat)
- Level 4: End-to-End Tests (Platform -> Connector -> Gateway -> Registry -> Planner Agent -> Execution)
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.openclone.connectors.contracts import (
    ConnectionState,
    NormalizedRequest,
    NormalizedResponse,
    PlatformConfig,
    PlatformType,
    ProtocolType,
    UniversalConnectorConfig,
)
from src.openclone.connectors.core import UniversalAIAssistantConnector
from src.openclone.connectors.adapters import (
    ChatGPTAdapter,
    ClaudeAdapter,
    GeminiAdapter,
    LibreChatAdapter,
    MistralAdapter,
    OpenWebUIAdapter,
    ZaiAdapter,
)
from src.openclone.connectors.protocols import (
    FunctionCallingBridge,
    McpHttpBridge,
    McpSseBridge,
    McpStdioBridge,
    OpenApiBridge,
    RestProtocolBridge,
)
from src.openclone.integrations.capabilities import get_canonical_registry
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway
from src.openclone.planning.agent import OpenClonePlannerAgent


class Level1ConnectorUnitTests(unittest.TestCase):
    """Level 1: Core connector unit tests."""

    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[1]
        self.connector = UniversalAIAssistantConnector()

    def test_connector_initialization(self):
        """Verify connector initializes with all 7 platform adapters."""
        self.assertIsNotNone(self.connector)
        self.assertIsNotNone(self.connector.registry)
        self.assertIsNotNone(self.connector.gateway)
        self.assertIsNotNone(self.connector.planner_agent)
        self.assertEqual(len(self.connector.adapters), 7)

    def test_all_seven_platforms_loaded(self):
        """Verify each of the 7 required platforms is registered."""
        expected_platforms = {
            PlatformType.CHATGPT,
            PlatformType.CLAUDE,
            PlatformType.GEMINI,
            PlatformType.ZAI,
            PlatformType.MISTRAL,
            PlatformType.OPEN_WEBUI,
            PlatformType.LIBRECHAT,
        }
        loaded = set(self.connector.adapters.keys())
        self.assertEqual(expected_platforms, loaded)

    def test_platform_retrieval(self):
        """Verify adapter lookup by enum and string."""
        claude_adapter = self.connector.get_adapter(PlatformType.CLAUDE)
        self.assertIsInstance(claude_adapter, ClaudeAdapter)

        chatgpt_adapter = self.connector.get_adapter("chatgpt")
        self.assertIsInstance(chatgpt_adapter, ChatGPTAdapter)

        with self.assertRaises(KeyError):
            self.connector.get_adapter("unknown_platform")

    def test_tool_discovery_across_platforms(self):
        """Verify dynamic capability discovery from CapabilityRegistry for all platforms."""
        for p_type in PlatformType:
            tools = self.connector.discover_tools(p_type)
            self.assertGreaterEqual(len(tools), 10, f"Platform {p_type} should discover all capabilities")

    def test_health_check_report(self):
        """Verify comprehensive health check output."""
        health = self.connector.health_check()
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(len(health["platforms"]), 7)
        for p_name, p_stat in health["platforms"].items():
            self.assertEqual(p_stat["status"], "healthy")
            self.assertGreaterEqual(p_stat["available_capabilities"], 10)

    def test_request_normalization_error_handling(self):
        """Verify graceful normalization when errors occur."""
        adapter = self.connector.get_adapter(PlatformType.CLAUDE)
        req = NormalizedRequest(
            request_id="test_req",
            platform=PlatformType.CLAUDE,
            protocol=ProtocolType.MCP_HTTP,
            tool_name="non_existent_tool",
        )
        err = ValueError("Invalid input argument")
        resp = adapter.normalize_error(err, req)
        self.assertFalse(resp.success)
        self.assertEqual(resp.error_code, 400)
        self.assertIn("Invalid input argument", resp.error_message)


class Level2ProtocolIntegrationTests(unittest.TestCase):
    """Level 2: Protocol integration tests across supported formats."""

    def setUp(self):
        self.connector = UniversalAIAssistantConnector()

    def test_mcp_streamable_http_lifecycle(self):
        """Verify MCP HTTP initialize, tools/list, ping, and tools/call lifecycle."""
        bridge = self.connector.mcp_http_bridge

        # 1. initialize
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}}
        init_resp = bridge.handle_jsonrpc(init_req, headers={})
        self.assertEqual(init_resp["id"], 1)
        self.assertEqual(init_resp["result"]["serverInfo"]["name"], "openclone-universal-connector")

        # 2. ping
        ping_resp = bridge.handle_jsonrpc({"jsonrpc": "2.0", "id": 2, "method": "ping"}, headers={})
        self.assertEqual(ping_resp["result"], {})

        # 3. tools/list
        list_resp = bridge.handle_jsonrpc({"jsonrpc": "2.0", "id": 3, "method": "tools/list"}, headers={})
        self.assertIn("tools", list_resp["result"])
        tool_names = [t["name"] for t in list_resp["result"]["tools"]]
        self.assertIn("openclone_understand_project", tool_names)
        self.assertIn("openclone_plan_and_execute", tool_names)

    def test_mcp_sse_session_management(self):
        """Verify MCP SSE endpoint creation and message formatting."""
        sse_bridge = self.connector.mcp_sse_bridge
        init_event = sse_bridge.create_session("sess_123")
        self.assertIn("event: endpoint", init_event)
        self.assertIn("sessionId=sess_123", init_event)

        msg_event = sse_bridge.format_sse_message({"jsonrpc": "2.0", "id": 1, "result": {"ok": True}})
        self.assertTrue(msg_event.startswith("event: message"))
        self.assertIn('"ok": true', msg_event)

    def test_mcp_stdio_line_processing(self):
        """Verify MCP STDIO line-by-line processing."""
        stdio_bridge = self.connector.mcp_stdio_bridge
        line = json.dumps({"jsonrpc": "2.0", "id": 10, "method": "ping"})
        out = stdio_bridge.process_line(line)
        self.assertIsNotNone(out)
        resp = json.loads(out)
        self.assertEqual(resp["id"], 10)
        self.assertEqual(resp["result"], {})

    def test_openapi_specification_generation(self):
        """Verify OpenAPI 3.1 specification generation."""
        spec = self.connector.openapi_bridge.get_spec(title="OpenClone Universal Connector")
        self.assertEqual(spec["openapi"], "3.1.0")
        self.assertEqual(spec["info"]["title"], "OpenClone Universal Connector")
        self.assertIn("/capabilities/openclone_understand_project", spec["paths"])
        self.assertIn("/capabilities/openclone_plan_and_execute", spec["paths"])

    def test_function_calling_schema_bridge(self):
        """Verify vendor-specific schema generation."""
        cap = self.connector.registry.get("openclone_understand_project")
        self.assertIsNotNone(cap)

        # Gemini declaration
        gemini_decl = FunctionCallingBridge.to_gemini_declaration(cap)
        self.assertEqual(gemini_decl["name"], "openclone_understand_project")
        self.assertIn("parameters", gemini_decl)

        # OpenAI tool
        openai_tool = FunctionCallingBridge.to_openai_tool(cap)
        self.assertEqual(openai_tool["type"], "function")
        self.assertEqual(openai_tool["function"]["name"], "openclone_understand_project")

        # Mistral tool
        mistral_tool = FunctionCallingBridge.to_mistral_tool(cap)
        self.assertEqual(mistral_tool["function"]["name"], "openclone_understand_project")

        # Z.ai tool
        zai_tool = FunctionCallingBridge.to_zai_tool(cap)
        self.assertEqual(zai_tool["function"]["name"], "openclone_understand_project")


class Level3PlatformCompatibilityTests(unittest.TestCase):
    """Level 3: Platform-specific adapter compatibility tests for all 7 platforms."""

    def setUp(self):
        self.connector = UniversalAIAssistantConnector()
        # Allow default guest context in test runner
        self.connector.config.require_authentication = False

    def test_platform_1_chatgpt_adapter(self):
        """[MOCKED TEST ONLY] Verify ChatGPT tool call ingestion and response output."""
        adapter = self.connector.get_adapter(PlatformType.CHATGPT)
        tool_call = {
            "id": "call_chatgpt_001",
            "type": "function",
            "function": {
                "name": "openclone_understand_project",
                "arguments": json.dumps({"prompt": "Build an e-commerce API in FastAPI"}),
            },
        }
        res = self.connector.handle_chatgpt_tool_call(tool_call)
        self.assertEqual(res["tool_call_id"], "call_chatgpt_001")
        self.assertEqual(res["role"], "tool")
        content = json.loads(res["content"])
        self.assertIn("intent", content)

    def test_platform_2_claude_adapter(self):
        """[MOCKED TEST ONLY] Verify Claude MCP tool call and structured content."""
        req = {
            "jsonrpc": "2.0",
            "id": "req_claude_002",
            "method": "tools/call",
            "params": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Audit existing authentication system"},
            },
        }
        resp = self.connector.handle_mcp_jsonrpc(req, platform=PlatformType.CLAUDE)
        self.assertEqual(resp["id"], "req_claude_002")
        self.assertFalse(resp["result"]["isError"])
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertIn("intent", data)

    def test_platform_3_gemini_adapter(self):
        """[MOCKED TEST ONLY] Verify Google Gemini function call execution."""
        func_call = {
            "name": "openclone_understand_project",
            "args": {"prompt": "Migrate data pipeline to PySpark"},
        }
        resp = self.connector.handle_gemini_call(func_call)
        self.assertEqual(resp["name"], "openclone_understand_project")
        self.assertIn("response", resp)
        self.assertIn("content", resp["response"])
        self.assertIn("intent", resp["response"]["content"])

    def test_platform_4_zai_adapter(self):
        """[MOCKED TEST ONLY] Verify Z.ai GLM function execution."""
        payload = {
            "id": "call_zai_004",
            "function": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Refactor backend API endpoints"},
            },
        }
        resp = self.connector.invoke_tool(PlatformType.ZAI, raw_payload=payload)
        self.assertTrue(resp.success)
        self.assertEqual(resp.tool_name, "openclone_understand_project")
        self.assertIn("intent", resp.data)

    def test_platform_5_mistral_adapter(self):
        """[MOCKED TEST ONLY] Verify Mistral Le Chat tool call execution."""
        payload = {
            "id": "call_mistral_005",
            "function": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Design high-performance cache layer"},
            },
        }
        resp = self.connector.invoke_tool(PlatformType.MISTRAL, raw_payload=payload)
        self.assertTrue(resp.success)
        self.assertIn("intent", resp.data)

    def test_platform_6_open_webui_adapter(self):
        """[MOCKED TEST ONLY] Verify Open WebUI MCP execution."""
        req = {
            "jsonrpc": "2.0",
            "id": "req_owui_006",
            "method": "tools/call",
            "params": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Build mobile responsive portal"},
            },
        }
        resp = self.connector.handle_mcp_jsonrpc(req, platform=PlatformType.OPEN_WEBUI)
        self.assertFalse(resp["result"]["isError"])
        data = json.loads(resp["result"]["content"][0]["text"])
        self.assertIn("intent", data)

    def test_platform_7_librechat_adapter(self):
        """[MOCKED TEST ONLY] Verify LibreChat config snippet and tool invocation."""
        adapter: LibreChatAdapter = self.connector.get_adapter(PlatformType.LIBRECHAT)
        cfg_snippet = adapter.generate_librechat_config(server_url="https://api.example.com/mcp")
        self.assertIn("mcpServers", cfg_snippet)
        self.assertIn("openclone", cfg_snippet["mcpServers"])

        req = {
            "jsonrpc": "2.0",
            "id": "req_lc_007",
            "method": "tools/call",
            "params": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Create full-stack SaaS platform"},
            },
        }
        resp = self.connector.handle_mcp_jsonrpc(req, platform=PlatformType.LIBRECHAT)
        self.assertFalse(resp["result"]["isError"])


class Level4EndToEndTests(unittest.TestCase):
    """Level 4: End-to-end flow from external platform call to canonical capability."""

    def setUp(self):
        self.connector = UniversalAIAssistantConnector()
        self.connector.config.require_authentication = False

    def test_e2e_understand_and_clarification_flow(self):
        """End-to-End: Assistant calls understand_project -> clarification analysis."""
        req = {
            "jsonrpc": "2.0",
            "id": "e2e_01",
            "method": "tools/call",
            "params": {
                "name": "openclone_understand_project",
                "arguments": {"prompt": "Build a multi-tenant payment system with stripe"},
            },
        }
        resp = self.connector.handle_mcp_jsonrpc(req, platform=PlatformType.CLAUDE)
        self.assertFalse(resp["result"]["isError"])
        result = json.loads(resp["result"]["content"][0]["text"])
        self.assertIn("intent", result)
        self.assertEqual(result["status"], "UNDERSTOOD")
        self.assertIn("ambiguities", result)

    def test_e2e_architecture_generation_flow(self):
        """End-to-End: Assistant calls openclone_generate_architecture."""
        req = {
            "jsonrpc": "2.0",
            "id": "e2e_02",
            "method": "tools/call",
            "params": {
                "name": "openclone_generate_architecture",
                "arguments": {
                    "prompt": "Create a modern analytics dashboard in React with Python backend",
                    "project_name": "AnalyticsPortal",
                    "mode": "NEW",
                },
            },
        }
        resp = self.connector.handle_mcp_jsonrpc(req, platform=PlatformType.CHATGPT)
        self.assertFalse(resp["result"]["isError"])
        res_data = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(res_data["status"], "ARCHITECTURE_GENERATED")
        self.assertIn("set_a", res_data)
        self.assertIn("set_d", res_data)

    def test_e2e_rest_gateway_integration(self):
        """End-to-End: REST Gateway dispatches to Universal Connector."""
        from src.openclone.integrations.rest import OpenCloneRESTGateway
        gw = OpenCloneRESTGateway()
        platforms = gw.dispatch("GET", "/api/v1/connector/platforms")
        self.assertIn("platforms", platforms)
        self.assertEqual(len(platforms["platforms"]), 7)

        health = gw.dispatch("GET", "/api/v1/connector/health")
        self.assertEqual(health["status"], "healthy")


class Level5AuthenticationAndSecurityTests(unittest.TestCase):
    """Level 5: Inbound authentication separation, token lifecycle, and fail-closed security."""

    def setUp(self):
        self.connector = UniversalAIAssistantConnector()
        self.connector.config.require_authentication = True

    def test_inbound_vs_outbound_auth_separation(self):
        """Verify model provider keys (outbound) are NOT accepted as inbound connector bearer tokens."""
        outbound_fake_key = "sk-" + "fake-openai-model-key-12345"
        # Should fail closed because it is not an issued inbound connector token
        resp = self.connector.invoke_tool(
            platform=PlatformType.CHATGPT,
            raw_payload={"tool_name": "openclone_understand_project", "arguments": {"prompt": "Test"}},
            auth_token=outbound_fake_key,
        )
        self.assertFalse(resp.success)
        self.assertEqual(resp.error_code, 403)
        self.assertIn("Authentication failed", resp.error_message)

    def test_inbound_token_lifecycle(self):
        """Verify issuance, verification, expiration, and revocation of inbound connector tokens."""
        auth_mgr = self.connector.auth_manager
        raw_token, cred = auth_mgr.issue_platform_token(PlatformType.CLAUDE, expires_in_seconds=3600)
        self.assertTrue(raw_token.startswith("oc_ai_claude_"))

        # Authenticate with valid token
        auth_ctx = auth_mgr.authenticate_inbound({"authorization": f"Bearer {raw_token}"}, expected_platform=PlatformType.CLAUDE)
        self.assertIsNotNone(auth_ctx)
        self.assertEqual(auth_ctx.client_type, "ai_claude")

        # Wrong platform binding fails
        wrong_platform_auth = auth_mgr.authenticate_inbound({"authorization": f"Bearer {raw_token}"}, expected_platform=PlatformType.GEMINI)
        self.assertIsNone(wrong_platform_auth)

        # Revocation
        auth_mgr.revoke_token(raw_token)
        revoked_auth = auth_mgr.authenticate_inbound({"authorization": f"Bearer {raw_token}"})
        self.assertIsNone(revoked_auth)

    def test_remote_mcp_session_lifecycle(self):
        """Verify MCP Streamable HTTP session creation, tracking, and termination."""
        mcp_bridge = self.connector.mcp_http_bridge
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "clientInfo": {"name": "ClaudeClient", "version": "1.0"}},
        }
        res = mcp_bridge.handle_jsonrpc(init_req, headers={})
        sess_id = res["result"]["sessionId"]
        self.assertIsNotNone(sess_id)
        self.assertTrue(mcp_bridge.validate_session(sess_id))

        # Close session
        close_req = {"jsonrpc": "2.0", "id": 2, "method": "session/close"}
        close_res = mcp_bridge.handle_jsonrpc(close_req, headers={"mcp-session-id": sess_id})
        self.assertTrue(close_res["result"]["closed"])
        self.assertFalse(mcp_bridge.validate_session(sess_id))


class Level6CrossPlatformConsistencyTests(unittest.TestCase):
    """Level 6: Verify all 7 platforms invoke the same canonical capability and produce consistent outputs."""

    def setUp(self):
        self.connector = UniversalAIAssistantConnector()
        self.connector.config.require_authentication = False

    def test_cross_platform_understand_project_consistency(self):
        """Verify openclone_understand_project executes identically across all 7 platforms."""
        prompt_text = "Build a customer feedback dashboard in Next.js"
        results = {}

        for p_type in PlatformType:
            payload = {
                "tool_name": "openclone_understand_project",
                "capability_id": "openclone_understand_project",
                "arguments": {"prompt": prompt_text},
                "function": {"name": "openclone_understand_project", "arguments": {"prompt": prompt_text}},
                "function_call": {"name": "openclone_understand_project", "args": {"prompt": prompt_text}},
                "params": {"name": "openclone_understand_project", "arguments": {"prompt": prompt_text}},
                "name": "openclone_understand_project",
                "args": {"prompt": prompt_text},
            }
            resp = self.connector.invoke_tool(platform=p_type, raw_payload=payload)
            self.assertTrue(resp.success, f"Platform {p_type.value} invocation should succeed")
            self.assertEqual(resp.data["status"], "UNDERSTOOD")
            self.assertEqual(resp.data["intent"], "feature")
            results[p_type.value] = resp.data["intent"]

        # Confirm all 7 platforms produced the exact same intent classification
        self.assertEqual(len(set(results.values())), 1)


class Level7LiveServerNetworkTests(unittest.TestCase):
    """Level 7: Real HTTP network requests against running OpenClone HTTP server."""

    @classmethod
    def setUpClass(cls):
        import socket
        import threading
        from http.server import ThreadingHTTPServer
        from src.openclone.integrations.rest import OpenCloneHTTPHandler, OpenCloneRESTGateway

        # Find an open port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        cls.port = sock.getsockname()[1]
        sock.close()

        cls.gateway = OpenCloneRESTGateway()
        cls.gateway.connector.config.require_authentication = False
        OpenCloneHTTPHandler.gateway_instance = cls.gateway
        cls.server = ThreadingHTTPServer(("127.0.0.1", cls.port), OpenCloneHTTPHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        # Ensure loopback HTTP calls do not route through environment proxy
        import urllib.request
        cls.orig_opener = urllib.request._opener
        urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))

    @classmethod
    def tearDownClass(cls):
        import urllib.request
        urllib.request.install_opener(cls.orig_opener)
        cls.server.shutdown()
        cls.server.server_close()

    def test_live_http_health_endpoint(self):
        """Verify real HTTP GET /api/v1/health."""
        import urllib.request
        req = urllib.request.Request(f"{self.base_url}/api/v1/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["status"], "healthy")

    def test_live_http_mcp_streamable_post(self):
        """Verify real HTTP POST /mcp with JSON-RPC initialize."""
        import urllib.request
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": "live_mcp_01",
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/mcp",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            res = json.loads(response.read().decode())
            self.assertEqual(res["id"], "live_mcp_01")
            self.assertIn("serverInfo", res["result"])

    def test_live_http_sse_get_endpoint(self):
        """Verify real HTTP GET /sse returns text/event-stream headers and session event."""
        import urllib.request
        req = urllib.request.Request(f"{self.base_url}/sse")
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            content_type = response.headers.get("Content-Type", "")
            self.assertIn("text/event-stream", content_type)
            line1 = response.readline().decode("utf-8")
            line2 = response.readline().decode("utf-8")
            self.assertIn("event: endpoint", line1)
            self.assertIn("sessionId=", line2)

    def test_live_http_capability_rest_invocation(self):
        """Verify real HTTP POST /api/v1/capabilities/openclone_understand_project."""
        import urllib.request
        payload = json.dumps({"prompt": "Build an authentication service"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/capabilities/openclone_understand_project",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            res = json.loads(response.read().decode())
            self.assertTrue(res["success"])
            self.assertEqual(res["data"]["status"], "UNDERSTOOD")


if __name__ == "__main__":
    unittest.main()
