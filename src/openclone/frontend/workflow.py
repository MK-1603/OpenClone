"""Frontend Engineering Lifecycle Workflow Orchestrator.

Orchestrates the frontend engineering lifecycle with task-based execution levels:
- Level 1: Micro-changes & focused UI fixes
- Level 2: Feature engineering & component additions
- Level 3: Complete application engineering (all 18 stages)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class WorkflowPhase(str, Enum):
    """The 18 canonical frontend engineering lifecycle phases."""
    PHASE_01_PROJECT_REQUEST = "01_project_request"
    PHASE_02_PROJECT_UNDERSTANDING = "02_project_understanding"
    PHASE_03_PROJECT_CLASSIFICATION = "03_project_classification"
    PHASE_04_REQUIREMENTS_ANALYSIS = "04_requirements_analysis"
    PHASE_05_UX_RESEARCH_IA = "05_ux_research_ia"
    PHASE_06_VISUAL_DIRECTION_DS = "06_visual_direction_ds"
    PHASE_07_FRONTEND_ARCHITECTURE = "07_frontend_architecture"
    PHASE_08_RESPONSIVE_A11Y_PLAN = "08_responsive_a11y_plan"
    PHASE_09_TECHNOLOGY_SELECTION = "09_technology_selection"
    PHASE_10_APPROVED_PLAN = "10_approved_plan"
    PHASE_11_HUMAN_APPROVAL_GATE = "11_human_approval_gate"
    PHASE_12_FRONTEND_IMPLEMENTATION = "12_frontend_implementation"
    PHASE_13_FUNCTIONAL_TESTING = "13_functional_testing"
    PHASE_14_RESPONSIVE_VERIFICATION = "14_responsive_verification"
    PHASE_15_A11Y_VERIFICATION = "15_a11y_verification"
    PHASE_16_SECURITY_VERIFICATION = "16_security_verification"
    PHASE_17_PERFORMANCE_VERIFICATION = "17_performance_verification"
    PHASE_18_EVIDENCE_BASED_COMPLETION = "18_evidence_based_completion"


class TaskExecutionLevel(str, Enum):
    """Task-scaled lifecycle execution scope."""
    LEVEL_1_MICRO = "level_1_micro"              # Small CSS/component bug fix (5 stages)
    LEVEL_2_FEATURE = "level_2_feature"          # New feature/page/interaction (11 stages)
    LEVEL_3_COMPLETE_APP = "level_3_complete_app"# Greenfield / large enterprise app (18 stages)


@dataclass
class PhaseExecution:
    """Execution status and output evidence for an individual phase."""
    phase: WorkflowPhase
    status: str  # COMPLETED, SKIPPED, IN_PROGRESS, FAILED, BLOCKED
    output: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass
class WorkflowExecutionResult:
    """Consolidated outcome of the lifecycle workflow execution."""
    project_id: str
    is_success: bool
    completed_phases: int
    total_phases: int
    phases: List[PhaseExecution] = field(default_factory=list)
    verdict: str = ""
    level: TaskExecutionLevel = TaskExecutionLevel.LEVEL_3_COMPLETE_APP


class FrontendLifecycleWorkflow:
    """Orchestrates and tracks the frontend engineering lifecycle across task execution levels."""

    LEVEL_PHASES: Dict[TaskExecutionLevel, List[WorkflowPhase]] = {
        TaskExecutionLevel.LEVEL_1_MICRO: [
            WorkflowPhase.PHASE_01_PROJECT_REQUEST,
            WorkflowPhase.PHASE_04_REQUIREMENTS_ANALYSIS,
            WorkflowPhase.PHASE_12_FRONTEND_IMPLEMENTATION,
            WorkflowPhase.PHASE_13_FUNCTIONAL_TESTING,
            WorkflowPhase.PHASE_18_EVIDENCE_BASED_COMPLETION,
        ],
        TaskExecutionLevel.LEVEL_2_FEATURE: [
            WorkflowPhase.PHASE_01_PROJECT_REQUEST,
            WorkflowPhase.PHASE_03_PROJECT_CLASSIFICATION,
            WorkflowPhase.PHASE_04_REQUIREMENTS_ANALYSIS,
            WorkflowPhase.PHASE_06_VISUAL_DIRECTION_DS,
            WorkflowPhase.PHASE_07_FRONTEND_ARCHITECTURE,
            WorkflowPhase.PHASE_11_HUMAN_APPROVAL_GATE,
            WorkflowPhase.PHASE_12_FRONTEND_IMPLEMENTATION,
            WorkflowPhase.PHASE_13_FUNCTIONAL_TESTING,
            WorkflowPhase.PHASE_14_RESPONSIVE_VERIFICATION,
            WorkflowPhase.PHASE_15_A11Y_VERIFICATION,
            WorkflowPhase.PHASE_18_EVIDENCE_BASED_COMPLETION,
        ],
        TaskExecutionLevel.LEVEL_3_COMPLETE_APP: list(WorkflowPhase),
    }

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.phases: List[PhaseExecution] = []

    def execute_lifecycle(
        self,
        project_type: str,
        requirements: List[str],
        has_human_approval: bool = True,
        verification_results: Optional[Dict[str, bool]] = None,
        level: TaskExecutionLevel = TaskExecutionLevel.LEVEL_3_COMPLETE_APP,
    ) -> WorkflowExecutionResult:
        """Runs the lifecycle through the active phases for the designated task level."""
        verif = verification_results or {}
        self.phases = []
        active_phases = self.LEVEL_PHASES.get(level, list(WorkflowPhase))

        for phase in active_phases:
            status = "COMPLETED"
            notes = ""
            output: Dict[str, Any] = {}

            if phase == WorkflowPhase.PHASE_03_PROJECT_CLASSIFICATION:
                output = {"project_type": project_type}
            elif phase == WorkflowPhase.PHASE_04_REQUIREMENTS_ANALYSIS:
                output = {"requirements_count": len(requirements)}
            elif phase == WorkflowPhase.PHASE_11_HUMAN_APPROVAL_GATE:
                if not has_human_approval:
                    status = "BLOCKED"
                    notes = "Human release approval required before proceeding to implementation."
                else:
                    output = {"approved": True}
            elif phase in [
                WorkflowPhase.PHASE_13_FUNCTIONAL_TESTING,
                WorkflowPhase.PHASE_14_RESPONSIVE_VERIFICATION,
                WorkflowPhase.PHASE_15_A11Y_VERIFICATION,
                WorkflowPhase.PHASE_16_SECURITY_VERIFICATION,
                WorkflowPhase.PHASE_17_PERFORMANCE_VERIFICATION,
            ]:
                check_key = phase.value
                passed = verif.get(check_key, True)
                if not passed:
                    status = "FAILED"
                    notes = f"Verification failed for {phase.value}"
                output = {"passed": passed}

            self.phases.append(PhaseExecution(phase=phase, status=status, output=output, notes=notes))

            # Stop lifecycle if blocked or failed
            if status in ["BLOCKED", "FAILED"]:
                break

        completed = sum(1 for p in self.phases if p.status == "COMPLETED")
        is_success = (completed == len(active_phases))

        verdict = "VERIFIED_DELIVERY" if is_success else f"HALTED_AT_{self.phases[-1].phase.value}"

        return WorkflowExecutionResult(
            project_id=self.project_id,
            is_success=is_success,
            completed_phases=completed,
            total_phases=len(active_phases),
            phases=self.phases,
            verdict=verdict,
            level=level,
        )
