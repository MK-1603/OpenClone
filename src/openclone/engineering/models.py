"""
OpenClone Engineering Intelligence System (EIS) Models and Registries.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


class MasterSector(str, Enum):
    EIS_01 = "EIS-01"  # Problem Intelligence & Requirements
    EIS_02 = "EIS-02"  # Systems Engineering
    EIS_03 = "EIS-03"  # Software Engineering
    EIS_04 = "EIS-04"  # Software Architecture & System Design
    EIS_05 = "EIS-05"  # AI & Intelligent Systems Engineering
    EIS_06 = "EIS-06"  # Machine Learning & Model Engineering
    EIS_07 = "EIS-07"  # Data Engineering & Intelligence
    EIS_08 = "EIS-08"  # Database & Storage Engineering
    EIS_09 = "EIS-09"  # Cloud & Infrastructure Engineering
    EIS_10 = "EIS-10"  # DevOps, Platform & Release Engineering
    EIS_11 = "EIS-11"  # Cybersecurity Engineering
    EIS_12 = "EIS-12"  # Quality, Testing & Verification
    EIS_13 = "EIS-13"  # Reliability, Resilience & Performance
    EIS_14 = "EIS-14"  # Networking & Communication
    EIS_15 = "EIS-15"  # Software Product & Experience Engineering
    EIS_16 = "EIS-16"  # Software Domain & Industry Engineering
    EIS_17 = "EIS-17"  # Engineering Research, Operations & Lifecycle


class KnowledgeType(str, Enum):
    TECHNICAL_CONCEPT = "technical_concept"
    ENGINEERING_PRINCIPLE = "engineering_principle"
    ARCHITECTURE_PATTERN = "architecture_pattern"
    ALGORITHM = "algorithm"
    IMPLEMENTATION_METHOD = "implementation_method"
    INDUSTRY_STANDARD = "industry_standard"
    FAILURE_PATTERN = "failure_pattern"
    CASE_STUDY = "case_study"


class KnowledgeMaturity(str, Enum):
    LEVEL_0_DISCOVERED = "L0_DISCOVERED"
    LEVEL_1_DOCUMENTED = "L1_DOCUMENTED"
    LEVEL_2_STRUCTURED = "L2_STRUCTURED"
    LEVEL_3_SOURCE_VERIFIED = "L3_SOURCE_VERIFIED"
    LEVEL_4_TECHNICALLY_VALIDATED = "L4_TECHNICALLY_VALIDATED"
    LEVEL_5_PRACTICALLY_TESTED = "L5_PRACTICALLY_TESTED"
    LEVEL_6_CONTINUOUSLY_MAINTAINED = "L6_CONTINUOUSLY_MAINTAINED"


@dataclass
class KnowledgeSourceRef:
    uri: str
    source_type: str = "specification"
    publisher: Optional[str] = None
    revision: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "source_type": self.source_type,
            "publisher": self.publisher,
            "revision": self.revision,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> KnowledgeSourceRef:
        return cls(
            uri=data.get("uri", ""),
            source_type=data.get("source_type", "specification"),
            publisher=data.get("publisher"),
            revision=data.get("revision"),
        )


@dataclass
class KnowledgeUnit:
    id: str
    title: str
    sector_id: MasterSector
    domain_id: str
    subdomain_id: str
    specialization_id: str
    knowledge_type: KnowledgeType
    description: str
    purpose: str
    schema_version: str = "2.0"
    technical_depth: str = "intermediate"
    prerequisites: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    principles: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    algorithms: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    standards: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    security_considerations: List[str] = field(default_factory=list)
    performance_considerations: List[str] = field(default_factory=list)
    validation_methods: List[str] = field(default_factory=list)
    related_knowledge: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    source_refs: List[KnowledgeSourceRef] = field(default_factory=list)
    authority: str = "verified"
    confidence: float = 0.95
    status: str = "active"
    maturity: KnowledgeMaturity = KnowledgeMaturity.LEVEL_4_TECHNICALLY_VALIDATED
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Optional[str] = None
    reviewed_at: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.sector_id, str):
            self.sector_id = MasterSector(self.sector_id)
        if isinstance(self.knowledge_type, str):
            self.knowledge_type = KnowledgeType(self.knowledge_type)
        if isinstance(self.maturity, str):
            self.maturity = KnowledgeMaturity(self.maturity)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "schema_version": self.schema_version,
            "title": self.title,
            "sector_id": self.sector_id.value,
            "domain_id": self.domain_id,
            "subdomain_id": self.subdomain_id,
            "specialization_id": self.specialization_id,
            "knowledge_type": self.knowledge_type.value,
            "description": self.description,
            "purpose": self.purpose,
            "technical_depth": self.technical_depth,
            "prerequisites": list(self.prerequisites),
            "concepts": list(self.concepts),
            "principles": list(self.principles),
            "methods": list(self.methods),
            "patterns": list(self.patterns),
            "algorithms": list(self.algorithms),
            "tools": list(self.tools),
            "standards": list(self.standards),
            "use_cases": list(self.use_cases),
            "limitations": list(self.limitations),
            "failure_modes": list(self.failure_modes),
            "security_considerations": list(self.security_considerations),
            "performance_considerations": list(self.performance_considerations),
            "validation_methods": list(self.validation_methods),
            "related_knowledge": list(self.related_knowledge),
            "dependencies": list(self.dependencies),
            "source_refs": [s.to_dict() if hasattr(s, "to_dict") else s for s in self.source_refs],
            "authority": self.authority,
            "confidence": self.confidence,
            "status": self.status,
            "maturity": self.maturity.value,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "reviewed_at": self.reviewed_at,
        }
