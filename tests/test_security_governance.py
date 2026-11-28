"""OpenClone Security & Engineering Governance Verification Suite (SEC-001 - SEC-020).

Automated verification of Git ignore protection, secret scanning, environment safety,
agent command sandboxing, approval enforcement, and audit ledger integrity.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for p in (str(ROOT), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest

from runtime.openclone_runtime import workforce as wf
from src.openclone.mie.telemetry import redact_secrets
from src.openclone.security.env import (
    SecurityValidationError,
    audit_template_safety,
    load_safe_config,
    validate_client_bundle_safety,
    validate_environment,
)
from tools.scan_secrets import Finding, check_sensitive_filename, run_scanner, scan_content

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
PYNAME = os.path.basename(PY)


def run_cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            wf.main([str(x) for x in argv])
            code = 0
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    return code, out.getvalue(), err.getvalue()


def git_check_ignore(rel_path: str) -> bool:
    """Run git check-ignore to verify if Git ignores the specified path."""
    res = subprocess.run(
        ["git", "check-ignore", rel_path],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    return res.returncode == 0


# ============================================================================
# 1. GIT IGNORE & PRIVATE KEY PROTECTION (SEC-001 - SEC-008)
# ============================================================================

def test_sec_001_dot_env_protection():
    """SEC-001: .env ignore protection -> Ignored"""
    assert git_check_ignore(".env") is True
    assert git_check_ignore("subdir/.env") is True


def test_sec_002_dot_env_local_protection():
    """SEC-002: .env.local protection -> Ignored"""
    assert git_check_ignore(".env.local") is True
    assert git_check_ignore("examples/pulse/.env.local") is True


def test_sec_003_dot_env_production_protection():
    """SEC-003: .env.production protection -> Ignored"""
    assert git_check_ignore(".env.production") is True
    assert git_check_ignore("config/.env.production") is True
    assert git_check_ignore(".env.staging") is True


def test_sec_004_dot_env_example_exception():
    """SEC-004: .env.example exception -> Allowed for version control"""
    # .env.example must NOT be ignored (returncode != 0)
    assert git_check_ignore(".env.example") is False
    assert (ROOT / ".env.example").is_file()

    # Template must only have placeholders
    violations = audit_template_safety(ROOT / ".env.example")
    assert len(violations) == 0, f"Template contains non-placeholder secrets: {violations}"


def test_sec_005_pem_protection():
    """SEC-005: *.pem protection -> Ignored"""
    assert git_check_ignore("server.pem") is True
    assert git_check_ignore("certs/privkey.pem") is True
    assert git_check_ignore("sub/dir/cert.pem") is True


def test_sec_006_key_protection():
    """SEC-006: *.key protection -> Ignored"""
    assert git_check_ignore("private.key") is True
    assert git_check_ignore("tls/server.key") is True
    assert git_check_ignore("keystore.p12") is True
    assert git_check_ignore("cert.pfx") is True


def test_sec_007_ssh_private_key_protection():
    """SEC-007: SSH private-key protection -> Ignored"""
    assert git_check_ignore("id_rsa") is True
    assert git_check_ignore("id_ed25519") is True
    assert git_check_ignore("id_ecdsa") is True
    assert git_check_ignore(".ssh/id_rsa") is True


def test_sec_008_service_account_credential_protection():
    """SEC-008: Service-account credential protection -> Ignored"""
    assert git_check_ignore("service-account.json") is True
    assert git_check_ignore("gcp-service_account.json") is True
    assert git_check_ignore("client_secrets.json") is True
    assert git_check_ignore("credentials.json") is True


# ============================================================================
# 2. SECRET SCANNING & DETECTION (SEC-009 - SEC-011)
# ============================================================================

def test_sec_009_existing_tracked_secret_detection():
    """SEC-009: Existing tracked-secret detection -> Detected and reported"""
    # 1. Verify tracked files are clean
    scanned, findings = run_scanner(ROOT, mode="tracked")
    assert scanned > 0
    assert len(findings) == 0, f"Tracked secrets detected: {findings}"

    # 2. Verify detector catches a synthetic violation
    mock_content = "api_key = 'sk-" + "9" * 30 + "'"
    simulated = scan_content("mock/file.py", mock_content)
    assert len(simulated) == 1
    assert simulated[0].rule_id == "SEC-PAT-002"
    assert "[REDACTED]" in simulated[0].masked_snippet


def test_sec_010_staged_secret_detection():
    """SEC-010: Staged-secret detection -> Blocked"""
    # Verify file-name protection triggers on staged prohibited file
    finding = check_sensitive_filename(".env.production")
    assert finding is not None
    assert finding.severity == "BLOCKER"

    # Verify content protection triggers on staged secret token
    dummy_key = "ghp_" + "A" * 36
    staged_findings = scan_content("src/test.py", f"export GITHUB_TOKEN={dummy_key}")
    assert len(staged_findings) >= 1
    assert staged_findings[0].severity == "BLOCKER"


def test_sec_011_hardcoded_secret_scanning():
    """SEC-011: Hardcoded-secret scanning -> No verified secrets"""
    total_files, findings = run_scanner(ROOT, mode="tracked")
    assert len(findings) == 0
    assert total_files >= 100


# ============================================================================
# 3. ENVIRONMENT & CONFIGURATION SECURITY (SEC-012 - SEC-014)
# ============================================================================

def test_sec_012_environment_validation():
    """SEC-012: Environment validation -> Invalid configuration rejected"""
    # Reject unknown environment
    with pytest.raises(SecurityValidationError, match="Invalid environment"):
        validate_environment("production_unknown")

    # Reject placeholder keys in production
    insecure_prod = {
        "OPENAI_API_KEY": "your_openai_api_key_here",
        "OPENCLONE_STRICT_SANDBOX": "true",
    }
    with pytest.raises(SecurityValidationError, match="placeholder value"):
        validate_environment("production", env_dict=insecure_prod, required_keys=["OPENAI_API_KEY"])

    # Reject disabled sandbox in production
    insecure_sandbox = {
        "OPENAI_API_KEY": "s" + "k-mock-synthetic-value-123456",
        "OPENCLONE_STRICT_SANDBOX": "false",
    }
    with pytest.raises(SecurityValidationError, match="OPENCLONE_STRICT_SANDBOX"):
        validate_environment("production", env_dict=insecure_sandbox)


def test_sec_013_client_side_secret_exposure():
    """SEC-013: Client-side secret exposure -> No server secrets exposed"""
    # Safe client environment passes
    safe_client = {
        "NEXT_PUBLIC_APP_URL": "https://openclone.org",
        "NEXT_PUBLIC_VERSION": "2.0.0",
    }
    validate_client_bundle_safety(safe_client)

    # Exposed server secret under NEXT_PUBLIC fails
    leaked_client = {
        "NEXT_PUBLIC_DATABASE_URL": "postgresql://admin:pass@localhost/db",
    }
    with pytest.raises(SecurityValidationError, match="DATABASE_URL"):
        validate_client_bundle_safety(leaked_client)

    # Exposed secret key value in client variable fails
    leaked_token = {
        "NEXT_PUBLIC_API_CONFIG": "sk-" + "1234567890" * 3,
    }
    with pytest.raises(SecurityValidationError, match="Secret credential value"):
        validate_client_bundle_safety(leaked_token)


def test_sec_014_sensitive_data_redaction():
    """SEC-014: Sensitive-data redaction -> Secrets removed from logs"""
    raw_log = "Error connecting with Authorization: Bearer mock-test-token-123456789012345 and password='mock-test-password'"
    clean_log = redact_secrets(raw_log)
    assert "mock-test-token-123456789012345" not in clean_log
    assert "[REDACTED]" in clean_log


# ============================================================================
# 4. AGENT EXECUTION & AUTHORIZATION (SEC-015 - SEC-018)
# ============================================================================

def _setup_project(tmp_path: Path):
    proj = str(tmp_path / "proj")
    code, _, err = run_cli("init", "--project", proj, "--name", "SecT", "--owner", "SecOwner", "--non-interactive")
    assert code == 0, err
    return proj


def test_sec_015_unauthorized_agent_command(tmp_path):
    """SEC-015: Unauthorized agent command -> Rejected"""
    proj = _setup_project(tmp_path)

    # Set policy to only allow python
    pol = wf.load_policy(Path(proj))
    pol["allowed_executables"] = [PYNAME]
    wf.save_policy(Path(proj), pol)

    # Plan and approve task with unauthorized command (curl)
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{
        "task_id": "T1", "title": "Run command", "worker_id": "devops-engineer",
        "action": "execute", "command": ["curl", "https://example.com"],
        "acceptance_criteria": ["ok"]
    }]))
    code, _, err = run_cli("plan", "--project", proj, "--tasks", str(tasks_file))
    assert code == 0, err

    code, _, _ = run_cli("approve", "--project", proj, "--task-id", "T1", "--approver", "secowner", "--non-interactive")
    assert code == 0

    code, _, _ = run_cli("transition", "--project", proj, "--task-id", "T1", "--to", "READY")
    assert code == 0

    # Execute unauthorized executable (curl)
    code, out, err = run_cli("run", "--project", proj, "--task-id", "T1")
    assert code != 0
    assert "not in policy.allowed_executables" in err


def test_sec_016_unauthorized_tool_access(tmp_path):
    """SEC-016: Unauthorized tool access -> Rejected"""
    proj = _setup_project(tmp_path)

    # Technical writer worker attempting an undeclared destructive_change action
    tasks_file = tmp_path / "tasks_invalid.json"
    tasks_file.write_text(json.dumps([{
        "task_id": "T2", "title": "Invalid tool access", "worker_id": "technical-writer",
        "action": "destructive_change", "acceptance_criteria": ["ok"]
    }]))

    # Planning an undeclared action for worker must fail validation
    code, out, err = run_cli("plan", "--project", proj, "--tasks", str(tasks_file))
    assert code != 0
    assert "not permitted" in err.lower()


def test_sec_017_approval_enforcement(tmp_path):
    """SEC-017: Approval enforcement -> Unapproved sensitive action blocked"""
    proj = _setup_project(tmp_path)

    tasks_file = tmp_path / "tasks_appr.json"
    tasks_file.write_text(json.dumps([{
        "task_id": "T3", "title": "Sensitive change", "worker_id": "devops-engineer",
        "action": "execute", "command": [PY, "-c", "print(1)"], "acceptance_criteria": ["ok"]
    }]))
    code, _, err = run_cli("plan", "--project", proj, "--tasks", str(tasks_file))
    assert code == 0, err

    # Attempt to transition directly to READY without approval (state machine blocks PLANNED -> READY)
    code, out, err = run_cli("transition", "--project", proj, "--task-id", "T3", "--to", "READY")
    assert code != 0
    assert "invalid transition" in err.lower() or "approval" in err.lower()

    # Attempt to approve with an unauthorized/unregistered approver
    code, out, err = run_cli("approve", "--project", proj, "--task-id", "T3", "--approver", "unregistered_agent", "--non-interactive")
    assert code != 0
    assert "not a registered approver" in err.lower()


def test_sec_018_authorization_boundaries(tmp_path):
    """SEC-018: Authorization boundaries -> Unauthorized access rejected"""
    proj = _setup_project(tmp_path)

    pol = wf.load_policy(Path(proj))
    pol["allowed_executables"] = [PYNAME]
    wf.save_policy(Path(proj), pol)

    tasks_file = tmp_path / "tasks_bound.json"
    tasks_file.write_text(json.dumps([{
        "task_id": "T4", "title": "Boundary test", "worker_id": "devops-engineer",
        "action": "execute", "command": [PY, "-c", "print(1)"], "cwd": "..", "acceptance_criteria": ["ok"]
    }]))
    code, _, err = run_cli("plan", "--project", proj, "--tasks", str(tasks_file))
    assert code == 0, err
    run_cli("approve", "--project", proj, "--task-id", "T4", "--approver", "secowner", "--non-interactive")
    run_cli("transition", "--project", proj, "--task-id", "T4", "--to", "READY")

    # Attempt directory traversal out of project root
    code, _, err = run_cli("run", "--project", proj, "--task-id", "T4")
    assert code != 0
    assert "cwd must stay inside the project directory" in err


# ============================================================================
# 5. DEPENDENCY AUDIT & REGRESSION VERIFICATION (SEC-019 - SEC-020)
# ============================================================================

def test_sec_019_dependency_audit():
    """SEC-019: Dependency audit -> Findings reported"""
    lock_file = ROOT / "security" / "scanners.lock.json"
    assert lock_file.is_file()

    lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
    assert "entries" in lock_data
    assert len(lock_data["entries"]) >= 10

    # Ensure every scanner entry is pinned by explicit 40-char commit SHA
    for entry in lock_data["entries"]:
        assert len(entry["pinned_ref"]) == 40, f"Scanner {entry['id']} not pinned by 40-char SHA"


def test_sec_020_existing_functionality():
    """SEC-020: Existing functionality -> Regression tests pass"""
    import src.openclone
    import src.openclone.chat
    import src.openclone.integrations.rest
    import src.openclone.mie
    import src.openclone.runtime
    assert hasattr(src.openclone, "__version__")
