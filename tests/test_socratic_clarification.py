"""Unit and integration tests for Socratic Clarification Engine (Stage 3)."""

from __future__ import annotations

import pytest

from src.openclone.intelligence.clarification import (
    ClarificationCategory,
    ClarificationOption,
    ClarificationQuestion,
    QuestionPriority,
    QuestionStatus,
    SocraticClarificationEngine,
)
from src.openclone.intelligence.project_intelligence import ProjectIntelligenceArchitect


def test_clarification_detects_missing_workload_and_persistence():
    engine = SocraticClarificationEngine()
    questions = engine.analyze_requirements("Build a basic task manager where users can create items.")
    assert len(questions) >= 2

    # Check for workload question
    workload_q = next((q for q in questions if q.category == ClarificationCategory.WORKLOAD_SCALE), None)
    assert workload_q is not None
    assert workload_q.priority == QuestionPriority.BLOCKER
    assert len(workload_q.options) >= 2

    # Check for persistence question
    persist_q = next((q for q in questions if q.category == ClarificationCategory.DATA_PERSISTENCE), None)
    assert persist_q is not None
    assert persist_q.priority in (QuestionPriority.HIGH, QuestionPriority.MEDIUM)


def test_clarification_no_missing_workload_when_dau_specified():
    engine = SocraticClarificationEngine()
    questions = engine.analyze_requirements("High scale messaging app targeting 500,000 DAU with PostgreSQL.")
    
    # Should not raise missing workload question
    workload_q = next((q for q in questions if q.category == ClarificationCategory.WORKLOAD_SCALE), None)
    assert workload_q is None

    # Should not raise missing DB question
    persist_q = next((q for q in questions if q.category == ClarificationCategory.DATA_PERSISTENCE), None)
    assert persist_q is None


def test_clarification_detects_ambiguity_and_contradictions():
    engine = SocraticClarificationEngine()
    questions = engine.analyze_requirements(
        requirements_text="Must be super fast and highly scalable real-time feed.",
        existing_gaps=[{"title": "Contradiction in storage retention limits vs zero-deletion clause"}],
    )

    categories = [q.category for q in questions]
    assert ClarificationCategory.AMBIGUITY_RESOLVE in categories
    assert ClarificationCategory.CONTRADICTION_RESOLVE in categories


def test_answer_recording_and_context_synthesis():
    engine = SocraticClarificationEngine()
    questions = engine.analyze_requirements("Design a financial ledger.")
    workload_q = next(q for q in questions if q.category == ClarificationCategory.WORKLOAD_SCALE)

    # Record answer
    answered = engine.record_answer(workload_q.question_id, "We expect 50,000 daily active users at peak.", answered_by="lead_architect")
    assert answered is not None
    assert answered.status == QuestionStatus.ANSWERED
    assert answered.answered_by == "lead_architect"

    # Context synthesis
    context = engine.synthesize_context_update()
    assert context["explicit_workload"].get("daily_active_users") == 50000

    # Summary
    summary = engine.get_clarification_summary()
    assert summary["answered_questions"] == 1
    assert summary["pending_questions"] == len(questions) - 1


def test_pia_integration_with_socratic_clarifications():
    pia = ProjectIntelligenceArchitect()
    res = pia.execute_new(
        prompt="Build a video streaming platform.",
        project_name="StreamCo",
    )

    assert "clarification_questions" in res
    assert len(res["clarification_questions"]) > 0
    categories = [q["category"] for q in res["clarification_questions"]]
    assert ClarificationCategory.WORKLOAD_SCALE.value in categories
