"""Installation ownership and state tracking manifest."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class HostInstallRecord:
    """Tracking record for an installed host adapter."""
    host_id: str
    scope: str
    installed_at: str
    core_version: str
    installed_files: Dict[str, str] = field(default_factory=dict)  # rel_path -> sha256
    backups: Dict[str, str] = field(default_factory=dict)  # rel_path -> backup_path


class InstallationManifest:
    """Manages the local .openclone/install-manifest.json state ledger."""

    def __init__(self, core_version: str = "1.0.0"):
        self.schema_version = "1.0.0"
        self.core_version = core_version
        self.hosts: Dict[str, HostInstallRecord] = {}

    @classmethod
    def manifest_path(cls, root: Path) -> Path:
        return root / ".openclone" / "install-manifest.json"

    @classmethod
    def load(cls, root: Path) -> "InstallationManifest":
        p = cls.manifest_path(root)
        inst = cls()
        if not p.exists():
            return inst
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            inst.schema_version = data.get("schema_version", "1.0.0")
            inst.core_version = data.get("core_version", "1.0.0")
            hosts_data = data.get("hosts", {})
            for hid, hrec in hosts_data.items():
                inst.hosts[hid] = HostInstallRecord(
                    host_id=hrec.get("host_id", hid),
                    scope=hrec.get("scope", "workspace"),
                    installed_at=hrec.get("installed_at", ""),
                    core_version=hrec.get("core_version", "1.0.0"),
                    installed_files=hrec.get("installed_files", {}),
                    backups=hrec.get("backups", {}),
                )
        except Exception:
            pass
        return inst

    def save(self, root: Path) -> None:
        p = self.manifest_path(root)
        p.parent.mkdir(parents=True, exist_ok=True)
        out = {
            "schema_version": self.schema_version,
            "core_version": self.core_version,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "hosts": {hid: asdict(rec) for hid, rec in self.hosts.items()},
        }
        p.write_text(json.dumps(out, indent=2), encoding="utf-8")

    def record_install(
        self,
        host_id: str,
        scope: str,
        installed_files: Dict[str, str],
        backups: Dict[str, str],
    ) -> None:
        self.hosts[host_id] = HostInstallRecord(
            host_id=host_id,
            scope=scope,
            installed_at=datetime.now(timezone.utc).isoformat(),
            core_version=self.core_version,
            installed_files=installed_files,
            backups=backups,
        )

    def remove_host(self, host_id: str) -> Optional[HostInstallRecord]:
        return self.hosts.pop(host_id, None)

    def verify_integrity(self, root: Path, host_id: str) -> Dict[str, Any]:
        """Verify that files recorded in the manifest still match physical hashes."""
        rec = self.hosts.get(host_id)
        if not rec:
            return {"installed": False, "intact": False, "missing": [], "modified": []}

        missing = []
        modified = []
        for rel, expected_hash in rec.installed_files.items():
            fpath = root / rel
            if not fpath.exists():
                missing.append(rel)
                continue
            cur_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if cur_hash != expected_hash:
                modified.append(rel)

        return {
            "installed": True,
            "intact": len(missing) == 0 and len(modified) == 0,
            "total_files": len(rec.installed_files),
            "missing": missing,
            "modified": modified,
        }
