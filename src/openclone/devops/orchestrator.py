"""OpenClone Universal DevOps, Infrastructure & Deployment Orchestrator.

Integrates development readiness, connected account management, evidence-backed
infrastructure scoring, database intelligence, deployment adapters, environment contracts,
and the canonical 21-state deployment state machine into a unified intelligence system.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.openclone.devops.accounts import AccountConnectionManager
from src.openclone.devops.adapters import get_adapter
from src.openclone.devops.database import DatabaseIntelligenceEngine, DatabaseIntelligenceSpec
from src.openclone.devops.environment import EnvironmentManager
from src.openclone.devops.infrastructure import InfrastructureIntelligenceEngine
from src.openclone.devops.models import (
    ConnectedAccountRecord,
    DeploymentState,
    DeploymentTransitionRecord,
    InfrastructureRecommendation,
)
from src.openclone.devops.readiness import DevelopmentReadinessEngine
from src.openclone.devops.statemachine import DeploymentStateMachine


@dataclass
class DevOpsIntelligencePackage:
    project_name: str
    development_readiness: Dict[str, Any]
    infrastructure_recommendations: List[InfrastructureRecommendation]
    database_spec: DatabaseIntelligenceSpec
    connected_accounts: List[ConnectedAccountRecord]
    env_example_template: str
    initial_deployment_state: DeploymentState
    deployment_history: List[DeploymentTransitionRecord]
    generated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "development_readiness": self.development_readiness,
            "infrastructure_recommendations": [
                {
                    "component_name": r.component_name,
                    "category": r.category.value,
                    "recommended_provider": r.recommended_provider,
                    "alternative_provider": r.alternative_provider,
                    "rationale": r.rationale,
                    "framework_compatibility": r.framework_compatibility,
                    "estimated_cost_tier": r.estimated_cost_tier,
                    "region_options": r.region_options,
                    "connection_status": r.connection_status.value,
                }
                for r in self.infrastructure_recommendations
            ],
            "database_spec": {
                "engine_type": self.database_spec.engine_type,
                "is_relational": self.database_spec.is_relational,
                "recommended_provider": self.database_spec.recommended_provider,
                "alternative_provider": self.database_spec.alternative_provider,
                "connection_pooling_required": self.database_spec.connection_pooling_required,
                "supports_branching": self.database_spec.supports_branching,
                "migration_tool": self.database_spec.migration_tool,
                "ssl_mode": self.database_spec.ssl_mode,
                "estimated_storage_gb": self.database_spec.estimated_storage_gb,
            },
            "connected_accounts": [
                {
                    "connection_id": a.connection_id,
                    "provider_id": a.provider_id,
                    "category": a.category.value,
                    "status": a.status.value,
                    "account_identifier": a.account_identifier,
                }
                for a in self.connected_accounts
            ],
            "env_example_template": self.env_example_template,
            "initial_deployment_state": self.initial_deployment_state.value,
            "deployment_history": [
                {
                    "transition_id": t.transition_id,
                    "from_state": t.from_state.value,
                    "to_state": t.to_state.value,
                    "actor": t.actor,
                    "timestamp": t.timestamp,
                    "evidence_digest": t.evidence_digest,
                }
                for t in self.deployment_history
            ],
            "generated_at": self.generated_at,
        }


class DevOpsOrchestrator:
    """Primary orchestrator for development readiness, infrastructure, and deployment lifecycle."""

    def __init__(self, account_manager: Optional[AccountConnectionManager] = None):
        self.account_manager = account_manager or AccountConnectionManager()

    def generate_devops_package(
        self,
        project_name: str,
        frontend_framework: str = "Next.js",
        backend_framework: str = "FastAPI",
        database_engine: str = "PostgreSQL",
        has_file_uploads: bool = False,
        requires_caching: bool = True,
        has_auth: bool = True,
        has_payments: bool = False,
    ) -> DevOpsIntelligencePackage:
        """Constructs a complete DevOps, infrastructure, and deployment package."""
        frameworks = [frontend_framework, backend_framework]
        readiness = DevelopmentReadinessEngine.evaluate_readiness(
            project_name=project_name,
            frameworks=frameworks,
        )

        infra = InfrastructureIntelligenceEngine.evaluate_infrastructure(
            frontend_framework=frontend_framework,
            backend_framework=backend_framework,
            database_engine=database_engine,
            has_file_uploads=has_file_uploads,
            requires_caching=requires_caching,
        )

        db_spec = DatabaseIntelligenceEngine.analyze_database_requirements(
            engine=database_engine,
            requires_branching=True,
            preferred_orm="prisma" if "next" in frontend_framework.lower() else "alembic",
        )

        accounts = self.account_manager.list_connections()

        env_vars = EnvironmentManager.generate_standard_variables(
            frontend_framework=frontend_framework,
            backend_framework=backend_framework,
            database_provider=db_spec.recommended_provider,
            has_auth=has_auth,
            has_payments=has_payments,
        )
        env_example = EnvironmentManager.generate_env_example_content(env_vars)

        # Initialize State Machine and advance to ANALYZED
        fsm = DeploymentStateMachine(project_id=project_name)
        fsm.transition_to(
            new_state=DeploymentState.ANALYZED,
            actor="system_orchestrator",
            notes="Initial project blueprint analysis completed.",
        )

        return DevOpsIntelligencePackage(
            project_name=project_name,
            development_readiness=readiness,
            infrastructure_recommendations=infra,
            database_spec=db_spec,
            connected_accounts=accounts,
            env_example_template=env_example,
            initial_deployment_state=fsm.current_state,
            deployment_history=fsm.get_history(),
        )
