"""Platform installation manager for OpenClone."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Optional

from src.openclone.platform.installation.detector import detect_installation_mode, InstallationInfo


class PlatformInstallationManager:
    """Manages installation verification, integrity checks, and repair routines."""

    def __init__(self):
        self.info = detect_installation_mode()

    def get_info(self) -> InstallationInfo:
        """Return cached installation information."""
        return self.info

    def verify_installation(self) -> Dict[str, Any]:
        """Verify installation integrity and key assets."""
        issues: List[str] = []
        
        # Check executable existence
        if not Path(self.info.executable_path).exists():
            issues.append(f"Executable not found at declared path: {self.info.executable_path}")

        # Check bundled templates
        frozen_base = getattr(sys, "_MEIPASS", None)
        package_root = Path(__file__).resolve().parent.parent.parent
        templates_candidates = [
            package_root / "templates",
            package_root.parent / "framework" / "templates",
        ]
        workers_candidates = [
            package_root / "workforce" / "registry" / "workers",
            package_root.parent / "framework" / "workforce" / "registry" / "workers",
        ]
        if frozen_base:
            templates_candidates.insert(0, Path(frozen_base) / "src" / "openclone" / "templates")
            templates_candidates.insert(1, Path(frozen_base) / "openclone" / "templates")
            workers_candidates.insert(0, Path(frozen_base) / "src" / "openclone" / "workforce" / "registry" / "workers")
            workers_candidates.insert(1, Path(frozen_base) / "openclone" / "workforce" / "registry" / "workers")

        templates_dir = next((p for p in templates_candidates if p.exists()), package_root / "templates")
        workers_dir = next((p for p in workers_candidates if p.exists()), package_root / "workforce" / "registry" / "workers")

        if not templates_dir.exists():
            issues.append("Templates directory missing from package")
        if not workers_dir.exists():
            issues.append("Worker contracts directory missing from package")

        return {
            "mode": self.info.mode,
            "executable": self.info.executable_path,
            "intact": len(issues) == 0,
            "issues": issues,
            "is_writable": self.info.is_writable,
        }

    def get_repair_guidance(self) -> str:
        """Provide tailored repair instructions based on installation mode."""
        mode = self.info.mode
        if mode == "python-pipx":
            return "Run 'pipx reinstall openclone' to repair corrupt installation files."
        elif mode in ("python-pip", "python-venv"):
            return "Run 'pip install --upgrade --force-reinstall openclone' to repair packages."
        elif mode == "standalone-binary":
            return "Re-download the latest standalone binary from the official GitHub Release page."
        elif mode == "source-checkout":
            return "Run 'git status' and 'git checkout .' to restore pristine repository source."
        return "Re-download or reinstall OpenClone distribution."
