"""Centralized Configuration System for OpenClone.

Provides structured access to environment variables, project-level settings,
deployment profiles, and runtime security flags with strict type validation.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class EnvironmentConfig:
    """Canonical environment configuration with safe defaults."""
    env_name: str = "development"
    debug: bool = False
    workspace_root: Path = field(default_factory=Path.cwd)
    allow_unapproved_tools: bool = False
    rate_limit_enabled: bool = True
    audit_ledger_enabled: bool = True

    @classmethod
    def from_env(cls, env: Optional[Dict[str, str]] = None) -> EnvironmentConfig:
        """Instantiate configuration from environment variables."""
        source = env if env is not None else os.environ
        env_name = source.get("OPENCLONE_ENV", source.get("ENVIRONMENT", "development")).lower()
        debug = source.get("OPENCLONE_DEBUG", "").lower() in ("1", "true", "yes")
        
        root_str = source.get("OPENCLONE_WORKSPACE_ROOT")
        workspace_root = Path(root_str).resolve() if root_str else Path.cwd()

        return cls(
            env_name=env_name,
            debug=debug,
            workspace_root=workspace_root,
            allow_unapproved_tools=source.get("OPENCLONE_ALLOW_UNAPPROVED", "").lower() == "true",
            rate_limit_enabled=source.get("OPENCLONE_RATE_LIMIT", "true").lower() != "false",
            audit_ledger_enabled=source.get("OPENCLONE_LEDGER", "true").lower() != "false",
        )
