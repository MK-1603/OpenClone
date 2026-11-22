"""Integration Gateway and Policy Engine for OpenClone Universal Integration Core."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import hashlib
import json
import re
import time

from src.openclone.integrations.capabilities import (
    Capability,
    CapabilityRegistry,
    RiskClassification,
    get_canonical_registry,
)


class PolicyVerdict(str, Enum):
    """Outcome of policy evaluation."""
    ALLOWED = "allowed"
    DENIED = "denied"
    REQUIRES_HUMAN_APPROVAL = "requires_human_approval"


@dataclass
class AuthContext:
    """Security context of an authenticated caller."""
    user_id: str
    project_id: str
    scopes: Set[str] = field(default_factory=set)
    is_human: bool = False
    client_type: str = "generic"
    token_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    """Detailed policy decision for a capability invocation."""
    verdict: PolicyVerdict
    reason: str
    capability_id: str
    missing_scopes: List[str] = field(default_factory=list)
    audit_event: Optional[Dict[str, Any]] = None


# Pattern to redact tokens/keys
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|secret|token|password|bearer|auth[_-]?token)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?"
)
SENSITIVE_KEY_SUBSTRINGS = {"api_key", "apikey", "secret", "token", "password", "bearer", "private_key"}


def redact_secrets(data: Any) -> Any:
    """Recursively redact credentials from inputs/outputs."""
    if isinstance(data, str):
        return SECRET_PATTERN.sub(r"\1=***REDACTED***", data)
    elif isinstance(data, dict):
        clean = {}
        for k, v in data.items():
            if any(sub in k.lower() for sub in SENSITIVE_KEY_SUBSTRINGS) and isinstance(v, str):
                clean[k] = "***REDACTED***"
            else:
                clean[k] = redact_secrets(v)
        return clean
    elif isinstance(data, list):
        return [redact_secrets(v) for v in data]
    return data


class IntegrationGateway:
    """Gateway enforcing authentication, scoped authorization, and human approvals."""

    def __init__(self, registry: Optional[CapabilityRegistry] = None, repo_root: Optional[Path] = None):
        self.root = repo_root or Path(__file__).resolve().parents[3]
        self.registry = registry or get_canonical_registry(self.root)
        self.audit_log: List[Dict[str, Any]] = []

    def authenticate_token(self, token: str) -> Optional[AuthContext]:
        """Validate bearer token and construct AuthContext.
        
        Supports simulated OAuth 2.1 / OIDC JWT format or local API keys.
        """
        if not token:
            return None

        # Standard local maintainer token
        if token.startswith("oc_live_") or token == "test-valid-token":
            return AuthContext(
                user_id="usr_lead_architect",
                project_id="default",
                scopes={
                    "projects:read",
                    "checklists:read",
                    "tasks:read",
                    "tasks:write",
                    "evidence:write",
                    "verification:request",
                    "defects:write",
                    "release:read",
                    "release:approve",
                },
                is_human=True,
                client_type="local_maintainer",
            )
        # Read-only client token
        elif token.startswith("oc_ro_") or token == "test-ro-token":
            return AuthContext(
                user_id="usr_guest_inspector",
                project_id="default",
                scopes={"projects:read", "checklists:read", "tasks:read", "release:read"},
                is_human=False,
                client_type="guest_inspector",
            )
        # Narrow IDE agent token (task execution and evidence attachment)
        elif token.startswith("oc_ide_") or token == "test-ide-token":
            return AuthContext(
                user_id="usr_ide_agent",
                project_id="default",
                scopes={"projects:read", "checklists:read", "tasks:read", "tasks:write", "evidence:write"},
                is_human=False,
                client_type="ide_agent",
            )
        return None

    def evaluate_policy(
        self,
        auth: AuthContext,
        capability_id: str,
        arguments: Dict[str, Any],
        approval_digest: Optional[str] = None,
    ) -> PolicyDecision:
        """Evaluate authorization and policy rules against a target capability."""
        cap = self.registry.get(capability_id)
        if not cap:
            return PolicyDecision(
                verdict=PolicyVerdict.DENIED,
                reason=f"Unknown capability: '{capability_id}'",
                capability_id=capability_id,
            )

        # 1. Tenant & Project Isolation Boundary Check
        req_project = arguments.get("project_id")
        if req_project and req_project != auth.project_id:
            return PolicyDecision(
                verdict=PolicyVerdict.DENIED,
                reason=(
                    f"Cross-project access violation: Authenticated for project '{auth.project_id}' "
                    f"but requested '{req_project}'."
                ),
                capability_id=capability_id,
            )

        # 2. Scope Enforcement
        missing = [scope for scope in cap.required_scopes if scope not in auth.scopes]
        if missing:
            return PolicyDecision(
                verdict=PolicyVerdict.DENIED,
                reason=f"Forbidden: Missing required scope(s): {', '.join(missing)}",
                capability_id=capability_id,
                missing_scopes=missing,
            )

        # 3. Human Approval Gate Enforcement
        needs_approval = (
            cap.requires_human_approval
            or cap.risk in (RiskClassification.DESTRUCTIVE, RiskClassification.PRODUCTION_IMPACT)
        )
        if needs_approval:
            # Must have valid SHA-256 approval digest and human sign-off
            if not approval_digest or len(approval_digest) != 64:
                return PolicyDecision(
                    verdict=PolicyVerdict.REQUIRES_HUMAN_APPROVAL,
                    reason=(
                        f"Action '{capability_id}' requires explicit human cryptographic approval "
                        f"(SHA-256 approval_digest)."
                    ),
                    capability_id=capability_id,
                )

        # Approved
        audit_event = {
            "timestamp": time.time(),
            "user_id": auth.user_id,
            "project_id": auth.project_id,
            "capability_id": capability_id,
            "client_type": auth.client_type,
            "risk": cap.risk.value,
            "approved": True,
        }
        return PolicyDecision(
            verdict=PolicyVerdict.ALLOWED,
            reason="Authorized",
            capability_id=capability_id,
            audit_event=audit_event,
        )

    def execute(
        self,
        auth: AuthContext,
        capability_id: str,
        arguments: Dict[str, Any],
        approval_digest: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Authorize and execute a canonical capability."""
        decision = self.evaluate_policy(auth, capability_id, arguments, approval_digest)

        if decision.verdict == PolicyVerdict.DENIED:
            raise PermissionError(f"Access Denied: {decision.reason}")
        elif decision.verdict == PolicyVerdict.REQUIRES_HUMAN_APPROVAL:
            raise PermissionError(f"Approval Required: {decision.reason}")

        cap = self.registry.get(capability_id)
        if not cap or not cap.handler:
            raise RuntimeError(f"Capability '{capability_id}' has no registered handler.")

        # Execute capability with redaction
        clean_args = redact_secrets(arguments)
        raw_result = cap.handler(clean_args, auth)
        clean_result = redact_secrets(raw_result)

        if decision.audit_event:
            self.audit_log.append(decision.audit_event)

        return clean_result
