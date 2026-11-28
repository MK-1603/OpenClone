"""Claude platform adapter for OpenClone Universal AI Assistant Connector."""
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


class ClaudeAdapter(BasePlatformAdapter):
    """Platform adapter for Anthropic Claude (Remote MCP & Local STDIO)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.CLAUDE,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.MCP_STDIO, ProtocolType.MCP_SSE],
            auth_token_env="OPENCLONE_CLAUDE_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format as canonical MCP Tool definition for Claude."""
        return {
            "name": capability.id,
            "description": f"{capability.description} [Category: {capability.category.value}, Risk: {capability.risk.value}]",
            "inputSchema": capability.input_schema,
        }

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize Claude MCP tools/call request."""
        self.invocation_count += 1
        headers = headers or {}
        req_id = str(raw_payload.get("id") or headers.get("x-request-id") or time.time())
        approval_digest = headers.get("x-openclone-approval") or raw_payload.get("approval_digest")

        # Standard MCP tools/call
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
        """Format canonical result as standard MCP CallToolResult."""
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
