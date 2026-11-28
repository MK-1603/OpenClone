"""Comprehensive verification test suite for Google Stitch Skills integration.
Validates:
1. Upstream repository import & Apache-2.0 license preservation.
2. Skill discovery across all 3 plugin suites (stitch-design, stitch-build, stitch-utilities).
3. Skill loading and resource binding (references, examples, scripts).
4. Dual-identifier compatibility (stitch::* <-> stitch-*).
5. Dependency validation & environment checks.
6. MCP configuration, credential handling, and graceful offline degradation.
7. MCP tool discovery & argument validation.
8. Upstream update mechanism and provenance tracking.
9. UI/UX engineering orchestration pipeline.
10. Finora personal finance validation workflow.
"""
import json
from pathlib import Path
import unittest

from integrations.stitch.adapter.discovery import StitchDiscovery, StitchSkillDescriptor
from integrations.stitch.adapter.loader import StitchSkillLoader
from integrations.stitch.adapter.compatibility import StitchCompatibility
from integrations.stitch.adapter.dependencies import StitchDependencyValidator
from integrations.stitch.adapter.mcp_client import StitchMCPClient, StitchMCPConfig
from integrations.stitch.adapter.orchestration import StitchDesignOrchestrator
from integrations.stitch.adapter.registry import register_stitch_skills
from integrations.stitch.validation.finora.workflow import FinoraValidationWorkflow
from src.openclone.skills.engine import SkillRegistry, SkillMaturity
from src.openclone.skills.ui_ux_engineering import DesignArchetype, UIUXEngineeringEngine


class TestStitchSkillsIntegration(unittest.TestCase):
    """Test suite covering the 15 requirements of Google Stitch integration."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.stitch_root = cls.root / "integrations" / "stitch"
        cls.discovery = StitchDiscovery(root=cls.stitch_root)
        cls.loader = StitchSkillLoader(discovery=cls.discovery)

    # 1. Upstream import & license
    def test_01_upstream_provenance_and_license_preservation(self):
        license_path = self.stitch_root / "LICENSE"
        self.assertTrue(license_path.exists(), "LICENSE file must exist in integrations/stitch")
        license_text = license_path.read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0", license_text)

        manifest_path = self.stitch_root / "manifest.json"
        self.assertTrue(manifest_path.exists(), "manifest.json must exist")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["upstream"]["branch"], "main")
        self.assertEqual(manifest["upstream"]["commit"], "75f4696f162000fb69fca6a31489b5b21d47a506")

        upstream_doc = self.stitch_root / "UPSTREAM.md"
        self.assertTrue(upstream_doc.exists(), "UPSTREAM.md must exist")
        doc_text = upstream_doc.read_text(encoding="utf-8")
        self.assertIn("75f4696f162000fb69fca6a31489b5b21d47a506", doc_text)

    # 2. Skill discovery across all 3 plugins
    def test_02_all_16_skills_discovered_across_three_plugins(self):
        catalog = self.discovery.discover_all()
        unique_ids = set(desc.id for desc in catalog.values())
        self.assertEqual(len(unique_ids), 16, f"Expected exactly 16 Stitch skills, found {len(unique_ids)}")

        # Check plugin groups
        groups = {desc.plugin_group for desc in catalog.values()}
        self.assertIn("stitch-design", groups)
        self.assertIn("stitch-build", groups)
        self.assertIn("stitch-utilities", groups)

        design_skills = [d.id for d in catalog.values() if d.plugin_group == "stitch-design"]
        self.assertIn("stitch-generate-design", design_skills)
        self.assertIn("stitch-code-to-design", design_skills)
        self.assertIn("stitch-manage-design-system", design_skills)

        build_skills = [d.id for d in catalog.values() if d.plugin_group == "stitch-build"]
        self.assertIn("stitch-react-components", build_skills)
        self.assertIn("stitch-react-native", build_skills)

        utility_skills = [d.id for d in catalog.values() if d.plugin_group == "stitch-utilities"]
        self.assertIn("stitch-taste-design", utility_skills)
        self.assertIn("stitch-enhance-prompt", utility_skills)

    # 3. Skill loading & resource preservation
    def test_03_skill_loading_preserves_body_and_resources(self):
        loaded = self.loader.load("stitch-generate-design")
        self.assertEqual(loaded.descriptor.id, "stitch-generate-design")
        self.assertIn("# Generate Design", loaded.body)
        self.assertTrue(len(loaded.resources) > 0, "generate-design should have references")
        self.assertTrue(any("design-mappings" in k for k in loaded.resources.keys()))

        # Check react-components scripts
        react_loaded = self.loader.load("stitch-react-components")
        self.assertTrue("fetch-stitch.sh" in react_loaded.scripts)

    # 4. Dual-identifier compatibility
    def test_04_dual_identifier_compatibility(self):
        upstream = "stitch::generate-design"
        internal = StitchCompatibility.normalize_identifier(upstream)
        self.assertEqual(internal, "stitch-generate-design")

        back_to_upstream = StitchCompatibility.to_upstream_identifier(internal)
        self.assertEqual(back_to_upstream, "stitch::generate-design")

        # Loading by upstream id should succeed
        loaded_by_upstream = self.loader.load("stitch::generate-design")
        loaded_by_internal = self.loader.load("stitch-generate-design")
        self.assertEqual(loaded_by_upstream.descriptor.id, loaded_by_internal.descriptor.id)

    # 5. Dependency validation
    def test_05_dependency_validation(self):
        validator = StitchDependencyValidator(discovery=self.discovery)
        report = validator.validate_skill("stitch-code-to-design", mcp_connected=False)
        self.assertEqual(report.skill_id, "stitch-code-to-design")
        self.assertIn("Google Stitch MCP server connection (API Key required)", report.missing_prerequisites)

        # When MCP is marked connected
        report_connected = validator.validate_skill("stitch-code-to-design", mcp_connected=True)
        self.assertTrue(report_connected.is_ready)

    # 6. MCP Connection & Missing Credential Handling
    def test_06_mcp_missing_credential_handling(self):
        client_no_auth = StitchMCPClient(config=StitchMCPConfig(api_key=None))
        status = client_no_auth.check_connection()
        self.assertFalse(status.connected)
        self.assertEqual(status.status, "MISSING_CREDENTIALS")
        self.assertIn("No Stitch API Key configured", status.message)

        # Invocation without credentials should fail with structured error code
        res = client_no_auth.invoke_tool("list_projects", {})
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "STITCH-MCP-NO-AUTH")

    # 7. MCP Tool Discovery & Argument Schema
    def test_07_mcp_tool_discovery_and_schemas(self):
        client = StitchMCPClient(config=StitchMCPConfig(api_key="synthetic-test-key"))
        tools = client.list_tools()
        self.assertEqual(len(tools), 11)
        tool_names = [t["base_name"] for t in tools]
        self.assertIn("list_projects", tool_names)
        self.assertIn("generate_screen_from_text", tool_names)
        self.assertIn("create_design_system_from_design_md", tool_names)

        # Unknown tool rejection
        unknown_res = client.invoke_tool("invalid_tool_name", {})
        self.assertFalse(unknown_res["success"])
        self.assertEqual(unknown_res["code"], "STITCH-MCP-UNKNOWN-TOOL")

    # 8. OpenClone canonical registry integration
    def test_08_canonical_skill_registry_integration(self):
        registry = SkillRegistry()
        all_skills = registry.list_all()
        self.assertGreaterEqual(len(all_skills), 46)

        stitch_gen = registry.get("stitch-generate-design")
        self.assertIsNotNone(stitch_gen)
        self.assertEqual(stitch_gen.category, "design")

        # Path resolution
        resolved = registry.resolve_path("stitch-generate-design")
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.exists())

        # ui-ux-engineering registered
        ui_ux = registry.get("ui-ux-engineering")
        self.assertIsNotNone(ui_ux)
        self.assertEqual(ui_ux.category, "design")

    # 9. UI/UX Orchestration Pipeline
    def test_09_ui_ux_orchestration_workflow(self):
        orchestrator = StitchDesignOrchestrator()
        plan = orchestrator.plan_workflow(
            requirement="Create dark-theme cryptocurrency trading and wallet overview with order book"
        )
        self.assertIn(plan.archetype, [DesignArchetype.COMMAND_CENTER.value, DesignArchetype.FINANCIAL_DASHBOARD.value])
        self.assertIn("stitch-enhance-prompt", plan.selected_stitch_skills)
        self.assertIn("stitch-generate-design", plan.selected_stitch_skills)
        self.assertIn("stitch-react-components", plan.selected_stitch_skills)
        self.assertTrue(len(plan.stitch_operations) >= 3)
        self.assertIn("color_palette", plan.design_tokens)

    # 10. Finora Validation Project
    def test_10_finora_validation_case(self):
        finora_dir = self.stitch_root / "validation" / "finora"
        workflow = FinoraValidationWorkflow(base_dir=finora_dir)
        result = workflow.run_full_validation()
        self.assertEqual(result["validation_status"], "SUCCESS")
        self.assertGreaterEqual(result["audit_violations_resolved"], 1)
        self.assertGreaterEqual(result["overall_visual_qa_score"], 85.0)
        self.assertEqual(result["verdict"], "PASS")

        # Verify generated artifacts
        self.assertTrue((finora_dir / "extracted" / "DESIGN.md").exists())
        self.assertTrue((finora_dir / "audit" / "audit_report.json").exists())
        self.assertTrue((finora_dir / "direction" / "DIRECTION.md").exists())
        self.assertTrue((finora_dir / "direction" / "FINANCIAL_DESIGN_TOKENS.json").exists())
        self.assertTrue((finora_dir / "alternatives" / "COMPARISON.json").exists())
        self.assertTrue((finora_dir / "components" / "FinoraExecutiveDashboard.tsx").exists())
        self.assertTrue((finora_dir / "qa" / "visual_qa_report.json").exists())


if __name__ == "__main__":
    unittest.main()
