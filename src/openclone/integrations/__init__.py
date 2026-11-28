"""OpenClone Universal AI Tool Integration & Global Plugin Ecosystem."""

from src.openclone.integrations.capabilities import (
    Capability,
    CapabilityCategory,
    RiskClassification,
    IntegrationSurface,
    CapabilityRegistry,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import (
    IntegrationGateway,
    AuthContext,
    PolicyDecision,
    PolicyVerdict,
)
from src.openclone.integrations.openapi import generate_openapi_spec, dispatch_rest_request
from src.openclone.integrations.registry import (
    PlatformMaturity,
    PlatformDescriptor,
    PlatformCapabilityRegistry,
    get_platform_registry,
)
from src.openclone.integrations.discovery import PlatformDiscoveryEngine
from src.openclone.integrations.manager import IntegrationManager
from src.openclone.integrations.acp import ACPAdapter, ACPSession

def get_rest_gateway(*args, **kwargs):
    from src.openclone.integrations.rest import OpenCloneRESTGateway
    return OpenCloneRESTGateway(*args, **kwargs)

def get_universal_ai_connector(*args, **kwargs):
    from src.openclone.connectors.core import UniversalAIAssistantConnector
    return UniversalAIAssistantConnector(*args, **kwargs)

__all__ = [
    "Capability",
    "CapabilityCategory",
    "RiskClassification",
    "IntegrationSurface",
    "CapabilityRegistry",
    "get_canonical_registry",
    "IntegrationGateway",
    "AuthContext",
    "PolicyDecision",
    "PolicyVerdict",
    "generate_openapi_spec",
    "dispatch_rest_request",
    "PlatformMaturity",
    "PlatformDescriptor",
    "PlatformCapabilityRegistry",
    "get_platform_registry",
    "PlatformDiscoveryEngine",
    "IntegrationManager",
    "ACPAdapter",
    "ACPSession",
    "OpenCloneRESTGateway",
    "get_universal_ai_connector",
]
