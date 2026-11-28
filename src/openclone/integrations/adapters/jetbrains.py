"""JetBrains IDEs Platform Adapter."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter


class JetBrainsAdapter(PlatformAdapter):
    """Adapter for JetBrains IDEs integration."""

    def __init__(self):
        super().__init__("jetbrains", "JetBrains IDEs")

    def _get_user_jetbrains_dir(self) -> Path:
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "JetBrains"
        return Path.home() / ".config" / "JetBrains"

    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        user_dir = self._get_user_jetbrains_dir()
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".idea" / "mcp.json"

        is_installed = user_dir.exists()
        is_configured = ws_mcp.exists()

        return DiscoveredPlatform(
            platform_id=self.platform_id,
            display_name=self.display_name,
            is_installed=is_installed,
            version="2024.1" if is_installed else None,
            installation_path=str(user_dir) if is_installed else None,
            config_path=str(user_dir),
            workspace_config_path=str(ws_mcp) if is_configured else None,
            is_configured=is_configured,
            supported_protocols=["mcp", "tools"],
            compatibility="COMPATIBLE" if is_installed else "NOT_DETECTED",
            details={"has_workspace_idea_dir": (ws / ".idea").exists()},
        )

    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".idea" / "mcp.json"
        config_data = None
        if ws_mcp.exists():
            try:
                config_data = json.loads(ws_mcp.read_text(encoding="utf-8"))
            except Exception:
                config_data = {"error": "Invalid JSON in .idea/mcp.json"}
        return {
            "discovered": disc.to_dict(),
            "workspace_config": config_data,
            "status": "CONFIGURED" if disc.is_configured else "AVAILABLE",
        }

    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        dot_idea = ws / ".idea"
        dot_idea.mkdir(parents=True, exist_ok=True)
        mcp_path = dot_idea / "mcp.json"

        if mcp_path.exists():
            backup_path = dot_idea / "mcp.json.bak"
            shutil.copy2(mcp_path, backup_path)

        data = {
            "servers": [
                {
                    "name": "OpenClone",
                    "command": "oc.exe",
                    "args": ["mcp"]
                }
            ]
        }
        mcp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        return {
            "platform_id": self.platform_id,
            "status": "CONNECTED",
            "config_path": str(mcp_path),
            "message": "JetBrains workspace configured with OpenClone MCP server",
        }

    def disconnect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        mcp_path = ws / ".idea" / "mcp.json"
        if mcp_path.exists():
            mcp_path.unlink()
            return {"platform_id": self.platform_id, "status": "DISCONNECTED", "removed_path": str(mcp_path)}
        return {"platform_id": self.platform_id, "status": "NOT_CONNECTED", "message": "No integration found"}

    def health_check(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        mcp_path = ws / ".idea" / "mcp.json"
        if not mcp_path.exists():
            return {"platform_id": self.platform_id, "status": "PENDING", "message": ".idea/mcp.json missing"}
        try:
            parsed = json.loads(mcp_path.read_text(encoding="utf-8"))
            servers = parsed.get("servers", [])
            if any(s.get("name") == "OpenClone" for s in servers):
                return {"platform_id": self.platform_id, "status": "PASS", "message": "JetBrains OpenClone MCP server configured"}
            return {"platform_id": self.platform_id, "status": "WARN", "message": "OpenClone entry missing from .idea/mcp.json"}
        except Exception as e:
            return {"platform_id": self.platform_id, "status": "FAIL", "message": f"Malformed JSON: {e}"}
