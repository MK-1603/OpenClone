"""
OpenClone Engineering Capability Model & Agent Mapping Engine.
Enforces clear distinction between Role, Competency, Skill, Tool, Capability, and Agent.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set
from openclone.engineering.models import MasterSector


@dataclass
class EngineeringCapability:
    """
    Formal specification of an executable engineering capability.
    """
    id: str
    name: str
    purpose: str
    sector_id: MasterSector
    required_knowledge: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    input_contract: Dict[str, Any] = field(default_factory=dict)
    output_contract: Dict[str, Any] = field(default_factory=dict)
    risk_level: str = "medium"  # low, medium, high, critical
    validation_criteria: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "purpose": self.purpose,
            "sector_id": self.sector_id.value if isinstance(self.sector_id, MasterSector) else self.sector_id,
            "required_knowledge": self.required_knowledge,
            "required_skills": self.required_skills,
            "required_tools": self.required_tools,
            "risk_level": self.risk_level,
            "validation_criteria": self.validation_criteria,
        }


class CapabilityRegistry:
    """
    Manages registered capabilities and matches them to executing roles and agents.
    """

    def __init__(self):
        self._capabilities: Dict[str, EngineeringCapability] = {}
        self._agent_capability_map: Dict[str, Set[str]] = {}
        self._role_capability_map: Dict[str, Set[str]] = {}
        self._init_core_capabilities()

    def _init_core_capabilities(self):
        # Sample canonical capabilities across sectors
        core = [
            EngineeringCapability(
                id="CAP-REQ-001",
                name="Requirements Extraction & BDD Formulation",
                purpose="Extract unambiguous Given-When-Then acceptance criteria from product vision.",
                sector_id=MasterSector.EIS_01,
                required_skills=["requirements-engineering", "product-discovery"],
                required_tools=["markdown", "json-schema"],
            ),
            EngineeringCapability(
                id="CAP-ARCH-001",
                name="System Boundary & C4 Diagram Formulation",
                purpose="Design C4 Container and Component models adhering to Monolith-First rule.",
                sector_id=MasterSector.EIS_04,
                required_skills=["system-design-engineering", "backend-architecture"],
                required_tools=["mermaid", "adr"],
            ),
            EngineeringCapability(
                id="CAP-DEV-001",
                name="Type-Safe API & Domain Service Implementation",
                purpose="Build input-validated REST/gRPC endpoints with structured error handling.",
                sector_id=MasterSector.EIS_03,
                required_skills=["api-engineering", "backend-architecture"],
                required_tools=["python", "fastapi", "pydantic", "go"],
            ),
            EngineeringCapability(
                id="CAP-DB-001",
                name="ACID Relational Modeling & Zero-Downtime Migration",
                purpose="Design 3NF schemas with foreign key indexes and expand-and-contract migrations.",
                sector_id=MasterSector.EIS_08,
                required_skills=["database-engineering", "multi-tenant-engineering"],
                required_tools=["postgresql", "sqlite", "alembic"],
            ),
            EngineeringCapability(
                id="CAP-SEC-001",
                name="STRIDE Threat Modeling & Secret Redaction Audit",
                purpose="Enforce zero-trust boundaries and 19-point SaaS security baseline checklist.",
                sector_id=MasterSector.EIS_11,
                required_skills=["saas-security-baseline", "secure-engineering"],
                required_tools=["semgrep", "bandit", "trufflehog"],
                risk_level="high",
            ),
            EngineeringCapability(
                id="CAP-AI-001",
                name="RAG Pipeline Engineering & Context Budgeting",
                purpose="Implement semantic vector search with prompt injection defense and schema validation.",
                sector_id=MasterSector.EIS_05,
                required_skills=["ai-context-engineering"],
                required_tools=["pgvector", "gemini", "claude", "openai"],
            ),
            EngineeringCapability(
                id="CAP-QA-001",
                name="Multi-Tier Test Pyramid & Release Gate Scoring",
                purpose="Author deterministic unit/integration/E2E test suites with >=90.0 score gate.",
                sector_id=MasterSector.EIS_12,
                required_skills=["testing-verification", "reliability-engineering"],
                required_tools=["pytest", "vitest", "playwright"],
            ),
            EngineeringCapability(
                id="CAP-VER-001",
                name="Independent Detached Verification & Attestation",
                purpose="Execute independent audit and sign cryptographic release gate without drafting bias.",
                sector_id=MasterSector.EIS_12,
                required_skills=["testing-verification", "saas-security-baseline"],
                required_tools=["sqlite3", "hashlib", "pytest"],
                risk_level="critical",
            ),
        ]
        for c in core:
            self.register_capability(c)

        # Map to native 16 specialist agents
        self.map_agent_capability("openclone-product-requirements-agent", "CAP-REQ-001")
        self.map_agent_capability("openclone-product-architect-agent", "CAP-ARCH-001")
        self.map_agent_capability("openclone-backend-agent", "CAP-DEV-001")
        self.map_agent_capability("openclone-database-agent", "CAP-DB-001")
        self.map_agent_capability("openclone-security-agent", "CAP-SEC-001")
        self.map_agent_capability("openclone-ai-engineering-agent", "CAP-AI-001")
        self.map_agent_capability("openclone-test-qa-agent", "CAP-QA-001")
        self.map_agent_capability("openclone-independent-verifier-agent", "CAP-VER-001")

    def register_capability(self, cap: EngineeringCapability) -> None:
        self._capabilities[cap.id] = cap

    def get_capability(self, cap_id: str) -> Optional[EngineeringCapability]:
        return self._capabilities.get(cap_id)

    def map_agent_capability(self, agent_id: str, cap_id: str) -> None:
        if cap_id in self._capabilities:
            self._agent_capability_map.setdefault(agent_id, set()).add(cap_id)

    def get_agent_capabilities(self, agent_id: str) -> List[EngineeringCapability]:
        cap_ids = self._agent_capability_map.get(agent_id, set())
        return [self._capabilities[cid] for cid in cap_ids if cid in self._capabilities]

    def find_capable_agents(self, cap_id: str) -> List[str]:
        agents = []
        for agent_id, cap_set in self._agent_capability_map.items():
            if cap_id in cap_set:
                agents.append(agent_id)
        return agents
