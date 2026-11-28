"""
OpenClone Memory Security Guardrails & Boundary Isolation.
"""

from __future__ import annotations
import re
from typing import List, Optional, Dict, Any, Tuple
from openclone.memory.models import MemoryRecord, MemoryScope


class MemorySecurityError(PermissionError):
    """Raised when an operation violates memory security or scope boundaries."""
    pass


class MemorySecurityGuard:
    """
    Enforces security, prompt-injection defense, and tenant/project boundary isolation.
    """

    INJECTION_PATTERNS = [
        re.compile(r"(?i)(ignore\s+previous\s+instructions|system\s+prompt|developer\s+mode)"),
        re.compile(r"(?i)(you\s+must\s+now|disregard\s+all\s+prior|reveal\s+secret)"),
        re.compile(r"(?i)<\s*script[^>]*>.*<\s*/\s*script\s*>"),
        re.compile(r"(?i)\[\s*system\s*:\s*"),
    ]

    SECRET_PATTERNS = [
        re.compile(r"(?i)(api[_-]?key|secret|password|bearer|auth[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{8,}['\"]"),
        re.compile(r"(?i)-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----"),
        re.compile(r"(?i)ghp_[A-Za-z0-9]{36}"),
        re.compile(r"(?i)sk-[A-Za-z0-9]{32,}"),
    ]

    @classmethod
    def sanitize_untrusted_memory(cls, text: str) -> str:
        """
        Frames memory content as untrusted data so LLM agents cannot confuse it with system instructions.
        """
        escaped = text.replace("```", "'''")
        return f"[UNTRUSTED_HISTORICAL_DATA]\n{escaped}\n[/UNTRUSTED_HISTORICAL_DATA]"

    @classmethod
    def audit_record_for_persistence(cls, record: MemoryRecord) -> Tuple[bool, List[str]]:
        """Verify that record does not contain prohibited secrets or active injections."""
        violations = []
        combined_text = f"{record.title}\n{record.statement}\n{record.details or ''}"

        # Check for secrets
        for pat in cls.SECRET_PATTERNS:
            if pat.search(combined_text):
                violations.append("Prohibited secret pattern detected in memory record!")

        # Check for injection attempts
        for pat in cls.INJECTION_PATTERNS:
            if pat.search(combined_text):
                violations.append(f"Prompt injection pattern detected: '{pat.pattern}'")

        return len(violations) == 0, violations

    @classmethod
    def assert_scope_access(cls, caller_scope: MemoryScope, target_scope: MemoryScope) -> None:
        """
        Enforce strict project and workspace isolation.
        A caller from Project A cannot access records from Project B.
        """
        if caller_scope.project_id != target_scope.project_id:
            raise MemorySecurityError(
                f"Cross-project access denied: Caller project '{caller_scope.project_id}' cannot access '{target_scope.project_id}'"
            )
        if caller_scope.workspace_id != target_scope.workspace_id:
            raise MemorySecurityError(
                f"Cross-workspace access denied: Caller workspace '{caller_scope.workspace_id}' cannot access '{target_scope.workspace_id}'"
            )
