"""Google Antigravity IDE Platform Adapter with Global and Workspace Installation."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter


class AntigravityAdapter(PlatformAdapter):
    """Adapter for Google Antigravity IDE integration."""

    def __init__(self):
        super().__init__("antigravity", "Google Antigravity IDE")

    def _get_global_plugin_dir(self) -> Path:
        """Global user-level plugin directory (~/.gemini/config/plugins/openclone)."""
        return Path.home() / ".gemini" / "config" / "plugins" / "openclone"

    def _get_legacy_global_dir(self) -> Path:
        """Fallback global plugin directory (~/.gemini/antigravity/plugins/openclone)."""
        return Path.home() / ".gemini" / "antigravity" / "plugins" / "openclone"

    def _get_workspace_plugin_dir(self, workspace_root: Optional[Path] = None) -> Path:
        """Workspace-level plugin directory."""
        ws = workspace_root or Path.cwd()
        return ws / ".gemini" / "plugins" / "openclone"

    def _get_source_bundle_dir(self) -> Path:
        """Locate bundled template in repository root."""
        repo_root = Path(__file__).resolve().parents[4]
        return repo_root / "plugins" / "openclone-antigravity"

    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        global_dir = self._get_global_plugin_dir()
        legacy_dir = self._get_legacy_global_dir()
        ws_dir = self._get_workspace_plugin_dir(workspace_root)

        ag_installed = (Path.home() / ".gemini").exists()
        is_global_configured = (global_dir / "plugin.json").exists() or (legacy_dir / "plugin.json").exists()
        is_ws_configured = (ws_dir / "plugin.json").exists()
        is_configured = is_global_configured or is_ws_configured

        active_config = None
        if is_ws_configured:
            active_config = str(ws_dir)
        elif (global_dir / "plugin.json").exists():
            active_config = str(global_dir)
        elif (legacy_dir / "plugin.json").exists():
            active_config = str(legacy_dir)

        return DiscoveredPlatform(
            platform_id=self.platform_id,
            display_name=self.display_name,
            is_installed=ag_installed,
            version="2.0.0" if ag_installed else None,
            installation_path=str(Path.home() / ".gemini"),
            config_path=active_config or str(global_dir),
            workspace_config_path=str(ws_dir) if is_ws_configured else None,
            is_configured=is_configured,
            supported_protocols=["mcp", "skills", "rules", "subagents", "hooks"],
            compatibility="COMPATIBLE" if ag_installed else "NOT_DETECTED",
            details={
                "global_dir": str(global_dir),
                "is_global_configured": is_global_configured,
                "is_workspace_configured": is_ws_configured,
            },
        )

    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        manifest_data = None
        if disc.config_path:
            m_path = Path(disc.config_path) / "plugin.json"
            if m_path.exists():
                try:
                    manifest_data = json.loads(m_path.read_text(encoding="utf-8"))
                except Exception:
                    manifest_data = {"error": "Invalid manifest JSON"}

        return {
            "discovered": disc.to_dict(),
            "manifest": manifest_data,
            "status": "CONFIGURED" if disc.is_configured else "AVAILABLE",
        }

    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        """Deploy OpenClone Antigravity plugin globally or to active workspace."""
        is_global = kwargs.get("is_global", False) or kwargs.get("global", False)
        target_dir = self._get_global_plugin_dir() if is_global else self._get_workspace_plugin_dir(workspace_root)
        target_dir.mkdir(parents=True, exist_ok=True)

        source_bundle = self._get_source_bundle_dir()
        if source_bundle.exists() and (source_bundle / "plugin.json").exists():
            # Copy complete pre-packaged bundle
            for item in source_bundle.iterdir():
                dest = target_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)
        else:
            # Inline fallback scaffold
            skills_dir = target_dir / "skills" / "openclone-engineering"
            skills_dir.mkdir(parents=True, exist_ok=True)
            rules_dir = target_dir / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)

            manifest = {
                "name": "openclone",
                "version": "2.0.0",
                "description": "OpenClone Universal AI Engineering Platform Plugin for Google Antigravity.",
                "author": "OpenClone Contributors",
                "suggestedPrompts": [
                    "Inspect project architecture and git status with OpenClone",
                    "Generate a governed task execution plan for this feature",
                    "Run governed task execution with tamper-evident audit ledger"
                ]
            }
            (target_dir / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            mcp_conf = {
                "mcpServers": {
                    "openclone": {
                        "command": "oc.exe",
                        "args": ["mcp"],
                        "description": "OpenClone Universal Engineering MCP Server"
                    }
                }
            }
            (target_dir / "mcp_config.json").write_text(json.dumps(mcp_conf, indent=2), encoding="utf-8")

            skill_md = """---
name: openclone-engineering
description: OpenClone Autonomous Engineering Execution Suite for Antigravity agents.
---
# OpenClone Autonomous Engineering Skill
Use this skill when analyzing requirements, designing architectures, executing governed tasks, or evaluating verification evidence.
"""
            (skills_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

            rule_md = """# OpenClone Deterministic Governance Rules
- Never claim a task passed without running tests and logging tamper-evident evidence.
- High-risk operations (destructive commands, migrations) require human cryptographic approval.
- Enforce strict workspace root boundaries.
"""
            (rules_dir / "AGENTS.md").write_text(rule_md, encoding="utf-8")

        return {
            "platform_id": self.platform_id,
            "status": "CONNECTED",
            "scope": "GLOBAL" if is_global else "WORKSPACE",
            "plugin_path": str(target_dir),
            "manifest_installed": (target_dir / "plugin.json").exists(),
            "mcp_installed": (target_dir / "mcp_config.json").exists() or (target_dir / "mcp.json").exists(),
        }

    def disconnect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        is_global = kwargs.get("is_global", False) or kwargs.get("global", False)
        target_dir = self._get_global_plugin_dir() if is_global else self._get_workspace_plugin_dir(workspace_root)
        removed = []
        if target_dir.exists():
            shutil.rmtree(target_dir)
            removed.append(str(target_dir))

        legacy = self._get_legacy_global_dir()
        if is_global and legacy.exists():
            shutil.rmtree(legacy)
            removed.append(str(legacy))

        if removed:
            return {"platform_id": self.platform_id, "status": "DISCONNECTED", "removed_paths": removed}
        return {"platform_id": self.platform_id, "status": "NOT_CONNECTED", "message": "No integration found"}

    def health_check(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        disc = self.discover(workspace_root)
        if not disc.is_installed:
            return {"platform_id": self.platform_id, "status": "SKIPPED", "message": "Antigravity directory not detected on host"}
        if not disc.is_configured:
            return {"platform_id": self.platform_id, "status": "PENDING", "message": "Antigravity detected but plugin not deployed"}

        # Validate JSON integrity
        cfg_path = Path(disc.config_path)
        m_file = cfg_path / "plugin.json"
        if not m_file.exists():
            return {"platform_id": self.platform_id, "status": "FAIL", "message": "plugin.json missing"}

        try:
            m_data = json.loads(m_file.read_text(encoding="utf-8"))
            if not m_data.get("name"):
                return {"platform_id": self.platform_id, "status": "WARN", "message": "Manifest missing 'name' field"}
            return {
                "platform_id": self.platform_id,
                "status": "PASS",
                "message": f"Antigravity plugin '{m_data.get('name')}' is valid and ready",
                "scope": "WORKSPACE" if disc.workspace_config_path else "GLOBAL",
            }
        except Exception as e:
            return {"platform_id": self.platform_id, "status": "FAIL", "message": f"Malformed plugin.json: {e}"}
