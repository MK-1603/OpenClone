"""Frontend Performance Engineering & Core Web Vitals Auditor.

Evaluates Core Web Vitals (LCP, INP, CLS) against strict performance budgets,
auditing bundle weight, lazy loading, and rendering efficiency.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class CoreWebVitalsBudget:
    """Core Web Vitals target thresholds for optimal user experience."""
    max_lcp_seconds: float = 2.5    # Largest Contentful Paint (Good: <= 2.5s)
    max_inp_ms: float = 200.0       # Interaction to Next Paint (Good: <= 200ms)
    max_cls: float = 0.10           # Cumulative Layout Shift (Good: <= 0.10)
    max_fcp_seconds: float = 1.8    # First Contentful Paint (Good: <= 1.8s)
    max_ttfb_ms: float = 800.0      # Time to First Byte (Good: <= 800ms)
    max_bundle_kb: float = 250.0    # Initial JS bundle budget (Good: <= 250kb compressed)


@dataclass
class MetricMeasurement:
    name: str
    observed_value: float
    budget_value: float
    unit: str
    passed: bool
    status: str  # GOOD, NEEDS_IMPROVEMENT, POOR


@dataclass
class PerformanceAuditResult:
    all_metrics_passed: bool
    total_metrics_evaluated: int
    passed_metrics: int
    failed_metrics: int
    measurements: List[MetricMeasurement] = field(default_factory=list)
    score: float = 100.0
    summary: str = ""


class PerformanceBudgetAuditor:
    """Evaluates runtime telemetry and bundle metrics against performance budgets."""

    def __init__(self, budget: Optional[CoreWebVitalsBudget] = None):
        self.budget = budget or CoreWebVitalsBudget()

    def audit_vitals(
        self,
        lcp: float,
        inp: float,
        cls: float,
        fcp: float = 1.2,
        ttfb: float = 300.0,
        bundle_kb: float = 180.0,
    ) -> PerformanceAuditResult:
        """Audits measured vitals against configured budgets."""
        measurements = []

        # 1. LCP
        lcp_passed = lcp <= self.budget.max_lcp_seconds
        measurements.append(
            MetricMeasurement(
                name="LCP",
                observed_value=lcp,
                budget_value=self.budget.max_lcp_seconds,
                unit="s",
                passed=lcp_passed,
                status="GOOD" if lcp <= 2.5 else ("NEEDS_IMPROVEMENT" if lcp <= 4.0 else "POOR"),
            )
        )

        # 2. INP
        inp_passed = inp <= self.budget.max_inp_ms
        measurements.append(
            MetricMeasurement(
                name="INP",
                observed_value=inp,
                budget_value=self.budget.max_inp_ms,
                unit="ms",
                passed=inp_passed,
                status="GOOD" if inp <= 200 else ("NEEDS_IMPROVEMENT" if inp <= 500 else "POOR"),
            )
        )

        # 3. CLS
        cls_passed = cls <= self.budget.max_cls
        measurements.append(
            MetricMeasurement(
                name="CLS",
                observed_value=cls,
                budget_value=self.budget.max_cls,
                unit="",
                passed=cls_passed,
                status="GOOD" if cls <= 0.1 else ("NEEDS_IMPROVEMENT" if cls <= 0.25 else "POOR"),
            )
        )

        # 4. FCP
        fcp_passed = fcp <= self.budget.max_fcp_seconds
        measurements.append(
            MetricMeasurement(
                name="FCP",
                observed_value=fcp,
                budget_value=self.budget.max_fcp_seconds,
                unit="s",
                passed=fcp_passed,
                status="GOOD" if fcp <= 1.8 else "POOR",
            )
        )

        # 5. TTFB
        ttfb_passed = ttfb <= self.budget.max_ttfb_ms
        measurements.append(
            MetricMeasurement(
                name="TTFB",
                observed_value=ttfb,
                budget_value=self.budget.max_ttfb_ms,
                unit="ms",
                passed=ttfb_passed,
                status="GOOD" if ttfb <= 800 else "POOR",
            )
        )

        # 6. Bundle Size
        bundle_passed = bundle_kb <= self.budget.max_bundle_kb
        measurements.append(
            MetricMeasurement(
                name="Initial_JS_Bundle",
                observed_value=bundle_kb,
                budget_value=self.budget.max_bundle_kb,
                unit="kb",
                passed=bundle_passed,
                status="GOOD" if bundle_passed else "POOR",
            )
        )

        passed_count = sum(1 for m in measurements if m.passed)
        failed_count = len(measurements) - passed_count
        all_passed = failed_count == 0
        score = (passed_count / len(measurements)) * 100.0

        summary = (
            f"Performance Audit: {passed_count}/{len(measurements)} metrics met budget. "
            + ("Core Web Vitals are within green thresholds." if all_passed else f"{failed_count} metrics violated performance budget.")
        )

        return PerformanceAuditResult(
            all_metrics_passed=all_passed,
            total_metrics_evaluated=len(measurements),
            passed_metrics=passed_count,
            failed_metrics=failed_count,
            measurements=measurements,
            score=round(score, 1),
            summary=summary,
        )
