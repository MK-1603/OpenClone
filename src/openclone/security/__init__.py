"""OpenClone Security, Firewall & Zero-Trust Architecture Module."""
from __future__ import annotations

from src.openclone.security.agent_gateway import (
    AgentSecurityGateway,
    AgentSecurityViolationError,
)
from src.openclone.security.database import (
    DatabaseSecurityError,
    DatabaseSecurityGuard,
)
from src.openclone.security.env import (
    SecurityValidationError,
    audit_template_safety,
    load_safe_config,
    validate_client_bundle_safety,
    validate_environment,
)
from src.openclone.security.firewall import (
    FirewallSecurityError,
    NetworkFirewall,
    SSRFSecurityError,
)
from src.openclone.security.monitoring import (
    SecurityLedgerTamperError,
    SecurityMonitor,
)
from src.openclone.security.waf import (
    RateLimiter,
    WafFinding,
    WafInspector,
    WafSecurityError,
    get_security_headers,
    sanitize_api_error,
)

__all__ = [
    # Environment
    "SecurityValidationError",
    "validate_environment",
    "load_safe_config",
    "validate_client_bundle_safety",
    "audit_template_safety",
    # Network Firewall & SSRF
    "NetworkFirewall",
    "FirewallSecurityError",
    "SSRFSecurityError",
    # WAF & API Security
    "WafInspector",
    "WafFinding",
    "WafSecurityError",
    "RateLimiter",
    "get_security_headers",
    "sanitize_api_error",
    # Agent Firewall Gateway
    "AgentSecurityGateway",
    "AgentSecurityViolationError",
    # Database Security
    "DatabaseSecurityGuard",
    "DatabaseSecurityError",
    # Security Monitoring
    "SecurityMonitor",
    "SecurityLedgerTamperError",
]
