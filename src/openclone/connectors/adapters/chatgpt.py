"""ChatGPT platform adapter for OpenClone Universal AI Assistant Connector."""
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


class ChatGPTAdapter(BasePlatformAdapter):
    """Platform adapter for OpenAI ChatGPT (Custom GPT Actions & Remote MCP)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.CHATGPT,
            primary_protocol=ProtocolType.OPENAPI,
            supported_protocols=[ProtocolType.OPENAPI, ProtocolType.MCP_HTTP, ProtocolType.FUNCTION_CALLING],
            auth_token_env="OPENCLONE_CHATGPT_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format as OpenAI / ChatGPT function tool definition."""
        return FunctionCallingBridge.to_openai_tool(capability)

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize ChatGPT Action webhook or OpenAI tool_call into canonical request."""
        self.invocation_count += 1
        headers = headers or {}
        req_id = headers.get("x-request-id") or str(raw_payload.get("id") or time.time())
        approval_digest = headers.get("x-openclone-approval") or raw_payload.get("approval_digest")

        # Case 1: OpenAI Tool Call object ({"id": "call_123", "type": "function", "function": {"name": ..., "arguments": ...}})
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

        # Case 2: MCP tools/call format
        elif raw_payload.get("method") == "tools/call":
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

        # Case 3: Direct OpenAPI REST webhook invocation
        tool_name = raw_payload.get("tool_name") or raw_payload.get("capability_id") or ""
        arguments = raw_payload.get("arguments") or {k: v for k, v in raw_payload.items() if k not in ("tool_name", "capability_id")}
        return NormalizedRequest(
            request_id=req_id,
            platform=self.platform,
            protocol=ProtocolType.OPENAPI,
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
        """Format canonical execution result for ChatGPT consumption."""
        raw_resp = None
        if request.protocol == ProtocolType.FUNCTION_CALLING:
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
