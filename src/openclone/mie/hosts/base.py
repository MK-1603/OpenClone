"""OpenClone Model Intelligence Engine (MIE) — Host Coding Environment Adapters.

Defines host adapter contracts for AI IDEs and CLI coding agents:
Google Antigravity, Anthropic Claude Code, Cursor IDE, OpenAI Codex, Kiro, and ChatGPT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.openclone.mie.models import TaskRequirement


@dataclass
class HostMetadata:
    """Declared capabilities, native model affinities, and governance policies of an AI host."""
    host_id: str
    display_name: str
    primary_interface: str               # "mcp", "cli", "extension", "api"
    native_model_affinity: List[str]      # Models natively hosted or bundled with this IDE
    supports_mcp: bool = True
    supports_terminal_tools: bool = True
    supports_visual_ui: bool = False
    governance_notes: str = ""


class BaseHostAdapter:
    """Canonical base adapter for an AI coding host environment."""

    def __init__(self, metadata: HostMetadata):
        self.metadata = metadata

    def format_task_prompt(self, req: TaskRequirement) -> str:
        """Format an engineering prompt with host-specific instructions and boundaries."""
        boundary = (
            f"\n\n[OpenClone Governance]\n"
            f"- Task Category: {req.category.value}\n"
            f"- Reasoning Required: {req.requires_reasoning}\n"
            f"- Tools Required: {req.requires_tools}\n"
            f"- Standard: Zero AI Slop. Deterministic engineering quality."
        )
        return req.prompt + boundary

    def to_dict(self) -> Dict[str, Any]:
        return {
            "host_id": self.metadata.host_id,
            "display_name": self.metadata.display_name,
            "primary_interface": self.metadata.primary_interface,
            "native_model_affinity": self.metadata.native_model_affinity,
            "supports_mcp": self.metadata.supports_mcp,
            "supports_terminal_tools": self.metadata.supports_terminal_tools,
            "supports_visual_ui": self.metadata.supports_visual_ui,
            "governance_notes": self.metadata.governance_notes,
        }


# Concrete Host Adapters
class AntigravityHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="antigravity",
                display_name="Google Antigravity",
                primary_interface="mcp",
                native_model_affinity=["gemini-2.0-flash", "gemini-1.5-pro"],
                supports_mcp=True,
                supports_terminal_tools=True,
                supports_visual_ui=True,
                governance_notes="Native Google IDE with MCP server integration and Generative UI support.",
            )
        )


class ClaudeCodeHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="claude_code",
                display_name="Claude Code CLI",
                primary_interface="cli",
                native_model_affinity=["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-3-5-haiku"],
                supports_mcp=True,
                supports_terminal_tools=True,
                supports_visual_ui=False,
                governance_notes="Autonomous terminal agent with Bash, Glob, Grep, Edit, and MCP support.",
            )
        )


class CursorHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="cursor",
                display_name="Cursor IDE",
                primary_interface="extension",
                native_model_affinity=["claude-3-5-sonnet", "gpt-6.2-sol", "gpt-6.2-astra"],
                supports_mcp=True,
                supports_terminal_tools=True,
                supports_visual_ui=True,
                governance_notes="VS Code fork with Composer, inline editing, and MCP client.",
            )
        )


class CodexHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="codex",
                display_name="OpenAI Codex / CLI",
                primary_interface="cli",
                native_model_affinity=["gpt-6.2-sol", "gpt-6.2-astra", "o3-mini", "o1"],
                supports_mcp=True,
                supports_terminal_tools=True,
                supports_visual_ui=False,
                governance_notes="OpenAI autonomous coding runner and evaluation harness.",
            )
        )


class KiroHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="kiro",
                display_name="Kiro AI",
                primary_interface="mcp",
                native_model_affinity=["gpt-6.2-sol", "claude-3-5-sonnet"],
                supports_mcp=True,
                supports_terminal_tools=True,
                supports_visual_ui=False,
                governance_notes="Agentic coding platform with autonomous file and test execution.",
            )
        )


class ChatGPTHostAdapter(BaseHostAdapter):
    def __init__(self):
        super().__init__(
            HostMetadata(
                host_id="chatgpt",
                display_name="ChatGPT Desktop & Advanced Data Analysis",
                primary_interface="api",
                native_model_affinity=["gpt-6.2-sol", "gpt-6.2-astra", "o1"],
                supports_mcp=False,
                supports_terminal_tools=False,
                supports_visual_ui=True,
                governance_notes="Web / desktop chat host with code interpreter container sandbox.",
            )
        )
