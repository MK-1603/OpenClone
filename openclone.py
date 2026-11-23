#!/usr/bin/env python3
"""OpenClone: Universal AI Software Engineering Framework.

Usage:
    python openclone.py <command> [options]
    openclone <command> [options]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

if __name__ == "__main__":
    from src.openclone.cli import main
    main()
