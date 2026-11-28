"""Test Suite for OpenClone Universal Master Engineering Orchestrator.

Validates Directive OC-UMEO-007:
- UMEO-001 through UMEO-025 acceptance criteria
- Scenarios A through G
- 3-level agent hierarchy (Master, 21 Domain Leads, Specialists)
- 11 lifecycle operating modes
- Global Capability Map
- Cross-agent verification and bounded delegation
"""
import pytest
from pathlib import Path

from src.openclone.orchestration.capability_map import GlobalCapabilityMap
from src.openclone.orchestration.hierarchy import AgentHierarchyManager
from src.openclone.orchestration.lifecycle import MasterEngineeringLifecycle
from src.openclone.orchestration.master import UniversalMasterOrchestrator
from src.openclone.orchestration.models import (
    AgentTier,
    ComponentMaturity,
    DelegatedTask,
    OrchestrationMode,
)
from src.openclone.planning.agent import OpenClonePlannerAgent


@pytest.fixture
def master_orchestrator(tmp_path):
    return UniversalMasterOrchestrator(workspace_root=tmp_path)


@pytest.fixture
def planner_agent(tmp_path):
    return OpenClonePlannerAgent(workspace_root=tmp_path)


# -----------------------------------------------------------------------------
# 1. Master Agent & Hierarchy Tests (UMEO-001 - UMEO-008, Scenario B)
# -----------------------------------------------------------------------------

def test_master_agent_reuse_and_central_authority(planner_agent):
    """UMEO-001, UMEO-002: OpenClonePlannerAgent remains single central Master authority."""
    assert hasattr(planner_agent, "master_orchestrator")
    assert isinstance(planner_agent.master_orchestrator, UniversalMasterOrchestrator)
    inventory = planner_agent.discover_ecosystem()
    assert inventory["total_agents"] > 20
    assert len(inventory["master_agents"]) == 1
    assert inventory["master_agents"][0]["agent_id"] == "master-orchestrator"


def test_21_canonical_domain_leads(master_orchestrator):
    """UMEO-004: All 21 Level 1 Domain Lead Agents are registered and discoverable."""
    domain_leads = master_orchestrator.hierarchy.list_agents(tier=AgentTier.DOMAIN_LEAD)
    assert len(domain_leads) == 21
    
    expected_lead_ids = {
        "lead-repository", "lead-architecture", "lead-engineering", "lead-knowledge",
        "lead-project", "lead-system-design", "lead-security", "lead-workforce",
        "lead-dev-env", "lead-model", "lead-frontend", "lead-backend",
        "lead-database", "lead-infrastructure", "lead-connected-accounts",
        "lead-deployment", "lead-testing-quality", "lead-debugging",
        "lead-performance", "lead-documentation", "lead-upgrade",
    }
    registered_ids = {a.agent_id for a in domain_leads}
    assert expected_lead_ids.issubset(registered_ids)


def test_dynamic_specialist_activation_and_bounds(master_orchestrator):
    """UMEO-005, UMEO-006: Dynamic specialist activation with recursion depth enforcement."""
    specialists = master_orchestrator.hierarchy.list_agents(tier=AgentTier.SPECIALIST)
    assert len(specialists) >= 16

    # Verify normal delegation
    task = DelegatedTask(
        assigned_agent="lead-security",
        scope="framework",
        inputs={"target": "api-gateway"},
    )
    res = master_orchestrator.hierarchy.delegate_task(task, depth=1)
    assert res.status == "SUCCEEDED"
    assert res.confidence > 0.9

    # Verify recursion depth barrier
    blocked = master_orchestrator.hierarchy.delegate_task(task, depth=4)
    assert blocked.status == "BLOCKED"
    assert "depth limit exceeded" in blocked.errors[0]


def test_cross_agent_verification(master_orchestrator):
    """UMEO-008, Scenario B: Independent peer verification between peer agents."""
    task = DelegatedTask(assigned_agent="lead-backend", scope="api-construction")
    res = master_orchestrator.delegate_task(task, verifier_agent_id="lead-testing-quality")
    assert res["status"] == "COMPLETED"
    assert res["cross_verification"] is not None
    assert res["cross_verification"]["verified"] is True
    assert res["cross_verification"]["verifier_agent_id"] == "lead-testing-quality"


# -----------------------------------------------------------------------------
# 2. Global Capability Map & Repository Audit (UMEO-021, Scenario A)
# -----------------------------------------------------------------------------

def test_global_capability_map_integrity(planner_agent):
    """UMEO-021, Scenario A: Global Capability Map tracks ownership, maturity, and tests."""
    audit = planner_agent.get_capability_map()
    assert audit["total_capabilities"] >= 14
    assert audit["verified_capabilities"] >= 14
    assert audit["verification_rate"] == 100.0

    # Ensure major capabilities are tracked
    cap_ids = {c["capability_id"] for c in audit["capabilities"]}
    assert "CAP-PIA-001" in cap_ids
    assert "CAP-PLAN-001" in cap_ids
    assert "CAP-SEC-001" in cap_ids
    assert "CAP-DEVOPS-001" in cap_ids
    assert "CAP-BRANDING-001" in cap_ids


# -----------------------------------------------------------------------------
# 3. 11 Lifecycle Operating Modes (UMEO-009 - UMEO-015, Scenario C, D, E, F)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("mode", [
    OrchestrationMode.DISCOVERY,
    OrchestrationMode.AUDIT,
    OrchestrationMode.VERIFICATION,
    OrchestrationMode.PLANNING,
    OrchestrationMode.BUILD,
    OrchestrationMode.TEST,
    OrchestrationMode.DEBUG,
    OrchestrationMode.UPGRADE,
    OrchestrationMode.OPTIMIZATION,
    OrchestrationMode.DEPLOYMENT,
    OrchestrationMode.FULL_LIFECYCLE,
])
def test_all_11_operating_modes_execution(planner_agent, mode):
    """Validates that all 11 operating modes execute with structured delivery outputs."""
    res = planner_agent.execute_lifecycle_mode(
        mode=mode.value,
        prompt="Verify and orchestrate OpenClone framework components",
        parameters={"scope": "framework", "test_target": "tests/test_mcp_server.py"},
    )
    assert "status" in res
    assert res["mode"] == mode.value
    assert res["execution_duration_sec"] >= 0.0


def test_scenario_e_debugging_orchestration(planner_agent):
    """Scenario E: Debugging agent captures error traces and verifies root-cause diagnosis."""
    res = planner_agent.execute_lifecycle_mode(
        mode=OrchestrationMode.DEBUG.value,
        prompt="Investigate token expiration error",
        parameters={"error_trace": "TokenExpiredError: Nonce 102 expired"},
    )
    assert res["status"] == "DEBUG_RESOLVED"
    assert "root_cause_analysis" in res
    assert res["regression_safety"] == "VERIFIED"


def test_scenario_g_security_and_approval_governance(planner_agent):
    """Scenario G, UMEO-016: Sensitive operations require explicit human approval."""
    res = planner_agent.execute_lifecycle_mode(
        mode=OrchestrationMode.DEPLOYMENT.value,
        prompt="Deploy target production infrastructure",
    )
    assert res["status"] == "DEPLOYMENT_READINESS_VERIFIED"
    assert res["approval_required"] is True
    assert "cryptographic human approval" in res["message"]


def test_end_to_end_full_lifecycle_orchestration(planner_agent):
    """UMEO-024, UMEO-025: End-to-end multi-agent engineering lifecycle run."""
    result = planner_agent.run_full_engineering_lifecycle(
        prompt="Synthesize and verify Universal Engineering Orchestrator",
        project_name="OrchestratorTest",
    )
    assert result["status"] == "FULL_LIFECYCLE_COMPLETED"
    assert "stages" in result
    assert result["stages"]["DISCOVER"] == "DISCOVERY_COMPLETED"
    assert result["stages"]["VERIFY"] in ("VERIFICATION_COMPLETED", "VERIFICATION_FAILED")
    assert result["stages"]["PLAN"] == "PLANNING_COORDINATED"
    assert result["stages"]["DELIVER"] == "READY"
