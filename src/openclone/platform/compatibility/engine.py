"""Multi-dimensional compatibility evaluation engine."""
from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class CompatibilityLevel(str, Enum):
    """Graded levels of platform compatibility."""
    FULLY_COMPATIBLE = "FULLY_COMPATIBLE"
    COMPATIBLE_WITH_MIGRATION = "COMPATIBLE_WITH_MIGRATION"
    COMPATIBLE_WITH_LIMITATIONS = "COMPATIBLE_WITH_LIMITATIONS"
    INCOMPATIBLE = "INCOMPATIBLE"
    UNKNOWN = "UNKNOWN"


@dataclass
class CompatibilityReport:
    """Detailed evaluation report across compatibility dimensions."""
    level: CompatibilityLevel
    reasons: List[str]
    system_profile: Dict[str, str]

    @property
    def is_compatible(self) -> bool:
        """True if operation can safely proceed without breaking changes."""
        return self.level in (
            CompatibilityLevel.FULLY_COMPATIBLE,
            CompatibilityLevel.COMPATIBLE_WITH_MIGRATION,
            CompatibilityLevel.COMPATIBLE_WITH_LIMITATIONS,
        )


class CompatibilityEngine:
    """Evaluates host system, Python runtime, and target requirements."""

    @staticmethod
    def get_current_system_profile() -> Dict[str, str]:
        """Capture host profile across operating system and architecture."""
        return {
            "os": sys.platform,
            "architecture": platform.machine().lower(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform_release": platform.release(),
        }

    @classmethod
    def evaluate(
        cls,
        min_python_version: str = "3.10.0",
        target_os: Optional[str] = None,
        target_arch: Optional[str] = None,
        schema_version: str = "1.0.0",
    ) -> CompatibilityReport:
        """Evaluate compatibility against target requirements."""
        profile = cls.get_current_system_profile()
        reasons: List[str] = []
        is_incompatible = False

        # 1. Python Runtime Evaluation
        py_ver = sys.version_info
        try:
            req_parts = [int(p) for p in min_python_version.split(".")[:3]]
            while len(req_parts) < 3:
                req_parts.append(0)
            if py_ver < tuple(req_parts):
                reasons.append(f"Incompatible Python version: {profile['python_version']} < {min_python_version}")
                is_incompatible = True
        except Exception:
            reasons.append(f"Could not parse minimum Python requirement '{min_python_version}'")

        # 2. Operating System Evaluation
        if target_os and target_os.lower() not in ("any", "all"):
            curr_os = profile["os"]
            expected = target_os.lower()
            if expected in ("windows", "win32") and not curr_os.startswith("win"):
                reasons.append(f"OS mismatch: expected Windows, running on {curr_os}")
                is_incompatible = True
            elif expected == "linux" and not curr_os.startswith("linux"):
                reasons.append(f"OS mismatch: expected Linux, running on {curr_os}")
                is_incompatible = True
            elif expected in ("macos", "darwin") and curr_os != "darwin":
                reasons.append(f"OS mismatch: expected macOS, running on {curr_os}")
                is_incompatible = True
            elif expected not in ("windows", "win32", "linux", "macos", "darwin"):
                reasons.append(f"Unrecognized or unsupported target OS '{target_os}'")
                is_incompatible = True

        # 3. CPU Architecture Evaluation
        if target_arch and target_arch.lower() not in ("any", "all", "universal"):
            curr_arch = profile["architecture"]
            expected_arch = target_arch.lower()
            if expected_arch in ("x64", "amd64", "x86_64") and curr_arch not in ("amd64", "x86_64"):
                reasons.append(f"CPU architecture mismatch: expected x64, running on {curr_arch}")
                is_incompatible = True

        if is_incompatible:
            return CompatibilityReport(level=CompatibilityLevel.INCOMPATIBLE, reasons=reasons, system_profile=profile)

        if reasons:
            return CompatibilityReport(level=CompatibilityLevel.COMPATIBLE_WITH_LIMITATIONS, reasons=reasons, system_profile=profile)

        return CompatibilityReport(level=CompatibilityLevel.FULLY_COMPATIBLE, reasons=["System fully compatible"], system_profile=profile)
