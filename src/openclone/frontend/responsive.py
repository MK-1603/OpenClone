"""Responsive Engineering & Viewport Matrix Auditor.

Evaluates user interfaces across device form factors from 320px to 1440px+,
verifying zero horizontal overflow, 44px minimum touch targets, navigation ergonomics,
and task-based viewport verification levels (Micro, Feature, Full App).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ViewportCategory(str, Enum):
    """Canonical device viewport matrix."""
    SMALL_MOBILE = "320px"
    STANDARD_MOBILE = "375px"
    LARGE_MOBILE = "430px"
    TABLET = "768px"
    LAPTOP_COMPACT = "1024px"
    LAPTOP_STANDARD = "1280px"
    DESKTOP_WIDE = "1440px"


class TaskVerificationLevel(str, Enum):
    """Task-scaled verification scope to avoid testing all viewports on micro-fixes."""
    LEVEL_1_MICRO = "level_1_micro"          # Tests Mobile (375px) and Desktop (1440px)
    LEVEL_2_FEATURE = "level_2_feature"      # Tests Mobile (375px), Tablet (768px), Desktop (1440px)
    LEVEL_3_FULL_APP = "level_3_full_app"    # Full 7-tier matrix evaluation


@dataclass
class ViewportTestResult:
    """Evaluation result for an individual viewport width."""
    viewport: ViewportCategory
    width: int
    has_horizontal_overflow: bool
    min_touch_target_px: int
    interactive_elements_usable: bool
    navigation_functional: bool
    passed: bool
    defect_notes: List[str] = field(default_factory=list)


@dataclass
class ResponsiveAuditResult:
    """Complete responsive viewport matrix verification report."""
    total_viewports_tested: int
    passed_viewports: int
    failed_viewports: int
    is_fully_responsive: bool
    viewports: List[ViewportTestResult] = field(default_factory=list)
    summary: str = ""


class ResponsiveMatrixAuditor:
    """Audits interfaces across the responsive viewport matrix with touch-target gating."""

    VIEWPORT_WIDTHS: Dict[ViewportCategory, int] = {
        ViewportCategory.SMALL_MOBILE: 320,
        ViewportCategory.STANDARD_MOBILE: 375,
        ViewportCategory.LARGE_MOBILE: 430,
        ViewportCategory.TABLET: 768,
        ViewportCategory.LAPTOP_COMPACT: 1024,
        ViewportCategory.LAPTOP_STANDARD: 1280,
        ViewportCategory.DESKTOP_WIDE: 1440,
    }

    LEVEL_VIEWPORTS: Dict[TaskVerificationLevel, List[ViewportCategory]] = {
        TaskVerificationLevel.LEVEL_1_MICRO: [
            ViewportCategory.STANDARD_MOBILE,
            ViewportCategory.DESKTOP_WIDE,
        ],
        TaskVerificationLevel.LEVEL_2_FEATURE: [
            ViewportCategory.STANDARD_MOBILE,
            ViewportCategory.TABLET,
            ViewportCategory.DESKTOP_WIDE,
        ],
        TaskVerificationLevel.LEVEL_3_FULL_APP: list(VIEWPORT_WIDTHS.keys()),
    }

    MIN_TOUCH_TARGET = 44  # 44x44 CSS pixels mandatory for touch viewports (WCAG 2.5.5 / 2.5.8)

    def __init__(self):
        self.results: List[ViewportTestResult] = []

    def run_matrix_audit(
        self,
        viewport_metrics: Optional[Dict[ViewportCategory, Dict[str, Any]]] = None,
        level: TaskVerificationLevel = TaskVerificationLevel.LEVEL_3_FULL_APP,
    ) -> ResponsiveAuditResult:
        """Execute responsive audit across target viewports for the specified task level."""
        self.results = []
        metrics = viewport_metrics or {}
        target_viewports = self.LEVEL_VIEWPORTS.get(level, list(self.VIEWPORT_WIDTHS.keys()))

        for vp in target_viewports:
            width = self.VIEWPORT_WIDTHS[vp]
            data = metrics.get(vp) or metrics.get(vp.value) or metrics.get(vp.name) or {}

            has_overflow = data.get("has_horizontal_overflow", data.get("has_overflow", False))
            touch_target = data.get("min_touch_target_px", data.get("min_touch_px", self.MIN_TOUCH_TARGET))
            interactive_ok = data.get("interactive_elements_usable", data.get("usable", True))
            nav_ok = data.get("navigation_functional", data.get("nav_ok", True))

            defects = []
            if has_overflow:
                defects.append(f"Horizontal scroll overflow detected at {width}px.")

            # Touch target enforcement on mobile/tablet viewports (<= 820px)
            if width <= 820 and touch_target < self.MIN_TOUCH_TARGET:
                defects.append(
                    f"Touch target {touch_target}px is smaller than 44x44px minimum at {width}px."
                )

            if not interactive_ok:
                defects.append(f"Interactive element clipping or occlusion detected at {width}px.")
            if not nav_ok:
                defects.append(f"Navigation collapsed or unresponsive at {width}px.")

            passed = len(defects) == 0

            self.results.append(
                ViewportTestResult(
                    viewport=vp,
                    width=width,
                    has_horizontal_overflow=has_overflow,
                    min_touch_target_px=touch_target,
                    interactive_elements_usable=interactive_ok,
                    navigation_functional=nav_ok,
                    passed=passed,
                    defect_notes=defects,
                )
            )

        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        is_responsive = failed_count == 0

        summary = (
            f"Responsive audit passed across {passed_count}/{len(self.results)} viewports (Level: {level.value})."
            if is_responsive
            else f"Responsive audit failed: {failed_count} viewport(s) contain defects."
        )

        return ResponsiveAuditResult(
            total_viewports_tested=len(self.results),
            passed_viewports=passed_count,
            failed_viewports=failed_count,
            is_fully_responsive=is_responsive,
            viewports=self.results,
            summary=summary,
        )

    def evaluate_matrix(
        self, viewport_metrics: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> ResponsiveAuditResult:
        """Alias to evaluate responsive matrix against viewport metrics."""
        return self.run_matrix_audit(viewport_metrics=viewport_metrics)

    def evaluate(
        self, viewport_metrics: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> ResponsiveAuditResult:
        """Alias for evaluate_matrix / run_matrix_audit."""
        return self.run_matrix_audit(viewport_metrics=viewport_metrics)
