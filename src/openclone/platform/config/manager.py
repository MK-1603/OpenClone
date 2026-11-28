"""Centralized file-based configuration manager for OpenClone."""
from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.platform.config.migrations import migrate_config_dict
from src.openclone.platform.config.schema import PlatformUserConfig


class ConfigurationManager:
    """Manages persistent user settings, migrations, and backups."""

    def __init__(self, config_path: Optional[Path] = None, portable_mode: bool = False):
        self.portable_mode = portable_mode
        self.config_path = config_path or self._resolve_default_path()

    def _resolve_default_path(self) -> Path:
        """Resolve standard or portable configuration file path with permission fallbacks."""
        # 1. Portable Mode Check
        if self.portable_mode or Path("./data").is_dir():
            return Path("./data/config.json").resolve()

        # 2. Explicit Environment Variable (OpenClone primary, OpenKryvex fallback)
        env_path = os.environ.get("OPENCLONE_CONFIG") or os.environ.get("OPENKRYVEX_CONFIG")
        if env_path:
            return Path(env_path).resolve()

        # 3. Candidate Paths
        candidates = [
            Path.home() / ".openclone" / "config.json",
        ]
        if sys.platform == "win32":
            appdata = os.environ.get("APPDATA")
            if appdata:
                candidates.insert(0, Path(appdata) / "OpenClone" / "config.json")
                # Fallback to existing OpenKryvex config if present
                if (Path(appdata) / "OpenKryvex" / "config.json").exists():
                    candidates.append(Path(appdata) / "OpenKryvex" / "config.json")

        if (Path.home() / ".openkryvex" / "config.json").exists():
            candidates.append(Path.home() / ".openkryvex" / "config.json")

        for c in candidates:
            try:
                c.parent.mkdir(parents=True, exist_ok=True)
                test_file = c.parent / ".write_test"
                test_file.touch()
                test_file.unlink(missing_ok=True)
                return c.resolve()
            except OSError:
                continue

        # Fallback to local workspace hidden directory
        local_dir = Path.cwd() / ".openclone"
        if not local_dir.exists() and (Path.cwd() / ".openkryvex").exists():
            local_dir = Path.cwd() / ".openkryvex"
        local_dir.mkdir(parents=True, exist_ok=True)
        return (local_dir / "config.json").resolve()

    def load_config(self) -> PlatformUserConfig:
        """Load, migrate, and validate persistent configuration from disk."""
        if not self.config_path.exists():
            default_cfg = PlatformUserConfig()
            self.save_config(default_cfg)
            return default_cfg

        try:
            raw_text = self.config_path.read_text(encoding="utf-8")
            data = json.loads(raw_text) if raw_text.strip() else {}
        except Exception:
            # Backup corrupted file and return safe defaults
            self._backup_file("corrupted")
            default_cfg = PlatformUserConfig()
            self.save_config(default_cfg)
            return default_cfg

        # Check for migration
        migrated = migrate_config_dict(data, target_version="1.0.0")
        if migrated != data:
            self._backup_file("pre-migration")
            cfg = PlatformUserConfig.from_dict(migrated)
            self.save_config(cfg)
            return cfg

        return PlatformUserConfig.from_dict(data)

    def save_config(self, config: PlatformUserConfig) -> None:
        """Persist configuration object to disk with atomic write."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = self.config_path.with_suffix(".tmp")
            payload = json.dumps(config.to_dict(), indent=2, sort_keys=True)
            tmp_path.write_text(payload, encoding="utf-8")
            tmp_path.replace(self.config_path)
        except OSError as e:
            # Fallback to local workspace if primary path fails
            try:
                fallback_path = Path.cwd() / ".openkryvex" / "config.json"
                fallback_path.parent.mkdir(parents=True, exist_ok=True)
                tmp_path = fallback_path.with_suffix(".tmp")
                payload = json.dumps(config.to_dict(), indent=2, sort_keys=True)
                tmp_path.write_text(payload, encoding="utf-8")
                tmp_path.replace(fallback_path)
                self.config_path = fallback_path
            except OSError:
                pass

    def _backup_file(self, tag: str) -> Optional[Path]:
        """Create a timestamped backup of the current configuration file."""
        if not self.config_path.exists():
            return None
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_dir = self.config_path.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"config_{tag}_{ts}.json"
        shutil.copy2(self.config_path, backup_file)
        return backup_file

    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """Retrieve a nested setting using dot notation (e.g. 'update.channel')."""
        cfg_dict = self.load_config().to_dict()
        tokens = key_path.split(".")
        current = cfg_dict
        for t in tokens:
            if isinstance(current, dict) and t in current:
                current = current[t]
            else:
                return default
        return current

    def set_setting(self, key_path: str, value: Any) -> None:
        """Set a nested setting using dot notation and persist."""
        cfg = self.load_config()
        cfg_dict = cfg.to_dict()
        tokens = key_path.split(".")
        current = cfg_dict
        for t in tokens[:-1]:
            if t not in current or not isinstance(current[t], dict):
                current[t] = {}
            current = current[t]
        current[tokens[-1]] = value
        updated_cfg = PlatformUserConfig.from_dict(cfg_dict)
        self.save_config(updated_cfg)
