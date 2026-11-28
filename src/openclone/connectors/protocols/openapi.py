"""OpenAPI 3.1 protocol bridge and schema generator for AI platform connectors."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.integrations.capabilities import Capability, CapabilityRegistry
from src.openclone.integrations.openapi import generate_openapi_spec


class OpenApiBridge:
    """Provides OpenAPI 3.1 schema generation and documentation for ChatGPT, Open WebUI, and LibreChat."""

    def __init__(self, registry: CapabilityRegistry, base_url: str = "https://api.openclone.org/v1"):
        self.registry = registry
        self.base_url = base_url

    def get_spec(
        self,
        filter_capabilities: Optional[List[str]] = None,
        title: str = "OpenClone Universal AI Assistant Connector API",
    ) -> Dict[str, Any]:
        """Generate OpenAPI 3.1 specification for external assistant import."""
        spec = generate_openapi_spec(self.registry, server_url=self.base_url)
        spec["info"]["title"] = title
        if filter_capabilities:
            allowed = set(filter_capabilities)
            filtered_paths = {}
            for path, path_item in spec.get("paths", {}).items():
                for method, op in path_item.items():
                    op_id = op.get("operationId")
                    if op_id in allowed:
                        filtered_paths[path] = path_item
                        break
            spec["paths"] = filtered_paths
        return spec
