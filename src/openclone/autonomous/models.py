"""Data models and state definitions for Autonomous Engineering Execution Engine."""
from __future__ import annotations

import enum
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


class ExecutionMode(str, enum.Enum):
    """Execution modes for controlled autonomous execution."""
    INSTANT = "instant"
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"
    AUTONOMOUS = "autonomous"


class RequestType(str, enum.Enum):
    """Categorization of engineering requests."""
    NEW_PROJECT = "new_project"
    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    MAINTENANCE = "maintenance"
    INVESTIGATION = "investigation"


class LifecycleStage(str, enum.Enum):
    """12-Stage Controlled Execution Lifecycle."""
    REQUEST = "REQUEST"
    UNDERSTAND = "UNDERSTAND"
    INSPECT = "INSPECT"
    PLAN = "PLAN"
    VALIDATE_PLAN = "VALIDATE_PLAN"
    APPROVE = "APPROVE"
    ROUTE_MODEL = "ROUTE_MODEL"
    ASSIGN_AGENTS = "ASSIGN_AGENTS"
    EXECUTE = "EXECUTE"
    TEST = "TEST"
    VERIFY = "VERIFY"
    REPAIR = "REPAIR"
    DELIVER = "DELIVER"
    FAILED = "FAILED"


class FailureType(str, enum.Enum):
    """Failure classification for bounded repair."""
    SYNTAX_ERROR = "syntax_error"
    TEST_ASSERTION = "test_assertion"
    DEPENDENCY_MISSING = "dependency_missing"
    PERMISSION_DENIED = "permission_denied"
    TIMEOUT = "timeout"
    GATE_REJECTED = "gate_rejected"
    UNKNOWN = "unknown"


@dataclass
class EngineeringRequest:
    """Developer input request with contextual constraints."""
    prompt: str
    mode: ExecutionMode = ExecutionMode.STANDARD
    workspace_root: Path = field(default_factory=Path.cwd)
    allowed_files: Optional[List[str]] = None
    timeout_seconds: int = 600
    request_id: str = field(default_factory=lambda: f"req-{uuid.uuid4().hex[:8]}")
    created_at: float = field(default_factory=time.time)


@dataclass
class TaskNode:
    """Individual task node within a topological execution plan."""
    task_id: str
    title: str
    worker_role: str
    action: str
    command: Optional[str] = None
    target_path: Optional[str] = None
    file_content: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)
    verification_command: Optional[str] = None
    is_critical: bool = False
    digest: Optional[str] = None
    status: str = "DRAFT"  # DRAFT, PLANNED, APPROVED, READY, RUNNING, SUCCEEDED, FAILED


@dataclass
class ExecutionPlan:
    """Topological execution plan validated against governance schemas."""
    plan_id: str
    request_id: str
    request_type: RequestType
    tasks: List[TaskNode]
    critical_path: List[str] = field(default_factory=list)
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    requires_human_approval: bool = False
    created_at: float = field(default_factory=time.time)
    validated: bool = False
    approval_digest: Optional[str] = None


@dataclass
class ExecutionResult:
    """Outcome of a single task or lifecycle stage."""
    stage: LifecycleStage
    task_id: Optional[str]
    success: bool
    output: str
    error: Optional[str] = None
    exit_code: int = 0
    duration_seconds: float = 0.0
    evidence_digest: Optional[str] = None


@dataclass
class DeliveryReport:
    """Structured delivery report summarizing execution outcomes."""
    request_id: str
    plan_id: str
    mode: ExecutionMode
    status: str  # COMPLETED, PARTIALLY_COMPLETED, FAILED
    created_files: List[str] = field(default_factory=list)
    modified_files: List[str] = field(default_factory=list)
    tests_executed: int = 0
    tests_passed: int = 0
    security_checks_passed: bool = True
    audit_ledger_records: int = 0
    ledger_hash: Optional[str] = None
    known_limitations: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    execution_duration_seconds: float = 0.0

    def to_markdown(self) -> str:
        """Render delivery report as formatted markdown."""
        lines = [
            f"# OpenClone Engineering Delivery Report",
            f"**Request ID:** `{self.request_id}` | **Plan ID:** `{self.plan_id}` | **Mode:** `{self.mode.value}`",
            f"**Status:** `{self.status}` | **Execution Duration:** `{self.execution_duration_seconds:.2f}s`",
            "",
            "## 1. Summary of Changes",
            f"- **Files Created:** {len(self.created_files)}",
        ]
        for f in self.created_files:
            lines.append(f"  - `{f}`")
        lines.append(f"- **Files Modified:** {len(self.modified_files)}")
        for f in self.modified_files:
            lines.append(f"  - `{f}`")

        lines.extend([
            "",
            "## 2. Verification & Testing Evidence",
            f"- **Tests Executed:** {self.tests_executed}",
            f"- **Tests Passed:** {self.tests_passed} (Pass Rate: {100.0 * (self.tests_passed / max(1, self.tests_executed)):.1f}%)",
            f"- **Security Verification:** {'PASS' if self.security_checks_passed else 'FAIL'}",
            f"- **Audit Ledger Records:** {self.audit_ledger_records}",
        ])
        if self.ledger_hash:
            lines.append(f"- **Audit Ledger Head Hash:** `{self.ledger_hash}`")

        if self.known_limitations:
            lines.extend(["", "## 3. Disclosed Limitations"])
            for lim in self.known_limitations:
                lines.append(f"- {lim}")

        if self.next_actions:
            lines.extend(["", "## 4. Recommended Next Actions"])
            for act in self.next_actions:
                lines.append(f"- {act}")

        return "\n".join(lines)
