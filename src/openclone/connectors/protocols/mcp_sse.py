"""MCP Server-Sent Events (SSE) protocol bridge."""
from __future__ import annotations

import json
from typing import Any, Callable, Dict, Generator, Optional
from src.openclone.connectors.protocols.mcp_http import McpHttpBridge


class McpSseBridge:
    """Manages Server-Sent Events streaming sessions for MCP endpoints (GET /sse and POST /messages)."""

    def __init__(self, http_bridge: McpHttpBridge):
        self.http_bridge = http_bridge
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str, endpoint_url: str = "/messages") -> str:
        """Generate initial SSE endpoint event informing client where to post messages."""
        self.active_sessions[session_id] = {"created_at": None, "state": "active"}
        endpoint_event = f"event: endpoint\ndata: {endpoint_url}?sessionId={session_id}\n\n"
        return endpoint_event

    def format_sse_message(self, payload: Dict[str, Any]) -> str:
        """Format JSON-RPC response as SSE message event."""
        return f"event: message\ndata: {json.dumps(payload)}\n\n"

    def handle_message(
        self,
        session_id: str,
        request_body: Dict[str, Any],
        headers: Dict[str, str],
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process incoming POST message in active SSE session."""
        return self.http_bridge.handle_jsonrpc(request_body, headers, auth_token=auth_token)
