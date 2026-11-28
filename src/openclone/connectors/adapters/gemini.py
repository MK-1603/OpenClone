"""Gemini platform adapter for OpenClone Universal AI Assistant Connector."""
from __future__ import annotations

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


class GeminiAdapter(BasePlatformAdapter):
    """Platform adapter for Google Gemini (Function Calling & API Bridge)."""

    def __init__(self, config: Optional[PlatformConfig] = None):
        cfg = config or PlatformConfig(
            platform=PlatformType.GEMINI,
            primary_protocol=ProtocolType.FUNCTION_CALLING,
            supported_protocols=[ProtocolType.FUNCTION_CALLING, ProtocolType.REST],
            auth_token_env="OPENCLONE_GEMINI_TOKEN",
        )
        super().__init__(cfg)

    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Format as Google Gemini FunctionDeclaration specification."""
        return FunctionCallingBridge.to_gemini_declaration(capability)

    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize Gemini function_call or REST payload."""
        self.invocation_count += 1
        headers = headers or {}
        req_id = headers.get("x-request-id") or str(raw_payload.get("id") or time.time())
        approval_digest = headers.get("x-openclone-approval") or raw_payload.get("approval_digest")

        # Handle Gemini function_call structure
        # e.g.: {"function_call": {"name": "openclone_understand_project", "args": {...}}}
        # or top-level {"name": "openclone_understand_project", "args": {...}}
        if "function_call" in raw_payload:
            call_obj = raw_payload["function_call"]
            name, args = FunctionCallingBridge.parse_gemini_call(call_obj)
        elif "name" in raw_payload and ("args" in raw_payload or "arguments" in raw_payload):
            name, args = FunctionCallingBridge.parse_gemini_call(raw_payload)
        else:
            name = raw_payload.get("tool_name", "")
            args = raw_payload.get("arguments", {})

        return NormalizedRequest(
            request_id=req_id,
            platform=self.platform,
            protocol=ProtocolType.FUNCTION_CALLING,
            tool_name=name,
            arguments=args,
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
        """Format canonical execution result as Gemini function_response."""
        gemini_response = {
            "name": request.tool_name,
            "response": {
                "name": request.tool_name,
                "content": canonical_result,
            },
        }
        return NormalizedResponse(
            request_id=request.request_id,
            platform=self.platform,
            tool_name=request.tool_name,
            success=True,
            data=canonical_result,
            raw_response=gemini_response,
            execution_time_ms=execution_time_ms,
        )
