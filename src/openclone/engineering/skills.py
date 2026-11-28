"""OpenClone Engineering Skill Registry.

Defines, indexes, and validates engineering skills across domains,
supporting intelligent skill selection for project planning.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain

logger = logging.getLogger("openclone.engineering.skills")


@dataclass
class EngineeringSkill:
    skill_id: str
    name: str
    domain: EngineeringDomain
    category: str
    description: str
    required_knowledge: List[str] = field(default_factory=list)
    related_technologies: List[str] = field(default_factory=list)
    related_roles: List[str] = field(default_factory=list)
    validation_criteria: List[str] = field(default_factory=list)
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "domain": self.domain.value,
            "category": self.category,
            "description": self.description,
            "related_technologies": self.related_technologies,
            "related_roles": self.related_roles,
            "version": self.version,
        }


class EngineeringSkillRegistry:
    """Master registry of engineering skills across the 23 domains."""

    _instance: Optional["EngineeringSkillRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.skills: Dict[str, EngineeringSkill] = {}
        self._populate_canonical_skills()
        self._initialized = True

    def _populate_canonical_skills(self) -> None:
        skills = [
            EngineeringSkill(
                skill_id="skill.frontend.responsive_design",
                name="Responsive Layout Engineering",
                domain=EngineeringDomain.DOMAIN_05_FRONTEND,
                category="Frontend UI",
                description="Engineering fluid grid layouts, CSS media queries, and touch-optimized interfaces",
                related_technologies=["CSS3", "Tailwind CSS", "React", "Vue"],
                related_roles=["frontend-engineer", "ui-designer"],
            ),
            EngineeringSkill(
                skill_id="skill.frontend.accessibility_wcag",
                name="WCAG 2.1 AA Accessibility Verification",
                domain=EngineeringDomain.DOMAIN_04_UX_UI,
                category="Accessibility",
                description="Ensuring screen reader support, keyboard navigation, and 4.5:1 color contrast ratios",
                related_technologies=["ARIA", "axe-core", "Pa11y"],
                related_roles=["accessibility-specialist", "frontend-engineer"],
            ),
            EngineeringSkill(
                skill_id="skill.backend.modular_monolith",
                name="Modular Monolith Service Decomposition",
                domain=EngineeringDomain.DOMAIN_06_BACKEND,
                category="Architecture",
                description="Structuring single-deployment backends with strict interface boundaries between modules",
                related_technologies=["Python", "Go", "Java", "TypeScript"],
                related_roles=["backend-engineer", "principal-architect"],
            ),
            EngineeringSkill(
                skill_id="skill.database.schema_migrations",
                name="Zero-Downtime Database Schema Evolution",
                domain=EngineeringDomain.DOMAIN_08_DATABASE,
                category="Database",
                description="Applying expand-and-contract parallel column additions and non-locking table updates",
                related_technologies=["PostgreSQL", "Alembic", "Prisma", "Flyway"],
                related_roles=["database-engineer", "backend-engineer"],
            ),
            EngineeringSkill(
                skill_id="skill.security.stride_threat_modeling",
                name="STRIDE Threat Vector Analysis",
                domain=EngineeringDomain.DOMAIN_12_SECURITY,
                category="Application Security",
                description="Decomposing software architectures against spoofing, tampering, repudiation, information disclosure, DoS, and elevation of privilege",
                related_technologies=["OWASP Top 10", "Semgrep", "Bandit"],
                related_roles=["security-engineer", "threat-modeler"],
            ),
            EngineeringSkill(
                skill_id="skill.system_design.capacity_modeling",
                name="Quantitative Capacity & Scale Modeling",
                domain=EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
                category="System Design",
                description="Calculating QPS, storage growth, network bandwidth, IOPS, and memory cache requirements",
                related_technologies=["CapacityEstimator", "Redis", "CDN"],
                related_roles=["solution-architect", "distributed-systems-engineer"],
            ),
            EngineeringSkill(
                skill_id="skill.ai.model_routing_and_budgeting",
                name="AI Model Routing and Context Budgeting",
                domain=EngineeringDomain.DOMAIN_11_AI,
                category="AI Engineering",
                description="Optimizing model selection, inference routing, prompt token budgets, and fallback tiers",
                related_technologies=["MIE", "OpenAI", "Anthropic", "Gemini", "Ollama"],
                related_roles=["ai-engineer", "prompt-engineer"],
            ),
        ]
        for s in skills:
            self.skills[s.skill_id] = s

    def register_skill(self, skill: EngineeringSkill) -> None:
        self.skills[skill.skill_id] = skill

    def get_skill(self, skill_id: str) -> Optional[EngineeringSkill]:
        return self.skills.get(skill_id)

    def list_skills(self, domain: Optional[EngineeringDomain] = None) -> List[EngineeringSkill]:
        if domain:
            return [s for s in self.skills.values() if s.domain == domain]
        return list(self.skills.values())
