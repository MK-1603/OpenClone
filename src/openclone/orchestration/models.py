"""OpenClone Universal Master Engineering Orchestrator — Data Models.

Defines agent tiers, lifecycle modes, capability contracts, delegation envelopes,
and cross-verification structures under Directive OC-UMEO-007.
"""
from __future__ import annotations

import enum
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set


class OrchestrationMode(str, enum.Enum):
    """11 Master Agent Operating Modes (OC-UMEO-007 Section 6)."""
    DISCOVERY = "DISCOVERY"
    AUDIT = "AUDIT"
    VERIFICATION = "VERIFICATION"
    PLANNING = "PLANNING"
    BUILD = "BUILD"
    TEST = "TEST"
    DEBUG = "DEBUG"
    UPGRADE = "UPGRADE"
    OPTIMIZATION = "OPTIMIZATION"
    DEPLOYMENT = "DEPLOYMENT"
    FULL_LIFECYCLE = "FULL_LIFECYCLE"


class AgentTier(str, enum.Enum):
    """Hierarchical Agent Tiers (OC-UMEO-007 Section 3)."""
    MASTER = "LEVEL_0_MASTER"
    DOMAIN_LEAD = "LEVEL_1_DOMAIN_LEAD"
    SPECIALIST = "LEVEL_2_SPECIALIST"
    SUB_SPECIALIST = "LEVEL_3_SUB_SPECIALIST"


class ComponentMaturity(str, enum.Enum):
    """Standardized Component Maturity Statuses (OC-UMEO-007 Section 7)."""
    PROPOSED = "PROPOSED"
    SPECIFIED = "SPECIFIED"
    IMPLEMENTED = "IMPLEMENTED"
    REGISTERED = "REGISTERED"
    INVOKABLE = "INVOKABLE"
    INTEGRATED = "INTEGRATED"
    TESTED = "TESTED"
    VERIFIED = "VERIFIED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    DEGRADED = "DEGRADED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


@dataclass
class AgentDescriptor:
    """Agent definition and contract within the hierarchy."""
    agent_id: str
    name: str
    tier: AgentTier
    domain: str
    specializations: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    supported_tasks: List[str] = field(default_factory=list)
    parent_agent: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    delegation_policy: str = "BOUNDED_HIERARCHICAL"
    verification_policy: str = "INDEPENDENT_PEER_REVIEW"
    dependencies: List[str] = field(default_factory=list)
    version: str = "2.0.0"
    runtime_status: str = "ACTIVE"

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["tier"] = self.tier.value
        return res


@dataclass
class DelegatedTask:
    """Task assigned down the agent hierarchy with strict boundaries."""
    task_id: str = field(default_factory=lambda: f"TASK-{uuid.uuid4().hex[:8]}")
    parent_task_id: Optional[str] = None
    assigned_agent: str = "principal-architect"
    scope: str = "framework"
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    risk_level: str = "LOW"
    requires_human_approval: bool = False
    verification_requirements: List[str] = field(default_factory=list)
    status: str = "PENDING"  # PENDING, IN_PROGRESS, SUCCEEDED, FAILED, BLOCKED
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DelegationResult:
    """Result returned by an executing specialist to its parent orchestrator."""
    task_id: str
    agent_id: str
    status: str  # SUCCEEDED, FAILED, BLOCKED
    findings: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    files_examined: List[str] = field(default_factory=list)
    components_examined: List[str] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    missing_functionality: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    confidence: float = 1.0  # 0.0 to 1.0
    remaining_work: List[str] = field(default_factory=list)
    execution_duration_sec: float = 0.0
    verified_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CrossVerificationResult:
    """Independent verification of one agent's output by a peer agent."""
    primary_agent_id: str
    verifier_agent_id: str
    subject_task_id: str
    verified: bool
    confidence: float
    discrepancies: List[str] = field(default_factory=list)
    resolution: str = "ALIGNED"  # ALIGNED, OVERRULED, ESCALATED_TO_MASTER

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GlobalCapability:
    """Comprehensive capability tracked in the Global Capability Map."""
    capability_id: str
    name: str
    owning_module: str
    owning_agent: str
    supporting_agents: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    related_schemas: List[str] = field(default_factory=list)
    runtime_interfaces: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    integration_status: str = "CONNECTED"  # CONNECTED, DISCONNECTED, DEPRECATED, BLOCKED
    maturity: ComponentMaturity = ComponentMaturity.VERIFIED
    known_issues: List[str] = field(default_factory=list)
    upgrade_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["maturity"] = self.maturity.value
        return res
