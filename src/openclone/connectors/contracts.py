"""Canonical contracts, models, and types for OpenClone Universal AI Assistant Connector."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set
import time


class PlatformType(str, Enum):
    """Supported external AI assistant platforms."""
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    ZAI = "zai"
    MISTRAL = "mistral"
    OPEN_WEBUI = "open_webui"
    LIBRECHAT = "librechat"


class ProtocolType(str, Enum):
    """Supported communication and integration protocols."""
    MCP_STDIO = "mcp_stdio"
    MCP_HTTP = "mcp_http"
    MCP_SSE = "mcp_sse"
    REST = "rest"
    OPENAPI = "openapi"
    FUNCTION_CALLING = "function_calling"


class ConnectionState(str, Enum):
    """Lifecycle state of an adapter connection."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    ERROR = "error"
    DEGRADED = "degraded"


@dataclass
class PlatformConfig:
    """Configuration for an individual platform adapter."""
    platform: PlatformType
    enabled: bool = True
    primary_protocol: ProtocolType = ProtocolType.MCP_HTTP
    supported_protocols: List[ProtocolType] = field(default_factory=list)
    auth_token_env: Optional[str] = None
    auth_header_name: str = "Authorization"
    auth_header_prefix: str = "Bearer"
    allowed_capabilities: Optional[List[str]] = None
    denied_capabilities: List[str] = field(default_factory=list)
    endpoint_url: Optional[str] = None
    rate_limit_per_min: int = 120
    custom_options: Dict[str, Any] = field(default_factory=dict)

    def is_capability_allowed(self, capability_id: str) -> bool:
        """Check if a capability is allowed by this platform's configuration."""
        if capability_id in self.denied_capabilities:
            return False
        if self.allowed_capabilities is not None:
            return capability_id in self.allowed_capabilities
        return True


@dataclass
class UniversalConnectorConfig:
    """Master configuration for the Universal AI Assistant Connector."""
    connector_id: str = "openclone-universal-connector"
    version: str = "1.0.0"
    workspace_root: Path = field(default_factory=lambda: Path.cwd().resolve())
    default_project_id: str = "default"
    host: str = "127.0.0.1"
    port: int = 8080
    enable_remote: bool = False
    rate_limit_per_min: int = 600
    require_authentication: bool = True
    platforms: Dict[PlatformType, PlatformConfig] = field(default_factory=dict)

    @classmethod
    def create_default(cls, workspace_root: Optional[Path] = None) -> "UniversalConnectorConfig":
        """Instantiate standard configuration with defaults for all 7 platforms."""
        root = (workspace_root or Path.cwd()).resolve()
        cfg = cls(workspace_root=root)
        
        cfg.platforms[PlatformType.CHATGPT] = PlatformConfig(
            platform=PlatformType.CHATGPT,
            enabled=True,
            primary_protocol=ProtocolType.OPENAPI,
            supported_protocols=[ProtocolType.OPENAPI, ProtocolType.MCP_HTTP],
            auth_token_env="OPENCLONE_CHATGPT_TOKEN",
            endpoint_url="/api/v1/capabilities",
        )
        cfg.platforms[PlatformType.CLAUDE] = PlatformConfig(
            platform=PlatformType.CLAUDE,
            enabled=True,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.MCP_STDIO, ProtocolType.MCP_SSE],
            auth_token_env="OPENCLONE_CLAUDE_TOKEN",
            endpoint_url="/mcp",
        )
        cfg.platforms[PlatformType.GEMINI] = PlatformConfig(
            platform=PlatformType.GEMINI,
            enabled=True,
            primary_protocol=ProtocolType.FUNCTION_CALLING,
            supported_protocols=[ProtocolType.FUNCTION_CALLING, ProtocolType.REST],
            auth_token_env="OPENCLONE_GEMINI_TOKEN",
        )
        cfg.platforms[PlatformType.ZAI] = PlatformConfig(
            platform=PlatformType.ZAI,
            enabled=True,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.MCP_SSE, ProtocolType.FUNCTION_CALLING],
            auth_token_env="OPENCLONE_ZAI_TOKEN",
            endpoint_url="/mcp",
        )
        cfg.platforms[PlatformType.MISTRAL] = PlatformConfig(
            platform=PlatformType.MISTRAL,
            enabled=True,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.FUNCTION_CALLING],
            auth_token_env="OPENCLONE_MISTRAL_TOKEN",
            endpoint_url="/mcp",
        )
        cfg.platforms[PlatformType.OPEN_WEBUI] = PlatformConfig(
            platform=PlatformType.OPEN_WEBUI,
            enabled=True,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.OPENAPI, ProtocolType.REST],
            auth_token_env="OPENCLONE_OPENWEBUI_TOKEN",
            endpoint_url="/mcp",
        )
        cfg.platforms[PlatformType.LIBRECHAT] = PlatformConfig(
            platform=PlatformType.LIBRECHAT,
            enabled=True,
            primary_protocol=ProtocolType.MCP_HTTP,
            supported_protocols=[ProtocolType.MCP_HTTP, ProtocolType.MCP_STDIO, ProtocolType.OPENAPI],
            auth_token_env="OPENCLONE_LIBRECHAT_TOKEN",
            endpoint_url="/mcp",
        )
        return cfg


@dataclass
class NormalizedRequest:
    """Canonical cross-platform tool invocation request."""
    request_id: str
    platform: PlatformType
    protocol: ProtocolType
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    raw_payload: Optional[Dict[str, Any]] = None
    headers: Dict[str, str] = field(default_factory=dict)
    auth_token: Optional[str] = None
    approval_digest: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class NormalizedResponse:
    """Canonical cross-platform tool execution response."""
    request_id: str
    platform: PlatformType
    tool_name: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_code: Optional[int] = None
    raw_response: Optional[Any] = None
    execution_time_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def to_mcp_result(self) -> Dict[str, Any]:
        """Convert normalized response to standard MCP CallToolResult structure."""
        import json
        if self.success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(self.data or {}, indent=2, default=str),
                    }
                ],
                "isError": False,
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error [{self.error_code or -32603}]: {self.error_message or 'Unknown error'}",
                    }
                ],
                "isError": True,
            }

    def to_gemini_function_response(self) -> Dict[str, Any]:
        """Convert normalized response to Gemini function response structure."""
        return {
            "name": self.tool_name,
            "response": {
                "content": self.data if self.success else {"error": self.error_message, "code": self.error_code}
            }
        }

    def to_openai_tool_call_output(self, tool_call_id: str) -> Dict[str, Any]:
        """Convert normalized response to OpenAI / ChatGPT tool message structure."""
        import json
        content = json.dumps(self.data or {}, default=str) if self.success else json.dumps({"error": self.error_message})
        return {
            "tool_call_id": tool_call_id,
            "role": "tool",
            "name": self.tool_name,
            "content": content,
        }
