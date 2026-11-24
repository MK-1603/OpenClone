"""Paperclip Remote HTTP Adapter Server.

Provides a secure HTTP REST interface for remote Paperclip instances to interact
with OpenClone Engineering Governance. Enforces HMAC-SHA256 signatures, replay protection
via nonces and timestamps, path containment, and authoritative human approvals.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from src.openclone.integrations.paperclip.connector import (
    PaperclipBudgetContext,
    PaperclipConnector,
    PaperclipTaskRequest,
    PaperclipTaskResponse,
    PaperclipTaskStatus,
)

logger = logging.getLogger("openclone.integrations.paperclip.server")


class PaperclipSecurityAuth:
    """Handles HMAC request signing, timestamp expiration, and nonce tracking."""

    def __init__(self, secret_key: str, max_drift_seconds: int = 300):
        self.secret_key = secret_key.encode("utf-8")
        self.max_drift_seconds = max_drift_seconds
        self._seen_nonces: Dict[str, float] = {}

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

        # Check nonce replay
        self._cleanup_old_nonces(now)
        if nonce in self._seen_nonces:
            return False, "Duplicate nonce detected: replay attack prevented"
        self._seen_nonces[nonce] = now

        # Compute HMAC-SHA256 signature
        body_hash = hashlib.sha256(body_bytes).hexdigest()
        canonical_string = f"{method.upper()}\n{path}\n{timestamp_str}\n{nonce}\n{body_hash}"
        computed_sig = hmac.new(self.secret_key, canonical_string.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(computed_sig, provided_signature):
            return False, "Invalid HMAC signature"

        return True, "Authorized"

    def _cleanup_old_nonces(self, now: float):
        cutoff = now - (self.max_drift_seconds * 2)
        expired = [k for k, v in self._seen_nonces.items() if v < cutoff]
        for k in expired:
            del self._seen_nonces[k]


class PaperclipHttpHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Paperclip integration endpoints."""

    connector: PaperclipConnector = PaperclipConnector()
    auth_engine: Optional[PaperclipSecurityAuth] = None

    def _send_json(self, status_code: int, data: Dict[str, Any]):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authenticate(self) -> bool:
        if self.auth_engine is None:
            # Local-only unauthenticated mode (or disabled authentication)
            return True

        method = self.command
        path = self.path.split("?")[0]
        timestamp = self.headers.get("X-Paperclip-Timestamp", "")
        nonce = self.headers.get("X-Paperclip-Nonce", "")
        signature = self.headers.get("X-Paperclip-Signature", "")

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b""
        self._cached_body = body_bytes

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
                "version": "2.0.0",
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
                    "human_approval_gate",
                ],
                "gateway_mode": "authenticated_remote" if self.auth_engine else "local_only",
            })
            return

        if path.startswith("/api/v1/paperclip/tasks/"):
            task_id = path.replace("/api/v1/paperclip/tasks/", "").strip()
            if task_id in self.connector._active_tasks:
                req = self.connector._active_tasks[task_id]
                self._send_json(200, {
                    "task_id": task_id,
                    "title": req.title,
                    "organization_id": req.organization_id,
                    "status": "registered",
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
                body_bytes = getattr(self, "_cached_body", None)
                if body_bytes is None:
                    content_length = int(self.headers.get("Content-Length", 0))
                    body_bytes = self.rfile.read(content_length)

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

        self._send_json(404, {"error": "NotFound", "path": path})

    def log_message(self, format, *args):
        pass  # Quiet standard logging to prevent clutter
