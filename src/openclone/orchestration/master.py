"""OpenClone Universal Master Engineering Orchestrator.

Central orchestration authority coordinating multi-agent discovery, dynamic specialist activation,
cross-agent verification, build/test execution, and lifecycle governance under Directive OC-UMEO-007.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.orchestration.capability_map import GlobalCapabilityMap
from src.openclone.orchestration.hierarchy import AgentHierarchyManager
from src.openclone.orchestration.lifecycle import MasterEngineeringLifecycle
from src.openclone.orchestration.models import (
    AgentDescriptor,
    AgentTier,
    ComponentMaturity,
    CrossVerificationResult,
    DelegatedTask,
    DelegationResult,
    GlobalCapability,
    OrchestrationMode,
)

logger = logging.getLogger("openclone.orchestration.master")


class UniversalMasterOrchestrator:
    """Master Engineering Orchestrator connecting all domain leads, specialists, and engines."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.hierarchy = AgentHierarchyManager()
        self.capability_map = GlobalCapabilityMap(self.workspace_root)
        self.lifecycle = MasterEngineeringLifecycle(
            workspace_root=self.workspace_root,
            hierarchy=self.hierarchy,
            capability_map=self.capability_map,
        )

    # -------------------------------------------------------------------------
    # Hierarchy & Agent Discovery
    # -------------------------------------------------------------------------

    def get_agent_inventory(self) -> Dict[str, Any]:
        """Discover and categorize all agents across the 3-level hierarchy."""
        all_agents = self.hierarchy.list_agents()
        master = [a.to_dict() for a in all_agents if a.tier == AgentTier.MASTER]
        domain_leads = [a.to_dict() for a in all_agents if a.tier == AgentTier.DOMAIN_LEAD]
        specialists = [a.to_dict() for a in all_agents if a.tier == AgentTier.SPECIALIST]

        return {
            "total_agents": len(all_agents),
            "master_agents": master,
            "domain_lead_count": len(domain_leads),
            "domain_leads": domain_leads,
            "specialist_count": len(specialists),
            "specialists_sample": specialists[:10],
        }

    # -------------------------------------------------------------------------
    # Capability Map & Audit
    # -------------------------------------------------------------------------

    def get_capability_map(self) -> Dict[str, Any]:
        """Return the complete Global Capability Map audit."""
        return self.capability_map.audit_all_capabilities()

    # -------------------------------------------------------------------------
    # Task Delegation & Cross-Verification
    # -------------------------------------------------------------------------

    def delegate_task(
        self,
        task: DelegatedTask,
        verifier_agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Delegate a task to an assigned specialist with optional cross-verification."""
        # 1. Execute task
        res = self.hierarchy.delegate_task(task)

        # 2. Independent peer cross-verification
        verification_report = None
        if verifier_agent_id:
            cross_ver = self.hierarchy.cross_verify(res, verifier_agent_id)
            verification_report = cross_ver.to_dict()
            res.verified_by = verifier_agent_id

        return {
            "task_id": task.task_id,
            "result": res.to_dict(),
            "cross_verification": verification_report,
            "status": "COMPLETED" if res.status == "SUCCEEDED" else "FAILED",
        }

    # -------------------------------------------------------------------------
    # Lifecycle Execution Modes (11 Modes)
    # -------------------------------------------------------------------------

    def execute_mode(
        self,
        mode: OrchestrationMode | str,
        prompt: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute one of the 11 authorized engineering lifecycle modes."""
        if isinstance(mode, str):
            mode = OrchestrationMode(mode.upper())
        return self.lifecycle.execute_mode(mode, prompt, parameters)

    # -------------------------------------------------------------------------
    # Complete Engineering Lifecycle Entrypoint
    # -------------------------------------------------------------------------

    def run_full_lifecycle(
        self,
        prompt: str,
        project_name: str = "OpenCloneProject",
    ) -> Dict[str, Any]:
        """Execute end-to-end multi-agent orchestration."""
        return self.lifecycle.execute_mode(
            OrchestrationMode.FULL_LIFECYCLE,
            prompt,
            parameters={"project_name": project_name},
        )
