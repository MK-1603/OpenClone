"""Toolchain inspection and validation for OpenClone runtime."""
from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ToolchainStatus:
    """Status of an external CLI tool or runtime dependency."""
    name: str
    available: bool
    path: Optional[str] = None
    version: Optional[str] = None
    required: bool = True
    error_message: Optional[str] = None


class ToolchainInspector:
    """Inspects development tools and runtime dependencies."""

    @staticmethod
    def inspect_python() -> ToolchainStatus:
        """Inspect active Python runtime."""
        ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        is_ok = sys.version_info >= (3, 10)
        return ToolchainStatus(
            name="Python",
            available=is_ok,
            path=sys.executable,
            version=ver,
            required=True,
            error_message=None if is_ok else "Python 3.10+ required",
        )

    @staticmethod
    def inspect_tool(name: str, cmd_args: List[str], required: bool = False) -> ToolchainStatus:
        """Inspect generic CLI tool by executing version check."""
        path = shutil.which(name)
        if not path:
            return ToolchainStatus(
                name=name,
                available=False,
                required=required,
                error_message=f"Executable '{name}' not found on system PATH",
            )
        try:
            res = subprocess.run(
                [path] + cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                check=False,
            )
            raw_out = (res.stdout or res.stderr).strip().splitlines()
            ver = raw_out[0] if raw_out else "available"
            return ToolchainStatus(
                name=name,
                available=True,
                path=path,
                version=ver[:60],
                required=required,
            )
        except Exception as e:
            return ToolchainStatus(
                name=name,
                available=False,
                path=path,
                required=required,
                error_message=str(e),
            )

    @classmethod
    def inspect_all(cls) -> Dict[str, ToolchainStatus]:
        """Perform comprehensive toolchain inspection."""
        return {
            "python": cls.inspect_python(),
            "git": cls.inspect_tool("git", ["--version"], required=True),
            "node": cls.inspect_tool("node", ["--version"], required=False),
            "npm": cls.inspect_tool("npm", ["--version"], required=False),
            "adb": cls.inspect_tool("adb", ["version"], required=False),
        }
