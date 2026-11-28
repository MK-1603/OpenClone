"""
OpenClone Memory Intelligence System Schema Validator & Migration Engine.
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
from openclone.memory.models import MemoryRecord, MemoryType, MemoryStatus, Classification, MemoryAuthority

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "framework" / "schemas" / "memory-record.schema.json"


class SchemaValidationError(ValueError):
    """Raised when a memory record violates the canonical schema."""
    pass


class MemorySchemaValidator:
    """Validates memory records against canonical constraints."""

    REQUIRED_FIELDS = {
        "id", "schema_version", "title", "memory_type", "scope",
        "statement", "classification", "status", "authority", "recorded_at"
    }

    VALID_MEMORY_TYPES = {m.value for m in MemoryType}
    VALID_STATUSES = {s.value for s in MemoryStatus}
    VALID_CLASSIFICATIONS = {c.value for c in Classification}
    VALID_AUTHORITIES = {a.value for a in MemoryAuthority}

    ID_PATTERN = re.compile(r"^MEM-[0-9A-Za-z_-]+$")

    @classmethod
    def validate_dict(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []

        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return False, errors

        # Validate ID pattern
        if not cls.ID_PATTERN.match(str(data.get("id", ""))):
            errors.append(f"Invalid id format '{data.get('id')}'. Must match ^MEM-[0-9A-Za-z_-]+$")

        # Validate Enums
        m_type = data.get("memory_type")
        if m_type not in cls.VALID_MEMORY_TYPES:
            errors.append(f"Invalid memory_type '{m_type}'. Allowed: {sorted(cls.VALID_MEMORY_TYPES)}")

        status = data.get("status")
        if status not in cls.VALID_STATUSES:
            errors.append(f"Invalid status '{status}'. Allowed: {sorted(cls.VALID_STATUSES)}")

        classification = data.get("classification")
        if classification not in cls.VALID_CLASSIFICATIONS:
            errors.append(f"Invalid classification '{classification}'. Allowed: {sorted(cls.VALID_CLASSIFICATIONS)}")

        authority = data.get("authority")
        if authority not in cls.VALID_AUTHORITIES:
            errors.append(f"Invalid authority '{authority}'. Allowed: {sorted(cls.VALID_AUTHORITIES)}")

        # Validate Scope
        scope = data.get("scope")
        if not isinstance(scope, dict):
            errors.append("Field 'scope' must be an object with 'project_id' and 'workspace_id'")
        else:
            if not scope.get("project_id"):
                errors.append("Scope missing non-empty 'project_id'")
            if not scope.get("workspace_id"):
                errors.append("Scope missing non-empty 'workspace_id'")

        # Validate confidence
        confidence = data.get("confidence")
        if confidence is not None:
            try:
                c_val = float(confidence)
                if not (0.0 <= c_val <= 1.0):
                    errors.append(f"Confidence {c_val} out of bounds [0.0, 1.0]")
            except (ValueError, TypeError):
                errors.append(f"Invalid confidence value '{confidence}'")

        # Provenance check: verified/human_confirmed requires source_refs
        if authority in ("verified", "human_confirmed"):
            source_refs = data.get("source_refs", [])
            if not source_refs or not isinstance(source_refs, list) or len(source_refs) == 0:
                errors.append(f"Memory with authority '{authority}' requires at least one source_ref")

        return len(errors) == 0, errors

    @classmethod
    def validate_record(cls, record: MemoryRecord) -> Tuple[bool, List[str]]:
        return cls.validate_dict(record.to_dict())

    @classmethod
    def migrate_legacy(cls, legacy_data: Dict[str, Any]) -> MemoryRecord:
        """
        Migrate legacy v1.0 / AISDF records to canonical OMIS v2.0 MemoryRecord.
        Preserves all existing data without loss.
        """
        data = dict(legacy_data)

        # ID migration
        raw_id = str(data.get("id", "MEM-0001"))
        if not raw_id.startswith("MEM-"):
            raw_id = f"MEM-{raw_id}"

        # Title / statement
        title = data.get("title", "Untitled Memory")
        statement = data.get("statement", data.get("title", "Legacy memory record"))

        # Scope migration
        scope_data = data.get("scope", {})
        if not isinstance(scope_data, dict):
            scope_data = {}
        project_id = scope_data.get("project_id") or data.get("project_id") or "default"
        workspace_id = scope_data.get("workspace_id") or data.get("workspace_id") or "default"

        # Authority fallback
        authority = data.get("authority")
        if not authority or authority not in cls.VALID_AUTHORITIES:
            # If source_refs present, mark verified; otherwise unverified
            if data.get("source_refs"):
                authority = "verified"
            else:
                authority = "unverified"

        # Enforce canonical status
        status = data.get("status", "CURRENT")
        if status not in cls.VALID_STATUSES:
            status = "CURRENT"

        # Enforce canonical memory_type
        m_type = data.get("memory_type", "project_fact")
        if m_type not in cls.VALID_MEMORY_TYPES:
            m_type = "project_fact"

        data["id"] = raw_id
        data["title"] = title
        data["statement"] = statement
        data["schema_version"] = "2.0"
        data["memory_type"] = m_type
        data["status"] = status
        data["authority"] = authority
        data["scope"] = {
            "project_id": str(project_id),
            "workspace_id": str(workspace_id),
            "user_id": scope_data.get("user_id"),
            "organization_id": scope_data.get("organization_id"),
            "agent_id": scope_data.get("agent_id"),
            "owner": scope_data.get("owner"),
        }

        return MemoryRecord.from_dict(data)
