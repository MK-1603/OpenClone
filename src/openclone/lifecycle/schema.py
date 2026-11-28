"""Data models and enums for the OpenClone Engineering Lifecycle & Verification System."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
import datetime
import hashlib
import json


class ItemType(str, Enum):
    PHASE = "PHASE"
    CATEGORY = "CATEGORY"
    TASK = "TASK"
    SUBTASK = "SUBTASK"
    VERIFICATION = "VERIFICATION"


class Applicability(str, Enum):
    REQUIRED = "REQUIRED"
    CONDITIONAL = "CONDITIONAL"
    OPTIONAL = "OPTIONAL"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ItemStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    IMPLEMENTED = "IMPLEMENTED"
    VERIFICATION_PENDING = "VERIFICATION_PENDING"
    FAILED = "FAILED"
    NEEDS_REWORK = "NEEDS_REWORK"
    BLOCKED = "BLOCKED"
    VERIFIED = "VERIFIED"
    WAIVED_WITH_APPROVAL = "WAIVED_WITH_APPROVAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Priority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class VerificationLevel(str, Enum):
    V0_UNVERIFIED = "V0_UNVERIFIED"
    V1_DECLARATION_ONLY = "V1_DECLARATION_ONLY"
    V2_ARTIFACT_PRESENT = "V2_ARTIFACT_PRESENT"
    V3_AUTOMATED_CHECK_PASSED = "V3_AUTOMATED_CHECK_PASSED"
    V4_BEHAVIOR_VERIFIED = "V4_BEHAVIOR_VERIFIED"
    V5_INDEPENDENTLY_REVIEWED = "V5_INDEPENDENTLY_REVIEWED"


class VerificationOutcome(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_RUN = "NOT_RUN"
    INCONCLUSIVE = "INCONCLUSIVE"
    WAIVED = "WAIVED"


class ProjectType(str, Enum):
    WEB_SAAS = "WEB_SAAS"
    STATIC_WEBSITE = "STATIC_WEBSITE"
    MOBILE_APP = "MOBILE_APP"
    API_PLATFORM = "API_PLATFORM"
    ECOMMERCE = "ECOMMERCE"
    AI_AGENT_PLATFORM = "AI_AGENT_PLATFORM"
    REALTIME_COLLABORATIVE = "REALTIME_COLLABORATIVE"
    DATA_ANALYTICS = "DATA_ANALYTICS"
    DESKTOP_APP = "DESKTOP_APP"
    LIBRARY_SDK = "LIBRARY_SDK"
    LINUX_DISTRIBUTION = "LINUX_DISTRIBUTION"
    KERNEL_DRIVER = "KERNEL_DRIVER"
    EMBEDDED_FIRMWARE = "EMBEDDED_FIRMWARE"
    ROBOTICS_PLATFORM = "ROBOTICS_PLATFORM"
    MACHINE_LEARNING = "MACHINE_LEARNING"
    DATA_SCIENCE = "DATA_SCIENCE"
    GAME_SIMULATION = "GAME_SIMULATION"
    DEVELOPER_TOOLS = "DEVELOPER_TOOLS"
    RESEARCH_COMPUTING = "RESEARCH_COMPUTING"


@dataclass
class EvidenceRecord:
    id: str
    item_id: str
    evidence_type: str  # code_diff, test_run, command_output, screenshot, audit_log
    ref: str            # file path, commit hash, test ID, screenshot path
    description: str
    produced_by: str    # human, ai_agent, tool_name
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    proves: str = ""
    limitations: str = ""
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            raw = f"{self.item_id}:{self.ref}:{self.description}:{self.timestamp}"
            self.checksum = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "evidence_type": self.evidence_type,
            "ref": self.ref,
            "description": self.description,
            "produced_by": self.produced_by,
            "timestamp": self.timestamp,
            "proves": self.proves,
            "limitations": self.limitations,
            "checksum": self.checksum,
        }


@dataclass
class VerificationCheck:
    id: str
    item_id: str
    title: str
    min_level: VerificationLevel = VerificationLevel.V3_AUTOMATED_CHECK_PASSED
    command: Optional[str] = None
    outcome: VerificationOutcome = VerificationOutcome.NOT_RUN
    evidence_id: Optional[str] = None
    verified_by: Optional[str] = None
    verified_at: Optional[str] = None
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "title": self.title,
            "min_level": self.min_level.value,
            "command": self.command,
            "outcome": self.outcome.value,
            "evidence_id": self.evidence_id,
            "verified_by": self.verified_by,
            "verified_at": self.verified_at,
            "details": self.details,
        }


@dataclass
class DefectRecord:
    id: str
    task_id: str
    title: str
    severity: Priority = Priority.HIGH
    expected: str = ""
    actual: str = ""
    steps: str = ""
    status: str = "OPEN"  # OPEN, TRIAGED, IN_PROGRESS, FIXED, RETEST_PENDING, VERIFIED_CLOSED
    fix_ref: Optional[str] = None
    retest_result: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "severity": self.severity.value,
            "expected": self.expected,
            "actual": self.actual,
            "steps": self.steps,
            "status": self.status,
            "fix_ref": self.fix_ref,
            "retest_result": self.retest_result,
            "created_at": self.created_at,
        }


@dataclass
class ChecklistItem:
    id: str
    project_id: str
    phase_id: str
    category: str
    title: str
    description: str
    why_it_matters: str
    type: ItemType = ItemType.TASK
    applicability: Applicability = Applicability.REQUIRED
    applicability_reason: str = "Standard lifecycle requirement"
    status: ItemStatus = ItemStatus.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    risk_level: RiskLevel = RiskLevel.MEDIUM
    parent_id: Optional[str] = None
    requirement_ids: List[str] = field(default_factory=list)
    dependency_ids: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    verification_method: str = "automated_test"  # automated_test, manual_review, visual_inspection, security_scan
    verification_command: Optional[str] = None
    evidence_refs: List[EvidenceRecord] = field(default_factory=list)
    checks: List[VerificationCheck] = field(default_factory=list)
    defects: List[DefectRecord] = field(default_factory=list)
    assignee_type: str = "unassigned"  # human, ai_agent, tool
    assignee_id: Optional[str] = None
    reviewer_id: Optional[str] = None
    waiver_reason: Optional[str] = None
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    completed_at: Optional[str] = None
    verified_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "phase_id": self.phase_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "why_it_matters": self.why_it_matters,
            "type": self.type.value,
            "applicability": self.applicability.value,
            "applicability_reason": self.applicability_reason,
            "status": self.status.value,
            "priority": self.priority.value,
            "risk_level": self.risk_level.value,
            "parent_id": self.parent_id,
            "requirement_ids": self.requirement_ids,
            "dependency_ids": self.dependency_ids,
            "acceptance_criteria": self.acceptance_criteria,
            "verification_method": self.verification_method,
            "verification_command": self.verification_command,
            "evidence_refs": [e.to_dict() for e in self.evidence_refs],
            "checks": [c.to_dict() for c in self.checks],
            "defects": [d.to_dict() for d in self.defects],
            "assignee_type": self.assignee_type,
            "assignee_id": self.assignee_id,
            "reviewer_id": self.reviewer_id,
            "waiver_reason": self.waiver_reason,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "verified_at": self.verified_at,
        }


@dataclass
class QualityGate:
    phase_id: str
    phase_name: str
    mandatory_item_ids: List[str] = field(default_factory=list)
    required_level: VerificationLevel = VerificationLevel.V3_AUTOMATED_CHECK_PASSED
    allow_unresolved_high_defects: bool = False
    waiver_policy: str = "explicit_owner_approval"
    status: str = "OPEN"  # OPEN, BLOCKED, PASSED, WAIVED
    blockers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "phase_name": self.phase_name,
            "mandatory_item_ids": self.mandatory_item_ids,
            "required_level": self.required_level.value,
            "allow_unresolved_high_defects": self.allow_unresolved_high_defects,
            "waiver_policy": self.waiver_policy,
            "status": self.status,
            "blockers": self.blockers,
        }
