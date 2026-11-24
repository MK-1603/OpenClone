"""Unit tests for Paperclip integration connector and Mobile compliance scanner."""
from __future__ import annotations

import tempfile
from pathlib import Path
import pytest

from src.openclone.integrations.paperclip.connector import (
    PaperclipBudgetContext,
    PaperclipConnector,
    PaperclipTaskRequest,
    PaperclipTaskStatus,
)
from src.openclone.compliance.mobile.app_store import (
    MobileComplianceScanner,
    ComplianceFinding,
)


def test_paperclip_task_intake_within_budget():
    """Verify Paperclip task is accepted when within budget."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        budget = PaperclipBudgetContext(budget_id="b1", max_spend_usd=100.0, current_spend_usd=10.0)
        req = PaperclipTaskRequest(
            external_task_id="ext-001",
            organization_id="org-acme",
            title="Implement OAuth Auth",
            description="Add OAuth provider support",
            requester_agent_id="agent-pm",
            budget=budget,
            target_project_root=tmpdir,
        )
        res = connector.intake_task(req)
        assert res.accepted is True
        assert res.status == PaperclipTaskStatus.IN_PROGRESS
        assert res.openclone_task_id is not None


def test_paperclip_task_rejected_on_exhausted_budget():
    """Verify Paperclip task is blocked when budget is exhausted."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        budget = PaperclipBudgetContext(budget_id="b2", max_spend_usd=50.0, current_spend_usd=50.0)
        req = PaperclipTaskRequest(
            external_task_id="ext-002",
            organization_id="org-acme",
            title="Costly Operation",
            description="Exceeds budget",
            requester_agent_id="agent-pm",
            budget=budget,
            target_project_root=tmpdir,
        )
        res = connector.intake_task(req)
        assert res.accepted is False
        assert res.status == PaperclipTaskStatus.BLOCKED
        assert "Budget ceiling exceeded" in res.reason


def test_paperclip_task_completion_evidence():
    """Verify task completion generates verifiable cryptographic evidence hashes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        req = PaperclipTaskRequest(
            external_task_id="ext-003",
            organization_id="org-acme",
            title="Audit File",
            description="Check report",
            requester_agent_id="agent-auditor",
            target_project_root=tmpdir,
        )
        connector.intake_task(req)
        
        # Create dummy evidence file
        ev_file = Path(tmpdir) / "evidence.txt"
        ev_file.write_text("Audit pass", encoding="utf-8")

        res = connector.complete_task("ext-003", evidence_files=[ev_file], spend_usd=0.25, tokens_consumed=150)
        assert res.accepted is True
        assert res.status == PaperclipTaskStatus.COMPLETED
        assert len(res.evidence_hashes) == 1
        assert "evidence.txt:" in res.evidence_hashes[0]


def test_paperclip_sensitive_action_requires_human_approval():
    """Verify Paperclip cannot bypass human approval for production deployment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector = PaperclipConnector(workspace_root=Path(tmpdir))
        req = PaperclipTaskRequest(
            external_task_id="ext-prod-deploy",
            organization_id="org-acme",
            title="Production Deploy of Billing Service",
            description="Deploying to prod cluster",
            requester_agent_id="agent-coordinator",
            target_project_root=tmpdir,
            metadata={"human_approved": False},
        )
        res = connector.intake_task(req)
        assert res.accepted is False
        assert res.status == PaperclipTaskStatus.NEEDS_APPROVAL
        assert "requires explicit human owner approval" in res.reason


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
