"""Component and extension lifecycle manager for OpenClone."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from src.openclone.platform.components.manifest import ComponentManifest
from src.openclone.platform.config.manager import ConfigurationManager


class ComponentManager:
    """Manages discovery, installation, activation, and removal of extension packs."""

    def __init__(self, components_dir: Optional[Path] = None):
        self.config_mgr = ConfigurationManager()
        self.components_dir = components_dir or self._resolve_components_dir()
        self.components_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_components_dir(self) -> Path:
        """Resolve component storage directory."""
        return self.config_mgr.config_path.parent / "components"

    def list_components(self) -> List[Dict[str, Any]]:
        """List all discovered components and active states."""
        components: List[Dict[str, Any]] = []
        for d in self.components_dir.iterdir():
            if d.is_dir():
                manifest_file = d / "component.json"
                if manifest_file.exists():
                    try:
                        cm = ComponentManifest.load_from_file(manifest_file)
                        enabled = not (d / ".disabled").exists()
                        components.append({
                            "id": cm.id,
                            "name": cm.name,
                            "version": cm.version,
                            "category": cm.category,
                            "enabled": enabled,
                            "path": str(d),
                        })
                    except Exception:
                        pass
        return components

    def inspect_component(self, component_id: str) -> Optional[ComponentManifest]:
        """Load manifest for a specific installed component."""
        target = self.components_dir / component_id / "component.json"
        if not target.exists():
            return None
        return ComponentManifest.load_from_file(target)

    def install_from_dir(self, source_dir: Path) -> Dict[str, Any]:
        """Install a component from a local directory containing component.json."""
        manifest_file = source_dir / "component.json"
        if not manifest_file.exists():
            return {"success": False, "message": "Source directory lacks component.json"}

        cm = ComponentManifest.load_from_file(manifest_file)
        dest = self.components_dir / cm.id
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source_dir, dest)

        return {
            "success": True,
            "component_id": cm.id,
            "version": cm.version,
            "message": f"Component '{cm.name}' installed successfully.",
        }

    def set_enabled(self, component_id: str, enable: bool) -> bool:
        """Enable or disable a component."""
        target = self.components_dir / component_id
        if not target.exists():
            return False
        disabled_marker = target / ".disabled"
        if enable:
            if disabled_marker.exists():
                disabled_marker.unlink()
        else:
            disabled_marker.touch()
        return True

    def remove_component(self, component_id: str) -> bool:
        """Safely remove an installed component."""
        target = self.components_dir / component_id
        if target.exists() and target.is_dir():
            shutil.rmtree(target)
            return True
        return False
