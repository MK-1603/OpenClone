"""Universal AI Assistant Connector for OpenClone.

Connects multiple external AI assistant platforms (ChatGPT, Claude, Gemini,
Z.ai, Mistral Le Chat, Open WebUI, LibreChat) to OpenClone Core via a single,
governed, normalized integration fabric.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import time

from src.openclone.connectors.adapters import (
    ChatGPTAdapter,
    ClaudeAdapter,
    GeminiAdapter,
    LibreChatAdapter,
    MistralAdapter,
    OpenWebUIAdapter,
    ZaiAdapter,
)
from src.openclone.connectors.auth import ConnectorAuthManager
from src.openclone.connectors.base import BasePlatformAdapter
from src.openclone.connectors.contracts import (
    ConnectionState,
    NormalizedRequest,
    NormalizedResponse,
    PlatformConfig,
    PlatformType,
    ProtocolType,
    UniversalConnectorConfig,
)
from src.openclone.connectors.protocols import (
    FunctionCallingBridge,
    McpHttpBridge,
    McpSseBridge,
    McpStdioBridge,
    OpenApiBridge,
    RestProtocolBridge,
)
from src.openclone.integrations.capabilities import (
    Capability,
    CapabilityRegistry,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway, redact_secrets
from src.openclone.planning.agent import OpenClonePlannerAgent

logger = logging.getLogger("openclone.connectors.universal")


class UniversalAIAssistantConnector:
    """Canonical Universal AI Assistant Connector orchestrating cross-platform integrations."""

    def __init__(
        self,
        config: Optional[UniversalConnectorConfig] = None,
        gateway: Optional[IntegrationGateway] = None,
        registry: Optional[CapabilityRegistry] = None,
        planner_agent: Optional[OpenClonePlannerAgent] = None,
    ):
        self.workspace_root = config.workspace_root if config else Path.cwd().resolve()
        self.config = config or UniversalConnectorConfig.create_default(self.workspace_root)
        self.registry = registry or get_canonical_registry(self.workspace_root)
        self.gateway = gateway or IntegrationGateway(registry=self.registry, repo_root=self.workspace_root)
        self.planner_agent = planner_agent or OpenClonePlannerAgent(workspace_root=self.workspace_root)
        self.auth_manager = ConnectorAuthManager(gateway=self.gateway)

        # Audit and invocation telemetry
        self.audit_log: List[Dict[str, Any]] = []
        self.rate_limiter: Dict[str, List[float]] = {}

        # 1. Initialize and register platform adapters
        self.adapters: Dict[PlatformType, BasePlatformAdapter] = {}
        self._init_platform_adapters()

        # 2. Initialize protocol bridges
        self.mcp_http_bridge = McpHttpBridge(
            server_name="openclone-universal-connector",
            server_version=self.config.version,
            tool_discovery_fn=self._get_mcp_tools_for_discovery,
            tool_invocation_fn=self._mcp_invoke_bridge,
        )
        self.mcp_sse_bridge = McpSseBridge(self.mcp_http_bridge)
        self.mcp_stdio_bridge = McpStdioBridge(self.mcp_http_bridge)
        self.rest_bridge = RestProtocolBridge(self._rest_invoke_bridge)
        self.openapi_bridge = OpenApiBridge(self.registry)
        self.function_bridge = FunctionCallingBridge()

    def _init_platform_adapters(self) -> None:
        """Instantiate and bind all 7 platform adapters to OpenClone Core."""
        adapter_classes = [
            (PlatformType.CHATGPT, ChatGPTAdapter),
            (PlatformType.CLAUDE, ClaudeAdapter),
            (PlatformType.GEMINI, GeminiAdapter),
            (PlatformType.ZAI, ZaiAdapter),
            (PlatformType.MISTRAL, MistralAdapter),
            (PlatformType.OPEN_WEBUI, OpenWebUIAdapter),
            (PlatformType.LIBRECHAT, LibreChatAdapter),
        ]

        for p_type, cls_adapter in adapter_classes:
            p_cfg = self.config.platforms.get(p_type)
            adapter = cls_adapter(config=p_cfg)
            adapter.bind_core(self.gateway, self.registry, auth_manager=self.auth_manager)
            self.adapters[p_type] = adapter

    def get_adapter(self, platform: Union[PlatformType, str]) -> BasePlatformAdapter:
        """Retrieve adapter for target platform."""
        if isinstance(platform, str):
            try:
                platform = PlatformType(platform.lower())
            except ValueError:
                raise KeyError(f"Unsupported platform '{platform}'. Supported: {[p.value for p in PlatformType]}")
        
        adapter = self.adapters.get(platform)
        if not adapter:
            raise KeyError(f"Platform adapter for '{platform}' not initialized.")
        return adapter

    def list_supported_platforms(self) -> List[Dict[str, Any]]:
        """Return status and metadata for all 7 supported AI assistant platforms."""
        result = []
        for p_type, adapter in self.adapters.items():
            result.append({
                "platform": p_type.value,
                "enabled": adapter.config.enabled,
                "primary_protocol": adapter.config.primary_protocol.value,
                "supported_protocols": [p.value for p in adapter.config.supported_protocols],
                "state": adapter.state.value,
                "endpoint_url": adapter.config.endpoint_url,
                "auth_header": adapter.config.auth_header_name,
            })
        return result

    def discover_tools(self, platform: Union[PlatformType, str]) -> List[Dict[str, Any]]:
        """Discover OpenClone capabilities formatted specifically for target platform."""
        adapter = self.get_adapter(platform)
        return adapter.discover_tools()

    def _check_rate_limit(self, client_id: str, limit_per_min: int) -> bool:
        """Sliding-window rate limiter preventing API abuse."""
        now = time.time()
        window_start = now - 60.0
        timestamps = self.rate_limiter.setdefault(client_id, [])
        # Prune old timestamps
        self.rate_limiter[client_id] = [t for t in timestamps if t > window_start]
        if len(self.rate_limiter[client_id]) >= limit_per_min:
            return False
        self.rate_limiter[client_id].append(now)
        return True

    def invoke_tool(
        self,
        platform: Union[PlatformType, str],
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        auth_token: Optional[str] = None,
    ) -> NormalizedResponse:
        """Canonical entry point: normalize, authenticate, authorize, and execute."""
        t0 = time.monotonic()
        headers = headers or {}
        adapter = self.get_adapter(platform)

        # 1. Normalize platform request into canonical NormalizedRequest
        norm_req = adapter.normalize_request(raw_payload, headers=headers)
        if auth_token:
            norm_req.auth_token = auth_token

        # Rate limiting check
        caller_id = f"{norm_req.platform.value}:{headers.get('x-forwarded-for', 'local')}"
        if not self._check_rate_limit(caller_id, adapter.config.rate_limit_per_min):
            return adapter.normalize_error(
                PermissionError(f"Rate limit exceeded for platform {norm_req.platform.value} ({adapter.config.rate_limit_per_min}/min)"),
                norm_req,
                execution_time_ms=(time.monotonic() - t0) * 1000,
            )

        # 2. Validate capability existence in CapabilityRegistry
        cap = self.registry.get(norm_req.tool_name)
        if not cap:
            return adapter.normalize_error(
                KeyError(f"Unknown OpenClone capability: '{norm_req.tool_name}'"),
                norm_req,
                execution_time_ms=(time.monotonic() - t0) * 1000,
            )

        # 3. Authenticate caller
        auth_context = adapter.authenticate(headers, token_override=norm_req.auth_token)
        if not auth_context:
            # In development/test mode or non-strict local mode, allow default context if configured
            if not self.config.require_authentication:
                auth_context = AuthContext(
                    user_id=f"guest_{norm_req.platform.value}",
                    project_id=self.config.default_project_id,
                    scopes={"projects:read", "tasks:read", "tasks:write"},
                    client_type=f"ai_{norm_req.platform.value}",
                )
            else:
                return adapter.normalize_error(
                    PermissionError(f"Authentication failed: valid bearer token required for {norm_req.platform.value}"),
                    norm_req,
                    execution_time_ms=(time.monotonic() - t0) * 1000,
                )

        # 4. Execute via IntegrationGateway (enforces policy, scopes, human approvals, and secret redaction)
        try:
            exec_result = self.gateway.execute(
                auth=auth_context,
                capability_id=norm_req.tool_name,
                arguments=norm_req.arguments,
                approval_digest=norm_req.approval_digest,
            )
            elapsed_ms = round((time.monotonic() - t0) * 1000, 2)
            norm_resp = adapter.normalize_response(exec_result, norm_req, execution_time_ms=elapsed_ms)

            # Audit logging
            self.audit_log.append({
                "timestamp": time.time(),
                "request_id": norm_req.request_id,
                "platform": norm_req.platform.value,
                "tool_name": norm_req.tool_name,
                "success": True,
                "execution_time_ms": elapsed_ms,
                "user_id": auth_context.user_id,
            })
            return norm_resp

        except Exception as e:
            elapsed_ms = round((time.monotonic() - t0) * 1000, 2)
            self.audit_log.append({
                "timestamp": time.time(),
                "request_id": norm_req.request_id,
                "platform": norm_req.platform.value,
                "tool_name": norm_req.tool_name,
                "success": False,
                "error": str(e),
                "execution_time_ms": elapsed_ms,
                "user_id": auth_context.user_id,
            })
            return adapter.normalize_error(e, norm_req, execution_time_ms=elapsed_ms)

    def _get_mcp_tools_for_discovery(self) -> List[Dict[str, Any]]:
        """Return universal MCP tool schemas derived from CapabilityRegistry."""
        return [cap.to_mcp_tool() for cap in self.registry.list_capabilities()]

    def _mcp_invoke_bridge(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        norm_req: NormalizedRequest,
    ) -> NormalizedResponse:
        """Internal bridge for MCP tools/call."""
        payload = {
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": norm_req.request_id,
        }
        return self.invoke_tool(
            platform=norm_req.platform,
            raw_payload=payload,
            headers=norm_req.headers,
            auth_token=norm_req.auth_token,
        )

    def _rest_invoke_bridge(
        self,
        capability_id: str,
        body: Dict[str, Any],
        norm_req: NormalizedRequest,
    ) -> NormalizedResponse:
        """Internal bridge for REST HTTP dispatch."""
        payload = {
            "capability_id": capability_id,
            "arguments": body,
        }
        return self.invoke_tool(
            platform=norm_req.platform,
            raw_payload=payload,
            headers=norm_req.headers,
            auth_token=norm_req.auth_token,
        )

    def handle_mcp_jsonrpc(
        self,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        platform: Union[PlatformType, str] = PlatformType.CLAUDE,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Entry point for remote MCP Streamable HTTP calls."""
        headers = headers or {}
        p_type = PlatformType(platform) if isinstance(platform, str) else platform
        return self.mcp_http_bridge.handle_jsonrpc(
            request_body=payload,
            headers=headers,
            platform=p_type,
            auth_token=auth_token,
        )

    def handle_gemini_call(
        self,
        function_call: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Entry point for Google Gemini Function Calling execution."""
        headers = headers or {}
        norm_resp = self.invoke_tool(
            platform=PlatformType.GEMINI,
            raw_payload={"function_call": function_call},
            headers=headers,
            auth_token=auth_token,
        )
        return norm_resp.to_gemini_function_response()

    def handle_chatgpt_tool_call(
        self,
        tool_call: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Entry point for OpenAI / ChatGPT tool message execution."""
        headers = headers or {}
        norm_resp = self.invoke_tool(
            platform=PlatformType.CHATGPT,
            raw_payload=tool_call,
            headers=headers,
            auth_token=auth_token,
        )
        return norm_resp.to_openai_tool_call_output(tool_call.get("id", "call_default"))

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive multi-platform health check."""
        now = time.time()
        platform_statuses = {p.value: adapter.health_check() for p, adapter in self.adapters.items()}
        all_healthy = all(s.get("status") == "healthy" for s in platform_statuses.values())

        return {
            "connector": self.config.connector_id,
            "version": self.config.version,
            "status": "healthy" if all_healthy else "degraded",
            "capabilities_total": len(self.registry.list_capabilities()),
            "audit_events_count": len(self.audit_log),
            "platforms": platform_statuses,
            "timestamp": now,
        }


_canonical_connector: Optional[UniversalAIAssistantConnector] = None


def get_universal_connector() -> UniversalAIAssistantConnector:
    """Retrieve or create the canonical UniversalAIAssistantConnector singleton."""
    global _canonical_connector
    if _canonical_connector is None:
        _canonical_connector = UniversalAIAssistantConnector()
    return _canonical_connector
