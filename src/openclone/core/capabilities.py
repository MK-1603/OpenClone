"""OpenClone Centralized Capability Management.

Allows every system component to declare, index, and discover capabilities with
semantic category tagging, risk evaluation, and security scopes.
"""
from __future__ import annotations

import enum
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

from src.openclone.integrations.capabilities import (
    CapabilityCategory,
    CapabilityRegistry,
    RiskClassification,
    get_canonical_registry,
)

logger = logging.getLogger("openclone.core.capabilities")


@dataclass
class CoreCapability:
    """Declared capability metadata."""
    capability_id: str
    name: str
    description: str
    domain: str
    category: CapabilityCategory
    risk_tier: RiskClassification = RiskClassification.READ_ONLY
    required_scopes: List[str] = field(default_factory=list)
    requires_human_approval: bool = False
    provider_module: str = "openclone.core"
    handler: Optional[Callable[..., Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.capability_id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "category": self.category.value,
            "risk_tier": self.risk_tier.value,
            "required_scopes": self.required_scopes,
            "requires_human_approval": self.requires_human_approval,
            "provider_module": self.provider_module,
        }


class UnifiedCapabilityRegistry:
    """Master capability registry unifying integration capabilities with core subsystem declarations."""

    _instance: Optional["UnifiedCapabilityRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.declared_capabilities: Dict[str, CoreCapability] = {}
        self.canonical_integration_registry = get_canonical_registry()
        self._populate_core_declared_capabilities()
        self._initialized = True

    def _populate_core_declared_capabilities(self) -> None:
        """Register the system's foundational capabilities across all 23 domains."""
        caps = [
            CoreCapability(
                capability_id="openclone.code_generation",
                name="Governed Code Generation",
                description="Synthesize production-quality software conforming to architectural blueprints",
                domain="software-engineering",
                category=CapabilityCategory.BACKEND,
                risk_tier=RiskClassification.HIGH_RISK_WRITE,
                required_scopes=["code:write"],
                requires_human_approval=True,
                provider_module="openclone.autonomous",
            ),
            CoreCapability(
                capability_id="openclone.architecture_analysis",
                name="Architecture & Systems Analysis",
                description="Evaluate architectural styles, monolithic vs microservice trade-offs, and ADRs",
                domain="software-architecture",
                category=CapabilityCategory.ARCHITECTURE,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["architecture:read"],
                provider_module="openclone.system_design",
            ),
            CoreCapability(
                capability_id="openclone.reverse_engineering",
                name="Static Codebase Reverse Engineering",
                description="Inspect repositories, extract AST symbols, API routes, data models, and technical debt",
                domain="reverse-engineering",
                category=CapabilityCategory.PROJECT_DISCOVERY,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["repo:read"],
                provider_module="openclone.reverse_engineering",
            ),
            CoreCapability(
                capability_id="openclone.database_design",
                name="Relational & NoSQL Database Design",
                description="Synthesize database models, zero-downtime migration plans, and RLS policies",
                domain="database-engineering",
                category=CapabilityCategory.BACKEND,
                risk_tier=RiskClassification.LOW_RISK_WRITE,
                required_scopes=["db:plan"],
                provider_module="openclone.backend",
            ),
            CoreCapability(
                capability_id="openclone.api_development",
                name="API Contract & Protocol Design",
                description="Generate REST, OpenAPI 3.1, gRPC, and WebSocket interface specifications",
                domain="api-engineering",
                category=CapabilityCategory.BACKEND,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["api:design"],
                provider_module="openclone.connectors",
            ),
            CoreCapability(
                capability_id="openclone.security_analysis",
                name="STRIDE Threat Modeling & Security Review",
                description="Identify security vulnerabilities, threat vectors, and zero-trust perimeter controls",
                domain="security-engineering",
                category=CapabilityCategory.SECURITY,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["security:audit"],
                provider_module="openclone.security",
            ),
            CoreCapability(
                capability_id="openclone.quality_verification",
                name="Independent Quality & Test Verification",
                description="Execute automated test suites, evaluate quality gates, and attest completion",
                domain="quality-engineering",
                category=CapabilityCategory.EVIDENCE_VERIFICATION,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["test:run"],
                provider_module="openclone.testing",
            ),
            CoreCapability(
                capability_id="openclone.ui_ux_design",
                name="Design System & UI/UX Architecture",
                description="Compute design tokens, typography scales, responsive breakpoints, and WCAG contrast",
                domain="ux-ui-engineering",
                category=CapabilityCategory.UI_UX,
                risk_tier=RiskClassification.READ_ONLY,
                required_scopes=["design:read"],
                provider_module="openclone.branding",
            ),
        ]
        for c in caps:
            self.declared_capabilities[c.capability_id] = c

    def register_capability(self, capability: CoreCapability) -> None:
        self.declared_capabilities[capability.capability_id] = capability

    def get_capability(self, capability_id: str) -> Optional[CoreCapability]:
        return self.declared_capabilities.get(capability_id)

    def list_capabilities(self, domain: Optional[str] = None, category: Optional[CapabilityCategory] = None) -> List[CoreCapability]:
        results = list(self.declared_capabilities.values())
        if domain:
            results = [c for c in results if c.domain.lower() == domain.lower()]
        if category:
            results = [c for c in results if c.category == category]
        return results

    def match_capabilities(self, required_tags: List[str]) -> List[CoreCapability]:
        matched = []
        for c in self.declared_capabilities.values():
            text = f"{c.capability_id} {c.name} {c.description} {c.domain}".lower()
            if any(tag.lower() in text for tag in required_tags):
                matched.append(c)
        return matched

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "HEALTHY",
            "declared_count": len(self.declared_capabilities),
            "canonical_integration_count": len(self.canonical_integration_registry.list_capabilities()),
        }
