"""OpenClone Agency Agents Integration Test Suite.

Validates the full external specialist workforce integration:
- Division discovery across all 14 divisions from divisions.json
- Agent profile parsing and unshortened identity preservation
- Native OpenClone (72) vs. external Agency Agents distinction
- Multi-criteria search and filtering
- Multi-agent team assembly and topological dependency resolution
- UX Pro 5-stage team workflow
- Execution adapter, prompt formatting, and MIE model binding
- Least-privilege action permissions and security approval gates
- MCP server tools (status, discover, profile, assemble)
- Upstream catalog synchronization reporting
"""

import unittest
from pathlib import Path

from src.openclone.mcp.server import OpenCloneMCPServer
from src.openclone.mie.models import RoutingMode
from src.openclone.workforce.agency.adapter import AgencyExecutionAdapter
from src.openclone.workforce.agency.catalog import AgencyCatalog
from src.openclone.workforce.agency.models import AgentSource, ExecutionStatus
from src.openclone.workforce.agency.team_orchestrator import AgencyTeamOrchestrator
from runtime.openclone_runtime.workforce import load_workers


ROOT = Path(__file__).resolve().parents[1]


class AgencyAgentsIntegrationTests(unittest.TestCase):
    """Test suite for Agency Agents external specialist workforce integration."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = AgencyCatalog()
        cls.orchestrator = AgencyTeamOrchestrator(cls.catalog)
        cls.adapter = AgencyExecutionAdapter()
        cls.mcp_server = OpenCloneMCPServer(ROOT)

    # 1. Division Discovery
    def test_all_14_divisions_discovered(self):
        divisions = self.catalog.list_divisions()
        self.assertEqual(len(divisions), 14)
        div_ids = {d.id for d in divisions}
        expected = {
            "engineering",
            "design",
            "product",
            "project-management",
            "testing",
            "marketing",
            "sales",
            "paid-media",
            "support",
            "finance",
            "spatial-computing",
            "game-development",
            "academic",
            "specialized",
        }
        self.assertEqual(div_ids, expected)

        # Check metadata on a specific division
        design_div = self.catalog.get_division("design")
        self.assertIsNotNone(design_div)
        self.assertEqual(design_div.label, "Design")
        self.assertEqual(design_div.icon, "Palette")
        self.assertEqual(design_div.color, "#EC4899")
        self.assertGreaterEqual(design_div.agent_count, 5)

    # 2. Agent Profile Parsing & Identity Preservation
    def test_ui_designer_profile_preservation(self):
        agent = self.catalog.get_agent("ui-designer")
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "UI Designer")
        self.assertEqual(agent.division, "design")
        self.assertEqual(agent.source, AgentSource.EXTERNAL_AGENCY)
        self.assertEqual(agent.license, "MIT")
        self.assertIn("https://github.com/msitarzewski/agency-agents", agent.upstream_url)

        # Verify preserved unshortened sections
        self.assertTrue(len(agent.identity_memory) > 50)
        self.assertTrue(len(agent.mission) > 30)
        self.assertGreaterEqual(len(agent.critical_rules), 3)
        self.assertGreaterEqual(len(agent.workflow_steps), 3)
        self.assertGreaterEqual(len(agent.deliverables), 3)
        self.assertIn("design token", agent.raw_content.lower())

    # 3. Native vs External Workforce Separation
    def test_native_vs_external_workforce_isolation(self):
        # Native workers remain exactly 72 core engineering roles
        native_workers = load_workers()
        self.assertEqual(len(native_workers), 72)
        self.assertIn("frontend-engineer", native_workers)

        # External agency agents are distinct
        agency_agents = self.catalog.list_agents()
        self.assertGreaterEqual(len(agency_agents), 15)
        for a in agency_agents:
            self.assertEqual(a.source, AgentSource.EXTERNAL_AGENCY)
            # Ensure no collision with native worker ids
            self.assertNotIn(f"agency_{a.id}", native_workers)

    # 4. Search and Filtering
    def test_search_and_filtering(self):
        # Search by keyword
        architects = self.catalog.search("architect")
        self.assertTrue(any(a.id == "backend-architect" for a in architects))
        self.assertTrue(any(a.id == "ux-architect" for a in architects))

        # Filter by division
        design_agents = self.catalog.list_agents(division="design")
        self.assertGreaterEqual(len(design_agents), 7)
        for a in design_agents:
            self.assertEqual(a.division, "design")

        # Search by capability
        contrast_agents = self.catalog.search("", capability="accessibility")
        self.assertTrue(len(contrast_agents) >= 1)

    # 5. UX Pro 5-Stage Specialist Team Assembly
    def test_ux_pro_team_assembly_and_dependencies(self):
        team = self.orchestrator.assemble_ui_ux_team("OpenClone Dashboard")
        self.assertEqual(len(team.members), 5)
        self.assertEqual(len(team.execution_order), 5)

        # Verify the 5 exact roles
        member_ids = [m.agent_id for m in team.members]
        expected_ids = ["ux-researcher", "ux-architect", "ui-designer", "frontend-developer", "ui-finish-gate-reviewer"]
        self.assertEqual(member_ids, expected_ids)

        # Verify topological handoff ordering:
        # UX Researcher -> UX Architect -> UI Designer -> Frontend Developer -> UI Finish-Gate Reviewer
        order = team.execution_order
        self.assertLess(order.index("ux-researcher"), order.index("ux-architect"))
        self.assertLess(order.index("ux-architect"), order.index("ui-designer"))
        self.assertLess(order.index("ui-designer"), order.index("frontend-developer"))
        self.assertLess(order.index("frontend-developer"), order.index("ui-finish-gate-reviewer"))

    # 6. Website Development Team Assembly
    def test_website_team_assembly(self):
        team = self.orchestrator.assemble_website_development_team("SaaS Marketing Portal")
        self.assertEqual(len(team.members), 7)
        order = team.execution_order
        # Project shepherd leads coordination
        self.assertEqual(order[0], "project-shepherd")
        # Finish gate reviewer evaluates at the end
        self.assertEqual(order[-1], "ui-finish-gate-reviewer")

    # 7. Execution Adapter, Prompt Formatting & MIE Model Routing
    def test_execution_adapter_prompt_and_model_routing(self):
        agent = self.catalog.get_agent("backend-architect")
        self.assertIsNotNone(agent)

        contract = self.adapter.create_execution_contract(
            agent=agent,
            task_prompt="Design a high-throughput event streaming API with Kafka.",
            requested_actions=["observe", "plan"],
            routing_mode=RoutingMode.BEST_QUALITY,
        )

        self.assertEqual(contract.agent_id, "backend-architect")
        self.assertIn("observe", contract.allowed_actions)
        self.assertIn("plan", contract.allowed_actions)
        self.assertFalse(contract.requires_approval)

        formatted_prompt = self.adapter.format_agent_prompt(agent, contract, project_name="Analytics Engine")
        self.assertIn("SPECIALIST IDENTITY: BACKEND ARCHITECT", formatted_prompt)
        self.assertIn("OPENCLONE GOVERNANCE & PROJECT CONTEXT", formatted_prompt)
        self.assertIn("Zero secret leakage", formatted_prompt)
        self.assertIn("Zero AI Slop", formatted_prompt)

    # 8. Security Governance & Least-Privilege Action Boundaries
    def test_security_action_permissions_and_approval_gates(self):
        agent = self.catalog.get_agent("frontend-developer")
        self.assertIsNotNone(agent)

        # Request with sensitive write action
        contract = self.adapter.create_execution_contract(
            agent=agent,
            task_prompt="Implement navigation component.",
            requested_actions=["observe", "write"],
        )

        # Writing is sensitive, so approval is required
        self.assertTrue(contract.requires_approval)
        self.assertEqual(contract.status, ExecutionStatus.WAITING_APPROVAL)

        # Unapproved write should be rejected
        self.assertFalse(self.adapter.validate_action_permissions(contract, "write", is_human_approved=False))

        # Approved write is permitted
        self.assertTrue(self.adapter.validate_action_permissions(contract, "write", is_human_approved=True))

        # Denied actions (raw shell) are strictly rejected even if approved
        self.assertFalse(self.adapter.validate_action_permissions(contract, "raw_shell", is_human_approved=True))

    # 9. MCP Server Integration
    def test_mcp_server_workforce_tools(self):
        # 1. Workforce Status
        status = self.mcp_server.call_tool("openclone_workforce_status", {})
        self.assertEqual(status["native_workers"], 72)
        self.assertGreaterEqual(status["external_agency_agents"], 15)
        self.assertEqual(status["total_divisions"], 14)
        self.assertIn("design", status["divisions"])

        # 2. Discover Agents
        discover_res = self.mcp_server.call_tool("openclone_discover_agents", {"division": "design"})
        self.assertIn("agents", discover_res)
        self.assertGreaterEqual(len(discover_res["agents"]), 5)

        # 3. Get Agent Profile
        profile = self.mcp_server.call_tool("openclone_get_agent_profile", {"agent_id": "ui-designer"})
        self.assertEqual(profile["name"], "UI Designer")
        self.assertEqual(profile["division"], "design")

        # 4. Assemble Team
        team_res = self.mcp_server.call_tool("openclone_assemble_team", {"team_type": "ui_ux", "project_name": "Test App"})
        self.assertEqual(len(team_res["members"]), 5)
        self.assertEqual(team_res["name"], "Test App UX Pro Specialist Team")

    # 10. Upstream Synchronization
    def test_catalog_synchronization_reporting(self):
        report = self.catalog.synchronize()
        self.assertEqual(report.status, "IN_SYNC")
        self.assertGreaterEqual(report.total_scanned, 15)
        self.assertEqual(len(report.new_agents), 0)
        self.assertEqual(len(report.modified_agents), 0)
        self.assertEqual(len(report.removed_agents), 0)


if __name__ == "__main__":
    unittest.main()
