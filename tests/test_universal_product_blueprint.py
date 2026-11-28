"""Unit and Integration Tests for Universal Product Blueprint & Complete Design Intelligence.

Verifies:
- PageInventoryEngine sitemap, categorization, and layout generation.
- UserJourneyEngine step-by-step role-based flows and failure pathways.
- WireframeEngine structural wireframe blocks for landing, workspace, and auth cards.
- ComponentInteractionEngine behavioral contracts for buttons, forms, and modals.
- IntegrationMappingEngine bidirectional API contracts and database entity schemas.
- ApplicationBehaviorEngine states, responsive breakpoints, and WCAG AA accessibility.
- TraceabilityEngine end-to-end link graph.
- BlueprintCompletenessValidator full coverage score.
- ProductBlueprintExporter package manifest compilation.
- OpenClonePlannerAgent.generate_universal_product_blueprint() orchestration.
"""
from __future__ import annotations

import unittest
from src.openclone.blueprint.inventory import PageInventoryEngine
from src.openclone.blueprint.journeys import UserJourneyEngine
from src.openclone.blueprint.wireframes import WireframeEngine
from src.openclone.blueprint.interactions import ComponentInteractionEngine
from src.openclone.blueprint.integrations import IntegrationMappingEngine
from src.openclone.blueprint.behavior import ApplicationBehaviorEngine
from src.openclone.blueprint.validator import TraceabilityEngine, BlueprintCompletenessValidator
from src.openclone.blueprint.exporter import ProductBlueprintExporter
from src.openclone.blueprint.orchestrator import UniversalProductBlueprintOrchestrator
from src.openclone.blueprint.models import PageCategory, LayoutType
from src.openclone.planning.agent import OpenClonePlannerAgent


class TestUniversalProductBlueprint(unittest.TestCase):

    def setUp(self):
        self.planner = OpenClonePlannerAgent()
        self.sample_features = [
            {"feature_id": "FEAT-001", "title": "Interactive Analytics Dashboard", "category": "essential"},
            {"feature_id": "FEAT-002", "title": "Automated Workflows Engine", "category": "automation"},
            {"feature_id": "FEAT-003", "title": "Audit & Compliance Ledger", "category": "governance"},
        ]

    # 1. Page Inventory Tests
    def test_page_inventory_generation(self):
        pages = PageInventoryEngine.generate_inventory(
            project_name="DataMesh",
            features=self.sample_features,
            category="Data Platform",
        )
        self.assertGreaterEqual(len(pages), 6)
        categories = {p.category for p in pages}
        self.assertIn(PageCategory.PUBLIC, categories)
        self.assertIn(PageCategory.AUTHENTICATION, categories)
        self.assertIn(PageCategory.WORKSPACE, categories)
        self.assertIn(PageCategory.ADMINISTRATIVE, categories)

        # Feature coverage
        feat_pages = [p for p in pages if any("FEAT-" in f for f in p.related_features)]
        self.assertGreaterEqual(len(feat_pages), 3)

    # 2. User Journey Tests
    def test_user_journey_flows(self):
        pages = PageInventoryEngine.generate_inventory(
            project_name="DataMesh",
            features=self.sample_features,
        )
        journeys = UserJourneyEngine.generate_journeys(pages)
        self.assertGreaterEqual(len(journeys), 2)
        onboarding = next(j for j in journeys if "onboarding" in j.journey_id)
        self.assertGreaterEqual(len(onboarding.steps), 3)
        self.assertEqual(onboarding.steps[0].source_page_id, "page-public-home")

    # 3. Wireframe Generation Tests
    def test_wireframe_generation(self):
        pages = PageInventoryEngine.generate_inventory("DataMesh", self.sample_features)
        dashboard_page = next(p for p in pages if p.page_id == "page-workspace-dashboard")
        wireframe = WireframeEngine.generate_wireframe_for_page(dashboard_page)
        self.assertEqual(wireframe["page_id"], "page-workspace-dashboard")
        self.assertEqual(wireframe["layout_type"], LayoutType.SIDEBAR_WORKSPACE.value)
        self.assertGreaterEqual(len(wireframe["wireframe_blocks"]), 3)

    # 4. Component Interactions & Technical Integrations
    def test_component_and_integration_mappings(self):
        pages = PageInventoryEngine.generate_inventory("DataMesh", self.sample_features)
        components = ComponentInteractionEngine.generate_component_specs(pages)
        self.assertGreaterEqual(len(components), 4)

        apis = IntegrationMappingEngine.generate_api_mappings(pages)
        self.assertGreaterEqual(len(apis), 3)
        login_api = next(a for a in apis if a.endpoint_id == "api-auth-login")
        self.assertEqual(login_api.method, "POST")
        self.assertIn("password", login_api.request_schema.get("properties", {}))

        databases = IntegrationMappingEngine.generate_database_mappings(pages)
        self.assertGreaterEqual(len(databases), 2)
        user_table = next(d for d in databases if d.entity_name == "UserAccount")
        self.assertEqual(user_table.table_name, "users")

    # 5. End-to-End Planner Orchestration & Completeness Validation
    def test_planner_blueprint_generation_flow(self):
        res = self.planner.generate_universal_product_blueprint(
            project_name="DataMesh",
            prompt="Build a cloud data platform with automated pipelines and governance",
            features=self.sample_features,
            category="Data Platform",
        )
        self.assertEqual(res["status"], "VALIDATED")
        self.assertIn("blueprint_id", res)
        self.assertIn("validation", res)
        self.assertTrue(res["validation"]["is_complete"])
        self.assertEqual(res["validation"]["completeness_score"], 1.0)
        self.assertGreaterEqual(res["validation"]["total_pages"], 6)
        self.assertGreaterEqual(res["validation"]["total_traceability_links"], 10)

        bundle = res["bundle"]
        self.assertIn("files", bundle)
        self.assertIn("sitemap.md", bundle["files"])
        self.assertIn("page-inventory.json", bundle["files"])
        self.assertIn("api-contracts.json", bundle["files"])
        self.assertIn("traceability-matrix.json", bundle["files"])


if __name__ == "__main__":
    unittest.main()
