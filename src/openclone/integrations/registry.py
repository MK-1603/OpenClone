"""Central Platform Capability Registry for OpenClone Universal Integration Ecosystem."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PlatformMaturity(str, Enum):
    """Maturity and verification tier of platform integration."""
    VERIFIED = "VERIFIED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    EXPERIMENTAL = "EXPERIMENTAL"
    PROPOSED = "PROPOSED"
    UNSUPPORTED = "UNSUPPORTED"


@dataclass
class PlatformDescriptor:
    """Specification of an integrated development environment or AI platform."""
    platform_id: str
    display_name: str
    maturity: PlatformMaturity
    supported_protocols: List[str]
    config_target: str
    min_version: str = "1.0.0"
    operating_systems: List[str] = field(default_factory=lambda: ["windows", "linux", "darwin"])
    requires_auth: bool = False
    permissions_required: List[str] = field(default_factory=lambda: ["read", "inspect", "plan"])
    health_check_mechanism: str = "loopback_ping"
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform_id": self.platform_id,
            "display_name": self.display_name,
            "maturity": self.maturity.value,
            "supported_protocols": self.supported_protocols,
            "config_target": self.config_target,
            "min_version": self.min_version,
            "operating_systems": self.operating_systems,
            "requires_auth": self.requires_auth,
            "permissions_required": self.permissions_required,
            "health_check_mechanism": self.health_check_mechanism,
            "notes": self.notes,
        }


class PlatformCapabilityRegistry:
    """Central registry describing supported platform capabilities."""

    def __init__(self):
        self._descriptors: Dict[str, PlatformDescriptor] = {}
        self._load_canonical_descriptors()

    def register(self, descriptor: PlatformDescriptor) -> None:
        self._descriptors[descriptor.platform_id] = descriptor

    def get(self, platform_id: str) -> Optional[PlatformDescriptor]:
        return self._descriptors.get(platform_id.lower())

    def list_all(self) -> List[PlatformDescriptor]:
        return sorted(list(self._descriptors.values()), key=lambda d: d.platform_id)

    def filter_by_maturity(self, maturity: PlatformMaturity) -> List[PlatformDescriptor]:
        return [d for d in self.list_all() if d.maturity == maturity]

    def _load_canonical_descriptors(self) -> None:
        self.register(PlatformDescriptor(
            platform_id="antigravity",
            display_name="Google Antigravity IDE",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["mcp", "skills", "rules", "subagents"],
            config_target="%USERPROFILE%/.gemini/antigravity/plugins/",
            min_version="1.0.0",
            notes="Full native plugin, MCP stdio server, custom skills, rules, and lifecycle agents.",
        ))
        self.register(PlatformDescriptor(
            platform_id="vscode",
            display_name="Visual Studio Code",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["mcp", "extension", "tasks"],
            config_target=".vscode/mcp.json",
            min_version="1.85.0",
            notes="Extension manifest, MCP stdio server, workspace tasks, and sidebar explorer.",
        ))
        self.register(PlatformDescriptor(
            platform_id="cursor",
            display_name="Cursor AI Editor",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["mcp", "rules"],
            config_target=".cursor/mcp.json",
            min_version="0.40.0",
            notes="Context server MCP configuration and .cursorrules governance prompt.",
        ))
        self.register(PlatformDescriptor(
            platform_id="jetbrains",
            display_name="JetBrains IDEs (IntelliJ, PyCharm, etc.)",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["mcp", "tools"],
            config_target=".idea/mcp.json",
            min_version="2024.1",
            notes="JetBrains MCP client and external tools runner configuration.",
        ))
        self.register(PlatformDescriptor(
            platform_id="zed",
            display_name="Zed Editor",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["acp", "mcp"],
            config_target=".config/zed/settings.json",
            min_version="0.160.0",
            notes="Agent Client Protocol (ACP) adapter and context server integration.",
        ))
        self.register(PlatformDescriptor(
            platform_id="claude-code",
            display_name="Anthropic Claude Code",
            maturity=PlatformMaturity.VERIFIED,
            supported_protocols=["mcp"],
            config_target=".claude/mcp.json",
            min_version="1.0.0",
            notes="Claude Code CLI MCP client configuration.",
        ))
        self.register(PlatformDescriptor(
            platform_id="codex",
            display_name="OpenAI Codex / CLI Agents",
            maturity=PlatformMaturity.PARTIALLY_SUPPORTED,
            supported_protocols=["mcp", "rest"],
            config_target="codex.config.json",
            min_version="1.0.0",
            notes="Partially supported via REST gateway and MCP stdio.",
        ))
        self.register(PlatformDescriptor(
            platform_id="generic",
            display_name="Generic MCP / REST Client",
            maturity=PlatformMaturity.EXPERIMENTAL,
            supported_protocols=["mcp", "rest"],
            config_target=".openclone/mcp.json",
            min_version="1.0.0",
            notes="Standardized fallback configuration for any compliant MCP client.",
        ))


_GLOBAL_REGISTRY = PlatformCapabilityRegistry()


def get_platform_registry() -> PlatformCapabilityRegistry:
    return _GLOBAL_REGISTRY
