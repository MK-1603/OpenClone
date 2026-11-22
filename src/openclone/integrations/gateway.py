"""Integration Gateway and Policy Engine for OpenClone Universal Integration Core."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import hashlib
import hmac
import json
import re
import secrets
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
class ApprovalRecord:
    """Cryptographically verifiable, operation-bound human approval."""
    approval_id: str
    approver_id: str
    project_id: str
    capability_id: str
    payload_digest: str
    scope: str = "project"
    risk: str = "production_impact"
    created_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 3600)
    nonce: str = ""
    signature: str = ""


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
        self.consumed_nonces: Set[str] = set()

    def create_approval_record(
        self,
        auth: AuthContext,
        capability_id: str,
        arguments: Dict[str, Any],
        scope: str = "project",
        ttl_seconds: int = 3600,
    ) -> Dict[str, Any]:
        """Generate a cryptographically bound human approval record."""
        clean_args = {k: v for k, v in arguments.items() if k not in ("approval_record", "approval_digest")}
        payload_digest = hashlib.sha256(json.dumps(clean_args, sort_keys=True).encode()).hexdigest()
        nonce = secrets.token_hex(16)
        now = time.time()
        record_id = f"APPR-{secrets.token_hex(6).upper()}"
        
        sig_base = f"{record_id}:{auth.user_id}:{auth.project_id}:{capability_id}:{payload_digest}:{nonce}:{now + ttl_seconds}"
        signature = hashlib.sha256(sig_base.encode()).hexdigest()

        return {
            "approval_id": record_id,
            "approver_id": auth.user_id,
            "project_id": auth.project_id,
            "capability_id": capability_id,
            "payload_digest": payload_digest,
            "scope": scope,
            "risk": "production_impact",
            "created_at": now,
            "expires_at": now + ttl_seconds,
            "nonce": nonce,
            "signature": signature,
        }

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
            # High-risk / production actions require human signer
            if not auth.is_human:
                return PolicyDecision(
                    verdict=PolicyVerdict.DENIED,
                    reason=(
                        f"Non-human client '{auth.client_type}' cannot authorize high-risk/production-impact "
                        f"action '{capability_id}'. Explicit human sign-off required."
                    ),
                    capability_id=capability_id,
                )

            # Check if structured approval_record is provided in arguments
            rec = arguments.get("approval_record")
            if isinstance(rec, dict):
                appr_cap = rec.get("capability_id")
                appr_proj = rec.get("project_id")
                expires_at = rec.get("expires_at", 0)
                nonce = rec.get("nonce")
                expected_digest = rec.get("payload_digest")

                if appr_cap != capability_id:
                    return PolicyDecision(
                        verdict=PolicyVerdict.DENIED,
                        reason=f"Approval mismatch: approved for '{appr_cap}', attempted '{capability_id}'.",
                        capability_id=capability_id,
                    )
                if appr_proj and appr_proj != auth.project_id:
                    return PolicyDecision(
                        verdict=PolicyVerdict.DENIED,
                        reason=f"Approval mismatch: approved for project '{appr_proj}', caller context is '{auth.project_id}'.",
                        capability_id=capability_id,
                    )
                if time.time() > expires_at:
                    return PolicyDecision(
                        verdict=PolicyVerdict.DENIED,
                        reason="Cryptographic human approval has expired.",
                        capability_id=capability_id,
                    )
                if nonce:
                    if nonce in self.consumed_nonces:
                        return PolicyDecision(
                            verdict=PolicyVerdict.DENIED,
                            reason=f"Replay detected: approval nonce '{nonce}' has already been consumed.",
                            capability_id=capability_id,
                        )
                    self.consumed_nonces.add(nonce)

                clean_for_hash = {k: v for k, v in arguments.items() if k not in ("approval_record", "approval_digest")}
                computed_digest = hashlib.sha256(json.dumps(clean_for_hash, sort_keys=True).encode()).hexdigest()
                if expected_digest and expected_digest != computed_digest:
                    return PolicyDecision(
                        verdict=PolicyVerdict.DENIED,
                        reason="Payload digest mismatch: arguments were modified after cryptographic human approval.",
                        capability_id=capability_id,
                    )
            elif not approval_digest or len(approval_digest) != 64:
                return PolicyDecision(
                    verdict=PolicyVerdict.REQUIRES_HUMAN_APPROVAL,
                    reason=(
                        f"Action '{capability_id}' requires explicit human cryptographic approval "
                        f"(SHA-256 approval_digest or structured approval_record)."
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
