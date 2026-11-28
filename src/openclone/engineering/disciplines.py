"""OpenClone Complete Engineering Discipline Registry.

Defines the comprehensive 155-discipline catalogue spanning all 23 canonical
engineering domains, with subdomains, objectives, key skills, and roles.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from src.openclone.engineering.taxonomy import EngineeringDomain


@dataclass
class DisciplineDescriptor:
    discipline_id: str
    name: str
    slug: str
    domain: EngineeringDomain
    subdomain: str
    description: str
    objectives: List[str] = field(default_factory=list)
    key_roles: List[str] = field(default_factory=list)
    key_skills: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    maturity_level: str = "mainstream"


class EngineeringDisciplineRegistry:
    """Master registry of all 155 specialized engineering disciplines."""

    _instance: Optional["EngineeringDisciplineRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.disciplines: Dict[str, DisciplineDescriptor] = {}
        self._domain_index: Dict[EngineeringDomain, List[str]] = {d: [] for d in EngineeringDomain}
        self._populate_all_disciplines()
        self._initialized = True

    def register_discipline(self, desc: DisciplineDescriptor) -> None:
        self.disciplines[desc.discipline_id] = desc
        if desc.domain in self._domain_index:
            if desc.discipline_id not in self._domain_index[desc.domain]:
                self._domain_index[desc.domain].append(desc.discipline_id)
        else:
            self._domain_index[desc.domain] = [desc.discipline_id]

    def get_discipline(self, discipline_id: str) -> Optional[DisciplineDescriptor]:
        return self.disciplines.get(discipline_id)

    def list_disciplines(self, domain: Optional[EngineeringDomain] = None) -> List[DisciplineDescriptor]:
        if domain:
            ids = self._domain_index.get(domain, [])
            return [self.disciplines[i] for i in ids if i in self.disciplines]
        return list(self.disciplines.values())

    def _populate_all_disciplines(self) -> None:
        raw_catalogue = [
            # GROUP A — Product, Business & Requirements (1–18)
            ("disc-001", "Product Vision & Strategy Definition", "product_discovery", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager", "principal-architect"], ["skill.product.strategy"]),
            ("disc-002", "Business Model Canvas & Value Proposition", "product_discovery", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager"], ["skill.product.strategy"]),
            ("disc-003", "User Persona & Customer Journey Mapping", "product_discovery", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager", "ux-designer"], ["skill.ux.research"]),
            ("disc-004", "Market Research & Competitive Intelligence", "benchmarking", EngineeringDomain.DOMAIN_03_RESEARCH, ["research-engineer"], ["skill.research.market"]),
            ("disc-005", "Technical Feasibility & PoC Scoping", "feasibility", EngineeringDomain.DOMAIN_03_RESEARCH, ["solution-architect", "research-engineer"], ["skill.research.feasibility"]),
            ("disc-006", "Feature Prioritization (RICE/MoSCoW)", "feature_engineering", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager"], ["skill.product.prioritization"]),
            ("disc-007", "Product Roadmap & Milestone Planning", "roadmapping", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager", "technical-program-manager"], ["skill.product.roadmap"]),
            ("disc-008", "Stakeholder Interviewing & Elicitation", "elicitation", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer"], ["skill.req.elicitation"]),
            ("disc-009", "Functional Requirements Specification", "specification", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer"], ["skill.req.specification"]),
            ("disc-010", "Non-Functional Requirements (NFR) Formulation", "specification", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer", "principal-architect"], ["skill.req.nfr"]),
            ("disc-011", "User Story Authoring & Epic Decomposition", "analysis", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer", "product-manager"], ["skill.req.stories"]),
            ("disc-012", "Acceptance Criteria & BDD Given-When-Then", "validation", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer", "qa-lead"], ["skill.req.bdd"]),
            ("disc-013", "Requirements Traceability Matrix Maintenance", "traceability", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer"], ["skill.req.traceability"]),
            ("disc-014", "Scope Management & Anti-Scope Boundaries", "analysis", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer"], ["skill.req.scope"]),
            ("disc-015", "Regulatory & Industry Mandate Discovery", "elicitation", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["compliance-officer", "requirements-engineer"], ["skill.gov.compliance"]),
            ("disc-016", "Domain-Driven Design Ubiquitous Language", "specification", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["principal-architect", "requirements-engineer"], ["skill.arch.ddd"]),
            ("disc-017", "Socratic Clarification & Ambiguity Elimination", "validation", EngineeringDomain.DOMAIN_02_REQUIREMENTS, ["requirements-engineer"], ["skill.req.clarification"]),
            ("disc-018", "KPI, Product Analytics & Success Metrics", "product_metrics", EngineeringDomain.DOMAIN_01_PRODUCT, ["product-manager", "data-analyst"], ["skill.product.analytics"]),

            # GROUP B — Software Architecture & System Design (19–38)
            ("disc-019", "Architectural Style Selection", "architectural_styles", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["principal-architect"], ["skill.arch.patterns"]),
            ("disc-020", "Modular Monolith Architecture", "architectural_styles", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["principal-architect", "backend-lead"], ["skill.arch.monolith"]),
            ("disc-021", "Microservices Decomposition & Boundaries", "architectural_styles", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["principal-architect", "distributed-systems-architect"], ["skill.arch.microservices"]),
            ("disc-022", "Event-Driven Architecture & Brokers", "architectural_styles", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["distributed-systems-architect"], ["skill.arch.eda"]),
            ("disc-023", "Clean Architecture & Dependency Inversion", "architectural_patterns", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["backend-lead"], ["skill.arch.clean"]),
            ("disc-024", "Hexagonal Architecture (Ports & Adapters)", "architectural_patterns", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["backend-lead"], ["skill.arch.hexagonal"]),
            ("disc-025", "Strategic & Tactical Domain-Driven Design", "domain_modeling", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["principal-architect"], ["skill.arch.ddd"]),
            ("disc-026", "CQRS Pattern Design", "architectural_patterns", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["distributed-systems-architect"], ["skill.arch.cqrs"]),
            ("disc-027", "Event Sourcing & Append-Only State", "architectural_patterns", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["distributed-systems-architect"], ["skill.arch.eventsourcing"]),
            ("disc-028", "Serverless & FaaS Architecture", "architectural_styles", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["cloud-architect"], ["skill.cloud.serverless"]),
            ("disc-029", "C4 Context Modeling", "c4_modeling", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect"], ["skill.sysdesign.c4"]),
            ("disc-030", "C4 Container Modeling", "c4_modeling", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect"], ["skill.sysdesign.c4"]),
            ("disc-031", "C4 Component Modeling", "c4_modeling", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect"], ["skill.sysdesign.c4"]),
            ("disc-032", "C4 Dynamic & Deployment Topology", "topology", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect", "cloud-architect"], ["skill.sysdesign.topology"]),
            ("disc-033", "High Availability & Disaster Recovery Topology", "resilience", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect", "sre-lead"], ["skill.sysdesign.ha"]),
            ("disc-034", "Zero-Invention Capacity Planning & Profiles", "capacity_planning", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["systems-architect"], ["skill.sysdesign.capacity"]),
            ("disc-035", "Cache Topologies & Invalidation Policies", "caching", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["backend-lead", "systems-architect"], ["skill.cache.redis"]),
            ("disc-036", "Message Queue & Event Stream Topologies", "messaging", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["distributed-systems-architect"], ["skill.msg.kafka"]),
            ("disc-037", "Async Task Processing & Worker Topologies", "messaging", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["backend-lead"], ["skill.worker.async"]),
            ("disc-038", "Architectural Decision Record (ADR) Formalization", "architecture_governance", EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE, ["principal-architect"], ["skill.arch.adr"]),

            # GROUP C — Frontend, Web, Mobile & UX (39–58)
            ("disc-039", "Information Architecture & Navigation", "information_architecture", EngineeringDomain.DOMAIN_04_UX_UI, ["ux-designer"], ["skill.ux.ia"]),
            ("disc-040", "Wireframing & Prototyping", "prototyping", EngineeringDomain.DOMAIN_04_UX_UI, ["ux-designer"], ["skill.ux.wireframing"]),
            ("disc-041", "Design System Tokens & Component Libraries", "design_systems", EngineeringDomain.DOMAIN_04_UX_UI, ["ui-designer", "frontend-engineer"], ["skill.ui.designsystems"]),
            ("disc-042", "WCAG 2.2 Level AA/AAA Accessibility", "accessibility", EngineeringDomain.DOMAIN_04_UX_UI, ["ui-designer", "frontend-engineer"], ["skill.a11y.wcag"]),
            ("disc-043", "Responsive & Adaptive Multi-Device Layouts", "responsive_design", EngineeringDomain.DOMAIN_04_UX_UI, ["ui-designer", "frontend-engineer"], ["skill.ui.responsive"]),
            ("disc-044", "Single-Page Application (SPA) Architecture", "spa_architecture", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-architect"], ["skill.frontend.spa"]),
            ("disc-045", "Server-Side Rendering (SSR) & SSG", "rendering_strategies", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-architect"], ["skill.frontend.ssr"]),
            ("disc-046", "Component Architecture & Composition", "component_architecture", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-engineer"], ["skill.frontend.components"]),
            ("disc-047", "Client-Side State Management", "state_management", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-engineer"], ["skill.frontend.state"]),
            ("disc-048", "Frontend Performance & Core Web Vitals", "performance", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-architect"], ["skill.frontend.perf"]),
            ("disc-049", "Micro-Frontends & Module Federation", "micro_frontends", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-architect"], ["skill.frontend.microfrontends"]),
            ("disc-050", "Progressive Web Apps & Service Workers", "pwa", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-engineer"], ["skill.frontend.pwa"]),
            ("disc-051", "Frontend Security (CSP, XSS, CSRF)", "frontend_security", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-engineer", "security-engineer"], ["skill.security.frontend"]),
            ("disc-052", "Native iOS Architecture (SwiftUI)", "ios_development", EngineeringDomain.DOMAIN_13_MOBILE, ["mobile-engineer"], ["skill.mobile.ios"]),
            ("disc-053", "Native Android Architecture (Compose)", "android_development", EngineeringDomain.DOMAIN_13_MOBILE, ["mobile-engineer"], ["skill.mobile.android"]),
            ("disc-054", "Cross-Platform Mobile (Flutter/RN)", "cross_platform", EngineeringDomain.DOMAIN_13_MOBILE, ["mobile-engineer"], ["skill.mobile.flutter"]),
            ("disc-055", "Mobile Offline-First Storage & Sync", "offline_sync", EngineeringDomain.DOMAIN_13_MOBILE, ["mobile-engineer"], ["skill.mobile.offline"]),
            ("disc-056", "Desktop Application (Tauri/Electron)", "desktop_architecture", EngineeringDomain.DOMAIN_14_DESKTOP, ["desktop-engineer"], ["skill.desktop.tauri"]),
            ("disc-057", "Multi-Window Lifecycle & Native OS Menus", "os_integration", EngineeringDomain.DOMAIN_14_DESKTOP, ["desktop-engineer"], ["skill.desktop.os"]),
            ("disc-058", "Frontend Internationalization (i18n)", "localization", EngineeringDomain.DOMAIN_05_FRONTEND, ["frontend-engineer"], ["skill.frontend.i18n"]),

            # GROUP D — Backend, APIs & Distributed Systems (59–78)
            ("disc-059", "Service Layer & Business Logic Isolation", "service_architecture", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.backend.service"]),
            ("disc-060", "RESTful API Design & OpenAPI / Swagger", "rest_api", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.rest"]),
            ("disc-061", "GraphQL Schema Design & Federation", "graphql", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.graphql"]),
            ("disc-062", "gRPC & Protocol Buffers RPC", "grpc", EngineeringDomain.DOMAIN_07_API, ["backend-lead"], ["skill.api.grpc"]),
            ("disc-063", "WebSocket & SSE Real-Time Streaming", "realtime", EngineeringDomain.DOMAIN_07_API, ["backend-lead"], ["skill.api.streaming"]),
            ("disc-064", "Webhook Ingestion & Signature Verification", "webhooks", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.webhooks"]),
            ("disc-065", "API Gateway Routing & Rate Limiting", "gateway", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.gateway"]),
            ("disc-066", "API Versioning & Deprecation Lifecycle", "api_lifecycle", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.lifecycle"]),
            ("disc-067", "Idempotency & Deduplication Keys", "api_lifecycle", EngineeringDomain.DOMAIN_07_API, ["backend-lead"], ["skill.backend.idempotency"]),
            ("disc-068", "Distributed Transactions & Saga Orchestration", "distributed_patterns", EngineeringDomain.DOMAIN_06_BACKEND, ["distributed-systems-architect"], ["skill.dist.saga"]),
            ("disc-069", "Two-Phase Commit & Consensus (Raft/Paxos)", "distributed_patterns", EngineeringDomain.DOMAIN_06_BACKEND, ["distributed-systems-architect"], ["skill.dist.consensus"]),
            ("disc-070", "Distributed Locking & Concurrency Control", "distributed_patterns", EngineeringDomain.DOMAIN_06_BACKEND, ["distributed-systems-architect"], ["skill.dist.locking"]),
            ("disc-071", "Circuit Breaker & Exponential Backoff", "resilience", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.backend.resilience"]),
            ("disc-072", "Outbox Pattern & Reliable Event Publishing", "event_publishing", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.dist.outbox"]),
            ("disc-073", "Background Job Queues & Distributed Schedulers", "job_processing", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.backend.jobs"]),
            ("disc-074", "Multi-Tenant Backend Isolation", "multitenancy", EngineeringDomain.DOMAIN_06_BACKEND, ["principal-architect"], ["skill.backend.multitenant"]),
            ("disc-075", "Service Mesh Integration & Traffic Splitting", "service_mesh", EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, ["cloud-architect"], ["skill.mesh.istio"]),
            ("disc-076", "Standardized Error Handling (RFC 7807)", "api_lifecycle", EngineeringDomain.DOMAIN_07_API, ["api-architect"], ["skill.api.errors"]),
            ("disc-077", "Middleware Pipelines & Interceptor Chains", "service_architecture", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.backend.middleware"]),
            ("disc-078", "Dependency Injection & IoC Containers", "service_architecture", EngineeringDomain.DOMAIN_06_BACKEND, ["backend-lead"], ["skill.backend.di"]),

            # GROUP E — Database, Data Engineering & Storage (79–96)
            ("disc-079", "Relational Data Modeling & Normalization", "relational_db", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.relational"]),
            ("disc-080", "Database Schema Migration & Versioning", "migrations", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.migrations"]),
            ("disc-081", "Query Optimization & Indexing Strategies", "query_optimization", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.indexing"]),
            ("disc-082", "ACID Transaction Boundaries & Isolation", "transactions", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.transactions"]),
            ("disc-083", "Document & Key-Value NoSQL Modeling", "nosql_db", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.nosql"]),
            ("disc-084", "Columnar & Data Warehousing Storage", "data_warehousing", EngineeringDomain.DOMAIN_08_DATABASE, ["data-platform-architect"], ["skill.data.warehouse"]),
            ("disc-085", "Time-Series Data Modeling", "specialized_db", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.timeseries"]),
            ("disc-086", "Graph Database Modeling", "specialized_db", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.graph"]),
            ("disc-087", "Vector Database & Embedding Indexing", "specialized_db", EngineeringDomain.DOMAIN_08_DATABASE, ["ai-systems-architect"], ["skill.db.vector"]),
            ("disc-088", "Read Replica Topologies & Read/Write Splitting", "scalability", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.replicas"]),
            ("disc-089", "Database Sharding & Partitioning Strategies", "scalability", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.sharding"]),
            ("disc-090", "ETL & ELT Batch Data Pipelines", "data_pipelines", EngineeringDomain.DOMAIN_08_DATABASE, ["data-platform-architect"], ["skill.data.etl"]),
            ("disc-091", "Stream Processing & Complex Event Processing", "data_pipelines", EngineeringDomain.DOMAIN_08_DATABASE, ["data-platform-architect"], ["skill.data.streaming"]),
            ("disc-092", "Data Lakehouse Architecture", "data_warehousing", EngineeringDomain.DOMAIN_08_DATABASE, ["data-platform-architect"], ["skill.data.lakehouse"]),
            ("disc-093", "Data Governance, Cataloging & Lineage", "data_governance", EngineeringDomain.DOMAIN_08_DATABASE, ["data-platform-architect"], ["skill.data.lineage"]),
            ("disc-094", "Backup, Point-In-Time Recovery & Disaster Plan", "backup_recovery", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.db.backup"]),
            ("disc-095", "Data Retention, Archival & Pruning Lifecycle", "data_governance", EngineeringDomain.DOMAIN_08_DATABASE, ["database-engineer"], ["skill.data.retention"]),
            ("disc-096", "Data Masking & PII Pseudonymization", "data_security", EngineeringDomain.DOMAIN_08_DATABASE, ["security-engineer", "database-engineer"], ["skill.data.masking"]),

            # GROUP F — AI, Machine Learning & Agentic Systems (97–114)
            ("disc-097", "Foundation Model Evaluation & Selection", "model_selection", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.models"]),
            ("disc-098", "Retrieval-Augmented Generation (RAG) Architecture", "rag_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.rag"]),
            ("disc-099", "Chunking, Document Embedding & Semantic Search", "rag_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.embeddings"]),
            ("disc-100", "Prompt Engineering & Versioning", "prompt_engineering", EngineeringDomain.DOMAIN_11_AI, ["prompt-engineer"], ["skill.ai.prompt"]),
            ("disc-101", "Autonomous Agent Design (ReAct/Plan-Solve)", "agent_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.agents"]),
            ("disc-102", "Multi-Agent Orchestration & Swarm Coordination", "agent_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.swarms"]),
            ("disc-103", "Model Context Protocol (MCP) Server/Client", "agent_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.mcp"]),
            ("disc-104", "Deterministic Tool Calling & Schema Validation", "agent_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.tools"]),
            ("disc-105", "Agent Memory Hierarchies (OMIS)", "memory_systems", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.memory"]),
            ("disc-106", "Model Fine-Tuning & PEFT (LoRA/QLoRA)", "model_training", EngineeringDomain.DOMAIN_11_AI, ["mlops-engineer"], ["skill.ai.finetuning"]),
            ("disc-107", "Model Quantization & Local Serving", "model_serving", EngineeringDomain.DOMAIN_11_AI, ["mlops-engineer"], ["skill.ai.quantization"]),
            ("disc-108", "LLM Evaluation Frameworks & Benchmark Scoring", "model_evaluation", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.evals"]),
            ("disc-109", "Safety Guardrails & Redaction Filters", "ai_safety", EngineeringDomain.DOMAIN_11_AI, ["security-engineer"], ["skill.ai.safety"]),
            ("disc-110", "AI Cost Management & Token Optimization", "finops", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.tokens"]),
            ("disc-111", "Streaming Responses & SSE Delivery", "model_serving", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.streaming"]),
            ("disc-112", "Human-in-the-Loop (HITL) Approval Gates", "ai_governance", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.hitl"]),
            ("disc-113", "MLOps Pipelines & Model Monitoring", "mlops", EngineeringDomain.DOMAIN_11_AI, ["mlops-engineer"], ["skill.ai.mlops"]),
            ("disc-114", "Agentic Self-Reflection & Multi-Turn Loops", "agent_architecture", EngineeringDomain.DOMAIN_11_AI, ["ai-systems-architect"], ["skill.ai.reflection"]),

            # GROUP G — Security, Compliance & Identity (115–128)
            ("disc-115", "Zero Trust Architecture & Least Privilege", "security_architecture", EngineeringDomain.DOMAIN_12_SECURITY, ["security-architect"], ["skill.sec.zerotrust"]),
            ("disc-116", "STRIDE Threat Vector Modeling", "threat_modeling", EngineeringDomain.DOMAIN_12_SECURITY, ["security-architect"], ["skill.sec.stride"]),
            ("disc-117", "Identity & Access Management (OAuth2/OIDC)", "identity_access", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.iam"]),
            ("disc-118", "Role-Based & Attribute-Based Access Control", "identity_access", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.rbac"]),
            ("disc-119", "Secrets Management & Key Rotation (Vault/KMS)", "secrets_management", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.secrets"]),
            ("disc-120", "Cryptographic Architecture & Hashing", "cryptography", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.crypto"]),
            ("disc-121", "OWASP Top 10 Application Security Hardening", "appsec", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.owasp"]),
            ("disc-122", "OWASP API Security Top 10 Hardening", "appsec", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.apiowasp"]),
            ("disc-123", "Software Supply-Chain Security & SBOM", "appsec", EngineeringDomain.DOMAIN_12_SECURITY, ["security-engineer"], ["skill.sec.sbom"]),
            ("disc-124", "Tamper-Evident Cryptographic Ledger Hashing", "ledger_governance", EngineeringDomain.DOMAIN_23_GOVERNANCE, ["compliance-officer"], ["skill.gov.ledger"]),
            ("disc-125", "SOC 2 Type II Compliance Architecture", "compliance", EngineeringDomain.DOMAIN_23_GOVERNANCE, ["compliance-officer"], ["skill.gov.soc2"]),
            ("disc-126", "HIPAA Health Information Privacy Controls", "compliance", EngineeringDomain.DOMAIN_23_GOVERNANCE, ["compliance-officer"], ["skill.gov.hipaa"]),
            ("disc-127", "GDPR / CCPA Data Subject Access & Deletion", "compliance", EngineeringDomain.DOMAIN_23_GOVERNANCE, ["compliance-officer"], ["skill.gov.gdpr"]),
            ("disc-128", "PCI-DSS Cardholder Data Isolation", "compliance", EngineeringDomain.DOMAIN_23_GOVERNANCE, ["compliance-officer"], ["skill.gov.pcidss"]),

            # GROUP H — Infrastructure, DevOps, SRE & Observability (129–144)
            ("disc-129", "OCI Containerization & Dockerfile Optimization", "containers", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.docker"]),
            ("disc-130", "Container Orchestration & Kubernetes Topologies", "orchestration", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.k8s"]),
            ("disc-131", "Infrastructure as Code (Terraform / Pulumi)", "iac", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.terraform"]),
            ("disc-132", "CI Pipelines & Deterministic Builds", "ci_cd", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.ci"]),
            ("disc-133", "CD Pipelines & GitOps (ArgoCD)", "ci_cd", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.cd"]),
            ("disc-134", "Blue-Green & Progressive Canary Rollouts", "release_engineering", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["devops-lead"], ["skill.infra.rollout"]),
            ("disc-135", "Three Pillars of Observability (Metrics, Logs, Traces)", "observability", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.telemetry"]),
            ("disc-136", "OpenTelemetry (OTel) Instrumentation", "observability", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.otel"]),
            ("disc-137", "Service Level Objectives (SLO) & Error Budgets", "sre_practices", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.slo"]),
            ("disc-138", "Distributed Alerting & Escalation Policies", "incident_management", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.alerting"]),
            ("disc-139", "Chaos Engineering & Fault Injection", "resilience_testing", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.chaos"]),
            ("disc-140", "SRE Incident Runbooks & Blameless Postmortems", "incident_management", EngineeringDomain.DOMAIN_17_RELIABILITY, ["sre-lead"], ["skill.sre.runbooks"]),
            ("disc-141", "Cloud Cost Optimization (FinOps) & Quotas", "finops", EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY, ["cloud-architect"], ["skill.cloud.finops"]),
            ("disc-142", "DNS, CDN, Edge Caching & Anycast Routing", "networking", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["cloud-architect"], ["skill.infra.cdn"]),
            ("disc-143", "VPC, Subnets & Network Security Groups", "networking", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["cloud-architect"], ["skill.infra.vpc"]),
            ("disc-144", "Zero-Downtime Database Migration Strategies", "database_ops", EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, ["database-engineer", "devops-lead"], ["skill.db.zerodowntime"]),

            # GROUP I — Quality, Reverse Engineering & Harness Governance (145–155)
            ("disc-145", "Testing Pyramid Formulation", "test_strategy", EngineeringDomain.DOMAIN_16_QUALITY, ["qa-lead"], ["skill.qa.pyramid"]),
            ("disc-146", "Property-Based Testing & Fuzz Testing", "test_automation", EngineeringDomain.DOMAIN_16_QUALITY, ["qa-lead"], ["skill.qa.fuzz"]),
            ("disc-147", "Mutation Testing & Test Quality Assessment", "test_automation", EngineeringDomain.DOMAIN_16_QUALITY, ["qa-lead"], ["skill.qa.mutation"]),
            ("disc-148", "Contract Testing (Pact / Consumer-Driven)", "test_automation", EngineeringDomain.DOMAIN_16_QUALITY, ["qa-lead"], ["skill.qa.contract"]),
            ("disc-149", "Deterministic Test Sandboxes & Ephemeral Mocks", "test_environments", EngineeringDomain.DOMAIN_16_QUALITY, ["qa-lead"], ["skill.qa.sandboxes"]),
            ("disc-150", "Static Code Analysis, AST Linting & Complexity", "code_analysis", EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING, ["reverse-engineer"], ["skill.code.ast"]),
            ("disc-151", "Legacy Codebase Architecture Reconstruction", "architecture_recovery", EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING, ["reverse-engineer"], ["skill.reverse.arch"]),
            ("disc-152", "Dependency Vulnerability & Tech Debt Quantification", "technical_debt", EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING, ["reverse-engineer"], ["skill.reverse.debt"]),
            ("disc-153", "Execution Harness Planning & Sandbox Boundaries", "harness_planning", EngineeringDomain.DOMAIN_18_HARNESS, ["harness-engineer"], ["skill.harness.sandbox"]),
            ("disc-154", "Autonomous Engineering Loop Lifecycle Planning", "loop_governance", EngineeringDomain.DOMAIN_19_LOOP, ["loop-architect"], ["skill.loop.lifecycle"]),
            ("disc-155", "Technology Radar, Version Lifecycle & Trade-Offs", "tech_radar", EngineeringDomain.DOMAIN_22_TECHNOLOGY_INTELLIGENCE, ["tech-lead"], ["skill.tech.radar"]),
        ]

        for item in raw_catalogue:
            disc_id, name, subdomain, domain, roles, skills = item
            slug = name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-")
            desc = DisciplineDescriptor(
                discipline_id=disc_id,
                name=name,
                slug=slug,
                domain=domain,
                subdomain=subdomain,
                description=f"Standard engineering discipline for {name} within {domain.value}.",
                objectives=[f"Deliver rigorous engineering excellence in {name}."],
                key_roles=roles,
                key_skills=skills,
            )
            self.register_discipline(desc)
