"""LibreChat platform adapter for OpenClone Universal AI Assistant Connector."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
import time

from src.openclone.connectors.base import BasePlatformAdapter
from src.openclone.connectors.contracts import (
    NormalizedRequest,
    NormalizedResponse,
    PlatformConfig,
    PlatformType,
    ProtocolType,
)
from src.openclone.integrations.capabilities import Capability


class LibreChatAdapter(BasePlatformAdapter):
    """Platform adapter for LibreChat (MCP server integration & Agent Tool format)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.LIBRECHAT,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.MCP_STDIO, ProtocolType.OPENAPI],
            auth_token_env="OPENCLONE_LIBRECHAT_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format capability as LibreChat MCP Tool definition."""
        return {
            "name": capability.id,
            "description": f"{capability.description} [OpenClone: {capability.category.value}]",
            "inputSchema": capability.input_schema,
        }

    def generate_librechat_config(self, server_url: Optional[str] = None) -> Dict[str, Any]:
        """Generate librechat.yaml MCP server block snippet."""
        url = server_url or "http://localhost:8080/mcp"
        return {
            "mcpServers": {
                "openclone": {
                    "type": "streamable-http",
                    "url": url,
                    "headers": {
                        "Authorization": "Bearer ${OPENCLONE_API_KEY}",
                    },
                }
            }
        }

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize LibreChat MCP request."""
        self.invocation_count += 1
        headers = headers or {}
        req_id = str(raw_payload.get("id") or headers.get("x-request-id") or time.time())
        approval_digest = headers.get("x-openclone-approval") or raw_payload.get("approval_digest")

        params = raw_payload.get("params", {})
        tool_name = params.get("name") or raw_payload.get("tool_name", "")
        arguments = params.get("arguments") or raw_payload.get("arguments", {})

        return NormalizedRequest(
            request_id=req_id,
            platform=self.platform,
            protocol=ProtocolType.MCP_HTTP,
            tool_name=tool_name,
            arguments=arguments,
            raw_payload=raw_payload,
            headers=headers,
            approval_digest=approval_digest,
        )

    def normalize_response(
        self,
        canonical_result: Dict[str, Any],
        request: NormalizedRequest,
        execution_time_ms: float = 0.0,
    ) -> NormalizedResponse:
        """Format canonical result as LibreChat MCP CallToolResult."""
        raw_mcp = {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(canonical_result, indent=2, default=str),
                }
            ],
            "isError": False,
        }
        return NormalizedResponse(
            request_id=request.request_id,
            platform=self.platform,
            tool_name=request.tool_name,
            success=True,
            data=canonical_result,
            raw_response=raw_mcp,
            execution_time_ms=execution_time_ms,
        )
