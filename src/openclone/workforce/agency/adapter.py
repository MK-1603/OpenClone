"""OpenClone Agency Agents Integration — Execution Adapter & Security Governance.

Binds external Agency Agents to OpenClone's execution environment,
injecting governance boundaries, formatting prompts, selecting models,
and enforcing least-privilege security controls.
"""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List, Optional

from src.openclone.mie.models import RoutingMode, TaskCategory
from src.openclone.mie.router import ModelRouter
from src.openclone.workforce.agency.models import (
    AgencyAgentProfile,
    ExecutionContract,
    ExecutionStatus,
)


class AgencyExecutionAdapter:
    """Execution adapter binding external Agency Agents to OpenClone governance and runtime."""

    SENSITIVE_ACTIONS = {"write", "execute", "external_access", "destructive_change", "release", "deploy", "security_test"}

    # Mapping Agency division to Model Intelligence Engine task categories
    DIVISION_CATEGORY_MAP: Dict[str, TaskCategory] = {
        "engineering": TaskCategory.BACKEND_API,
        "design": TaskCategory.FRONTEND_UI,
        "product": TaskCategory.ARCHITECTURE_DESIGN,
        "project-management": TaskCategory.GENERAL_ORCHESTRATION,
        "testing": TaskCategory.TEST_ENGINEERING,
        "security": TaskCategory.SECURITY_AUDIT,
        "marketing": TaskCategory.DOCUMENTATION_SPECS,
        "finance": TaskCategory.DOCUMENTATION_SPECS,
        "spatial-computing": TaskCategory.FRONTEND_UI,
        "game-development": TaskCategory.BACKEND_API,
        "academic": TaskCategory.DOCUMENTATION_SPECS,
        "specialized": TaskCategory.GENERAL_ORCHESTRATION,
    }

    def __init__(self, model_router: Optional[ModelRouter] = None):
        self.router = model_router or ModelRouter()

    def create_execution_contract(
        self,
        agent: AgencyAgentProfile,
        task_prompt: str,
        project_context: Optional[Dict[str, Any]] = None,
        requested_actions: Optional[List[str]] = None,
        routing_mode: RoutingMode = RoutingMode.BALANCED,
    ) -> ExecutionContract:
        """Create a validated execution contract for an external specialist agent."""
        cid = f"contract_{uuid.uuid4().hex[:10]}"
        tid = f"task_{uuid.uuid4().hex[:8]}"
        ctx = project_context or {}

        # Default allowed actions based on division
        actions = requested_actions or ["observe", "plan", "design"]
        if agent.division in ("engineering", "specialized") and "write" in actions:
            # Requires approval check below
            pass

        # Determine if approval is strictly required
        requires_approval = any(act in self.SENSITIVE_ACTIONS for act in actions)

        # Select optimal model via Model Intelligence Engine (MIE)
        category = self.DIVISION_CATEGORY_MAP.get(agent.division, TaskCategory.GENERAL_ORCHESTRATION)
        route_decision = self.router.route_task(
            prompt=f"[{agent.name}] {task_prompt}",
            mode=routing_mode,
        )
        selected_model = route_decision.selected_model.model_id if route_decision.selected_model else "gpt-6.2-sol"

        return ExecutionContract(
            contract_id=cid,
            task_id=tid,
            agent_id=agent.id,
            division=agent.division,
            prompt=task_prompt,
            project_context=ctx,
            allowed_actions=actions,
            requires_approval=requires_approval,
            assigned_model=selected_model,
            status=ExecutionStatus.WAITING_APPROVAL if requires_approval else ExecutionStatus.PENDING,
        )

    def format_agent_prompt(
        self,
        agent: AgencyAgentProfile,
        contract: ExecutionContract,
        project_name: str = "OpenClone Project",
    ) -> str:
        """Format the execution prompt combining original personality with OpenClone boundaries."""
        rules_text = "\n".join(f"- {r}" for r in agent.critical_rules) if agent.critical_rules else "- Follow domain best practices."
        deliverables_text = "\n".join(f"- {d}" for d in agent.deliverables) if agent.deliverables else "- Standard technical deliverables."
        workflow_text = "\n".join(f"{i+1}. {w}" for i, w in enumerate(agent.workflow_steps)) if agent.workflow_steps else "Execute structured methodology."

        return (
            f"=== SPECIALIST IDENTITY: {agent.name.upper()} ({agent.division.upper()}) ===\n"
            f"Vibe: {agent.vibe}\n\n"
            f"# Identity & Memory\n{agent.identity_memory}\n\n"
            f"# Core Mission\n{agent.mission}\n\n"
            f"# Critical Rules\n{rules_text}\n\n"
            f"# Expected Deliverables\n{deliverables_text}\n\n"
            f"# Workflow Process\n{workflow_text}\n\n"
            f"=== OPENCLONE GOVERNANCE & PROJECT CONTEXT ===\n"
            f"- Project: {project_name}\n"
            f"- Task ID: {contract.task_id}\n"
            f"- Assigned Model: {contract.assigned_model}\n"
            f"- Permitted Actions: {', '.join(contract.allowed_actions)}\n"
            f"- Security Gate: Zero secret leakage. No unauthorized file writes or shell access.\n"
            f"- Standard: OpenClone Universal Engineering Standard (Zero AI Slop).\n\n"
            f"=== ASSIGNED TASK ===\n"
            f"{contract.prompt}\n"
        )

    def validate_action_permissions(
        self,
        contract: ExecutionContract,
        requested_action: str,
        is_human_approved: bool = False,
    ) -> bool:
        """Check whether a requested action is permitted under the execution contract."""
        if requested_action in contract.denied_actions:
            return False

        if requested_action in self.SENSITIVE_ACTIONS:
            if not is_human_approved and contract.requires_approval:
                return False

        return requested_action in contract.allowed_actions
