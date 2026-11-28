"""Base platform adapter interface for OpenClone Universal AI Assistant Connector."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time

from src.openclone.connectors.contracts import (
    ConnectionState,
    NormalizedRequest,
    NormalizedResponse,
    PlatformConfig,
    PlatformType,
    ProtocolType,
)
from src.openclone.integrations.capabilities import Capability, CapabilityRegistry
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway


class BasePlatformAdapter(ABC):
    """Abstract interface that every external AI platform adapter must implement."""

    def __init__(self, config: PlatformConfig):
        self.config = config
        self.state: ConnectionState = ConnectionState.DISCONNECTED
        self.last_health_check: float = 0.0
        self.invocation_count: int = 0
        self.error_count: int = 0
        self._gateway: Optional[IntegrationGateway] = None
        self._registry: Optional[CapabilityRegistry] = None
        self._auth_manager: Optional[Any] = None

    @property
    def platform(self) -> PlatformType:
        return self.config.platform

    def bind_core(
        self,
        gateway: IntegrationGateway,
        registry: CapabilityRegistry,
        auth_manager: Optional[Any] = None,
    ) -> None:
        """Bind OpenClone Core gateway, capability registry, and auth manager."""
        self._gateway = gateway
        self._registry = registry
        self._auth_manager = auth_manager
        self.state = ConnectionState.CONNECTED

    @abstractmethod
    def format_capability_schema(self, capability: Capability) -> Dict[str, Any]:
        """Convert a canonical capability into the platform's native tool/function schema."""
        pass

    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover and format all enabled OpenClone capabilities for this platform."""
        if not self._registry:
            return []
        
        tools = []
        for cap in self._registry.list_capabilities():
            if not self.config.is_capability_allowed(cap.id):
                continue
            formatted = self.format_capability_schema(cap)
            if formatted:
                tools.append(formatted)
        return tools

    @abstractmethod
    def normalize_request(
        self,
        raw_payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> NormalizedRequest:
        """Normalize an incoming platform-specific tool call into a canonical NormalizedRequest."""
        pass

    @abstractmethod
    def normalize_response(
        self,
        canonical_result: Dict[str, Any],
        request: NormalizedRequest,
        execution_time_ms: float = 0.0,
    ) -> NormalizedResponse:
        """Format canonical capability output into platform-native structure."""
        pass

    def normalize_error(
        self,
        error: Exception,
        request: NormalizedRequest,
        execution_time_ms: float = 0.0,
    ) -> NormalizedResponse:
        """Normalize an execution or validation error into a structured response."""
        self.error_count += 1
        err_msg = str(error)
        code = -32603
        if isinstance(error, PermissionError):
            code = 403
        elif isinstance(error, KeyError):
            code = 404
        elif isinstance(error, ValueError):
            code = 400

        return NormalizedResponse(
            request_id=request.request_id,
            platform=self.platform,
            tool_name=request.tool_name,
            success=False,
            data=None,
            error_message=err_msg,
            error_code=code,
            execution_time_ms=execution_time_ms,
        )

    def authenticate(
        self,
        headers: Dict[str, str],
        token_override: Optional[str] = None,
    ) -> Optional[AuthContext]:
        """Authenticate platform caller against inbound connector auth policies."""
        # 1. Use dedicated ConnectorAuthManager if bound
        if self._auth_manager:
            auth = self._auth_manager.authenticate_inbound(
                headers=headers,
                token_override=token_override,
                expected_platform=self.platform,
            )
            if auth:
                return auth

        # 2. Check if platform has an authorized inbound environment token configured
        token = token_override
        if not token:
            header_val = headers.get(self.config.auth_header_name.lower()) or headers.get(self.config.auth_header_name)
            if header_val and header_val.startswith(f"{self.config.auth_header_prefix} "):
                token = header_val[len(self.config.auth_header_prefix) + 1:].strip()
            elif header_val:
                token = header_val.strip()

        if not token and self.config.auth_token_env:
            import os
            token = os.environ.get(self.config.auth_token_env)

        if not token or not self._gateway:
            return None

        auth = self._gateway.authenticate_token(token)
        if auth:
            auth.client_type = f"ai_assistant_{self.platform.value}"
        return auth

    def health_check(self) -> Dict[str, Any]:
        """Verify connectivity, registry presence, and platform readiness."""
        self.last_health_check = time.time()
        is_healthy = self._gateway is not None and self._registry is not None and self.config.enabled
        return {
            "platform": self.platform.value,
            "status": "healthy" if is_healthy else "unhealthy",
            "state": self.state.value,
            "primary_protocol": self.config.primary_protocol.value,
            "invocations": self.invocation_count,
            "errors": self.error_count,
            "available_capabilities": len(self.discover_tools()),
            "timestamp": self.last_health_check,
        }
