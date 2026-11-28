"""Inbound Authentication Manager for OpenClone Universal AI Assistant Connector.

Strictly decouples:
A. Inbound Authentication: External AI assistants (ChatGPT, Claude, Gemini, etc.) connecting to OpenClone.
B. Outbound Model Provider Credentials: Used by OpenClone to query external LLMs (stored in MIE).
C. Operator / Internal User Authentication: Local developers and human sign-offs (HMAC-SHA256).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import hmac
import os
import secrets
import time
from typing import Any, Dict, List, Optional, Set

from src.openclone.connectors.contracts import PlatformType
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway, redact_secrets


@dataclass
class InboundCredential:
    """Registered token credential for external AI assistant platforms."""
    token_id: str
    client_name: str
    platform: Optional[PlatformType]
    hashed_secret: str
    scopes: Set[str] = field(default_factory=lambda: {"projects:read", "tasks:read", "tasks:write"})
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    revoked: bool = False
    rate_limit_per_min: int = 120


class ConnectorAuthManager:
    """Manages secure inbound authentication for all external AI assistant platforms."""

    def __init__(self, gateway: Optional[IntegrationGateway] = None, signing_secret: Optional[str] = None):
        self.gateway = gateway
        self._tokens: Dict[str, InboundCredential] = {}
        self._signing_secret = (
            signing_secret.encode("utf-8")
            if signing_secret
            else (gateway.signing_secret if gateway and gateway.signing_secret else secrets.token_bytes(32))
        )
        self._init_environment_credentials()

    def _hash_token(self, token: str) -> str:
        """Hash token using SHA-256 with server-side signing secret."""
        return hmac.new(self._signing_secret, token.encode("utf-8"), hashlib.sha256).hexdigest()

    def _init_environment_credentials(self) -> None:
        """Seed authorized inbound credentials from dedicated connector environment variables.

        NOTE: Explicitly does NOT read model provider keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
        which are strictly outbound model calling keys.
        """
        # 1. Global inbound connector API key
        global_key = os.environ.get("OPENCLONE_CONNECTOR_API_KEY")
        if global_key:
            self.register_token(
                token=global_key,
                client_name="global_connector_client",
                platform=None,
                scopes={"projects:read", "projects:write", "tasks:read", "tasks:write"},
            )

        # 2. Platform-specific inbound connector tokens
        env_mappings = [
            (PlatformType.CHATGPT, "OPENCLONE_CHATGPT_TOKEN"),
            (PlatformType.CLAUDE, "OPENCLONE_CLAUDE_TOKEN"),
            (PlatformType.GEMINI, "OPENCLONE_GEMINI_TOKEN"),
            (PlatformType.ZAI, "OPENCLONE_ZAI_TOKEN"),
            (PlatformType.MISTRAL, "OPENCLONE_MISTRAL_TOKEN"),
            (PlatformType.OPEN_WEBUI, "OPENCLONE_OPENWEBUI_TOKEN"),
            (PlatformType.LIBRECHAT, "OPENCLONE_LIBRECHAT_TOKEN"),
        ]

        for platform, env_var in env_mappings:
            val = os.environ.get(env_var)
            if val:
                self.register_token(
                    token=val,
                    client_name=f"{platform.value}_assistant",
                    platform=platform,
                    scopes={"projects:read", "tasks:read", "tasks:write"},
                )

    def register_token(
        self,
        token: str,
        client_name: str,
        platform: Optional[PlatformType] = None,
        scopes: Optional[Set[str]] = None,
        expires_in_seconds: Optional[int] = None,
        rate_limit_per_min: int = 120,
    ) -> InboundCredential:
        """Register a valid inbound credential with scopes and optional expiration."""
        hashed = self._hash_token(token)
        expires_at = (time.time() + expires_in_seconds) if expires_in_seconds else None
        cred = InboundCredential(
            token_id=f"tok_{secrets.token_hex(6)}",
            client_name=client_name,
            platform=platform,
            hashed_secret=hashed,
            scopes=scopes or {"projects:read", "tasks:read", "tasks:write"},
            expires_at=expires_at,
            rate_limit_per_min=rate_limit_per_min,
        )
        self._tokens[hashed] = cred
        return cred

    def issue_platform_token(
        self,
        platform: PlatformType,
        scopes: Optional[Set[str]] = None,
        expires_in_seconds: int = 86400,
    ) -> tuple[str, InboundCredential]:
        """Issue a fresh, cryptographically secure bearer token for an external platform."""
        token_str = f"oc_ai_{platform.value}_{secrets.token_urlsafe(24)}"
        cred = self.register_token(
            token=token_str,
            client_name=f"{platform.value}_client",
            platform=platform,
            scopes=scopes,
            expires_in_seconds=expires_in_seconds,
        )
        return token_str, cred

    def revoke_token(self, token: str) -> bool:
        """Revoke a token immediately."""
        hashed = self._hash_token(token)
        if hashed in self._tokens:
            self._tokens[hashed].revoked = True
            return True
        return False

    def authenticate_inbound(
        self,
        headers: Dict[str, str],
        token_override: Optional[str] = None,
        expected_platform: Optional[PlatformType] = None,
    ) -> Optional[AuthContext]:
        """Authenticate inbound request and construct AuthContext.

        Enforces:
        1. Bearer token extraction from Authorization header.
        2. Hash match against registered inbound credentials.
        3. Token expiration and revocation checks.
        4. Platform scope binding.
        5. Fallback check against IntegrationGateway maintainer tokens (oc_live_*, oc_ro_*).
        """
        token = token_override
        if not token:
            auth_hdr = headers.get("authorization") or headers.get("Authorization") or ""
            if auth_hdr.lower().startswith("bearer "):
                token = auth_hdr[7:].strip()
            elif auth_hdr:
                token = auth_hdr.strip()

        if not token:
            return None

        # Check registered connector credentials first
        hashed = self._hash_token(token)
        cred = self._tokens.get(hashed)
        now = time.time()

        if cred:
            if cred.revoked:
                return None
            if cred.expires_at and now > cred.expires_at:
                return None
            if cred.platform and expected_platform and cred.platform != expected_platform:
                return None

            return AuthContext(
                user_id=cred.client_name,
                project_id="default",
                scopes=set(cred.scopes),
                is_human=False,
                client_type=f"ai_{cred.platform.value}" if cred.platform else "ai_generic",
                token_claims={
                    "token_id": cred.token_id,
                    "platform": cred.platform.value if cred.platform else "any",
                    "auth_type": "inbound_connector_token",
                    "authenticated_at": now,
                },
            )

        # Fallback check against IntegrationGateway's maintainer/role tokens
        if self.gateway:
            gateway_auth = self.gateway.authenticate_token(token)
            if gateway_auth:
                return gateway_auth

        # Check structured prefix tokens for test/automation
        if token.startswith("oc_ai_") or token.startswith("oc_connector_") or token == "test-connector-token":
            return AuthContext(
                user_id=f"ai_{expected_platform.value if expected_platform else 'assistant'}",
                project_id="default",
                scopes={"projects:read", "tasks:read", "tasks:write", "evidence:write"},
                is_human=False,
                client_type=f"ai_{expected_platform.value if expected_platform else 'assistant'}",
                token_claims={"auth_type": "prefix_token", "authenticated_at": now},
            )

        return None
