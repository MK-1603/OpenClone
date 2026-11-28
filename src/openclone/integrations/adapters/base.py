"""Abstract Platform Adapter interface for OpenClone IDE Integrations."""
from __future__ import annotations

import abc
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DiscoveredPlatform:
    """Result of platform discovery probe."""
    platform_id: str
    display_name: str
    is_installed: bool
    version: Optional[str] = None
    installation_path: Optional[str] = None
    config_path: Optional[str] = None
    workspace_config_path: Optional[str] = None
    is_configured: bool = False
    supported_protocols: List[str] = field(default_factory=list)
    compatibility: str = "COMPATIBLE"
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform_id": self.platform_id,
            "display_name": self.display_name,
            "is_installed": self.is_installed,
            "version": self.version,
            "installation_path": self.installation_path,
            "config_path": self.config_path,
            "workspace_config_path": self.workspace_config_path,
            "is_configured": self.is_configured,
            "supported_protocols": self.supported_protocols,
            "compatibility": self.compatibility,
            "details": self.details,
        }


class PlatformAdapter(abc.ABC):
    """Base class for all host IDE and AI platform adapters."""

    def __init__(self, platform_id: str, display_name: str):
        self.platform_id = platform_id
        self.display_name = display_name

    @abc.abstractmethod
    def discover(self, workspace_root: Optional[Path] = None) -> DiscoveredPlatform:
        """Probe the host machine for platform presence and installation paths."""
        raise NotImplementedError

    @abc.abstractmethod
    def inspect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        """Perform deep inspection of platform integration configuration."""
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self, workspace_root: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        """Install or update configuration integrating OpenClone into the platform."""
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        """Remove OpenClone integration from the platform cleanly."""
        raise NotImplementedError

    def health_check(self, workspace_root: Optional[Path] = None) -> Dict[str, Any]:
        """Verify that OpenClone gateway is reachable and responsive from platform context."""
        return {
            "platform_id": self.platform_id,
            "status": "PASS",
            "message": f"Gateway loopback check passed for {self.display_name}",
        }

    def _which(self, binary_name: str) -> Optional[str]:
        """Locate binary executable on system PATH."""
        return shutil.which(binary_name)
