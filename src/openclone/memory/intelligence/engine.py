"""
OpenClone Memory Intelligence Engine.
Detects contradictions, manages supersession, and traces project evolution.
"""

from __future__ import annotations
import re
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus
from openclone.memory.storage.base import MemoryStorageAdapter


class MemoryConflict:
    """Represents an identified contradiction between two memory records."""

    def __init__(self, record_a: MemoryRecord, record_b: MemoryRecord, topic: str, reason: str):
        self.record_a_id = record_a.id
        self.record_b_id = record_b.id
        self.topic = topic
        self.reason = reason
        self.detected_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_a_id": self.record_a_id,
            "record_b_id": self.record_b_id,
            "topic": self.topic,
            "reason": self.reason,
            "detected_at": self.detected_at,
        }


class MemoryIntelligenceEngine:
    """
    Analyzes semantic relationships, contradictions, supersessions, and architecture evolution.
    """

    TOPIC_EXTRACTORS = {
        "database": re.compile(r"(?i)\b(database|postgres|postgresql|sqlite|mongodb|mysql|redis)\b"),
        "language": re.compile(r"(?i)\b(python|typescript|javascript|golang|go|rust|java)\b"),
        "frontend": re.compile(r"(?i)\b(react|next\.js|nextjs|vue|nuxt|tailwind|vite)\b"),
        "backend": re.compile(r"(?i)\b(fastapi|django|express|nestjs|gin|echo|spring)\b"),
        "architecture": re.compile(r"(?i)\b(monolith|modular monolith|microservices|serverless|event-driven)\b"),
    }

    def __init__(self, storage: MemoryStorageAdapter):
        self.storage = storage

    def detect_conflicts(self, scope: MemoryScope) -> List[MemoryConflict]:
        """Scan active decisions and facts within a scope to detect contradictions."""
        records = self.storage.list(scope=scope, status=MemoryStatus.CURRENT.value, limit=500)
        conflicts: List[MemoryConflict] = []

        # Group records by topic
        topic_map: Dict[str, List[MemoryRecord]] = {}
        for rec in records:
            text = f"{rec.title} {rec.statement}".lower()
            for topic, pat in self.TOPIC_EXTRACTORS.items():
                if pat.search(text):
                    topic_map.setdefault(topic, []).append(rec)

        for topic, rec_list in topic_map.items():
            if len(rec_list) < 2:
                continue
            for i in range(len(rec_list)):
                for j in range(i + 1, len(rec_list)):
                    r1 = rec_list[i]
                    r2 = rec_list[j]
                    # If both are decisions or both are facts
                    if r1.memory_type == r2.memory_type == MemoryType.DECISION:
                        # Extract matches
                        m1 = set(self.TOPIC_EXTRACTORS[topic].findall(r1.statement.lower()))
                        m2 = set(self.TOPIC_EXTRACTORS[topic].findall(r2.statement.lower()))
                        if m1 and m2 and m1 != m2 and not (r1.id in r2.supersedes or r2.id in r1.supersedes):
                            conflicts.append(MemoryConflict(
                                record_a=r1,
                                record_b=r2,
                                topic=topic,
                                reason=f"Conflicting decisions on {topic}: '{r1.statement[:40]}' ({m1}) vs '{r2.statement[:40]}' ({m2})"
                            ))

        return conflicts

    def supersede(self, old_memory_id: str, new_record: MemoryRecord, scope: MemoryScope) -> Tuple[MemoryRecord, MemoryRecord]:
        """
        Supersede an existing memory record with a new approved decision/fact.
        Ensures bidirectional linkage: old.superseded_by contains new.id, new.supersedes contains old.id.
        """
        old_record = self.storage.read(old_memory_id, scope=scope)
        if not old_record:
            raise ValueError(f"Old memory record {old_memory_id} not found in scope.")

        # Update old record
        superseded_by = list(old_record.superseded_by)
        if new_record.id not in superseded_by:
            superseded_by.append(new_record.id)

        self.storage.update(old_memory_id, {
            "status": MemoryStatus.SUPERSEDED.value,
            "superseded_by": superseded_by,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }, scope=scope)
        updated_old = self.storage.read(old_memory_id, scope=scope)

        # Update new record's supersedes list
        if old_memory_id not in new_record.supersedes:
            new_record.supersedes.append(old_memory_id)

        # Persist new record if not already stored
        existing_new = self.storage.read(new_record.id, scope=scope)
        if existing_new:
            self.storage.update(new_record.id, {
                "supersedes": new_record.supersedes,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }, scope=scope)
        else:
            self.storage.create(new_record)

        updated_new = self.storage.read(new_record.id, scope=scope)
        return updated_old, updated_new

    def get_project_evolution(self, scope: MemoryScope) -> Dict[str, Any]:
        """
        Trace the timeline of decisions, supersessions, and milestones for a project.
        """
        records = self.storage.list(scope=scope, limit=500)
        # Sort chronologically
        records.sort(key=lambda r: r.recorded_at or "")

        decisions = [r.to_dict() for r in records if r.memory_type == MemoryType.DECISION]
        superseded = [r.to_dict() for r in records if r.status == MemoryStatus.SUPERSEDED]
        checkpoints = [r.to_dict() for r in records if r.memory_type == MemoryType.SESSION_CHECKPOINT]

        return {
            "project_id": scope.project_id,
            "total_records": len(records),
            "timeline": [
                {
                    "id": r.id,
                    "type": r.memory_type.value,
                    "title": r.title,
                    "recorded_at": r.recorded_at,
                    "status": r.status.value,
                    "supersedes": r.supersedes,
                }
                for r in records
            ],
            "active_decisions_count": len([d for d in decisions if d["status"] == MemoryStatus.CURRENT.value]),
            "superseded_decisions_count": len(superseded),
            "session_checkpoints_count": len(checkpoints),
        }
