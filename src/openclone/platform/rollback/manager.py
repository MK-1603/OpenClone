"""Rollback and state recovery management for OpenClone."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.platform.config.manager import ConfigurationManager


class RollbackManager:
    """Manages pre-update snapshots, state backups, and safe restoration."""

    def __init__(self, backup_root: Optional[Path] = None):
        self.config_mgr = ConfigurationManager()
        self.backup_root = backup_root or self._resolve_backup_root()

    def _resolve_backup_root(self) -> Path:
        """Resolve backup directory based on configuration path."""
        return self.config_mgr.config_path.parent / "backups"

    def create_snapshot(self, version: str, metadata: Optional[Dict[str, Any]] = None) -> Path:
        """Create a pre-update snapshot of configuration and platform metadata."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        snapshot_dir = self.backup_root / f"snapshot_{version}_{ts}"
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # 1. Backup Config
        if self.config_mgr.config_path.exists():
            shutil.copy2(self.config_mgr.config_path, snapshot_dir / "config.json")

        # 2. Write Snapshot Metadata
        meta_payload = {
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        (snapshot_dir / "snapshot_meta.json").write_text(json.dumps(meta_payload, indent=2), encoding="utf-8")
        return snapshot_dir

    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots ordered from newest to oldest."""
        if not self.backup_root.exists():
            return []

        snapshots: List[Dict[str, Any]] = []
        for d in sorted(self.backup_root.glob("snapshot_*"), reverse=True):
            if d.is_dir():
                meta_file = d / "snapshot_meta.json"
                if meta_file.exists():
                    try:
                        meta = json.loads(meta_file.read_text(encoding="utf-8"))
                        snapshots.append({
                            "directory": str(d),
                            "version": meta.get("version"),
                            "timestamp": meta.get("timestamp"),
                        })
                    except Exception:
                        pass
        return snapshots

    def restore_latest_snapshot(self) -> Dict[str, Any]:
        """Restore the most recent valid snapshot."""
        snapshots = self.list_snapshots()
        if not snapshots:
            return {"success": False, "message": "No snapshots found to restore"}

        target = Path(snapshots[0]["directory"])
        config_backup = target / "config.json"
        if config_backup.exists():
            shutil.copy2(config_backup, self.config_mgr.config_path)

        return {
            "success": True,
            "restored_version": snapshots[0]["version"],
            "restored_from": str(target),
            "message": f"Successfully restored state from {snapshots[0]['timestamp']}",
        }
