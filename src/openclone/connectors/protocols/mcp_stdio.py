"""MCP STDIO protocol bridge for local client integrations (Claude Desktop, local tooling)."""
from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict, Optional
from src.openclone.connectors.contracts import NormalizedRequest, PlatformType, ProtocolType
from src.openclone.connectors.protocols.mcp_http import McpHttpBridge


class McpStdioBridge:
    """Handles local stdio stream execution conforming to standard MCP JSON-RPC 2.0."""

    def __init__(self, http_bridge: McpHttpBridge):
        self.http_bridge = http_bridge

    def process_line(self, line: str, platform: PlatformType = PlatformType.CLAUDE) -> Optional[str]:
        """Parse, process, and respond to a single JSON-RPC line from stdin."""
        line = line.strip()
        if not line:
            return None
        try:
            req = json.loads(line)
            resp = self.http_bridge.handle_jsonrpc(req, headers={}, platform=platform)
            return json.dumps(resp)
        except json.JSONDecodeError:
            err = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error: invalid JSON"},
            }
            return json.dumps(err)
