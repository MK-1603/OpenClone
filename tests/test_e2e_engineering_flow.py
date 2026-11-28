"""End-to-End Integration Tests for the Upgraded OpenClone Engineering Framework."""
import shutil
import tempfile
import unittest
from pathlib import Path

from src.openclone.intelligence.project_intelligence import ProjectIntelligenceArchitect
from src.openclone.intelligence.router import resolve_software_architect
from src.openclone.planning.builder import PlanBuilder
from src.openclone.quality.evaluator import QualityEvaluator
from src.openclone.reverse_engineering.engine import ReverseEngineeringEngine
from src.openclone.reverse_engineering.models import ExecutionLevel
from src.openclone.runtime.workforce import _validate_task, load_workers, topo
from src.openclone.system_design.capacity import CapacityEstimator


class TestEndToEndEngineeringFlow(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.workers = load_workers()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_complete_greenfield_flow(self):
        """Test full pipeline: PIA (Sets A-D) -> Software Architect -> System Design -> Plan Builder -> Quality Evaluator."""
        # 1. Project Intelligence Architect (PIA-NEW)
        pia = ProjectIntelligenceArchitect()
        prompt = "Build a real-time event analytics platform in Python FastAPI with PostgreSQL."
        pia_result = pia.execute_new(prompt, project_name="AnalyticsEventHub")

        self.assertIn("set_a_features", pia_result)
        self.assertIn("set_b_gaps_problems", pia_result)
        self.assertIn("set_c_solutions", pia_result)
        self.assertIn("set_d_final_blueprint", pia_result)

        set_d = pia_result["set_d_final_blueprint"]
        self.assertTrue(set_d["traceability_verified"])
        self.assertGreaterEqual(len(set_d["traceability_matrix"]), 1)

        # 2. Software Architect Resolution
        arch_worker = resolve_software_architect(scope="system", domain="backend")
        self.assertEqual(arch_worker, "backend-architect")
        self.assertIn(arch_worker, self.workers)

        # 3. System Design Zero-Invention Rule
        estimator = CapacityEstimator()
        # When workload is absent, returns NOT_ESTIMATED
        cap_report = estimator.estimate(profile=None)
        self.assertEqual(cap_report.status, "NOT_ESTIMATED")
        self.assertIn("daily_active_users", cap_report.missing_metrics)

        # 4. Plan Builder
        builder = PlanBuilder(self.workers)
        tasks, plan_md = builder.build_plan(set_d, project_name="AnalyticsEventHub")

        self.assertGreaterEqual(len(tasks), 4)
        for t in tasks:
            _validate_task(t, self.workers)
        order = topo(tasks)
        self.assertEqual(order[0], "PHASE-01-START")
        self.assertEqual(order[-1], "PHASE-01-COMPLETION")

        # 5. Quality Evaluation & Release Gate
        evaluator = QualityEvaluator()
        quality_report = evaluator.evaluate(
            set_d_blueprint=set_d,
            tasks=tasks,
            test_results={"total": 20, "passed": 20, "failed": 0},
            system_design_report={"status": "QUALITATIVE_STRUCTURAL_ONLY"},
            ledger_verified=True,
        )

        self.assertGreaterEqual(quality_report.overall_score, 80.0)
        self.assertEqual(quality_report.release_verdict, "PASS")
        self.assertEqual(len(quality_report.blockers), 0)

    def test_complete_brownfield_evolution_flow(self):
        """Test brownfield pipeline: Reverse Engineering -> PIA-EVOLUTION -> Plan Builder -> Quality Evaluator."""
        # 1. Setup sample legacy codebase
        code_file = self.workspace / "service.py"
        code_file.write_text(
            'from fastapi import FastAPI\n'
            'app = FastAPI()\n\n'
            '@app.get("/telemetry")\n'
            'def get_telemetry():\n'
            '    return {"status": "ok"}\n',
            encoding="utf-8",
        )
        schema_file = self.workspace / "schema.sql"
        schema_file.write_text(
            'CREATE TABLE telemetry_events (\n'
            '  id SERIAL PRIMARY KEY,\n'
            '  payload TEXT\n'
            ');\n',
            encoding="utf-8",
        )

        # 2. Reverse Engineering Intelligence
        re_engine = ReverseEngineeringEngine(self.workspace)
        as_is_report = re_engine.analyze(ExecutionLevel.LEVEL_1_STATIC)

        self.assertEqual(as_is_report.total_files, 2)
        self.assertEqual(len(as_is_report.endpoints), 1)
        self.assertEqual(len(as_is_report.entities), 1)

        # 3. PIA-EVOLUTION
        pia = ProjectIntelligenceArchitect()
        pia_result = pia.execute_evolution(self.workspace, project_name="LegacyTelemetry")

        self.assertEqual(pia_result["mode"], "PIA-EVOLUTION")
        self.assertIn("as_is_report", pia_result)
        self.assertIn("AS-IS-Architecture-Report.md", pia_result["artifacts"])

        # 4. Plan Builder for Modernization
        builder = PlanBuilder(self.workers)
        tasks, _ = builder.build_plan(pia_result["set_d_final_blueprint"], project_name="LegacyTelemetry")
        for t in tasks:
            _validate_task(t, self.workers)

        # 5. Quality Evaluator
        evaluator = QualityEvaluator()
        quality_report = evaluator.evaluate(
            set_d_blueprint=pia_result["set_d_final_blueprint"],
            tasks=tasks,
            test_results={"total": 10, "passed": 10, "failed": 0},
            ledger_verified=True,
        )
        self.assertGreaterEqual(quality_report.overall_score, 80.0)


if __name__ == "__main__":
    unittest.main()
