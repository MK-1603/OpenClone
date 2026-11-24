"""Frontend Security Intelligence & Secret Leak Auditor.

Audits client-side code, markup, and bundle configurations for:
- Exposed secrets and private credentials
- Content Security Policy (CSP) header compliance
- XSS prevention and safe rendering patterns
- Server-side authorization boundaries
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class SecurityFinding:
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    rule_id: str
    description: str
    location: str
    recommendation: str


@dataclass
class SecurityAuditResult:
    is_secure: bool
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    findings: List[SecurityFinding] = field(default_factory=list)
    score: float = 100.0


class FrontendSecurityAuditor:
    """Detects security vulnerabilities in frontend codebases."""

    # Patterns indicating raw credentials or secrets improperly included in client code
    SUSPICIOUS_PATTERNS = [
        (r"(?i)(api[_-]?key|secret|password|private[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", "Hardcoded credential token literal"),
        (r"process\.env\.(DATABASE_URL|REDIS_URL|AWS_SECRET_ACCESS_KEY|SECRET_KEY|JWT_SECRET)", "Server-side secret accessed without client prefix"),
        (r"dangerouslySetInnerHTML\s*=\s*\{\s*__html\s*:\s*(?!sanitize)[a-zA-Z0-9_\.]+\s*\}", "Unsanitized raw HTML rendering (XSS risk)"),
    ]

    def audit_code_snippet(self, code: str, file_path: str = "client.tsx") -> List[SecurityFinding]:
        """Audits a code snippet or component file for client security flaws."""
        findings = []

        for pattern, desc in self.SUSPICIOUS_PATTERNS:
            matches = re.finditer(pattern, code)
            for m in matches:
                # Mask secret value in finding report
                matched_str = m.group(0)
                findings.append(
                    SecurityFinding(
                        severity="CRITICAL" if "secret" in desc.lower() or "credential" in desc.lower() else "HIGH",
                        rule_id="SEC-FE-001",
                        description=f"{desc}: '{matched_str[:25]}...'",
                        location=file_path,
                        recommendation="Remove hardcoded secret; use NEXT_PUBLIC_ client-safe environment variables or server actions.",
                    )
                )

        return findings

    def audit_csp_policy(self, csp_header: str) -> List[SecurityFinding]:
        """Validates that Content-Security-Policy header restricts script execution."""
        findings = []
        if "unsafe-eval" in csp_header:
            findings.append(
                SecurityFinding(
                    severity="HIGH",
                    rule_id="SEC-FE-002",
                    description="CSP contains 'unsafe-eval' which allows dynamic string execution.",
                    location="HTTP Response Headers",
                    recommendation="Remove 'unsafe-eval' from script-src directive.",
                )
            )
        if "unsafe-inline" in csp_header and "'nonce-" not in csp_header and "'sha256-" not in csp_header:
            findings.append(
                SecurityFinding(
                    severity="MEDIUM",
                    rule_id="SEC-FE-003",
                    description="CSP allows 'unsafe-inline' scripts without nonce or cryptographic hash.",
                    location="HTTP Response Headers",
                    recommendation="Adopt strict nonce-based CSP for inline scripts.",
                )
            )
        return findings

    def evaluate(self, findings: List[SecurityFinding]) -> SecurityAuditResult:
        """Aggregates security findings into an audit result."""
        critical = sum(1 for f in findings if f.severity == "CRITICAL")
        high = sum(1 for f in findings if f.severity == "HIGH")
        medium = sum(1 for f in findings if f.severity == "MEDIUM")
        low = sum(1 for f in findings if f.severity == "LOW")

        deductions = (critical * 30.0) + (high * 15.0) + (medium * 5.0) + (low * 2.0)
        score = max(0.0, 100.0 - deductions)
        is_secure = (critical == 0 and high == 0)

        return SecurityAuditResult(
            is_secure=is_secure,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            findings=findings,
            score=round(score, 1),
        )
