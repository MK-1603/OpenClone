"""Unit and integration tests for Enterprise Operational Intelligence components:
- Paperclip Remote HTTP Adapter (HMAC authentication, replay protection, endpoints)
- Engineering Command Center Dashboard Service (DAG calculation, HTML generation)
- Mobile Device Lab Adapter (hardware descriptors, ADB availability)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import tempfile
import time
from pathlib import Path
import pytest

from src.openclone.integrations.paperclip.connector import PaperclipConnector, PaperclipTaskRequest
from src.openclone.integrations.paperclip.server import PaperclipSecurityAuth, PaperclipHttpHandler
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
    """Verify duplicate nonces are rejected as replay attacks."""
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


def test_paperclip_hmac_expired_timestamp():
    """Verify expired timestamps (>300s) are rejected."""
    auth = PaperclipSecurityAuth(secret_key="key", max_drift_seconds=300)
    old_time_str = str(time.time() - 400)
    ok, reason = auth.verify_request("GET", "/health", old_time_str, "nonce-x", b"", "any-sig")
    assert ok is False
    assert "expired" in reason.lower()


def test_dashboard_service_overview_and_dag():
    """Verify DashboardService produces accurate overview and task DAG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        ledger = Ledger(p)
        ledger.conn.execute(
            "INSERT INTO tasks(task_id, project_id, title, worker_id, status, action, budget_usd, estimated_cost_usd, depends_on, created_at, updated_at) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("T1", "proj", "Build Feature", "frontend-engineer", "RUNNING", "write", 50.0, 50.0, "[]", "2026-01-01", "2026-01-01")
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
        assert overview.running_tasks == 1
        assert overview.ledger_integrity_ok is True

        dag = service.get_task_dag()
        assert dag["node_count"] == 2
        assert dag["edge_count"] == 1
        assert dag["edges"][0] == {"from": "T1", "to": "T2"}

        html = service.render_html_dashboard()
        assert "OpenKryvex Engineering Command Center" in html
        assert "T1" in html
        assert "T2" in html


def test_mobile_device_lab_adapter():
    """Verify device lab adapter data structures and discovery behavior."""
    adapter = LocalAdbDeviceLabAdapter(adb_path="mock-non-existent-adb")
    assert adapter.is_available() is False
    assert adapter.list_devices() == []

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
