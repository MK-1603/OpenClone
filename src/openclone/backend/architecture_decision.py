"""Backend Architecture Decision Engine for OpenClone.

Recommends the smallest trustworthy architecture satisfying functional requirements
and operational constraints without introducing premature complexity.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkloadProfile:
    """Operational profile defining scale, concurrency, and compliance constraints."""
    project_name: str
    archetype: str
    expected_daily_active_users: int = 1000
    peak_writes_per_second: float = 10.0
    peak_reads_per_second: float = 50.0
    data_volume_gb: float = 20.0
    tenant_model: str = "single_tenant"  # single_tenant, shared_database_rls, schema_per_tenant, database_per_tenant
    requires_realtime: bool = False
    requires_offline: bool = False
    compliance_requirements: List[str] = field(default_factory=list)
    existing_stack: Optional[str] = None


@dataclass
class ArchitectureDecision:
    """Structured architectural blueprint recommendation with explicit trade-offs."""
    project_name: str
    pattern: str  # Modular Monolith, Layered Service, Microservices, Serverless, Edge
    framework: str
    runtime: str
    database: str
    orm_strategy: str
    migration_strategy: str
    cache_strategy: str
    rate_limit_strategy: str
    async_strategy: str
    observability_strategy: str
    deployment_model: str
    rationale: List[str] = field(default_factory=list)
    trade_offs: List[str] = field(default_factory=list)
    operational_complexity: str = "LOW"  # LOW, MODERATE, HIGH
    cost_tier: str = "LOW"  # LOW, MODERATE, HIGH
    conditions_for_revisiting: List[str] = field(default_factory=list)


class BackendArchitectureDecisionEngine:
    """Evaluates workload parameters and synthesizes grounded architectural decisions."""

    @classmethod
    def evaluate(cls, profile: WorkloadProfile) -> ArchitectureDecision:
        """Synthesize architecture decision record enforcing minimal sufficient complexity."""
        rationale: List[str] = []
        trade_offs: List[str] = []
        conditions: List[str] = []

        # 1. Architecture Pattern
        # Rule: Microservices only justified when writes > 10,000/sec or data > 5,000 GB
        if profile.peak_writes_per_second > 10000 or profile.data_volume_gb > 5000:
            pattern = "Event-Driven Microservices"
            complexity = "HIGH"
            cost = "HIGH"
            rationale.append("High write concurrency (>10k/sec) and multi-terabyte data volume require horizontally decoupled microservices.")
            trade_offs.append("Increased operational complexity: distributed tracing, network latency, and eventual consistency.")
            conditions.append("Revisit if write traffic normalizes below 2,000 writes/sec.")
        elif profile.requires_offline:
            pattern = "Offline-First Local Core with Cloud Sync"
            complexity = "MODERATE"
            cost = "LOW"
            rationale.append("Offline requirement mandates embedded local database with background state synchronization.")
            trade_offs.append("Conflict resolution logic required for concurrent multi-device updates.")
            conditions.append("Revisit if application transitions to strictly online-only collaboration.")
        elif profile.archetype in ["static_site", "documentation_site", "blog"]:
            pattern = "Jamstack / Static Edge API"
            complexity = "LOW"
            cost = "LOW"
            rationale.append("Read-heavy static content requires edge caching without persistent server infrastructure.")
            trade_offs.append("Dynamic user-generated features require external serverless function integration.")
            conditions.append("Revisit if user authentication or real-time persistence is added.")
        else:
            # Default Canonical Recommendation: Modular Monolith
            pattern = "Modular Monolith"
            complexity = "LOW"
            cost = "LOW"
            rationale.append("Modular Monolith satisfies concurrency requirements (<10k writes/sec) with strong ACID transactions and single deployment pipeline.")
            trade_offs.append("Shared deployment unit requires disciplined package boundaries to prevent tight coupling.")
            conditions.append("Revisit if independent service deployment cadences or extreme write bottlenecks emerge.")

        # 2. Database Choice
        if profile.requires_offline:
            database = "SQLite (Local) + PostgreSQL (Cloud Sync)"
            orm = "Drizzle ORM / SQLite Driver"
        elif profile.archetype in ["static_site", "documentation_site"]:
            database = "Git / Markdown Store (Optional Turso/SQLite for dynamic metrics)"
            orm = "Content Collections / Native Driver"
        elif profile.tenant_model in ["shared_database_rls", "schema_per_tenant", "database_per_tenant"]:
            database = "PostgreSQL (with Row-Level Security)"
            orm = "Prisma / Drizzle ORM (with tenant session scoping)"
            rationale.append("PostgreSQL provides native Row-Level Security (RLS) for multi-tenant data isolation.")
        else:
            database = "PostgreSQL"
            orm = "Prisma / Drizzle ORM"

        # 3. Cache Strategy
        if profile.peak_reads_per_second > 1000 or profile.expected_daily_active_users > 50000:
            cache = "Redis Cache-Aside with Probabilistic Expiration (XFetch)"
            rationale.append("High read load (>1k reads/sec) warrants dedicated Redis cache cluster.")
        else:
            cache = "In-Memory LRU / Database Query Caching"
            rationale.append("Traffic profile does not justify external Redis cluster; in-memory caching minimizes operational cost.")

        # 4. Rate Limiting Strategy
        if profile.archetype in ["saas", "api_platform", "enterprise_application"]:
            rate_limit = "Tiered Sliding Window Counter (Per-IP for Auth, Per-API-Key for Endpoints, Per-Tenant for Background)"
        else:
            rate_limit = "Token Bucket (Per-IP on Auth/Write Endpoints)"

        # 5. Asynchronous Processing Strategy
        if profile.peak_writes_per_second > 1000:
            async_strat = "Kafka / RabbitMQ Event Broker with Transactional Outbox"
        elif profile.requires_realtime:
            async_strat = "Redis Streams / WebSockets with Worker Pool"
        else:
            async_strat = "Database-Backed Transactional Queue (e.g. pg-boss or Celery/BullMQ)"
            rationale.append("Database-backed job queue eliminates separate broker infrastructure while guaranteeing transactional consistency.")

        # 6. Observability
        observability = "Structured JSON Logging (with trace_id) + Prometheus Golden Signals + OTel Trace Hooks"

        # 7. Deployment Model
        if profile.requires_offline:
            deployment = "Mobile/Desktop Client + Cloud Sync API Container"
        elif profile.archetype in ["static_site", "landing_page"]:
            deployment = "Global Edge CDN (Cloudflare / Vercel)"
        elif profile.peak_writes_per_second > 5000:
            deployment = "Containerized Kubernetes Cluster (EKS/GKE) with Horizontal Pod Autoscaling"
        else:
            deployment = "Containerized Service (Docker / Cloud Run / AWS ECS) with Managed Database"
            rationale.append("Containerized PaaS/Cloud Run provides effortless auto-scaling and automated TLS without Kubernetes overhead.")

        return ArchitectureDecision(
            project_name=profile.project_name,
            pattern=pattern,
            framework="Next.js / Node.js (or FastAPI for Python services)",
            runtime="Node.js 22 LTS / Python 3.12+",
            database=database,
            orm_strategy=orm,
            migration_strategy="Version-Controlled Forward Migrations with Expand-and-Contract",
            cache_strategy=cache,
            rate_limit_strategy=rate_limit,
            async_strategy=async_strat,
            observability_strategy=observability,
            deployment_model=deployment,
            rationale=rationale,
            trade_offs=trade_offs,
            operational_complexity=complexity,
            cost_tier=cost,
            conditions_for_revisiting=conditions,
        )
