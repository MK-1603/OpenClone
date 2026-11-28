"""MCP Streamable HTTP protocol bridge for remote AI platform integrations."""
from __future__ import annotations

import json
import secrets
import time
from typing import Any, Callable, Dict, List, Optional
from src.openclone.connectors.contracts import NormalizedRequest, NormalizedResponse, PlatformType, ProtocolType


class McpHttpBridge:
    """Handles JSON-RPC 2.0 requests over Streamable HTTP (POST /mcp)."""

    SUPPORTED_VERSIONS = ["2024-11-05", "latest"]

    def __init__(
        self,
        server_name: str = "openclone-universal-connector",
        server_version: str = "1.0.0",
        tool_discovery_fn: Optional[Callable[[], List[Dict[str, Any]]]] = None,
        tool_invocation_fn: Optional[Callable[[str, Dict[str, Any], NormalizedRequest], NormalizedResponse]] = None,
    ):
        self.server_name = server_name
        self.server_version = server_version
        self.tool_discovery_fn = tool_discovery_fn
        self.tool_invocation_fn = tool_invocation_fn
        # Session store: session_id -> {client_info, created_at, last_active, protocol_version}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout_seconds = 3600.0

    def create_session(self, client_info: Optional[Dict[str, Any]] = None, protocol_version: str = "2024-11-05") -> str:
        """Create a new managed MCP session."""
        session_id = f"mcp_sess_{secrets.token_hex(12)}"
        now = time.time()
        self.sessions[session_id] = {
            "session_id": session_id,
            "client_info": client_info or {},
            "created_at": now,
            "last_active": now,
            "protocol_version": protocol_version,
            "state": "active",
        }
        return session_id

    def validate_session(self, session_id: str) -> bool:
        """Validate whether a session exists and has not timed out."""
        sess = self.sessions.get(session_id)
        if not sess:
            return False
        if sess.get("state") != "active":
            return False
        now = time.time()
        if (now - sess.get("last_active", 0)) > self.session_timeout_seconds:
            sess["state"] = "expired"
            return False
        sess["last_active"] = now
        return True

    def close_session(self, session_id: str) -> bool:
        """Explicitly terminate an active session."""
        if session_id in self.sessions:
            self.sessions[session_id]["state"] = "closed"
            return True
        return False

    def handle_jsonrpc(
        self,
        request_body: Dict[str, Any],
        headers: Dict[str, str],
        platform: PlatformType = PlatformType.CLAUDE,
        auth_token: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process incoming JSON-RPC 2.0 payload according to MCP specification."""
        req_id = request_body.get("id")
        method = request_body.get("method")
        params = request_body.get("params", {})

        if not method:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: missing method"},
            }

        # Session tracking (via parameter, header, or query)
        active_sess_id = (
            session_id
            or headers.get("mcp-session-id")
            or headers.get("Mcp-Session-Id")
            or params.get("sessionId")
        )

        # 1. MCP initialize handshake
        if method == "initialize":
            client_version = params.get("protocolVersion", "2024-11-05")
            negotiated_version = client_version if client_version in self.SUPPORTED_VERSIONS else "2024-11-05"
            new_session_id = self.create_session(
                client_info=params.get("clientInfo"),
                protocol_version=negotiated_version,
            )

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": negotiated_version,
                    "serverInfo": {
                        "name": self.server_name,
                        "version": self.server_version,
                    },
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {},
                        "prompts": {},
                        "logging": {},
                    },
                    "sessionId": new_session_id,
                },
            }

        # 2. MCP initialized notification
        elif method == "notifications/initialized":
            if active_sess_id and active_sess_id in self.sessions:
                self.sessions[active_sess_id]["state"] = "active"
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        # 3. MCP tools/list discovery
        elif method == "tools/list":
            tools = self.tool_discovery_fn() if self.tool_discovery_fn else []
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": tools},
            }

        # 4. MCP tools/call execution
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            norm_req = NormalizedRequest(
                request_id=str(req_id or ""),
                platform=platform,
                protocol=ProtocolType.MCP_HTTP,
                tool_name=tool_name,
                arguments=arguments,
                raw_payload=request_body,
                headers=headers,
                auth_token=auth_token,
            )

            if not self.tool_invocation_fn:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": "Server tool invocation handler not configured"},
                }

            norm_resp = self.tool_invocation_fn(tool_name, arguments, norm_req)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": norm_resp.to_mcp_result(),
            }

        # 5. MCP ping
        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        # 6. Session termination
        elif method in ("session/close", "connection/close"):
            if active_sess_id:
                self.close_session(active_sess_id)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"closed": True}}

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: '{method}'"},
            }
