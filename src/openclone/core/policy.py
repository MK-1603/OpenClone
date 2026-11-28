"""OpenClone Canonical Phase 0 Planning Boundary Policy.

Enforces strict separation between planning-time intelligence and autonomous target-project
implementation execution. Fails closed against unauthorized code mutation or implementation dispatches.
"""
from __future__ import annotations

import enum
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("openclone.core.policy")


class OperationClassification(str, enum.Enum):
    PLANNING_INSPECTION = "PLANNING_INSPECTION"
    SOCRATIC_CLARIFICATION = "SOCRATIC_CLARIFICATION"
    ARCHITECTURE_SYNTHESIS = "ARCHITECTURE_SYNTHESIS"
    PLAN_GENERATION = "PLAN_GENERATION"
    DEV_READINESS_EVALUATION = "DEV_READINESS_EVALUATION"
    INFRASTRUCTURE_RECOMMENDATION = "INFRASTRUCTURE_RECOMMENDATION"
    DEPLOYMENT_PLANNING = "DEPLOYMENT_PLANNING"
    TARGET_CODE_MUTATION = "TARGET_CODE_MUTATION"
    TARGET_TASK_EXECUTION = "TARGET_TASK_EXECUTION"
    TARGET_INFRASTRUCTURE_PROVISION = "TARGET_INFRASTRUCTURE_PROVISION"
    TARGET_PRODUCTION_DEPLOYMENT = "TARGET_PRODUCTION_DEPLOYMENT"


class Phase0BoundaryViolation(PermissionError):
    """Raised when an operation violates the Phase 0 Planning-Only boundary."""
    def __init__(self, message: str, operation: Optional[str] = None, audit_code: str = "ERR_PHASE0_BOUNDARY_VIOLATION"):
        super().__init__(message)
        self.operation = operation
        self.audit_code = audit_code


@dataclass
class BoundaryAuditRecord:
    operation: str
    classification: OperationClassification
    allowed: bool
    actor: str
    reason: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


class Phase0BoundaryPolicy:
    """Canonical governance engine enforcing Phase 0 planning boundaries."""

    _audit_log: List[BoundaryAuditRecord] = []

    ALLOWED_PHASE_0_OPERATIONS = {
        OperationClassification.PLANNING_INSPECTION,
        OperationClassification.SOCRATIC_CLARIFICATION,
        OperationClassification.ARCHITECTURE_SYNTHESIS,
        OperationClassification.PLAN_GENERATION,
        OperationClassification.DEV_READINESS_EVALUATION,
        OperationClassification.INFRASTRUCTURE_RECOMMENDATION,
        OperationClassification.DEPLOYMENT_PLANNING,
    }

    RESTRICTED_OPERATIONS = {
        OperationClassification.TARGET_CODE_MUTATION,
        OperationClassification.TARGET_TASK_EXECUTION,
        OperationClassification.TARGET_INFRASTRUCTURE_PROVISION,
        OperationClassification.TARGET_PRODUCTION_DEPLOYMENT,
    }

    @classmethod
    def check_operation(
        cls,
        classification: OperationClassification,
        actor: str = "anonymous",
        allow_external_execution: bool = False,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Evaluates whether an operation is permissible within the Phase 0 boundary.

        Fails closed on any target implementation execution unless explicit external
        human authorization digest is provided and verified.
        """
        if classification in cls.ALLOWED_PHASE_0_OPERATIONS:
            cls._audit_log.append(
                BoundaryAuditRecord(
                    operation=classification.value,
                    classification=classification,
                    allowed=True,
                    actor=actor,
                    reason="Planning-only operation permitted in Phase 0.",
                )
            )
            return True

        # Restricted target execution operation
        reason = (
            f"Phase 0 Boundary Enforced: Operation '{classification.value}' "
            "represents autonomous target-project execution and is strictly prohibited in Phase 0."
        )
        cls._audit_log.append(
            BoundaryAuditRecord(
                operation=classification.value,
                classification=classification,
                allowed=False,
                actor=actor,
                reason=reason,
            )
        )
        logger.warning(reason)
        raise Phase0BoundaryViolation(reason, operation=classification.value)

    @classmethod
    def get_audit_log(cls) -> List[BoundaryAuditRecord]:
        return list(cls._audit_log)
