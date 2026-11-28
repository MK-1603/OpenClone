"""
OpenClone Engineering Intelligence System (EIS) Manager.
Façade coordinating Knowledge Graph, Capability Registry, and Problem-Solving Engine.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
from openclone.engineering.models import MasterSector, KnowledgeUnit, KnowledgeType, KnowledgeSourceRef, KnowledgeMaturity
from openclone.engineering.graph import KnowledgeGraphEngine
from openclone.engineering.capabilities import CapabilityRegistry, EngineeringCapability
from openclone.engineering.epse import EngineeringProblemSolvingEngine, ProblemCategory, ProblemSolvingPlan


class EngineeringIntelligenceSystem:
    """
    Unified entrypoint for the OpenClone Engineering Intelligence System.
    """

    def __init__(self):
        self.graph = KnowledgeGraphEngine()
        self.capabilities = CapabilityRegistry()
        self.epse = EngineeringProblemSolvingEngine(self.graph, self.capabilities)
        self._populate_core_knowledge_units()

    def _populate_core_knowledge_units(self):
        """Populate representative high-quality knowledge units across sectors."""
        units = [
            KnowledgeUnit(
                id="EIS-KNOW-001",
                title="Monolith-First Architectural Principle",
                sector_id=MasterSector.EIS_04,
                domain_id="SOFTWARE-ARCHITECTURE",
                subdomain_id="MODULAR-MONOLITHS",
                specialization_id="SYSTEM-DECOMPOSITION",
                knowledge_type=KnowledgeType.ENGINEERING_PRINCIPLE,
                description="Default to well-structured Modular Monolith unless organizational size or throughput dictates microservices.",
                purpose="Prevent premature microservice distributed complexity, network latency, and distributed transaction failures.",
                principles=["Single deployment unit", "Strict module boundaries via interfaces", "Zero direct cross-boundary DB queries"],
                tools=["python", "go", "java", "typescript"],
                standards=["ISO/IEC/IEEE 42010"],
                source_refs=[KnowledgeSourceRef(uri="framework/skills/backend-architecture/SKILL.md", source_type="architecture_standard")],
                maturity=KnowledgeMaturity.LEVEL_5_PRACTICALLY_TESTED
            ),
            KnowledgeUnit(
                id="EIS-KNOW-002",
                title="Expand-and-Contract Zero-Downtime Migration Pattern",
                sector_id=MasterSector.EIS_08,
                domain_id="DATABASE-ENGINEERING",
                subdomain_id="RELATIONAL-DATABASES",
                specialization_id="SCHEMA-EVOLUTION",
                knowledge_type=KnowledgeType.ARCHITECTURE_PATTERN,
                description="Perform schema changes via parallel run: add column, dual-write, backfill, migrate reads, contract old column.",
                purpose="Ensure 100% online database migrations without downtime or table lock starvation.",
                tools=["alembic", "prisma", "flyway", "postgresql"],
                patterns=["Parallel Run", "Dual-Write Phase"],
                source_refs=[KnowledgeSourceRef(uri="framework/skills/database-engineering/SKILL.md", source_type="database_standard")],
                maturity=KnowledgeMaturity.LEVEL_5_PRACTICALLY_TESTED
            ),
            KnowledgeUnit(
                id="EIS-KNOW-003",
                title="STRIDE Threat Modeling & Zero-Trust Defense",
                sector_id=MasterSector.EIS_11,
                domain_id="CYBERSECURITY-ENGINEERING",
                subdomain_id="APPLICATION-SECURITY",
                specialization_id="THREAT-MODELING",
                knowledge_type=KnowledgeType.ENGINEERING_PRINCIPLE,
                description="Decompose software architectures against Spoofing, Tampering, Repudiation, Information Disclosure, DoS, and Elevation of Privilege.",
                purpose="Eliminate structural vulnerabilities and enforce zero-trust authentication boundaries prior to implementation.",
                tools=["semgrep", "bandit", "trufflehog", "owasp-zap"],
                standards=["NIST SP 800-53", "OWASP Top 10"],
                source_refs=[KnowledgeSourceRef(uri="framework/skills/saas-security-baseline/SKILL.md", source_type="security_baseline")],
                maturity=KnowledgeMaturity.LEVEL_5_PRACTICALLY_TESTED
            ),
            KnowledgeUnit(
                id="EIS-KNOW-004",
                title="Deterministic Goldfish Verification Boundary",
                sector_id=MasterSector.EIS_12,
                domain_id="QUALITY-AND-VERIFICATION",
                subdomain_id="INDEPENDENT-AUDIT",
                specialization_id="VERIFICATION-GOVERNANCE",
                knowledge_type=KnowledgeType.ENGINEERING_PRINCIPLE,
                description="Independent Verifiers must operate with zero drafting conversation memory, evaluating only tangible disk evidence.",
                purpose="Prevent confirmation bias and ensure detached, objective quality gate evaluation.",
                tools=["pytest", "sqlite3", "hashlib"],
                standards=["OpenClone Rule 1 (No Speculative Success)"],
                source_refs=[KnowledgeSourceRef(uri="agents/independent-verifier-agent.md", source_type="agent_specification")],
                maturity=KnowledgeMaturity.LEVEL_5_PRACTICALLY_TESTED
            ),
        ]
        for u in units:
            self.graph.register_unit(u)

    def solve_problem(
        self,
        title: str,
        description: str,
        category: ProblemCategory
    ) -> ProblemSolvingPlan:
        return self.epse.solve_problem(title, description, category)
