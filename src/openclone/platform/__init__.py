"""OpenClone Platform Management Layer.

Provides unified installation detection, runtime verification, persistent configuration,
transactional updates, rollback recovery, and component extensibility.
"""

from src.openclone.platform.config.manager import ConfigurationManager
from src.openclone.platform.installation.detector import detect_installation_mode, InstallationInfo
from src.openclone.platform.runtime.manager import RuntimeManager

__all__ = [
    "ConfigurationManager",
    "detect_installation_mode",
    "InstallationInfo",
    "RuntimeManager",
]
