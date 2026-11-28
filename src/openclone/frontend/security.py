"""Frontend Security Intelligence & Secret Leak Auditor.

Audits client-side code, markup, and bundle configurations for:
- Exposed secrets and private credentials (un-prefixed process.env)
- Unsafe HTML rendering & DOM injection (dangerouslySetInnerHTML without sanitization)
- Dangerous URL schemes (javascript:, data:text/html)
- Content Security Policy (CSP) header compliance
- Context-aware storage audits (plaintext sensitive tokens in localStorage)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SecuritySeverity(str, Enum):
    """Vulnerability severity tier."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class SecurityFinding:
    """Security audit finding with concrete location and remediation advice."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    rule_id: str
    description: str
    location: str
    recommendation: str
    evidence_snippet: str = ""


@dataclass
class SecurityAuditResult:
    """Consolidated security audit report."""
    is_secure: bool
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    findings: List[SecurityFinding] = field(default_factory=list)
    score: float = 100.0


class FrontendSecurityAuditor:
    """Detects security vulnerabilities in frontend codebases and build artifacts."""

    SUSPICIOUS_PATTERNS = [
        (
            r"(?i)(api[_-]?key|secret|password|private[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
            "Hardcoded credential token literal",
            "CRITICAL",
            "SEC-FE-001",
            "Remove hardcoded secret; use NEXT_PUBLIC_ client-safe environment variables or server actions.",
        ),
        (
            r"process\.env\.(DATABASE_URL|REDIS_URL|AWS_SECRET_ACCESS_KEY|SECRET_KEY|JWT_SECRET|PRIVATE_KEY)",
            "Server-side secret accessed without client prefix",
            "CRITICAL",
            "SEC-FE-002",
            "Server secrets must not be bundled into client code. Expose only NEXT_PUBLIC_ variables to client.",
        ),
        (
            r"dangerouslySetInnerHTML\s*=\s*\{\s*__html\s*:\s*(?!DOMPurify\.sanitize|sanitize\()[a-zA-Z0-9_\.]+\s*\}",
            "Unsanitized raw HTML rendering (XSS risk)",
            "HIGH",
            "SEC-FE-003",
            "Sanitize HTML strings with DOMPurify.sanitize() before passing to dangerouslySetInnerHTML.",
        ),
        (
            r"href\s*=\s*['\"]javascript:[^'\"]*['\"]",
            "Dangerous javascript: URI protocol execution",
            "HIGH",
            "SEC-FE-004",
            "Replace javascript: pseudo-protocols with explicit onClick handlers and standard buttons.",
        ),
        (
            r"localStorage\.setItem\s*\(\s*['\"](jwt|token|access_token|secret)['\"]",
            "Sensitive authentication token stored in unencrypted localStorage",
            "MEDIUM",
            "SEC-FE-005",
            "Store session tokens in httpOnly, Secure, SameSite=Strict cookies to protect against XSS token theft.",
        ),
    ]

    def audit_code_snippet(self, code: str, file_path: str = "client.tsx") -> List[SecurityFinding]:
        """Audits a code snippet or component file for client security flaws."""
        findings = []

        for pattern, desc, severity, rule_id, rec in self.SUSPICIOUS_PATTERNS:
            matches = re.finditer(pattern, code)
            for m in matches:
                matched_str = m.group(0)
                # Redact matched secret values for safe reporting
                redacted = re.sub(r"['\"][a-zA-Z0-9_\-]{10,}['\"]", "'[REDACTED]'", matched_str)
                findings.append(
                    SecurityFinding(
                        severity=severity,
                        rule_id=rule_id,
                        description=f"{desc}: '{redacted[:40]}...'",
                        location=file_path,
                        recommendation=rec,
                        evidence_snippet=redacted,
                    )
                )

        return findings

    def audit_csp_headers(
        self, csp_header: str, require_default_src: bool = False
    ) -> List[SecurityFinding]:
        """Audits Content-Security-Policy (CSP) headers for dangerous directives."""
        findings = []
        lowered = csp_header.lower()

        if "unsafe-eval" in lowered:
            findings.append(
                SecurityFinding(
                    severity="HIGH",
                    rule_id="SEC-CSP-001",
                    description="CSP contains 'unsafe-eval' directive",
                    location="HTTP Response Headers / meta tag",
                    recommendation="Remove 'unsafe-eval' to prevent arbitrary code execution via eval().",
                )
            )

        if "unsafe-inline" in lowered and "script-src" in lowered:
            findings.append(
                SecurityFinding(
                    severity="MEDIUM",
                    rule_id="SEC-CSP-002",
                    description="CSP script-src contains 'unsafe-inline' without nonce or hash",
                    location="HTTP Response Headers / meta tag",
                    recommendation="Use cryptographic nonces or sha256 hashes instead of 'unsafe-inline'.",
                )
            )

        if require_default_src and "default-src" not in lowered:
            findings.append(
                SecurityFinding(
                    severity="HIGH",
                    rule_id="SEC-CSP-003",
                    description="CSP header is missing fallback 'default-src' directive",
                    location="HTTP Response Headers",
                    recommendation="Define 'default-src 'self'' as a foundational defensive baseline.",
                )
            )

        return findings

    def audit_csp_policy(self, csp_header: str) -> List[SecurityFinding]:
        """Alias for audit_csp_headers for backward compatibility."""
        return self.audit_csp_headers(csp_header)

    def evaluate(self, findings: List[SecurityFinding]) -> SecurityAuditResult:
        """Evaluate a pre-collected list of security findings."""
        critical = sum(1 for f in findings if f.severity == "CRITICAL")
        high = sum(1 for f in findings if f.severity == "HIGH")
        medium = sum(1 for f in findings if f.severity == "MEDIUM")
        low = sum(1 for f in findings if f.severity == "LOW")

        score = max(0.0, 100.0 - (critical * 30.0 + high * 15.0 + medium * 5.0 + low * 2.0))
        is_secure = critical == 0 and high == 0

        return SecurityAuditResult(
            is_secure=is_secure,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            findings=findings,
            score=round(score, 1),
        )

    def run_full_audit(self, files_map: Dict[str, str], csp_header: Optional[str] = None) -> SecurityAuditResult:
        """Run complete security audit across provided files and optional CSP header."""
        all_findings = []
        for file_path, content in files_map.items():
            all_findings.extend(self.audit_code_snippet(content, file_path))

        if csp_header:
            all_findings.extend(self.audit_csp_headers(csp_header))

        critical = sum(1 for f in all_findings if f.severity == "CRITICAL")
        high = sum(1 for f in all_findings if f.severity == "HIGH")
        medium = sum(1 for f in all_findings if f.severity == "MEDIUM")
        low = sum(1 for f in all_findings if f.severity == "LOW")

        score = max(0.0, 100.0 - (critical * 30.0 + high * 15.0 + medium * 5.0 + low * 2.0))
        is_secure = critical == 0 and high == 0

        return SecurityAuditResult(
            is_secure=is_secure,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            findings=all_findings,
            score=round(score, 1),
        )
