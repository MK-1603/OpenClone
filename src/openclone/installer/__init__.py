"""OpenClone Global Plugin Installer and Host Management Engine."""

from src.openclone.installer.detector import detect_hosts, HostDetectionResult
from src.openclone.installer.engine import InstallerEngine
from src.openclone.installer.manifest import InstallationManifest

__all__ = [
    "detect_hosts",
    "HostDetectionResult",
    "InstallerEngine",
    "InstallationManifest",
]
