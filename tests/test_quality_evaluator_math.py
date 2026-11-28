"""Unit tests for OpenClone Quality Evaluator exact mathematical formulas."""
import unittest

from src.openclone.quality.evaluator import QualityEvaluator


class TestQualityEvaluatorMath(unittest.TestCase):

    def setUp(self):
        self.evaluator = QualityEvaluator()

    def test_example_a_compliant_production_release(self):
        """Example A: 100% tests, 85% coverage, 4.2 complexity, clean security, clean architecture -> 99.0 PASS."""
        report = self.evaluator.evaluate_codebase(
            test_results={"total": 466, "passed": 466, "failed": 0},
            coverage_pct=85.0,
            avg_complexity=4.2,
            security_scan={"executed": True, "critical": 0, "high": 0, "medium": 0},
            architecture_metrics={"circular_deps": 0, "layer_violations": 0},
            doc_metrics={"public_symbols": 100, "documented_symbols": 90},
            dependency_metrics={"pinned": True, "cves": 0},
        )

        self.assertEqual(report.overall_score, 99.0)
        self.assertEqual(report.release_verdict, "PASS")
        self.assertEqual(len(report.blockers), 0)

    def test_example_b_missing_evidence_blocked(self):
        """Example B: Missing coverage, unexecuted security, unscanned dependencies -> 51.5 BLOCKED."""
        report = self.evaluator.evaluate_codebase(
            test_results={"total": 466, "passed": 466, "failed": 0},
            coverage_pct=None,  # Missing: 0.0 pts
            avg_complexity=6.0,  # 90.0 pts * 0.15 = 13.5
            security_scan=None,  # Missing: 0.0 pts
            architecture_metrics=None,  # Baseline: 50.0 pts * 0.10 = 5.0
            doc_metrics={"public_symbols": 100, "documented_symbols": 50},  # 50.0 * 0.10 = 5.0
            dependency_metrics=None,  # Missing: 0.0 pts
        )

        # 25.0 (tests) + 0.0 (cov) + 13.5 (comp) + 0.0 (sec) + 5.0 (arch) + 5.0 (doc) + 0.0 (dep) = 48.5
        self.assertLess(report.overall_score, 85.0)
        self.assertEqual(report.release_verdict, "BLOCKED")

    def test_example_c_critical_security_finding_overrides_score(self):
        """Example C: High score, but 1 critical finding triggers mandatory blocker -> BLOCKED."""
        report = self.evaluator.evaluate_codebase(
            test_results={"total": 466, "passed": 466, "failed": 0},
            coverage_pct=90.0,
            avg_complexity=3.5,
            security_scan={"executed": True, "critical": 1, "high": 0, "medium": 0},
            architecture_metrics={"circular_deps": 0, "layer_violations": 0},
            doc_metrics={"public_symbols": 100, "documented_symbols": 100},
            dependency_metrics={"pinned": True, "cves": 0},
        )

        self.assertEqual(report.release_verdict, "BLOCKED")
        self.assertTrue(any("Critical" in b for b in report.blockers))


if __name__ == "__main__":
    unittest.main()
