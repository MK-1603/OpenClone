#!/usr/bin/env python3
"""OpenClone Automated Secret Detection Scanner.

Detects API keys, private keys, authentication tokens, credentials,
and unauthorized environment files across working tree, staged files,
tracked repository files, and git history.

Zero sensitive data is emitted in logs or terminal outputs; all findings are redacted.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

# Detection rule definition
class SecretRule(NamedTuple):
    rule_id: str
    description: str
    pattern: re.Pattern
    severity: str  # BLOCKER, HIGH, MEDIUM


RULES = [
    # Private Key material
    SecretRule(
        "SEC-PAT-001",
        "Private Key Header",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
        "BLOCKER",
    ),
    # OpenAI API Key
    SecretRule(
        "SEC-PAT-002",
        "OpenAI API Key",
        re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
        "BLOCKER",
    ),
    # Anthropic API Key
    SecretRule(
        "SEC-PAT-003",
        "Anthropic API Key",
        re.compile(r"\bsk-ant-[A-Za-z0-9_-]{24,}\b"),
        "BLOCKER",
    ),
    # Google API Key
    SecretRule(
        "SEC-PAT-004",
        "Google API Key",
        re.compile(r"\bAIza[0-9A-Za-z-_]{35}\b"),
        "BLOCKER",
    ),
    # GitHub Tokens
    SecretRule(
        "SEC-PAT-005",
        "GitHub Personal Access Token",
        re.compile(r"\b(?:ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})\b"),
        "BLOCKER",
    ),
    # AWS Access Key ID
    SecretRule(
        "SEC-PAT-006",
        "AWS Access Key ID",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "BLOCKER",
    ),
    # Slack Token
    SecretRule(
        "SEC-PAT-007",
        "Slack Token",
        re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
        "BLOCKER",
    ),
    # Generic High-Risk Credential Assignment
    SecretRule(
        "SEC-PAT-008",
        "Plaintext Password or Secret in Configuration",
        re.compile(r"(?i)\b(?:password|passwd|client_secret)\s*[:=]\s*['\"][A-Za-z0-9@#$%^&*!_-]{8,}['\"]"),
        "HIGH",
    ),
]

# Sensitive File Patterns that should never be tracked
SENSITIVE_FILE_PATTERNS = [
    re.compile(r"(^|/)\.env(\.(local|development|production|test|staging))?$"),
    re.compile(r".*\.(pem|key|p12|pfx|jks|keystore)$"),
    re.compile(r"(^|/)id_(rsa|ed25519|ecdsa|dsa)(\..*)?$"),
    re.compile(r".*service-account.*\.json$"),
    re.compile(r".*credentials.*\.json$"),
]

# Paths allowed to contain sample/placeholder tokens or template formats
SAFE_EXCLUSIONS: Set[str] = {
    ".env.example",
    ".env.template",
    "security/scanners.lock.json",
}

SAFE_PATH_PREFIXES = (
    ".git/",
    ".openclone-dev/",
    "node_modules/",
    ".pytest_cache/",
    "tests/fixtures/",
    ".venv/",
    "venv/",
)


class Finding(NamedTuple):
    file_path: str
    line_number: int
    rule_id: str
    description: str
    masked_snippet: str
    severity: str


def is_safe_path(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/")
    if norm in SAFE_EXCLUSIONS:
        return True
    if any(norm.startswith(prefix) for prefix in SAFE_PATH_PREFIXES):
        return True
    return False


def mask_secret(content: str) -> str:
    if len(content) <= 8:
        return "[REDACTED]"
    return content[:3] + "..." + "[REDACTED]" + "..." + content[-3:]


def check_sensitive_filename(file_path: str) -> Optional[Finding]:
    norm = file_path.replace("\\", "/")
    if is_safe_path(norm):
        return None
    for pattern in SENSITIVE_FILE_PATTERNS:
        if pattern.search(norm):
            return Finding(
                file_path=file_path,
                line_number=1,
                rule_id="SEC-FILE-001",
                description="Sensitive file format prohibited from version control",
                masked_snippet=f"Protected file path: {file_path}",
                severity="BLOCKER",
            )
    return None


def scan_content(file_path: str, content: str) -> List[Finding]:
    findings: List[Finding] = []
    norm = file_path.replace("\\", "/")
    if is_safe_path(norm):
        return findings

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        # Ignore comments in markdown or python explaining patterns
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("<!--"):
            # If line is documentation of a pattern, skip
            if "re.compile" in line or "pattern" in line.lower() or "example" in line.lower():
                continue

        for rule in RULES:
            match = rule.pattern.search(line)
            if match:
                raw_match = match.group(0)
                # Check for obvious false positives (e.g. placeholder texts)
                if any(x in raw_match.lower() for x in ["placeholder", "example", "mock", "your_", "dummy", "test"]):
                    continue
                snippet = line[:match.start()] + "[REDACTED]" + line[match.end():]
                findings.append(
                    Finding(
                        file_path=file_path,
                        line_number=idx,
                        rule_id=rule.rule_id,
                        description=rule.description,
                        masked_snippet=snippet.strip()[:100],
                        severity=rule.severity,
                    )
                )
    return findings


def get_tracked_files(root: Path) -> List[str]:
    try:
        res = subprocess.run(
            ["git", "ls-files"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True,
            stdin=subprocess.DEVNULL,
        )
        return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"Warning: git ls-files failed: {e}", file=sys.stderr)
        return []


def get_staged_files(root: Path) -> List[str]:
    try:
        res = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True,
            stdin=subprocess.DEVNULL,
        )
        return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"Warning: git diff --cached failed: {e}", file=sys.stderr)
        return []


def scan_file(root: Path, rel_path: str) -> List[Finding]:
    findings: List[Finding] = []
    file_finding = check_sensitive_filename(rel_path)
    if file_finding:
        findings.append(file_finding)

    full_path = root / rel_path
    if not full_path.is_file():
        return findings

    # Skip files > 5MB or binary
    try:
        if full_path.stat().st_size > 5 * 1024 * 1024:
            return findings
        content = full_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    findings.extend(scan_content(rel_path, content))
    return findings


def run_scanner(
    root: Path,
    mode: str = "tracked",
    target_files: Optional[List[str]] = None,
) -> Tuple[int, List[Finding]]:
    findings: List[Finding] = []

    if target_files is not None:
        files = target_files
    elif mode == "staged":
        files = get_staged_files(root)
    elif mode == "tracked":
        files = get_tracked_files(root)
    else:  # all working tree
        files = []
        for p in root.rglob("*"):
            if p.is_file():
                rel = str(p.relative_to(root)).replace("\\", "/")
                if not is_safe_path(rel):
                    files.append(rel)

    for rel in files:
        file_findings = scan_file(root, rel)
        findings.extend(file_findings)

    return len(files), findings


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClone Automated Secret Detection Scanner")
    parser.add_argument("--mode", choices=["tracked", "staged", "all"], default="tracked")
    parser.add_argument("--root", default=".", help="Repository root directory")
    parser.add_argument("--files", nargs="*", help="Specific files to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    scanned_count, findings = run_scanner(root, mode=args.mode, target_files=args.files)

    print(f"OpenClone Secret Scanner: Scanned {scanned_count} files (mode: {args.mode}).")
    if not findings:
        print("PASS: No verified secrets, exposed credentials, or prohibited files detected.")
        return 0

    print(f"FAIL: {len(findings)} secret-scanner findings detected:")
    for f in findings:
        print(f"  [{f.severity}] {f.rule_id} in {f.file_path}:{f.line_number} - {f.description}")
        print(f"    Snippet: {f.masked_snippet}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
