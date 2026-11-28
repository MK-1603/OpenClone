"""OpenClone — Universal AI Software Engineering Platform."""
import sys
from pathlib import Path

# Add src/openclone to __path__ so that submodules (openclone.runtime, openclone.platform, etc.) resolve directly
_src_pkg = Path(__file__).resolve().parent.parent / "src" / "openclone"
if _src_pkg.is_dir() and str(_src_pkg) not in __path__:
    __path__.append(str(_src_pkg))
else:
    # Check adjacent site-packages/src/openclone if installed
    _site_src = Path(__file__).resolve().parent.parent / "src" / "openclone"
    if _site_src.is_dir() and str(_site_src) not in __path__:
        __path__.append(str(_site_src))

from src.openclone import *
from src.openclone import __version__, __product__, __standard__
