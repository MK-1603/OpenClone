"""Test suite for UI/UX Engineering Skill and Visual QA Engine."""
import unittest
from pathlib import Path

from src.openclone.skills.engine import SkillRegistry
from src.openclone.skills.ui_ux_engineering import (
    UIUXEngineeringEngine,
    DesignArchetype,
    VisualQAScorecard,
)


class TestUIUXEngineeringSkill(unittest.TestCase):
    """Tests for UI/UX Engineering skill registration, tokens, anti-slop, and Visual QA."""

    def setUp(self):
        self.registry = SkillRegistry()
        self.engine = UIUXEngineeringEngine()

    def test_skill_registration_and_path_resolution(self):
        skill = self.registry.get("ui-ux-engineering")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "design")
        self.assertEqual(skill.precedence, 9)

        resolved = self.registry.resolve_path("ui-ux-engineering")
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.exists())

    def test_archetype_token_differentiation(self):
        fin_tokens = self.engine.generate_design_system_tokens(DesignArchetype.FINANCIAL_DASHBOARD)
        dev_tokens = self.engine.generate_design_system_tokens(DesignArchetype.AI_DEVELOPER_TOOL)
        saas_tokens = self.engine.generate_design_system_tokens(DesignArchetype.SAAS_ADMIN_APP)

        # Tokens must genuinely differ across archetypes
        self.assertNotEqual(fin_tokens["color_palette"]["brand_accent"], dev_tokens["color_palette"]["brand_accent"])
        self.assertIn("Roboto Mono", fin_tokens["font_family"])
        self.assertIn("JetBrains Mono", dev_tokens["font_family"])
        self.assertEqual(fin_tokens["density"], "compact")

    def test_anti_slop_audit(self):
        slop_markup = """
        <div class="min-h-screen bg-slate-950">
          <div class="from-purple-600 to-indigo-600 blur-3xl"></div>
          <div class="grid grid-cols-4 total users">
            <div class="backdrop-blur bg-white/5">Card 1</div>
          </div>
        </div>
        """
        is_clean, violations = self.engine.audit_anti_slop(slop_markup, DesignArchetype.AI_DEVELOPER_TOOL)
        self.assertFalse(is_clean)
        self.assertGreaterEqual(len(violations), 2)

    def test_visual_qa_scorecard_evaluation(self):
        component_code = """
        import React from "react";
        export const Dashboard = () => (
          <div className="p-6 bg-[#0B0E14] text-white font-mono">
            <h1 className="text-xl font-bold">Ledger</h1>
            <table className="w-full tabular-nums">
              <tbody><tr><td>ETH</td><td>$3,400.00</td></tr></tbody>
            </table>
          </div>
        );
        """
        scorecard = self.engine.evaluate_visual_qa(component_code, DesignArchetype.FINANCIAL_DASHBOARD)
        self.assertIsInstance(scorecard, VisualQAScorecard)
        self.assertEqual(len(scorecard.dimensions), 10)
        self.assertGreaterEqual(scorecard.total_score, 70.0)


if __name__ == "__main__":
    unittest.main()
