"""Tests for Paperclip connector, authoritative approval gates, and mobile compliance."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import time
import pytest

from src.openclone.integrations.paperclip.connector import (
    AuthoritativeApprovalRecord,
    AuthoritativeApprovalStore,
    PaperclipBudgetContext,
    PaperclipConnector,
    PaperclipTaskRequest,
    PaperclipTaskResponse,
    PaperclipTaskStatus,
)
from src.openclone.compliance.mobile.app_store import MobileComplianceScanner


def test_paperclip_connector_intake_normal_task():
    """Verify standard engineering task intake succeeds within budget."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        req = PaperclipTaskRequest(
            external_task_id="ext-task-001",
            organization_id="org-acme",
            title="Refactor auth module",
            description="Refactor user session storage",
            requester_agent_id="agent-coordinator",
            budget=PaperclipBudgetContext(budget_id="b-1", max_spend_usd=100.0, current_spend_usd=10.0),
            target_project_root=tmpdir,
        )
        res = connector.intake_task(req)
        assert res.accepted is True
        assert res.status == PaperclipTaskStatus.IN_PROGRESS
        assert res.openclone_task_id is not None


def test_paperclip_connector_rejects_budget_overrun():
    """Verify task is rejected when budget ceiling is exceeded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        req = PaperclipTaskRequest(
            external_task_id="ext-task-overbudget",
            organization_id="org-acme",
            title="Train model",
            description="Heavy GPU job",
            requester_agent_id="agent-coordinator",
            budget=PaperclipBudgetContext(budget_id="b-2", max_spend_usd=50.0, current_spend_usd=55.0),
            target_project_root=tmpdir,
        )
        res = connector.intake_task(req)
        assert res.accepted is False
        assert res.status == PaperclipTaskStatus.BLOCKED
        assert "Budget ceiling exceeded" in res.reason


def test_paperclip_connector_rejects_path_escape():
    """Verify connector prevents path traversal outside project root."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir) / "subproject")
        req = PaperclipTaskRequest(
            external_task_id="ext-escape-001",
            organization_id="org-acme",
            title="Wipe parent directory",
            description="Escape sandbox",
            requester_agent_id="agent-malicious",
            target_project_root=str(Path(tmpdir)),  # Escapes subproject
        )
        res = connector.intake_task(req)
        assert res.accepted is False
        assert res.status == PaperclipTaskStatus.BLOCKED
        assert "violates workspace trust boundary" in res.reason


def test_paperclip_task_completion_records_evidence():
    """Verify task completion computes SHA-256 evidence hashes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        req = PaperclipTaskRequest(
            external_task_id="ext-task-complete",
            organization_id="org-acme",
            title="Generate API docs",
            description="Build documentation",
            requester_agent_id="agent-docs",
            target_project_root=tmpdir,
        )
        connector.intake_task(req)

        evidence_file = Path(tmpdir) / "evidence.txt"
        evidence_file.write_text("verification pass data", encoding="utf-8")

        res = connector.complete_task(
            external_task_id="ext-task-complete",
            evidence_files=[evidence_file],
            spend_usd=1.5,
            tokens_consumed=1200,
        )
        assert res.accepted is True
        assert res.status == PaperclipTaskStatus.COMPLETED
        assert len(res.evidence_hashes) == 1
        assert "evidence.txt:" in res.evidence_hashes[0]


def test_paperclip_authoritative_approval_matrix():
    """Comprehensive verification of the 9 authoritative approval scenarios."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = AuthoritativeApprovalStore(allowed_approvers=["alice-admin"])
        connector = PaperclipConnector(workspace_root=Path(tmpdir), approval_store=store)

        org_id = "org-acme"
        ext_task_id = "ext-prod-deploy-001"
        title = "Production Deploy of Billing Service"
        desc = "Deploying to prod cluster"
        action = "production deploy"
        now = time.time()

        # Compute matching canonical digest
        canonical_digest = PaperclipConnector.compute_task_digest(
            organization_id=org_id,
            external_task_id=ext_task_id,
            workspace_root=tmpdir,
            action=action,
            title=title,
            description=desc,
        )

        # SCENARIO 1: human_approved: True without approval_id is strictly REJECTED
        req1 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"human_approved": True},
        )
        res1 = connector.intake_task(req1)
        assert res1.accepted is False
        assert res1.status == PaperclipTaskStatus.NEEDS_APPROVAL
        assert "authoritative human approval record" in res1.reason

        # SCENARIO 2: Invalid approval_digest format (not 64-char hex) is REJECTED
        req2 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-001", "approval_digest": "not-valid-hex!"},
        )
        res2 = connector.intake_task(req2)
        assert res2.accepted is False
        assert "Invalid SHA-256 approval digest format" in res2.reason

        # SCENARIO 3: Non-existent approval_id is REJECTED
        req3 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-nonexistent"},
        )
        res3 = connector.intake_task(req3)
        assert res3.accepted is False
        assert "not found in authoritative registry" in res3.reason

        # SCENARIO 4: Expired approval is REJECTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-expired",
            approver_id="alice-admin",
            task_digest=canonical_digest,
            workspace_root=tmpdir,
            action=action,
            created_at=now - 200,
            expires_at=now - 50,  # Expired
        ))
        req4 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-expired"},
        )
        res4 = connector.intake_task(req4)
        assert res4.accepted is False
        assert "Approval has expired" in res4.reason

        # SCENARIO 5: Tampered task contents (digest mismatch) is REJECTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-tampered",
            approver_id="alice-admin",
            task_digest=canonical_digest,
            workspace_root=tmpdir,
            action=action,
            created_at=now,
            expires_at=now + 3600,
        ))
        req5 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description="TAMPERED DESCRIPTION: drop database instead",
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-tampered"},
        )
        res5 = connector.intake_task(req5)
        assert res5.accepted is False
        assert "Cryptographic task digest mismatch" in res5.reason

        # SCENARIO 6: Cross-workspace mismatch is REJECTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-diff-ws",
            approver_id="alice-admin",
            task_digest=canonical_digest,
            workspace_root="/some/other/workspace",
            action=action,
            created_at=now,
            expires_at=now + 3600,
        ))
        req6 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-diff-ws"},
        )
        res6 = connector.intake_task(req6)
        assert res6.accepted is False
        assert "does not match target workspace" in res6.reason

        # SCENARIO 7: Action mismatch is REJECTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-diff-action",
            approver_id="alice-admin",
            task_digest=canonical_digest,
            workspace_root=tmpdir,
            action="rotate keys",  # Different action
            created_at=now,
            expires_at=now + 3600,
        ))
        req7 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-diff-action"},
        )
        res7 = connector.intake_task(req7)
        assert res7.accepted is False
        assert "does not match requested action" in res7.reason

        # SCENARIO 8: Unauthorized approver identity is REJECTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-bad-approver",
            approver_id="untrusted-user",
            task_digest=canonical_digest,
            workspace_root=tmpdir,
            action=action,
            created_at=now,
            expires_at=now + 3600,
        ))
        req8 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-bad-approver"},
        )
        res8 = connector.intake_task(req8)
        assert res8.accepted is False
        assert "not in authorized human approver policy" in res8.reason

        # SCENARIO 9: Valid bound approval is ACCEPTED
        store.register_approval(AuthoritativeApprovalRecord(
            approval_id="app-valid",
            approver_id="alice-admin",
            task_digest=canonical_digest,
            workspace_root=tmpdir,
            action=action,
            created_at=now,
            expires_at=now + 3600,
        ))
        req9 = PaperclipTaskRequest(
            external_task_id=ext_task_id,
            organization_id=org_id,
            title=title,
            description=desc,
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"approval_id": "app-valid"},
        )
        res9 = connector.intake_task(req9)
        assert res9.accepted is True
        assert res9.status == PaperclipTaskStatus.IN_PROGRESS

        # SCENARIO 10: Replay attack (consuming already-consumed approval) is REJECTED
        res10 = connector.intake_task(req9)
        assert res10.accepted is False
        assert "already been consumed" in res10.reason


def test_mobile_compliance_scanner_clean():
    """Verify scanner flags missing PrivacyInfo.xcprivacy with a warning."""
    with tempfile.TemporaryDirectory() as tmpdir:
        scanner = MobileComplianceScanner(project_root=Path(tmpdir))
        report = scanner.run_audit()
        assert report.ios_compliant is True  # Warning does not fail compliance error gate
        assert any(f.rule_id == "IOS-PRIVACY-001" for f in report.findings)


def test_mobile_compliance_scanner_catches_missing_key():
    """Verify scanner catches PrivacyInfo.xcprivacy missing mandatory keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "PrivacyInfo.xcprivacy"
        p.write_text("<plist><dict><key>SomeKey</key><string>Val</string></dict></plist>", encoding="utf-8")
        scanner = MobileComplianceScanner(project_root=Path(tmpdir))
        report = scanner.run_audit()
        assert report.ios_compliant is False
        assert any(f.rule_id == "IOS-PRIVACY-002" for f in report.findings)
