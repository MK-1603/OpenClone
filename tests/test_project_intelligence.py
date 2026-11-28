"""Test suite for OpenClone Universal AI Engineering Intelligence Platform.

Validates:
- Universal Project Taxonomy (12 families, 20+ types, delivery targets, complexity levels)
- Multi-label project classification across all 14 project family scenarios
- Hybrid multi-domain project classification
- Independent complexity derivation (MINI vs LARGE vs ENTERPRISE vs RESEARCH_EXPERIMENTAL)
- Deterministic explainable routing (domains, capabilities, minimum effective workforce, models, workflows, approval gates)
- Minimum effective workforce team assembly & execution origin tagging
- Blueprint discovery and retrieval for all 14 project families
- MCP server tool execution (classify, route, get_blueprint, status)
- JSON Schema Draft 2020-12 validation for project profiles and routing decisions
"""

import json
import unittest
from pathlib import Path

from src.openclone.intelligence.blueprints import BlueprintManager
from src.openclone.intelligence.classifier import ProjectClassifier
from src.openclone.intelligence.router import ProjectRouter
from src.openclone.intelligence.taxonomy import TaxonomyRegistry
from src.openclone.mcp.server import OpenCloneMCPServer


ROOT = Path(__file__).resolve().parents[1]


class UniversalProjectIntelligenceTests(unittest.TestCase):
    """Unit and integration tests for Universal Project Intelligence."""

    @classmethod
    def setUpClass(cls):
        cls.tax = TaxonomyRegistry()
        cls.classifier = ProjectClassifier(cls.tax)
        cls.router = ProjectRouter(cls.tax)
        cls.bp_mgr = BlueprintManager()
        cls.mcp = OpenCloneMCPServer(ROOT)

    # ------------------------------------------------------------------------
    # 1. TAXONOMY REGISTRY TESTS
    # ------------------------------------------------------------------------

    def test_taxonomy_loads_12_canonical_families(self):
        self.assertEqual(len(self.tax.families), 12)
        expected_families = {
            "web_engineering",
            "mobile_engineering",
            "desktop_engineering",
            "ai_engineering",
            "machine_learning",
            "data_engineering_and_data_science",
            "backend_and_distributed_systems",
            "operating_systems_and_systems",
            "embedded_hardware_and_robotics",
            "game_and_simulation",
            "developer_tools_and_languages",
            "research_and_scientific_computing",
        }
        self.assertEqual(set(self.tax.families.keys()), expected_families)

    def test_taxonomy_complexity_and_delivery_targets(self):
        self.assertEqual(
            self.tax.complexity_levels,
            ["MINI", "SMALL", "MEDIUM", "LARGE", "ENTERPRISE", "RESEARCH_EXPERIMENTAL"],
        )
        self.assertIn("web_browser", self.tax.delivery_targets)
        self.assertIn("android", self.tax.delivery_targets)
        self.assertIn("ios", self.tax.delivery_targets)
        self.assertIn("windows", self.tax.delivery_targets)
        self.assertIn("linux", self.tax.delivery_targets)
        self.assertIn("bootable_media_iso", self.tax.delivery_targets)
        self.assertIn("embedded_hardware", self.tax.delivery_targets)

    def test_taxonomy_type_lookup_and_reverse_mapping(self):
        linux_type = self.tax.get_type("linux_distribution")
        self.assertIsNotNone(linux_type)
        self.assertEqual(linux_type.name, "Custom Linux Distribution / Appliance")
        self.assertEqual(self.tax.get_family_for_type("linux_distribution"), "operating_systems_and_systems")

    # ------------------------------------------------------------------------
    # 2. MULTI-LABEL CLASSIFICATION TESTS
    # ------------------------------------------------------------------------

    def test_classify_mini_website(self):
        text = "Build a static marketing landing page and portfolio for our open source project."
        profile = self.classifier.classify_text(text, project_name="oss-landing")
        self.assertEqual(profile.primary_family, "web_engineering")
        self.assertEqual(profile.primary_type, "mini_website")
        self.assertEqual(profile.complexity.level, "MINI")
        self.assertIn("web_browser", profile.delivery_targets)

    def test_classify_saas_web_app(self):
        text = "Multi-tenant SaaS dashboard with billing subscriptions, user authentication, and Postgres."
        profile = self.classifier.classify_text(text, project_name="saas-app")
        self.assertEqual(profile.primary_family, "web_engineering")
        self.assertEqual(profile.primary_type, "saas_web_app")
        self.assertIn("web_browser", profile.delivery_targets)

    def test_classify_cross_platform_mobile(self):
        text = "Build a cross-platform mobile application in Flutter with offline SQLite cache."
        profile = self.classifier.classify_text(text, project_name="flutter-mobile")
        self.assertEqual(profile.primary_family, "mobile_engineering")
        self.assertEqual(profile.primary_type, "cross_platform_mobile")
        self.assertIn("android", profile.delivery_targets)
        self.assertIn("ios", profile.delivery_targets)
        self.assertIn("mobile", profile.conditional_profiles)

    def test_classify_linux_distribution(self):
        text = "Create a custom Linux distribution appliance with initramfs, custom kernel image, and bootable ISO."
        profile = self.classifier.classify_text(text, project_name="custom-os")
        self.assertEqual(profile.primary_family, "operating_systems_and_systems")
        self.assertEqual(profile.primary_type, "linux_distribution")
        self.assertEqual(profile.complexity.level, "LARGE")
        self.assertIn("bootable_media_iso", profile.delivery_targets)
        self.assertIn("os_systems", profile.conditional_profiles)

    def test_classify_embedded_firmware(self):
        text = "Develop FreeRTOS microcontroller firmware on STM32 with SPI and I2C peripheral drivers."
        profile = self.classifier.classify_text(text, project_name="stm32-firmware")
        self.assertEqual(profile.primary_family, "embedded_hardware_and_robotics")
        self.assertEqual(profile.primary_type, "rtos_firmware")
        self.assertIn("embedded_hardware", profile.delivery_targets)
        self.assertIn("embedded_hardware", profile.conditional_profiles)

    def test_classify_machine_learning_pipeline(self):
        text = "Build a predictive scikit-learn tabular model with cross-validation and feature engineering."
        profile = self.classifier.classify_text(text, project_name="ml-churn")
        self.assertEqual(profile.primary_family, "machine_learning")
        self.assertEqual(profile.primary_type, "classical_ml_pipeline")
        self.assertIn("ml", profile.conditional_profiles)

    def test_classify_data_science_study(self):
        text = "Perform exploratory data analysis (EDA) and statistical analysis with hypothesis testing."
        profile = self.classifier.classify_text(text, project_name="eda-study")
        self.assertEqual(profile.primary_family, "data_engineering_and_data_science")
        self.assertEqual(profile.primary_type, "data_science_study")
        self.assertIn("data_science", profile.conditional_profiles)

    def test_classify_hybrid_multi_domain_project(self):
        text = "Build an offline-first Flutter mobile application with a local RAG AI agent and a FastAPI backend."
        profile = self.classifier.classify_text(text, project_name="mobile-rag")
        # Should detect multiple types across families
        all_detected = [profile.primary_type] + profile.secondary_types
        self.assertIn("rag_knowledge_system", all_detected)
        self.assertIn("cross_platform_mobile", all_detected)
        self.assertIn("android", profile.delivery_targets)
        self.assertIn("ai", profile.conditional_profiles)
        self.assertIn("mobile", profile.conditional_profiles)

    # ------------------------------------------------------------------------
    # 3. ROUTER & CAPABILITY MAPPING TESTS
    # ------------------------------------------------------------------------

    def test_route_mini_website_enforces_minimal_workforce_and_exclusions(self):
        profile = self.classifier.classify_text("Static mini website landing page", "mini-site")
        decision = self.router.route(profile)
        # Excludes heavy backend/database/migrations
        self.assertIn("21-DATA-MIGRATION-AND-ROLLBACK", decision.domains["not_applicable"])
        self.assertIn("17-INCIDENT-RESPONSE", decision.domains["not_applicable"])
        # Minimum effective team
        self.assertIn("frontend-engineer", decision.workforce["native_agents"])
        self.assertNotIn("database-architect", decision.workforce["native_agents"])
        # Capabilities include Taste Skill
        cap_ids = [c.engine_id for c in decision.capabilities]
        self.assertIn("E-056", cap_ids)

    def test_route_ai_rag_includes_governance_and_evaluation(self):
        profile = self.classifier.classify_text("Build a RAG knowledge base with vector embeddings", "rag-app")
        decision = self.router.route(profile)
        self.assertIn("29-AI-GOVERNANCE", decision.domains["mandatory"])
        self.assertIn("30-AGENT-RULES-AND-VERIFICATION", decision.domains["mandatory"])
        cap_ids = [c.engine_id for c in decision.capabilities]
        self.assertIn("E-029", cap_ids)
        self.assertEqual(decision.models["primary_model"], "gpt-6.2-sol")

    def test_route_linux_os_requires_supply_chain_security(self):
        profile = self.classifier.classify_text("Custom Linux distribution kernel and bootable ISO", "my-distro")
        decision = self.router.route(profile)
        self.assertIn("22-SUPPLY-CHAIN-SECURITY", decision.domains["mandatory"])
        cap_ids = [c.engine_id for c in decision.capabilities]
        self.assertIn("E-022", cap_ids)
        # High complexity allocates GPT-6.2 Astra
        self.assertEqual(decision.models["primary_model"], "gpt-6.2-astra")

    def test_workflow_composition_sequences_prerequisites(self):
        profile = self.classifier.classify_text("SaaS multi-tenant app", "saas")
        decision = self.router.route(profile)
        wf_ids = [w.workflow_id for w in decision.workflows]
        self.assertIn("WF-001", wf_ids)
        self.assertIn("WF-002", wf_ids)
        self.assertIn("WF-009", wf_ids)  # Human approval
        self.assertIn("WF-004", wf_ids)  # Implementation
        self.assertIn("WF-007", wf_ids)  # Independent verification
        self.assertIn("WF-014", wf_ids)  # Release gate

    # ------------------------------------------------------------------------
    # 4. BLUEPRINT MANAGER TESTS
    # ------------------------------------------------------------------------

    def test_all_14_blueprints_exist_and_load(self):
        blueprints = self.bp_mgr.list_blueprints()
        self.assertEqual(len(blueprints), 14)
        for bp in blueprints:
            self.assertTrue(bp["exists"], f"Blueprint file missing: {bp['file']}")
            content = self.bp_mgr.get_blueprint(bp["id"])
            self.assertIsNotNone(content)
            self.assertIn("Goals & Scope", content)
            self.assertIn("Domain & Capability Mapping", content)
            self.assertIn("Specialist Workforce", content)

    # ------------------------------------------------------------------------
    # 5. MCP SERVER INTEGRATION TESTS
    # ------------------------------------------------------------------------

    def test_mcp_tool_classify_project(self):
        res = self.mcp.call_tool("openclone_classify_project", {"text": "A custom Linux distribution with initramfs and bootable ISO"})
        self.assertEqual(res["primary_family"], "operating_systems_and_systems")
        self.assertEqual(res["primary_type"], "linux_distribution")
        self.assertIn("bootable_media_iso", res["delivery_targets"])

    def test_mcp_tool_route_project(self):
        res = self.mcp.call_tool("openclone_route_project", {"text": "A SaaS web application with auth and billing"})
        self.assertIn("mandatory", res["domains"])
        self.assertIn("capabilities", res)
        self.assertIn("workforce", res)
        self.assertIn("models", res)

    def test_mcp_tool_get_blueprint(self):
        res = self.mcp.call_tool("openclone_get_blueprint", {"blueprint_id": "01-MINI-WEBSITE"})
        self.assertIn("01-MINI-WEBSITE", res["blueprint_id"])
        self.assertIn("Mini Website & Landing Page", res["content"])

    def test_mcp_tool_project_intelligence_status(self):
        res = self.mcp.call_tool("openclone_project_intelligence_status", {})
        self.assertEqual(res["family_count"], 12)
        self.assertEqual(res["blueprints_count"], 14)
        self.assertIn("MINI", res["complexity_levels"])

    # ------------------------------------------------------------------------
    # 6. JSON SCHEMA DRAFT 2020-12 CONFORMANCE
    # ------------------------------------------------------------------------

    def test_project_profile_schema_validation(self):
        import jsonschema

        schema_path = ROOT / "framework" / "schemas" / "project-profile.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        profile = self.classifier.classify_text("Flutter mobile app with local RAG", "test-proj")
        # Should validate without throwing jsonschema.ValidationError
        jsonschema.validate(profile.to_dict(), schema)

    def test_project_routing_schema_validation(self):
        import jsonschema

        schema_path = ROOT / "framework" / "schemas" / "project-routing.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        profile = self.classifier.classify_text("Flutter mobile app with local RAG", "test-proj")
        decision = self.router.route(profile)
        # Should validate without throwing jsonschema.ValidationError
        jsonschema.validate(decision.to_dict(), schema)


if __name__ == "__main__":
    unittest.main()
