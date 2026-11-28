"""OpenClone Technology Catalog & Intelligence Registry.

Maintains multi-criteria evaluation matrices, compatibility rules,
and trade-off models across programming languages, frameworks, databases, and runtimes.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain

logger = logging.getLogger("openclone.engineering.technologies")


class TechnologyCategory(str, Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    AI_MODEL_TOOL = "ai_model_tool"
    TESTING_TOOL = "testing_tool"


@dataclass
class TechnologyItem:
    tech_id: str
    name: str
    category: TechnologyCategory
    domain: EngineeringDomain
    maturity_tier: str = "PRODUCTION_STABLE"
    strengths: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    recommended_for: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    license: str = "MIT"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tech_id": self.tech_id,
            "name": self.name,
            "category": self.category.value,
            "domain": self.domain.value,
            "maturity_tier": self.maturity_tier,
            "strengths": self.strengths,
            "limitations": self.limitations,
            "recommended_for": self.recommended_for,
            "alternatives": self.alternatives,
            "license": self.license,
        }


class TechnologyCatalogRegistry:
    """Master technology intelligence catalog."""

    _instance: Optional["TechnologyCatalogRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.technologies: Dict[str, TechnologyItem] = {}
        self._populate_canonical_technologies()
        self._initialized = True

    def _populate_canonical_technologies(self) -> None:
        items = [
            TechnologyItem(
                tech_id="tech.lang.python",
                name="Python",
                category=TechnologyCategory.LANGUAGE,
                domain=EngineeringDomain.DOMAIN_06_BACKEND,
                strengths=["Rapid development", "Massive AI/ML ecosystem", "Clear readable syntax"],
                limitations=["GIL concurrency limits", "Interpreted CPU performance"],
                recommended_for=["AI/ML systems", "Backend APIs", "Data engineering", "Automation"],
                alternatives=["Go", "Rust", "TypeScript"],
            ),
            TechnologyItem(
                tech_id="tech.lang.typescript",
                name="TypeScript",
                category=TechnologyCategory.LANGUAGE,
                domain=EngineeringDomain.DOMAIN_05_FRONTEND,
                strengths=["Static type safety", "Universal browser/Node runtime", "Extensive npm registry"],
                limitations=["Complex type configurations", "Build transpilation step"],
                recommended_for=["Modern web apps", "Full-stack Node services", "Design systems"],
                alternatives=["JavaScript", "Dart", "Rust"],
            ),
            TechnologyItem(
                tech_id="tech.framework.fastapi",
                name="FastAPI",
                category=TechnologyCategory.FRAMEWORK,
                domain=EngineeringDomain.DOMAIN_07_API,
                strengths=["Native async ASGI throughput", "Automatic OpenAPI/Swagger generation", "Pydantic validation"],
                limitations=["Async DB ORM learning curve"],
                recommended_for=["High-performance REST APIs", "AI microservices"],
                alternatives=["Flask", "Django Ninja", "Go Gin"],
            ),
            TechnologyItem(
                tech_id="tech.framework.react",
                name="React",
                category=TechnologyCategory.FRAMEWORK,
                domain=EngineeringDomain.DOMAIN_05_FRONTEND,
                strengths=["Massive ecosystem", "Component reusability", "Next.js SSR support"],
                limitations=["Client bundle size if unoptimized", "State management fragmentation"],
                recommended_for=["Interactive web dashboards", "Enterprise SaaS UIs"],
                alternatives=["Vue.js", "Svelte", "Angular"],
            ),
            TechnologyItem(
                tech_id="tech.db.postgresql",
                name="PostgreSQL",
                category=TechnologyCategory.DATABASE,
                domain=EngineeringDomain.DOMAIN_08_DATABASE,
                strengths=["ACID transactions", "Row-Level Security (RLS)", "Rich JSONB and Vector extensions"],
                limitations=["Vertical write scaling limits beyond 20k writes/sec"],
                recommended_for=["Primary transactional data", "Multi-tenant SaaS", "Relational models"],
                alternatives=["MySQL", "CockroachDB", "SQLite"],
            ),
            TechnologyItem(
                tech_id="tech.db.sqlite",
                name="SQLite",
                category=TechnologyCategory.DATABASE,
                domain=EngineeringDomain.DOMAIN_08_DATABASE,
                strengths=["Zero configuration", "Embedded local execution", "Rock-solid reliability"],
                limitations=["Single writer lock concurrency limit"],
                recommended_for=["Local control-plane", "Desktop apps", "Audit ledgers", "Mobile offline cache"],
                alternatives=["PostgreSQL", "DuckDB", "Turso"],
            ),
            TechnologyItem(
                tech_id="tech.infra.docker",
                name="Docker",
                category=TechnologyCategory.INFRASTRUCTURE,
                domain=EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
                strengths=["Reproducible runtime environments", "Standardized container packaging"],
                limitations=["Container image size overhead"],
                recommended_for=["Service isolation", "CI/CD builds", "Deployment artifacts"],
                alternatives=["Podman", "Containerd"],
            ),
        ]
        for item in items:
            self.technologies[item.tech_id] = item

    def get_technology(self, tech_id: str) -> Optional[TechnologyItem]:
        return self.technologies.get(tech_id)

    def list_technologies(self, category: Optional[TechnologyCategory] = None) -> List[TechnologyItem]:
        if category:
            return [t for t in self.technologies.values() if t.category == category]
        return list(self.technologies.values())
