"""OpenClone Master Engineering Role Registry.

Indexes, validates, and discovers workforce roles across all 23 Engineering Domains,
binding seamlessly to the 73 workforce worker contracts.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain
from src.openclone.runtime.workforce import load_workers

logger = logging.getLogger("openclone.engineering.roles")


@dataclass
class EngineeringRole:
    role_id: str
    name: str
    domain: EngineeringDomain
    division: str
    tier: int = 1
    responsibilities: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    optional_skills: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)
    related_agents: List[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role_id": self.role_id,
            "name": self.name,
            "domain": self.domain.value,
            "division": self.division,
            "tier": self.tier,
            "responsibilities": self.responsibilities,
            "required_skills": self.required_skills,
            "technologies": self.technologies,
            "tools": self.tools,
            "expected_outputs": self.expected_outputs,
            "description": self.description,
        }


class EngineeringRoleRegistry:
    """Central registry of all 73 workforce roles mapped to the 23 Engineering Domains."""

    _instance: Optional["EngineeringRoleRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.roles: Dict[str, EngineeringRole] = {}
        self._load_from_workforce()
        self._initialized = True

    def _map_division_to_domain(self, division: str, role_id: str) -> EngineeringDomain:
        d = division.lower()
        r = role_id.lower()
        if "security" in d or "appsec" in r or "threat" in r:
            return EngineeringDomain.DOMAIN_12_SECURITY
        elif "quality" in d or "test" in r or "verifier" in r:
            return EngineeringDomain.DOMAIN_16_QUALITY
        elif "product" in d or "requirements" in r:
            return EngineeringDomain.DOMAIN_01_PRODUCT if "product" in r else EngineeringDomain.DOMAIN_02_REQUIREMENTS
        elif "ux" in d or "design" in d:
            return EngineeringDomain.DOMAIN_04_UX_UI
        elif "frontend" in d or "react" in r or "vue" in r:
            return EngineeringDomain.DOMAIN_05_FRONTEND
        elif "backend" in d or "api" in r:
            return EngineeringDomain.DOMAIN_06_BACKEND
        elif "data" in d or "database" in d or "dba" in r:
            return EngineeringDomain.DOMAIN_08_DATABASE
        elif "architecture" in d:
            return EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE
        elif "ai" in d or "ml" in d or "agent" in r or "prompt" in r:
            return EngineeringDomain.DOMAIN_11_AI
        elif "mobile" in d or "flutter" in r or "android" in r:
            return EngineeringDomain.DOMAIN_13_MOBILE
        elif "desktop" in d or "electron" in r or "tauri" in r:
            return EngineeringDomain.DOMAIN_14_DESKTOP
        elif "devops" in d or "platform" in d or "release" in r or "cloud" in r:
            return EngineeringDomain.DOMAIN_15_INFRASTRUCTURE
        elif "sre" in r or "reliability" in r:
            return EngineeringDomain.DOMAIN_17_RELIABILITY
        elif "reverse" in r or "evolution" in r:
            return EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING
        return EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY

    def _load_from_workforce(self) -> None:
        """Load and map workers from the runtime workforce registry."""
        raw_workers = load_workers()
        for role_id, details in raw_workers.items():
            division = details.get("division", "specialized")
            domain = self._map_division_to_domain(division, role_id)
            name = role_id.replace("-", " ").title()
            role = EngineeringRole(
                role_id=role_id,
                name=name,
                domain=domain,
                division=division,
                tier=details.get("tier", 1),
                responsibilities=details.get("responsibilities", []),
                required_skills=details.get("capabilities", []),
                technologies=details.get("tools", []),
                tools=details.get("tools", []),
                expected_outputs=details.get("outputs", []),
                description=details.get("description", f"Specialist worker role {name}"),
            )
            self.roles[role_id] = role

    def get_role(self, role_id: str) -> Optional[EngineeringRole]:
        return self.roles.get(role_id)

    def list_roles(self, domain: Optional[EngineeringDomain] = None) -> List[EngineeringRole]:
        if domain:
            return [r for r in self.roles.values() if r.domain == domain]
        return list(self.roles.values())

    def match_role_for_task(self, task_description: str) -> str:
        """Select best matching workforce worker for an engineering task."""
        t = task_description.lower()
        if any(k in t for k in ["threat", "security", "vulnerability", "authn", "authz", "jwt", "owasp"]):
            return "security-engineer"
        elif any(k in t for k in ["test", "verification", "pytest", "spec", "assert", "coverage"]):
            return "automation-test-engineer"
        elif any(k in t for k in ["database", "migration", "schema", "sql", "postgres", "sqlite", "table"]):
            return "database-engineer"
        elif any(k in t for k in ["ui", "frontend", "css", "component", "react", "html", "tailwind"]):
            return "frontend-engineer"
        elif any(k in t for k in ["api", "route", "endpoint", "backend", "controller", "fastapi"]):
            return "backend-engineer"
        elif any(k in t for k in ["architecture", "adr", "c4", "system design", "capacity"]):
            return "principal-architect"
        elif any(k in t for k in ["docker", "deploy", "kubernetes", "ci/cd", "infra"]):
            return "devops-engineer"
        return "principal-architect"
