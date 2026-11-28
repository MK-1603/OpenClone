"""OpenClone Dynamic Engineering Domain Activation Engine.

Analyzes project prompts, requirements, technology constraints, and classifications
to dynamically select and activate relevant engineering domains, subdomains, and disciplines.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain, EngineeringDomainRegistry
from src.openclone.engineering.disciplines import EngineeringDisciplineRegistry, DisciplineDescriptor


class ActivationLevel(str, enum.Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    CONDITIONAL = "CONDITIONAL"
    OPTIONAL = "OPTIONAL"
    INACTIVE = "INACTIVE"


@dataclass
class DomainActivationRecord:
    domain: EngineeringDomain
    level: ActivationLevel
    reason: str
    confidence: float
    active_disciplines: List[str] = field(default_factory=list)
    prerequisite_domains: List[EngineeringDomain] = field(default_factory=list)


@dataclass
class ProjectActivationReport:
    project_name: str
    primary_domains: List[EngineeringDomain]
    secondary_domains: List[EngineeringDomain]
    conditional_domains: List[EngineeringDomain]
    inactive_domains: List[EngineeringDomain]
    records: Dict[EngineeringDomain, DomainActivationRecord]
    activated_disciplines: List[str]


class DynamicDomainActivationEngine:
    """Dynamically activates engineering disciplines based on project context."""

    def __init__(self):
        self.domain_reg = EngineeringDomainRegistry()
        self.disc_reg = EngineeringDisciplineRegistry()

    def activate_domains_for_project(
        self,
        prompt: str,
        project_name: str = "TargetProject",
        project_type: Optional[str] = None,
        constraints: Optional[List[str]] = None,
    ) -> ProjectActivationReport:
        p_lower = prompt.lower()
        records: Dict[EngineeringDomain, DomainActivationRecord] = {}

        # Default foundational domains active for all software engineering projects
        records[EngineeringDomain.DOMAIN_01_PRODUCT] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_01_PRODUCT,
            level=ActivationLevel.PRIMARY,
            reason="Core product vision, features, and user personas.",
            confidence=1.0,
        )
        records[EngineeringDomain.DOMAIN_02_REQUIREMENTS] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_02_REQUIREMENTS,
            level=ActivationLevel.PRIMARY,
            reason="Core requirements elicitation, user stories, and acceptance criteria.",
            confidence=1.0,
        )
        records[EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
            level=ActivationLevel.PRIMARY,
            reason="Essential architecture style, component boundaries, and structural patterns.",
            confidence=1.0,
        )
        records[EngineeringDomain.DOMAIN_16_QUALITY] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_16_QUALITY,
            level=ActivationLevel.SECONDARY,
            reason="Testing strategy, quality pyramid, and verification.",
            confidence=0.9,
        )

        # Frontend / Web / UX
        if any(k in p_lower for k in ["ui", "frontend", "web", "react", "vue", "dashboard", "portal", "css", "screen", "mobile", "ios", "android"]):
            records[EngineeringDomain.DOMAIN_04_UX_UI] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_04_UX_UI,
                level=ActivationLevel.PRIMARY,
                reason="UI design system, accessibility, and user experience.",
                confidence=0.95,
            )
            records[EngineeringDomain.DOMAIN_05_FRONTEND] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_05_FRONTEND,
                level=ActivationLevel.PRIMARY,
                reason="Client-side architecture, state management, and web components.",
                confidence=0.95,
            )

        # Mobile
        if any(k in p_lower for k in ["mobile", "ios", "android", "flutter", "react native", "phone", "tablet"]):
            records[EngineeringDomain.DOMAIN_13_MOBILE] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_13_MOBILE,
                level=ActivationLevel.PRIMARY,
                reason="Mobile application architecture, native OS lifecycle, and offline storage.",
                confidence=0.98,
            )

        # Backend & API
        if any(k in p_lower for k in ["backend", "api", "service", "server", "microservice", "rest", "graphql", "database", "saas", "platform"]):
            records[EngineeringDomain.DOMAIN_06_BACKEND] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_06_BACKEND,
                level=ActivationLevel.PRIMARY,
                reason="Server-side service architecture, business logic isolation, and worker queues.",
                confidence=0.95,
            )
            records[EngineeringDomain.DOMAIN_07_API] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_07_API,
                level=ActivationLevel.PRIMARY,
                reason="API contracts, OpenAPI formalization, and rate limiting.",
                confidence=0.95,
            )
            records[EngineeringDomain.DOMAIN_08_DATABASE] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_08_DATABASE,
                level=ActivationLevel.PRIMARY,
                reason="Data persistence, schema design, and ACID transaction boundaries.",
                confidence=0.95,
            )
            records[EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
                level=ActivationLevel.PRIMARY,
                reason="C4 diagrams, high availability, and scaling topologies.",
                confidence=0.9,
            )

        # AI / LLM / Multi-Agent
        if any(k in p_lower for k in ["ai", "llm", "agent", "rag", "embedding", "gpt", "model", "swarm", "vector"]):
            records[EngineeringDomain.DOMAIN_11_AI] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_11_AI,
                level=ActivationLevel.PRIMARY,
                reason="Foundation model selection, RAG pipelines, prompt engineering, and agent governance.",
                confidence=0.98,
            )
            records[EngineeringDomain.DOMAIN_08_DATABASE] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_08_DATABASE,
                level=ActivationLevel.PRIMARY,
                reason="Vector database embedding storage and retrieval.",
                confidence=0.95,
            )

        # Security & Governance
        if any(k in p_lower for k in ["auth", "security", "token", "payment", "stripe", "fintech", "hipaa", "soc2", "privacy", "gdpr", "pci"]):
            records[EngineeringDomain.DOMAIN_12_SECURITY] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_12_SECURITY,
                level=ActivationLevel.PRIMARY,
                reason="STRIDE threat modeling, least privilege, zero trust, and cryptographic controls.",
                confidence=0.98,
            )
            records[EngineeringDomain.DOMAIN_23_GOVERNANCE] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_23_GOVERNANCE,
                level=ActivationLevel.PRIMARY,
                reason="Regulatory compliance, audit ledger hashing, and policy validation.",
                confidence=0.95,
            )
        else:
            records[EngineeringDomain.DOMAIN_12_SECURITY] = DomainActivationRecord(
                domain=EngineeringDomain.DOMAIN_12_SECURITY,
                level=ActivationLevel.SECONDARY,
                reason="Baseline security hygiene and OWASP Top 10 hardening.",
                confidence=0.8,
            )

        # Infrastructure / DevOps / SRE
        records[EngineeringDomain.DOMAIN_15_INFRASTRUCTURE] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
            level=ActivationLevel.SECONDARY,
            reason="Containerization, CI/CD pipelines, and cloud environment specification.",
            confidence=0.85,
        )
        records[EngineeringDomain.DOMAIN_17_RELIABILITY] = DomainActivationRecord(
            domain=EngineeringDomain.DOMAIN_17_RELIABILITY,
            level=ActivationLevel.SECONDARY,
            reason="Observability, metrics, logs, and SLO formulation.",
            confidence=0.85,
        )

        # Mark remaining canonical domains as INACTIVE or CONDITIONAL
        for dom in EngineeringDomain:
            if dom not in records:
                records[dom] = DomainActivationRecord(
                    domain=dom,
                    level=ActivationLevel.INACTIVE,
                    reason="Not indicated by initial project requirements or architectural drivers.",
                    confidence=0.9,
                )

        # Collate disciplines for active domains
        active_disciplines: List[str] = []
        for dom, rec in records.items():
            if rec.level in (ActivationLevel.PRIMARY, ActivationLevel.SECONDARY):
                discs = self.disc_reg.list_disciplines(dom)
                rec.active_disciplines = [d.discipline_id for d in discs]
                active_disciplines.extend(rec.active_disciplines)

        primaries = [d for d, r in records.items() if r.level == ActivationLevel.PRIMARY]
        secondaries = [d for d, r in records.items() if r.level == ActivationLevel.SECONDARY]
        conditionals = [d for d, r in records.items() if r.level == ActivationLevel.CONDITIONAL]
        inactives = [d for d, r in records.items() if r.level == ActivationLevel.INACTIVE]

        return ProjectActivationReport(
            project_name=project_name,
            primary_domains=primaries,
            secondary_domains=secondaries,
            conditional_domains=conditionals,
            inactive_domains=inactives,
            records=records,
            activated_disciplines=active_disciplines,
        )
