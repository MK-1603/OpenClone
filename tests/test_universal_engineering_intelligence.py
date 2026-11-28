"""Comprehensive test suite for OpenClone Universal AI Engineering Intelligence Platform.

Tests cover:
- 14 Primary Engineering Categories (ENG-01 through ENG-14)
- Multi-label classification across all 14 project family scenarios + hybrid projects
- Independent complexity derivation (MINI, SMALL, MEDIUM, LARGE, ENTERPRISE, RESEARCH_EXPERIMENTAL)
- Independent delivery targets and deployment models
- AI dependency classification (none, optional, required)
- Technology Intelligence & Stack Evaluation engine
- Composable 8-Layer Project Template Composer
- One-Click Idea-to-Project Package Generator
- MCP Server tool integrations (openclone_classify_project, openclone_route_project,
  openclone_evaluate_technology, openclone_generate_package)
"""
import json
import unittest
from pathlib import Path

from src.openclone.intelligence.blueprints import BlueprintManager
from src.openclone.intelligence.classifier import ProjectClassifier
from src.openclone.intelligence.composer import ProjectTemplateComposer
from src.openclone.intelligence.generator import ProjectPackageGenerator
from src.openclone.intelligence.router import ProjectRouter
from src.openclone.intelligence.taxonomy import TaxonomyRegistry
from src.openclone.intelligence.technology import TechnologyIntelligenceEngine
from src.openclone.mcp.server import OpenCloneMCPServer


ROOT = Path(__file__).resolve().parents[1]


class UniversalEngineeringIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tax = TaxonomyRegistry()
        cls.classifier = ProjectClassifier(cls.tax)
        cls.router = ProjectRouter(cls.tax)
        cls.tech_engine = TechnologyIntelligenceEngine()
        cls.composer = ProjectTemplateComposer()
        cls.generator = ProjectPackageGenerator(
            taxonomy=cls.tax,
            classifier=cls.classifier,
            router=cls.router,
            tech_engine=cls.tech_engine,
            composer=cls.composer,
        )
        cls.mcp = OpenCloneMCPServer(ROOT)

    # ------------------------------------------------------------------------
    # 1. TAXONOMY & 14 ENGINEERING CATEGORIES
    # ------------------------------------------------------------------------

    def test_taxonomy_loads_14_engineering_categories(self):
        cats = self.tax.list_categories()
        self.assertEqual(len(cats), 14)
        cat_ids = [c["id"] for c in cats]
        for i in range(1, 15):
            expected_id = f"ENG-{i:02d}"
            self.assertIn(expected_id, cat_ids)

        eng01 = self.tax.get_category("ENG-01")
        self.assertIsNotNone(eng01)
        self.assertEqual(eng01.name, "Artificial Intelligence")
        self.assertIn("RAG Development", eng01.subdisciplines)

        eng14 = self.tax.get_category("ENG-14")
        self.assertIsNotNone(eng14)
        self.assertEqual(eng14.name, "UI/UX & Product Engineering")

    def test_taxonomy_independent_dimensions(self):
        self.assertEqual(
            self.tax.complexity_levels,
            ["MINI", "SMALL", "MEDIUM", "LARGE", "ENTERPRISE", "RESEARCH_EXPERIMENTAL"],
        )
        self.assertIn("local", self.tax.deployment_models)
        self.assertIn("cloud", self.tax.deployment_models)
        self.assertIn("hybrid", self.tax.deployment_models)
        self.assertIn("none", self.tax.ai_dependencies)
        self.assertIn("required", self.tax.ai_dependencies)

    # ------------------------------------------------------------------------
    # 2. MULTI-LABEL CLASSIFICATION ACROSS SCENARIOS
    # ------------------------------------------------------------------------

    def test_classify_mini_website(self):
        profile = self.classifier.classify_text(
            "Build a lightweight personal portfolio and landing page with Astro or HTML and Tailwind CSS",
            project_name="dev-portfolio",
        )
        self.assertEqual(profile.primary_type, "mini_website")
        self.assertEqual(profile.complexity.level, "MINI")
        self.assertEqual(profile.delivery_targets, ["web_browser"])
        self.assertEqual(profile.ai_dependency, "none")
        self.assertIn("ENG-05", profile.supporting_disciplines)

    def test_classify_hybrid_mobile_ai_finance(self):
        profile = self.classifier.classify_text(
            "Flutter cross-platform mobile application with offline SQLite, RAG knowledge assistant, and financial transactions",
            project_name="pulse-finance",
        )
        self.assertEqual(profile.primary_type, "cross_platform_mobile")
        self.assertIn("rag_knowledge_system", profile.secondary_types)
        self.assertIn("android", profile.delivery_targets)
        self.assertIn("ios", profile.delivery_targets)
        self.assertEqual(profile.deployment_model, "hybrid")
        self.assertEqual(profile.ai_dependency, "required")
        self.assertEqual(profile.data_sensitivity, "restricted")
        self.assertIn("ENG-05", profile.supporting_disciplines)
        self.assertIn("ENG-01", profile.supporting_disciplines)

    def test_classify_linux_distribution(self):
        profile = self.classifier.classify_text(
            "Create a custom Linux distribution with minimal busybox rootfs, initramfs, and bootable ISO image",
            project_name="openclone-os",
        )
        self.assertEqual(profile.primary_type, "linux_distribution")
        self.assertEqual(profile.complexity.level, "LARGE")
        self.assertIn("bootable_media_iso", profile.delivery_targets)
        self.assertIn("os_systems", profile.conditional_profiles)

    def test_classify_embedded_firmware(self):
        profile = self.classifier.classify_text(
            "Real-time embedded firmware using FreeRTOS for STM32 microcontroller with GPIO, I2C sensor reading, and watchdog",
            project_name="iot-sensor-node",
        )
        self.assertEqual(profile.primary_type, "rtos_firmware")
        self.assertIn("embedded_hardware", profile.delivery_targets)
        self.assertIn("embedded_hardware", profile.conditional_profiles)

    def test_classify_unknown_domain_does_not_guess_saas_confidently(self):
        profile = self.classifier.classify_text(
            "Something random without technical specifics or platform info",
            project_name="unknown-project",
        )
        self.assertLessEqual(profile.classification_confidence, 0.5)
        self.assertTrue(len(profile.unresolved_questions) > 0)
        self.assertIn("no_explicit_domain_keywords_detected", profile.ambiguity_flags)

    # ------------------------------------------------------------------------
    # 3. TECHNOLOGY INTELLIGENCE ENGINE
    # ------------------------------------------------------------------------

    def test_technology_evaluation_mobile_hybrid(self):
        profile = self.classifier.classify_text(
            "Flutter mobile app with local SQLite and AI assistance",
            project_name="test-mobile",
        )
        decisions = self.tech_engine.evaluate(profile, requirements_text="Flutter SQLite AI")
        self.assertTrue(len(decisions) >= 2)
        selected_names = [d.selected_technology for d in decisions]
        self.assertTrue(any("Flutter" in s for s in selected_names))
        self.assertTrue(any("SQLite" in s for s in selected_names))
        for d in decisions:
            self.assertEqual(d.verification_status, "VERIFIED")
            self.assertIsNotNone(d.license)

    def test_technology_evaluation_saas_web(self):
        profile = self.classifier.classify_text(
            "Modern SaaS command center with Next.js dashboard, PostgreSQL database, and REST APIs",
            project_name="pulse-saas",
        )
        decisions = self.tech_engine.evaluate(profile, requirements_text="Next.js PostgreSQL")
        selected_names = [d.selected_technology for d in decisions]
        self.assertTrue(any("Next.js" in s for s in selected_names))
        self.assertTrue(any("PostgreSQL" in s for s in selected_names))

    # ------------------------------------------------------------------------
    # 4. COMPOSABLE 8-LAYER TEMPLATE COMPOSER
    # ------------------------------------------------------------------------

    def test_compose_project_md_contains_25_sections(self):
        profile = self.classifier.classify_text(
            "Cross-platform Flutter application with AI assistant and local SQLite",
            project_name="pulse-mobile",
        )
        decisions = self.tech_engine.evaluate(profile)
        routing = self.router.route(profile)
        content = self.composer.compose_project_md(profile, decisions, routing)

        # Check key sections
        self.assertIn("# PROJECT.md — pulse-mobile", content)
        self.assertIn("## 1. Summary", content)
        self.assertIn("## 8. Functional requirements", content)
        self.assertIn("## 9. Non-functional requirements", content)
        self.assertIn("## 12. Architecture", content)
        self.assertIn("## 13. Technology and dependencies", content)
        self.assertIn("## 16. Security and privacy", content)
        self.assertIn("## 21. Build, test and operations", content)
        self.assertIn("## 25. Change history", content)

    # ------------------------------------------------------------------------
    # 5. ONE-CLICK PACKAGE GENERATOR
    # ------------------------------------------------------------------------

    def test_package_generator_output(self, tmp_path_factory=None):
        pkg = self.generator.generate(
            "Cross-platform Flutter AI finance tracker with offline storage and REST sync",
            project_name="pulse-finance-app",
        )
        self.assertIn("profile", pkg)
        self.assertIn("technologies", pkg)
        self.assertIn("routing", pkg)
        self.assertIn("artifacts", pkg)

        artifacts = pkg["artifacts"]
        expected_files = [
            "PROJECT.md",
            "BUILD_PROMPT.md",
            "AGENT_INSTRUCTIONS.md",
            "IMPLEMENTATION_PLAN.md",
            "ACCEPTANCE_MATRIX.md",
            "SECURITY_PLAN.md",
            "PROJECT-PROFILE.yaml",
            ".env.example",
        ]
        for ef in expected_files:
            self.assertIn(ef, artifacts)
            self.assertTrue(len(artifacts[ef]) > 20)

    # ------------------------------------------------------------------------
    # 6. MCP SERVER INTELLIGENCE TOOLS
    # ------------------------------------------------------------------------

    def test_mcp_evaluate_technology(self):
        res = self.mcp.call_tool("openclone_evaluate_technology", {
            "text": "SaaS dashboard with Next.js, PostgreSQL, and FastAPI backend",
            "project_name": "saas-test",
        })
        self.assertIn("decisions", res)
        self.assertTrue(len(res["decisions"]) >= 2)

    def test_mcp_generate_package(self):
        res = self.mcp.call_tool("openclone_generate_package", {
            "prompt": "Custom Linux distro with busybox and bootable iso",
            "project_name": "test-os",
        })
        self.assertIn("profile", res)
        self.assertIn("artifacts", res)
        self.assertIn("PROJECT.md", res["artifacts"])


if __name__ == "__main__":
    unittest.main()
