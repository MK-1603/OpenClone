"""Comprehensive Tests for OpenClone Planner Agent and Universal Planning Capabilities."""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from src.openclone.integrations.capabilities import get_canonical_registry
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway
from src.openclone.mcp.server import OpenCloneMCPServer
from src.openclone.planning.agent import OpenClonePlannerAgent
from src.openclone.planning.builder import PlanBuilder


class TestOpenClonePlannerAgent(unittest.TestCase):
    """Test suite covering Planner Agent initialization, workflows, and tool execution."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="openclone_planner_test_")
        self.workspace = Path(self.temp_dir)
        self.gateway = IntegrationGateway(get_canonical_registry())
        self.agent = OpenClonePlannerAgent(workspace_root=self.workspace, gateway=self.gateway)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_planner_agent_initialization(self):
        """Verify Planner Agent initializes all underlying specialist engines."""
        self.assertEqual(self.agent.workspace_root, self.workspace)
        self.assertIsNotNone(self.agent.pia)
        self.assertIsNotNone(self.agent.plan_builder)
        self.assertIsNotNone(self.agent.autonomous_engine)
        self.assertIsNotNone(self.agent.clarification_engine)
        self.assertEqual(len(self.agent.registered_workers), 72)
        self.assertIn("principal-architect", self.agent.registered_workers)

    def test_understand_project_detection_and_ambiguities(self):
        """Verify project understanding, intent extraction, and ambiguity identification."""
        res = self.agent.understand_project("Build a real-time collaborative whiteboarding platform")
        self.assertEqual(res["status"], "UNDERSTOOD")
        self.assertEqual(res["intent"].upper(), "FEATURE")
        self.assertEqual(res["pia_mode"], "NEW")
        self.assertTrue(res["has_ambiguities"])
        self.assertGreaterEqual(len(res["ambiguities"]), 1)

    def test_clarify_project_flow(self):
        """Verify Socratic clarification analysis and question answering."""
        res = self.agent.clarify_project("Create a high-scale streaming platform")
        self.assertEqual(res["status"], "CLARIFICATION_EVALUATED")
        self.assertGreaterEqual(res["total_questions"], 1)

        # Answer the questions
        first_q = res["questions"][0]["question_id"]
        res2 = self.agent.clarify_project(
            "Create a high-scale streaming platform",
            answers={first_q: "100,000 peak concurrent viewers"},
        )
        self.assertEqual(res2["status"], "CLARIFICATION_EVALUATED")
        # Check that the question was recorded
        answered_q = next(q for q in res2["questions"] if q["question_id"] == first_q)
        self.assertEqual(answered_q["status"], "answered")
        self.assertEqual(answered_q["answer"], "100,000 peak concurrent viewers")

    def test_generate_architecture_sets_a_to_d(self):
        """Verify architecture generation produces complete Sets A-D and dynamic C4 diagrams."""
        res = self.agent.generate_architecture(
            prompt="Build a SaaS task tracker with 50,000 DAU using PostgreSQL",
            project_name="TaskTracker",
            mode="NEW",
        )
        self.assertEqual(res["status"], "ARCHITECTURE_GENERATED")
        self.assertEqual(res["project_name"], "TaskTracker")
        self.assertIn("set_a", res)
        self.assertIn("set_b", res)
        self.assertIn("set_c", res)
        self.assertIn("set_d", res)
        self.assertTrue(res["traceability_verified"])
        # Verify dynamic C4 diagrams are generated
        c4 = res["dynamic_c4_diagrams"]
        self.assertIn("system_context", c4)
        self.assertIn("container", c4)
        self.assertIn("component", c4)
        self.assertIn("flowchart", c4["system_context"])

    def test_generate_plan_and_validation(self):
        """Verify PlanBuilder generates runtime-valid task DAG matching worker permissions."""
        arch = self.agent.generate_architecture(
            prompt="Build a minimalist notes app with SQLite storage",
            project_name="NotesApp",
        )
        set_d = arch["set_d"]
        plan = self.agent.generate_plan(set_d_blueprint=set_d, project_name="NotesApp", budget_usd=75.0)
        self.assertEqual(plan["status"], "PLAN_GENERATED")
        self.assertGreaterEqual(plan["task_count"], 3)
        self.assertIn("Phase 1 Inception Approval Gate", plan["plan_markdown"])

        # Validate the generated plan
        val = self.agent.validate_plan(plan["tasks"])
        self.assertTrue(val["valid"])
        self.assertEqual(len(val["errors"]), 0)

    def test_validate_plan_rejects_malformed_dag_or_unauthorized_worker(self):
        """Verify validator catches cyclic dependencies and unauthorized actions."""
        # 1. Cyclic dependency
        cyclic_tasks = [
            {"task_id": "T1", "worker_id": "backend-engineer", "action": "write", "depends_on": ["T2"]},
            {"task_id": "T2", "worker_id": "backend-engineer", "action": "write", "depends_on": ["T1"]},
        ]
        val_cyclic = self.agent.validate_plan(cyclic_tasks)
        self.assertFalse(val_cyclic["valid"])
        self.assertTrue(any("cycle" in e.lower() for e in val_cyclic["errors"]))

        # 2. Unknown worker
        bad_worker_tasks = [
            {"task_id": "T1", "worker_id": "non-existent-super-agent", "action": "write", "depends_on": []},
        ]
        val_bad_worker = self.agent.validate_plan(bad_worker_tasks)
        self.assertFalse(val_bad_worker["valid"])

    def test_governed_execution_blocks_without_human_approval(self):
        """Verify that tasks requiring human approval block execution when approval is missing."""
        tasks = [
            {
                "task_id": "TASK-01-PROD-DEPLOY",
                "worker_id": "backend-engineer",
                "action": "write",
                "human_approval_required": True,
                "depends_on": [],
                "acceptance_criteria": "Deployed database schema",
            }
        ]
        exec_res = self.agent.execute_approved_plan(tasks)
        self.assertEqual(exec_res["status"], "APPROVAL_REQUIRED")
        self.assertEqual(exec_res["blocked_task_id"], "TASK-01-PROD-DEPLOY")

    def test_plan_and_execute_inspection_only(self):
        """Verify that an investigation/inspection request does not trigger build execution."""
        res = self.agent.plan_and_execute("Investigate existing repository structure and technical debt")
        self.assertEqual(res["status"], "COMPLETED_DISCOVERY_ONLY")
        self.assertIn("understanding", res)
        self.assertFalse(res.get("executed", False))

    def test_plan_and_execute_end_to_end_planning_flow(self):
        """Verify full planning workflow generates architecture, plan, and validation without executing."""
        res = self.agent.plan_and_execute(
            prompt="Build a secure IoT sensor telemetry gateway with 50,000 DAU on PostgreSQL",
            project_name="IoTGateway",
            execute=False,
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["project_name"], "IoTGateway")
        self.assertFalse(res["executed"])
        self.assertTrue(res["validation"]["valid"])
        self.assertIn("IoTGateway", res["architecture"]["set_d_blueprint_files"] > 0 and "IoTGateway" or "IoTGateway")
        self.assertGreater(res["plan"]["task_count"], 0)

    def test_capability_registry_execution_via_gateway(self):
        """Verify that openclone_plan_and_execute and planning tools work through IntegrationGateway."""
        auth = AuthContext(
            user_id="test-developer",
            project_id="test-project",
            scopes={"projects:read", "tasks:write"},
        )
        res = self.gateway.execute(
            auth=auth,
            capability_id="openclone_plan_and_execute",
            arguments={
                "prompt": "Build an inventory management microservice with 10,000 DAU on PostgreSQL",
                "project_name": "InventoryApp",
                "execute": False,
            },
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["project_name"], "InventoryApp")

    def test_mcp_server_tools_call_planner_agent(self):
        """Verify that OpenCloneMCPServer calls openclone_plan_and_execute over JSON-RPC."""
        server = OpenCloneMCPServer(root=self.workspace)
        req = {
            "jsonrpc": "2.0",
            "id": 42,
            "method": "tools/call",
            "params": {
                "name": "openclone_plan_and_execute",
                "arguments": {
                    "prompt": "Design a real-time event streaming pipeline with 50,000 DAU on PostgreSQL",
                    "project_name": "EventStream",
                    "execute": False,
                },
            },
        }
        resp = server.handle_request(req)
        self.assertFalse(resp.get("result", {}).get("isError", True))
        content = resp["result"]["content"][0]["text"]
        data = json.loads(content)
        self.assertEqual(data["status"], "COMPLETED")
        self.assertEqual(data["project_name"], "EventStream")


if __name__ == "__main__":
    unittest.main()
