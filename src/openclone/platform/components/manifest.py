"""Component manifest parser and permission boundary validator."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ComponentManifest:
    """Parsed and validated component manifest."""
    id: str
    name: str
    version: str
    publisher: str
    description: str
    category: str
    min_platform_version: str
    max_platform_version: Optional[str] = None
    entrypoint: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ComponentManifest:
        """Instantiate component manifest from dictionary with validation."""
        for req in ("id", "name", "version", "publisher", "description", "category", "min_platform_version"):
            if req not in data:
                raise ValueError(f"Invalid component manifest: missing '{req}'")

        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            publisher=data["publisher"],
            description=data["description"],
            category=data["category"],
            min_platform_version=data["min_platform_version"],
            max_platform_version=data.get("max_platform_version"),
            entrypoint=data.get("entrypoint"),
            permissions=data.get("permissions", []),
            dependencies=data.get("dependencies", []),
        )

    @classmethod
    def load_from_file(cls, path: Path) -> ComponentManifest:
        """Load and parse component.json file."""
        if not path.exists():
            raise FileNotFoundError(f"Component manifest not found at: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def validate_permissions(self) -> List[str]:
        """Validate requested permissions against known safe scopes."""
        allowed_prefixes = ("filesystem:read", "filesystem:write", "subprocess:", "network:")
        warnings: List[str] = []
        for perm in self.permissions:
            if not any(perm.startswith(prefix) for prefix in allowed_prefixes):
                warnings.append(f"Unrecognized permission request: '{perm}'")
        return warnings
