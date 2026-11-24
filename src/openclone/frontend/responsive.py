"""Responsive Engineering & Viewport Matrix Auditor.

Evaluates user interfaces across device form factors from 320px to 1440px+,
verifying zero horizontal overflow, appropriate touch targets, and fluid layout.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ViewportCategory(str, Enum):
    SMALL_MOBILE = "320px"
    STANDARD_MOBILE = "375px"
    LARGE_MOBILE = "430px"
    TABLET = "768px"
    LAPTOP_COMPACT = "1024px"
    LAPTOP_STANDARD = "1280px"
    DESKTOP_WIDE = "1440px"


@dataclass
class ViewportTestResult:
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
    total_viewports_tested: int
    passed_viewports: int
    failed_viewports: int
    is_fully_responsive: bool
    viewports: List[ViewportTestResult] = field(default_factory=list)
    summary: str = ""


class ResponsiveMatrixAuditor:
    """Audits layouts against the mandatory responsive viewport matrix."""

    VIEWPORT_WIDTHS = {
        ViewportCategory.SMALL_MOBILE: 320,
        ViewportCategory.STANDARD_MOBILE: 375,
        ViewportCategory.LARGE_MOBILE: 430,
        ViewportCategory.TABLET: 768,
        ViewportCategory.LAPTOP_COMPACT: 1024,
        ViewportCategory.LAPTOP_STANDARD: 1280,
        ViewportCategory.DESKTOP_WIDE: 1440,
    }

    MIN_TOUCH_TARGET = 44  # 44x44 CSS pixels required for touch

    def __init__(self):
        self.results: List[ViewportTestResult] = []

    def evaluate_viewport(
        self,
        category: ViewportCategory,
        has_horizontal_overflow: bool = False,
        min_touch_target_px: int = 44,
        interactive_elements_usable: bool = True,
        navigation_functional: bool = True,
    ) -> ViewportTestResult:
        """Audits a specific viewport resolution."""
        defects = []
        width = self.VIEWPORT_WIDTHS[category]

        if has_horizontal_overflow:
            defects.append(f"Horizontal overflow detected at {width}px viewport width.")

        # Touch targets matter for mobile/tablet widths (< 1024px)
        if width < 1024 and min_touch_target_px < self.MIN_TOUCH_TARGET:
            defects.append(
                f"Touch target size {min_touch_target_px}px is below minimum {self.MIN_TOUCH_TARGET}px at {width}px."
            )

        if not interactive_elements_usable:
            defects.append(f"Interactive controls obstructed or overlapping at {width}px.")

        if not navigation_functional:
            defects.append(f"Navigation menu or drawer failed to operate at {width}px.")

        passed = len(defects) == 0

        res = ViewportTestResult(
            viewport=category,
            width=width,
            has_horizontal_overflow=has_horizontal_overflow,
            min_touch_target_px=min_touch_target_px,
            interactive_elements_usable=interactive_elements_usable,
            navigation_functional=navigation_functional,
            passed=passed,
            defect_notes=defects,
        )
        self.results.append(res)
        return res

    def evaluate_matrix(self, observation_dict: Optional[Dict[ViewportCategory, Dict[str, Any]]] = None) -> ResponsiveAuditResult:
        """Evaluates all standard viewports across the matrix."""
        self.results = []
        obs = observation_dict or {}

        for category in ViewportCategory:
            viewport_obs = obs.get(category, {})
            self.evaluate_viewport(
                category=category,
                has_horizontal_overflow=viewport_obs.get("has_overflow", False),
                min_touch_target_px=viewport_obs.get("min_touch_px", 44),
                interactive_elements_usable=viewport_obs.get("usable", True),
                navigation_functional=viewport_obs.get("nav_ok", True),
            )

        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        all_passed = failed_count == 0

        summary = (
            f"Responsive Matrix Audit: {passed_count}/{len(self.results)} viewports passed. "
            + ("Layout is clean and fully responsive." if all_passed else f"{failed_count} viewports contain layout defects.")
        )

        return ResponsiveAuditResult(
            total_viewports_tested=len(self.results),
            passed_viewports=passed_count,
            failed_viewports=failed_count,
            is_fully_responsive=all_passed,
            viewports=self.results,
            summary=summary,
        )
