"""REST protocol bridge for OpenClone Universal AI Assistant Connector."""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional
from src.openclone.connectors.contracts import NormalizedRequest, NormalizedResponse, PlatformType, ProtocolType


class RestProtocolBridge:
    """Dispatches direct REST HTTP capability invocations (/api/v1/capabilities/{id})."""

    def __init__(
        self,
        tool_invocation_fn: Callable[[str, Dict[str, Any], NormalizedRequest], NormalizedResponse],
    ):
        self.tool_invocation_fn = tool_invocation_fn

    def dispatch(
        self,
        method: str,
        capability_id: str,
        body: Optional[Dict[str, Any]],
        headers: Dict[str, str],
        platform: PlatformType = PlatformType.OPEN_WEBUI,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Dispatch REST HTTP request to canonical capability execution."""
        req_id = headers.get("x-request-id") or "rest_req"
        norm_req = NormalizedRequest(
            request_id=req_id,
            platform=platform,
            protocol=ProtocolType.REST,
            tool_name=capability_id,
            arguments=body or {},
            raw_payload={"method": method, "capability_id": capability_id, "body": body},
            headers=headers,
            auth_token=auth_token,
        )

        norm_resp = self.tool_invocation_fn(capability_id, body or {}, norm_req)
        if norm_resp.success:
            return {
                "status": "success",
                "capability_id": capability_id,
                "data": norm_resp.data,
                "execution_time_ms": norm_resp.execution_time_ms,
            }
        else:
            return {
                "status": "error",
                "capability_id": capability_id,
                "code": norm_resp.error_code or 500,
                "message": norm_resp.error_message,
                "execution_time_ms": norm_resp.execution_time_ms,
            }
