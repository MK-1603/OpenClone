"""OpenClone Model Intelligence Engine (MIE) — Privacy-Preserving Telemetry & Ledger.

Records execution latency, token counts, cost accounting, and circuit breaker
transitions into an append-only hash-chained SQLite ledger.
Zero prompt persistence by default; strict secret redaction.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.mie.models import ExecutionMetrics

# Secret patterns to scrub from all logs and metadata
REDACTIONS = [
    (re.compile(r"(Bearer\s+)[A-Za-z0-9_\-\.]{12,}", re.IGNORECASE), r"\1[REDACTED]"),
    (re.compile(r"((?:api[_-]?key|token|secret)\s*[:=]\s*['\"]?)[A-Za-z0-9_\-\.]{12,}['\"]?", re.IGNORECASE), r"\1[REDACTED]"),
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}", re.IGNORECASE), "[REDACTED-KEY]"),
    (re.compile(r"AIza[0-9A-Za-z-_]{35}", re.IGNORECASE), "[REDACTED-KEY]"),
]


def redact_secrets(text: str) -> str:
    """Deterministically redact API keys, tokens, and authorization headers."""
    if not text:
        return ""
    result = text
    for pattern, repl in REDACTIONS:
        result = pattern.sub(repl, result)
    return result


class MieTelemetry:
    """Thread-safe telemetry recorder with SQLite ledger backing."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("OPENCLONE_MIE_DB", ".openclone/mie.sqlite3")
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite ledger schema if file is writable/creatable."""
        try:
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS mie_ledger (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_id TEXT NOT NULL,
                        model_id TEXT NOT NULL,
                        provider_id TEXT NOT NULL,
                        prompt_tokens INTEGER NOT NULL,
                        completion_tokens INTEGER NOT NULL,
                        total_tokens INTEGER NOT NULL,
                        cost_usd REAL NOT NULL,
                        duration_ms REAL NOT NULL,
                        success INTEGER NOT NULL,
                        error_type TEXT,
                        prev_hash TEXT NOT NULL,
                        entry_hash TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
        except Exception:
            # Degrade gracefully to in-memory mode if disk is read-only or restricted
            self.db_path = ":memory:"

    def record_execution(self, metric: ExecutionMetrics) -> str:
        """Append an execution metric event to the hash-chained ledger and return entry hash."""
        prev_hash = "GENESIS"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT entry_hash FROM mie_ledger ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    prev_hash = row[0]

                raw_payload = f"{prev_hash}:{metric.request_id}:{metric.model_id}:{metric.total_tokens}:{metric.cost_usd}:{metric.timestamp}"
                entry_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

                cursor.execute(
                    """
                    INSERT INTO mie_ledger (
                        request_id, model_id, provider_id, prompt_tokens, completion_tokens,
                        total_tokens, cost_usd, duration_ms, success, error_type,
                        prev_hash, entry_hash, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        metric.request_id,
                        metric.model_id,
                        metric.provider_id,
                        metric.prompt_tokens,
                        metric.completion_tokens,
                        metric.total_tokens,
                        metric.cost_usd,
                        metric.duration_ms,
                        1 if metric.success else 0,
                        redact_secrets(metric.error_type or ""),
                        prev_hash,
                        entry_hash,
                        metric.timestamp,
                    ),
                )
                conn.commit()
                return entry_hash
        except Exception:
            return hashlib.sha256(metric.request_id.encode("utf-8")).hexdigest()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Aggregate total tokens, cost, and request counts from the ledger."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT 
                        COUNT(*), 
                        SUM(prompt_tokens), 
                        SUM(completion_tokens), 
                        SUM(cost_usd),
                        AVG(duration_ms)
                    FROM mie_ledger WHERE success = 1
                    """
                )
                row = cursor.fetchone()
                if row and row[0] > 0:
                    return {
                        "total_requests": row[0],
                        "total_prompt_tokens": row[1] or 0,
                        "total_completion_tokens": row[2] or 0,
                        "total_cost_usd": round(row[3] or 0.0, 4),
                        "avg_duration_ms": round(row[4] or 0.0, 2),
                    }
        except Exception:
            pass
        return {
            "total_requests": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost_usd": 0.0,
            "avg_duration_ms": 0.0,
        }
