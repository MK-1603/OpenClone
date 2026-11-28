"""Unit tests verifying Autonomous Execution Engine grounds strictly in the 72-worker registry."""
import unittest
from pathlib import Path

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import EngineeringRequest, ExecutionMode
from src.openclone.autonomous.policies import get_mode_policy
from src.openclone.runtime.workforce import load_workers


class TestAutonomousEngineRegistry(unittest.TestCase):

    def setUp(self):
        self.engine = AutonomousExecutionEngine()
        self.registered_workers = load_workers()

    def test_registry_contains_72_workers(self):
        """Verify the immutable registry has exactly 72 workers."""
        self.assertEqual(len(self.registered_workers), 72)

    def test_planned_tasks_use_registered_workers_only(self):
        """Verify _plan() never assigns unregistered software-developer or qa-engineer."""
        req = EngineeringRequest(prompt="Implement database migration", mode=ExecutionMode.STANDARD)
        policy = get_mode_policy(req.mode)
        req_type = self.engine._understand(req)
        plan = self.engine._plan(req, req_type, policy)

        for task in plan.tasks:
            self.assertIn(
                task.worker_role,
                self.registered_workers,
                f"Task {task.task_id} assigned unregistered worker '{task.worker_role}'",
            )
            self.assertNotEqual(task.worker_role, "software-developer")
            self.assertNotEqual(task.worker_role, "qa-engineer")

    def test_fallback_worker_assignment_uses_registered_workers(self):
        """Verify _assign_agents() fallback maps strictly to registered workers."""
        class MockTask:
            worker_role = "unregistered-fictional-agent"
            action = "code"

        assigned = self.engine._assign_agents(MockTask())
        self.assertIn(assigned, self.registered_workers)
        self.assertEqual(assigned, "backend-engineer")


if __name__ == "__main__":
    unittest.main()
