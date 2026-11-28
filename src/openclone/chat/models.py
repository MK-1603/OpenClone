"""Data models for OpenClone Conversational AI Engine."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class IntentType(str, Enum):
    CHAT = "chat"
    INSPECT = "inspect"
    PLAN = "plan"
    EXECUTE = "execute"
    VERIFY = "verify"
    WORKFORCE = "workforce"
    MODELS = "models"
    PROVIDERS = "providers"
    WORKFLOWS = "workflows"
    DIAGNOSTICS = "diagnostics"
    CONFIG = "config"
    SLASH_COMMAND = "slash_command"


@dataclass
class ChatMessage:
    """A single turn in the conversational session."""
    role: MessageRole
    content: str
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    metadata: Dict[str, Any] = field(default_factory=dict)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "tool_calls": self.tool_calls,
        }


@dataclass
class ConversationSession:
    """Multi-turn conversation session preserving conversation history."""
    session_id: str = field(default_factory=lambda: f"sess-{uuid.uuid4().hex[:8]}")
    workspace_root: Path = field(default_factory=Path.cwd)
    created_at: float = field(default_factory=time.time)
    messages: List[ChatMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: MessageRole, content: str, **kwargs) -> ChatMessage:
        msg = ChatMessage(role=role, content=content, **kwargs)
        self.messages.append(msg)
        return msg

    def clear(self) -> None:
        """Clear session messages while preserving session ID and workspace."""
        self.messages.clear()

    def get_recent_history(self, limit: int = 10) -> List[ChatMessage]:
        """Return the most recent messages up to limit."""
        return self.messages[-limit:] if limit > 0 else self.messages
