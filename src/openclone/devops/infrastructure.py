"""OpenClone Infrastructure Recommendation Engine.

Analyzes application blueprints to recommend optimal frontend hosting, backend compute,
databases, storage, CDN, and monitoring providers with strict adherence to Zero-Invention rules.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.devops.models import InfrastructureRecommendation, ProviderCategory, ConnectionStatus
from src.openclone.devops.accounts import AccountConnectionManager


class InfrastructureIntelligenceEngine:
    """Generates evidence-backed infrastructure recommendations based on project stack."""

    @classmethod
    def evaluate_infrastructure(
        cls,
        frontend_framework: str = "Next.js",
        backend_framework: str = "FastAPI",
        database_engine: str = "PostgreSQL",
        has_file_uploads: bool = False,
        requires_caching: bool = True,
    ) -> List[InfrastructureRecommendation]:
        account_mgr = AccountConnectionManager()
        recommendations: List[InfrastructureRecommendation] = []

        # 1. Frontend Hosting
        vercel_conn = account_mgr.get_connection_by_provider("vercel")
        recommendations.append(InfrastructureRecommendation(
            component_name="Frontend Web Application",
            category=ProviderCategory.FRONTEND_HOSTING,
            recommended_provider="Vercel",
            alternative_provider="Cloudflare Pages",
            rationale="Native SSR/ISR optimization, global edge CDN, and zero-config deployment.",
            framework_compatibility=f"Optimal for {frontend_framework}",
            estimated_cost_tier="Hobby (Free) / Pro ($20/mo)",
            region_options=["iad1 (US East)", "sfo1 (US West)", "fra1 (EU Frankfurt)"],
            connection_status=vercel_conn.status if vercel_conn else ConnectionStatus.NOT_CONNECTED,
        ))

        # 2. Backend Hosting
        render_conn = account_mgr.get_connection_by_provider("render")
        recommendations.append(InfrastructureRecommendation(
            component_name="Backend API & Worker Services",
            category=ProviderCategory.BACKEND_HOSTING,
            recommended_provider="Render",
            alternative_provider="Railway",
            rationale="Managed web services with automated SSL, private networking, and background job support.",
            framework_compatibility=f"Native Docker & {backend_framework} support",
            estimated_cost_tier="Starter ($7/mo) / Standard ($25/mo)",
            region_options=["us-east (Ohio)", "us-west (Oregon)", "eu-central (Frankfurt)"],
            connection_status=render_conn.status if render_conn else ConnectionStatus.NOT_CONNECTED,
        ))

        # 3. Database Engine
        neon_conn = account_mgr.get_connection_by_provider("neon")
        recommendations.append(InfrastructureRecommendation(
            component_name="Primary Database",
            category=ProviderCategory.DATABASE,
            recommended_provider="Neon Serverless PostgreSQL",
            alternative_provider="Supabase",
            rationale="Instant serverless branching, connection pooling (PgBouncer), and autoscaling compute.",
            framework_compatibility="PostgreSQL 16+ compatible via connection pooling",
            estimated_cost_tier="Free Tier (0.5 GiB) / Launch ($19/mo)",
            region_options=["aws-us-east-1", "aws-us-east-2", "aws-eu-central-1"],
            connection_status=neon_conn.status if neon_conn else ConnectionStatus.NOT_CONNECTED,
        ))

        # 4. Storage & CDN
        if has_file_uploads:
            cf_conn = account_mgr.get_connection_by_provider("cloudflare")
            recommendations.append(InfrastructureRecommendation(
                component_name="Object Storage & File Assets",
                category=ProviderCategory.STORAGE,
                recommended_provider="Cloudflare R2",
                alternative_provider="Supabase Storage",
                rationale="S3-compatible object storage with zero egress fees and global CDN integration.",
                framework_compatibility="Standard AWS S3 SDK compatible",
                estimated_cost_tier="Pay-as-you-go ($0.015/GB-month, $0 egress)",
                region_options=["Automatic Global Distribution"],
                connection_status=cf_conn.status if cf_conn else ConnectionStatus.NOT_CONNECTED,
            ))

        # 5. Caching & Key-Value
        if requires_caching:
            recommendations.append(InfrastructureRecommendation(
                component_name="Cache & Real-time Key-Value",
                category=ProviderCategory.CACHE,
                recommended_provider="Upstash Redis",
                alternative_provider="Render Redis",
                rationale="Serverless REST/RESP Redis with per-request pricing and zero idle cost.",
                framework_compatibility="Standard Redis client compatible",
                estimated_cost_tier="Free Tier (10k commands/day) / Payg ($0.20/100k commands)",
                region_options=["us-east-1", "eu-central-1"],
                connection_status=ConnectionStatus.NOT_CONNECTED,
            ))

        return recommendations
