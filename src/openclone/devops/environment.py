"""OpenClone Environment Variable & Secret Management Engine.

Generates safe, structured .env.example contracts, distinguishes public frontend variables
from server-only secrets, prevents secret leakage, and enforces redaction rules.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


class EnvScope(str, enum.Enum):
    PUBLIC_CLIENT = "PUBLIC_CLIENT"  # NEXT_PUBLIC_*, VITE_*, safe for browser bundle
    SERVER_ONLY = "SERVER_ONLY"      # Backend runtime only, private API keys, DB urls
    PROVIDER_CREDENTIAL = "PROVIDER_CREDENTIAL"  # Cloud tokens, deploy hooks, admin keys


@dataclass
class EnvVariableDefinition:
    key: str
    scope: EnvScope
    description: str
    is_required: bool = True
    example_value: str = ""
    sensitive: bool = True


class EnvironmentManager:
    """Manages environment contracts, secret scopes, and .env.example generation."""

    @classmethod
    def generate_standard_variables(
        cls,
        frontend_framework: str = "Next.js",
        backend_framework: str = "FastAPI",
        database_provider: str = "neon",
        has_auth: bool = True,
        has_payments: bool = False,
    ) -> List[EnvVariableDefinition]:
        variables: List[EnvVariableDefinition] = []

        # Database
        variables.append(
            EnvVariableDefinition(
                key="DATABASE_URL",
                scope=EnvScope.SERVER_ONLY,
                description="Primary pooled PostgreSQL connection string",
                is_required=True,
                example_value="postgresql://user:password@ep-sample-123.us-east-2.aws.neon.tech/neondb?sslmode=require",
                sensitive=True,
            )
        )
        variables.append(
            EnvVariableDefinition(
                key="DIRECT_URL",
                scope=EnvScope.SERVER_ONLY,
                description="Direct non-pooled database connection string for migrations",
                is_required=True,
                example_value="postgresql://user:password@ep-sample-123.us-east-2.aws.neon.tech/neondb?sslmode=require",
                sensitive=True,
            )
        )

        # Backend App Secrets
        variables.append(
            EnvVariableDefinition(
                key="APP_ENV",
                scope=EnvScope.SERVER_ONLY,
                description="Application environment mode (development, staging, production)",
                is_required=True,
                example_value="development",
                sensitive=False,
            )
        )
        variables.append(
            EnvVariableDefinition(
                key="SECRET_KEY",
                scope=EnvScope.SERVER_ONLY,
                description="Cryptographic key for signing sessions, CSRF, and JWTs",
                is_required=True,
                example_value="generate-with-openssl-rand-hex-32",
                sensitive=True,
            )
        )

        # Frontend Client Variables
        prefix = "NEXT_PUBLIC_" if "next" in frontend_framework.lower() else "VITE_"
        variables.append(
            EnvVariableDefinition(
                key=f"{prefix}API_URL",
                scope=EnvScope.PUBLIC_CLIENT,
                description="Publicly reachable backend API base URL",
                is_required=True,
                example_value="https://api.example.com",
                sensitive=False,
            )
        )

        # Optional Auth
        if has_auth:
            variables.append(
                EnvVariableDefinition(
                    key="AUTH_SECRET",
                    scope=EnvScope.SERVER_ONLY,
                    description="Authentication session encryption key",
                    is_required=True,
                    example_value="auth-secret-replace-in-production",
                    sensitive=True,
                )
            )
            variables.append(
                EnvVariableDefinition(
                    key=f"{prefix}AUTH_PROVIDER_URL",
                    scope=EnvScope.PUBLIC_CLIENT,
                    description="Public authentication provider endpoint",
                    is_required=False,
                    example_value="https://auth.example.com",
                    sensitive=False,
                )
            )

        # Optional Payments
        if has_payments:
            variables.append(
                EnvVariableDefinition(
                    key=f"{prefix}STRIPE_PUBLISHABLE_KEY",
                    scope=EnvScope.PUBLIC_CLIENT,
                    description="Stripe client-side publishable key",
                    is_required=True,
                    example_value="pk_test_sample",
                    sensitive=False,
                )
            )
            variables.append(
                EnvVariableDefinition(
                    key="STRIPE_SECRET_KEY",
                    scope=EnvScope.PROVIDER_CREDENTIAL,
                    description="Stripe secret API key for backend charges",
                    is_required=True,
                    example_value="sk_test_sample",
                    sensitive=True,
                )
            )

        return variables

    @classmethod
    def generate_env_example_content(cls, variables: List[EnvVariableDefinition]) -> str:
        """Formats definitions into a clean .env.example string with security warnings."""
        lines = [
            "# ===================================================================",
            "# OPENCLONE ENVIRONMENT CONFIGURATION CONTRACT",
            "# WARNING: Never commit actual values or secrets to version control.",
            "# ===================================================================",
            "",
        ]

        # Group by scope
        client_vars = [v for v in variables if v.scope == EnvScope.PUBLIC_CLIENT]
        server_vars = [v for v in variables if v.scope == EnvScope.SERVER_ONLY]
        provider_vars = [v for v in variables if v.scope == EnvScope.PROVIDER_CREDENTIAL]

        if client_vars:
            lines.append("# --- PUBLIC CLIENT-SIDE VARIABLES (Exposed to Browser Bundle) ---")
            for v in client_vars:
                lines.append(f"# {v.description}")
                lines.append(f"{v.key}={v.example_value}")
            lines.append("")

        if server_vars:
            lines.append("# --- SERVER-ONLY SECRETS (Never Expose to Frontend) ---")
            for v in server_vars:
                lines.append(f"# {v.description}")
                lines.append(f"{v.key}={v.example_value}")
            lines.append("")

        if provider_vars:
            lines.append("# --- THIRD-PARTY / CLOUD PROVIDER CREDENTIALS ---")
            for v in provider_vars:
                lines.append(f"# {v.description}")
                lines.append(f"{v.key}={v.example_value}")
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def audit_security(cls, provided_env: Dict[str, str]) -> List[str]:
        """Audits provided environment mapping for obvious security leaks or bad scopes."""
        warnings: List[str] = []
        for key, value in provided_env.items():
            k_upper = key.upper()
            # Check if secret leaked in public prefix
            if k_upper.startswith("NEXT_PUBLIC_") or k_upper.startswith("VITE_"):
                if any(bad in k_upper for bad in ("SECRET", "PRIVATE", "KEY_SECRET", "PASSWORD")):
                    warnings.append(
                        f"CRITICAL LEAK RISK: Variable {key} is prefixed for client bundling "
                        f"but contains sensitive keyword."
                    )
        return warnings
