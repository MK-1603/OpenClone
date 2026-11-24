"""Frontend Quality Gates & Interactive State Evaluation Engine.

Implements the mandatory 15 frontend quality gates and 10 interactive component
states required for production-level frontend verification.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any


class ComponentState(str, Enum):
    """The 10 mandatory interactive component states."""
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
    verdict: str
    gate_results: List[QualityGateResult] = field(default_factory=list)


def evaluate_component_states(implemented_states: Set[ComponentState]) -> Dict[str, Any]:
    """Audits whether an interactive component implements the required states.
    
    A standard interactive component (e.g. Button, Form Field) requires at least
    the core interactive states: DEFAULT, HOVER, FOCUS, ACTIVE, and DISABLED.
    Data components also evaluate LOADING, SUCCESS, ERROR, and EMPTY.
    """
    required_core = {
        ComponentState.DEFAULT,
        ComponentState.HOVER,
        ComponentState.FOCUS,
        ComponentState.ACTIVE,
        ComponentState.DISABLED,
    }
    missing_core = required_core - implemented_states
    has_full_lifecycle = {
        ComponentState.LOADING,
        ComponentState.SUCCESS,
        ComponentState.ERROR,
        ComponentState.EMPTY,
    }.issubset(implemented_states)

    return {
        "implemented_count": len(implemented_states),
        "total_possible": len(ComponentState),
        "missing_core_states": [s.value for s in missing_core],
        "is_core_complete": len(missing_core) == 0,
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
        ("GATE-06", "Interactive States", "10 component states (hover, focus, loading, error, etc.) verified"),
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

    def evaluate_all(self, criteria_map: Dict[str, bool], evidence_map: Optional[Dict[str, Any]] = None) -> FrontendScorecard:
        """Evaluates all 15 gates against provided evidence boolean flags."""
        evidence_map = evidence_map or {}
        self.results = []
        passed = 0
        failed = 0
        na = 0

        for gate_id, name, desc in self.GATES:
            if gate_id not in criteria_map:
                status = GateStatus.NOT_APPLICABLE
                details = f"Not evaluated / omitted: {desc}"
                na += 1
            elif criteria_map[gate_id]:
                status = GateStatus.PASS
                details = f"Passed: {desc}"
                passed += 1
            else:
                status = GateStatus.FAIL
                details = f"Failed verification: {desc}"
                failed += 1

            self.results.append(
                QualityGateResult(
                    gate_id=gate_id,
                    name=name,
                    status=status,
                    details=details,
                    evidence=evidence_map.get(gate_id, {}),
                )
            )

        active_gates = passed + failed
        score = (passed / active_gates * 100.0) if active_gates > 0 else 0.0

        if failed == 0 and passed >= 12:
            verdict = "PRODUCTION_READY"
        elif failed == 0:
            verdict = "PARTIALLY_VERIFIED"
        else:
            verdict = "REJECTED_GATES_FAILED"

        return FrontendScorecard(
            total_gates=len(self.GATES),
            passed_gates=passed,
            failed_gates=failed,
            not_applicable=na,
            compliance_score=round(score, 1),
            verdict=verdict,
            gate_results=self.results,
        )
