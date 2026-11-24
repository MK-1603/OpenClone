"""OpenClone local control plane runtime."""
from __future__ import annotations
from pathlib import Path
from src.openclone.runtime import workforce

def _get_version():
    try:
        return (Path(__file__).resolve().parents[3] / "VERSION").read_text(encoding="utf-8").strip()
    except Exception:
        return "1.0.0"

__version__ = _get_version()
__all__ = ["workforce", "__version__"]
