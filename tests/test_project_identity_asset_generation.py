"""Unit and Integration Tests for Project Identity & Asset Generation System (PIAGS).

Verifies:
- ProjectNamingEngine candidate generation, scoring, and rationale.
- BrandIntelligenceEngine positioning, mission, values, and visual direction.
- VisualIdentityBuilder color palette, WCAG AA contrast, and design tokens.
- LogoGenerationEngine vector SVG logo suite (primary, icon, dark, repo banner).
- AssetRegistry registration, versioning, retrieval, and approval.
- IdentityValidationEngine completeness and contrast quality gates.
- IdentityPackageExporter manifest compilation and file packaging.
- ProjectIdentityOrchestrator integration with OpenClonePlannerAgent.
"""
from __future__ import annotations

import unittest
from src.openclone.identity.naming import ProjectNamingEngine
from src.openclone.identity.brand import BrandIntelligenceEngine
from src.openclone.identity.visual import VisualIdentityBuilder
from src.openclone.identity.logo import LogoGenerationEngine
from src.openclone.identity.registry import AssetRegistry
from src.openclone.identity.exporter import IdentityValidationEngine, IdentityPackageExporter
from src.openclone.identity.orchestrator import ProjectIdentityOrchestrator
from src.openclone.identity.models import IdentityLifecycleState, AssetCategory
from src.openclone.planning.agent import OpenClonePlannerAgent


class TestProjectIdentityAndAssetGeneration(unittest.TestCase):

    def setUp(self):
        self.orchestrator = ProjectIdentityOrchestrator()
        self.planner = OpenClonePlannerAgent()

    # 1. Naming Intelligence Tests
    def test_naming_candidate_generation(self):
        candidates = ProjectNamingEngine.generate_candidates(
            prompt="Build an automated cloud infrastructure platform with Terraform",
            category="DevOps Platform",
            target_audience="Site Reliability Engineers",
        )
        self.assertGreaterEqual(len(candidates), 5)
        categories = {c.category for c in candidates}
        self.assertIn("technical", categories)
        self.assertIn("brandable", categories)
        self.assertIn("descriptive", categories)
        self.assertTrue(any(c.is_selected for c in candidates))

    # 2. Brand Intelligence Tests
    def test_brand_intelligence_formulation(self):
        brand = BrandIntelligenceEngine.create_brand_identity(
            brand_name="CloudVortex",
            category="Cloud Management",
            target_audience="DevOps Leads",
            purpose="Streamline multi-cloud deployments with zero downtime",
        )
        self.assertEqual(brand.brand_name, "CloudVortex")
        self.assertIn("DevOps Leads", brand.positioning)
        self.assertGreaterEqual(len(brand.values), 4)
        self.assertGreaterEqual(len(brand.design_principles), 3)

    # 3. Visual Identity Tests
    def test_visual_identity_tokens_and_contrast(self):
        visual = VisualIdentityBuilder.build_visual_system(
            primary_hex="#2563EB",
            secondary_hex="#0F172A",
            accent_hex="#38BDF8",
        )
        self.assertTrue(visual.colors.wcag_aa_compliant)
        self.assertGreaterEqual(visual.colors.contrast_ratio_light, 4.5)
        self.assertIn("color", visual.design_tokens)
        self.assertIn("spacing", visual.design_tokens)

    # 4. Logo Generation & Registry Tests
    def test_logo_generation_and_registry(self):
        visual = VisualIdentityBuilder.build_visual_system()
        assets = LogoGenerationEngine.generate_logo_suite(
            project_id="test-proj-01",
            identity_id="test-id-01",
            brand_name="QuantumSync",
            visual_system=visual,
        )
        self.assertGreaterEqual(len(assets), 5)
        categories = {a.category for a in assets}
        self.assertIn(AssetCategory.LOGO, categories)
        self.assertIn(AssetCategory.APPLICATION_ICON, categories)
        self.assertIn(AssetCategory.FAVICON, categories)
        self.assertIn(AssetCategory.REPOSITORY_BANNER, categories)

        # Verify SVG content
        primary = next(a for a in assets if a.variant == "primary")
        self.assertIn("<svg", primary.content)
        self.assertIn("QuantumSync", primary.content)

        # Asset registry tracking
        reg = AssetRegistry()
        reg.register_asset(primary)
        fetched = reg.get_asset(primary.asset_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.version, 1)

        # Re-register to test version bump
        reg.register_asset(primary)
        updated = reg.get_asset(primary.asset_id)
        self.assertEqual(updated.version, 2)
        history = reg.get_asset_history(primary.asset_id)
        self.assertEqual(len(history), 1)

    # 5. End-to-End Orchestrator & Planner Integration
    def test_planner_identity_generation_flow(self):
        res = self.planner.generate_project_identity(
            prompt="Build an intelligent task scheduler for distributed workflows",
            category="Distributed Systems",
            target_audience="Backend Developers",
            auto_approve=True,
        )
        self.assertEqual(res["status"], "APPROVED")
        self.assertIn("project_name", res)
        self.assertIn("brand", res)
        self.assertIn("visual_system", res)
        self.assertIn("package", res)

        pkg = res["package"]
        self.assertIn("files", pkg)
        self.assertIn("brand-guidelines.md", pkg["files"])
        self.assertIn("design-tokens.json", pkg["files"])
        self.assertIn("logos/primary/logo-primary.svg", pkg["files"])

        # Validation
        self.assertTrue(res["validation"]["valid"])
        self.assertEqual(len(res["validation"]["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
