"""Design Intelligence and Multi-Category Differentiation Test Suite.

Verifies:
1. Multi-Category Differentiation: 5 distinct product categories (Personal Finance,
   SaaS Admin, AI Developer Tool, E-Commerce, Project Management) generate uniquely
   tailored layouts, palettes, typography scales, and information densities.
2. Anti-Slop Enforcement: Automated detection and rejection of AI cliches.
3. 12-Dimension Design Brief Synthesis.
4. 3-Concept Generation and 7-criteria comparative ranking.
5. 10-Dimension Visual QA Scorecard.
"""
import unittest

from src.openclone.skills.ui_ux_engineering import (
    UIUXEngineeringEngine,
    DesignArchetype,
    DesignBrief,
    DesignConcept,
    ConceptComparisonReport,
    VisualQAScorecard,
)


class TestDesignIntelligenceDifferentiation(unittest.TestCase):
    """Rigorous tests ensuring zero uncritical layout cloning across product categories."""

    def setUp(self):
        self.engine = UIUXEngineeringEngine()

    def test_01_five_product_categories_generate_divergent_briefs(self):
        """Verify 5 different product categories produce fundamentally differentiated briefs."""
        prompts = {
            "finance": "Personal finance and portfolio rebalancing terminal with live tickers",
            "saas_admin": "Multi-tenant B2B employee provisioning and compliance admin console",
            "ai_devtool": "Low-level WebAssembly compiler debugger with live AST visualizer",
            "ecommerce": "Artisanal luxury leather goods storefront and checkout bag",
            "project_mgmt": "Agile software sprint planner with kanban board and backlog",
        }

        briefs = {cat: self.engine.synthesize_design_brief(p, cat) for cat, p in prompts.items()}

        # 1. Densities must differ
        self.assertEqual(briefs["finance"].information_density, "ultra-compact")
        self.assertEqual(briefs["ai_devtool"].information_density, "compact")
        self.assertEqual(briefs["ecommerce"].information_density, "spacious")
        self.assertEqual(briefs["project_mgmt"].information_density, "balanced")

        # 2. Navigation requirements must differ
        navs = [b.navigation_requirements for b in briefs.values()]
        self.assertIn("command-palette", navs)
        self.assertIn("top-navbar", navs)
        self.assertIn("hybrid-dock", navs)
        self.assertIn("contextual-rail", navs)

        # 3. Data presentation needs must differ
        data_pres = [b.data_presentation_needs for b in briefs.values()]
        self.assertIn("tabular-ledger", data_pres)
        self.assertIn("document-stream", data_pres)
        self.assertIn("card-mosaic", data_pres)
        self.assertIn("kanban-matrix", data_pres)

        # 4. Brand palettes must differ
        palettes = [b.brand_identity["primary"] for b in briefs.values()]
        self.assertEqual(len(set(palettes)), 5, "All 5 categories must feature distinct primary color tokens")

    def test_02_three_concepts_generated_with_distinct_archetypes(self):
        """Verify 3 distinct concepts are generated and compared across 7 criteria."""
        brief = self.engine.synthesize_design_brief(
            prompt="Institutional wealth management portal for private equity partners",
            project_name="ApexWealth",
        )
        report = self.engine.generate_three_concepts(brief)

        self.assertEqual(len(report.concepts), 3)
        concept_names = [c.name for c in report.concepts]
        self.assertIn("Financial Command Terminal", concept_names)
        self.assertIn("Executive Wealth & Cash Flow Navigator", concept_names)
        self.assertIn("Transaction-First Settlement Workspace", concept_names)

        # Ensure scores across 7 criteria exist
        for c in report.concepts:
            self.assertEqual(len(c.scores), 7)
            self.assertIn("suitability", c.scores)
            self.assertIn("workflow_efficiency", c.scores)
            self.assertIn("hierarchy", c.scores)
            self.assertIn("distinction", c.scores)
            self.assertIn("a11y", c.scores)
            self.assertIn("responsive", c.scores)
            self.assertIn("feasibility", c.scores)

        # Winner must be selected with explanation
        self.assertIn(report.selected_concept_id, ["concept-a", "concept-b", "concept-c"])
        self.assertTrue(len(report.selection_explanation) > 20)

    def test_03_design_tokens_authenticity(self):
        """Tokens generated for Command Center vs Workspace vs SaaS Admin must differ."""
        cc_tokens = self.engine.generate_design_system_tokens(DesignArchetype.COMMAND_CENTER)
        ws_tokens = self.engine.generate_design_system_tokens(DesignArchetype.WORKSPACE_INTERFACE)
        saas_tokens = self.engine.generate_design_system_tokens(DesignArchetype.SAAS_ADMIN_APP)

        self.assertNotEqual(cc_tokens["font_family"], ws_tokens["font_family"])
        self.assertNotEqual(cc_tokens["color_palette"]["brand_accent"], saas_tokens["color_palette"]["brand_accent"])
        self.assertEqual(cc_tokens["density"], "compact")
        self.assertEqual(saas_tokens["density"], "comfortable")

    def test_04_anti_slop_catches_ai_templates(self):
        """Ensure automated detection catches meaningless AI blobs and uncritical 4-card KPI grids."""
        bad_code = """
        <div class="from-purple-600 to-indigo-600 blur-3xl">
          <div class="grid grid-cols-4 total users">
            <div class="backdrop-blur bg-white/5">Bad Card</div>
          </div>
        </div>
        """
        is_clean, violations = self.engine.audit_anti_slop(bad_code, DesignArchetype.COMMAND_CENTER)
        self.assertFalse(is_clean)
        self.assertEqual(len(violations), 3)

    def test_05_visual_qa_10_dimension_evaluation(self):
        """Verify 10 dimensions are objectively evaluated."""
        clean_component = """
        import React from "react";
        export const Terminal = () => (
          <div className="bg-[#0B0E14] text-white p-4 font-mono">
            <header className="flex justify-between items-center mb-4">
              <h1 className="text-sm font-semibold">Ledger</h1>
              <button className="px-2 py-1 bg-[#00D47E] text-black text-xs font-bold rounded">Trade</button>
            </header>
            <table className="w-full text-xs tabular-nums">
              <thead><tr><th>Asset</th><th>Price</th></tr></thead>
              <tbody><tr><td>BTC</td><td>$98,400.00</td></tr></tbody>
            </table>
          </div>
        );
        """
        scorecard = self.engine.evaluate_visual_qa(clean_component, DesignArchetype.COMMAND_CENTER)
        self.assertEqual(len(scorecard.dimensions), 10)
        self.assertEqual(scorecard.verdict, "PASS")
        self.assertGreaterEqual(scorecard.total_score, 85.0)


if __name__ == "__main__":
    unittest.main()
