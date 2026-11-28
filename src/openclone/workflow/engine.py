"""OpenClone Canonical Workflow Engine.

Orchestrates the 10-stage engineering lifecycle with checkpointing,
state persistence, failure recovery, and audit ledger tracking.
"""
from __future__ import annotations

import enum
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("openclone.workflow.engine")


class WorkflowStage(str, enum.Enum):
    REQUEST = "request"
    UNDERSTANDING = "understanding"
    PROJECT_ANALYSIS = "project_analysis"
    PLANNING = "planning"
    ENGINEERING_SELECTION = "engineering_selection"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    SECURITY_REVIEW = "security_review"
    INDEPENDENT_VERIFICATION = "independent_verification"
    DELIVERY = "delivery"


class StageStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    BLOCKED_APPROVAL = "BLOCKED_APPROVAL"


@dataclass
class WorkflowCheckpoint:
    stage: WorkflowStage
    status: StageStatus
    timestamp: float = field(default_factory=time.time)
    output: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage.value,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "output": self.output,
            "error_message": self.error_message,
        }


class WorkflowEngine:
    """Manages the configurable 10-stage engineering lifecycle."""

    CANONICAL_STAGES = [
        WorkflowStage.REQUEST,
        WorkflowStage.UNDERSTANDING,
        WorkflowStage.PROJECT_ANALYSIS,
        WorkflowStage.PLANNING,
        WorkflowStage.ENGINEERING_SELECTION,
        WorkflowStage.IMPLEMENTATION,
        WorkflowStage.TESTING,
        WorkflowStage.SECURITY_REVIEW,
        WorkflowStage.INDEPENDENT_VERIFICATION,
        WorkflowStage.DELIVERY,
    ]

    def __init__(self, workspace_root: Optional[Path] = None, workflow_id: Optional[str] = None):
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
        self.workflow_id = workflow_id or f"wf-{int(time.time())}"
        self.checkpoints: Dict[WorkflowStage, WorkflowCheckpoint] = {
            s: WorkflowCheckpoint(stage=s, status=StageStatus.PENDING) for s in self.CANONICAL_STAGES
        }
        self.current_stage: WorkflowStage = WorkflowStage.REQUEST
        self.state_file = self.workspace_root / ".openclone" / f"{self.workflow_id}.json"

    def advance_stage(self, stage: WorkflowStage, status: StageStatus, output: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> None:
        """Record stage checkpoint and advance lifecycle."""
        self.current_stage = stage
        self.checkpoints[stage] = WorkflowCheckpoint(
            stage=stage,
            status=status,
            timestamp=time.time(),
            output=output or {},
            error_message=error,
        )
        self.persist_state()

    def persist_state(self) -> None:
        """Persist state to workspace ledger directory."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "workflow_id": self.workflow_id,
                "current_stage": self.current_stage.value,
                "checkpoints": {s.value: cp.to_dict() for s, cp in self.checkpoints.items()},
                "updated_at": time.time(),
            }
            self.state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to persist workflow state: {e}")

    def load_state(self) -> bool:
        """Load state from persistence file if present."""
        if not self.state_file.exists():
            return False
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            self.workflow_id = data.get("workflow_id", self.workflow_id)
            self.current_stage = WorkflowStage(data.get("current_stage", WorkflowStage.REQUEST.value))
            for s_val, cp_data in data.get("checkpoints", {}).items():
                stg = WorkflowStage(s_val)
                self.checkpoints[stg] = WorkflowCheckpoint(
                    stage=stg,
                    status=StageStatus(cp_data.get("status", "PENDING")),
                    timestamp=cp_data.get("timestamp", time.time()),
                    output=cp_data.get("output", {}),
                    error_message=cp_data.get("error_message"),
                )
            return True
        except Exception as e:
            logger.error(f"Failed to restore workflow state: {e}")
            return False

    def get_progress_summary(self) -> Dict[str, Any]:
        completed = sum(1 for cp in self.checkpoints.values() if cp.status == StageStatus.COMPLETED)
        return {
            "workflow_id": self.workflow_id,
            "current_stage": self.current_stage.value,
            "total_stages": len(self.CANONICAL_STAGES),
            "completed_stages": completed,
            "progress_pct": round((completed / len(self.CANONICAL_STAGES)) * 100, 1),
            "is_complete": self.checkpoints[WorkflowStage.DELIVERY].status == StageStatus.COMPLETED,
        }
