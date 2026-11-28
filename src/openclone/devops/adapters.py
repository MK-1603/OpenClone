"""OpenClone Deployment Provider Adapters.

Defines unified adapter interfaces and concrete implementations for Vercel, Cloudflare,
Render, Supabase, and Neon. Provides safe offline/simulation verification mode.
"""
from __future__ import annotations

import abc
import hashlib
import time
import uuid
from typing import Any, Dict, List, Optional
from src.openclone.devops.models import ConnectedAccountRecord, ConnectionStatus, DeploymentState


class BaseDeploymentAdapter(abc.ABC):
    """Abstract base class for all external deployment provider adapters."""

    def __init__(self, provider_id: str):
        self.provider_id = provider_id

    @abc.abstractmethod
    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        """Validates that credentials exist, are active, and have sufficient scope."""
        pass

    @abc.abstractmethod
    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Produces a deterministic deployment execution plan."""
        pass

    @abc.abstractmethod
    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Deploys an ephemeral preview environment."""
        pass

    @abc.abstractmethod
    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Deploys to production environment, strictly gated by human approval digest."""
        pass

    @abc.abstractmethod
    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        """Polls or inspects deployment status and health."""
        pass

    @abc.abstractmethod
    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        """Reverts deployment to a previous healthy release."""
        pass


class VercelAdapter(BaseDeploymentAdapter):
    """Deployment adapter for Vercel Frontend and Edge Hosting."""

    def __init__(self):
        super().__init__("vercel")

    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        return account.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED)

    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        framework = configuration.get("framework", "Next.js")
        return {
            "provider": self.provider_id,
            "project_id": project_id,
            "framework": framework,
            "build_command": configuration.get("build_command", "npm run build"),
            "output_directory": configuration.get("output_directory", ".next"),
            "planned_routes": ["/*"],
            "plan_status": "PLAN_READY",
        }

    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        dep_id = f"dpl_vrc_{uuid.uuid4().hex[:8]}"
        preview_url = f"https://{project_id}-{branch_name}.vercel.app"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "preview",
            "branch": branch_name,
            "url": preview_url,
            "state": DeploymentState.PREVIEW_DEPLOYED.value,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not approval_digest or len(approval_digest) < 16:
            raise ValueError("Human approval digest required for production Vercel deployment.")
        dep_id = f"dpl_vrc_prod_{uuid.uuid4().hex[:8]}"
        prod_url = f"https://{project_id}.vercel.app"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "production",
            "url": prod_url,
            "approval_digest": approval_digest,
            "state": DeploymentState.PRODUCTION_DEPLOYED.value,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        return {
            "deployment_id": deployment_id,
            "provider": self.provider_id,
            "status": "READY",
            "health": "HEALTHY",
        }

    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        return {
            "deployment_id": deployment_id,
            "target_version": target_version,
            "status": "ROLLED_BACK",
            "rolled_back_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }


class CloudflareAdapter(BaseDeploymentAdapter):
    """Deployment adapter for Cloudflare Pages and Workers."""

    def __init__(self):
        super().__init__("cloudflare")

    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        return account.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED)

    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.provider_id,
            "project_id": project_id,
            "target": configuration.get("target", "pages"),
            "plan_status": "PLAN_READY",
        }

    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        dep_id = f"cf_dpl_{uuid.uuid4().hex[:8]}"
        preview_url = f"https://{branch_name}.{project_id}.pages.dev"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "preview",
            "branch": branch_name,
            "url": preview_url,
            "state": DeploymentState.PREVIEW_DEPLOYED.value,
        }

    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not approval_digest:
            raise ValueError("Approval digest required for Cloudflare production deployment.")
        dep_id = f"cf_prod_{uuid.uuid4().hex[:8]}"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "production",
            "url": f"https://{project_id}.pages.dev",
            "approval_digest": approval_digest,
            "state": DeploymentState.PRODUCTION_DEPLOYED.value,
        }

    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "provider": self.provider_id, "health": "HEALTHY"}

    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "status": "ROLLED_BACK", "target_version": target_version}


class RenderAdapter(BaseDeploymentAdapter):
    """Deployment adapter for Render Web Services & Docker."""

    def __init__(self):
        super().__init__("render")

    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        return account.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED)

    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.provider_id,
            "project_id": project_id,
            "service_type": "web_service",
            "env": configuration.get("env", "python"),
            "plan_status": "PLAN_READY",
        }

    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        dep_id = f"rnd_prv_{uuid.uuid4().hex[:8]}"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "preview",
            "branch": branch_name,
            "url": f"https://{project_id}-pr-{branch_name}.onrender.com",
            "state": DeploymentState.PREVIEW_DEPLOYED.value,
        }

    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not approval_digest:
            raise ValueError("Human approval digest required for Render production deployment.")
        dep_id = f"rnd_prod_{uuid.uuid4().hex[:8]}"
        return {
            "deployment_id": dep_id,
            "provider": self.provider_id,
            "environment": "production",
            "url": f"https://{project_id}.onrender.com",
            "approval_digest": approval_digest,
            "state": DeploymentState.PRODUCTION_DEPLOYED.value,
        }

    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "provider": self.provider_id, "health": "HEALTHY"}

    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "status": "ROLLED_BACK", "target_version": target_version}


class SupabaseAdapter(BaseDeploymentAdapter):
    """Deployment adapter for Supabase Projects (BaaS & Postgres)."""

    def __init__(self):
        super().__init__("supabase")

    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        return account.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED)

    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.provider_id,
            "project_id": project_id,
            "database": "postgresql",
            "auth_enabled": True,
            "storage_enabled": True,
            "plan_status": "PLAN_READY",
        }

    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "deployment_id": f"spb_branch_{uuid.uuid4().hex[:8]}",
            "provider": self.provider_id,
            "environment": "preview_branch",
            "branch": branch_name,
            "state": DeploymentState.PREVIEW_DEPLOYED.value,
        }

    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not approval_digest:
            raise ValueError("Human approval digest required for Supabase production migration.")
        return {
            "deployment_id": f"spb_prod_{uuid.uuid4().hex[:8]}",
            "provider": self.provider_id,
            "environment": "production",
            "approval_digest": approval_digest,
            "state": DeploymentState.PRODUCTION_DEPLOYED.value,
        }

    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "provider": self.provider_id, "health": "HEALTHY"}

    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "status": "ROLLED_BACK", "target_version": target_version}


class NeonAdapter(BaseDeploymentAdapter):
    """Deployment adapter for Neon Serverless PostgreSQL."""

    def __init__(self):
        super().__init__("neon")

    def validate_credentials(self, account: ConnectedAccountRecord) -> bool:
        return account.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED)

    def plan_deployment(self, project_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.provider_id,
            "project_id": project_id,
            "database": "postgresql",
            "branching": True,
            "plan_status": "PLAN_READY",
        }

    def deploy_preview(self, project_id: str, branch_name: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "deployment_id": f"neon_br_{uuid.uuid4().hex[:8]}",
            "provider": self.provider_id,
            "environment": "preview_branch",
            "branch": branch_name,
            "connection_uri": f"postgres://user:pass@ep-preview-123.us-east-2.aws.neon.tech/{project_id}",
            "state": DeploymentState.PREVIEW_DEPLOYED.value,
        }

    def deploy_production(
        self,
        project_id: str,
        approval_digest: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not approval_digest:
            raise ValueError("Human approval digest required for Neon production migration.")
        return {
            "deployment_id": f"neon_prod_{uuid.uuid4().hex[:8]}",
            "provider": self.provider_id,
            "environment": "production",
            "approval_digest": approval_digest,
            "state": DeploymentState.PRODUCTION_DEPLOYED.value,
        }

    def check_status(self, deployment_id: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "provider": self.provider_id, "health": "HEALTHY"}

    def rollback(self, deployment_id: str, target_version: str) -> Dict[str, Any]:
        return {"deployment_id": deployment_id, "status": "ROLLED_BACK", "target_version": target_version}


def get_adapter(provider_id: str) -> Optional[BaseDeploymentAdapter]:
    """Factory function returning the appropriate adapter for a given provider."""
    adapters = {
        "vercel": VercelAdapter,
        "cloudflare": CloudflareAdapter,
        "render": RenderAdapter,
        "supabase": SupabaseAdapter,
        "neon": NeonAdapter,
    }
    adapter_cls = adapters.get(provider_id.lower())
    return adapter_cls() if adapter_cls else None
