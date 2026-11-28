"""OpenClone Model Intelligence Engine (MIE) — Host Adapters Package."""

from typing import Dict

from src.openclone.mie.hosts.base import (
    AntigravityHostAdapter,
    BaseHostAdapter,
    ChatGPTHostAdapter,
    ClaudeCodeHostAdapter,
    CodexHostAdapter,
    CursorHostAdapter,
    HostMetadata,
    KiroHostAdapter,
)

HOST_REGISTRY: Dict[str, BaseHostAdapter] = {
    "antigravity": AntigravityHostAdapter(),
    "claude_code": ClaudeCodeHostAdapter(),
    "cursor": CursorHostAdapter(),
    "codex": CodexHostAdapter(),
    "kiro": KiroHostAdapter(),
    "chatgpt": ChatGPTHostAdapter(),
}


def get_host_adapter(host_id: str) -> BaseHostAdapter:
    """Retrieve host adapter by identifier (defaults to Antigravity)."""
    return HOST_REGISTRY.get(host_id.lower(), HOST_REGISTRY["antigravity"])


__all__ = [
    "AntigravityHostAdapter",
    "BaseHostAdapter",
    "ChatGPTHostAdapter",
    "ClaudeCodeHostAdapter",
    "CodexHostAdapter",
    "CursorHostAdapter",
    "HOST_REGISTRY",
    "HostMetadata",
    "KiroHostAdapter",
    "get_host_adapter",
]
