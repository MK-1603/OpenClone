#!/usr/bin/env python3
"""OpenClone (AISDF) CLI entrypoint compatibility shim."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

if __name__ == "__main__":
    from src.openclone.cli import main
    main()
