"""Tests for OpenClone Skill Discovery, Selection, and Reporting Engine."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.openclone.skills.engine import SkillRegistry, SkillSelector, SkillReportGenerator, Skill

class SkillsEngineTests(unittest.TestCase):
    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)
        self.selector = SkillSelector(registry=self.registry)

    def test_registry_contains_core_skills(self):
        skills = self.registry.list_all()
        self.assertGreaterEqual(len(skills), 7)
        skill_ids = [s.id for s in skills]
        self.assertIn("taste-skill", skill_ids)
        self.assertIn("saas-security-baseline", skill_ids)
        self.assertIn("motion-design", skill_ids)
        self.assertIn("typography-standards", skill_ids)
        self.assertIn("strix-pentest-adapter", skill_ids)
        self.assertIn("backend-architecture", skill_ids)
        self.assertIn("ai-context-engineering", skill_ids)

    def test_saas_dashboard_task_selection(self):
        task = "Build a responsive SaaS dashboard with Tailwind CSS and user profile settings"
        res = self.selector.select(task)
        selected_ids = [s.id for s in res["selected_skills"]]
        self.assertIn("taste-skill", selected_ids)
        self.assertIn("saas-security-baseline", selected_ids)
        # Precedence: saas-security-baseline (5) must appear before taste-skill (10)
        self.assertLess(selected_ids.index("saas-security-baseline"), selected_ids.index("taste-skill"))

    def test_negative_trigger_exclusion(self):
        task = "Create a database schema and backend API endpoints (backend-only, no-ui)"
        res = self.selector.select(task)
        selected_ids = [s.id for s in res["selected_skills"]]
        self.assertIn("backend-architecture", selected_ids)
        self.assertNotIn("taste-skill", selected_ids)  # Excluded by negative trigger 'backend-only'

    def test_motion_design_selection(self):
        task = "Implement smooth view transition animations and hover microinteractions"
        res = self.selector.select(task)
        selected_ids = [s.id for s in res["selected_skills"]]
        self.assertIn("motion-design", selected_ids)

    def test_pentest_selection(self):
        task = "Execute automated dynamic penetration test with strix against authorized staging target"
        res = self.selector.select(task)
        selected_ids = [s.id for s in res["selected_skills"]]
        self.assertIn("strix-pentest-adapter", selected_ids)

    def test_selection_report_generation(self):
        task = "Build accessible login UI form with auth validation"
        res = self.selector.select(task)
        report = SkillReportGenerator.generate_selection_report("TASK-AUTH-UI", res)
        self.assertIn("# SKILL_SELECTION_REPORT", report)
        self.assertIn("TASK-AUTH-UI", report)
        self.assertIn("Selected Skills", report)
        self.assertIn("Skipped Skills", report)

    def test_application_report_generation(self):
        records = [
            {
                "skill_id": "taste-skill",
                "reason": "UI form task",
                "source": "skills/taste-skill",
                "actions_completed": "plan-check.mjs passed",
                "evidence": "0 slop patterns detected",
                "status": "APPLIED",
            },
            {
                "skill_id": "saas-security-baseline",
                "reason": "Auth task",
                "source": "docs/security/saas-security-baseline.md",
                "actions_completed": "Password hash verified",
                "evidence": "Argon2id tests passed",
                "status": "APPLIED",
            }
        ]
        report = SkillReportGenerator.generate_application_report("TASK-AUTH-UI", records)
        self.assertIn("# SKILL_APPLICATION_REPORT", report)
        self.assertIn("TASK-AUTH-UI", report)
        self.assertIn("taste-skill", report)
        self.assertIn("saas-security-baseline", report)
        self.assertIn("`APPLIED`", report)

if __name__ == "__main__":
    unittest.main()
