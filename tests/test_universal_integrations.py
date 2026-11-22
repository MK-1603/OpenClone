"""Unit and integration tests for OpenClone Universal AI Tool Integration & Gateway."""

import json
import unittest
from pathlib import Path

from src.openclone.integrations.capabilities import (
    CapabilityCategory,
    RiskClassification,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import (
    AuthContext,
    IntegrationGateway,
    PolicyVerdict,
    redact_secrets,
)
from src.openclone.integrations.openapi import generate_openapi_spec, dispatch_rest_request
from src.openclone.mcp.server import OpenCloneMCPServer


class UniversalIntegrationsTests(unittest.TestCase):
    """Test suite verifying universal integration core, gateway, and adapters."""

    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.registry = get_canonical_registry(self.root)
        self.gateway = IntegrationGateway(self.registry, self.root)

    def test_canonical_capability_registry(self):
        """Verify canonical capabilities are registered and schemas valid."""
        caps = self.registry.list_capabilities()
        self.assertGreaterEqual(len(caps), 12)

        # Check category filter
        discovery_caps = self.registry.list_capabilities(CapabilityCategory.PROJECT_DISCOVERY)
        self.assertTrue(any(c.id == "openclone_list_projects" for c in discovery_caps))

        # Check MCP tool conversion
        mcp_tools = self.registry.get_mcp_tools()
        self.assertTrue(any(t["name"] == "openclone_get_checklist" for t in mcp_tools))

    def test_gateway_authentication_and_scopes(self):
        """Verify token authentication and scope enforcement."""
        # Valid maintainer token
        auth_admin = self.gateway.authenticate_token("test-valid-token")
        self.assertIsNotNone(auth_admin)
        self.assertTrue(auth_admin.is_human)

        # Execute allowed read capability
        res = self.gateway.execute(auth_admin, "openclone_list_projects", {})
        self.assertIn("projects", res)

        # Read-only token attempting write action
        auth_ro = self.gateway.authenticate_token("test-ro-token")
        self.assertIsNotNone(auth_ro)
        with self.assertRaises(PermissionError) as cm:
            self.gateway.execute(
                auth_ro,
                "openclone_update_task_status",
                {"item_id": "TASK_01", "new_status": "IN_PROGRESS"},
            )
        self.assertIn("Missing required scope", str(cm.exception))

    def test_gateway_cross_project_isolation(self):
        """Verify cross-project boundary isolation is strictly enforced."""
        auth = AuthContext(
            user_id="user_tenant_a",
            project_id="tenant_a_project",
            scopes={"projects:read"},
        )
        # Attempt to access tenant_b_project
        with self.assertRaises(PermissionError) as cm:
            self.gateway.execute(
                auth,
                "openclone_get_project_context",
                {"project_id": "tenant_b_project"},
            )
        self.assertIn("Cross-project access violation", str(cm.exception))

    def test_gateway_human_approval_enforcement(self):
        """Verify that high-risk production-impact actions require cryptographic approval."""
        auth = self.gateway.authenticate_token("test-valid-token")
        self.assertIsNotNone(auth)

        # Attempt release deployment without valid SHA-256 digest
        with self.assertRaises(PermissionError) as cm:
            self.gateway.execute(
                auth,
                "openclone_approve_release_deployment",
                {"target_environment": "production", "approval_digest": "short_invalid"},
            )
        self.assertIn("Approval Required", str(cm.exception))

        # With 64-char SHA-256 digest
        valid_digest = "a" * 64
        res = self.gateway.execute(
            auth,
            "openclone_approve_release_deployment",
            {"target_environment": "production", "approval_digest": valid_digest},
            approval_digest=valid_digest,
        )
        self.assertTrue(res["authorized"])

    def test_gateway_cryptographic_approval_record_lifecycle(self):
        """Verify structured cryptographic approval generation, verification, and replay rejection."""
        auth = self.gateway.authenticate_token("test-valid-token")
        args = {"target_environment": "production", "release_id": "v1.0.0"}
        
        # 1. Create cryptographic approval record
        approval_rec = self.gateway.create_approval_record(auth, "openclone_approve_release_deployment", args)
        self.assertIn("approval_id", approval_rec)
        self.assertIn("nonce", approval_rec)
        self.assertIn("signature", approval_rec)

        # 2. Execute with valid approval record
        exec_args = dict(args)
        exec_args["approval_record"] = approval_rec
        res = self.gateway.execute(auth, "openclone_approve_release_deployment", exec_args)
        self.assertTrue(res["authorized"])

        # 3. Replay attack rejection: using same approval record/nonce
        with self.assertRaises(PermissionError) as cm:
            self.gateway.execute(auth, "openclone_approve_release_deployment", exec_args)
        self.assertIn("Replay detected", str(cm.exception))

        # 4. Tampered payload rejection: modified argument
        tampered_rec = self.gateway.create_approval_record(auth, "openclone_approve_release_deployment", args)
        tampered_args = dict(args)
        tampered_args["target_environment"] = "staging"  # modified after approval!
        tampered_args["approval_record"] = tampered_rec
        with self.assertRaises(PermissionError) as cm_tamper:
            self.gateway.execute(auth, "openclone_approve_release_deployment", tampered_args)
        self.assertIn("Payload digest mismatch", str(cm_tamper.exception))

    def test_evidence_integrity_and_containment(self):
        """Verify evidence attachment validates workspace containment and computes SHA-256."""
        auth = self.gateway.authenticate_token("test-valid-token")

        # 1. Path traversal escape rejection
        with self.assertRaises(PermissionError) as cm:
            self.gateway.execute(
                auth,
                "openclone_submit_evidence",
                {
                    "item_id": "TASK_01",
                    "evidence_type": "code_diff",
                    "artifact_path": "../../secret.txt",
                    "summary": "Malicious traversal",
                },
            )
        self.assertIn("escapes workspace boundary", str(cm.exception))

        # 2. Valid file submission
        res = self.gateway.execute(
            auth,
            "openclone_submit_evidence",
            {
                "item_id": "TASK_01",
                "evidence_type": "code_diff",
                "artifact_path": "VERSION",
                "summary": "Verified version file",
            },
        )
        self.assertEqual(res["status"], "ATTACHED")
        self.assertTrue(res["verified"])
        self.assertIsNotNone(res["sha256_hash"])
        self.assertGreater(res["file_size"], 0)

    def test_gateway_secret_redaction(self):
        """Verify credentials and secret tokens are stripped from inputs/outputs."""
        dirty = {
            "api_key": "sk-proj-secret12345678",
            "safe": "normal_value",
            "nested": {"token": "ghp_1234567890abcdef"},
        }
        clean = redact_secrets(dirty)
        self.assertIn("***REDACTED***", clean["api_key"])
        self.assertIn("***REDACTED***", clean["nested"]["token"])
        self.assertEqual(clean["safe"], "normal_value")

    def test_openapi_spec_generation_and_rest_dispatch(self):
        """Verify OpenAPI 3.1 specification generation and REST request dispatch."""
        spec = generate_openapi_spec(self.registry)
        self.assertEqual(spec["openapi"], "3.1.0")
        self.assertIn("/capabilities/openclone_list_projects", spec["paths"])

        # Test REST dispatch
        auth = self.gateway.authenticate_token("test-valid-token")
        res = dispatch_rest_request(
            self.gateway,
            auth,
            method="GET",
            path="/v1/capabilities/openclone_list_projects",
        )
        self.assertIn("projects", res)

    def test_mcp_server_extended_tools(self):
        """Verify that OpenCloneMCPServer supports canonical capability tools."""
        server = OpenCloneMCPServer(self.root)

        # Tools list with canonical capabilities
        resp = server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {"all": True}})
        tools = resp["result"]["tools"]
        tool_names = {t["name"] for t in tools}
        self.assertIn("openclone_get_status", tool_names)
        self.assertIn("openclone_list_projects", tool_names)
        self.assertIn("openclone_get_checklist", tool_names)

        # Call canonical tool over MCP
        call_resp = server.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "openclone_list_projects",
                "arguments": {},
            },
        })
        self.assertFalse(call_resp.get("result", {}).get("isError", True))
        content = json.loads(call_resp["result"]["content"][0]["text"])
        self.assertIn("projects", content)

    def test_mcp_server_resources_primitives(self):
        """Verify MCP resources/list and resources/read."""
        server = OpenCloneMCPServer(self.root)

        # resources/list
        list_resp = server.handle_request({"jsonrpc": "2.0", "id": 10, "method": "resources/list"})
        resources = list_resp["result"]["resources"]
        uris = {r["uri"] for r in resources}
        self.assertIn("openclone://project/overview", uris)
        self.assertIn("openclone://project/checklist", uris)

        # resources/read
        read_resp = server.handle_request({
            "jsonrpc": "2.0",
            "id": 11,
            "method": "resources/read",
            "params": {"uri": "openclone://project/overview"},
        })
        content_text = read_resp["result"]["contents"][0]["text"]
        data = json.loads(content_text)
        self.assertEqual(data["product"], "OpenClone")

    def test_mcp_server_prompts_primitives(self):
        """Verify MCP prompts/list and prompts/get."""
        server = OpenCloneMCPServer(self.root)

        # prompts/list
        list_resp = server.handle_request({"jsonrpc": "2.0", "id": 20, "method": "prompts/list"})
        prompts = list_resp["result"]["prompts"]
        prompt_names = {p["name"] for p in prompts}
        self.assertIn("openclone_plan_feature", prompt_names)
        self.assertIn("openclone_implement_task", prompt_names)

        # prompts/get
        get_resp = server.handle_request({
            "jsonrpc": "2.0",
            "id": 21,
            "method": "prompts/get",
            "params": {
                "name": "openclone_plan_feature",
                "arguments": {"feature_description": "User profile dashboard"},
            },
        })
        messages = get_resp["result"]["messages"]
        self.assertIn("OpenClone Project Architect", messages[0]["content"]["text"])


if __name__ == "__main__":
    unittest.main()
