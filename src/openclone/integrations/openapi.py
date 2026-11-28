"""OpenAPI 3.1 Specification Generator and REST Dispatcher for OpenClone."""

from pathlib import Path
from typing import Any, Dict, Optional
import json

from src.openclone.integrations.capabilities import (
    Capability,
    CapabilityRegistry,
    IntegrationSurface,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway


def generate_openapi_spec(
    registry: Optional[CapabilityRegistry] = None,
    server_url: str = "https://api.openclone.org/v1",
) -> Dict[str, Any]:
    """Generate OpenAPI 3.1.0 specification from canonical capability registry."""
    reg = registry or get_canonical_registry()
    paths: Dict[str, Any] = {}

    for cap in reg.list_capabilities():
        if IntegrationSurface.HTTP_API not in cap.supported_surfaces:
            continue

        endpoint_path = f"/capabilities/{cap.id}"
        # Determine HTTP method: read-only -> GET, else POST
        method = "get" if cap.risk.value == "read_only" else "post"

        op: Dict[str, Any] = {
            "summary": cap.name,
            "description": cap.description,
            "operationId": cap.id,
            "tags": [cap.category.value],
            "security": [{"BearerAuth": cap.required_scopes}],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "schema": cap.output_schema,
                        }
                    },
                },
                "401": {"description": "Unauthorized / Missing Token"},
                "403": {"description": "Forbidden / Insufficient Scopes"},
            },
        }

        if method == "post":
            op["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": cap.input_schema,
                    }
                },
            }

        paths[endpoint_path] = {method: op}

    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "OpenClone Universal AI Tool Integration API",
            "version": "1.0.0",
            "description": (
                "Provider-neutral HTTP REST API exposing OpenClone canonical engineering capabilities "
                "to external AI hosts (ChatGPT Actions, webhooks, automation runtimes)."
            ),
            "contact": {
                "name": "OpenClone Architecture Team",
                "url": "https://github.com/MK-1603/OpenClone",
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            },
        },
        "servers": [{"url": server_url, "description": "OpenClone Integration Gateway"}],
        "paths": paths,
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "OAuth 2.1 / OIDC Bearer Token with capability scopes.",
                }
            }
        },
    }
    return spec


def dispatch_rest_request(
    gateway: IntegrationGateway,
    auth: AuthContext,
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Dispatch an incoming HTTP REST request to the appropriate canonical capability."""
    # Format: /capabilities/{capability_id} or /v1/capabilities/{capability_id}
    clean_path = path.strip("/")
    if clean_path.startswith("v1/"):
        clean_path = clean_path[3:]

    parts = clean_path.split("/")
    if len(parts) == 2 and parts[0] == "capabilities":
        capability_id = parts[1]
    else:
        raise ValueError(f"Endpoint not found: {method} {path}")

    args = body or {}
    return gateway.execute(auth, capability_id, args)
