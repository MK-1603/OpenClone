"""OpenClone Universal Project Taxonomy Loader and Validator."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[3]
TAXONOMY_REGISTRY_PATH = ROOT / "framework" / "registries" / "project-taxonomy.json"


@dataclass
class ProjectTypeDefinition:
    id: str
    name: str
    description: str
    default_domains: List[str]
    mandatory_capabilities: List[str]
    conditional_capabilities: List[str] = field(default_factory=list)
    typical_delivery_targets: List[str] = field(default_factory=list)
    recommended_workforce: List[str] = field(default_factory=list)
    status: str = "SPECIFIED"


@dataclass
class ProjectFamilyDefinition:
    id: str
    name: str
    description: str
    types: Dict[str, ProjectTypeDefinition] = field(default_factory=dict)


class TaxonomyRegistry:
    """Singleton loader and accessor for the canonical OpenClone Project Taxonomy."""

    def __init__(self, registry_path: Optional[Path] = None):
        self.path = registry_path or TAXONOMY_REGISTRY_PATH
        self.version = "1.0.0"
        self.updated_at = ""
        self.complexity_levels: List[str] = []
        self.delivery_targets: List[str] = []
        self.maturity_levels: List[str] = []
        self.families: Dict[str, ProjectFamilyDefinition] = {}
        self._type_to_family: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.version = data.get("version", "1.0.0")
        self.updated_at = data.get("updated_at", "")
        self.complexity_levels = data.get("complexity_levels", [])
        self.delivery_targets = data.get("delivery_targets", [])
        self.maturity_levels = data.get("maturity_levels", [])

        for fam_data in data.get("families", []):
            fam_id = fam_data["id"]
            fam = ProjectFamilyDefinition(
                id=fam_id,
                name=fam_data["name"],
                description=fam_data["description"],
            )
            for t_data in fam_data.get("types", []):
                t_id = t_data["id"]
                pt = ProjectTypeDefinition(
                    id=t_id,
                    name=t_data["name"],
                    description=t_data["description"],
                    default_domains=t_data.get("default_domains", []),
                    mandatory_capabilities=t_data.get("mandatory_capabilities", []),
                    conditional_capabilities=t_data.get("conditional_capabilities", []),
                    typical_delivery_targets=t_data.get("typical_delivery_targets", []),
                    recommended_workforce=t_data.get("recommended_workforce", []),
                    status=t_data.get("status", "SPECIFIED"),
                )
                fam.types[t_id] = pt
                self._type_to_family[t_id] = fam_id
            self.families[fam_id] = fam

    def get_family(self, family_id: str) -> Optional[ProjectFamilyDefinition]:
        return self.families.get(family_id)

    def get_type(self, type_id: str) -> Optional[ProjectTypeDefinition]:
        fam_id = self._type_to_family.get(type_id)
        if fam_id and fam_id in self.families:
            return self.families[fam_id].types.get(type_id)
        # Search all families
        for fam in self.families.values():
            if type_id in fam.types:
                return fam.types[type_id]
        return None

    def get_family_for_type(self, type_id: str) -> Optional[str]:
        return self._type_to_family.get(type_id)

    def list_families(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "type_count": len(f.types),
            }
            for f in self.families.values()
        ]

    def list_types(self, family_id: Optional[str] = None) -> List[Dict[str, Any]]:
        res = []
        target_fams = [self.families[family_id]] if family_id and family_id in self.families else self.families.values()
        for fam in target_fams:
            for pt in fam.types.values():
                res.append({
                    "id": pt.id,
                    "family_id": fam.id,
                    "name": pt.name,
                    "description": pt.description,
                    "status": pt.status,
                    "delivery_targets": pt.typical_delivery_targets,
                })
        return res
