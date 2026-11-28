"""OpenClone Environment and Configuration Security Protection.

Validates environment configurations, isolates development/production scopes,
prevents client-side secret leakage, and enforces safe template practices.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set


class SecurityValidationError(ValueError):
    """Raised when environment or configuration violates security constraints."""
    pass


# Allowed execution environments
VALID_ENVIRONMENTS: Set[str] = {"development", "test", "staging", "production"}

# Known placeholder markers allowed in templates
PLACEHOLDER_SUBSTRINGS = [
    "your_",
    "placeholder",
    "example",
    "dummy",
    "mock",
    "<set-in-production>",
    "changeme",
]

# Sensitive keys that must NEVER be leaked into client bundles
PRIVATE_KEY_FRAGMENTS = [
    "API_KEY",
    "SECRET",
    "PRIVATE",
    "PASSWORD",
    "PASSWD",
    "AUTH_TOKEN",
    "DATABASE_URL",
    "DB_PASS",
    "SERVICE_ACCOUNT",
    "CREDENTIALS",
]

# Safe public keys allowed in client bundles
ALLOWED_PUBLIC_KEYS = {
    "NEXT_PUBLIC_APP_URL",
    "NEXT_PUBLIC_APP_NAME",
    "NEXT_PUBLIC_VERSION",
    "NEXT_PUBLIC_ENVIRONMENT",
    "NEXT_PUBLIC_BUILD_ID",
    "PUBLIC_URL",
}


def is_placeholder(value: str) -> bool:
    """Check if a configuration string is a non-secret placeholder."""
    val_lower = value.strip().lower()
    return any(p in val_lower for p in PLACEHOLDER_SUBSTRINGS) or len(val_lower) == 0


def load_safe_config(file_path: Optional[Path] = None, raw_content: Optional[str] = None) -> Dict[str, str]:
    """Parse environment key-value pairs safely without executing code."""
    config: Dict[str, str] = {}
    if raw_content is None:
        if file_path is None or not file_path.is_file():
            return config
        raw_content = file_path.read_text(encoding="utf-8", errors="ignore")

    for line in raw_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            config[key] = val
    return config


def validate_environment(
    env_name: str,
    env_dict: Optional[Dict[str, str]] = None,
    required_keys: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Validate runtime environment parameters against security policies.

    Raises SecurityValidationError if:
      - env_name is not one of development, test, staging, production
      - required keys are missing or contain placeholder values in production
      - strict sandbox is disabled in production
    """
    env_normalized = env_name.strip().lower()
    if env_normalized not in VALID_ENVIRONMENTS:
        raise SecurityValidationError(
            f"Invalid environment '{env_name}'. Allowed environments: {sorted(VALID_ENVIRONMENTS)}"
        )

    current_env = env_dict if env_dict is not None else dict(os.environ)

    # In production, required keys must exist and must not be placeholders
    if env_normalized == "production":
        # Disallow disabling strict sandbox in production
        if current_env.get("OPENCLONE_STRICT_SANDBOX", "true").lower() in ("false", "0", "no"):
            raise SecurityValidationError("Security policy violation: OPENCLONE_STRICT_SANDBOX cannot be disabled in production.")

        if required_keys:
            for key in required_keys:
                val = current_env.get(key)
                if not val:
                    raise SecurityValidationError(f"Missing required production environment variable: '{key}'")
                if is_placeholder(val):
                    raise SecurityValidationError(
                        f"Insecure production configuration: '{key}' contains a placeholder value."
                    )

    return current_env


def validate_client_bundle_safety(client_env: Dict[str, str]) -> None:
    """Ensure server-side secrets are not accidentally exposed in client configuration.

    Raises SecurityValidationError if client-accessible keys contain sensitive terms
    or high-entropy private key / token values.
    """
    for key, val in client_env.items():
        key_upper = key.upper()
        if key_upper in ALLOWED_PUBLIC_KEYS:
            continue

        # Check if client key name exposes a private server concept
        for secret_frag in PRIVATE_KEY_FRAGMENTS:
            if secret_frag in key_upper:
                raise SecurityValidationError(
                    f"Client bundle security violation: Server secret '{secret_frag}' detected in client variable '{key}'"
                )

        # Check if the value looks like a real private token or key header
        if re.search(r"sk-[A-Za-z0-9_-]{20,}", val) or "PRIVATE KEY" in val or re.search(r"ghp_[A-Za-z0-9]{36}", val):
            raise SecurityValidationError(
                f"Client bundle security violation: Secret credential value detected in client variable '{key}'"
            )


def audit_template_safety(template_path: Path) -> List[str]:
    """Audit .env.example or template file to ensure it only has safe placeholders."""
    violations: List[str] = []
    if not template_path.is_file():
        violations.append(f"Template file '{template_path}' not found.")
        return violations

    cfg = load_safe_config(template_path)
    for k, v in cfg.items():
        if not v:
            continue
        # If it looks like a private key or API token and not a placeholder, flag it
        if not is_placeholder(v):
            if re.search(r"sk-[A-Za-z0-9_-]{20,}", v) or re.search(r"AIza[0-9A-Za-z-_]{35}", v) or "BEGIN" in v:
                violations.append(f"Hardcoded credential in template '{template_path.name}' for key '{k}'")
    return violations
