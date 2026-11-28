"""Unit tests for OpenClone 7-Dimensional Quality Evaluator."""
import unittest

from src.openclone.quality.evaluator import QualityEvaluator


class TestQualityEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = QualityEvaluator()
        self.sample_blueprint = {
            "feature_catalogue": [{"feature_id": "FEAT-001", "title": "Core Engine"}],
            "solutions": [{"solution_id": "SOL-001", "dependencies": ["FEAT-001"]}],
            "traceability_matrix": [
                {
                    "feature_id": "FEAT-001",
                    "solution_id": "SOL-001",
                    "acceptance_criteria": ["All tests pass"],
                }
            ],
        }
        self.sample_tasks = [
            {"task_id": "PHASE-01-START", "worker_id": "principal-architect"},
            {"task_id": "TASK-01-BUILD", "worker_id": "backend-engineer"},
            {"task_id": "PHASE-01-COMPLETION", "worker_id": "principal-architect"},
        ]

    def test_quality_evaluator_all_pass(self):
        report = self.evaluator.evaluate(
            set_d_blueprint=self.sample_blueprint,
            tasks=self.sample_tasks,
            test_results={"total": 25, "passed": 25, "failed": 0},
            ledger_verified=True,
        )

        self.assertGreaterEqual(report.overall_score, 85.0)
        self.assertEqual(report.release_verdict, "PASS")
        self.assertEqual(len(report.blockers), 0)
        self.assertEqual(len(report.dimensions), 7)

        # Markdown render test
        md = report.to_markdown()
        self.assertIn("# QUALITY EVALUATION REPORT", md)
        self.assertIn("Project Definition", md)
        self.assertIn("Verification & Testing", md)
        self.assertIn("PASS", md)

    def test_quality_evaluator_test_failure_triggers_blocker(self):
        report = self.evaluator.evaluate(
            set_d_blueprint=self.sample_blueprint,
            tasks=self.sample_tasks,
            test_results={"total": 25, "passed": 22, "failed": 3},
            ledger_verified=True,
        )

        self.assertEqual(report.release_verdict, "BLOCKED")
        self.assertTrue(any("failed" in b.lower() for b in report.blockers))

    def test_open_critical_finding_overrides_high_numerical_score(self):
        report = self.evaluator.evaluate(
            set_d_blueprint=self.sample_blueprint,
            tasks=self.sample_tasks,
            test_results={"total": 50, "passed": 50, "failed": 0},
            ledger_verified=True,
            open_findings=[
                {
                    "finding_id": "SEC-001",
                    "severity": "CRITICAL",
                    "status": "OPEN",
                    "description": "Exposed credential in repo",
                }
            ],
        )

        # Score remains high quantitatively, but release verdict is BLOCKED
        self.assertGreaterEqual(report.overall_score, 80.0)
        self.assertEqual(report.release_verdict, "BLOCKED")
        self.assertTrue(any("SEC-001" in b for b in report.blockers))


if __name__ == "__main__":
    unittest.main()
