"""OpenClone Web Application Firewall (WAF) & API Defense Engine.

Inspects incoming HTTP payloads for SQL injection, XSS, path traversal,
enforces rate limiting, request size bounds, and injects OWASP secure headers.
"""
from __future__ import annotations

import re
import time
from collections import defaultdict, deque
from typing import Any, Dict, List, NamedTuple, Optional, Set


class WafSecurityError(Exception):
    """Raised when an incoming request violates WAF security policy."""
    pass


class WafFinding(NamedTuple):
    attack_type: str
    severity: str
    description: str
    parameter: str
    matched_pattern: str


# Attack Detection Regular Expressions
SQLI_PATTERNS = [
    (re.compile(r"(?i)\bUNION\s+(?:ALL\s+)?SELECT\b"), "SQL Injection (UNION SELECT)"),
    (re.compile(r"(?i)'\s*OR\s*'?[0-9a-z]+'?\s*=\s*'?[0-9a-z]+"), "SQL Injection (Boolean Tautology)"),
    (re.compile(r"(?i)\b(?:DROP|ALTER|TRUNCATE)\s+TABLE\b"), "SQL Injection (DDL Tampering)"),
    (re.compile(r"(?i)\bSLEEP\s*\(\s*\d+\s*\)"), "SQL Injection (Time-based Blind)"),
    (re.compile(r"(?i)(?:--|/\*|\*/|#)"), "SQL Injection (Comment Delimiter)"),
    (re.compile(r"(?i)\bEXEC(?:UTE)?\s*\(|\bxp_cmdshell\b"), "SQL Injection (Command Execution)"),
]

XSS_PATTERNS = [
    (re.compile(r"(?i)<script\b[^>]*>.*?</script>|<script\b"), "Cross-Site Scripting (<script> tag)"),
    (re.compile(r"(?i)javascript:\s*[^\s]+"), "Cross-Site Scripting (javascript: pseudo-protocol)"),
    (re.compile(r"(?i)\bon(?:error|load|click|mouseover|focus|blur)\s*="), "Cross-Site Scripting (Inline Event Handler)"),
    (re.compile(r"(?i)<(?:iframe|embed|object|applet)\b"), "Cross-Site Scripting (Embedded Frame / Object)"),
    (re.compile(r"(?i)document\.(?:cookie|location|write)"), "Cross-Site Scripting (DOM Manipulation)"),
]

PATH_TRAVERSAL_PATTERNS = [
    (re.compile(r"(?:\.\./|\.\.\\|%2e%2e%2f|%2e%2e/|\.\.%2f)"), "Path Traversal (Directory Climb)"),
    (re.compile(r"(?i)(?:/etc/passwd|/etc/shadow|windows[\\/]system32)"), "Path Traversal (Sensitive System Target)"),
]

ALLOWED_HTTP_METHODS: Set[str] = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
DEFAULT_MAX_BODY_BYTES = 2 * 1024 * 1024  # 2 Megabytes


class WafInspector:
    """Inspects API requests against attack signatures and protocol anomalies."""

    def __init__(self, max_body_bytes: int = DEFAULT_MAX_BODY_BYTES):
        self.max_body_bytes = max_body_bytes

    def inspect_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
    ) -> List[WafFinding]:
        """Inspect request parameters and return any security findings."""
        findings: List[WafFinding] = []

        # 1. HTTP Method Restriction
        clean_method = method.strip().upper()
        if clean_method not in ALLOWED_HTTP_METHODS:
            findings.append(
                WafFinding(
                    attack_type="METHOD_ABUSE",
                    severity="HIGH",
                    description=f"HTTP method '{clean_method}' is prohibited",
                    parameter="method",
                    matched_pattern=clean_method,
                )
            )

        # 2. Request Size Restriction
        if body and len(body.encode("utf-8")) > self.max_body_bytes:
            findings.append(
                WafFinding(
                    attack_type="SIZE_VIOLATION",
                    severity="HIGH",
                    description=f"Request payload size exceeds maximum limit of {self.max_body_bytes} bytes",
                    parameter="body",
                    matched_pattern=f"size={len(body)}",
                )
            )

        # 3. Path Traversal & Injection in Path
        self._check_string(path, "path", findings)

        # 4. Query Parameters Inspection
        if query_params:
            for k, v in query_params.items():
                self._check_string(str(k), f"query_key:{k}", findings)
                self._check_string(str(v), f"query_val:{k}", findings)

        # 5. Body Content Inspection
        if body and clean_method in ("POST", "PUT", "PATCH"):
            self._check_string(body, "body", findings)

        return findings

    def _check_string(self, text: str, param_name: str, findings: List[WafFinding]) -> None:
        if not text:
            return

        # Check Path Traversal
        for pattern, desc in PATH_TRAVERSAL_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(
                    WafFinding(
                        attack_type="PATH_TRAVERSAL",
                        severity="BLOCKER",
                        description=desc,
                        parameter=param_name,
                        matched_pattern=match.group(0),
                    )
                )

        # Check SQL Injection
        for pattern, desc in SQLI_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(
                    WafFinding(
                        attack_type="SQL_INJECTION",
                        severity="BLOCKER",
                        description=desc,
                        parameter=param_name,
                        matched_pattern=match.group(0),
                    )
                )

        # Check Cross-Site Scripting
        for pattern, desc in XSS_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(
                    WafFinding(
                        attack_type="XSS",
                        severity="BLOCKER",
                        description=desc,
                        parameter=param_name,
                        matched_pattern=match.group(0),
                    )
                )


class RateLimiter:
    """Sliding-window rate limiter for API endpoints."""

    def __init__(self, max_requests: int = 100, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, client_key: str) -> bool:
        """Return True if client is within rate limits; False if exceeded."""
        now = time.monotonic()
        timestamps = self._history[client_key]

        # Evict timestamps outside sliding window
        while timestamps and timestamps[0] <= now - self.window_seconds:
            timestamps.popleft()

        if len(timestamps) >= self.max_requests:
            return False

        timestamps.append(now)
        return True


def get_security_headers() -> Dict[str, str]:
    """Return OWASP-recommended security headers for API responses."""
    return {
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
    }


def sanitize_api_error(error: Any, request_id: str = "req_anon") -> Dict[str, Any]:
    """Strip internal details, file paths, credentials, and stack traces from client errors."""
    return {
        "error": "A security or validation error occurred while processing the request.",
        "code": "REQUEST_REJECTED",
        "request_id": request_id,
        "timestamp": int(time.time()),
    }
