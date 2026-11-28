"""Frontend Quality Gates & Interactive State Evaluation Engine.

Implements the mandatory 15 frontend quality gates and component-specific interactive
state validation models (Button, Input, Checkbox, DataTable, Dialog, Generic)
with structured evidence tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union


class ComponentState(str, Enum):
    """The 10 canonical interactive component states."""
    DEFAULT = "default"
    HOVER = "hover"
    FOCUS = "focus"
    ACTIVE = "active"
    DISABLED = "disabled"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"
    EMPTY = "empty"
    SELECTED = "selected"


class GateStatus(str, Enum):
    """Evaluation status for quality gates."""
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_VERIFIED = "NOT_VERIFIED"


@dataclass
class QualityGateResult:
    """Evaluation output for an individual quality gate."""
    gate_id: str
    name: str
    status: GateStatus
    details: str
    evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FrontendScorecard:
    """Overall frontend quality scorecard."""
    total_gates: int
    passed_gates: int
    failed_gates: int
    not_applicable: int
    compliance_score: float
    verdict: str  # PASS, FAIL, BLOCKED
    gate_results: List[QualityGateResult] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)


# Component-Specific State Expectations
COMPONENT_STATE_REQUIREMENTS: Dict[str, Set[ComponentState]] = {
    "button": {
        ComponentState.DEFAULT,
        ComponentState.HOVER,
        ComponentState.FOCUS,
        ComponentState.ACTIVE,
        ComponentState.DISABLED,
        ComponentState.LOADING,
    },
    "input": {
        ComponentState.DEFAULT,
        ComponentState.FOCUS,
        ComponentState.ACTIVE,
        ComponentState.DISABLED,
        ComponentState.ERROR,
    },
    "checkbox": {
        ComponentState.DEFAULT,
        ComponentState.HOVER,
        ComponentState.FOCUS,
        ComponentState.DISABLED,
        ComponentState.SELECTED,
    },
    "data_table": {
        ComponentState.DEFAULT,
        ComponentState.LOADING,
        ComponentState.EMPTY,
        ComponentState.ERROR,
    },
    "dialog": {
        ComponentState.DEFAULT,
        ComponentState.FOCUS,
        ComponentState.LOADING,
        ComponentState.ACTIVE,
    },
    "generic": {
        ComponentState.DEFAULT,
        ComponentState.HOVER,
        ComponentState.FOCUS,
        ComponentState.ACTIVE,
        ComponentState.DISABLED,
    },
}


def evaluate_component_states(
    implemented_states: Set[ComponentState],
    component_type: str = "generic",
) -> Dict[str, Any]:
    """Audits whether an interactive component implements its required states.
    
    Uses component-specific state requirements rather than forcing all 10 states
    onto every component (e.g. Data Tables need loading/empty/error; Buttons need hover/active/loading).
    """
    comp_key = component_type.lower().replace("-", "_")
    required = COMPONENT_STATE_REQUIREMENTS.get(comp_key, COMPONENT_STATE_REQUIREMENTS["generic"])

    missing_core = required - implemented_states
    has_full_lifecycle = {
        ComponentState.LOADING,
        ComponentState.SUCCESS,
        ComponentState.ERROR,
        ComponentState.EMPTY,
    }.issubset(implemented_states)

    is_complete = len(missing_core) == 0

    return {
        "component_type": component_type,
        "implemented_count": len(implemented_states),
        "total_possible": len(ComponentState),
        "required_for_type": [s.value for s in required],
        "missing_core_states": [s.value for s in missing_core],
        "is_core_complete": is_complete,
        "is_full_lifecycle": has_full_lifecycle,
        "coverage_ratio": len(implemented_states) / len(ComponentState),
    }


class FrontendQualityGate:
    """Evaluates the 15 mandatory frontend engineering quality gates."""

    GATES = [
        ("GATE-01", "Requirements", "Approved functional scope is satisfied without scope creep"),
        ("GATE-02", "Visual Design", "Consistent with approved design direction & 8px spatial grid"),
        ("GATE-03", "UX Workflows", "Main user workflows and journeys function without dead ends"),
        ("GATE-04", "Responsive Matrix", "Verified across 320px, 375px, 430px, 768px, 1024px, 1440px+"),
        ("GATE-05", "Accessibility (a11y)", "WCAG 2.2 AA compliant, full keyboard navigation & ARIA"),
        ("GATE-06", "Interactive States", "Component states (hover, focus, loading, error, etc.) verified"),
        ("GATE-07", "Component Architecture", "Modular feature-based design, props type-safe, reusable"),
        ("GATE-08", "Frontend Security", "No XSS vulnerabilities, safe HTML rendering, strict CSP"),
        ("GATE-09", "Secret Hygiene", "Zero private secrets or un-prefixed .env variables in client code"),
        ("GATE-10", "Performance Budgets", "Core Web Vitals within budget (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1)"),
        ("GATE-11", "Browser Compatibility", "Functional parity across modern Chromium, WebKit, and Gecko"),
        ("GATE-12", "Automated Testing", "Unit, component, and integration tests executed with 100% pass"),
        ("GATE-13", "Runtime Health", "Zero unhandled console errors or persistent hydration mismatches"),
        ("GATE-14", "Scope Governance", "Strict No AI Slope adherence; zero unrequested cosmetic rewrites"),
        ("GATE-15", "Evidence & Audit", "Verifiable audit evidence and scorecard generated"),
    ]

    def __init__(self):
        self.results: List[QualityGateResult] = []

    def evaluate_all(
        self,
        criteria_map: Dict[str, Union[bool, GateStatus, str]],
        evidence_map: Optional[Dict[str, Any]] = None,
    ) -> FrontendScorecard:
        """Evaluates all 15 gates against provided evidence and statuses."""
        evidence_map = evidence_map or {}
        self.results = []
        passed = 0
        failed = 0
        na = 0
        blockers = []

        for gate_id, name, desc in self.GATES:
            val = criteria_map.get(gate_id, criteria_map.get(name.lower(), True))
            evidence = evidence_map.get(gate_id, {})

            if isinstance(val, GateStatus):
                status = val
            elif isinstance(val, str):
                try:
                    status = GateStatus(val.upper())
                except ValueError:
                    status = GateStatus.PASS if val.lower() in ("true", "pass", "1") else GateStatus.FAIL
            else:
                status = GateStatus.PASS if bool(val) else GateStatus.FAIL

            details = f"{name}: {desc}"

            if status == GateStatus.PASS:
                passed += 1
            elif status == GateStatus.FAIL:
                failed += 1
                blockers.append(f"{gate_id} ({name}) failed: {desc}")
            elif status == GateStatus.BLOCKED:
                failed += 1
                blockers.append(f"{gate_id} ({name}) is blocked.")
            elif status == GateStatus.NOT_APPLICABLE:
                na += 1
            else:
                # NOT_VERIFIED counts as not yet passed
                failed += 1
                blockers.append(f"{gate_id} ({name}) not verified.")

            self.results.append(
                QualityGateResult(
                    gate_id=gate_id,
                    name=name,
                    status=status,
                    details=details,
                    evidence=evidence,
                )
            )

        active_gates = len(self.GATES) - na
        score = (passed / max(1, active_gates)) * 100.0 if active_gates > 0 else 100.0
        verdict = "PRODUCTION_READY" if failed == 0 else ("BLOCKED" if any(r.status == GateStatus.BLOCKED for r in self.results) else "NEEDS_REMEDIATION")

        return FrontendScorecard(
            total_gates=len(self.GATES),
            passed_gates=passed,
            failed_gates=failed,
            not_applicable=na,
            compliance_score=round(score, 1),
            verdict=verdict,
            gate_results=self.results,
            blockers=blockers,
        )
