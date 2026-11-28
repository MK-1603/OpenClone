"""
OpenClone Memory Intelligence Storage Adapter Abstract Base Class.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from openclone.memory.models import MemoryRecord, MemoryScope


class MemoryStorageAdapter(ABC):
    """Abstract interface for all OMIS storage backends."""

    @abstractmethod
    def create(self, record: MemoryRecord) -> MemoryRecord:
        """Persist a new memory record atomically."""
        pass

    @abstractmethod
    def read(self, memory_id: str, scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        """Read a single memory record by ID with optional scope enforcement."""
        pass

    @abstractmethod
    def update(self, memory_id: str, changes: Dict[str, Any], scope: Optional[MemoryScope] = None) -> Optional[MemoryRecord]:
        """Update an existing memory record atomically."""
        pass

    @abstractmethod
    def delete(self, memory_id: str, scope: Optional[MemoryScope] = None, hard: bool = False) -> bool:
        """Delete or archive a memory record by ID."""
        pass

    @abstractmethod
    def list(self, scope: Optional[MemoryScope] = None, memory_type: Optional[str] = None, status: Optional[str] = None, limit: int = 100) -> List[MemoryRecord]:
        """List memory records matching scope and filter criteria."""
        pass

    @abstractmethod
    def search(self, query: str, scope: Optional[MemoryScope] = None, limit: int = 20) -> List[MemoryRecord]:
        """Search memory records using full-text or keyword matching."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Return storage health metrics and adapter capabilities."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Release open connections and resources."""
        pass
