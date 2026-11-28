"""Central Integration Manager for OpenClone Universal Platform Ecosystem."""
from __future__ import annotations

import json
import logging
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.integrations.discovery import PlatformDiscoveryEngine
from src.openclone.integrations.registry import PlatformCapabilityRegistry, get_platform_registry

logger = logging.getLogger("openclone.integrations.manager")


class IntegrationManager:
    """Manages discovery, connection, configuration, safety backups, and health checks for IDEs."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.discovery_engine = PlatformDiscoveryEngine()
        self.registry: PlatformCapabilityRegistry = get_platform_registry()
        self.backups_dir = self.workspace_root / ".openclone" / "backups"

    def discover_platforms(self) -> List[Dict[str, Any]]:
        """Discover installed platforms on host system."""
        results = self.discovery_engine.discover_all(self.workspace_root)
        return [p.to_dict() for p in results]

    def list_platforms(self) -> List[Dict[str, Any]]:
        """List all supported platforms and their registry declarations."""
        descriptors = self.registry.list_all()
        return [d.to_dict() for d in descriptors]

    def inspect_platform(self, platform_id: str) -> Dict[str, Any]:
        """Inspect specific platform status and configuration."""
        adapter = self.discovery_engine.get_adapter(platform_id)
        if not adapter:
            descriptor = self.registry.get(platform_id)
            if not descriptor:
                raise ValueError(f"Unknown platform: '{platform_id}'")
            return {
                "platform_id": platform_id,
                "status": "UNSUPPORTED_OR_NO_ADAPTER",
                "descriptor": descriptor.to_dict(),
            }
        inspection = adapter.inspect(self.workspace_root)
        desc = self.registry.get(platform_id)
        if desc:
            inspection["descriptor"] = desc.to_dict()
        return inspection

    def _create_backup(self, platform_id: str, file_path: Path) -> Optional[Path]:
        """Create a timestamped safety backup of a configuration file."""
        if not file_path.exists():
            return None
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        backup_file = self.backups_dir / f"{platform_id}_{timestamp}_{file_path.name}"
        shutil.copy2(file_path, backup_file)
        return backup_file

    def connect_platform(self, platform_id: str, is_global: bool = False, **kwargs) -> Dict[str, Any]:
        """Configure platform connection with safety backup."""
        adapter = self.discovery_engine.get_adapter(platform_id)
        if not adapter:
            raise ValueError(f"Unknown platform adapter: '{platform_id}'")

        # Probe for existing configuration file to back up
        disc = adapter.discover(self.workspace_root)
        if disc.workspace_config_path and not is_global:
            p = Path(disc.workspace_config_path)
            self._create_backup(platform_id, p)
        elif disc.config_path:
            p = Path(disc.config_path)
            if p.is_file():
                self._create_backup(platform_id, p)

        res = adapter.connect(self.workspace_root, is_global=is_global, **kwargs)
        res["health"] = adapter.health_check(self.workspace_root)
        return res

    def disconnect_platform(self, platform_id: str, is_global: bool = False, **kwargs) -> Dict[str, Any]:
        """Remove platform integration safely."""
        adapter = self.discovery_engine.get_adapter(platform_id)
        if not adapter:
            raise ValueError(f"Unknown platform adapter: '{platform_id}'")
        return adapter.disconnect(self.workspace_root, is_global=is_global, **kwargs)

    def install_integration(self, platform_id: str, is_global: bool = False, **kwargs) -> Dict[str, Any]:
        """Guided installation of platform integration."""
        return self.connect_platform(platform_id, is_global=is_global, **kwargs)

    def remove_integration(self, platform_id: str, is_global: bool = False, **kwargs) -> Dict[str, Any]:
        """Guided removal of platform integration."""
        return self.disconnect_platform(platform_id, is_global=is_global, **kwargs)

    def health_check(self, platform_id: Optional[str] = None) -> Dict[str, Any]:
        """Run health check on a specific platform or all platforms."""
        if platform_id:
            adapter = self.discovery_engine.get_adapter(platform_id)
            if not adapter:
                return {"platform_id": platform_id, "status": "FAIL", "message": f"Adapter not found: '{platform_id}'"}
            return adapter.health_check(self.workspace_root)

        results = {}
        for p in self.discovery_engine.discover_all(self.workspace_root):
            adapter = self.discovery_engine.get_adapter(p.platform_id)
            if adapter:
                results[p.platform_id] = adapter.health_check(self.workspace_root)
        return {"health_checks": results, "status": "COMPLETED"}

    def get_status(self) -> Dict[str, Any]:
        """Get ecosystem status across all platforms."""
        discovered = self.discovery_engine.discover_all(self.workspace_root)
        return {
            "workspace_root": str(self.workspace_root),
            "platforms": [
                {
                    "platform_id": p.platform_id,
                    "display_name": p.display_name,
                    "is_installed": p.is_installed,
                    "is_configured": p.is_configured,
                    "compatibility": p.compatibility,
                }
                for p in discovered
            ],
            "total_supported": len(discovered),
            "total_configured": sum(1 for p in discovered if p.is_configured),
        }
