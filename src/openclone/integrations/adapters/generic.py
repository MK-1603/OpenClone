"""Generic MCP / REST Client Platform Adapter."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter


class GenericPlatformAdapter(PlatformAdapter):
    """Adapter for generic MCP and REST integration clients."""

    def __init__(self):
        super().__init__("generic", "Generic MCP / REST Client")

    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".openclone" / "mcp.json"
        is_configured = ws_mcp.exists()

        return DiscoveredPlatform(
            platform_id=self.platform_id,
            display_name=self.display_name,
            is_installed=True,
            version="1.0.0",
            installation_path=str(ws),
            config_path=str(ws / ".openclone"),
            workspace_config_path=str(ws_mcp) if is_configured else None,
            is_configured=is_configured,
            supported_protocols=["mcp", "rest"],
            compatibility="COMPATIBLE",
            details={"type": "standard_mcp_config"},
        )

    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".openclone" / "mcp.json"
        data = None
        if ws_mcp.exists():
            try:
                data = json.loads(ws_mcp.read_text(encoding="utf-8"))
            except Exception:
                data = {"error": "Invalid JSON"}
        return {"discovered": disc.to_dict(), "config": data, "status": "CONFIGURED" if disc.is_configured else "AVAILABLE"}

    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        dot_oc = ws / ".openclone"
        dot_oc.mkdir(parents=True, exist_ok=True)
        mcp_path = dot_oc / "mcp.json"

        data = {
            "mcpServers": {
                "openclone": {
                    "command": "oc.exe",
                    "args": ["mcp"],
                    "env": {
                        "OPENCLONE_WORKSPACE": str(ws)
                    }
                }
            }
        }
        mcp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"platform_id": self.platform_id, "status": "CONNECTED", "config_path": str(mcp_path)}

    def disconnect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        mcp_path = ws / ".openclone" / "mcp.json"
        if mcp_path.exists():
            mcp_path.unlink()
            return {"platform_id": self.platform_id, "status": "DISCONNECTED", "removed_path": str(mcp_path)}
        return {"platform_id": self.platform_id, "status": "NOT_CONNECTED"}

    def health_check(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        return {"platform_id": self.platform_id, "status": "PASS", "message": "Generic adapter loopback OK"}
