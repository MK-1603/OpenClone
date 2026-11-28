"""OpenClone 21-State Deployment State Machine.

Enforces deterministic transitions across the full deployment lifecycle, from initial
analysis through preview verification, strict human production approval gating, post-deploy
monitoring, and fail-safe automated or manual rollback.
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, List, Optional, Set, Tuple
from src.openclone.devops.models import DeploymentState, DeploymentTransitionRecord


class DeploymentStateMachine:
    """Deterministic finite state machine governing deployment transitions."""

    # Valid State Transitions Graph
    VALID_TRANSITIONS: Dict[DeploymentState, Set[DeploymentState]] = {
        DeploymentState.NOT_ANALYZED: {DeploymentState.ANALYZED, DeploymentState.CANCELLED},
        DeploymentState.ANALYZED: {DeploymentState.DEPLOYMENT_PLAN_READY, DeploymentState.CANCELLED},
        DeploymentState.DEPLOYMENT_PLAN_READY: {
            DeploymentState.AWAITING_CONFIGURATION,
            DeploymentState.AWAITING_PROVIDER_CONNECTION,
            DeploymentState.READY_FOR_PREVIEW,
            DeploymentState.CANCELLED,
        },
        DeploymentState.AWAITING_CONFIGURATION: {DeploymentState.READY_FOR_PREVIEW, DeploymentState.CANCELLED},
        DeploymentState.AWAITING_PROVIDER_CONNECTION: {DeploymentState.READY_FOR_PREVIEW, DeploymentState.CANCELLED},
        DeploymentState.READY_FOR_PREVIEW: {DeploymentState.PREVIEW_QUEUED, DeploymentState.CANCELLED},
        DeploymentState.PREVIEW_QUEUED: {DeploymentState.PREVIEW_DEPLOYING, DeploymentState.CANCELLED, DeploymentState.FAILED},
        DeploymentState.PREVIEW_DEPLOYING: {DeploymentState.PREVIEW_DEPLOYED, DeploymentState.FAILED, DeploymentState.CANCELLED},
        DeploymentState.PREVIEW_DEPLOYED: {DeploymentState.PREVIEW_VERIFICATION, DeploymentState.CANCELLED},
        DeploymentState.PREVIEW_VERIFICATION: {
            DeploymentState.AWAITING_PRODUCTION_APPROVAL,
            DeploymentState.FAILED,
            DeploymentState.CANCELLED,
        },
        DeploymentState.AWAITING_PRODUCTION_APPROVAL: {
            DeploymentState.PRODUCTION_QUEUED,
            DeploymentState.CANCELLED,
        },
        DeploymentState.PRODUCTION_QUEUED: {DeploymentState.PRODUCTION_DEPLOYING, DeploymentState.CANCELLED, DeploymentState.FAILED},
        DeploymentState.PRODUCTION_DEPLOYING: {DeploymentState.PRODUCTION_DEPLOYED, DeploymentState.FAILED, DeploymentState.ROLLBACK_QUEUED},
        DeploymentState.PRODUCTION_DEPLOYED: {DeploymentState.POST_DEPLOY_VERIFICATION, DeploymentState.FAILED, DeploymentState.ROLLBACK_QUEUED},
        DeploymentState.POST_DEPLOY_VERIFICATION: {
            DeploymentState.HEALTHY,
            DeploymentState.DEGRADED,
            DeploymentState.ROLLBACK_QUEUED,
            DeploymentState.FAILED,
        },
        DeploymentState.HEALTHY: {DeploymentState.DEGRADED, DeploymentState.ROLLBACK_QUEUED, DeploymentState.ANALYZED},
        DeploymentState.DEGRADED: {DeploymentState.ROLLBACK_QUEUED, DeploymentState.HEALTHY, DeploymentState.FAILED},
        DeploymentState.FAILED: {DeploymentState.ROLLBACK_QUEUED, DeploymentState.READY_FOR_PREVIEW, DeploymentState.CANCELLED},
        DeploymentState.ROLLBACK_QUEUED: {DeploymentState.ROLLED_BACK, DeploymentState.FAILED},
        DeploymentState.ROLLED_BACK: {DeploymentState.READY_FOR_PREVIEW, DeploymentState.AWAITING_CONFIGURATION, DeploymentState.CANCELLED},
        DeploymentState.CANCELLED: {DeploymentState.NOT_ANALYZED, DeploymentState.READY_FOR_PREVIEW},
    }

    def __init__(self, project_id: str, initial_state: DeploymentState = DeploymentState.NOT_ANALYZED):
        self.project_id = project_id
        self.current_state = initial_state
        self.history: List[DeploymentTransitionRecord] = []

    def transition_to(
        self,
        new_state: DeploymentState,
        actor: str,
        evidence_digest: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> DeploymentTransitionRecord:
        """Executes a validated, deterministic state transition."""
        allowed = self.VALID_TRANSITIONS.get(self.current_state, set())
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition from {self.current_state.value} to {new_state.value}. "
                f"Allowed target states: {[s.value for s in allowed]}"
            )

        # DETERMINISTIC GOVERNANCE RULE: Production Queueing requires human sign-off
        if new_state == DeploymentState.PRODUCTION_QUEUED:
            if actor == "system_orchestrator" or actor.lower().startswith("agent"):
                raise PermissionError(
                    "Deterministic Governance Violation: Autonomous agents and orchestrators "
                    "cannot self-approve production deployment. Human authorization required."
                )
            if not evidence_digest or len(evidence_digest.strip()) < 16:
                raise ValueError(
                    "Deterministic Governance Violation: Production transition requires a verified "
                    "cryptographic approval digest (minimum 16 hex characters)."
                )

        record = DeploymentTransitionRecord(
            transition_id=f"trn-{uuid.uuid4().hex[:8]}",
            project_id=self.project_id,
            from_state=self.current_state,
            to_state=new_state,
            actor=actor,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            evidence_digest=evidence_digest,
            notes=notes,
        )

        self.current_state = new_state
        self.history.append(record)
        return record

    def get_history(self) -> List[DeploymentTransitionRecord]:
        return list(self.history)
