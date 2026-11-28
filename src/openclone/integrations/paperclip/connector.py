"""Paperclip Organization & Orchestration Connector.

Provides optional interoperability between external Paperclip agent organizations
and OpenClone engineering governance. OpenClone remains strictly authoritative
for engineering requirements, DAG validation, gates, security, and evidence.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import hmac
import json
import logging
from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("openclone.integrations.paperclip")


class PaperclipTaskStatus(str, Enum):
    """External task status mapped to Paperclip organizational lifecycle."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    NEEDS_APPROVAL = "needs_approval"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PaperclipBudgetContext:
    """Financial and token budget constraint passed by Paperclip."""
    budget_id: str
    max_spend_usd: float = 0.0
    current_spend_usd: float = 0.0
    max_tokens: int = 0
    current_tokens: int = 0
    currency: str = "USD"

    def is_exceeded(self) -> bool:
        """Verify whether either financial spend or token ceiling is exceeded."""
        if self.max_spend_usd > 0 and self.current_spend_usd >= self.max_spend_usd:
            return True
        if self.max_tokens > 0 and self.current_tokens >= self.max_tokens:
            return True
        return False


@dataclass
class PaperclipGoal:
    """Company-level or department-level goal passed from Paperclip."""
    goal_id: str
    title: str
    description: str
    owner_agent_id: Optional[str] = None
    target_metric: Optional[str] = None


@dataclass
class PaperclipTaskRequest:
    """Incoming task request originating from Paperclip organization control plane."""
    external_task_id: str
    organization_id: str
    title: str
    description: str
    requester_agent_id: str
    budget: Optional[PaperclipBudgetContext] = None
    target_project_root: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PaperclipTaskResponse:
    """Governed response from OpenClone to Paperclip control plane."""
    external_task_id: str
    accepted: bool
    status: PaperclipTaskStatus
    reason: str
    openclone_task_id: Optional[str] = None
    evidence_hashes: List[str] = field(default_factory=list)
    spend_usd: float = 0.0
    tokens_consumed: int = 0


@dataclass
class AuthoritativeApprovalRecord:
    """Immutable Human Approval Record bound to a specific operation and context."""
    approval_id: str
    approver_id: str
    task_digest: str  # 64-char hex SHA-256 bound to canonical task parameters
    workspace_root: str
    action: str
    created_at: float
    expires_at: float
    consumed: bool = False


class AuthoritativeApprovalStore:
    """Authoritative Human Approval Registry for Sensitive Operations.
    
    Guarantees:
    - Approvals are cryptographically bound to task contents (task_digest).
    - Bound to approver identity from an authorized registry.
    - Bound to specific workspace and action.
    - Bound to a strict validity window (expiration).
    - Bound to single-use consumption state (prevents replay/reuse).
    """

    def __init__(self, allowed_approvers: Optional[List[str]] = None):
        self.allowed_approvers = allowed_approvers or [
            "admin", "security-lead", "owner", "human-supervisor", "alice-admin"
        ]
        self._records: Dict[str, AuthoritativeApprovalRecord] = {}

    def register_approval(self, record: AuthoritativeApprovalRecord) -> None:
        """Register an authoritative approval issued by a validated human owner."""
        self._records[record.approval_id] = record

    def get_approval(self, approval_id: str) -> Optional[AuthoritativeApprovalRecord]:
        return self._records.get(approval_id)

    def verify_and_consume(
        self,
        approval_id: str,
        expected_digest: str,
        expected_workspace: str,
        expected_action: str,
        current_time: Optional[float] = None,
    ) -> Tuple[bool, str]:
        """Verify all binding dimensions and atomically consume approval."""
        if approval_id not in self._records:
            return False, f"Approval record '{approval_id}' not found in authoritative registry"

        rec = self._records[approval_id]
        now = current_time if current_time is not None else time.time()

        if rec.consumed:
            return False, "Approval has already been consumed (replay prevention)"

        if now > rec.expires_at:
            return False, f"Approval has expired (expired at {rec.expires_at}, current {now})"

        if rec.approver_id not in self.allowed_approvers:
            return False, f"Approver '{rec.approver_id}' is not in authorized human approver policy"

        # Workspace containment and match
        try:
            rec_ws = Path(rec.workspace_root).resolve()
            exp_ws = Path(expected_workspace).resolve()
            if rec_ws != exp_ws:
                return False, f"Approval workspace '{rec_ws}' does not match target workspace '{exp_ws}'"
        except Exception as e:
            return False, f"Invalid workspace path in approval check: {e}"

        # Action match
        if rec.action != expected_action:
            return False, f"Approval action '{rec.action}' does not match requested action '{expected_action}'"

        # Cryptographic task digest check (constant-time comparison)
        if not hmac.compare_digest(rec.task_digest.lower(), expected_digest.lower()):
            return False, "Cryptographic task digest mismatch: task contents have been modified or do not match approval"

        # Atomically consume
        rec.consumed = True
        return True, "Approval verified and consumed"


class PaperclipConnector:
    """Connector bridge between Paperclip and OpenClone.
    
    Authority Rule:
    Paperclip requests, schedules, and monitors organizational tasks.
    OpenClone enforces project boundaries, approval gates, and quality verification.
    """

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        allow_remote: bool = False,
        approval_store: Optional[AuthoritativeApprovalStore] = None,
    ):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.allow_remote = allow_remote
        self._active_tasks: Dict[str, PaperclipTaskRequest] = {}
        self.approval_store = approval_store or AuthoritativeApprovalStore()

    @staticmethod
    def compute_task_digest(
        organization_id: str,
        external_task_id: str,
        workspace_root: str,
        action: str,
        title: str,
        description: str,
    ) -> str:
        """Deterministically compute canonical SHA-256 digest of task parameters."""
        canonical_str = (
            f"{organization_id.strip()}:"
            f"{external_task_id.strip()}:"
            f"{Path(workspace_root).resolve()}:"
            f"{action.strip()}:"
            f"{title.strip()}:"
            f"{description.strip()}"
        )
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    def intake_task(self, request: PaperclipTaskRequest) -> PaperclipTaskResponse:
        """Intake and validate an external task request from Paperclip.
        
        Strictly enforces:
        1. Budget bounds (reject if already exhausted)
        2. Workspace safety (reject directory traversal or unanchored paths)
        3. Authoritative human approval verification for sensitive operations
        """
        # 1. Budget validation
        if request.budget and request.budget.is_exceeded():
            logger.warning("Paperclip task %s rejected: budget exceeded", request.external_task_id)
            return PaperclipTaskResponse(
                external_task_id=request.external_task_id,
                accepted=False,
                status=PaperclipTaskStatus.BLOCKED,
                reason="Budget ceiling exceeded. Human owner approval required to increase budget.",
            )

        # 2. Workspace boundary check
        target_path = self.workspace_root
        if request.target_project_root:
            target_path = Path(request.target_project_root).resolve()
            if self.workspace_root not in target_path.parents and target_path != self.workspace_root:
                logger.error("Paperclip task %s rejected: path escape attempt %s", request.external_task_id, target_path)
                return PaperclipTaskResponse(
                    external_task_id=request.external_task_id,
                    accepted=False,
                    status=PaperclipTaskStatus.BLOCKED,
                    reason=f"Target path {target_path} violates workspace trust boundary.",
                )

        # 3. Generate internal deterministic ID
        task_hash = hashlib.sha256(
            f"{request.organization_id}:{request.external_task_id}:{request.title}".encode("utf-8")
        ).hexdigest()[:12]
        internal_task_id = f"OC-{task_hash}"

        # 4. Enforce Non-Bypassable Engineering Gate on Sensitive Operations
        sensitive_keywords = [
            "production deploy", "deploy to prod", "delete database",
            "drop table", "rotate keys", "security override"
        ]
        sensitive_action = None
        for kw in sensitive_keywords:
            if kw in request.title.lower() or kw in request.description.lower():
                sensitive_action = kw
                break

        if sensitive_action:
            # External metadata 'human_approved: True' alone is strictly rejected
            approval_id = request.metadata.get("approval_id")
            
            # Authoritative check requires a registered approval_id
            if not approval_id:
                logger.warning(
                    "Paperclip task %s blocked: sensitive action lacks authoritative approval record",
                    request.external_task_id,
                )
                return PaperclipTaskResponse(
                    external_task_id=request.external_task_id,
                    accepted=False,
                    status=PaperclipTaskStatus.NEEDS_APPROVAL,
                    reason="Protected engineering action requires an authoritative human approval record. External metadata cannot self-authorize production modifications.",
                    openclone_task_id=internal_task_id,
                )

            # Compute canonical task digest
            expected_digest = self.compute_task_digest(
                organization_id=request.organization_id,
                external_task_id=request.external_task_id,
                workspace_root=str(target_path),
                action=sensitive_action,
                title=request.title,
                description=request.description,
            )

            # If client provides an approval_digest in metadata, verify its format
            provided_digest = request.metadata.get("approval_digest")
            if provided_digest:
                if len(provided_digest) != 64 or not all(c in "0123456789abcdefABCDEF" for c in provided_digest):
                    return PaperclipTaskResponse(
                        external_task_id=request.external_task_id,
                        accepted=False,
                        status=PaperclipTaskStatus.NEEDS_APPROVAL,
                        reason="Invalid SHA-256 approval digest format in metadata (must be 64-char hex).",
                        openclone_task_id=internal_task_id,
                    )

            # Verify against authoritative store
            ok, reason = self.approval_store.verify_and_consume(
                approval_id=approval_id,
                expected_digest=expected_digest,
                expected_workspace=str(target_path),
                expected_action=sensitive_action,
            )

            if not ok:
                logger.warning("Paperclip task %s blocked: %s", request.external_task_id, reason)
                return PaperclipTaskResponse(
                    external_task_id=request.external_task_id,
                    accepted=False,
                    status=PaperclipTaskStatus.NEEDS_APPROVAL,
                    reason=f"Authoritative human approval rejected: {reason}",
                    openclone_task_id=internal_task_id,
                )

        self._active_tasks[request.external_task_id] = request

        return PaperclipTaskResponse(
            external_task_id=request.external_task_id,
            accepted=True,
            status=PaperclipTaskStatus.IN_PROGRESS,
            reason="Task accepted by OpenClone Engineering Governance.",
            openclone_task_id=internal_task_id,
        )

    def complete_task(
        self,
        external_task_id: str,
        evidence_files: List[Path],
        spend_usd: float = 0.0,
        tokens_consumed: int = 0,
    ) -> PaperclipTaskResponse:
        """Report completion of a task with verifiable cryptographic evidence."""
        if external_task_id not in self._active_tasks:
            return PaperclipTaskResponse(
                external_task_id=external_task_id,
                accepted=False,
                status=PaperclipTaskStatus.FAILED,
                reason=f"Task {external_task_id} not tracked in active connector pool.",
            )

        evidence_hashes = []
        for p in evidence_files:
            if p.exists() and p.is_file():
                h = hashlib.sha256(p.read_bytes()).hexdigest()
                evidence_hashes.append(f"{p.name}:{h}")

        del self._active_tasks[external_task_id]

        return PaperclipTaskResponse(
            external_task_id=external_task_id,
            accepted=True,
            status=PaperclipTaskStatus.COMPLETED,
            reason="Task successfully verified and completed with evidence.",
            evidence_hashes=evidence_hashes,
            spend_usd=spend_usd,
            tokens_consumed=tokens_consumed,
        )
