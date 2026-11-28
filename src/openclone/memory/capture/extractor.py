"""
OpenClone Memory Capture Engine.
Extracts candidate memories from session logs, decisions, and completed tasks.
"""

from __future__ import annotations
import re
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus, MemoryAuthority, Classification, SourceRef
from openclone.memory.schema import MemorySchemaValidator


class MemoryCandidate:
    """Represents a potential memory extracted from an activity."""

    def __init__(
        self,
        title: str,
        statement: str,
        memory_type: MemoryType,
        source_uri: str,
        details: Optional[str] = None,
        authority: MemoryAuthority = MemoryAuthority.UNVERIFIED,
        confidence: float = 0.8
    ):
        self.title = title
        self.statement = statement
        self.memory_type = memory_type
        self.source_uri = source_uri
        self.details = details
        self.authority = authority
        self.confidence = confidence


class MemoryCaptureEngine:
    """
    Identifies durable facts, approved architecture decisions, and session milestones.
    Filters out secrets and ephemeral chat noise.
    """

    SECRET_PATTERNS = [
        re.compile(r"(?i)(api[_-]?key|secret|password|bearer|auth[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{8,}['\"]"),
        re.compile(r"(?i)-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----"),
        re.compile(r"(?i)ghp_[A-Za-z0-9]{36}"),
        re.compile(r"(?i)sk-[A-Za-z0-9]{32,}"),
    ]

    DECISION_PATTERNS = [
        re.compile(r"(?i)(we have decided to|approved decision|decided that|architecture decision:)\s*(.+)", re.MULTILINE),
        re.compile(r"(?i)ADR-\d+:\s*(.+)", re.MULTILINE),
    ]

    LESSON_PATTERNS = [
        re.compile(r"(?i)(key takeaway|lesson learned|root cause was|bug fix resolution:)\s*(.+)", re.MULTILINE),
    ]

    @classmethod
    def contains_secrets(cls, text: str) -> bool:
        for pat in cls.SECRET_PATTERNS:
            if pat.search(text):
                return True
        return False

    @classmethod
    def extract_from_text(cls, text: str, source_uri: str) -> List[MemoryCandidate]:
        if cls.contains_secrets(text):
            # Reject content with secrets
            return []

        candidates: List[MemoryCandidate] = []

        # Extract Decisions
        for pat in cls.DECISION_PATTERNS:
            for match in pat.finditer(text):
                statement = match.group(0).strip()
                title = statement[:60] + ("..." if len(statement) > 60 else "")
                candidates.append(MemoryCandidate(
                    title=title,
                    statement=statement,
                    memory_type=MemoryType.DECISION,
                    source_uri=source_uri,
                    authority=MemoryAuthority.VERIFIED,
                    confidence=0.9
                ))

        # Extract Lessons
        for pat in cls.LESSON_PATTERNS:
            for match in pat.finditer(text):
                statement = match.group(0).strip()
                title = statement[:60] + ("..." if len(statement) > 60 else "")
                candidates.append(MemoryCandidate(
                    title=title,
                    statement=statement,
                    memory_type=MemoryType.LESSON,
                    source_uri=source_uri,
                    authority=MemoryAuthority.VERIFIED,
                    confidence=0.85
                ))

        return candidates

    @classmethod
    def create_record(
        cls,
        candidate: MemoryCandidate,
        scope: MemoryScope,
        memory_id: Optional[str] = None
    ) -> MemoryRecord:
        rec_id = memory_id or f"MEM-{uuid.uuid4().hex[:8].upper()}"
        return MemoryRecord(
            id=rec_id,
            title=candidate.title,
            statement=candidate.statement,
            details=candidate.details,
            memory_type=candidate.memory_type,
            scope=scope,
            authority=candidate.authority,
            confidence=candidate.confidence,
            source_refs=[SourceRef(uri=candidate.source_uri, source_type="session_log", revision_or_date=datetime.now(timezone.utc).date().isoformat())],
            recorded_at=datetime.now(timezone.utc).isoformat(),
        )
