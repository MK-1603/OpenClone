"""Paperclip Remote HTTP Adapter Server.

Provides a secure HTTP REST interface for remote Paperclip instances to interact
with OpenClone Engineering Governance. Enforces HMAC-SHA256 signatures, replay protection
via nonces and timestamps, path containment, and authoritative human approvals.
"""
from __future__ import annotations

import collections
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import sqlite3
import threading
import time
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.integrations.paperclip.connector import (
    AuthoritativeApprovalRecord,
    AuthoritativeApprovalStore,
    PaperclipBudgetContext,
    PaperclipConnector,
    PaperclipTaskRequest,
    PaperclipTaskResponse,
    PaperclipTaskStatus,
)

logger = logging.getLogger("openclone.integrations.paperclip.server")

MAX_REQUEST_BYTES = 10 * 1024 * 1024  # 10MB payload ceiling to prevent DoS


class PaperclipRateLimiter:
    """Thread-safe sliding-window rate limiter per client identifier."""

    def __init__(self, max_requests: int = 120, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, collections.deque] = collections.defaultdict(collections.deque)
        self._lock = threading.Lock()

    def is_allowed(self, client_key: str, now: Optional[float] = None) -> bool:
        t = now or time.time()
        with self._lock:
            q = self._history[client_key]
            cutoff = t - self.window_seconds
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= self.max_requests:
                return False
            q.append(t)
            return True


class PaperclipSecurityAuth:
    """Handles HMAC request signing, timestamp expiration, and persistent/atomic nonce tracking."""

    def __init__(
        self,
        secret_key: str,
        max_drift_seconds: int = 300,
        nonce_db_path: Optional[Path] = None,
    ):
        self.secret_key = secret_key.encode("utf-8")
        self.max_drift_seconds = max_drift_seconds
        self.nonce_db_path = nonce_db_path
        self._seen_nonces: Dict[str, float] = {}
        self._lock = threading.Lock()

        if self.nonce_db_path:
            self._init_sqlite_nonce_db()

    def _init_sqlite_nonce_db(self):
        """Initialize atomic SQLite persistent nonce store."""
        if not self.nonce_db_path:
            return
        self.nonce_db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.nonce_db_path))
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS paperclip_nonces ("
                "nonce TEXT PRIMARY KEY, "
                "timestamp REAL NOT NULL"
                ")"
            )
            conn.commit()
        finally:
            conn.close()

    def verify_request(
        self,
        method: str,
        path: str,
        timestamp_str: str,
        nonce: str,
        body_bytes: bytes,
        provided_signature: str,
    ) -> Tuple[bool, str]:
        """Verify request authenticity and protect against replay attacks."""
        if not timestamp_str or not nonce or not provided_signature:
            return False, "Missing required security headers (X-Paperclip-Timestamp, X-Paperclip-Nonce, X-Paperclip-Signature)"

        try:
            req_time = float(timestamp_str)
        except ValueError:
            return False, "Invalid timestamp format"

        now = time.time()
        if abs(now - req_time) > self.max_drift_seconds:
            return False, f"Request timestamp expired or skewed beyond {self.max_drift_seconds}s limit"

        # Check nonce replay atomically
        if not self._record_nonce_atomic(nonce, req_time, now):
            return False, "Duplicate nonce detected: replay attack prevented"

        # Compute HMAC-SHA256 signature
        body_hash = hashlib.sha256(body_bytes).hexdigest()
        canonical_string = f"{method.upper()}\n{path}\n{timestamp_str}\n{nonce}\n{body_hash}"
        computed_sig = hmac.new(self.secret_key, canonical_string.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(computed_sig, provided_signature):
            return False, "Invalid HMAC signature"

        return True, "Authorized"

    def _record_nonce_atomic(self, nonce: str, req_time: float, now: float) -> bool:
        """Atomically record nonce; returns False if already seen (replay)."""
        if self.nonce_db_path:
            conn = None
            try:
                conn = sqlite3.connect(str(self.nonce_db_path), timeout=5.0)
                cutoff = now - (self.max_drift_seconds * 2)
                conn.execute("DELETE FROM paperclip_nonces WHERE timestamp < ?", (cutoff,))
                conn.execute("INSERT INTO paperclip_nonces(nonce, timestamp) VALUES(?, ?)", (nonce, req_time))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
            except Exception as e:
                logger.error("SQLite nonce check error: %s; falling back to in-memory check", e)
            finally:
                if conn:
                    conn.close()

        # In-memory fallback
        with self._lock:
            cutoff = now - (self.max_drift_seconds * 2)
            expired = [k for k, v in self._seen_nonces.items() if v < cutoff]
            for k in expired:
                del self._seen_nonces[k]

            if nonce in self._seen_nonces:
                return False
            self._seen_nonces[nonce] = req_time
            return True


class PaperclipHttpHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Paperclip integration endpoints."""

    connector: PaperclipConnector = PaperclipConnector()
    auth_engine: Optional[PaperclipSecurityAuth] = None
    rate_limiter: PaperclipRateLimiter = PaperclipRateLimiter()

    def _send_json(self, status_code: int, data: Dict[str, Any]):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_rate_limit(self) -> bool:
        client_ip = self.client_address[0] if self.client_address else "unknown"
        if not self.rate_limiter.is_allowed(client_ip):
            self._send_json(429, {"error": "TooManyRequests", "reason": "Rate limit exceeded"})
            return False
        return True

    def _authenticate(self) -> bool:
        if not self._check_rate_limit():
            return False

        # Enforce request payload size ceiling
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self._send_json(400, {"error": "InvalidContentLength"})
            return False

        if content_length > MAX_REQUEST_BYTES:
            self._send_json(413, {"error": "PayloadTooLarge", "reason": f"Payload exceeds {MAX_REQUEST_BYTES} bytes"})
            return False

        body_bytes = self.rfile.read(content_length) if content_length > 0 else b""
        self._cached_body = body_bytes

        if self.auth_engine is None:
            # Local-only unauthenticated mode
            return True

        method = self.command
        path = self.path.split("?")[0]
        timestamp = self.headers.get("X-Paperclip-Timestamp", "")
        nonce = self.headers.get("X-Paperclip-Nonce", "")
        signature = self.headers.get("X-Paperclip-Signature", "")

        ok, reason = self.auth_engine.verify_request(method, path, timestamp, nonce, body_bytes, signature)
        if not ok:
            self._send_json(401, {"error": "Unauthorized", "reason": reason})
            return False
        return True

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/v1/paperclip/health":
            self._send_json(200, {
                "status": "healthy",
                "service": "openclone-paperclip-adapter",
                "version": "1.0.0",
                "active_tasks": len(self.connector._active_tasks),
            })
            return

        if not self._authenticate():
            return

        if path == "/api/v1/paperclip/capabilities":
            self._send_json(200, {
                "capabilities": [
                    "governed_task_intake",
                    "cryptographic_evidence_verification",
                    "budget_ceiling_enforcement",
                    "authoritative_human_approval_gate",
                    "persistent_replay_protection",
                    "task_cancellation",
                ],
                "gateway_mode": "authenticated_remote" if self.auth_engine else "local_only",
            })
            return

        if path == "/api/v1/paperclip/tasks":
            summaries = [
                {
                    "task_id": tid,
                    "title": req.title,
                    "organization_id": req.organization_id,
                    "status": "in_progress",
                }
                for tid, req in self.connector._active_tasks.items()
            ]
            self._send_json(200, {"tasks": summaries, "count": len(summaries)})
            return

        if path.startswith("/api/v1/paperclip/tasks/"):
            task_id = path.replace("/api/v1/paperclip/tasks/", "").strip()
            if task_id in self.connector._active_tasks:
                req = self.connector._active_tasks[task_id]
                self._send_json(200, {
                    "task_id": task_id,
                    "title": req.title,
                    "organization_id": req.organization_id,
                    "status": "in_progress",
                })
            else:
                self._send_json(404, {"error": "TaskNotFound", "task_id": task_id})
            return

        self._send_json(404, {"error": "NotFound", "path": path})

    def do_POST(self):
        path = self.path.split("?")[0]
        if not self._authenticate():
            return

        if path == "/api/v1/paperclip/tasks":
            try:
                body_bytes = getattr(self, "_cached_body", b"")
                payload = json.loads(body_bytes.decode("utf-8"))
                budget_data = payload.get("budget")
                budget = PaperclipBudgetContext(**budget_data) if budget_data else None

                task_req = PaperclipTaskRequest(
                    external_task_id=payload["external_task_id"],
                    organization_id=payload.get("organization_id", "default"),
                    title=payload["title"],
                    description=payload.get("description", ""),
                    requester_agent_id=payload.get("requester_agent_id", "external-agent"),
                    budget=budget,
                    target_project_root=payload.get("target_project_root"),
                    metadata=payload.get("metadata", {}),
                )
                response = self.connector.intake_task(task_req)
                code = 200 if response.accepted else 400
                self._send_json(code, asdict(response))
            except Exception as e:
                self._send_json(400, {"error": "InvalidRequestPayload", "message": str(e)})
            return

        if path.endswith("/cancel"):
            # Task cancellation endpoint: /api/v1/paperclip/tasks/{task_id}/cancel
            parts = path.split("/")
            if len(parts) >= 6 and parts[4] == "tasks" and parts[5] != "cancel":
                task_id = parts[5]
                if task_id in self.connector._active_tasks:
                    del self.connector._active_tasks[task_id]
                    self._send_json(200, {"task_id": task_id, "status": "cancelled", "reason": "User cancelled"})
                else:
                    self._send_json(404, {"error": "TaskNotFound", "task_id": task_id})
                return

        self._send_json(404, {"error": "NotFound", "path": path})

    def do_DELETE(self):
        path = self.path.split("?")[0]
        if not self._authenticate():
            return

        if path.startswith("/api/v1/paperclip/tasks/"):
            task_id = path.replace("/api/v1/paperclip/tasks/", "").strip()
            if task_id in self.connector._active_tasks:
                del self.connector._active_tasks[task_id]
                self._send_json(200, {"task_id": task_id, "status": "deleted", "reason": "Task removed"})
            else:
                self._send_json(404, {"error": "TaskNotFound", "task_id": task_id})
            return

        self._send_json(404, {"error": "NotFound", "path": path})

    def log_message(self, format, *args):
        pass  # Quiet standard logging to prevent clutter
