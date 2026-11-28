"""
OpenClone Markdown Vault Memory Storage Adapter.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus, MemoryAuthority
from openclone.memory.schema import MemorySchemaValidator
from openclone.memory.storage.base import MemoryStorageAdapter


class MarkdownVaultAdapter(MemoryStorageAdapter):
    """
    Human-readable Markdown & Obsidian-compatible memory vault adapter.
    Preserves YAML frontmatter and markdown body structure.
    """

    FOLDER_MAPPING = {
        MemoryType.DECISION: "decisions",
        MemoryType.PROJECT_FACT: "facts",
        MemoryType.LESSON: "lessons",
        MemoryType.SESSION_CHECKPOINT: "sessions",
        MemoryType.PREFERENCE: "preferences",
        MemoryType.KNOWLEDGE_REFERENCE: "knowledge",
        MemoryType.WORKING_MEMORY: "working",
    }

    def __init__(self, vault_path: Path | str):
        self.vault_path = Path(vault_path).resolve()
        self.vault_path.mkdir(parents=True, exist_ok=True)
        for folder in self.FOLDER_MAPPING.values():
            (self.vault_path / folder).mkdir(parents=True, exist_ok=True)

    def _parse_file(self, file_path: Path) -> Optional[MemoryRecord]:
        if not file_path.is_file() or file_path.name.startswith("_"):
            return None
        text = file_path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None
        end_idx = text.find("\n---", 3)
        if end_idx == -1:
            return None

        fm_text = text[3:end_idx].strip()
        body = text[end_idx + 4:].strip()

        # Parse key-values from frontmatter
        data: Dict[str, Any] = {}
        curr_key = None
        for line in fm_text.splitlines():
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            if re.match(r"^-\s+", line_str) and curr_key:
                val = re.sub(r"^-\s+", "", line_str).strip().strip("\"'")
                data.setdefault(curr_key, []).append(val)
            elif ":" in line and not line.startswith(" "):
                k, _, v = line.partition(":")
                curr_key = k.strip()
                v_str = v.strip().strip("\"'")
                data[curr_key] = v_str if v_str else []

        if "id" not in data or "title" not in data:
            return None

        if body and "statement" not in data:
            data["statement"] = body
        elif not data.get("statement"):
            data["statement"] = data["title"]

        # Scope defaults if not set in frontmatter
        if "scope" not in data or not isinstance(data["scope"], dict):
            data["scope"] = {
                "project_id": data.get("project_id", "default"),
                "workspace_id": data.get("workspace_id", "default")
            }

        return MemorySchemaValidator.migrate_legacy(data)

    def _serialize_record(self, record: MemoryRecord) -> str:
        fm = [
            "---",
            f"id: \"{record.id}\"",
            f"schema_version: \"{record.schema_version}\"",
            f"title: \"{record.title}\"",
            f"memory_type: \"{record.memory_type.value}\"",
            f"project_id: \"{record.scope.project_id}\"",
            f"workspace_id: \"{record.scope.workspace_id}\"",
            f"classification: \"{record.classification.value}\"",
            f"status: \"{record.status.value}\"",
            f"authority: \"{record.authority.value}\"",
            f"confidence: {record.confidence}",
            f"recorded_at: \"{record.recorded_at}\"",
        ]
        if record.verified_at:
            fm.append(f"verified_at: \"{record.verified_at}\"")
        if record.review_due_at:
            fm.append(f"review_due_at: \"{record.review_due_at}\"")
        if record.approved_by:
            fm.append(f"approved_by: \"{record.approved_by}\"")

        if record.source_refs:
            fm.append("source_refs:")
            for s in record.source_refs:
                uri = s.uri if hasattr(s, "uri") else str(s)
                fm.append(f"  - uri: \"{uri}\"")
        else:
            fm.append("source_refs: []")

        if record.supersedes:
            fm.append("supersedes:")
            for s in record.supersedes:
                fm.append(f"  - \"{s}\"")

        if record.related_records:
            fm.append("related_records:")
            for r in record.related_records:
                fm.append(f"  - \"{r}\"")

        fm.append("---")
        fm.append("")
        fm.append(record.statement)
        if record.details:
            fm.append("")
            fm.append("### Details")
            fm.append(record.details)

        return "\n".join(fm) + "\n"

    def _get_record_path(self, record: MemoryRecord) -> Path:
        folder = self.FOLDER_MAPPING.get(record.memory_type, "facts")
        safe_title = re.sub(r"[^\w\s-]", "", record.title).strip().lower()
        safe_title = re.sub(r"[\s_]+", "-", safe_title)[:40]
        filename = f"{record.id}-{safe_title}.md" if safe_title else f"{record.id}.md"
        return self.vault_path / folder / filename

    def create(self, record: MemoryRecord) -> MemoryRecord:
        path = self._get_record_path(record)
        content = self._serialize_record(record)
        path.write_text(content, encoding="utf-8")
        return record

    def read(self, memory_id: str, scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        for p in self.vault_path.rglob("*.md"):
            if memory_id in p.name:
                rec = self._parse_file(p)
                if rec and rec.id == memory_id:
                    if scope:
                        if rec.scope.project_id != scope.project_id or rec.scope.workspace_id != scope.workspace_id:
                            return None
                    return rec
        return None

    def update(self, memory_id: str, changes: Dict[str, Any], scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        existing = self.read(memory_id, scope=scope)
        if not existing:
            return None
        data = existing.to_dict()
        for k, v in changes.items():
            if k != "id":
                data[k] = v
        updated = MemoryRecord.from_dict(data)
        # Re-write to vault
        self.create(updated)
        return updated

    def delete(self, memory_id: str, scope: Optional[MemoryScope] = None, hard: bool = False) -> bool:
        for p in self.vault_path.rglob("*.md"):
            if memory_id in p.name:
                rec = self._parse_file(p)
                if rec and rec.id == memory_id:
                    if scope and (rec.scope.project_id != scope.project_id or rec.scope.workspace_id != scope.workspace_id):
                        return False
                    if hard:
                        p.unlink(missing_ok=True)
                    else:
                        self.update(memory_id, {"status": MemoryStatus.ARCHIVED.value}, scope=scope)
                    return True
        return False

    def list(self, scope: Optional[MemoryScope] = None, memory_type: Optional[str] = None, status: Optional[str] = None, limit: int = 100) -> List[MemoryRecord]:
        records = []
        for p in sorted(self.vault_path.rglob("*.md")):
            rec = self._parse_file(p)
            if not rec:
                continue
            if scope and (rec.scope.project_id != scope.project_id or rec.scope.workspace_id != scope.workspace_id):
                continue
            if memory_type and rec.memory_type.value != memory_type:
                continue
            if status:
                if rec.status.value != status:
                    continue
            elif rec.status == MemoryStatus.ARCHIVED:
                continue
            records.append(rec)
            if len(records) >= limit:
                break
        return records

    def search(self, query: str, scope: Optional[MemoryScope] = None, limit: int = 20) -> List[MemoryRecord]:
        terms = [t.lower() for t in query.split() if t]
        all_records = self.list(scope=scope, limit=1000)
        results = []
        for rec in all_records:
            haystack = f"{rec.title} {rec.statement} {rec.details or ''}".lower()
            if any(term in haystack for term in terms):
                results.append(rec)
            if len(results) >= limit:
                break
        return results

    def health_check(self) -> Dict[str, Any]:
        count = len(list(self.vault_path.rglob("*.md")))
        return {
            "status": "HEALTHY",
            "vault_path": str(self.vault_path),
            "total_markdown_files": count,
        }

    def close(self) -> None:
        pass
