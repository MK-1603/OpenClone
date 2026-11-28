"""System Design Decision Engine & ADR Generator.

Evaluates quality attributes, system boundaries, traffic constraints, and operational
limits to recommend minimal effective architectures and generate formal ADRs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class QualityAttributes:
    """Explicitly weighted architectural quality attributes."""
    availability_target: str = "99.9%"  # 99.0%, 99.9%, 99.99%
    max_p99_latency_ms: float = 200.0
    consistency_model: str = "strong"  # strong, eventual, causal
    scalability_tier: str = "medium"    # low (<1k rps), medium (<10k rps), high (>10k rps)
    auditability: str = "high"          # standard, high, regulated
    cost_sensitivity: str = "medium"    # low, medium, high


@dataclass
class SystemRequirements:
    """Requirements profile passed to the decision engine."""
    project_name: str
    functional_summary: str
    peak_rps: float
    total_data_gb: float
    multi_tenant: bool = False
    real_time_updates: bool = False
    requires_offline_sync: bool = False
    requires_event_sourcing: bool = False
    quality_attributes: QualityAttributes = field(default_factory=QualityAttributes)


@dataclass
class ArchitectureRecommendation:
    """Result of architectural trade-off evaluation."""
    primary_pattern: str  # Modular Monolith, Layered Monolith, Microservices, Event-Driven
    rationale: str
    code_pattern: str     # Hexagonal (Ports & Adapters), Clean Architecture, Layered
    database_tier: str    # Single Primary PostgreSQL, Primary-Replica, Distributed CockroachDB/Spanner
    caching_tier: str     # In-Process Cache, Redis Cache-Aside, None
    queue_tier: str       # PostgreSQL SKIP LOCKED / Transactional Outbox, Redis Streams, Kafka/RabbitMQ
    real_time_tier: str   # Server-Sent Events (SSE), WebSockets, Long-Polling, None
    operational_complexity: str  # Low, Medium, High
    warnings: List[str] = field(default_factory=list)
    alternatives_considered: List[str] = field(default_factory=list)


class SystemDesignDecisionEngine:
    """Evaluates constraints and enforces the Monolith-First Rule."""

    def evaluate(self, req: SystemRequirements) -> ArchitectureRecommendation:
        warnings = []
        alternatives = []

        # 1. Determine Primary Architecture Pattern
        if req.requires_offline_sync:
            primary_pattern = "Offline-First Client-Server Architecture"
            rationale = "Offline sync requirements dictate local embedded storage (SQLite) with CRDT or timestamp-based bidirectional sync."
            code_pattern = "Hexagonal Architecture (Ports & Adapters with Sync Boundary)"
            database_tier = "SQLite Embedded on Client + PostgreSQL Sync Master"
            caching_tier = "In-Process LRU Cache"
            queue_tier = "Local SQLite Outbox + Sync Queue"
            real_time_tier = "Server-Sent Events (SSE) for Sync Triggers" if req.real_time_updates else "None"
            operational_complexity = "Medium"
            alternatives = ["Cloud-only Web App (rejected due to offline requirement)"]

        elif req.peak_rps > 10_000 and req.total_data_gb > 10_000:
            primary_pattern = "Event-Driven Distributed Microservices"
            rationale = (
                f"Peak load of {req.peak_rps:,.0f} RPS and {req.total_data_gb:,.0f} GB exceeds single-instance "
                "database and application vertical scaling boundaries. Domain-separated microservices are justified."
            )
            code_pattern = "Domain-Driven Design (Bounded Contexts with Hexagonal Ports)"
            database_tier = "Polyglot Distributed Databases (PostgreSQL Sharded + Redis)"
            caching_tier = "Redis Cluster with XFetch Stampede Prevention"
            queue_tier = "Distributed Message Broker (Kafka or AWS SQS) with Transactional Outbox"
            real_time_tier = "WebSocket Cluster behind Load Balancer" if req.real_time_updates else "None"
            operational_complexity = "High"
            warnings.append("Distributed architectures require distributed tracing, correlation IDs, and automated circuit breakers.")
            alternatives = ["Modular Monolith (rejected: exceeds single-database write throughput)"]

        elif req.peak_rps > 1_000 or req.total_data_gb > 1_000:
            primary_pattern = "Modular Monolith with Read Replicas & Cache-Aside"
            rationale = (
                f"Peak load of {req.peak_rps:,.0f} RPS and {req.total_data_gb:,.0f} GB is efficiently handled by a "
                "Modular Monolith utilizing a primary relational database with read replicas and Redis cache-aside."
            )
            code_pattern = "Clean Architecture / Hexagonal Architecture"
            database_tier = "PostgreSQL Primary-Replica Topology with Connection Pooling (PgBouncer)"
            caching_tier = "Redis Cache-Aside with probabilistic early expiration (XFetch)"
            queue_tier = "Redis Streams / Celery with Dead-Letter Queue (DLQ)"
            real_time_tier = "WebSockets with Redis Pub/Sub adapter" if req.real_time_updates else "None"
            operational_complexity = "Medium"
            alternatives = ["Microservices (rejected: unnecessary network boundaries, IPC overhead, and operational cost)"]

        else:
            primary_pattern = "Modular Monolith (Monolith-First Standard)"
            rationale = (
                f"Moderate load ({req.peak_rps:,.0f} RPS, {req.total_data_gb:,.0f} GB) is best served by a single "
                "deployable Modular Monolith. Delivers zero IPC latency, ACID transactions, simple CI/CD, and lowest TCO."
            )
            code_pattern = "Layered Architecture with strict internal package boundaries"
            database_tier = "Single PostgreSQL Instance with Automated WAL Backups & Connection Pooling"
            caching_tier = "In-Process Memory Cache (or single Redis instance if multi-worker)"
            queue_tier = "PostgreSQL Transactional Outbox / Background Job Worker (e.g. pg-boss or Celery)"
            real_time_tier = "Server-Sent Events (SSE)" if req.real_time_updates else "None"
            operational_complexity = "Low"
            alternatives = [
                "Microservices (rejected per OpenClone Monolith-First Rule; premature decomposition)",
                "Serverless functions (rejected: cold start latency and database connection exhaustion risk)",
            ]

        if req.multi_tenant:
            warnings.append("Multi-tenant isolation required: Enforce Row-Level Security (RLS) and tenant-prefixed cache keys.")

        return ArchitectureRecommendation(
            primary_pattern=primary_pattern,
            rationale=rationale,
            code_pattern=code_pattern,
            database_tier=database_tier,
            caching_tier=caching_tier,
            queue_tier=queue_tier,
            real_time_tier=real_time_tier,
            operational_complexity=operational_complexity,
            warnings=warnings,
            alternatives_considered=alternatives,
        )


class ADRGenerator:
    """Generates standardized Architecture Decision Record documents."""

    @staticmethod
    def generate_adr(
        adr_id: str,
        title: str,
        req: SystemRequirements,
        rec: ArchitectureRecommendation,
    ) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        lines = [
            f"# ADR-{adr_id}: {title}",
            "",
            "## Metadata",
            f"- **Status:** APPROVED",
            f"- **Date:** {date_str}",
            f"- **Project:** {req.project_name}",
            f"- **Decision Maker:** OpenClone System Design Intelligence Engine",
            "",
            "## 1. Context & Problem Statement",
            f"{req.functional_summary}",
            "",
            "### Workload Constraints",
            f"- **Peak Concurrency / RPS:** {req.peak_rps:,.0f} req/s",
            f"- **Storage Volume:** {req.total_data_gb:,.0f} GB",
            f"- **Multi-Tenancy:** {'Yes (Strict Isolation)' if req.multi_tenant else 'No'}",
            f"- **Real-time Requirements:** {'Yes' if req.real_time_updates else 'No'}",
            f"- **Availability Target:** {req.quality_attributes.availability_target}",
            f"- **Target Max Latency (p99):** {req.quality_attributes.max_p99_latency_ms} ms",
            "",
            "## 2. Decision Outcome",
            f"**Chosen Architecture:** `{rec.primary_pattern}`",
            "",
            f"**Rationale:** {rec.rationale}",
            "",
            "### Component Specifications",
            f"- **Code Organization:** {rec.code_pattern}",
            f"- **Database Architecture:** {rec.database_tier}",
            f"- **Caching Tier:** {rec.caching_tier}",
            f"- **Asynchronous & Queue Tier:** {rec.queue_tier}",
            f"- **Real-time Communication:** {rec.real_time_tier}",
            f"- **Operational Complexity Score:** {rec.operational_complexity}",
            "",
            "## 3. Considered Alternatives",
        ]
        for alt in rec.alternatives_considered:
            lines.append(f"- {alt}")

        lines.extend([
            "",
            "## 4. Consequences & Trade-offs",
            "### Positive Consequences",
            "- Minimal operational footprint and deterministic failure domains.",
            "- High engineering velocity through unified codebase and shared testing harness.",
            "- Strong data consistency guaranteed by ACID database boundaries.",
            "",
            "### Negative Consequences & Mitigation",
            "- Resource contention must be managed via database connection pooling.",
            "- Long-running background jobs must be strictly delegated to asynchronous queues.",
            "",
            "## 5. Governance & Revisit Triggers",
            "- If peak write throughput exceeds 10,000 WPS consistently for 14 days.",
            "- If independent team organizational scaling creates unresolvable release merge conflicts.",
        ])

        if rec.warnings:
            lines.extend(["", "## 6. Critical Security & Engineering Warnings"])
            for w in rec.warnings:
                lines.append(f"- ⚠️ {w}")

        return "\n".join(lines)
