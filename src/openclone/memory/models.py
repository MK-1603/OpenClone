"""
OpenClone Memory Intelligence System (OMIS) Core Models and Contracts.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


class MemoryType(str, Enum):
    PROJECT_FACT = "project_fact"
    DECISION = "decision"
    SESSION_CHECKPOINT = "session_checkpoint"
    LESSON = "lesson"
    PREFERENCE = "preference"
    KNOWLEDGE_REFERENCE = "knowledge_reference"
    WORKING_MEMORY = "working_memory"


class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class MemoryStatus(str, Enum):
    CURRENT = "CURRENT"
    REVIEW_DUE = "REVIEW_DUE"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    DISPUTED = "DISPUTED"
    UNVERIFIED = "UNVERIFIED"
    ARCHIVED = "ARCHIVED"


class MemoryAuthority(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    HUMAN_CONFIRMED = "human_confirmed"


@dataclass
class SourceRef:
    uri: str
    source_type: str = "document"
    revision_or_date: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "source_type": self.source_type,
            "revision_or_date": self.revision_or_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SourceRef:
        return cls(
            uri=data.get("uri", ""),
            source_type=data.get("source_type", "document"),
            revision_or_date=data.get("revision_or_date", ""),
        )


@dataclass
class MemoryScope:
    project_id: str
    workspace_id: str
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    agent_id: Optional[str] = None
    owner: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "user_id": self.user_id,
            "organization_id": self.organization_id,
            "agent_id": self.agent_id,
            "owner": self.owner,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryScope:
        return cls(
            project_id=str(data.get("project_id", "")),
            workspace_id=str(data.get("workspace_id", "")),
            user_id=data.get("user_id"),
            organization_id=data.get("organization_id"),
            agent_id=data.get("agent_id"),
            owner=data.get("owner"),
        )


@dataclass
class MemoryRecord:
    id: str
    title: str
    statement: str
    memory_type: MemoryType = MemoryType.PROJECT_FACT
    scope: MemoryScope = field(default_factory=lambda: MemoryScope(project_id="default", workspace_id="default"))
    schema_version: str = "2.0"
    details: Optional[str] = None
    classification: Classification = Classification.INTERNAL
    status: MemoryStatus = MemoryStatus.CURRENT
    authority: MemoryAuthority = MemoryAuthority.VERIFIED
    confidence: float = 1.0
    source_refs: List[SourceRef] = field(default_factory=list)
    observed_at: Optional[str] = None
    recorded_at: Optional[str] = None
    verified_at: Optional[str] = None
    review_due_at: Optional[str] = None
    expires_at: Optional[str] = None
    approved_by: Optional[str] = None
    supersedes: List[str] = field(default_factory=list)
    superseded_by: List[str] = field(default_factory=list)
    related_records: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if not self.recorded_at:
            self.recorded_at = datetime.now(timezone.utc).isoformat()
        if isinstance(self.memory_type, str):
            self.memory_type = MemoryType(self.memory_type)
        if isinstance(self.classification, str):
            self.classification = Classification(self.classification)
        if isinstance(self.status, str):
            self.status = MemoryStatus(self.status)
        if isinstance(self.authority, str):
            self.authority = MemoryAuthority(self.authority)
        if isinstance(self.scope, dict):
            self.scope = MemoryScope.from_dict(self.scope)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "schema_version": self.schema_version,
            "title": self.title,
            "memory_type": self.memory_type.value,
            "scope": self.scope.to_dict(),
            "statement": self.statement,
            "details": self.details,
            "classification": self.classification.value,
            "status": self.status.value,
            "authority": self.authority.value,
            "confidence": self.confidence,
            "source_refs": [s.to_dict() if hasattr(s, "to_dict") else s for s in self.source_refs],
            "observed_at": self.observed_at,
            "recorded_at": self.recorded_at,
            "verified_at": self.verified_at,
            "review_due_at": self.review_due_at,
            "expires_at": self.expires_at,
            "approved_by": self.approved_by,
            "supersedes": list(self.supersedes),
            "superseded_by": list(self.superseded_by),
            "related_records": list(self.related_records),
            "limitations": list(self.limitations),
            "created_by": self.created_by,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryRecord:
        d = dict(data)
        scope_data = d.get("scope", {})
        scope = MemoryScope.from_dict(scope_data) if isinstance(scope_data, dict) else scope_data
        sources = [
            SourceRef.from_dict(s) if isinstance(s, dict) else s
            for s in d.get("source_refs", [])
        ]
        return cls(
            id=d["id"],
            title=d["title"],
            statement=d.get("statement", d.get("title", "")),
            memory_type=MemoryType(d.get("memory_type", MemoryType.PROJECT_FACT.value)),
            scope=scope,
            schema_version=d.get("schema_version", "2.0"),
            details=d.get("details"),
            classification=Classification(d.get("classification", Classification.INTERNAL.value)),
            status=MemoryStatus(d.get("status", MemoryStatus.CURRENT.value)),
            authority=MemoryAuthority(d.get("authority", MemoryAuthority.VERIFIED.value)),
            confidence=float(d.get("confidence", 1.0)),
            source_refs=sources,
            observed_at=d.get("observed_at"),
            recorded_at=d.get("recorded_at"),
            verified_at=d.get("verified_at"),
            review_due_at=d.get("review_due_at"),
            expires_at=d.get("expires_at"),
            approved_by=d.get("approved_by"),
            supersedes=list(d.get("supersedes", [])),
            superseded_by=list(d.get("superseded_by", [])),
            related_records=list(d.get("related_records", [])),
            limitations=list(d.get("limitations", [])),
            created_by=d.get("created_by"),
            updated_at=d.get("updated_at"),
        )
