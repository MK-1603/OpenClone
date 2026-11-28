"""Release manifest parser, validator, and cryptographic verifier."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ReleaseArtifact:
    """Declared release distribution file metadata."""
    filename: str
    os: str
    arch: str
    distribution_type: str
    sha256: str
    size_bytes: int
    url: str


@dataclass
class ReleaseManifest:
    """Parsed and validated release manifest."""
    product: str
    version: str
    channel: str
    published_at: str
    min_python_version: str
    artifacts: List[ReleaseArtifact]
    release_notes_url: Optional[str] = None
    required_migrations: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ReleaseManifest:
        """Instantiate ReleaseManifest from dictionary with validation."""
        for required_key in ("product", "version", "channel", "published_at", "artifacts"):
            if required_key not in data:
                raise ValueError(f"Malformed release manifest: missing required key '{required_key}'")

        artifacts = [
            ReleaseArtifact(
                filename=a["filename"],
                os=a.get("os", "any"),
                arch=a.get("arch", "any"),
                distribution_type=a.get("distribution_type", "wheel"),
                sha256=a["sha256"].lower(),
                size_bytes=int(a["size_bytes"]),
                url=a["url"],
            )
            for a in data["artifacts"]
        ]

        return cls(
            product=data["product"],
            version=data["version"],
            channel=data["channel"],
            published_at=data["published_at"],
            min_python_version=data.get("min_python_version", "3.10.0"),
            artifacts=artifacts,
            release_notes_url=data.get("release_notes_url"),
            required_migrations=data.get("required_migrations", []),
        )

    def find_artifact_for_system(self, target_os: str, target_arch: str, target_dist: Optional[str] = None) -> Optional[ReleaseArtifact]:
        """Find best matching artifact for target platform."""
        for a in self.artifacts:
            os_match = a.os in ("any", target_os.lower())
            arch_match = a.arch in ("any", target_arch.lower(), "universal")
            dist_match = (target_dist is None) or (a.distribution_type == target_dist)
            if os_match and arch_match and dist_match:
                return a
        return None


def verify_file_sha256(file_path: Path, expected_sha256: str) -> bool:
    """Verify SHA-256 hash of a local file matches expected checksum."""
    if not file_path.exists():
        return False
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower() == expected_sha256.lower()
