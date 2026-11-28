"""Mistral platform adapter for OpenClone Universal AI Assistant Connector."""
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
from src.openclone.connectors.protocols.function_calling import FunctionCallingBridge
from src.openclone.integrations.capabilities import Capability


class MistralAdapter(BasePlatformAdapter):
    """Platform adapter for Mistral (Le Chat MCP connector & Mistral API function calling)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.MISTRAL,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.FUNCTION_CALLING],
            auth_token_env="OPENCLONE_MISTRAL_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format as Mistral function tool definition."""
        return FunctionCallingBridge.to_mistral_tool(capability)

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize Mistral tool call or MCP method invocation."""
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

        # 2. Mistral Function Calling payload
        if "function" in raw_payload:
            name, args, call_id = FunctionCallingBridge.parse_openai_call(raw_payload)
            return NormalizedRequest(
                request_id=call_id or req_id,
                platform=self.platform,
                protocol=ProtocolType.FUNCTION_CALLING,
                tool_name=name,
                arguments=args,
                raw_payload=raw_payload,
                headers=headers,
                approval_digest=approval_digest,
            )

        return NormalizedRequest(
            request_id=req_id,
            platform=self.platform,
            protocol=ProtocolType.FUNCTION_CALLING,
            tool_name=raw_payload.get("tool_name", ""),
            arguments=raw_payload.get("arguments", {}),
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
        """Format canonical result for Mistral Le Chat response."""
        raw_resp = {
            "tool_call_id": request.request_id,
            "role": "tool",
            "name": request.tool_name,
            "content": json.dumps(canonical_result, default=str),
        }
        return NormalizedResponse(
            request_id=request.request_id,
            platform=self.platform,
            tool_name=request.tool_name,
            success=True,
            data=canonical_result,
            raw_response=raw_resp,
            execution_time_ms=execution_time_ms,
        )
