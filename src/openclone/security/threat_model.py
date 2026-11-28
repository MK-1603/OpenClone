"""OpenClone Planning-Time STRIDE Threat Modeling Engine.

Analyzes architectural blueprints, data sensitivity, and external integration surfaces
to synthesize threat matrices and countermeasure specifications.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ThreatCategory(str, enum.Enum):
    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"


class ThreatSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ThreatItem:
    threat_id: str
    category: ThreatCategory
    title: str
    description: str
    target_component: str
    severity: ThreatSeverity
    countermeasure: str
    verification_check: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "threat_id": self.threat_id,
            "category": self.category.value,
            "title": self.title,
            "description": self.description,
            "target_component": self.target_component,
            "severity": self.severity.value,
            "countermeasure": self.countermeasure,
            "verification_check": self.verification_check,
        }


class STRIDEThreatModeler:
    """Synthesizes planning-time STRIDE threat models based on architecture parameters."""

    @classmethod
    def evaluate(
        cls,
        project_name: str,
        architecture_pattern: str,
        has_auth: bool = True,
        is_multi_tenant: bool = False,
        has_external_api: bool = True,
    ) -> Dict[str, Any]:
        threats: List[ThreatItem] = []
        idx = 1

        # 1. Spoofing
        if has_auth:
            threats.append(ThreatItem(
                threat_id=f"THR-{idx:03d}",
                category=ThreatCategory.SPOOFING,
                title="JWT Forgery & Session Hijacking",
                description="Attacker creates unauthorized JWT tokens or replays intercepted bearer tokens.",
                target_component="Auth Gateway / API Handlers",
                severity=ThreatSeverity.HIGH,
                countermeasure="Enforce RS256/EdDSA asymmetric signature verification with short token lifespans (15m) and rotating refresh keys.",
                verification_check="Automated security test verifying rejection of unsigned or HMAC-downgraded tokens.",
            ))
            idx += 1

        # 2. Tampering
        threats.append(ThreatItem(
            threat_id=f"THR-{idx:03d}",
            category=ThreatCategory.TAMPERING,
            title="Payload & SQL/ORM Injection",
            description="Malicious input vectors bypass basic client-side validation to manipulate queries or state.",
            target_component="Database & API Ingress",
            severity=ThreatSeverity.CRITICAL,
            countermeasure="Strict Pydantic / JSON-Schema validation on ingress; parameterized ORM queries only (zero string concatenation).",
            verification_check="Semgrep & Bandit static analysis passing with zero high-severity findings.",
        ))
        idx += 1

        # 3. Repudiation
        threats.append(ThreatItem(
            threat_id=f"THR-{idx:03d}",
            category=ThreatCategory.REPUDIATION,
            title="Unverifiable High-Privilege State Mutations",
            description="Users dispute administrative actions due to absent or forgeable audit logs.",
            target_component="Audit Ledger Subsystem",
            severity=ThreatSeverity.MEDIUM,
            countermeasure="Write-only hash-chained SQLite audit ledger recording user ID, action, SHA-256 payload digest, and timestamp.",
            verification_check="Ledger verification test confirming tamper-detection on modified records.",
        ))
        idx += 1

        # 4. Information Disclosure
        threats.append(ThreatItem(
            threat_id=f"THR-{idx:03d}",
            category=ThreatCategory.INFORMATION_DISCLOSURE,
            title="Credential Leakage via Error Stack Traces",
            description="Unhandled backend exceptions leak environment secrets or database schemas to clients.",
            target_component="Error Handling Middleware",
            severity=ThreatSeverity.HIGH,
            countermeasure="Global exception handler intercepting errors and sanitizing all API responses to generic error codes.",
            verification_check="Automated test confirming zero tracebacks in HTTP 500 response bodies.",
        ))
        idx += 1

        # 5. Denial of Service
        threats.append(ThreatItem(
            threat_id=f"THR-{idx:03d}",
            category=ThreatCategory.DENIAL_OF_SERVICE,
            title="Resource Starvation & Endpoint Flooding",
            description="Unauthenticated flooding of expensive computation or database endpoints exhausting worker threads.",
            target_component="Reverse Proxy / Rate Limiter",
            severity=ThreatSeverity.HIGH,
            countermeasure="Token-bucket rate limiting (e.g. 100 req/min/IP) and explicit connection read/write timeouts (5s).",
            verification_check="Rate limiter load test asserting HTTP 429 Too Many Requests response under burst traffic.",
        ))
        idx += 1

        # 6. Elevation of Privilege
        if is_multi_tenant:
            threats.append(ThreatItem(
                threat_id=f"THR-{idx:03d}",
                category=ThreatCategory.ELEVATION_OF_PRIVILEGE,
                title="Cross-Tenant Data Leakage & Horizontal Escalation",
                description="Authenticated tenant accesses or mutates records belonging to a different tenant organization.",
                target_component="Database Row-Level Security (RLS)",
                severity=ThreatSeverity.CRITICAL,
                countermeasure="Enforce PostgreSQL Row-Level Security (RLS) with session-scoped tenant ID parameterization.",
                verification_check="Integration test confirming tenant A queries return 0 rows for tenant B resources.",
            ))
            idx += 1

        return {
            "project_name": project_name,
            "architecture_pattern": architecture_pattern,
            "total_threats": len(threats),
            "threats": [t.to_dict() for t in threats],
            "severity_summary": {
                "critical": sum(1 for t in threats if t.severity == ThreatSeverity.CRITICAL),
                "high": sum(1 for t in threats if t.severity == ThreatSeverity.HIGH),
                "medium": sum(1 for t in threats if t.severity == ThreatSeverity.MEDIUM),
            },
        }
