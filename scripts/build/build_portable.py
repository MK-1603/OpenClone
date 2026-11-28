#!/usr/bin/env python3
"""Build script for packaging OpenKryvex into a portable self-contained zip distribution.

Usage:
    python scripts/build/build_portable.py
"""

import shutil
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = REPO_ROOT / "dist"
STANDALONE_EXE = DIST_DIR / "openclone" / ("openclone.exe" if sys.platform == "win32" else "openclone")
PORTABLE_ZIP = DIST_DIR / "OpenKryvex-portable-v1.0.0.zip"


def build_portable():
    """Create self-contained portable package with ./data/ directory."""
    print("=== Packaging OpenKryvex Portable Distribution ===")
    
    stage_dir = DIST_DIR / "portable_staging"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create ./data/ directory for isolated storage
    (stage_dir / "data").mkdir(exist_ok=True)
    (stage_dir / "data" / "README.txt").write_text(
        "OpenKryvex Portable Data Directory.\nAll configuration, ledgers, and cache files will be stored here.\n",
        encoding="utf-8",
    )

    # 2. Copy binary if exists or placeholder guidance
    if STANDALONE_EXE.exists():
        shutil.copy2(STANDALONE_EXE, stage_dir / STANDALONE_EXE.name)
    else:
        print(f"Notice: Standalone executable not found at {STANDALONE_EXE}.")
        print("Creating portable launcher wrapper...")
        # Create a launcher batch script for Windows or shell script for Linux/macOS
        if sys.platform == "win32":
            (stage_dir / "openclone.cmd").write_text(
                "@echo off\r\nset OPENKRYVEX_PORTABLE=1\r\npython -m openclone %*\r\n",
                encoding="utf-8",
            )
        else:
            sh_launcher = stage_dir / "openclone"
            sh_launcher.write_text("#!/bin/sh\nexport OPENKRYVEX_PORTABLE=1\npython3 -m openclone \"$@\"\n", encoding="utf-8")
            sh_launcher.chmod(0o755)

    # 3. Copy License and Quickstart
    shutil.copy2(REPO_ROOT / "LICENSE", stage_dir / "LICENSE")
    (stage_dir / "PORTABLE_QUICKSTART.md").write_text(
        "# OpenKryvex Portable Edition\n\nRun `openclone --version` or `openclone doctor`.\nAll persistent state resides inside `./data/`.\n",
        encoding="utf-8",
    )

    # 4. Create ZIP archive
    print(f"Creating archive: {PORTABLE_ZIP}")
    with zipfile.ZipFile(PORTABLE_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in stage_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(stage_dir)
                zf.write(file, arcname)

    print(f"SUCCESS: Portable package created at {PORTABLE_ZIP}")
    shutil.rmtree(stage_dir)
    return 0


if __name__ == "__main__":
    sys.exit(build_portable())
