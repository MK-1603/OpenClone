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
]
