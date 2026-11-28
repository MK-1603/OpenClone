"""OpenClone — Universal AI Software Engineering Platform."""
from pathlib import Path as _P

def _read_version():
    try:
        return (_P(__file__).resolve().parents[2] / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "1.0.0"

__version__ = _read_version()
__product__ = "OpenClone"
__platform__ = "OpenClone"
__standard__ = "AIEF"
