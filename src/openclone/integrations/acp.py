"""OpenClone Agent Client Protocol (ACP) Interoperability Adapter.

Provides standardized JSON-RPC 2.0 protocol handling for editors and streaming
AI clients supporting the Agent Client Protocol (e.g. Zed Assistant, ACP clients).
"""
from __future__ import annotations

import json
import logging
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import ExecutionMode
from src.openclone.integrations.gateway import redact_secrets

logger = logging.getLogger("openclone.integrations.acp")


class ACPSession:
    """Active ACP conversation and execution session."""

    def __init__(self, session_id: str, workspace_root: Path, client_capabilities: Optional[List[str]] = None):
        self.session_id = session_id
        self.workspace_root = workspace_root
        self.client_capabilities = client_capabilities or []
        self.created_at = time.time()
        self.last_active = time.time()
        self.history: List[Dict[str, Any]] = []
        self.active_plan: Optional[Dict[str, Any]] = None
        self.status = "READY"


class ACPAdapter:
    """Agent Client Protocol Adapter for OpenClone Gateway."""

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.sessions: Dict[str, ACPSession] = {}
        self.engine = AutonomousExecutionEngine(self.workspace_root)

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch an ACP JSON-RPC 2.0 message."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "initialize":
                return self._handle_initialize(req_id, params)
            elif method == "session/create":
                return self._handle_session_create(req_id, params)
            elif method == "session/prompt":
                return self._handle_session_prompt(req_id, params)
            elif method == "session/status":
                return self._handle_session_status(req_id, params)
            elif method == "session/cancel":
                return self._handle_session_cancel(req_id, params)
            elif method == "ping":
                return {"jsonrpc": "2.0", "id": req_id, "result": {"pong": True}}
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not supported: '{method}'"},
                }
        except Exception as e:
            logger.exception("ACP processing error: %s", e)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"ACP execution error: {str(e)}"},
            }

    def _handle_initialize(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to client handshake."""
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": self.PROTOCOL_VERSION,
                "server": {
                    "name": "openclone-acp-adapter",
                    "version": "2.0.0",
                },
                "capabilities": {
                    "sessions": True,
                    "streaming": True,
                    "diffStreaming": True,
                    "toolConfirmation": True,
                    "governedExecution": True,
                },
            },
        }

    def _handle_session_create(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize a new ACP session."""
        ws_str = params.get("workspace_root")
        ws = Path(ws_str).resolve() if ws_str else self.workspace_root
        caps = params.get("capabilities", [])
        session_id = f"acp-{uuid.uuid4().hex[:12]}"
        session = ACPSession(session_id, ws, client_capabilities=caps)
        self.sessions[session_id] = session

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "session_id": session_id,
                "workspace_root": str(ws),
                "status": "READY",
            },
        }

    def _handle_session_prompt(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process an ACP user prompt through AutonomousExecutionEngine."""
        session_id = params.get("session_id")
        text = params.get("text", "")
        mode_str = params.get("mode", "Standard")

        if not text:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": "Missing 'text' in prompt request"},
            }

        session = self.sessions.get(session_id)
        if not session:
            # Auto-create fallback session if omitted
            session_id = f"acp-{uuid.uuid4().hex[:12]}"
            session = ACPSession(session_id, self.workspace_root)
            self.sessions[session_id] = session

        session.last_active = time.time()
        session.status = "RUNNING"

        mode_str = params.get("mode", "standard").lower()
        try:
            mode_enum = ExecutionMode(mode_str)
        except ValueError:
            mode_enum = ExecutionMode.FAST if "fast" in mode_str else ExecutionMode.STANDARD
        report = self.engine.run(text, mode=mode_enum)

        session.status = "IDLE"
        summary_md = report.to_markdown() if hasattr(report, "to_markdown") else str(report)
        clean_summary = redact_secrets(summary_md)

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "session_id": session_id,
                "request_id": report.request_id,
                "status": report.status,
                "summary": clean_summary,
                "tests_passed": report.tests_passed,
                "execution_duration_seconds": report.execution_duration_seconds,
                "artifacts_modified": [str(a) for a in (report.modified_files + report.created_files)],
            },
        }

    def _handle_session_status(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id")
        session = self.sessions.get(session_id)
        if not session:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Session not found: {session_id}"},
            }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "session_id": session.session_id,
                "workspace_root": str(session.workspace_root),
                "status": session.status,
                "created_at": session.created_at,
            },
        }

    def _handle_session_cancel(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id")
        if session_id in self.sessions:
            self.sessions[session_id].status = "CANCELLED"
            return {"jsonrpc": "2.0", "id": req_id, "result": {"cancelled": True}}
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32602, "message": f"Session not found: {session_id}"},
        }

    def run_stdio(self) -> None:
        """Run ACP stdio server loop."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Invalid JSON"}}
                sys.stdout.write(json.dumps(err) + "\n")
                sys.stdout.flush()
