"""OpenClone 23 Canonical Engineering Domains Taxonomy.

Defines the universal taxonomy of software, AI, and systems engineering disciplines,
mapping cleanly to legacy EIS sectors and framework domains.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class EngineeringDomain(str, enum.Enum):
    DOMAIN_01_PRODUCT = "domain-01-product-engineering"
    DOMAIN_02_REQUIREMENTS = "domain-02-requirements-engineering"
    DOMAIN_03_RESEARCH = "domain-03-research-and-intelligence"
    DOMAIN_04_UX_UI = "domain-04-ux-ui-and-design"
    DOMAIN_05_FRONTEND = "domain-05-frontend-engineering"
    DOMAIN_06_BACKEND = "domain-06-backend-engineering"
    DOMAIN_07_API = "domain-07-api-and-integration"
    DOMAIN_08_DATABASE = "domain-08-database-and-data"
    DOMAIN_09_SOFTWARE_ARCHITECTURE = "domain-09-software-architecture"
    DOMAIN_10_SYSTEM_DESIGN = "domain-10-system-design"
    DOMAIN_11_AI = "domain-11-ai-engineering"
    DOMAIN_12_SECURITY = "domain-12-security-engineering"
    DOMAIN_13_MOBILE = "domain-13-mobile-engineering"
    DOMAIN_14_DESKTOP = "domain-14-desktop-engineering"
    DOMAIN_15_INFRASTRUCTURE = "domain-15-infrastructure-and-devops"
    DOMAIN_16_QUALITY = "domain-16-quality-engineering"
    DOMAIN_17_RELIABILITY = "domain-17-reliability-and-sre"
    DOMAIN_18_HARNESS = "domain-18-harness-engineering"
    DOMAIN_19_LOOP = "domain-19-loop-engineering"
    DOMAIN_20_REVERSE_ENGINEERING = "domain-20-reverse-engineering"
    DOMAIN_21_PROJECT_DELIVERY = "domain-21-project-and-delivery"
    DOMAIN_22_TECHNOLOGY_INTELLIGENCE = "domain-22-technology-intelligence"
    DOMAIN_23_GOVERNANCE = "domain-23-governance-engineering"


@dataclass
class DomainDescriptor:
    domain_id: EngineeringDomain
    code: str
    name: str
    category: str
    description: str
    subdomains: List[str] = field(default_factory=list)
    key_roles: List[str] = field(default_factory=list)
    legacy_eis_sector: Optional[str] = None
    legacy_framework_domain: Optional[str] = None


class EngineeringDomainRegistry:
    """Master registry of the 23 Canonical Engineering Domains."""

    _instance: Optional["EngineeringDomainRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.domains: Dict[EngineeringDomain, DomainDescriptor] = {}
        self._populate_canonical_domains()
        self._initialized = True

    def _populate_canonical_domains(self) -> None:
        descriptors = [
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_01_PRODUCT,
                code="DOM-01",
                name="Product Engineering",
                category="Strategy & Requirements",
                description="Product discovery, product vision, market validation, user personas, MVP definition, feature prioritization.",
                subdomains=["product_discovery", "feature_engineering", "roadmapping", "product_metrics"],
                key_roles=["principal-architect", "product-manager", "business-analyst"],
                legacy_eis_sector="EIS-15",
                legacy_framework_domain="04-PRODUCT-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_02_REQUIREMENTS,
                code="DOM-02",
                name="Requirements Engineering",
                category="Strategy & Requirements",
                description="Requirements elicitation, Socratic clarification, user stories, acceptance criteria, non-functional requirements.",
                subdomains=["elicitation", "analysis", "specification", "traceability", "validation"],
                key_roles=["requirements-engineer", "business-analyst"],
                legacy_eis_sector="EIS-01",
                legacy_framework_domain="03-REQUIREMENTS-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_03_RESEARCH,
                code="DOM-03",
                name="Research and Intelligence Engineering",
                category="Discovery & Intelligence",
                description="Technical research, feasibility studies, competitor benchmarking, source evaluation, research synthesis.",
                subdomains=["feasibility", "benchmarking", "evidence_evaluation", "synthesis"],
                key_roles=["research-engineer", "solution-architect"],
                legacy_eis_sector="EIS-17",
                legacy_framework_domain="02-PROJECT-INTELLIGENCE",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_04_UX_UI,
                code="DOM-04",
                name="UX/UI and Design Engineering",
                category="Experience & Design",
                description="UX research, information architecture, wireframing, design tokens, typography scales, accessibility contrast.",
                subdomains=["ux_research", "design_systems", "design_tokens", "accessibility_design"],
                key_roles=["ux-designer", "ui-designer", "design-system-engineer"],
                legacy_eis_sector="EIS-15",
                legacy_framework_domain="05-UX-UI-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_05_FRONTEND,
                code="DOM-05",
                name="Frontend Engineering",
                category="Application Engineering",
                description="Web application architecture, SPA/SSR/SSG, state management, client routing, frontend security, web performance.",
                subdomains=["rendering_strategies", "state_management", "component_architecture", "web_performance"],
                key_roles=["frontend-engineer", "react-specialist", "vue-specialist"],
                legacy_eis_sector="EIS-03",
                legacy_framework_domain="05-UX-UI-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_06_BACKEND,
                code="DOM-06",
                name="Backend Engineering",
                category="Application Engineering",
                description="Backend service boundaries, modular monoliths, microservices, business logic layers, concurrency, async queues.",
                subdomains=["service_boundaries", "concurrency", "async_processing", "caching_layer"],
                key_roles=["backend-engineer", "api-engineer", "golang-specialist"],
                legacy_eis_sector="EIS-03",
                legacy_framework_domain="08-SOFTWARE-ARCHITECTURE",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_07_API,
                code="DOM-07",
                name="API and Integration Engineering",
                category="Integration & Communication",
                description="REST, OpenAPI 3.1, GraphQL, gRPC, WebSockets, rate limiting, authentication headers, idempotency keys.",
                subdomains=["rest_openapi", "graphql_grpc", "streaming_websockets", "api_gateway"],
                key_roles=["api-engineer", "integration-engineer"],
                legacy_eis_sector="EIS-14",
                legacy_framework_domain="16-API-AND-INTEGRATION-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_08_DATABASE,
                code="DOM-08",
                name="Database and Data Engineering",
                category="Data & Storage",
                description="Relational & NoSQL modeling, schema evolution, zero-downtime migrations, indexing, RLS multi-tenancy, data pipelines.",
                subdomains=["relational_modeling", "nosql_storage", "migrations", "replication_sharding"],
                key_roles=["database-engineer", "data-engineer", "dba-specialist"],
                legacy_eis_sector="EIS-08",
                legacy_framework_domain="15-DATA-AND-DATABASE-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
                code="DOM-09",
                name="Software Architecture",
                category="Architecture & Systems",
                description="Layered architecture, clean architecture, domain-driven design, CQRS, event sourcing, architecture decision records.",
                subdomains=["patterns", "ddd_bounded_contexts", "adrs", "tradeoff_analysis"],
                key_roles=["principal-architect", "enterprise-architect", "solution-architect"],
                legacy_eis_sector="EIS-04",
                legacy_framework_domain="08-SOFTWARE-ARCHITECTURE",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
                code="DOM-10",
                name="System Design",
                category="Architecture & Systems",
                description="High-level & low-level design, quantitative capacity estimation, C4 Mermaid diagrams, distributed systems resilience.",
                subdomains=["capacity_planning", "c4_diagrams", "scalability", "load_balancing"],
                key_roles=["solution-architect", "distributed-systems-engineer"],
                legacy_eis_sector="EIS-04",
                legacy_framework_domain="21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_11_AI,
                code="DOM-11",
                name="AI Engineering",
                category="Intelligent Systems",
                description="Model Intelligence Engine, model routing, prompt engineering, context budgeting, RAG, vector stores, AI agent protocols.",
                subdomains=["model_routing", "prompt_context_budget", "rag_vector_db", "ai_agent_orchestration"],
                key_roles=["ai-engineer", "ml-engineer", "prompt-engineer"],
                legacy_eis_sector="EIS-05",
                legacy_framework_domain="10-AI-AND-MODEL-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_12_SECURITY,
                code="DOM-12",
                name="Security Engineering",
                category="Security & Governance",
                description="STRIDE threat modeling, attack surface analysis, OWASP Top 10, zero-trust boundaries, RBAC/ABAC, secret redaction.",
                subdomains=["threat_modeling", "authn_authz", "secret_management", "appsec_compliance"],
                key_roles=["security-engineer", "appsec-specialist", "threat-modeler"],
                legacy_eis_sector="EIS-11",
                legacy_framework_domain="14-SECURITY-AND-PRIVACY",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_13_MOBILE,
                code="DOM-13",
                name="Mobile Engineering",
                category="Platform Engineering",
                description="Native & cross-platform mobile apps (Flutter, React Native), offline-first sync, push notifications, mobile security.",
                subdomains=["cross_platform", "offline_first", "native_capabilities", "mobile_security"],
                key_roles=["mobile-engineer", "frontend-engineer"],
                legacy_eis_sector="EIS-03",
                legacy_framework_domain="09-PLATFORM-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_14_DESKTOP,
                code="DOM-14",
                name="Desktop Engineering",
                category="Platform Engineering",
                description="Desktop apps (Electron, Tauri), inter-process communication (IPC), OS filesystem sandboxing, auto-updaters.",
                subdomains=["desktop_frameworks", "ipc_architecture", "os_integration", "packagers_installers"],
                key_roles=["desktop-engineer", "platform-engineer"],
                legacy_eis_sector="EIS-03",
                legacy_framework_domain="09-PLATFORM-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
                code="DOM-15",
                name="Infrastructure and DevOps Engineering",
                category="Infrastructure & Operations",
                description="Cloud architecture, containerization (Docker, Kubernetes), CI/CD pipelines, reverse proxies, environment isolation.",
                subdomains=["cloud_architecture", "containers_kubernetes", "cicd_pipelines", "environment_management"],
                key_roles=["devops-engineer", "cloud-architect", "platform-engineer"],
                legacy_eis_sector="EIS-09",
                legacy_framework_domain="18-DEVOPS-AND-CLOUD-ENGINEERING",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_16_QUALITY,
                code="DOM-16",
                name="Quality Engineering",
                category="Verification & Quality",
                description="Test strategy, unit, integration, contract, regression, and security testing, quality gates, Definition of Done.",
                subdomains=["test_strategy", "automated_testing", "quality_gates", "independent_verification"],
                key_roles=["test-engineer", "qa-lead", "independent-verifier"],
                legacy_eis_sector="EIS-12",
                legacy_framework_domain="17-TESTING-AND-VERIFICATION",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_17_RELIABILITY,
                code="DOM-17",
                name="Reliability and SRE",
                category="Infrastructure & Operations",
                description="SLIs, SLOs, SLAs, error budgets, circuit breakers, rate limiting, disaster recovery, fault tolerance.",
                subdomains=["sli_slo_error_budgets", "fault_tolerance", "disaster_recovery", "observability_monitoring"],
                key_roles=["sre-specialist", "devops-engineer"],
                legacy_eis_sector="EIS-13",
                legacy_framework_domain="20-RELIABILITY-AND-OBSERVABILITY",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_18_HARNESS,
                code="DOM-18",
                name="Harness Engineering",
                category="Execution & Control",
                description="Process execution boundaries, command allowlisting, filesystem sandboxing, loopback network controls, evidence capture.",
                subdomains=["process_isolation", "command_allowlisting", "sandbox_boundaries", "evidence_generation"],
                key_roles=["platform-engineer", "security-engineer"],
                legacy_eis_sector="EIS-10",
                legacy_framework_domain="13-HARNESS-AND-EXECUTION",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_19_LOOP,
                code="DOM-19",
                name="Loop Engineering",
                category="Execution & Control",
                description="Agent iteration cycles, bounded repair loops, failure classification, non-self-approving governance, escalation rules.",
                subdomains=["iteration_policy", "repair_loops", "termination_conditions", "governed_escalation"],
                key_roles=["ai-engineer", "orchestrator"],
                legacy_eis_sector="EIS-10",
                legacy_framework_domain="12-ORCHESTRATION-AND-CONTEXT",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING,
                code="DOM-20",
                name="Reverse Engineering",
                category="Discovery & Intelligence",
                description="Static repository inspection, dependency manifests, AST symbols, database schema reconstruction, technical debt scoring.",
                subdomains=["ast_inspection", "dependency_discovery", "route_extraction", "technical_debt_analysis"],
                key_roles=["reverse-engineering-specialist", "solution-architect"],
                legacy_eis_sector="EIS-02",
                legacy_framework_domain="02-PROJECT-INTELLIGENCE",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY,
                code="DOM-21",
                name="Project and Delivery Engineering",
                category="Delivery & Governance",
                description="Work breakdown structures, topological DAG planning, critical path analysis, milestone scheduling, worker allocation.",
                subdomains=["wbs_decomposition", "dag_scheduling", "critical_path", "delivery_validation"],
                key_roles=["principal-architect", "product-manager", "release-manager"],
                legacy_eis_sector="EIS-17",
                legacy_framework_domain="01-METHODOLOGY",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_22_TECHNOLOGY_INTELLIGENCE,
                code="DOM-22",
                name="Technology Intelligence",
                category="Discovery & Intelligence",
                description="Objective multi-criteria evaluation of languages, frameworks, runtimes, and databases with trade-off matrices.",
                subdomains=["stack_evaluation", "maturity_scoring", "tradeoff_analysis", "build_vs_buy"],
                key_roles=["solution-architect", "principal-architect"],
                legacy_eis_sector="EIS-04",
                legacy_framework_domain="06-TECHNOLOGY-INTELLIGENCE",
            ),
            DomainDescriptor(
                domain_id=EngineeringDomain.DOMAIN_23_GOVERNANCE,
                code="DOM-23",
                name="Governance Engineering",
                category="Delivery & Governance",
                description="Hash-chained SQLite ledger, cryptographic approval digests, human-in-the-loop gates, release gate policies.",
                subdomains=["audit_ledger", "approval_digests", "policy_enforcement", "risk_classification"],
                key_roles=["principal-architect", "compliance-auditor", "independent-verifier"],
                legacy_eis_sector="EIS-17",
                legacy_framework_domain="00-GOVERNANCE",
            ),
        ]
        for desc in descriptors:
            self.domains[desc.domain_id] = desc

    def get_domain(self, domain_id: EngineeringDomain) -> Optional[DomainDescriptor]:
        return self.domains.get(domain_id)

    def list_domains(self, category: Optional[str] = None) -> List[DomainDescriptor]:
        if category:
            return [d for d in self.domains.values() if d.category.lower() == category.lower()]
        return list(self.domains.values())

    def resolve_domains_for_project_type(self, project_type: str) -> List[EngineeringDomain]:
        """Determine mandatory and recommended domains for a project archetype."""
        p = project_type.lower()
        base_domains = [
            EngineeringDomain.DOMAIN_01_PRODUCT,
            EngineeringDomain.DOMAIN_02_REQUIREMENTS,
            EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
            EngineeringDomain.DOMAIN_16_QUALITY,
            EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY,
            EngineeringDomain.DOMAIN_22_TECHNOLOGY_INTELLIGENCE,
            EngineeringDomain.DOMAIN_23_GOVERNANCE,
        ]

        if any(k in p for k in ["saas", "web", "platform", "portal", "dashboard"]):
            base_domains.extend([
                EngineeringDomain.DOMAIN_04_UX_UI,
                EngineeringDomain.DOMAIN_05_FRONTEND,
                EngineeringDomain.DOMAIN_06_BACKEND,
                EngineeringDomain.DOMAIN_07_API,
                EngineeringDomain.DOMAIN_08_DATABASE,
                EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
                EngineeringDomain.DOMAIN_12_SECURITY,
                EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
                EngineeringDomain.DOMAIN_17_RELIABILITY,
            ])
        if any(k in p for k in ["ai", "rag", "agent", "llm", "ml"]):
            base_domains.extend([
                EngineeringDomain.DOMAIN_11_AI,
                EngineeringDomain.DOMAIN_19_LOOP,
            ])
        if any(k in p for k in ["mobile", "ios", "android", "flutter", "react native"]):
            base_domains.extend([
                EngineeringDomain.DOMAIN_13_MOBILE,
                EngineeringDomain.DOMAIN_04_UX_UI,
                EngineeringDomain.DOMAIN_07_API,
            ])
        if any(k in p for k in ["desktop", "electron", "tauri"]):
            base_domains.extend([
                EngineeringDomain.DOMAIN_14_DESKTOP,
                EngineeringDomain.DOMAIN_04_UX_UI,
            ])
        if any(k in p for k in ["refactor", "legacy", "audit", "evolution", "reverse"]):
            base_domains.extend([
                EngineeringDomain.DOMAIN_20_REVERSE_ENGINEERING,
            ])

        return list(set(base_domains))
