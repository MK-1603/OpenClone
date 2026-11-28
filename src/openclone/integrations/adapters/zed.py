"""Zed Editor Platform Adapter."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter


class ZedAdapter(PlatformAdapter):
    """Adapter for Zed Editor integration."""

    def __init__(self):
        super().__init__("zed", "Zed Editor")

    def _get_user_zed_dir(self) -> Path:
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Zed"
        return Path.home() / ".config" / "zed"

    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        cli_path = self._which("zed") or self._which("zed.exe")
        user_dir = self._get_user_zed_dir()
        ws = workspace_root or Path.cwd()
        ws_zed = ws / ".zed" / "settings.json"

        is_installed = cli_path is not None or user_dir.exists()
        is_configured = ws_zed.exists()

        return DiscoveredPlatform(
            platform_id=self.platform_id,
            display_name=self.display_name,
            is_installed=is_installed,
            version="0.160.0" if is_installed else None,
            installation_path=cli_path or str(user_dir),
            config_path=str(user_dir),
            workspace_config_path=str(ws_zed) if is_configured else None,
            is_configured=is_configured,
            supported_protocols=["acp", "mcp"],
            compatibility="COMPATIBLE" if is_installed else "NOT_DETECTED",
            details={"has_workspace_zed_dir": (ws / ".zed").exists()},
        )

    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        ws = workspace_root or Path.cwd()
        ws_zed = ws / ".zed" / "settings.json"
        config_data = None
        if ws_zed.exists():
            try:
                config_data = json.loads(ws_zed.read_text(encoding="utf-8"))
            except Exception:
                config_data = {"error": "Invalid JSON in .zed/settings.json"}
        return {
            "discovered": disc.to_dict(),
            "workspace_config": config_data,
            "status": "CONFIGURED" if disc.is_configured else "AVAILABLE",
        }

    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        dot_zed = ws / ".zed"
        dot_zed.mkdir(parents=True, exist_ok=True)
        settings_path = dot_zed / "settings.json"

        if settings_path.exists():
            backup_path = dot_zed / "settings.json.bak"
            shutil.copy2(settings_path, backup_path)
            try:
                current_data = json.loads(settings_path.read_text(encoding="utf-8"))
            except Exception:
                current_data = {}
        else:
            current_data = {}

        # Merge context_servers
        servers = current_data.setdefault("context_servers", {})
        servers["openclone"] = {
            "command": "oc.exe",
            "args": ["mcp"],
            "enabled": True,
        }
        settings_path.write_text(json.dumps(current_data, indent=2), encoding="utf-8")

        return {
            "platform_id": self.platform_id,
            "status": "CONNECTED",
            "config_path": str(settings_path),
            "message": "Zed workspace configured with OpenClone context server",
        }

    def disconnect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        settings_path = ws / ".zed" / "settings.json"
        if settings_path.exists():
            try:
                current_data = json.loads(settings_path.read_text(encoding="utf-8"))
                if "openclone" in current_data.get("context_servers", {}):
                    del current_data["context_servers"]["openclone"]
                    settings_path.write_text(json.dumps(current_data, indent=2), encoding="utf-8")
                    return {"platform_id": self.platform_id, "status": "DISCONNECTED", "updated_path": str(settings_path)}
            except Exception:
                settings_path.unlink()
                return {"platform_id": self.platform_id, "status": "DISCONNECTED", "removed_path": str(settings_path)}
        return {"platform_id": self.platform_id, "status": "NOT_CONNECTED", "message": "No integration found"}

    def health_check(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        settings_path = ws / ".zed" / "settings.json"
        if not settings_path.exists():
            return {"platform_id": self.platform_id, "status": "PENDING", "message": ".zed/settings.json missing"}
        try:
            parsed = json.loads(settings_path.read_text(encoding="utf-8"))
            if "openclone" in parsed.get("context_servers", {}):
                return {"platform_id": self.platform_id, "status": "PASS", "message": "Zed OpenClone context server configured"}
            return {"platform_id": self.platform_id, "status": "WARN", "message": "openclone entry missing from context_servers"}
        except Exception as e:
            return {"platform_id": self.platform_id, "status": "FAIL", "message": f"Malformed JSON: {e}"}
