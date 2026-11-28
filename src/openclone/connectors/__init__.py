"""OpenClone Universal AI Assistant Connector package."""
from src.openclone.connectors.contracts import (
    ConnectionState,
    NormalizedRequest,
    NormalizedResponse,
    PlatformConfig,
    PlatformType,
    ProtocolType,
    UniversalConnectorConfig,
)
from src.openclone.connectors.base import BasePlatformAdapter
from src.openclone.connectors.core import UniversalAIAssistantConnector

__all__ = [
    "ConnectionState",
    "NormalizedRequest",
    "NormalizedResponse",
    "PlatformConfig",
    "PlatformType",
    "ProtocolType",
    "UniversalConnectorConfig",
    "BasePlatformAdapter",
    "UniversalAIAssistantConnector",
]
