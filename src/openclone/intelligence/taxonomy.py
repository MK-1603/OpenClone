"""OpenClone Universal Project Taxonomy Loader and Validator."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[3]
TAXONOMY_REGISTRY_PATH = ROOT / "framework" / "registries" / "project-taxonomy.json"


@dataclass
class CategoryDefinition:
    id: str  # e.g. ENG-01
    code: str  # e.g. ai_engineering
    name: str  # e.g. Artificial Intelligence
    description: str
    subdisciplines: List[str] = field(default_factory=list)
    default_domains: List[str] = field(default_factory=list)
    mandatory_capabilities: List[str] = field(default_factory=list)
    recommended_workforce: List[str] = field(default_factory=list)


@dataclass
class ArchetypeDefinition:
    id: str
    name: str
    category: str
    family: str


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
        self.version = "2.0.0"
        self.updated_at = ""
        self.complexity_levels: List[str] = []
        self.delivery_targets: List[str] = []
        self.maturity_levels: List[str] = []
        self.deployment_models: List[str] = []
        self.ai_dependencies: List[str] = []
        self.data_sensitivity_levels: List[str] = []
        self.reliability_tiers: List[str] = []
        self.families: Dict[str, ProjectFamilyDefinition] = {}
        self.categories: Dict[str, CategoryDefinition] = {}
        self.archetypes: Dict[str, ArchetypeDefinition] = {}
        self._type_to_family: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.version = data.get("version", "2.0.0")
        self.updated_at = data.get("updated_at", "")
        self.complexity_levels = data.get("complexity_levels", [])
        self.delivery_targets = data.get("delivery_targets", [])
        self.maturity_levels = data.get("maturity_levels", [])
        self.deployment_models = data.get("deployment_models", ["local", "cloud", "hybrid", "on_premises", "edge"])
        self.ai_dependencies = data.get("ai_dependencies", ["none", "optional", "required"])
        self.data_sensitivity_levels = data.get("data_sensitivity_levels", ["public", "internal", "confidential", "restricted"])
        self.reliability_tiers = data.get("reliability_tiers", ["standard_99_0", "high_99_9", "mission_critical_99_99"])

        # Load 14 primary engineering categories
        for cat_data in data.get("engineering_categories", []):
            cat = CategoryDefinition(
                id=cat_data["id"],
                code=cat_data["code"],
                name=cat_data["name"],
                description=cat_data["description"],
                subdisciplines=cat_data.get("subdisciplines", []),
                default_domains=cat_data.get("default_domains", []),
                mandatory_capabilities=cat_data.get("mandatory_capabilities", []),
                recommended_workforce=cat_data.get("recommended_workforce", []),
            )
            self.categories[cat.id] = cat
            self.categories[cat.code] = cat

        # Load archetypes
        for arch_data in data.get("archetypes", []):
            arch = ArchetypeDefinition(
                id=arch_data["id"],
                name=arch_data["name"],
                category=arch_data["category"],
                family=arch_data["family"],
            )
            self.archetypes[arch.id] = arch

        # Load families and types (canonical 12 families)
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

    def get_category(self, cat_id_or_code: str) -> Optional[CategoryDefinition]:
        return self.categories.get(cat_id_or_code)

    def list_categories(self) -> List[Dict[str, Any]]:
        # Return unique by id (ENG-01 .. ENG-14)
        seen = set()
        res = []
        for cat in self.categories.values():
            if cat.id not in seen:
                seen.add(cat.id)
                res.append({
                    "id": cat.id,
                    "code": cat.code,
                    "name": cat.name,
                    "description": cat.description,
                    "subdisciplines_count": len(cat.subdisciplines),
                    "default_domains": cat.default_domains,
                })
        return sorted(res, key=lambda x: x["id"])

    def get_archetype(self, archetype_id: str) -> Optional[ArchetypeDefinition]:
        return self.archetypes.get(archetype_id)

    def list_archetypes(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": a.id,
                "name": a.name,
                "category": a.category,
                "family": a.family,
            }
            for a in self.archetypes.values()
        ]

    def get_family(self, family_id: str) -> Optional[ProjectFamilyDefinition]:
        return self.families.get(family_id)

    def get_type(self, type_id: str) -> Optional[ProjectTypeDefinition]:
        fam_id = self._type_to_family.get(type_id)
        if fam_id and fam_id in self.families:
            return self.families[fam_id].types.get(type_id)
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
