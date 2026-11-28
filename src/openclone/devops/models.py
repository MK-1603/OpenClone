"""OpenClone Universal DevOps, Infrastructure & Deployment Intelligence Data Models.

Defines schemas for connected accounts, infrastructure recommendations, database providers,
deployment adapters, 21-state deployment state machine, and environment variables.
"""
from __future__ import annotations

import enum
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


class ProviderCategory(str, enum.Enum):
    SOURCE_CONTROL = "SOURCE_CONTROL"
    FRONTEND_HOSTING = "FRONTEND_HOSTING"
    BACKEND_HOSTING = "BACKEND_HOSTING"
    DATABASE = "DATABASE"
    STORAGE = "STORAGE"
    CACHE = "CACHE"
    DNS_CDN = "DNS_CDN"
    MONITORING = "MONITORING"
    EMAIL = "EMAIL"
    PAYMENTS = "PAYMENTS"


class ConnectionStatus(str, enum.Enum):
    NOT_CONNECTED = "NOT_CONNECTED"
    AUTHORIZATION_PENDING = "AUTHORIZATION_PENDING"
    CONNECTED = "CONNECTED"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    LIMITED_PERMISSIONS = "LIMITED_PERMISSIONS"
    EXPIRED = "EXPIRED"
    REAUTH_REQUIRED = "REAUTH_REQUIRED"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"


class ProviderMaturity(str, enum.Enum):
    PROPOSED = "PROPOSED"
    SPECIFIED = "SPECIFIED"
    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    VERIFIED = "VERIFIED"
    DEGRADED = "DEGRADED"
    UNSUPPORTED = "UNSUPPORTED"


class DeploymentState(str, enum.Enum):
    """Canonical 21-state deployment state machine."""
    NOT_ANALYZED = "NOT_ANALYZED"
    ANALYZED = "ANALYZED"
    DEPLOYMENT_PLAN_READY = "DEPLOYMENT_PLAN_READY"
    AWAITING_CONFIGURATION = "AWAITING_CONFIGURATION"
    AWAITING_PROVIDER_CONNECTION = "AWAITING_PROVIDER_CONNECTION"
    READY_FOR_PREVIEW = "READY_FOR_PREVIEW"
    PREVIEW_QUEUED = "PREVIEW_QUEUED"
    PREVIEW_DEPLOYING = "PREVIEW_DEPLOYING"
    PREVIEW_DEPLOYED = "PREVIEW_DEPLOYED"
    PREVIEW_VERIFICATION = "PREVIEW_VERIFICATION"
    AWAITING_PRODUCTION_APPROVAL = "AWAITING_PRODUCTION_APPROVAL"
    PRODUCTION_QUEUED = "PRODUCTION_QUEUED"
    PRODUCTION_DEPLOYING = "PRODUCTION_DEPLOYING"
    PRODUCTION_DEPLOYED = "PRODUCTION_DEPLOYED"
    POST_DEPLOY_VERIFICATION = "POST_DEPLOY_VERIFICATION"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    ROLLBACK_QUEUED = "ROLLBACK_QUEUED"
    ROLLED_BACK = "ROLLED_BACK"
    CANCELLED = "CANCELLED"


@dataclass
class ConnectedAccountRecord:
    connection_id: str
    user_id: str
    workspace_id: str
    provider_id: str
    category: ProviderCategory
    authentication_type: str  # oauth2, api_token, iam_role, github_app
    account_identifier: str  # username, org name, team slug
    granted_scopes: List[str] = field(default_factory=list)
    authorized_resources: List[str] = field(default_factory=list)
    token_expiry: Optional[str] = None
    status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED
    last_verified_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


@dataclass
class InfrastructureRecommendation:
    component_name: str
    category: ProviderCategory
    recommended_provider: str
    alternative_provider: str
    rationale: str
    framework_compatibility: str
    estimated_cost_tier: str  # free_tier, pay_as_you_go, pro
    region_options: List[str]
    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED


@dataclass
class DatabaseIntelligenceSpec:
    engine_type: str  # postgresql, mysql, sqlite, mongodb, redis
    is_relational: bool
    recommended_provider: str  # neon, supabase, render_pg, railway_pg, planetscale
    alternative_provider: str
    connection_pooling_required: bool
    supports_branching: bool
    migration_tool: str  # alembic, prisma, flyway, drizzle
    ssl_mode: str = "require"
    estimated_storage_gb: str = "NOT_ESTIMATED"  # zero-invention rule


@dataclass
class DeploymentTransitionRecord:
    transition_id: str
    project_id: str
    from_state: DeploymentState
    to_state: DeploymentState
    actor: str  # human_user, system_orchestrator
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    evidence_digest: Optional[str] = None
    notes: Optional[str] = None
