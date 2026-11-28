"""
OpenClone Engineering Knowledge Graph Engine.
Maintains relational entity mappings, cross-sector relationships, and prerequisite resolution.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any, Set, Tuple
from openclone.engineering.models import KnowledgeUnit, MasterSector
from src.openclone.engineering.taxonomy import EngineeringDomain, EngineeringDomainRegistry
from src.openclone.engineering.roles import EngineeringRoleRegistry, EngineeringRole
from src.openclone.engineering.skills import EngineeringSkillRegistry, EngineeringSkill
from src.openclone.engineering.technologies import TechnologyCatalogRegistry, TechnologyItem


class KnowledgeGraphEngine:
    """
    In-memory and relational graph representation of engineering entities.
    Tracks relationships:
    - requires (prerequisites)
    - uses (tools)
    - implements (patterns)
    - governed_by (standards)
    - depends_on (other knowledge units)
    """

    def __init__(self):
        self._units: Dict[str, KnowledgeUnit] = {}
        self._sector_index: Dict[str, Set[str]] = {s.value: set() for s in MasterSector}
        self._tool_index: Dict[str, Set[str]] = {}
        self._pattern_index: Dict[str, Set[str]] = {}
        self._standard_index: Dict[str, Set[str]] = {}

    def register_unit(self, unit: KnowledgeUnit) -> None:
        self._units[unit.id] = unit
        self._sector_index[unit.sector_id.value].add(unit.id)

        for tool in unit.tools:
            self._tool_index.setdefault(tool.lower(), set()).add(unit.id)
        for pat in unit.patterns:
            self._pattern_index.setdefault(pat.lower(), set()).add(unit.id)
        for std in unit.standards:
            self._standard_index.setdefault(std.lower(), set()).add(unit.id)

    def get_unit(self, unit_id: str) -> Optional[KnowledgeUnit]:
        return self._units.get(unit_id)

    def get_units_by_sector(self, sector_id: str | MasterSector) -> List[KnowledgeUnit]:
        sec_val = sector_id.value if isinstance(sector_id, MasterSector) else sector_id
        unit_ids = self._sector_index.get(sec_val, set())
        return [self._units[uid] for uid in unit_ids]

    def resolve_prerequisites(self, unit_id: str) -> List[KnowledgeUnit]:
        """Traverse the prerequisite tree recursively detecting cycles."""
        visited: Set[str] = set()
        order: List[KnowledgeUnit] = []

        def dfs(curr_id: str):
            if curr_id in visited or curr_id not in self._units:
                return
            visited.add(curr_id)
            unit = self._units[curr_id]
            for prereq_id in unit.prerequisites:
                dfs(prereq_id)
            order.append(unit)

        dfs(unit_id)
        return order

    def search_knowledge(self, query: str, sector_filter: Optional[str] = None, limit: int = 10) -> List[KnowledgeUnit]:
        terms = [t.lower() for t in query.split() if t]
        scored: List[Tuple[float, KnowledgeUnit]] = []

        for unit in self._units.values():
            if sector_filter and unit.sector_id.value != sector_filter:
                continue

            haystack = f"{unit.title} {unit.description} {unit.purpose} {' '.join(unit.concepts)} {' '.join(unit.tools)}".lower()
            matches = sum(1 for term in terms if term in haystack)
            if matches > 0:
                score = matches / len(terms) if terms else 1.0
                scored.append((score, unit))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [u for _, u in scored[:limit]]

    def find_by_tool(self, tool_name: str) -> List[KnowledgeUnit]:
        unit_ids = self._tool_index.get(tool_name.lower(), set())
        return [self._units[uid] for uid in unit_ids]

    def find_by_standard(self, standard_id: str) -> List[KnowledgeUnit]:
        unit_ids = self._standard_index.get(standard_id.lower(), set())
        return [self._units[uid] for uid in unit_ids]

    def traverse_domain_relationships(self, domain: EngineeringDomain) -> Dict[str, Any]:
        """Traverse 8-level relationship hierarchy for a specific engineering domain.
        Domain -> Role -> Skill -> Technology -> Capability.
        """
        role_reg = EngineeringRoleRegistry()
        skill_reg = EngineeringSkillRegistry()
        tech_reg = TechnologyCatalogRegistry()

        roles = role_reg.list_roles(domain)
        skills = skill_reg.list_skills(domain)
        techs = [t for t in tech_reg.list_technologies() if t.domain == domain]

        return {
            "domain": domain.value,
            "roles": [r.to_dict() for r in roles],
            "skills": [s.to_dict() for s in skills],
            "technologies": [t.to_dict() for t in techs],
            "knowledge_units": [u.to_dict() for u in self._units.values() if u.domain_id.lower() in domain.value.lower()],
        }

    def recommend_engineering_package(self, project_type: str) -> Dict[str, Any]:
        """Synthesize tailored engineering package based on project archetype."""
        dom_reg = EngineeringDomainRegistry()
        role_reg = EngineeringRoleRegistry()
        tech_reg = TechnologyCatalogRegistry()

        active_domains = dom_reg.resolve_domains_for_project_type(project_type)
        recommended_roles: List[str] = ["principal-architect"]
        recommended_techs: List[str] = []

        for dom in active_domains:
            for r in role_reg.list_roles(dom):
                if r.role_id not in recommended_roles:
                    recommended_roles.append(r.role_id)
            for t in tech_reg.list_technologies():
                if t.domain == dom and t.name not in recommended_techs:
                    recommended_techs.append(t.name)

        return {
            "project_type": project_type,
            "active_domains": [d.value for d in active_domains],
            "active_domain_count": len(active_domains),
            "recommended_roles": recommended_roles[:12],  # Primary core team
            "recommended_technologies": recommended_techs,
            "primary_architect": "principal-architect",
        }
