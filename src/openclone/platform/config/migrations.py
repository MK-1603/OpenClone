"""Configuration migration engine for OpenClone."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Tuple

logger = logging.getLogger("openclone.config.migrations")

# Registry of migration functions: (source_version, target_version) -> migration_fn
MIGRATION_REGISTRY: Dict[Tuple[str, str], Callable[[Dict[str, Any]], Dict[str, Any]]] = {}


def register_migration(from_ver: str, to_ver: str):
    """Decorator to register a configuration migration handler."""
    def decorator(fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        MIGRATION_REGISTRY[(from_ver, to_ver)] = fn
        return fn
    return decorator


def migrate_config_dict(data: Dict[str, Any], target_version: str = "1.0.0") -> Dict[str, Any]:
    """Migrate configuration dictionary to the target version idempotently."""
    current_version = data.get("version", "0.9.0")
    if current_version == target_version:
        return data

    updated = dict(data)
    # Sequentially apply known migrations if necessary
    for (src, dst), fn in MIGRATION_REGISTRY.items():
        if updated.get("version") == src:
            logger.info("Migrating configuration from %s to %s", src, dst)
            updated = fn(updated)
            updated["version"] = dst
            if dst == target_version:
                break

    updated["version"] = target_version
    return updated
