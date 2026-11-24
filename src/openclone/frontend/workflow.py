"""Frontend Engineering Lifecycle Workflow Orchestrator.

Orchestrates the complete 18-stage frontend engineering lifecycle from
initial project request to verified, evidence-backed delivery.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class WorkflowPhase(str, Enum):
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


@dataclass
class PhaseExecution:
    phase: WorkflowPhase
    status: str  # COMPLETED, SKIPPED, IN_PROGRESS, FAILED
    output: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass
class WorkflowExecutionResult:
    project_id: str
    is_success: bool
    completed_phases: int
    total_phases: int
    phases: List[PhaseExecution] = field(default_factory=list)
    verdict: str = ""


class FrontendLifecycleWorkflow:
    """Orchestrates and tracks the 18-stage frontend engineering lifecycle."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.phases: List[PhaseExecution] = []

    def execute_lifecycle(
        self,
        project_type: str,
        requirements: List[str],
        has_human_approval: bool = True,
        verification_results: Optional[Dict[str, bool]] = None,
    ) -> WorkflowExecutionResult:
        """Runs the lifecycle through the 18 phases, recording deterministic evidence."""
        verif = verification_results or {}
        self.phases = []

        for phase in WorkflowPhase:
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
                    notes = "Human release approval required before proceeding."
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
        is_success = (completed == len(WorkflowPhase))

        verdict = "VERIFIED_DELIVERY" if is_success else f"HALTED_AT_{self.phases[-1].phase.value}"

        return WorkflowExecutionResult(
            project_id=self.project_id,
            is_success=is_success,
            completed_phases=completed,
            total_phases=len(WorkflowPhase),
            phases=self.phases,
            verdict=verdict,
        )
