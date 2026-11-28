"""Platform Discovery Engine for OpenClone Universal Integration Ecosystem."""
from __future__ import annotations

import platform
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter
from src.openclone.integrations.adapters.antigravity import AntigravityAdapter
from src.openclone.integrations.adapters.vscode import VSCodeAdapter
from src.openclone.integrations.adapters.cursor import CursorAdapter
from src.openclone.integrations.adapters.jetbrains import JetBrainsAdapter
from src.openclone.integrations.adapters.zed import ZedAdapter
from src.openclone.integrations.adapters.generic import GenericPlatformAdapter
from src.openclone.integrations.registry import get_platform_registry


class PlatformDiscoveryEngine:
    """Discovers installed development environments and IDEs on the user host machine."""

    def __init__(self):
        self._adapters: Dict[str, PlatformAdapter] = {}
        self._registry = get_platform_registry()
        self._register_default_adapters()

    def _register_default_adapters(self) -> None:
        self.register_adapter(AntigravityAdapter())
        self.register_adapter(VSCodeAdapter())
        self.register_adapter(CursorAdapter())
        self.register_adapter(JetBrainsAdapter())
        self.register_adapter(ZedAdapter())
        self.register_adapter(GenericPlatformAdapter())

    def register_adapter(self, adapter: PlatformAdapter) -> None:
        """Register a custom or third-party platform adapter."""
        self._adapters[adapter.platform_id.lower()] = adapter

    def get_adapter(self, platform_id: str) -> Optional[PlatformAdapter]:
        """Retrieve adapter by platform identifier."""
        return self._adapters.get(platform_id.lower())

    def discover_all(self, workspace_root: Optional[Path] = None) -> List[DiscoveredPlatform]:
        """Probe host system for all registered platforms."""
        results: List[DiscoveredPlatform] = []
        for adapter in self._adapters.values():
            try:
                disc = adapter.discover(workspace_root)
                results.append(disc)
            except Exception as e:
                results.append(DiscoveredPlatform(
                    platform_id=adapter.platform_id,
                    display_name=adapter.display_name,
                    is_installed=False,
                    compatibility="ERROR",
                    details={"discovery_error": str(e)},
                ))
        return results

    def discover(self, platform_id: str, workspace_root: Optional[Path] = None) -> Optional[DiscoveredPlatform]:
        """Probe host system for a specific platform."""
        adapter = self.get_adapter(platform_id)
        if not adapter:
            return None
        return adapter.discover(workspace_root)

    def get_system_summary(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        """Generate a structured diagnostic summary of host OS and discovered platforms."""
        ws = workspace_root or Path.cwd()
        discovered = self.discover_all(ws)
        installed = [p for p in discovered if p.is_installed]
        configured = [p for p in discovered if p.is_configured]

        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_architecture": platform.machine(),
            "workspace_root": str(ws),
            "total_supported_platforms": len(discovered),
            "detected_installed_platforms": len(installed),
            "active_configured_platforms": len(configured),
            "installed_ids": [p.platform_id for p in installed],
            "configured_ids": [p.platform_id for p in configured],
        }
