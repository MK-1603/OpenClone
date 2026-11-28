#!/usr/bin/env python3
"""Build script for compiling OpenKryvex into a standalone binary using PyInstaller.

Usage:
    python scripts/build/build_standalone.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = REPO_ROOT / "packaging" / "pyinstaller" / "openclone.spec"


def build_standalone():
    """Run PyInstaller with the official OpenKryvex specification."""
    print("=== Building OpenKryvex Standalone Executable ===")
    print(f"Repository Root: {REPO_ROOT}")
    print(f"Spec File:       {SPEC_PATH}")

    # Check PyInstaller availability
    try:
        import PyInstaller
        print(f"PyInstaller Version: {PyInstaller.__version__}")
    except ImportError:
        print("ERROR: PyInstaller is not installed in the current environment.")
        print("Run: pip install pyinstaller")
        return 1

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(SPEC_PATH),
    ]

    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if res.returncode == 0:
        print("\nSUCCESS: Standalone executable built in dist/ directory.")
    else:
        print(f"\nFAILED: Standalone build failed with exit code {res.returncode}")
    return res.returncode


if __name__ == "__main__":
    sys.exit(build_standalone())
