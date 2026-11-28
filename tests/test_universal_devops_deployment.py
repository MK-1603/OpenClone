"""Tests for OpenClone Universal DevOps, Infrastructure & Deployment Intelligence System.

Validates development readiness, connected account management, evidence-backed
infrastructure recommendations, database engine/provider decoupling, deployment adapters,
21-state deployment state machine, and planner agent integration.
"""
import pytest
from src.openclone.devops.models import (
    ConnectedAccountRecord,
    ConnectionStatus,
    DatabaseIntelligenceSpec,
    DeploymentState,
    DeploymentTransitionRecord,
    InfrastructureRecommendation,
    ProviderCategory,
    ProviderMaturity,
)
from src.openclone.devops.accounts import AccountConnectionManager
from src.openclone.devops.readiness import DevelopmentReadinessEngine
from src.openclone.devops.infrastructure import InfrastructureIntelligenceEngine
from src.openclone.devops.database import DatabaseIntelligenceEngine
from src.openclone.devops.adapters import (
    VercelAdapter,
    CloudflareAdapter,
    RenderAdapter,
    SupabaseAdapter,
    NeonAdapter,
    get_adapter,
)
from src.openclone.devops.statemachine import DeploymentStateMachine
from src.openclone.devops.environment import EnvironmentManager, EnvScope, EnvVariableDefinition
from src.openclone.devops.orchestrator import DevOpsOrchestrator, DevOpsIntelligencePackage
from src.openclone.planning.agent import OpenClonePlannerAgent


def test_account_connection_lifecycle():
    mgr = AccountConnectionManager()
    rec = mgr.connect_account(
        provider_id="vercel",
        category=ProviderCategory.FRONTEND_HOSTING,
        account_identifier="openclone-team",
        authentication_type="oauth2",
        verify_immediately=True,
    )
    assert rec.connection_id.startswith("conn-")
    assert rec.status == ConnectionStatus.VERIFIED
    assert rec.last_verified_at is not None

    lookup = mgr.get_connection_by_provider("vercel")
    assert lookup is not None
    assert lookup.account_identifier == "openclone-team"

    conns = mgr.list_connections(category=ProviderCategory.FRONTEND_HOSTING)
    assert any(c.provider_id == "vercel" for c in conns)

    verified = mgr.verify_connection("vercel")
    assert verified is True

    disc = mgr.disconnect_account("vercel")
    assert disc is True
    assert mgr.get_connection_by_provider("vercel").status == ConnectionStatus.DISCONNECTED


def test_development_readiness_engine():
    res = DevelopmentReadinessEngine.evaluate_readiness(
        project_name="ShopClone",
        frameworks=["Next.js", "FastAPI", "Docker"],
        category="E-Commerce",
    )
    assert res["project_name"] == "ShopClone"
    assert res["recommended_ide"] == "Google Antigravity"
    assert res["recommended_coding_agent"] == "Claude Code"
    assert "Anthropic" in res["primary_model_provider"]
    assert any(t["name"] == "Docker" and t["status"] == "REQUIRED" for t in res["development_tools"])
    assert res["readiness_status"] == "READY_FOR_DEVELOPMENT"


def test_infrastructure_recommendation_engine():
    mgr = AccountConnectionManager()
    mgr.connect_account("neon", ProviderCategory.DATABASE, "neon-user", verify_immediately=True)

    recs = InfrastructureIntelligenceEngine.evaluate_infrastructure(
        frontend_framework="Next.js",
        backend_framework="FastAPI",
        database_engine="PostgreSQL",
        has_file_uploads=True,
        requires_caching=True,
    )
    categories = [r.category for r in recs]
    assert ProviderCategory.FRONTEND_HOSTING in categories
    assert ProviderCategory.BACKEND_HOSTING in categories
    assert ProviderCategory.DATABASE in categories
    assert ProviderCategory.STORAGE in categories
    assert ProviderCategory.CACHE in categories

    db_rec = next(r for r in recs if r.category == ProviderCategory.DATABASE)
    assert "Neon" in db_rec.recommended_provider
    assert db_rec.connection_status == ConnectionStatus.VERIFIED


def test_database_intelligence_engine_decoupling():
    # PostgreSQL serverless
    pg_spec = DatabaseIntelligenceEngine.analyze_database_requirements(
        engine="postgresql",
        is_serverless_compute=True,
        requires_branching=True,
    )
    assert pg_spec.is_relational is True
    assert pg_spec.recommended_provider == "neon"
    assert pg_spec.alternative_provider == "supabase"
    assert pg_spec.connection_pooling_required is True
    assert pg_spec.supports_branching is True
    assert pg_spec.estimated_storage_gb == "NOT_ESTIMATED"

    # MySQL
    mysql_spec = DatabaseIntelligenceEngine.analyze_database_requirements(engine="mysql")
    assert mysql_spec.is_relational is True
    assert mysql_spec.recommended_provider == "planetscale"

    # Profile inspection
    profile = DatabaseIntelligenceEngine.get_provider_profile("neon")
    assert profile is not None
    assert profile.pooling_mechanism == "pgbouncer"


def test_deployment_provider_adapters():
    account = ConnectedAccountRecord(
        connection_id="conn-test",
        user_id="user1",
        workspace_id="ws1",
        provider_id="vercel",
        category=ProviderCategory.FRONTEND_HOSTING,
        authentication_type="oauth2",
        account_identifier="test-user",
        status=ConnectionStatus.VERIFIED,
    )

    # Vercel Adapter
    vercel = get_adapter("vercel")
    assert isinstance(vercel, VercelAdapter)
    assert vercel.validate_credentials(account) is True

    plan = vercel.plan_deployment("proj-1", {"framework": "Next.js"})
    assert plan["plan_status"] == "PLAN_READY"

    preview = vercel.deploy_preview("proj-1", "feature-branch", {})
    assert preview["state"] == DeploymentState.PREVIEW_DEPLOYED.value
    assert "feature-branch" in preview["url"]

    # Production gate error if digest missing
    with pytest.raises(ValueError, match="Human approval digest required"):
        vercel.deploy_production("proj-1", "", {})

    valid_digest = "0123456789abcdef0123456789abcdef"
    prod = vercel.deploy_production("proj-1", valid_digest, {})
    assert prod["state"] == DeploymentState.PRODUCTION_DEPLOYED.value

    # Rollback
    rb = vercel.rollback(prod["deployment_id"], "v1.0.0")
    assert rb["status"] == "ROLLED_BACK"

    # Other adapters instantiate cleanly
    assert isinstance(get_adapter("cloudflare"), CloudflareAdapter)
    assert isinstance(get_adapter("render"), RenderAdapter)
    assert isinstance(get_adapter("supabase"), SupabaseAdapter)
    assert isinstance(get_adapter("neon"), NeonAdapter)


def test_deployment_state_machine_deterministic_transitions():
    fsm = DeploymentStateMachine(project_id="shop-app")
    assert fsm.current_state == DeploymentState.NOT_ANALYZED

    # Advance through preview flow
    fsm.transition_to(DeploymentState.ANALYZED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.DEPLOYMENT_PLAN_READY, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.READY_FOR_PREVIEW, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.PREVIEW_QUEUED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.PREVIEW_DEPLOYING, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.PREVIEW_DEPLOYED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.PREVIEW_VERIFICATION, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.AWAITING_PRODUCTION_APPROVAL, actor="system_orchestrator")

    assert fsm.current_state == DeploymentState.AWAITING_PRODUCTION_APPROVAL

    # Production gate rule: system cannot self-approve production
    with pytest.raises(PermissionError, match="Autonomous agents and orchestrators cannot self-approve"):
        fsm.transition_to(
            DeploymentState.PRODUCTION_QUEUED,
            actor="system_orchestrator",
            evidence_digest="0123456789abcdef0123456789abcdef",
        )

    # Production gate rule: missing approval digest
    with pytest.raises(ValueError, match="cryptographic approval digest"):
        fsm.transition_to(
            DeploymentState.PRODUCTION_QUEUED,
            actor="human_user",
            evidence_digest="",
        )

    # Valid human approval
    fsm.transition_to(
        DeploymentState.PRODUCTION_QUEUED,
        actor="human_user",
        evidence_digest="a1b2c3d4e5f67890abcdef1234567890",
    )
    assert fsm.current_state == DeploymentState.PRODUCTION_QUEUED

    # Complete deployment to healthy
    fsm.transition_to(DeploymentState.PRODUCTION_DEPLOYING, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.PRODUCTION_DEPLOYED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.POST_DEPLOY_VERIFICATION, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.HEALTHY, actor="system_orchestrator")
    assert fsm.current_state == DeploymentState.HEALTHY

    # Rollback path
    fsm.transition_to(DeploymentState.DEGRADED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.ROLLBACK_QUEUED, actor="system_orchestrator")
    fsm.transition_to(DeploymentState.ROLLED_BACK, actor="system_orchestrator")
    assert fsm.current_state == DeploymentState.ROLLED_BACK

    assert len(fsm.get_history()) >= 14


def test_environment_manager_contract_and_security():
    vars_list = EnvironmentManager.generate_standard_variables(
        frontend_framework="Next.js",
        backend_framework="FastAPI",
        database_provider="neon",
        has_auth=True,
        has_payments=True,
    )
    env_content = EnvironmentManager.generate_env_example_content(vars_list)
    assert "DATABASE_URL" in env_content
    assert "NEXT_PUBLIC_API_URL" in env_content
    assert "STRIPE_SECRET_KEY" in env_content
    assert "Never commit actual values" in env_content

    # Security leak audit
    leaks = EnvironmentManager.audit_security({
        "NEXT_PUBLIC_STRIPE_SECRET_KEY": "sk_live_12345",
        "DATABASE_URL": "postgresql://...",
    })
    assert len(leaks) == 1
    assert "CRITICAL LEAK RISK" in leaks[0]


def test_devops_orchestrator():
    orchestrator = DevOpsOrchestrator()
    pkg = orchestrator.generate_devops_package(
        project_name="MegaPlatform",
        frontend_framework="Next.js",
        backend_framework="FastAPI",
        database_engine="PostgreSQL",
        has_file_uploads=True,
        requires_caching=True,
        has_auth=True,
        has_payments=True,
    )
    assert isinstance(pkg, DevOpsIntelligencePackage)
    assert pkg.project_name == "MegaPlatform"
    assert pkg.initial_deployment_state == DeploymentState.ANALYZED
    d = pkg.to_dict()
    assert d["project_name"] == "MegaPlatform"
    assert len(d["infrastructure_recommendations"]) >= 4
    assert "DATABASE_URL" in d["env_example_template"]


def test_planner_agent_devops_integration():
    planner = OpenClonePlannerAgent()
    devops_info = planner.generate_devops_intelligence(
        project_name="ShopApp",
        frontend_framework="Next.js",
        backend_framework="FastAPI",
        database_engine="PostgreSQL",
    )
    assert devops_info["project_name"] == "ShopApp"
    assert len(devops_info["infrastructure_recommendations"]) >= 3

    readiness = planner.evaluate_deployment_readiness(
        project_name="ShopApp",
        frameworks=["Next.js", "FastAPI"],
    )
    assert readiness["recommended_ide"] == "Google Antigravity"
    assert readiness["readiness_status"] == "READY_FOR_DEVELOPMENT"

    # Verify Phase 0 execution boundary remains fail-closed
    result = planner.plan_and_execute(
        prompt="Design a shopping application with postgres and nextjs",
        project_name="ShopApp",
        execute=True,
        answers={"clarif_1": "10000 DAU", "clarif_2": "PostgreSQL"},
    )
    assert result["executed"] is False
    assert result["execution"]["status"] == "REJECTED_PHASE_0_BOUNDARY"
