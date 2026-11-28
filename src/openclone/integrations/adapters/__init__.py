"""Platform Adapters Package."""
from src.openclone.integrations.adapters.base import DiscoveredPlatform, PlatformAdapter
from src.openclone.integrations.adapters.antigravity import AntigravityAdapter
from src.openclone.integrations.adapters.vscode import VSCodeAdapter
from src.openclone.integrations.adapters.cursor import CursorAdapter
from src.openclone.integrations.adapters.jetbrains import JetBrainsAdapter
from src.openclone.integrations.adapters.zed import ZedAdapter
from src.openclone.integrations.adapters.windsurf import WindsurfAdapter
from src.openclone.integrations.adapters.generic import GenericPlatformAdapter

__all__ = [
    "PlatformAdapter",
    "DiscoveredPlatform",
    "AntigravityAdapter",
    "VSCodeAdapter",
    "CursorAdapter",
    "JetBrainsAdapter",
    "ZedAdapter",
    "WindsurfAdapter",
    "GenericPlatformAdapter",
]
