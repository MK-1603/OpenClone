"""Tests for Phase 0 Boundary Policy and REST Gateway Security Enforcement."""
from __future__ import annotations

import pytest
from src.openclone.core.policy import (
    OperationClassification,
    Phase0BoundaryPolicy,
    Phase0BoundaryViolation,
)
from src.openclone.integrations.rest import OpenCloneRESTGateway


def test_phase0_boundary_policy_allows_planning_operations():
    allowed_ops = [
        OperationClassification.PLANNING_INSPECTION,
        OperationClassification.SOCRATIC_CLARIFICATION,
        OperationClassification.ARCHITECTURE_SYNTHESIS,
        OperationClassification.PLAN_GENERATION,
        OperationClassification.DEV_READINESS_EVALUATION,
        OperationClassification.INFRASTRUCTURE_RECOMMENDATION,
        OperationClassification.DEPLOYMENT_PLANNING,
    ]
    for op in allowed_ops:
        assert Phase0BoundaryPolicy.check_operation(op, actor="planner_test") is True


def test_phase0_boundary_policy_rejects_implementation_execution():
    restricted_ops = [
        OperationClassification.TARGET_CODE_MUTATION,
        OperationClassification.TARGET_TASK_EXECUTION,
        OperationClassification.TARGET_INFRASTRUCTURE_PROVISION,
        OperationClassification.TARGET_PRODUCTION_DEPLOYMENT,
    ]
    for op in restricted_ops:
        with pytest.raises(Phase0BoundaryViolation, match="Phase 0 Boundary Enforced"):
            Phase0BoundaryPolicy.check_operation(op, actor="malicious_agent")


def test_rest_gateway_execution_endpoint_fails_closed():
    gw = OpenCloneRESTGateway()

    # GET returns locked status
    get_res = gw.dispatch("GET", "/api/v1/execution")
    assert get_res["status"] == "PHASE_0_LOCKED"
    assert "disabled in Phase 0" in get_res["message"]

    # POST returns 403 boundary violation
    post_res = gw.dispatch("POST", "/api/v1/execution", {"prompt": "Implement user auth"})
    assert post_res["status_code"] == 403
    assert post_res["phase"] == "PHASE_0_PLANNING_LOCKED"
    assert post_res["executed"] is False
    assert "Phase 0 Boundary Enforced" in post_res["error"]


def test_rest_gateway_verification_reports_passing():
    gw = OpenCloneRESTGateway()
    verif = gw.dispatch("GET", "/api/v1/verification")
    assert verif["status"] == "PASS"
    assert verif["tests_passed"] >= 720
    assert verif["ledger_verified"] is True
