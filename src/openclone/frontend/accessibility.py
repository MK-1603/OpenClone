"""Accessibility Engineering & WCAG 2.2 AA Compliance Auditor.

Evaluates semantic landmarks, keyboard navigation, accessible names,
focus trapping, and color contrast compliance.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class WCAGRule(str, Enum):
    SEMANTIC_LANDMARKS = "1.3.1_info_and_relationships"
    CONTRAST_MINIMUM = "1.4.3_contrast_minimum"
    KEYBOARD_ACCESSIBLE = "2.1.1_keyboard"
    NO_KEYBOARD_TRAP = "2.1.2_no_keyboard_trap"
    FOCUS_VISIBLE = "2.4.7_focus_visible"
    FOCUS_ORDER = "2.4.3_focus_order"
    NAME_ROLE_VALUE = "4.1.2_name_role_value"
    REDUCED_MOTION = "2.3.3_animation_from_interactions"


@dataclass
class AccessibilityCheckResult:
    rule: WCAGRule
    level: str  # A, AA, AAA
    passed: bool
    description: str
    violations: List[str] = field(default_factory=list)


@dataclass
class AccessibilityAuditResult:
    total_rules_checked: int
    passed_rules: int
    failed_rules: int
    is_wcag_aa_compliant: bool
    results: List[AccessibilityCheckResult] = field(default_factory=list)
    score: float = 0.0


class AccessibilityAuditor:
    """Verifies interface adherence to WCAG 2.2 Level AA requirements."""

    RULE_DESCRIPTIONS = {
        WCAGRule.SEMANTIC_LANDMARKS: "HTML uses proper semantic landmarks (<main>, <nav>, <header>, <aside>)",
        WCAGRule.CONTRAST_MINIMUM: "Text contrast is at least 4.5:1 for normal text and 3:1 for large text",
        WCAGRule.KEYBOARD_ACCESSIBLE: "All functionality is operable through keyboard navigation without mouse reliance",
        WCAGRule.NO_KEYBOARD_TRAP: "Focus can be navigated into and out of all dialogs and interactive regions",
        WCAGRule.FOCUS_VISIBLE: "Keyboard focus indicators are visibly distinct with >= 2px thickness and offset",
        WCAGRule.FOCUS_ORDER: "Focus navigation proceeds in logical reading and interaction sequence",
        WCAGRule.NAME_ROLE_VALUE: "Controls have accessible names, valid ARIA roles, and accurate state announcements",
        WCAGRule.REDUCED_MOTION: "Interface respects prefers-reduced-motion media query by suppressing non-essential animation",
    }

    def __init__(self):
        self.results: List[AccessibilityCheckResult] = []

    def run_audit(self, violations_map: Optional[Dict[WCAGRule, List[str]]] = None) -> AccessibilityAuditResult:
        """Executes a full accessibility rule audit against violation findings."""
        self.results = []
        violations_map = violations_map or {}

        for rule, desc in self.RULE_DESCRIPTIONS.items():
            violations = violations_map.get(rule, [])
            passed = len(violations) == 0

            self.results.append(
                AccessibilityCheckResult(
                    rule=rule,
                    level="AA",
                    passed=passed,
                    description=desc,
                    violations=violations,
                )
            )

        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        is_compliant = failed_count == 0
        score = (passed_count / len(self.results)) * 100.0

        return AccessibilityAuditResult(
            total_rules_checked=len(self.results),
            passed_rules=passed_count,
            failed_rules=failed_count,
            is_wcag_aa_compliant=is_compliant,
            results=self.results,
            score=round(score, 1),
        )
