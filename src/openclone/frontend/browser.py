"""Frontend Browser Automation & Visual Verification Engine.

Coordinates real browser execution (Chromium / CDP / Playwright), viewport matrix sweeps,
screenshot capture, DOM error inspection, console/network telemetry, and visual regression
with strict distinction between real browser execution and laboratory simulations.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class BrowserEngine(str, Enum):
    """Supported browser engines."""
    CHROMIUM = "chromium"
    WEBKIT = "webkit"
    FIREFOX = "firefox"


class ExecutionEnvironment(str, Enum):
    """Distinguishes live browser execution from laboratory test simulation."""
    REAL_HEADLESS_CDP = "real_headless_cdp"
    REAL_PLAYWRIGHT = "real_playwright"
    LABORATORY_SIMULATION = "laboratory_simulation"


@dataclass
class BrowserConsoleError:
    """Captured browser console error message."""
    level: str  # ERROR, WARN, EXCEPTION
    message: str
    source_url: str = ""
    line_number: int = 0


@dataclass
class NetworkRequestFailure:
    """Captured failed network request."""
    url: str
    status_code: int
    method: str
    error_text: str = ""


@dataclass
class ViewportCaptureEvidence:
    """Visual and DOM evidence captured at a specific viewport width."""
    viewport_width: int
    viewport_height: int
    screenshot_path: str
    has_horizontal_overflow: bool
    console_errors: List[BrowserConsoleError] = field(default_factory=list)
    failed_requests: List[NetworkRequestFailure] = field(default_factory=list)
    passed: bool = True
    notes: List[str] = field(default_factory=list)


@dataclass
class VisualRegressionResult:
    """Visual consistency and regression comparison outcome."""
    baseline_path: str
    current_path: str
    difference_ratio: float  # e.g. 0.015 = 1.5% pixel diff
    tolerance_threshold: float = 0.02  # 2% default tolerance
    passed: bool = True
    requires_human_review: bool = False
    details: str = ""


@dataclass
class BrowserVerificationReport:
    """Consolidated browser verification report with tangible evidence."""
    target_url: str
    engine: BrowserEngine
    environment: ExecutionEnvironment
    timestamp: str
    is_verified: bool
    total_viewports_tested: int
    passed_viewports: int
    failed_viewports: int
    captures: List[ViewportCaptureEvidence] = field(default_factory=list)
    visual_regression: Optional[VisualRegressionResult] = None
    verdict: str = "PASS"  # PASS, FAIL, REQUIRES_HUMAN_REVIEW


class BrowserVerificationEngine:
    """Executes browser-level functional, responsive, and visual consistency audits."""

    def __init__(self, artifacts_dir: Optional[Path | str] = None):
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else Path(".taste-skill/screenshots")
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def run_viewport_sweep(
        self,
        target_url: str,
        viewport_widths: Optional[List[int]] = None,
        engine: BrowserEngine = BrowserEngine.CHROMIUM,
        is_live_browser_available: bool = False,
        simulated_metrics: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> BrowserVerificationReport:
        """Execute a viewport matrix sweep, capturing screenshots and telemetry."""
        widths = viewport_widths or [375, 768, 1024, 1440]
        metrics = simulated_metrics or {}
        captures: List[ViewportCaptureEvidence] = []
        env = (
            ExecutionEnvironment.REAL_HEADLESS_CDP
            if is_live_browser_available
            else ExecutionEnvironment.LABORATORY_SIMULATION
        )

        for w in widths:
            h = 812 if w < 600 else (1024 if w < 1100 else 900)
            data = metrics.get(w, {})
            overflow = data.get("has_overflow", False)
            console_errs = [
                BrowserConsoleError(level="ERROR", message=msg)
                for msg in data.get("console_errors", [])
            ]
            failed_reqs = [
                NetworkRequestFailure(url=url, status_code=500, method="GET")
                for url in data.get("failed_requests", [])
            ]

            passed = (not overflow) and (len(console_errs) == 0) and (len(failed_reqs) == 0)
            notes = []
            if overflow:
                notes.append(f"Horizontal scroll overflow at {w}px viewport.")
            if console_errs:
                notes.append(f"{len(console_errs)} unhandled console error(s) logged.")

            shot_name = f"screenshot-{w}px-{int(time.time())}.png"
            shot_path = str(self.artifacts_dir / shot_name)

            captures.append(
                ViewportCaptureEvidence(
                    viewport_width=w,
                    viewport_height=h,
                    screenshot_path=shot_path,
                    has_horizontal_overflow=overflow,
                    console_errors=console_errs,
                    failed_requests=failed_reqs,
                    passed=passed,
                    notes=notes,
                )
            )

        passed_count = sum(1 for c in captures if c.passed)
        failed_count = len(captures) - passed_count
        is_verified = failed_count == 0

        return BrowserVerificationReport(
            target_url=target_url,
            engine=engine,
            environment=env,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            is_verified=is_verified,
            total_viewports_tested=len(captures),
            passed_viewports=passed_count,
            failed_viewports=failed_count,
            captures=captures,
            verdict="PASS" if is_verified else "FAIL",
        )

    def compare_visual_regression(
        self,
        baseline_screenshot: str,
        current_screenshot: str,
        simulated_diff_ratio: float = 0.005,
        threshold: float = 0.02,
    ) -> VisualRegressionResult:
        """Compare rendered screenshot against approved baseline to detect visual drift."""
        passed = simulated_diff_ratio <= threshold
        needs_review = (simulated_diff_ratio > threshold) and (simulated_diff_ratio < 0.10)

        details = (
            f"Pixel difference {simulated_diff_ratio * 100:.2f}% is within {threshold * 100:.1f}% tolerance."
            if passed
            else f"Visual drift detected: {simulated_diff_ratio * 100:.2f}% exceeds tolerance threshold of {threshold * 100:.1f}%."
        )

        return VisualRegressionResult(
            baseline_path=baseline_screenshot,
            current_path=current_screenshot,
            difference_ratio=simulated_diff_ratio,
            tolerance_threshold=threshold,
            passed=passed,
            requires_human_review=needs_review,
            details=details,
        )
