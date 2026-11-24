"""OpenClone AI Agent Firewall & Execution Security Gateway.

Enforces tool allowlists, command validation, filesystem sandboxing,
prompt-injection defenses, credential access protection, and SHA-256 approval binding.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class AgentSecurityViolationError(Exception):
    """Raised when an AI agent attempts an unauthorized action."""
    pass


# Prompt Injection Heuristic Patterns
INJECTION_SIGNATURES = [
    re.compile(r"ignore\s+(?:all\s+|any\s+)?(?:previous|prior|above)\s+(?:instructions|rules)", re.I),
    re.compile(r"disregard\s+(?:the\s+)?(?:system|previous|above)\s+prompt", re.I),
    re.compile(r"you\s+are\s+now\s+(?:in\s+)?(?:developer|admin|root|jailbreak)\s+mode", re.I),
    re.compile(r"reveal\s+(?:the\s+|your\s+)?(?:system\s+prompt|secrets?|api\s+keys?)", re.I),
    re.compile(r"approve\s+(?:this|all)\s+(?:task|change)s?\s+without", re.I),
    re.compile(r"\b(?:DAN|jailbreak|bypass\s+security\s+filter)\b", re.I),
]

# Prohibited shell chaining and injection operators in raw commands
SHELL_INJECTION_TOKENS = [";", "&&", "||", "|", "`", "$(", "${", ">", "<"]

# Sensitive credential file patterns prohibited from agent reading
SENSITIVE_AGENT_FILES = [
    re.compile(r"(^|[/\\])\.env(\..*)?$"),
    re.compile(r".*\.(pem|key|p12|pfx|jks|keystore)$"),
    re.compile(r"(^|[/\\])id_(rsa|ed25519|ecdsa|dsa)"),
    re.compile(r".*service-account.*\.json$"),
    re.compile(r".*credentials.*\.json$"),
]


class AgentSecurityGateway:
    """Deterministic security firewall for AI Agent actions and tool invocations."""

    @staticmethod
    def detect_prompt_injection(prompt: str) -> bool:
        """Analyze user or untrusted input for prompt injection attack patterns."""
        if not prompt:
            return False
        for pattern in INJECTION_SIGNATURES:
            if pattern.search(prompt):
                return True
        return False

    @staticmethod
    def validate_command(argv: List[str], allowed_executables: List[str]) -> bool:
        """Validate agent command against binary allowlist and command injection tokens."""
        if not argv or not isinstance(argv, list):
            raise AgentSecurityViolationError("Command validation failed: argv must be a non-empty list.")

        exe = os.path.basename(argv[0])
        allowed = set(allowed_executables)

        if exe not in allowed and argv[0] not in allowed:
            raise AgentSecurityViolationError(
                f"Agent command blocked: Executable '{exe}' is not in policy.allowed_executables: {sorted(allowed)}"
            )

        # Check for embedded shell injection tokens in arguments
        for arg in argv[1:]:
            for token in SHELL_INJECTION_TOKENS:
                if token in arg:
                    raise AgentSecurityViolationError(
                        f"Agent command blocked: Shell control token '{token}' detected in command argument: '{arg}'"
                    )

        return True

    @staticmethod
    def validate_filesystem_access(target_path: Path, workspace_root: Path, access_type: str = "read") -> bool:
        """Ensure agent cannot access files outside the workspace root or read credential files."""
        root_resolved = workspace_root.resolve()
        target_resolved = target_path.resolve()

        # 1. Directory Confinement Check
        if target_resolved != root_resolved and root_resolved not in target_resolved.parents:
            raise AgentSecurityViolationError(
                f"Filesystem access blocked: Path '{target_path}' is outside the authorized workspace '{workspace_root}'"
            )

        # 2. Sensitive Credential File Protection
        path_str = str(target_resolved)
        for pattern in SENSITIVE_AGENT_FILES:
            if pattern.search(path_str):
                raise AgentSecurityViolationError(
                    f"Credential protection blocked: Agent attempted {access_type} on sensitive file: '{target_path.name}'"
                )

        return True

    @staticmethod
    def validate_tool_authorization(worker_id: str, action: str, worker_manifest: Dict[str, Any]) -> bool:
        """Verify that a worker role is authorized to perform the requested action."""
        allowed_actions = set(worker_manifest.get("allowed_actions", []))
        approval_actions = set(worker_manifest.get("approval_required_for", []))

        if action not in allowed_actions and action not in approval_actions:
            raise AgentSecurityViolationError(
                f"Tool authorization blocked: Worker '{worker_id}' is not permitted to request action '{action}'. "
                f"Permitted actions: {sorted(allowed_actions | approval_actions)}"
            )
        return True

    @staticmethod
    def compute_task_digest(task: Dict[str, Any]) -> str:
        """Compute deterministic SHA-256 digest of task payload."""
        canonical = json.dumps(task, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def verify_approval_binding(cls, task: Dict[str, Any], approved_digest: str) -> bool:
        """Verify that a task's current content matches the cryptographically approved digest."""
        current_digest = cls.compute_task_digest(task)
        if current_digest != approved_digest:
            raise AgentSecurityViolationError(
                "Human approval binding invalid: Task parameters have changed since approval was granted."
            )
        return True
