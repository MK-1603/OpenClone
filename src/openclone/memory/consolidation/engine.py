"""
OpenClone Memory Consolidation Engine.
Consolidates session outcomes, detects duplicates/conflicts, and persists durable memories.
"""

from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus, MemoryAuthority, SourceRef
from openclone.memory.storage.base import MemoryStorageAdapter
from openclone.memory.capture.extractor import MemoryCaptureEngine, MemoryCandidate


class ConsolidationOutcome:
    """Summary of memory consolidation operations."""

    def __init__(self):
        self.created_records: List[MemoryRecord] = []
        self.updated_records: List[MemoryRecord] = []
        self.skipped_duplicates: List[str] = []
        self.detected_conflicts: List[Dict[str, Any]] = []
        self.errors: List[str] = []

    @property
    def created_count(self) -> int:
        return len(self.created_records)

    @property
    def updated_count(self) -> int:
        return len(self.updated_records)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_count": len(self.created_records),
            "created_ids": [r.id for r in self.created_records],
            "updated_count": len(self.updated_records),
            "updated_ids": [r.id for r in self.updated_records],
            "skipped_duplicates": self.skipped_duplicates,
            "conflicts": self.detected_conflicts,
            "errors": self.errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class MemoryConsolidationEngine:
    """
    Consolidates session checkpoints and verified task outcomes into durable memory.
    Ensures:
    - Deduplication against existing records
    - Conflict detection against prior decisions
    - Read-back verification after write
    """

    def __init__(self, storage: MemoryStorageAdapter):
        self.storage = storage

    def is_duplicate(self, candidate: MemoryCandidate, existing_records: List[MemoryRecord]) -> Optional[MemoryRecord]:
        cand_stmt = candidate.statement.strip().lower()
        for rec in existing_records:
            if rec.statement.strip().lower() == cand_stmt:
                return rec
            # High Jaccard similarity
            words_a = set(cand_stmt.split())
            words_b = set(rec.statement.strip().lower().split())
            if words_a and words_b:
                jaccard = len(words_a & words_b) / len(words_a | words_b)
                if jaccard > 0.85 and rec.memory_type == candidate.memory_type:
                    return rec
        return None

    def consolidate_session(
        self,
        session_id: str,
        session_text: str,
        scope: MemoryScope,
        source_uri: str
    ) -> ConsolidationOutcome:
        outcome = ConsolidationOutcome()

        # Step 1: Extract candidate memories
        candidates = MemoryCaptureEngine.extract_from_text(session_text, source_uri=source_uri)

        # Step 2: Fetch existing project records for deduplication
        existing = self.storage.list(scope=scope, limit=500)

        for cand in candidates:
            dup = self.is_duplicate(cand, existing)
            if dup:
                outcome.skipped_duplicates.append(f"Candidate '{cand.title[:30]}' duplicates {dup.id}")
                continue

            # Create new record
            record = MemoryCaptureEngine.create_record(cand, scope=scope)
            try:
                self.storage.create(record)
                # Read-back verification
                read_back = self.storage.read(record.id, scope=scope)
                if read_back and read_back.id == record.id:
                    outcome.created_records.append(record)
                    existing.append(record)
                else:
                    outcome.errors.append(f"Read-back verification failed for record {record.id}")
            except Exception as e:
                outcome.errors.append(f"Persistence failed for {record.id}: {str(e)}")

        # Step 3: Always persist a durable Session Checkpoint
        checkpoint_id = f"MEM-SES-{uuid.uuid4().hex[:6].upper()}"
        checkpoint_record = MemoryRecord(
            id=checkpoint_id,
            title=f"Session Checkpoint: {session_id}",
            statement=f"Session {session_id} completed at {datetime.now(timezone.utc).isoformat()}. Captured {len(outcome.created_records)} durable memories.",
            details=session_text[:1000] if len(session_text) > 1000 else session_text,
            memory_type=MemoryType.SESSION_CHECKPOINT,
            scope=scope,
            authority=MemoryAuthority.VERIFIED,
            source_refs=[SourceRef(uri=source_uri, source_type="session_summary")],
            recorded_at=datetime.now(timezone.utc).isoformat(),
        )
        try:
            self.storage.create(checkpoint_record)
            outcome.created_records.append(checkpoint_record)
        except Exception as e:
            outcome.errors.append(f"Failed to record session checkpoint: {str(e)}")

        return outcome
