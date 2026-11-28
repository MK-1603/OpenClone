"""Windsurf AI Editor Platform Adapter (Codeium)."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter


class WindsurfAdapter(PlatformAdapter):
    """Adapter for Windsurf AI Editor integration (Codeium cascade and rules)."""

    def __init__(self):
        super().__init__("windsurf", "Windsurf AI Editor")

    def _get_user_windsurf_dir(self) -> Path:
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Windsurf" / "User"
        return Path.home() / ".codeium" / "windsurf"

    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        cli_path = self._which("windsurf") or self._which("windsurf.cmd")
        user_dir = self._get_user_windsurf_dir()
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".codeium" / "windsurf" / "mcp_config.json"
        ws_rules = ws / ".windsurfrules"

        is_installed = cli_path is not None or user_dir.exists()
        is_configured = ws_mcp.exists() or ws_rules.exists()

        return DiscoveredPlatform(
            platform_id=self.platform_id,
            display_name=self.display_name,
            is_installed=is_installed,
            version="1.0.0" if is_installed else None,
            installation_path=cli_path or str(user_dir),
            config_path=str(user_dir),
            workspace_config_path=str(ws_mcp) if ws_mcp.exists() else (str(ws_rules) if ws_rules.exists() else None),
            is_configured=is_configured,
            supported_protocols=["mcp", "rules", "cascade"],
            compatibility="COMPATIBLE" if is_installed else "NOT_DETECTED",
            details={
                "has_windsurfrules": ws_rules.exists(),
                "has_codeium_dir": (ws / ".codeium").exists(),
            },
        )

    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        ws = workspace_root or Path.cwd()
        ws_mcp = ws / ".codeium" / "windsurf" / "mcp_config.json"
        ws_rules = ws / ".windsurfrules"

        config_data = None
        if ws_mcp.exists():
            try:
                config_data = json.loads(ws_mcp.read_text(encoding="utf-8"))
            except Exception:
                config_data = {"error": "Invalid JSON in .codeium/windsurf/mcp_config.json"}

        rules_content = None
        if ws_rules.exists():
            try:
                rules_content = ws_rules.read_text(encoding="utf-8")
            except Exception:
                rules_content = "<error reading .windsurfrules>"

        return {
            "discovered": disc.to_dict(),
            "workspace_config": config_data,
            "has_rules": ws_rules.exists(),
            "rules_preview": rules_content[:300] if rules_content else None,
            "status": "CONFIGURED" if disc.is_configured else "AVAILABLE",
        }

    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        codeium_dir = ws / ".codeium" / "windsurf"
        codeium_dir.mkdir(parents=True, exist_ok=True)
        mcp_path = codeium_dir / "mcp_config.json"

        if mcp_path.exists():
            backup_path = codeium_dir / "mcp_config.json.bak"
            shutil.copy2(mcp_path, backup_path)
            try:
                existing_data = json.loads(mcp_path.read_text(encoding="utf-8"))
                if isinstance(existing_data, dict) and "mcpServers" in existing_data:
                    existing_data["mcpServers"]["openclone"] = {
                        "command": "python",
                        "args": ["-m", "src.openclone.mcp.server"],
                        "description": "OpenClone Deterministic Governance & PIA Gateway",
                    }
                    data = existing_data
                else:
                    data = {
                        "mcpServers": {
                            "openclone": {
                                "command": "python",
                                "args": ["-m", "src.openclone.mcp.server"],
                                "description": "OpenClone Deterministic Governance & PIA Gateway",
                            }
                        }
                    }
            except Exception:
                data = {
                    "mcpServers": {
                        "openclone": {
                            "command": "python",
                            "args": ["-m", "src.openclone.mcp.server"],
                            "description": "OpenClone Deterministic Governance & PIA Gateway",
                        }
                    }
                }
        else:
            data = {
                "mcpServers": {
                    "openclone": {
                        "command": "python",
                        "args": ["-m", "src.openclone.mcp.server"],
                        "description": "OpenClone Deterministic Governance & PIA Gateway",
                    }
                }
            }
        mcp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        # Also generate .windsurfrules for Taste Skill 2.6.0 anti-slop rules, preserving user rules if present
        rules_path = ws / ".windsurfrules"
        rules_content = (
            "# OpenClone Deterministic Governance Rules for Windsurf\n\n"
            "- Read before write: Inspect target modules before making edits.\n"
            "- Deterministic verification: Run test suites and log tangible evidence before declaring success.\n"
            "- Zero synthetic assumption: Never fabricate DAU, traffic, or architecture constraints.\n"
            "- Workspace boundary: Never traverse outside workspace root.\n"
        )
        if rules_path.exists():
            backup_rules = ws / ".windsurfrules.bak"
            shutil.copy2(rules_path, backup_rules)
            existing_rules = rules_path.read_text(encoding="utf-8")
            if "# OpenClone Deterministic Governance Rules" not in existing_rules:
                rules_path.write_text(existing_rules.rstrip() + "\n\n" + rules_content, encoding="utf-8")
        else:
            rules_path.write_text(rules_content, encoding="utf-8")

        return {
            "platform_id": self.platform_id,
            "status": "CONNECTED",
            "mcp_config_path": str(mcp_path),
            "rules_path": str(rules_path),
        }

    def disconnect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        ws = workspace_root or Path.cwd()
        mcp_path = ws / ".codeium" / "windsurf" / "mcp_config.json"
        rules_path = ws / ".windsurfrules"

        removed = []
        if mcp_path.exists():
            mcp_path.unlink()
            removed.append(str(mcp_path))
        if rules_path.exists():
            rules_path.unlink()
            removed.append(str(rules_path))

        return {
            "platform_id": self.platform_id,
            "status": "DISCONNECTED",
            "removed_files": removed,
        }
