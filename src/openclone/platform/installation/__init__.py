"""Installation management module."""
from src.openclone.platform.installation.detector import detect_installation_mode, InstallationInfo
from src.openclone.platform.installation.manager import PlatformInstallationManager

__all__ = ["detect_installation_mode", "InstallationInfo", "PlatformInstallationManager"]
