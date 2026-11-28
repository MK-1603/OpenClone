"""Comprehensive Environmental and Platform Doctor for OpenClone."""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.platform.config.manager import ConfigurationManager
from src.openclone.platform.installation.detector import detect_installation_mode
from src.openclone.platform.runtime.toolchains import ToolchainInspector


@dataclass
class DiagnosticCheck:
    """Individual diagnostic inspection result."""
    category: str
    name: str
    status: str  # PASS, WARNING, ERROR, NOT_APPLICABLE
    details: str
    remediation: Optional[str] = None


class PlatformDoctor:
    """Performs deep environmental, installation, runtime, and platform checks."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.config_mgr = ConfigurationManager()

    def run_all_checks(self) -> List[DiagnosticCheck]:
        """Execute complete diagnostic suite."""
        checks: List[DiagnosticCheck] = []

        # 1. Installation Diagnostics
        inst_info = detect_installation_mode()
        checks.append(DiagnosticCheck(
            category="Installation",
            name="Installation Mode",
            status="PASS",
            details=f"Detected: {inst_info.mode} (Executable: {inst_info.executable_path})",
        ))

        # Check executable accessibility
        if Path(inst_info.executable_path).exists():
            checks.append(DiagnosticCheck(
                category="Installation",
                name="Executable Integrity",
                status="PASS",
                details=f"Binary accessible at {inst_info.executable_path}",
            ))
        else:
            checks.append(DiagnosticCheck(
                category="Installation",
                name="Executable Integrity",
                status="ERROR",
                details="Declared executable path not accessible",
                remediation="Reinstall OpenClone using your package manager.",
            ))

        # 2. Runtime Diagnostics
        py_tool = ToolchainInspector.inspect_python()
        if py_tool.available:
            checks.append(DiagnosticCheck(
                category="Runtime",
                name="Python Runtime",
                status="PASS",
                details=f"Python {py_tool.version} (supported)",
            ))
        else:
            checks.append(DiagnosticCheck(
                category="Runtime",
                name="Python Runtime",
                status="ERROR",
                details=f"Python {py_tool.version} (requires >= 3.10)",
                remediation="Upgrade Python to version 3.10 or newer.",
            ))

        # External Toolchains
        toolchains = ToolchainInspector.inspect_all()
        for t_key, t_stat in toolchains.items():
            if t_key == "python":
                continue
            if t_stat.available:
                checks.append(DiagnosticCheck(
                    category="Runtime",
                    name=f"Toolchain: {t_stat.name}",
                    status="PASS",
                    details=f"Found: {t_stat.path} ({t_stat.version or 'ok'})",
                ))
            elif t_stat.required:
                checks.append(DiagnosticCheck(
                    category="Runtime",
                    name=f"Toolchain: {t_stat.name}",
                    status="ERROR",
                    details=t_stat.error_message or "Required toolchain missing",
                    remediation=f"Install '{t_stat.name}' and ensure it is on your system PATH.",
                ))
            else:
                checks.append(DiagnosticCheck(
                    category="Runtime",
                    name=f"Toolchain: {t_stat.name}",
                    status="WARNING",
                    details="Optional toolchain not found",
                    remediation=f"Optional: Install '{t_stat.name}' for enhanced capabilities.",
                ))

        # 3. Environment & Configuration Diagnostics
        try:
            cfg = self.config_mgr.load_config()
            checks.append(DiagnosticCheck(
                category="Environment",
                name="User Configuration",
                status="PASS",
                details=f"Config path: {self.config_mgr.config_path} (Channel: {cfg.update.channel})",
            ))
        except Exception as e:
            checks.append(DiagnosticCheck(
                category="Environment",
                name="User Configuration",
                status="WARNING",
                details=f"Configuration read error: {e}",
                remediation="Run 'openclone config migrate' to reset or repair configuration.",
            ))

        # Workspace write access
        is_writeable = os.access(self.workspace_root, os.W_OK)
        checks.append(DiagnosticCheck(
            category="Environment",
            name="Workspace Write Access",
            status="PASS" if is_writeable else "ERROR",
            details=str(self.workspace_root),
            remediation=None if is_writeable else "Grant write permissions to workspace directory.",
        ))

        # 4. Platform Core Assets
        frozen_base = getattr(sys, "_MEIPASS", None)
        package_root = Path(__file__).resolve().parent.parent.parent
        worker_candidates = [
            package_root / "workforce" / "registry" / "workers",
            package_root.parent / "framework" / "workforce" / "registry" / "workers",
        ]
        if frozen_base:
            worker_candidates.insert(0, Path(frozen_base) / "src" / "openclone" / "workforce" / "registry" / "workers")
            worker_candidates.insert(1, Path(frozen_base) / "openclone" / "workforce" / "registry" / "workers")

        workers_dir = next((p for p in worker_candidates if p.exists()), package_root / "workforce" / "registry" / "workers")

        if workers_dir.exists():
            count = len(list(workers_dir.glob("*.json")))
            checks.append(DiagnosticCheck(
                category="Platform",
                name="Worker Contracts",
                status="PASS" if count >= 70 else "WARNING",
                details=f"{count} worker contracts verified",
            ))
        else:
            checks.append(DiagnosticCheck(
                category="Platform",
                name="Worker Contracts",
                status="ERROR",
                details="Worker contracts directory missing",
                remediation="Run 'openclone install repair' or reinstall package.",
            ))

        # Templates
        template_candidates = [
            package_root / "templates",
            package_root.parent / "framework" / "templates",
        ]
        if frozen_base:
            template_candidates.insert(0, Path(frozen_base) / "src" / "openclone" / "templates")
            template_candidates.insert(1, Path(frozen_base) / "openclone" / "templates")

        templates_dir = next((p for p in template_candidates if p.exists()), package_root / "templates")

        if templates_dir.exists() and (templates_dir / "PROJECT.template.md").exists():
            checks.append(DiagnosticCheck(
                category="Platform",
                name="Project Templates",
                status="PASS",
                details="Canonical project and agent templates verified",
            ))
        else:
            checks.append(DiagnosticCheck(
                category="Platform",
                name="Project Templates",
                status="WARNING",
                details="Packaged template files missing (using built-in fallbacks)",
            ))

        return checks

    def render_report(self, json_output: bool = False) -> int:
        """Render diagnostic report to stdout with exit code."""
        checks = self.run_all_checks()
        if json_output:
            data = [
                {
                    "category": c.category,
                    "name": c.name,
                    "status": c.status,
                    "details": c.details,
                    "remediation": c.remediation,
                }
                for c in checks
            ]
            print(json.dumps(data, indent=2))
            return 0 if all(c.status != "ERROR" for c in checks) else 1

        print("=== OpenClone Environmental & Platform Doctor ===")
        has_error = False
        for c in checks:
            badge = f"[{c.status:^7}]"
            print(f"  {badge} {c.category:13} : {c.name:24} -> {c.details}")
            if c.remediation:
                print(f"            Tip: {c.remediation}")
            if c.status == "ERROR":
                has_error = True

        total_pass = sum(1 for c in checks if c.status == "PASS")
        print(f"\nResult: {total_pass}/{len(checks)} checks passed.")

        # High-level category summary
        inst_ok = "PASS" if all(c.status != "ERROR" for c in checks if c.category == "Installation") else "FAIL"
        rt_ok = "PASS" if all(c.status != "ERROR" for c in checks if c.category == "Runtime") else "FAIL"
        pkg_ok = "PASS" if all(c.status != "ERROR" for c in checks if c.category == "Platform") else "FAIL"
        cfg_ok = "PASS" if all(c.status != "ERROR" for c in checks if c.category == "Environment") else "FAIL"
        cli_ok = "PASS" if all(c.status != "ERROR" for c in checks if "Executable" in c.name) else "FAIL"

        print("\nDiagnostic Summary:")
        print(f"  Installation     : {inst_ok}")
        print(f"  Runtime          : {rt_ok}")
        print(f"  Package Integrity: {pkg_ok}")
        print(f"  Configuration    : {cfg_ok}")
        print(f"  CLI              : {cli_ok}\n")

        if has_error:
            print("Status: Issues detected. Follow recommendations above.")
            return 1
        print("Status: All critical systems healthy.")
        return 0
