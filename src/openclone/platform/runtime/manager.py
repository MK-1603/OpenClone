"""Runtime environment and execution management for OpenClone."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from src.openclone.platform.runtime.toolchains import ToolchainInspector, ToolchainStatus


class RuntimeManager:
    """Oversees runtime environment, resource resolution, and sandboxed execution."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def get_python_info(self) -> Dict[str, str]:
        """Return structured runtime information about current Python."""
        return {
            "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "executable": sys.executable,
            "platform": sys.platform,
            "is_venv": hasattr(sys, "real_prefix") or (sys.base_prefix != sys.prefix),
            "prefix": sys.prefix,
        }

    def check_toolchains(self) -> Dict[str, ToolchainStatus]:
        """Run toolchain inspections."""
        return ToolchainInspector.inspect_all()

    def resolve_package_resource(self, relative_path: str) -> Optional[Path]:
        """Resolve a packaged resource path safely across wheel, frozen, and dev checkouts."""
        # Check PyInstaller frozen bundle path
        frozen_base = getattr(sys, "_MEIPASS", None)
        if frozen_base:
            p = Path(frozen_base) / relative_path
            if p.exists():
                return p

        # Check relative to openclone package root
        package_root = Path(__file__).resolve().parent.parent.parent
        p = package_root / relative_path
        if p.exists():
            return p

        # Check repository root
        repo_root = package_root.parent
        p = repo_root / relative_path
        if p.exists():
            return p

        return None
