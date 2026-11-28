"""Transactional platform update engine for OpenClone."""
from __future__ import annotations

import json
import logging
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from src.openclone.platform.config.manager import ConfigurationManager
from src.openclone.platform.installation.detector import detect_installation_mode
from src.openclone.platform.updates.channels import ReleaseChannel
from src.openclone.platform.updates.manifest import ReleaseManifest, verify_file_sha256

logger = logging.getLogger("openclone.updates")

CANONICAL_MANIFEST_ENDPOINT = "https://raw.githubusercontent.com/MK-1603/OpenClone/main/framework/releases/manifest.json"


@dataclass
class UpdateCheckResult:
    """Result of checking for new platform updates."""
    update_available: bool
    current_version: str
    latest_version: str
    channel: str
    release_notes_url: Optional[str] = None
    manifest: Optional[ReleaseManifest] = None
    message: str = ""


class UpdateEngine:
    """Orchestrates update discovery, transactional staging, and execution."""

    def __init__(self, config_manager: Optional[ConfigurationManager] = None):
        self.config_mgr = config_manager or ConfigurationManager()
        self.install_info = detect_installation_mode()

    def get_channel(self) -> ReleaseChannel:
        """Get currently configured update channel."""
        ch_str = self.config_mgr.get_setting("update.channel", "stable")
        return ReleaseChannel.normalize(ch_str)

    def set_channel(self, channel_name: str) -> ReleaseChannel:
        """Set update channel in user configuration."""
        ch = ReleaseChannel.normalize(channel_name)
        self.config_mgr.set_setting("update.channel", ch.value)
        return ch

    def check_for_updates(self, manifest_override: Optional[Dict[str, Any]] = None) -> UpdateCheckResult:
        """Check for updates matching current channel and platform."""
        current_ver = self.install_info.package_version
        channel = self.get_channel()

        # Load manifest
        if manifest_override:
            manifest_data = manifest_override
        else:
            try:
                manifest_url = self.config_mgr.get_setting("update.manifest_url") or CANONICAL_MANIFEST_ENDPOINT
                req = urllib.request.Request(manifest_url, headers={"User-Agent": "OpenClone-UpdateEngine/1.0.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    manifest_data = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                return UpdateCheckResult(
                    update_available=False,
                    current_version=current_ver,
                    latest_version=current_ver,
                    channel=channel.value,
                    message=f"Update discovery failed: {e}",
                )

        try:
            manifest = ReleaseManifest.from_dict(manifest_data)
        except Exception as e:
            return UpdateCheckResult(
                update_available=False,
                current_version=current_ver,
                latest_version=current_ver,
                channel=channel.value,
                message=f"Invalid release manifest: {e}",
            )

        # Check channel match
        if manifest.channel != channel.value and channel != ReleaseChannel.NIGHTLY:
            return UpdateCheckResult(
                update_available=False,
                current_version=current_ver,
                latest_version=current_ver,
                channel=channel.value,
                message=f"Latest release ({manifest.version}) is on channel '{manifest.channel}', current is '{channel.value}'",
            )

        # Version comparison
        update_available = manifest.version != current_ver
        return UpdateCheckResult(
            update_available=update_available,
            current_version=current_ver,
            latest_version=manifest.version,
            channel=channel.value,
            release_notes_url=manifest.release_notes_url,
            manifest=manifest,
            message=f"New version {manifest.version} available" if update_available else "System is up to date",
        )

    def apply_update(self, check_result: UpdateCheckResult) -> Dict[str, Any]:
        """Apply update respecting installation ownership."""
        if not check_result.update_available or not check_result.manifest:
            return {"success": False, "message": "No update available to apply"}

        mode = self.install_info.mode

        # Route 1: Pip / Pipx Package Installations
        if mode == "python-pipx":
            cmd = ["pipx", "upgrade", "openclone"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "success": res.returncode == 0,
                "mode": mode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "message": "Pipx upgrade complete" if res.returncode == 0 else "Pipx upgrade failed",
            }
        elif mode in ("python-pip", "python-venv"):
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "openclone"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "success": res.returncode == 0,
                "mode": mode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "message": "Pip upgrade complete" if res.returncode == 0 else "Pip upgrade failed",
            }
        elif mode == "source-checkout":
            cmd = ["git", "pull", "--ff-only", "origin", "main"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "success": res.returncode == 0,
                "mode": mode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "message": "Source updated via git" if res.returncode == 0 else "Git pull failed",
            }
        else:
            return {
                "success": False,
                "mode": mode,
                "message": f"Manual update required for installation mode '{mode}'. Visit: {check_result.release_notes_url or 'https://github.com/MK-1603/OpenClone/releases'}",
            }
