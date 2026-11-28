"""Open WebUI platform adapter for OpenClone Universal AI Assistant Connector."""
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


class OpenWebUIAdapter(BasePlatformAdapter):
    """Platform adapter for Open WebUI (Streamable MCP & OpenAPI actions)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.OPEN_WEBUI,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.OPENAPI, ProtocolType.REST],
            auth_token_env="OPENCLONE_OPENWEBUI_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format capability as standard MCP tool for Open WebUI."""
        return {
            "name": capability.id,
            "description": f"{capability.description} [OpenClone: {capability.category.value}]",
            "inputSchema": capability.input_schema,
        }

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize Open WebUI MCP or REST action invocation."""
        self.invocation_count += 1
        headers = headers or {}
        req_id = str(raw_payload.get("id") or headers.get("x-request-id") or time.time())
        approval_digest = headers.get("x-openclone-approval") or raw_payload.get("approval_digest")

        # 1. MCP method call
        if raw_payload.get("method") == "tools/call":
            params = raw_payload.get("params", {})
            return NormalizedRequest(
                request_id=req_id,
                platform=self.platform,
                protocol=ProtocolType.MCP_HTTP,
                tool_name=params.get("name", ""),
                arguments=params.get("arguments", {}),
                raw_payload=raw_payload,
                headers=headers,
                approval_digest=approval_digest,
            )

        # 2. REST / OpenAPI action call
        tool_name = raw_payload.get("tool_name") or raw_payload.get("capability_id", "")
        arguments = raw_payload.get("arguments") or {k: v for k, v in raw_payload.items() if k not in ("tool_name", "capability_id")}
        return NormalizedRequest(
            request_id=req_id,
            platform=self.platform,
            protocol=ProtocolType.REST,
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
        """Format canonical execution result for Open WebUI."""
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
