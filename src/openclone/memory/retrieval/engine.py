"""
OpenClone Memory Intelligence Retrieval Engine & Multi-Attribute Ranking Model.
"""

from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryStatus, MemoryAuthority
from openclone.memory.storage.base import MemoryStorageAdapter


class MemoryRetrievalResult:
    """Wrapper for a retrieved memory record with ranking explanation."""

    def __init__(self, record: MemoryRecord, score: float, reasons: List[str]):
        self.record = record
        self.score = score
        self.reasons = reasons

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record": self.record.to_dict(),
            "score": round(self.score, 4),
            "reasons": self.reasons,
        }


class MemoryRetrievalEngine:
    """
    Intelligent Memory Retrieval Engine.
    Executes multi-attribute ranking:
    - Textual relevance (lexical matching)
    - Authority weight (human_confirmed: 1.5, verified: 1.2, unverified: 0.8)
    - Freshness decay (penalizes stale/old records)
    - Status weighting (CURRENT: 1.0, REVIEW_DUE: 0.7, STALE/DISPUTED: 0.2, SUPERSEDED/ARCHIVED: 0.0)
    - Scope strictness (enforced at query boundary)
    """

    AUTHORITY_WEIGHTS = {
        MemoryAuthority.HUMAN_CONFIRMED: 1.5,
        MemoryAuthority.VERIFIED: 1.2,
        MemoryAuthority.UNVERIFIED: 0.8,
    }

    STATUS_WEIGHTS = {
        MemoryStatus.CURRENT: 1.0,
        MemoryStatus.REVIEW_DUE: 0.7,
        MemoryStatus.STALE: 0.2,
        MemoryStatus.DISPUTED: 0.2,
        MemoryStatus.UNVERIFIED: 0.5,
        MemoryStatus.SUPERSEDED: 0.0,
        MemoryStatus.ARCHIVED: 0.0,
    }

    def __init__(self, storage: MemoryStorageAdapter):
        self.storage = storage

    def _calculate_freshness(self, record: MemoryRecord) -> float:
        """Calculate exponential time-decay freshness factor in [0.1, 1.0]."""
        if not record.recorded_at:
            return 0.5
        try:
            # Parse ISO date
            rec_date = datetime.fromisoformat(record.recorded_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            delta_days = max(0.0, (now - rec_date).total_seconds() / 86400.0)
            # Half-life of 90 days for general memories, 180 for decisions
            half_life = 180.0 if record.memory_type.value == "decision" else 90.0
            return math.exp(-0.693 * (delta_days / half_life))
        except Exception:
            return 0.8

    def _score_record(self, record: MemoryRecord, query_terms: List[str]) -> Tuple[float, List[str]]:
        reasons = []

        # Status check
        s_weight = self.STATUS_WEIGHTS.get(record.status, 0.5)
        if s_weight == 0.0:
            return 0.0, [f"Status {record.status.value} suppressed from active retrieval"]

        # Text relevance
        term_matches = 0
        haystack = f"{record.title} {record.statement} {record.details or ''}".lower()
        for term in query_terms:
            if term in haystack:
                term_matches += 1
        base_relevance = (term_matches / len(query_terms)) if query_terms else 1.0
        reasons.append(f"Base relevance: {base_relevance:.2f}")

        # Authority weight
        auth_weight = self.AUTHORITY_WEIGHTS.get(record.authority, 1.0)
        reasons.append(f"Authority ({record.authority.value}): x{auth_weight:.2f}")

        # Freshness
        freshness = self._calculate_freshness(record)
        reasons.append(f"Freshness decay: x{freshness:.2f}")

        # Confidence
        conf = record.confidence
        reasons.append(f"Confidence: x{conf:.2f}")

        total_score = base_relevance * auth_weight * s_weight * freshness * conf
        return total_score, reasons

    def retrieve(
        self,
        query: str,
        scope: MemoryScope,
        memory_type: Optional[str] = None,
        min_score: float = 0.1,
        limit: int = 10,
        include_superseded: bool = False
    ) -> List[MemoryRetrievalResult]:
        """
        Execute scoped search and return scored, ranked memory records.
        """
        # Scope boundary check
        if not scope or not scope.project_id or not scope.workspace_id:
            raise ValueError("Scope with non-empty project_id and workspace_id is strictly required.")

        # Candidate selection from storage
        candidates = self.storage.search(query, scope=scope, limit=limit * 3)
        if not candidates and not query.strip():
            candidates = self.storage.list(scope=scope, memory_type=memory_type, limit=limit * 3)

        query_terms = [t.lower() for t in query.split() if t]
        scored_results: List[MemoryRetrievalResult] = []

        for rec in candidates:
            # Memory type filter
            if memory_type and rec.memory_type.value != memory_type:
                continue

            # Superseded filter
            if not include_superseded and rec.status == MemoryStatus.SUPERSEDED:
                continue

            score, reasons = self._score_record(rec, query_terms)
            if score >= min_score:
                scored_results.append(MemoryRetrievalResult(record=rec, score=score, reasons=reasons))

        # Sort descending by score
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_by_id(self, memory_id: str, scope: MemoryScope) -> Optional[MemoryRecord]:
        """Retrieve memory by exact ID, strictly adhering to scope boundary."""
        if not scope or not scope.project_id:
            raise ValueError("Scope is strictly required to get memory by ID.")
        return self.storage.read(memory_id, scope=scope)
