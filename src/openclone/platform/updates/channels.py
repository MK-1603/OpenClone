"""Release channels definition and management."""
from __future__ import annotations

from enum import Enum
from typing import Set


class ReleaseChannel(str, Enum):
    """Supported distribution channels."""
    STABLE = "stable"
    BETA = "beta"
    NIGHTLY = "nightly"

    @classmethod
    def valid_channels(cls) -> Set[str]:
        """Return set of valid channel identifiers."""
        return {c.value for c in cls}

    @classmethod
    def normalize(cls, name: str) -> ReleaseChannel:
        """Normalize channel name with safe fallback to STABLE."""
        clean = (name or "").strip().lower()
        if clean == "beta":
            return cls.BETA
        elif clean == "nightly":
            return cls.NIGHTLY
        return cls.STABLE
