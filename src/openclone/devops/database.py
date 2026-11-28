"""OpenClone Database Intelligence Engine.

Decouples relational and non-relational database engines from managed hosting providers
(Neon, Supabase, Render PostgreSQL, Railway PostgreSQL, PlanetScale, MongoDB Atlas, Upstash).
Models connection pooling, branching, SSL modes, migration tooling, and zero-invention sizing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from src.openclone.devops.models import DatabaseIntelligenceSpec


@dataclass
class DatabaseProviderProfile:
    provider_id: str
    name: str
    supported_engines: List[str]
    is_serverless: bool
    supports_branching: bool
    connection_pooling_native: bool
    pooling_mechanism: str  # pgbouncer, native_http, none
    default_ssl_mode: str
    recommended_migration_tools: List[str]
    free_tier_limits: str
    pricing_model: str


SUPPORTED_DATABASE_PROVIDERS: Dict[str, DatabaseProviderProfile] = {
    "neon": DatabaseProviderProfile(
        provider_id="neon",
        name="Neon Serverless PostgreSQL",
        supported_engines=["postgresql"],
        is_serverless=True,
        supports_branching=True,
        connection_pooling_native=True,
        pooling_mechanism="pgbouncer",
        default_ssl_mode="require",
        recommended_migration_tools=["alembic", "prisma", "drizzle"],
        free_tier_limits="0.5 GiB storage, 1 compute branch",
        pricing_model="consumption_based",
    ),
    "supabase": DatabaseProviderProfile(
        provider_id="supabase",
        name="Supabase Managed PostgreSQL",
        supported_engines=["postgresql"],
        is_serverless=False,
        supports_branching=True,
        connection_pooling_native=True,
        pooling_mechanism="supavisor",
        default_ssl_mode="require",
        recommended_migration_tools=["prisma", "drizzle", "supabase_cli"],
        free_tier_limits="500 MB database, 2 free projects",
        pricing_model="tiered",
    ),
    "render_pg": DatabaseProviderProfile(
        provider_id="render_pg",
        name="Render Managed PostgreSQL",
        supported_engines=["postgresql"],
        is_serverless=False,
        supports_branching=False,
        connection_pooling_native=False,
        pooling_mechanism="none",
        default_ssl_mode="require",
        recommended_migration_tools=["alembic", "prisma"],
        free_tier_limits="1 GB storage (expires after 90 days on free tier)",
        pricing_model="instance_based",
    ),
    "railway_pg": DatabaseProviderProfile(
        provider_id="railway_pg",
        name="Railway Managed PostgreSQL",
        supported_engines=["postgresql"],
        is_serverless=False,
        supports_branching=False,
        connection_pooling_native=False,
        pooling_mechanism="none",
        default_ssl_mode="require",
        recommended_migration_tools=["alembic", "prisma"],
        free_tier_limits="$5 monthly usage credit",
        pricing_model="usage_based",
    ),
    "planetscale": DatabaseProviderProfile(
        provider_id="planetscale",
        name="PlanetScale Vitess MySQL",
        supported_engines=["mysql"],
        is_serverless=True,
        supports_branching=True,
        connection_pooling_native=True,
        pooling_mechanism="vitess_vtgate",
        default_ssl_mode="verify-ca",
        recommended_migration_tools=["prisma", "drizzle"],
        free_tier_limits="Paid only / trial tier",
        pricing_model="consumption_based",
    ),
}


class DatabaseIntelligenceEngine:
    """Evaluates data layer requirements and couples engines to managed providers."""

    @classmethod
    def analyze_database_requirements(
        cls,
        engine: str = "postgresql",
        expected_concurrency: str = "moderate",
        requires_branching: bool = True,
        preferred_orm: str = "prisma",
        is_serverless_compute: bool = True,
    ) -> DatabaseIntelligenceSpec:
        engine_lower = engine.lower()
        is_relational = engine_lower in ("postgresql", "postgres", "mysql", "sqlite")

        if engine_lower in ("postgresql", "postgres"):
            if is_serverless_compute or requires_branching:
                recommended = "neon"
                alternative = "supabase"
            else:
                recommended = "render_pg"
                alternative = "railway_pg"
            conn_pooling = True
            branching = True if recommended in ("neon", "supabase") else False
            migration_tool = preferred_orm if preferred_orm in ("prisma", "drizzle", "alembic") else "alembic"

        elif engine_lower == "mysql":
            recommended = "planetscale"
            alternative = "railway_pg"
            conn_pooling = True
            branching = True
            migration_tool = "prisma"

        else:
            # Fallback for lightweight / embedded
            recommended = "sqlite_local"
            alternative = "turso"
            conn_pooling = False
            branching = False
            migration_tool = "alembic"

        return DatabaseIntelligenceSpec(
            engine_type=engine_lower,
            is_relational=is_relational,
            recommended_provider=recommended,
            alternative_provider=alternative,
            connection_pooling_required=conn_pooling,
            supports_branching=branching,
            migration_tool=migration_tool,
            ssl_mode="require",
            estimated_storage_gb="NOT_ESTIMATED",  # Enforce Zero-Invention Rule
        )

    @classmethod
    def get_provider_profile(cls, provider_id: str) -> Optional[DatabaseProviderProfile]:
        return SUPPORTED_DATABASE_PROVIDERS.get(provider_id.lower())
