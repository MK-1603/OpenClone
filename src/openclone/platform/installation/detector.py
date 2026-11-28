"""Installation mode and environment detection for OpenClone."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class InstallationInfo:
    """Detailed metadata about the running OpenClone installation."""
    mode: str  # 'standalone-binary', 'python-pipx', 'python-pip', 'python-venv', 'portable', 'source-checkout'
    executable_path: str
    install_prefix: str
    is_frozen: bool
    is_portable: bool
    is_writable: bool
    package_version: str = "1.0.0"


def detect_installation_mode() -> InstallationInfo:
    """Detect how OpenClone is currently running."""
    exe = sys.executable
    is_frozen = getattr(sys, "frozen", False)
    
    # 1. Portable Mode Check (OpenClone primary, OpenKryvex fallback)
    data_dir = Path("./data")
    is_portable = data_dir.is_dir() or os.environ.get("OPENCLONE_PORTABLE", "").lower() in ("1", "true") or os.environ.get("OPENKRYVEX_PORTABLE", "").lower() in ("1", "true")

    # 2. Frozen Standalone Binary (PyInstaller)
    if is_frozen:
        mode = "portable" if is_portable else "standalone-binary"
        install_prefix = str(Path(exe).parent)
        is_writable = os.access(install_prefix, os.W_OK)
        return InstallationInfo(
            mode=mode,
            executable_path=exe,
            install_prefix=install_prefix,
            is_frozen=True,
            is_portable=is_portable,
            is_writable=is_writable,
        )

    # 3. Pipx Environment Check
    pipx_home = os.environ.get("PIPX_HOME", "pipx")
    is_pipx = pipx_home in exe or "pipx" in str(Path(exe).parts)

    # 4. Virtualenv / Pip
    is_venv = hasattr(sys, "real_prefix") or (sys.base_prefix != sys.prefix)
    
    # Check if running from source checkout (has pyproject.toml in parents)
    package_dir = Path(__file__).resolve().parent.parent.parent
    is_source = (package_dir.parent / "pyproject.toml").exists() and (package_dir.parent / ".git").exists()

    if is_portable:
        mode = "portable"
    elif is_source:
        mode = "source-checkout"
    elif is_pipx:
        mode = "python-pipx"
    elif is_venv:
        mode = "python-venv"
    else:
        mode = "python-pip"

    install_prefix = sys.prefix
    is_writable = os.access(install_prefix, os.W_OK)

    return InstallationInfo(
        mode=mode,
        executable_path=exe,
        install_prefix=install_prefix,
        is_frozen=False,
        is_portable=is_portable,
        is_writable=is_writable,
    )
