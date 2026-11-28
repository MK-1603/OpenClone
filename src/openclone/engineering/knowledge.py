"""OpenClone Engineering Knowledge Catalogue & Decision Intelligence.

Provides structured models for concepts, principles, patterns, standards,
frameworks, technologies, tools, and context-dependent architectural trade-offs.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain


class ConceptType(str, enum.Enum):
    PRINCIPLE = "PRINCIPLE"
    PATTERN = "PATTERN"
    ARCHITECTURE_STYLE = "ARCHITECTURE_STYLE"
    METHODOLOGY = "METHODOLOGY"
    TECHNIQUE = "TECHNIQUE"
    STANDARD = "STANDARD"
    FRAMEWORK = "FRAMEWORK"
    TECHNOLOGY = "TECHNOLOGY"
    TOOL = "TOOL"
    ANTI_PATTERN = "ANTI_PATTERN"


@dataclass
class DecisionIntelligenceRecord:
    concept_id: str
    concept_name: str
    applicable_when: List[str] = field(default_factory=list)
    avoid_when: List[str] = field(default_factory=list)
    advantages: List[str] = field(default_factory=list)
    disadvantages: List[str] = field(default_factory=list)
    complexity_level: str = "medium"  # low, medium, high, extreme
    alternatives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)


@dataclass
class EngineeringConceptNode:
    concept_id: str
    name: str
    concept_type: ConceptType
    domain: EngineeringDomain
    subdomain: str
    description: str
    decision_record: Optional[DecisionIntelligenceRecord] = None
    related_concepts: List[str] = field(default_factory=list)
    prerequisite_concepts: List[str] = field(default_factory=list)
    applicable_roles: List[str] = field(default_factory=list)
    applicable_standards: List[str] = field(default_factory=list)


class EngineeringKnowledgeCatalogue:
    """Master repository of governed engineering concepts and decision trade-offs."""

    _instance: Optional["EngineeringKnowledgeCatalogue"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.concepts: Dict[str, EngineeringConceptNode] = {}
        self._populate_core_concepts()
        self._initialized = True

    def register_concept(self, concept: EngineeringConceptNode) -> None:
        self.concepts[concept.concept_id] = concept

    def get_concept(self, concept_id: str) -> Optional[EngineeringConceptNode]:
        return self.concepts.get(concept_id)

    def list_concepts(self, domain: Optional[EngineeringDomain] = None) -> List[EngineeringConceptNode]:
        if domain:
            return [c for c in self.concepts.values() if c.domain == domain]
        return list(self.concepts.values())

    def get_decision_intelligence(self, concept_id: str) -> Optional[DecisionIntelligenceRecord]:
        concept = self.get_concept(concept_id)
        return concept.decision_record if concept else None

    def _populate_core_concepts(self) -> None:
        # Microservices Architecture
        self.register_concept(
            EngineeringConceptNode(
                concept_id="concept.arch.microservices",
                name="Microservices Architecture",
                concept_type=ConceptType.ARCHITECTURE_STYLE,
                domain=EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
                subdomain="architectural_styles",
                description="Decomposition of an application into loosely coupled, independently deployable services.",
                decision_record=DecisionIntelligenceRecord(
                    concept_id="concept.arch.microservices",
                    concept_name="Microservices Architecture",
                    applicable_when=[
                        "Independent scaling of specific business components is required",
                        "Multiple autonomous engineering teams own distinct bounded contexts",
                        "Heterogeneous technology stacks are technically justified",
                    ],
                    avoid_when=[
                        "Small teams or early-stage MVPs with rapid domain boundary shifts",
                        "Low operational maturity in distributed observability, CI/CD, and networking",
                    ],
                    advantages=["Independent deployments", "Fault isolation", "Targeted horizontal scaling"],
                    disadvantages=["Distributed complexity", "Eventual consistency hurdles", "Network latency"],
                    complexity_level="high",
                    alternatives=["concept.arch.modular_monolith", "concept.arch.serverless"],
                    prerequisites=["concept.ops.ci_cd", "concept.ops.containers", "concept.sre.distributed_tracing"],
                    failure_modes=["Distributed monolith (tight coupling)", "Cascading network timeouts"],
                ),
                related_concepts=["concept.arch.saga_pattern", "concept.arch.cqrs", "concept.sys.api_gateway"],
                applicable_roles=["principal-architect", "distributed-systems-architect"],
            )
        )

        # Modular Monolith
        self.register_concept(
            EngineeringConceptNode(
                concept_id="concept.arch.modular_monolith",
                name="Modular Monolith",
                concept_type=ConceptType.ARCHITECTURE_STYLE,
                domain=EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
                subdomain="architectural_styles",
                description="Unified deployment artifact with strictly enforced internal module boundaries and domain isolation.",
                decision_record=DecisionIntelligenceRecord(
                    concept_id="concept.arch.modular_monolith",
                    concept_name="Modular Monolith",
                    applicable_when=[
                        "Fast initial delivery is needed without distributed operational overhead",
                        "Domain boundaries are still being discovered or clarified",
                        "Single or co-located engineering team",
                    ],
                    avoid_when=[
                        "Massive scale requires independent team release cycles at high cadence",
                        "Extreme workload variance demands individual micro-service autoscaling",
                    ],
                    advantages=["Simple deployment", "Single database ACID transactions", "Low operational overhead"],
                    disadvantages=["Shared runtime failure domain", "Potential boundary erosion without strict linting"],
                    complexity_level="medium",
                    alternatives=["concept.arch.microservices"],
                    prerequisites=["concept.arch.clean_architecture", "concept.code.ast_analysis"],
                    failure_modes=["Big ball of mud if dependency rules are not linted"],
                ),
                related_concepts=["concept.arch.clean_architecture", "concept.arch.ddd"],
                applicable_roles=["principal-architect", "backend-lead"],
            )
        )

        # Saga Pattern
        self.register_concept(
            EngineeringConceptNode(
                concept_id="concept.arch.saga_pattern",
                name="Saga Pattern",
                concept_type=ConceptType.PATTERN,
                domain=EngineeringDomain.DOMAIN_06_BACKEND,
                subdomain="distributed_patterns",
                description="Manages distributed transactions through a sequence of local transactions and compensating transactions.",
                decision_record=DecisionIntelligenceRecord(
                    concept_id="concept.arch.saga_pattern",
                    concept_name="Saga Pattern",
                    applicable_when=[
                        "Transactions span multiple microservices with individual databases",
                        "Eventual consistency is acceptable to business domain",
                    ],
                    avoid_when=[
                        "Single database ACID transactions are possible",
                        "Compensating actions cannot restore a sensible business state",
                    ],
                    advantages=["Maintains consistency across distributed services without distributed locks"],
                    disadvantages=["Complex compensation workflows", "Lack of cross-service isolation"],
                    complexity_level="high",
                    alternatives=["concept.arch.two_phase_commit"],
                    prerequisites=["concept.msg.event_driven", "concept.arch.outbox_pattern"],
                    failure_modes=["Failed compensation causing orphaned intermediate states"],
                ),
                related_concepts=["concept.arch.two_phase_commit", "concept.arch.outbox_pattern"],
                applicable_roles=["distributed-systems-architect", "backend-lead"],
            )
        )

        # Zero Trust Security
        self.register_concept(
            EngineeringConceptNode(
                concept_id="concept.sec.zero_trust",
                name="Zero Trust Architecture",
                concept_type=ConceptType.PRINCIPLE,
                domain=EngineeringDomain.DOMAIN_12_SECURITY,
                subdomain="security_architecture",
                description="Never trust, always verify: strict identity verification, micro-segmentation, and least privilege.",
                decision_record=DecisionIntelligenceRecord(
                    concept_id="concept.sec.zero_trust",
                    concept_name="Zero Trust Architecture",
                    applicable_when=[
                        "Enterprise applications handling sensitive, financial, or healthcare data",
                        "Distributed cloud and hybrid multi-tenant environments",
                    ],
                    avoid_when=["Never avoided for production systems; essential default."],
                    advantages=["Prevents lateral movement in breaches", "Explicit cryptographic verification"],
                    disadvantages=["Requires mature identity and secret management infrastructure"],
                    complexity_level="medium",
                    alternatives=[],
                    prerequisites=["concept.sec.iam", "concept.sec.mtls"],
                    failure_modes=["Overly permissive service account tokens"],
                ),
                related_concepts=["concept.sec.stride", "concept.sec.rbac", "concept.sec.least_privilege"],
                applicable_roles=["security-architect", "security-engineer"],
            )
        )

        # Retrieval-Augmented Generation (RAG)
        self.register_concept(
            EngineeringConceptNode(
                concept_id="concept.ai.rag",
                name="Retrieval-Augmented Generation (RAG)",
                concept_type=ConceptType.PATTERN,
                domain=EngineeringDomain.DOMAIN_11_AI,
                subdomain="rag_architecture",
                description="Grounds LLM responses in external verified knowledge via semantic vector search.",
                decision_record=DecisionIntelligenceRecord(
                    concept_id="concept.ai.rag",
                    concept_name="Retrieval-Augmented Generation (RAG)",
                    applicable_when=[
                        "LLMs require private, proprietary, or rapidly changing domain knowledge",
                        "Minimizing hallucinations through verified source citations is critical",
                    ],
                    avoid_when=[
                        "The task requires purely structured calculations or deterministic lookups",
                    ],
                    advantages=["Eliminates need for continuous model retraining", "Source attribution"],
                    disadvantages=["Chunking & embedding drift", "Context window token costs"],
                    complexity_level="medium",
                    alternatives=["concept.ai.fine_tuning", "concept.ai.prompt_stuffing"],
                    prerequisites=["concept.db.vector_search", "concept.ai.embeddings"],
                    failure_modes=["Retrieving irrelevant chunks polluting generation context"],
                ),
                related_concepts=["concept.db.vector_search", "concept.ai.embeddings", "concept.ai.mcp"],
                applicable_roles=["ai-systems-architect", "prompt-engineer"],
            )
        )
