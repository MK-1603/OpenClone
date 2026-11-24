"""OpenClone Network Firewall & Traffic Security Engine.

Enforces zero-trust inbound/outbound traffic policies, SSRF prevention,
metadata endpoint protection, and network segmentation.
"""
from __future__ import annotations

import ipaddress
import re
import socket
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse


class FirewallSecurityError(Exception):
    """Raised when network traffic violates firewall policy."""
    pass


class SSRFSecurityError(FirewallSecurityError):
    """Raised when an outbound URL violates SSRF protection rules."""
    pass


# Default allowed inbound application ports
DEFAULT_ALLOWED_INBOUND_PORTS: Set[int] = {80, 443, 3000, 8000, 8080}

# Prohibited internal service ports that must never bind publicly (0.0.0.0)
RESTRICTED_INTERNAL_PORTS: Dict[int, str] = {
    5432: "PostgreSQL Database",
    3306: "MySQL Database",
    6379: "Redis Cache / Queue",
    27017: "MongoDB Database",
    9200: "Elasticsearch",
    2375: "Docker Daemon (Unencrypted)",
    2376: "Docker Daemon (TLS)",
    22: "SSH Management",
}

# Cloud Metadata service hostnames and IPs
CLOUD_METADATA_TARGETS: Set[str] = {
    "169.254.169.254",
    "metadata.google.internal",
    "metadata.aws.internal",
    "169.254.169.250",
    "fd00:ec2::254",
}

# RFC1918 and link-local private network ranges
PRIVATE_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


class NetworkFirewall:
    """Zero-trust Network Firewall and Traffic Controller."""

    def __init__(
        self,
        allowed_inbound_ports: Optional[Set[int]] = None,
        allowed_outbound_domains: Optional[List[str]] = None,
    ):
        self.allowed_inbound_ports = allowed_inbound_ports or set(DEFAULT_ALLOWED_INBOUND_PORTS)
        self.allowed_outbound_domains = [d.lower() for d in allowed_outbound_domains] if allowed_outbound_domains else None

    def validate_inbound_port(self, port: int) -> bool:
        """Validate if an inbound port is allowed under default-deny policy."""
        if port not in self.allowed_inbound_ports:
            raise FirewallSecurityError(
                f"Inbound traffic blocked: Port {port} is not permitted under default-deny policy. "
                f"Allowed ports: {sorted(self.allowed_inbound_ports)}"
            )
        return True

    def validate_service_binding(self, service_name: str, host: str, port: int) -> bool:
        """Prevent internal database and cache ports from binding to public interfaces."""
        host_clean = host.strip().lower()
        is_public_binding = host_clean in ("0.0.0.0", "::", "")

        if port in RESTRICTED_INTERNAL_PORTS and is_public_binding:
            service_desc = RESTRICTED_INTERNAL_PORTS[port]
            raise FirewallSecurityError(
                f"Public exposure blocked: Internal service '{service_name}' ({service_desc}) "
                f"attempted to bind port {port} to public interface '{host}'. Must bind to loopback (127.0.0.1) only."
            )
        return True

    def validate_outbound_url(
        self,
        url: str,
        allowed_domains: Optional[List[str]] = None,
        allow_local: bool = False,
    ) -> bool:
        """Enforce strict SSRF protection and outbound destination controls.

        Blocks:
          - Non-HTTP(S) protocols (file://, gopher://, ftp://, dict://)
          - Cloud metadata endpoints (169.254.169.254, metadata.google.internal)
          - Private RFC1918 / loopback IP addresses (unless allow_local=True)
          - Domains outside allowed_domains if allowlist is configured
        """
        if not url:
            raise SSRFSecurityError("Outbound request rejected: Empty URL provided.")

        try:
            parsed = urlparse(url)
        except Exception as e:
            raise SSRFSecurityError(f"Malformed URL: {e}")

        # 1. Protocol Scheme Validation
        scheme = (parsed.scheme or "").lower()
        if scheme not in ("http", "https"):
            raise SSRFSecurityError(
                f"SSRF violation: Prohibited protocol scheme '{scheme}'. Only HTTP and HTTPS are permitted."
            )

        hostname = (parsed.hostname or "").strip().lower()
        if not hostname:
            raise SSRFSecurityError("SSRF violation: Missing hostname in URL.")

        # 2. Cloud Metadata Endpoint Protection
        if hostname in CLOUD_METADATA_TARGETS or hostname.endswith(".internal"):
            raise SSRFSecurityError(
                f"SSRF violation: Access to cloud metadata service '{hostname}' is strictly blocked."
            )

        # 3. IP Resolution & Private Network Blocking
        try:
            # Check if hostname is directly an IP literal
            ip_obj = ipaddress.ip_address(hostname)
            is_ip = True
        except ValueError:
            is_ip = False
            ip_obj = None

        if is_ip and ip_obj:
            if not allow_local:
                for net in PRIVATE_NETWORKS:
                    if ip_obj in net:
                        raise SSRFSecurityError(
                            f"SSRF violation: Outbound request to private network IP '{ip_obj}' is blocked."
                        )
        else:
            # Check for common localhost aliases
            if not allow_local and hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
                raise SSRFSecurityError(
                    f"SSRF violation: Outbound request to loopback host '{hostname}' is blocked."
                )

        # 4. Domain Allowlist Validation
        effective_domains = allowed_domains or self.allowed_outbound_domains
        if effective_domains:
            domain_allowed = any(
                hostname == allowed.lower() or hostname.endswith("." + allowed.lower())
                for allowed in effective_domains
            )
            if not domain_allowed:
                raise SSRFSecurityError(
                    f"Outbound firewall violation: Host '{hostname}' is not in the allowed domain list: {effective_domains}"
                )

        return True

    @staticmethod
    def get_network_segmentation_rules() -> Dict[str, Any]:
        """Return reference network segmentation architecture for container deployments."""
        return {
            "networks": {
                "public-net": {"driver": "bridge", "internal": False, "description": "Public ingress to API/Web only"},
                "app-net": {"driver": "bridge", "internal": True, "description": "Application services and workers"},
                "db-net": {"driver": "bridge", "internal": True, "description": "Databases and caches isolated from internet"},
                "sandbox-net": {"driver": "bridge", "internal": True, "description": "Isolated agent subprocess executions"},
            }
        }
