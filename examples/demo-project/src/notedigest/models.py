"""Data models for NoteDigest application."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ActionItem:
    """An action item extracted from text."""
    id: str
    description: str
    owner: str = "Unassigned"
    deadline: Optional[str] = None
    priority: str = "Normal"


@dataclass
class Decision:
    """A decision recorded during a meeting or discussion."""
    id: str
    summary: str
    context: Optional[str] = None


@dataclass
class KeyPoint:
    """A key discussion point or topic."""
    topic: str
    details: str


@dataclass
class DigestResult:
    """Full structured digest output."""
    title: str
    executive_summary: str
    decisions: List[Decision] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    key_points: List[KeyPoint] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
    raw_word_count: int = 0
