"""
OpenClone SQLite & FTS5 Persistent Storage Adapter.
"""

from __future__ import annotations
import json
import re
import sqlite3
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryStatus
from openclone.memory.schema import MemorySchemaValidator, SchemaValidationError
from openclone.memory.storage.base import MemoryStorageAdapter


class SQLiteMemoryAdapter(MemoryStorageAdapter):
    """
    Transactional, ACID-compliant local storage engine for memory records.
    Features:
    - WAL journal mode for high concurrency
    - Full-text search (FTS5) for rapid lexical queries
    - Project, workspace, and tenant scope isolation
    - Strict atomic writes and rollback protection
    """

    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(str(self.db_path), timeout=30.0)
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA foreign_keys = ON")
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_records (
                    id TEXT PRIMARY KEY,
                    schema_version TEXT NOT NULL,
                    title TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    project_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    user_id TEXT,
                    organization_id TEXT,
                    agent_id TEXT,
                    statement TEXT NOT NULL,
                    details TEXT,
                    classification TEXT NOT NULL,
                    status TEXT NOT NULL,
                    authority TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source_refs TEXT NOT NULL,
                    observed_at TEXT,
                    recorded_at TEXT NOT NULL,
                    verified_at TEXT,
                    review_due_at TEXT,
                    expires_at TEXT,
                    approved_by TEXT,
                    supersedes TEXT NOT NULL,
                    superseded_by TEXT NOT NULL,
                    related_records TEXT NOT NULL,
                    limitations TEXT NOT NULL,
                    created_by TEXT,
                    updated_at TEXT,
                    raw_payload TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_scope ON memory_records(project_id, workspace_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_type_status ON memory_records(memory_type, status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_authority ON memory_records(authority)")

            # Check if FTS5 is available
            try:
                conn.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                        id UNINDEXED,
                        title,
                        statement,
                        details,
                        tokenize = 'porter unicode61'
                    )
                """)
                self._has_fts = True
            except sqlite3.OperationalError:
                self._has_fts = False

    def create(self, record: MemoryRecord) -> MemoryRecord:
        valid, errors = MemorySchemaValidator.validate_record(record)
        if not valid:
            raise SchemaValidationError(f"Cannot persist invalid record: {'; '.join(errors)}")

        conn = self._get_conn()
        payload = json.dumps(record.to_dict())
        with conn:
            conn.execute("""
                INSERT INTO memory_records (
                    id, schema_version, title, memory_type, project_id, workspace_id,
                    user_id, organization_id, agent_id, statement, details,
                    classification, status, authority, confidence, source_refs,
                    observed_at, recorded_at, verified_at, review_due_at, expires_at,
                    approved_by, supersedes, superseded_by, related_records, limitations,
                    created_by, updated_at, raw_payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.id, record.schema_version, record.title, record.memory_type.value,
                record.scope.project_id, record.scope.workspace_id,
                record.scope.user_id, record.scope.organization_id, record.scope.agent_id,
                record.statement, record.details, record.classification.value,
                record.status.value, record.authority.value, record.confidence,
                json.dumps([s.to_dict() if hasattr(s, "to_dict") else s for s in record.source_refs]),
                record.observed_at, record.recorded_at, record.verified_at,
                record.review_due_at, record.expires_at, record.approved_by,
                json.dumps(record.supersedes), json.dumps(record.superseded_by),
                json.dumps(record.related_records), json.dumps(record.limitations),
                record.created_by, record.updated_at, payload
            ))
            if getattr(self, "_has_fts", False):
                conn.execute(
                    "INSERT INTO memory_fts(id, title, statement, details) VALUES (?, ?, ?, ?)",
                    (record.id, record.title, record.statement, record.details or "")
                )
        return record

    def read(self, memory_id: str, scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        conn = self._get_conn()
        if scope:
            cur = conn.execute(
                "SELECT raw_payload FROM memory_records WHERE id = ? AND project_id = ? AND workspace_id = ?",
                (memory_id, scope.project_id, scope.workspace_id)
            )
        else:
            cur = conn.execute("SELECT raw_payload FROM memory_records WHERE id = ?", (memory_id,))
        row = cur.fetchone()
        if not row:
            return None
        data = json.loads(row["raw_payload"])
        return MemoryRecord.from_dict(data)

    def update(self, memory_id: str, changes: Dict[str, Any], scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        existing = self.read(memory_id, scope=scope)
        if not existing:
            return None

        data = existing.to_dict()
        for k, v in changes.items():
            if k != "id":  # Do not mutate immutable ID
                data[k] = v

        updated_record = MemoryRecord.from_dict(data)
        valid, errors = MemorySchemaValidator.validate_record(updated_record)
        if not valid:
            raise SchemaValidationError(f"Invalid record update: {'; '.join(errors)}")

        conn = self._get_conn()
        payload = json.dumps(updated_record.to_dict())
        with conn:
            conn.execute("""
                UPDATE memory_records SET
                    schema_version = ?, title = ?, memory_type = ?, project_id = ?, workspace_id = ?,
                    user_id = ?, organization_id = ?, agent_id = ?, statement = ?, details = ?,
                    classification = ?, status = ?, authority = ?, confidence = ?, source_refs = ?,
                    observed_at = ?, recorded_at = ?, verified_at = ?, review_due_at = ?, expires_at = ?,
                    approved_by = ?, supersedes = ?, superseded_by = ?, related_records = ?, limitations = ?,
                    created_by = ?, updated_at = ?, raw_payload = ?
                WHERE id = ?
            """, (
                updated_record.schema_version, updated_record.title, updated_record.memory_type.value,
                updated_record.scope.project_id, updated_record.scope.workspace_id,
                updated_record.scope.user_id, updated_record.scope.organization_id, updated_record.scope.agent_id,
                updated_record.statement, updated_record.details, updated_record.classification.value,
                updated_record.status.value, updated_record.authority.value, updated_record.confidence,
                json.dumps([s.to_dict() if hasattr(s, "to_dict") else s for s in updated_record.source_refs]),
                updated_record.observed_at, updated_record.recorded_at, updated_record.verified_at,
                updated_record.review_due_at, updated_record.expires_at, updated_record.approved_by,
                json.dumps(updated_record.supersedes), json.dumps(updated_record.superseded_by),
                json.dumps(updated_record.related_records), json.dumps(updated_record.limitations),
                updated_record.created_by, updated_record.updated_at, payload, memory_id
            ))
            if getattr(self, "_has_fts", False):
                conn.execute("DELETE FROM memory_fts WHERE id = ?", (memory_id,))
                conn.execute(
                    "INSERT INTO memory_fts(id, title, statement, details) VALUES (?, ?, ?, ?)",
                    (updated_record.id, updated_record.title, updated_record.statement, updated_record.details or "")
                )
        return updated_record

    def delete(self, memory_id: str, scope: Optional[MemoryScope] = None, hard: bool = False) -> bool:
        record = self.read(memory_id, scope=scope)
        if not record:
            return False

        conn = self._get_conn()
        with conn:
            if hard:
                conn.execute("DELETE FROM memory_records WHERE id = ?", (memory_id,))
                if getattr(self, "_has_fts", False):
                    conn.execute("DELETE FROM memory_fts WHERE id = ?", (memory_id,))
            else:
                # Soft delete -> mark ARCHIVED
                self.update(memory_id, {"status": MemoryStatus.ARCHIVED.value}, scope=scope)
                if getattr(self, "_has_fts", False):
                    # Remove from search index so archived records do not appear in active search
                    conn.execute("DELETE FROM memory_fts WHERE id = ?", (memory_id,))
        return True

    def list(self, scope: Optional[MemoryScope] = None, memory_type: Optional[str] = None, status: Optional[str] = None, limit: int = 100) -> List[MemoryRecord]:
        conn = self._get_conn()
        query = "SELECT raw_payload FROM memory_records WHERE 1=1"
        params: List[Any] = []

        if scope:
            query += " AND project_id = ? AND workspace_id = ?"
            params.extend([scope.project_id, scope.workspace_id])
        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        else:
            # Default exclude ARCHIVED unless explicitly requested
            query += " AND status != 'ARCHIVED'"

        query += " ORDER BY recorded_at DESC LIMIT ?"
        params.append(limit)

        cur = conn.execute(query, params)
        records = []
        for row in cur.fetchall():
            records.append(MemoryRecord.from_dict(json.loads(row["raw_payload"])))
        return records

    def search(self, query: str, scope: Optional[MemoryScope] = None, limit: int = 20) -> List[MemoryRecord]:
        conn = self._get_conn()
        clean_q = query.strip()
        if not clean_q:
            return self.list(scope=scope, limit=limit)

        records: List[MemoryRecord] = []
        # Try FTS5 search
        if getattr(self, "_has_fts", False):
            # Sanitize query for FTS5
            fts_query = re.sub(r"[^\w\s]", "", clean_q)
            fts_terms = " OR ".join([f"{t}*" for t in fts_query.split() if t])
            if fts_terms:
                try:
                    sql = """
                        SELECT r.raw_payload FROM memory_records r
                        JOIN memory_fts f ON r.id = f.id
                        WHERE memory_fts MATCH ?
                    """
                    params: List[Any] = [fts_terms]
                    if scope:
                        sql += " AND r.project_id = ? AND r.workspace_id = ?"
                        params.extend([scope.project_id, scope.workspace_id])
                    sql += " AND r.status != 'ARCHIVED' LIMIT ?"
                    params.append(limit)

                    cur = conn.execute(sql, params)
                    for row in cur.fetchall():
                        records.append(MemoryRecord.from_dict(json.loads(row["raw_payload"])))
                    if records:
                        return records
                except sqlite3.OperationalError:
                    pass

        # Fallback to standard LIKE search
        like_term = f"%{clean_q}%"
        sql = """
            SELECT raw_payload FROM memory_records
            WHERE (title LIKE ? OR statement LIKE ? OR details LIKE ?)
        """
        params = [like_term, like_term, like_term]
        if scope:
            sql += " AND project_id = ? AND workspace_id = ?"
            params.extend([scope.project_id, scope.workspace_id])
        sql += " AND status != 'ARCHIVED' ORDER BY recorded_at DESC LIMIT ?"
        params.append(limit)

        cur = conn.execute(sql, params)
        for row in cur.fetchall():
            records.append(MemoryRecord.from_dict(json.loads(row["raw_payload"])))
        return records

    def health_check(self) -> Dict[str, Any]:
        conn = self._get_conn()
        count_cur = conn.execute("SELECT count(*) as cnt FROM memory_records")
        total_records = count_cur.fetchone()["cnt"]

        return {
            "status": "HEALTHY",
            "db_path": str(self.db_path),
            "total_records": total_records,
            "has_fts5": getattr(self, "_has_fts", False),
            "journal_mode": "WAL",
        }

    def close(self) -> None:
        if hasattr(self._local, "conn") and self._local.conn is not None:
            self._local.conn.close()
            self._local.conn = None
