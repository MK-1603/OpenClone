"""Tests for OpenClone Autonomous Engineering Execution Engine."""
import tempfile
from pathlib import Path
import pytest

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import (
    EngineeringRequest,
    ExecutionMode,
    ExecutionPlan,
    LifecycleStage,
    RequestType,
    TaskNode,
)
from src.openclone.autonomous.policies import get_mode_policy


def test_execution_mode_policies():
    """Verify policies are configured for all 5 execution modes."""
    modes = [
        ExecutionMode.INSTANT,
        ExecutionMode.FAST,
        ExecutionMode.STANDARD,
        ExecutionMode.DEEP,
        ExecutionMode.AUTONOMOUS,
    ]
    for mode in modes:
        policy = get_mode_policy(mode)
        assert policy.mode == mode
        assert policy.max_tasks >= 1
        assert policy.time_budget_seconds > 0
        assert policy.max_retries >= 1
        assert len(policy.model_tier) > 0


def test_request_intent_classification():
    """Verify engine correctly classifies engineering intent."""
    engine = AutonomousExecutionEngine()

    assert engine._understand(EngineeringRequest(prompt="Run pytest test suite")) == RequestType.TESTING
    assert engine._understand(EngineeringRequest(prompt="Fix null pointer exception")) == RequestType.BUGFIX
    assert engine._understand(EngineeringRequest(prompt="Refactor database queries")) == RequestType.REFACTOR
    assert engine._understand(EngineeringRequest(prompt="Update API documentation in README")) == RequestType.DOCUMENTATION
    assert engine._understand(EngineeringRequest(prompt="Design microservices architecture")) == RequestType.ARCHITECTURE
    assert engine._understand(EngineeringRequest(prompt="Initialize new project workspace")) == RequestType.NEW_PROJECT
    assert engine._understand(EngineeringRequest(prompt="Add OAuth2 authentication provider")) == RequestType.FEATURE


def test_plan_generation_and_validation():
    """Verify plan decomposition, topological sorting, and digest computation."""
    engine = AutonomousExecutionEngine()
    req = EngineeringRequest(prompt="Implement authentication feature", mode=ExecutionMode.STANDARD)
    policy = get_mode_policy(req.mode)

    plan = engine._plan(req, RequestType.FEATURE, policy)
    assert len(plan.tasks) > 0
    assert plan.request_type == RequestType.FEATURE

    valid = engine._validate_plan(plan)
    assert valid is True
    assert plan.validated is True
    for task in plan.tasks:
        assert task.digest is not None
        assert len(task.digest) == 64


def test_model_intelligence_routing():
    """Verify task routing to appropriate AI model provider tier."""
    engine = AutonomousExecutionEngine()
    instant_policy = get_mode_policy(ExecutionMode.INSTANT)
    standard_policy = get_mode_policy(ExecutionMode.STANDARD)
    deep_policy = get_mode_policy(ExecutionMode.DEEP)

    task = TaskNode(task_id="t-1", title="Test task", worker_role="software-developer", action="code")

    fast_route = engine._route_model(task, instant_policy)
    assert fast_route["reasoning"] == "fast_local"

    std_route = engine._route_model(task, standard_policy)
    assert std_route["reasoning"] == "deep_reasoning"

    deep_route = engine._route_model(task, deep_policy)
    assert deep_route["reasoning"] == "frontier_autonomous"


def test_worker_contract_assignment():
    """Verify task assignment maps to existing 72 worker roles."""
    engine = AutonomousExecutionEngine()
    task = TaskNode(task_id="t-1", title="Write tests", worker_role="qa-engineer", action="test")
    assigned = engine._assign_agents(task)
    assert assigned in engine.registered_workers or assigned == "software-developer"


def test_end_to_end_autonomous_execution(tmp_path):
    """Verify complete execution lifecycle and delivery report generation."""
    engine = AutonomousExecutionEngine(workspace_root=tmp_path)
    report = engine.run("Fix error handling in authentication", mode=ExecutionMode.FAST)

    assert report.status == "COMPLETED"
    assert report.request_id.startswith("req-")
    assert report.plan_id.startswith("plan-")
    assert report.execution_duration_seconds > 0.0

    md = report.to_markdown()
    assert "OpenClone Engineering Delivery Report" in md
    assert "Summary of Changes" in md
    assert "Verification & Testing Evidence" in md
