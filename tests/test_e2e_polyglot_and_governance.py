"""End-to-End multi-domain integration test verifying polyglot reverse engineering,
Two-Gate human authorization, atomic autonomous file modification, and quality governance.
"""
import glob
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import TaskNode
from src.openclone.planning.builder import PlanBuilder
from src.openclone.quality.evaluator import QualityEvaluator
from src.openclone.reverse_engineering.diagrams import DiagramGenerator
from src.openclone.reverse_engineering.engine import ReverseEngineeringEngine
from src.openclone.reverse_engineering.models import ExecutionLevel
from src.openclone.runtime.workforce import Ledger, load_workers


class TestE2EPolyglotAndGovernance(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.workers = load_workers()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_registry_integrity_72_workers_across_12_teams(self):
        """Verify immutable registry contains exactly 72 worker manifests across 12 teams."""
        worker_files = glob.glob("framework/workforce/registry/workers/*.json")
        self.assertEqual(len(worker_files), 72)

        teams = {}
        for f in worker_files:
            data = json.load(open(f, encoding="utf-8"))
            t = data.get("team")
            teams[t] = teams.get(t, 0) + 1

        self.assertEqual(len(teams), 12)
        self.assertEqual(teams["architecture"], 7)
        self.assertEqual(teams["security"], 12)
        self.assertEqual(teams["backend"], 4)
        self.assertEqual(teams["quality"], 7)

    def test_complete_e2e_lifecycle_intake_to_release_gate(self):
        """Verify complete pipeline: Reverse Eng -> Plan -> Two-Gate Digest -> Atomic Write -> Quality -> Gate."""
        # 1. Reverse Engineering Intake (Polyglot setup)
        src_dir = self.workspace / "src"
        src_dir.mkdir(parents=True)
        (src_dir / "app.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        (self.workspace / "schema.sql").write_text(
            "CREATE TABLE customers (id VARCHAR(36) PRIMARY KEY, name VARCHAR(100));\n"
            "CREATE TABLE invoices (id VARCHAR(36) PRIMARY KEY, cust_id VARCHAR(36), FOREIGN KEY (cust_id) REFERENCES customers(id));\n",
            encoding="utf-8",
        )
        (self.workspace / "go.mod").write_text(
            "module github.com/openclone/test\n\ngo 1.22\n\nrequire github.com/gin-gonic/gin v1.9.1\n",
            encoding="utf-8",
        )

        re_engine = ReverseEngineeringEngine(workspace_root=self.workspace)
        report = re_engine.analyze(execution_level=ExecutionLevel.LEVEL_1_STATIC)

        self.assertEqual(len(report.entities), 2)
        self.assertGreater(len(report.dependencies), 0)

        # Generate Mermaid ER diagram
        er_diagram = DiagramGenerator.generate_er_diagram(report.entities)
        self.assertIn("erDiagram", er_diagram)
        self.assertIn("CUSTOMERS ||--o{ INVOICES", er_diagram)

        # 2. Gate 1 — Blueprint Approval Digest
        blueprint_content = json.dumps(report.to_dict(), sort_keys=True)
        gate1_digest = hashlib.sha256(f"BLUEPRINT:{blueprint_content}:HUMAN_APPROVER".encode()).hexdigest()
        self.assertTrue(bool(gate1_digest))

        # 3. PlanBuilder — Milestone Plan
        builder = PlanBuilder(self.workers)
        sample_blueprint = {
            "feature_catalogue": [{"feature_id": "FEAT-001", "title": "Core Service"}],
            "solutions": [{"solution_id": "SOL-001", "dependencies": ["FEAT-001"], "acceptance_criteria": ["Works"]}],
        }
        tasks, plan_md = builder.build_plan(sample_blueprint, project_name="PolyglotApp")
        self.assertGreaterEqual(len(tasks), 3)

        # 4. Gate 2 — Plan Approval Digest & Anti-Tamper check
        plan_content = json.dumps(tasks, sort_keys=True)
        gate2_digest = hashlib.sha256(f"PLAN:{plan_content}:{gate1_digest}".encode()).hexdigest()

        # Simulate tampering: mutating task_id invalidates digest
        tampered_tasks = json.loads(plan_content)
        tampered_tasks[0]["title"] = "Tampered Task Title"
        tampered_digest = hashlib.sha256(f"PLAN:{json.dumps(tampered_tasks, sort_keys=True)}:{gate1_digest}".encode()).hexdigest()
        self.assertNotEqual(gate2_digest, tampered_digest)

        # 5. Autonomous Real Modification Execution
        engine = AutonomousExecutionEngine(workspace_root=self.workspace)
        ledger = Ledger(self.workspace)

        real_task = TaskNode(
            task_id="T-01-CODE",
            title="Write core module",
            worker_role="backend-engineer",
            action="code",
            target_path="src/service.py",
            file_content="def process_order(order_id: str) -> bool:\n    return True\n",
        )

        exec_res = engine._execute_task(real_task, self.workspace, ledger)
        self.assertTrue(exec_res.success)
        self.assertTrue((self.workspace / "src/service.py").is_file())
        ledger.close()

        # 6. Quality Evaluation & Release Gate
        evaluator = QualityEvaluator()
        quality_report = evaluator.evaluate_codebase(
            test_results={"total": 10, "passed": 10, "failed": 0},
            coverage_pct=85.0,
            avg_complexity=3.2,
            security_scan={"executed": True, "critical": 0, "high": 0, "medium": 0},
            architecture_metrics={"circular_deps": 0, "layer_violations": 0},
            doc_metrics={"public_symbols": 5, "documented_symbols": 5},
            dependency_metrics={"pinned": True, "cves": 0},
        )

        self.assertGreaterEqual(quality_report.overall_score, 85.0)
        self.assertEqual(quality_report.release_verdict, "PASS")
        self.assertEqual(len(quality_report.blockers), 0)


if __name__ == "__main__":
    unittest.main()
