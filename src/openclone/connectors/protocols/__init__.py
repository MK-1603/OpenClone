"""Protocol bridges package."""
from src.openclone.connectors.protocols.function_calling import FunctionCallingBridge
from src.openclone.connectors.protocols.mcp_http import McpHttpBridge
from src.openclone.connectors.protocols.mcp_sse import McpSseBridge
from src.openclone.connectors.protocols.mcp_stdio import McpStdioBridge
from src.openclone.connectors.protocols.rest import RestProtocolBridge
from src.openclone.connectors.protocols.openapi import OpenApiBridge

__all__ = [
    "FunctionCallingBridge",
    "McpHttpBridge",
    "McpSseBridge",
    "McpStdioBridge",
    "RestProtocolBridge",
    "OpenApiBridge",
]
