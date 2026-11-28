#!/usr/bin/env python3
"""OpenClone (AISDF) runtime CLI entrypoint shim."""
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from src.openclone.runtime.workforce import main

if __name__ == "__main__":
    sys.exit(main())
