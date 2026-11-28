"""
OpenClone Memory Intelligence System Unified Manager & Entrypoint.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict, Any, List
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus
from openclone.memory.storage.sqlite_adapter import SQLiteMemoryAdapter
from openclone.memory.storage.markdown_adapter import MarkdownVaultAdapter
from openclone.memory.retrieval.engine import MemoryRetrievalEngine
from openclone.memory.capture.extractor import MemoryCaptureEngine
from openclone.memory.consolidation.engine import MemoryConsolidationEngine
from openclone.memory.intelligence.engine import MemoryIntelligenceEngine
from openclone.memory.context.builder import MemoryContextBuilder
from openclone.memory.security.guardrails import MemorySecurityGuard


class MemoryManager:
    """
    Unified façade coordinating Storage, Retrieval, Capture, Consolidation,
    Intelligence, and Context Building for OpenClone.
    """

    def __init__(self, workspace_path: Path | str, db_name: str = "memory.sqlite3", vault_name: str = "memory/vault"):
        self.workspace = Path(workspace_path).resolve()
        state_dir = self.workspace / ".openclone"
        state_dir.mkdir(parents=True, exist_ok=True)

        self.sqlite_adapter = SQLiteMemoryAdapter(state_dir / db_name)
        self.markdown_adapter = MarkdownVaultAdapter(self.workspace / vault_name)

        self.retrieval_engine = MemoryRetrievalEngine(storage=self.sqlite_adapter)
        self.consolidation_engine = MemoryConsolidationEngine(storage=self.sqlite_adapter)
        self.intelligence_engine = MemoryIntelligenceEngine(storage=self.sqlite_adapter)
        self.context_builder = MemoryContextBuilder(retrieval_engine=self.retrieval_engine)

    def store_record(self, record: MemoryRecord, sync_markdown: bool = True) -> MemoryRecord:
        """Audit and store record in SQLite, with optional Markdown vault sync."""
        valid, violations = MemorySecurityGuard.audit_record_for_persistence(record)
        if not valid:
            raise PermissionError(f"Security audit failed: {'; '.join(violations)}")

        stored = self.sqlite_adapter.create(record)
        if sync_markdown:
            try:
                self.markdown_adapter.create(record)
            except Exception:
                pass  # Primary store is SQLite
        return stored

    def close(self) -> None:
        self.sqlite_adapter.close()
        self.markdown_adapter.close()
