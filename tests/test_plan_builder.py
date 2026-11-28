"""Unit tests for OpenClone Implementation Plan Builder."""
import unittest

from src.openclone.planning.builder import PlanBuilder
from src.openclone.runtime.workforce import _validate_task, load_workers, topo


class TestPlanBuilder(unittest.TestCase):

    def setUp(self):
        self.workers = load_workers()
        self.builder = PlanBuilder(self.workers)
        self.sample_blueprint = {
            "feature_catalogue": [
                {
                    "feature_id": "FEAT-001",
                    "title": "User Authentication API",
                    "category": "essential",
                },
                {
                    "feature_id": "FEAT-002",
                    "title": "Interactive Dashboard UI",
                    "category": "essential",
                },
            ],
            "solutions": [
                {
                    "solution_id": "SOL-001",
                    "dependencies": ["FEAT-001"],
                    "acceptance_criteria": ["JWT token returned on valid credentials"],
                },
                {
                    "solution_id": "SOL-002",
                    "dependencies": ["FEAT-002"],
                    "acceptance_criteria": ["Responsive charts render within 200ms"],
                },
            ],
        }

    def test_plan_builder_generates_valid_tasks(self):
        tasks, plan_md = self.builder.build_plan(self.sample_blueprint, project_name="AnalyticsApp")

        self.assertGreaterEqual(len(tasks), 5)  # Start, Scaffold, 2 Features, Verification, Completion
        self.assertEqual(tasks[0]["task_id"], "PHASE-01-START")
        self.assertEqual(tasks[-1]["task_id"], "PHASE-01-COMPLETION")

        # Verify every task passes workforce runtime validation
        for t in tasks:
            _validate_task(t, self.workers)

        # Verify topological sort resolves without cycles
        order = topo(tasks)
        self.assertEqual(order[0], "PHASE-01-START")
        self.assertEqual(order[-1], "PHASE-01-COMPLETION")

        # Verify markdown output contains key sections
        self.assertIn("# ENGINEERING IMPLEMENTATION PLAN — AnalyticsApp", plan_md)
        self.assertIn("PHASE-01-START", plan_md)
        self.assertIn("TASK-01-SCAFFOLD", plan_md)
        self.assertIn("PHASE-01-COMPLETION", plan_md)

    def test_plan_builder_worker_assignments(self):
        tasks, _ = self.builder.build_plan(self.sample_blueprint)
        workers_used = {t["worker_id"] for t in tasks}

        self.assertIn("principal-architect", workers_used)
        self.assertIn("backend-engineer", workers_used)
        self.assertIn("frontend-engineer", workers_used)
        self.assertIn("automation-test-engineer", workers_used)

    def test_runtime_task_validation_rejects_unknown_worker(self):
        invalid_task = {
            "task_id": "TASK-TEST-UNKNOWN",
            "title": "Invalid Worker Task",
            "worker_id": "nonexistent-super-worker",
            "action": "write",
            "acceptance_criteria": "None",
        }
        with self.assertRaises(ValueError) as ctx:
            _validate_task(invalid_task, self.workers)
        self.assertIn("unknown worker", str(ctx.exception))

    def test_runtime_task_validation_rejects_unpermitted_action(self):
        # principal-architect is not allowed to execute shell commands directly
        invalid_task = {
            "task_id": "TASK-TEST-ACTION",
            "title": "Invalid Action Task",
            "worker_id": "principal-architect",
            "action": "execute",
            "command": ["pytest"],
            "acceptance_criteria": "None",
            "human_approval_required": True,
        }
        with self.assertRaises(PermissionError) as ctx:
            _validate_task(invalid_task, self.workers)
        self.assertIn("not permitted", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
