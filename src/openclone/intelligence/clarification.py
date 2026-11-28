"""Socratic Clarification Engine for Project Intelligence.

Systematically identifies ambiguities, contradictions, unstated technical assumptions,
and missing workload/business parameters in software requirements. Generates targeted,
prioritized clarification questions and integrates answered context back into PIA models.
"""
from __future__ import annotations

import enum
import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


class QuestionPriority(str, enum.Enum):
    """Priority level for clarifying questions."""
    BLOCKER = "blocker"  # Must be answered before architecture can proceed safely
    HIGH = "high"        # Significant architectural or sizing impact
    MEDIUM = "medium"    # Affects technology choice or API design
    LOW = "low"          # Implementation detail or optional polish


class ClarificationCategory(str, enum.Enum):
    """Domain category for clarification questions."""
    WORKLOAD_SCALE = "workload_scale"
    DATA_PERSISTENCE = "data_persistence"
    SECURITY_AUTH = "security_auth"
    DEPLOYMENT_TARGET = "deployment_target"
    BUSINESS_GOALS = "business_goals"
    API_CONTRACTS = "api_contracts"
    AMBIGUITY_RESOLVE = "ambiguity_resolve"
    CONTRADICTION_RESOLVE = "contradiction_resolve"


class QuestionStatus(str, enum.Enum):
    """Lifecycle state of a clarification question."""
    PENDING = "pending"
    ANSWERED = "answered"
    DEFERRED = "deferred"
    RESOLVED = "resolved"


@dataclass
class ClarificationOption:
    """Pre-formulated multiple choice option for actionable decision making."""
    option_id: str
    label: str
    architectural_impact: str
    is_recommended: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "option_id": self.option_id,
            "label": self.label,
            "architectural_impact": self.architectural_impact,
            "is_recommended": self.is_recommended,
        }


@dataclass
class ClarificationQuestion:
    """Actionable clarifying question targeting ambiguous or missing requirements."""
    question_id: str
    priority: QuestionPriority
    category: ClarificationCategory
    title: str
    question_text: str
    why_it_matters: str
    default_assumption_if_unanswered: str
    options: List[ClarificationOption] = field(default_factory=list)
    status: QuestionStatus = QuestionStatus.PENDING
    answer: Optional[str] = None
    answered_by: Optional[str] = None
    affected_components: List[str] = field(default_factory=list)
    source_evidence_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "priority": self.priority.value,
            "category": self.category.value,
            "title": self.title,
            "question_text": self.question_text,
            "why_it_matters": self.why_it_matters,
            "default_assumption_if_unanswered": self.default_assumption_if_unanswered,
            "options": [opt.to_dict() for opt in self.options],
            "status": self.status.value,
            "answer": self.answer,
            "answered_by": self.answered_by,
            "affected_components": self.affected_components,
            "source_evidence_id": self.source_evidence_id,
        }


class SocraticClarificationEngine:
    """Engine that inspects requirements, extracts gaps, and manages clarification lifecycles."""

    def __init__(self):
        self.question_history: Dict[str, ClarificationQuestion] = {}

    def analyze_requirements(
        self,
        requirements_text: str,
        profile: Optional[Any] = None,
        existing_gaps: Optional[List[Dict[str, Any]]] = None,
        evidence_items: Optional[List[Any]] = None,
    ) -> List[ClarificationQuestion]:
        """Inspect requirements text, profile, and evidence to generate prioritized questions."""
        text = requirements_text or ""
        text_lower = text.lower()
        questions: List[ClarificationQuestion] = []

        # 1. Missing Workload Parameters Check
        has_dau = bool(re.search(r"\b(\d+[\d,]*)\s*(dau|daily\s+active\s+users)\b", text_lower))
        has_rps = bool(re.search(r"\b(\d+[\d,]*)\s*(rps|qps|req/s|requests\s+per\s+second)\b", text_lower))
        if not has_dau and not has_rps:
            qid = "CLARIF-SCALE-001"
            questions.append(
                ClarificationQuestion(
                    question_id=qid,
                    priority=QuestionPriority.BLOCKER,
                    category=ClarificationCategory.WORKLOAD_SCALE,
                    title="Expected Daily Active Users and Request Volume",
                    question_text="What is the anticipated peak and sustained daily active user (DAU) count or requests-per-second (RPS)?",
                    why_it_matters="Without explicit workload metrics, capacity estimation cannot size database storage, replication, cache tiers, or connection pools without guessing.",
                    default_assumption_if_unanswered="System will be initialized in UnestimatedCapacityReport status until explicit workload scale is provided.",
                    options=[
                        ClarificationOption("OPT-1", "Early Stage (< 5,000 DAU, < 10 RPS)", "Single relational DB node, simple local cache, low operational overhead.", is_recommended=True),
                        ClarificationOption("OPT-2", "Mid Scale (5,000 - 100,000 DAU, 10 - 200 RPS)", "Primary-replica relational DB, Redis cluster, background workers.", is_recommended=False),
                        ClarificationOption("OPT-3", "High Scale (> 100,000 DAU, > 1,000 RPS)", "Horizontally partitioned/sharded DB, distributed cache, event-driven queueing.", is_recommended=False),
                    ],
                    affected_components=["CapacityEstimator", "DatabaseTier", "CacheTier"],
                )
            )

        # 2. Authentication & Authorization Clarification
        auth_keywords = ["login", "user", "signup", "auth", "permission", "rbac", "jwt", "session"]
        has_user_mention = any(k in text_lower for k in auth_keywords)
        has_explicit_auth_spec = any(k in text_lower for k in ["oauth2", "oidc", "jwt", "session cookie", "saml", "sso"])
        if has_user_mention and not has_explicit_auth_spec:
            qid = "CLARIF-AUTH-001"
            questions.append(
                ClarificationQuestion(
                    question_id=qid,
                    priority=QuestionPriority.HIGH,
                    category=ClarificationCategory.SECURITY_AUTH,
                    title="Authentication & Session Strategy",
                    question_text="Which authentication and identity management mechanism should the service implement?",
                    why_it_matters="Decides whether the backend requires cryptographic token verification (stateless JWT), centralized Redis sessions, or external identity provider integration (OIDC/SAML).",
                    default_assumption_if_unanswered="Stateless HMAC-SHA256 JWT tokens with short expiry and refresh token rotation.",
                    options=[
                        ClarificationOption("OPT-AUTH-1", "Stateless JWT (HMAC-SHA256)", "Low database lookup overhead, ideal for microservices and REST APIs.", is_recommended=True),
                        ClarificationOption("OPT-AUTH-2", "Stateful Server Sessions in Redis", "Immediate server-side revocation, session inspection, higher state dependency.", is_recommended=False),
                        ClarificationOption("OPT-AUTH-3", "External OAuth2 / OIDC Provider", "Delegated identity (Google/GitHub/Auth0), reduces secret management burden.", is_recommended=False),
                    ],
                    affected_components=["AuthGateway", "SecurityModel", "UserStore"],
                )
            )

        # 3. Data Persistence & ACID Requirements
        has_data_keywords = any(k in text_lower for k in ["data", "record", "transaction", "payment", "order", "entity", "store", "items", "task", "create items"])
        has_explicit_db = any(k in text_lower for k in ["postgres", "postgresql", "mysql", "sqlite", "mongodb", "dynamodb", "cassandra"])
        if has_data_keywords and not has_explicit_db:
            qid = "CLARIF-DATA-001"
            questions.append(
                ClarificationQuestion(
                    question_id=qid,
                    priority=QuestionPriority.HIGH,
                    category=ClarificationCategory.DATA_PERSISTENCE,
                    title="Database Storage Model and ACID Consistency",
                    question_text="What primary data persistence model best fits your operational requirements?",
                    why_it_matters="Influences schema migration tooling, transaction isolation, relationship modeling, and horizontal sharding complexity.",
                    default_assumption_if_unanswered="Relational PostgreSQL with ACID transactions and structured migration files.",
                    options=[
                        ClarificationOption("OPT-DATA-1", "Relational Database (PostgreSQL)", "Strict schema integrity, relational joins, ACID compliance, broad ecosystem support.", is_recommended=True),
                        ClarificationOption("OPT-DATA-2", "Document Database (MongoDB/DocumentDB)", "Flexible schema for evolving hierarchical documents, eventual consistency.", is_recommended=False),
                        ClarificationOption("OPT-DATA-3", "Embedded Relational (SQLite)", "Zero-ops single-file database, suited for standalone CLI, desktop, or local agent nodes.", is_recommended=False),
                    ],
                    affected_components=["DatabaseTier", "SchemaMigrations", "ORM"],
                )
            )

        # 4. Deployment Target & Hosting Platform
        has_deploy_spec = any(k in text_lower for k in ["kubernetes", "k8s", "docker", "serverless", "aws", "gcp", "azure", "bare metal", "linux systemd"])
        if not has_deploy_spec:
            qid = "CLARIF-DEPLOY-001"
            questions.append(
                ClarificationQuestion(
                    question_id=qid,
                    priority=QuestionPriority.MEDIUM,
                    category=ClarificationCategory.DEPLOYMENT_TARGET,
                    title="Target Deployment Runtime",
                    question_text="Where and how will the application runtime be deployed and orchestrated?",
                    why_it_matters="Determines whether to author Dockerfiles, Kubernetes manifests, Serverless configs, or native OS systemd service units.",
                    default_assumption_if_unanswered="Containerized service with multi-stage Dockerfile and docker-compose.yml for local and staging orchestration.",
                    options=[
                        ClarificationOption("OPT-DEP-1", "OCI Containers (Docker / Docker Compose)", "Universal portability, reproducible builds across dev and production.", is_recommended=True),
                        ClarificationOption("OPT-DEP-2", "Kubernetes (EKS / GKE / AKS)", "Automated autoscaling, ingress management, high-density cluster workloads.", is_recommended=False),
                        ClarificationOption("OPT-DEP-3", "Serverless / Container-as-a-Service (Cloud Run / AWS Lambda)", "Zero idle cost, automatic scaling, strict stateless execution boundaries.", is_recommended=False),
                    ],
                    affected_components=["DeploymentManifests", "CICDPipeline", "ContainerConfig"],
                )
            )

        # 5. Check Contradictions Across Requirements / Gaps
        if existing_gaps:
            for g in existing_gaps:
                g_title = g.get("title", "") if isinstance(g, dict) else getattr(g, "title", "")
                if "conflict" in g_title.lower() or "contradiction" in g_title.lower():
                    qid = f"CLARIF-CONF-{len(questions)+1:03d}"
                    questions.append(
                        ClarificationQuestion(
                            question_id=qid,
                            priority=QuestionPriority.BLOCKER,
                            category=ClarificationCategory.CONTRADICTION_RESOLVE,
                            title=f"Resolve Contradiction: {g_title[:40]}",
                            question_text=f"A specification contradiction was detected: '{g_title}'. Which requirement takes precedence?",
                            why_it_matters="Contradictory specifications prevent deterministic phase execution and create architecture divergence.",
                            default_assumption_if_unanswered="Higher-tier architecture constraints override lower-tier feature notes.",
                            affected_components=["SpecificationAlignment"],
                        )
                    )

        # 6. Ambiguity checks (e.g., words like "fast", "scalable", "user friendly" without metrics)
        vague_patterns = [
            (re.compile(r"\b(real[\s-]time|fast|low[\s-]latency)\b", re.IGNORECASE), "Latency SLA Requirement", "What is the acceptable P99 and P95 latency threshold (e.g. < 100ms)?"),
            (re.compile(r"\b(scalable|high[\s-]availability|fault[\s-]tolerant)\b", re.IGNORECASE), "Availability Target (SLA)", "What uptime SLA is required (e.g. 99.9% vs 99.99%)?"),
        ]
        for pat, title, qtext in vague_patterns:
            if pat.search(text):
                qid = f"CLARIF-AMBIG-{len(questions)+1:03d}"
                questions.append(
                    ClarificationQuestion(
                        question_id=qid,
                        priority=QuestionPriority.MEDIUM,
                        category=ClarificationCategory.AMBIGUITY_RESOLVE,
                        title=title,
                        question_text=qtext,
                        why_it_matters="Abstract adjectives without quantitative metrics cannot be validated in automated quality gates.",
                        default_assumption_if_unanswered="Target P99 latency < 250ms and 99.9% availability.",
                        affected_components=["SLAPolicy", "ObservabilityMetrics"],
                    )
                )

        # Register generated questions in history
        for q in questions:
            self.question_history[q.question_id] = q

        return questions

    def record_answer(
        self,
        question_id: str,
        answer: str,
        answered_by: str = "human",
    ) -> Optional[ClarificationQuestion]:
        """Record an answer to an existing question and update its lifecycle status."""
        q = self.question_history.get(question_id)
        if not q:
            return None

        q.answer = answer.strip()
        q.answered_by = answered_by
        q.status = QuestionStatus.ANSWERED
        return q

    def get_pending_blockers(self) -> List[ClarificationQuestion]:
        """Return all unresolved BLOCKER questions."""
        return [
            q for q in self.question_history.values()
            if q.status == QuestionStatus.PENDING and q.priority == QuestionPriority.BLOCKER
        ]

    def get_clarification_summary(self) -> Dict[str, Any]:
        """Produce a structured status summary across all tracked clarification items."""
        total = len(self.question_history)
        answered = sum(1 for q in self.question_history.values() if q.status == QuestionStatus.ANSWERED)
        pending = sum(1 for q in self.question_history.values() if q.status == QuestionStatus.PENDING)
        blockers = sum(1 for q in self.question_history.values() if q.priority == QuestionPriority.BLOCKER and q.status == QuestionStatus.PENDING)

        return {
            "total_questions": total,
            "answered_questions": answered,
            "pending_questions": pending,
            "active_blockers": blockers,
            "questions": [q.to_dict() for q in self.question_history.values()],
        }

    def synthesize_context_update(self) -> Dict[str, Any]:
        """Convert answered questions into explicit project context updates for PIA."""
        context_updates: Dict[str, Any] = {
            "explicit_workload": {},
            "explicit_technologies": [],
            "resolved_constraints": [],
        }

        for q in self.question_history.values():
            if q.status != QuestionStatus.ANSWERED or not q.answer:
                continue

            if q.category == ClarificationCategory.WORKLOAD_SCALE:
                dau_m = re.search(r"(\d[\d,]*)\s*(?:dau|daily\s+active\s+users)", q.answer, re.IGNORECASE)
                if dau_m:
                    context_updates["explicit_workload"]["daily_active_users"] = int(dau_m.group(1).replace(",", ""))
                elif "5,000" in q.answer or "early" in q.answer.lower():
                    context_updates["explicit_workload"]["daily_active_users"] = 5_000
                elif "100,000" in q.answer or "mid" in q.answer.lower():
                    context_updates["explicit_workload"]["daily_active_users"] = 50_000

            elif q.category == ClarificationCategory.DATA_PERSISTENCE:
                if "postgres" in q.answer.lower():
                    context_updates["explicit_technologies"].append("PostgreSQL")
                elif "sqlite" in q.answer.lower():
                    context_updates["explicit_technologies"].append("SQLite")
                elif "mongo" in q.answer.lower():
                    context_updates["explicit_technologies"].append("MongoDB")

            elif q.category == ClarificationCategory.SECURITY_AUTH:
                if "jwt" in q.answer.lower():
                    context_updates["explicit_technologies"].append("JWT")
                elif "oauth" in q.answer.lower() or "oidc" in q.answer.lower():
                    context_updates["explicit_technologies"].append("OAuth2/OIDC")

            context_updates["resolved_constraints"].append(f"{q.title}: {q.answer}")

        return context_updates
