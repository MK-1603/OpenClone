"""OpenClone Security Monitoring & Tamper-Evident Audit Ledger.

Records structured security events, authorization failures, and firewall blocks
into an append-only, cryptographically hash-chained audit ledger.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.mie.telemetry import redact_secrets


class SecurityLedgerTamperError(Exception):
    """Raised when an audit ledger hash-chain integrity verification fails."""
    pass


class SecurityMonitor:
    """Security monitoring engine with cryptographically verifiable hash-chained ledger."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        self._shared_conn = None
        if self.db_path == ":memory:":
            self._shared_conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self._shared_conn is not None:
            return self._shared_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                actor TEXT NOT NULL,
                details TEXT NOT NULL,
                prev_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL
            )
        """)
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    def _get_last_hash(self, conn: sqlite3.Connection) -> str:
        cursor = conn.execute("SELECT entry_hash FROM security_events ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else "GENESIS_SECURITY_BLOCK"

    def record_event(
        self,
        event_type: str,
        severity: str,
        actor: str = "system",
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record a structured security event into the hash-chained ledger."""
        now_str = datetime.now(timezone.utc).isoformat()
        evt_id = str(uuid.uuid4())

        # Redact any accidental tokens from details
        raw_details_json = json.dumps(details or {}, sort_keys=True)
        clean_details_json = redact_secrets(raw_details_json)

        conn = self._get_connection()
        prev_hash = self._get_last_hash(conn)

        # Compute tamper-evident hash binding
        payload = {
            "event_id": evt_id,
            "timestamp": now_str,
            "event_type": event_type,
            "severity": severity,
            "actor": actor,
            "details": clean_details_json,
            "prev_hash": prev_hash,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        entry_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        conn.execute(
            """
            INSERT INTO security_events (event_id, timestamp, event_type, severity, actor, details, prev_hash, entry_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (evt_id, now_str, event_type, severity, actor, clean_details_json, prev_hash, entry_hash),
        )
        conn.commit()
        if self._shared_conn is None:
            conn.close()

        return entry_hash

    def verify_ledger_integrity(self) -> bool:
        """Verify the cryptographic hash-chain across all recorded security events."""
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT event_id, timestamp, event_type, severity, actor, details, prev_hash, entry_hash "
            "FROM security_events ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        if self._shared_conn is None:
            conn.close()

        expected_prev = "GENESIS_SECURITY_BLOCK"
        for row in rows:
            evt_id, ts, ev_type, sev, actor, details, prev_h, entry_h = row
            if prev_h != expected_prev:
                raise SecurityLedgerTamperError(
                    f"Audit ledger integrity failure at event {evt_id}: prev_hash mismatch."
                )

            payload = {
                "event_id": evt_id,
                "timestamp": ts,
                "event_type": ev_type,
                "severity": sev,
                "actor": actor,
                "details": details,
                "prev_hash": prev_h,
            }
            canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
            computed_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

            if computed_hash != entry_h:
                raise SecurityLedgerTamperError(
                    f"Audit ledger integrity failure at event {evt_id}: entry_hash tampering detected."
                )
            expected_prev = entry_h

        return True

    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent security events."""
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT event_id, timestamp, event_type, severity, actor, details, entry_hash "
            "FROM security_events ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        if self._shared_conn is None:
            conn.close()

        return [
            {
                "event_id": r[0],
                "timestamp": r[1],
                "event_type": r[2],
                "severity": r[3],
                "actor": r[4],
                "details": json.loads(r[5]),
                "entry_hash": r[6],
            }
            for r in rows
        ]
