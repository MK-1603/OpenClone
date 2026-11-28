"""Unit and integration tests for Enterprise Operational Intelligence components:
- Paperclip Remote HTTP Adapter (HMAC authentication, persistent replay protection, rate limiting, endpoints)
- Engineering Command Center Dashboard Service (DAG calculation, cycle detection, path security, HTML generation)
- Mobile Device Lab Adapter (hardware descriptors, security sanitization, ADB execution contracts)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
import tempfile
import time
from pathlib import Path
import pytest

from src.openclone.integrations.paperclip.connector import (
    AuthoritativeApprovalRecord,
    AuthoritativeApprovalStore,
    PaperclipConnector,
    PaperclipTaskRequest,
    PaperclipTaskStatus,
)
from src.openclone.integrations.paperclip.server import (
    PaperclipHttpHandler,
    PaperclipRateLimiter,
    PaperclipSecurityAuth,
)
from src.openclone.dashboard.service import DashboardService
from src.openclone.testing.mobile.adapter import DeviceInfo, LocalAdbDeviceLabAdapter
from src.openclone.runtime.workforce import Ledger


def test_paperclip_hmac_auth_valid():
    """Verify HMAC signature passes verification with fresh timestamp and valid nonce."""
    secret = "test-secret-key-12345"
    auth = PaperclipSecurityAuth(secret_key=secret)
    now_str = str(time.time())
    nonce = "unique-nonce-1"
    body = b'{"task": "deploy"}'
    
    body_hash = hashlib.sha256(body).hexdigest()
    canonical = f"POST\n/api/v1/paperclip/tasks\n{now_str}\n{nonce}\n{body_hash}"
    sig = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()

    ok, reason = auth.verify_request("POST", "/api/v1/paperclip/tasks", now_str, nonce, body, sig)
    assert ok is True
    assert reason == "Authorized"


def test_paperclip_hmac_replay_prevention():
    """Verify duplicate nonces are rejected as replay attacks in-memory."""
    secret = "test-secret-key-12345"
    auth = PaperclipSecurityAuth(secret_key=secret)
    now_str = str(time.time())
    nonce = "replay-nonce-test"
    body = b'{"task": "test"}'
    
    body_hash = hashlib.sha256(body).hexdigest()
    canonical = f"POST\n/api/v1/paperclip/tasks\n{now_str}\n{nonce}\n{body_hash}"
    sig = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()

    # First attempt passes
    ok1, _ = auth.verify_request("POST", "/api/v1/paperclip/tasks", now_str, nonce, body, sig)
    assert ok1 is True

    # Immediate second attempt with same nonce is rejected
    ok2, reason2 = auth.verify_request("POST", "/api/v1/paperclip/tasks", now_str, nonce, body, sig)
    assert ok2 is False
    assert "Duplicate nonce detected" in reason2


def test_paperclip_persistent_sqlite_replay_prevention():
    """Verify replay protection persists across server instances using SQLite atomic storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "nonces.sqlite3"
        secret = "persistent-secret-key-999"

        # Server instance 1 receives request
        auth1 = PaperclipSecurityAuth(secret_key=secret, nonce_db_path=db_path)
        now_str = str(time.time())
        nonce = "persistent-nonce-xyz"
        body = b'{"task": "db-migration"}'

        body_hash = hashlib.sha256(body).hexdigest()
        canonical = f"POST\n/api/v1/paperclip/tasks\n{now_str}\n{nonce}\n{body_hash}"
        sig = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()

        ok1, reason1 = auth1.verify_request("POST", "/api/v1/paperclip/tasks", now_str, nonce, body, sig)
        assert ok1 is True
        assert reason1 == "Authorized"

        # Server instance 2 (simulating restart or second worker) receives replayed request
        auth2 = PaperclipSecurityAuth(secret_key=secret, nonce_db_path=db_path)
        ok2, reason2 = auth2.verify_request("POST", "/api/v1/paperclip/tasks", now_str, nonce, body, sig)
        assert ok2 is False
        assert "Duplicate nonce detected" in reason2


def test_paperclip_rate_limiter():
    """Verify rate limiter blocks client requests exceeding the configured ceiling."""
    limiter = PaperclipRateLimiter(max_requests=3, window_seconds=10.0)
    client = "192.168.1.100"
    now = time.time()

    assert limiter.is_allowed(client, now=now) is True
    assert limiter.is_allowed(client, now=now + 1) is True
    assert limiter.is_allowed(client, now=now + 2) is True
    # 4th request exceeds max_requests=3
    assert limiter.is_allowed(client, now=now + 3) is False
    # After window passes, new requests are allowed
    assert limiter.is_allowed(client, now=now + 11) is True


def test_paperclip_hmac_expired_timestamp():
    """Verify expired timestamps (>300s) are rejected."""
    auth = PaperclipSecurityAuth(secret_key="key", max_drift_seconds=300)
    old_time_str = str(time.time() - 400)
    ok, reason = auth.verify_request("GET", "/health", old_time_str, "nonce-x", b"", "any-sig")
    assert ok is False
    assert "expired" in reason.lower()


def test_dashboard_service_overview_and_dag():
    """Verify DashboardService produces accurate overview, task DAG, cycle detection, and tiers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        ledger = Ledger(p)
        ledger.conn.execute(
            "INSERT INTO tasks(task_id, project_id, title, worker_id, status, action, budget_usd, estimated_cost_usd, depends_on, created_at, updated_at) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("T1", "proj", "Build Feature", "frontend-engineer", "SUCCEEDED", "write", 50.0, 50.0, "[]", "2026-01-01", "2026-01-01")
        )
        ledger.conn.execute(
            "INSERT INTO tasks(task_id, project_id, title, worker_id, status, action, budget_usd, estimated_cost_usd, depends_on, created_at, updated_at) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("T2", "proj", "Test Feature", "test-engineer", "PLANNED", "execute", 25.0, 25.0, '["T1"]', "2026-01-01", "2026-01-01")
        )
        ledger.commit()
        ledger.close()

        service = DashboardService(p)
        overview = service.get_overview()
        assert overview.total_tasks == 2
        assert overview.completed_tasks == 1
        assert overview.ledger_integrity_ok is True

        dag = service.get_task_dag()
        assert dag["node_count"] == 2
        assert dag["edge_count"] == 1
        assert dag["has_cycles"] is False
        assert "T2" in dag["ready_tasks"]
        assert dag["tiers"]["T1"] == 0
        assert dag["tiers"]["T2"] == 1

        details = service.get_task_details("T1")
        assert details is not None
        assert details["title"] == "Build Feature"
        assert details["status"] == "SUCCEEDED"

        # Path traversal protection test
        safe_path = service.resolve_safe_artifact_path("src/module.py")
        assert safe_path is not None
        unsafe_path = service.resolve_safe_artifact_path("../../etc/passwd")
        assert unsafe_path is None

        html = service.render_html_dashboard()
        assert "OpenClone Engineering Command Center" in html
        assert "T1" in html
        assert "T2" in html


def test_dashboard_service_detects_cycles():
    """Verify DashboardService correctly flags dependency cycles in the DAG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        ledger = Ledger(p)
        # T1 depends on T2, T2 depends on T1
        ledger.conn.execute(
            "INSERT INTO tasks(task_id, project_id, title, worker_id, status, action, budget_usd, estimated_cost_usd, depends_on, created_at, updated_at) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("T1", "proj", "Task 1", "w1", "PLANNED", "write", 10.0, 10.0, '["T2"]', "2026-01-01", "2026-01-01")
        )
        ledger.conn.execute(
            "INSERT INTO tasks(task_id, project_id, title, worker_id, status, action, budget_usd, estimated_cost_usd, depends_on, created_at, updated_at) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("T2", "proj", "Task 2", "w2", "PLANNED", "write", 10.0, 10.0, '["T1"]', "2026-01-01", "2026-01-01")
        )
        ledger.commit()
        ledger.close()

        service = DashboardService(p)
        dag = service.get_task_dag()
        assert dag["has_cycles"] is True
        html = service.render_html_dashboard()
        assert "Cycle detected" in html


def test_mobile_device_lab_adapter():
    """Verify device lab adapter data structures, discovery, and input validation."""
    adapter = LocalAdbDeviceLabAdapter(adb_path="mock-non-existent-adb")
    assert adapter.is_available() is False
    assert adapter.list_devices() == []

    # Input validation tests: rejecting dangerous shell metacharacters
    assert adapter._validate_device_id("emulator-5554") is True
    assert adapter._validate_device_id("RFCW10ABCDE") is True
    assert adapter._validate_device_id("device; rm -rf /") is False
    assert adapter._validate_device_id("device | cat /etc/passwd") is False
    assert adapter._validate_device_id("dev`whoami`") is False
    assert adapter._validate_device_id("") is False

    dev = DeviceInfo(
        device_id="device-1234",
        platform="android",
        model="Pixel 8 Pro",
        os_version="Android 14",
        status="device",
        is_emulator=False,
    )
    assert dev.is_emulator is False
    assert dev.model == "Pixel 8 Pro"
