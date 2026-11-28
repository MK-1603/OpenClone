"""Function calling translation bridge for API-driven AI platforms (OpenAI, Gemini, Mistral, GLM)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.integrations.capabilities import Capability


class FunctionCallingBridge:
    """Translates canonical OpenClone capabilities into vendor-specific function schemas and back."""

    @staticmethod
    def to_openai_tool(capability: Capability) -> Dict[str, Any]:
        """Format as OpenAI / ChatGPT tool definition."""
        return {
            "type": "function",
            "function": {
                "name": capability.id,
                "description": f"{capability.description} [Category: {capability.category.value}]",
                "parameters": capability.input_schema,
                "strict": False,
            },
        }

    @staticmethod
    def to_gemini_declaration(capability: Capability) -> Dict[str, Any]:
        """Format as Google Gemini FunctionDeclaration specification."""
        # Gemini expects properties and type in OpenAPI 3.0 schema
        schema = dict(capability.input_schema)
        # Ensure 'type' is uppercase for Gemini if needed, or valid OpenAPI format
        return {
            "name": capability.id,
            "description": capability.description,
            "parameters": schema,
        }

    @staticmethod
    def to_mistral_tool(capability: Capability) -> Dict[str, Any]:
        """Format as Mistral Le Chat / Mistral API tool definition."""
        return {
            "type": "function",
            "function": {
                "name": capability.id,
                "description": capability.description,
                "parameters": capability.input_schema,
            },
        }

    @staticmethod
    def to_zai_tool(capability: Capability) -> Dict[str, Any]:
        """Format as Z.ai GLM tool declaration."""
        return {
            "type": "function",
            "function": {
                "name": capability.id,
                "description": capability.description,
                "parameters": capability.input_schema,
            },
        }

    @staticmethod
    def parse_gemini_call(call_payload: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """Extract function name and arguments from Gemini function_call object."""
        # Gemini payload: {"name": "func_name", "args": {...}}
        name = call_payload.get("name", "")
        args = call_payload.get("args") or call_payload.get("arguments") or {}
        return name, args

    @staticmethod
    def parse_openai_call(call_payload: Dict[str, Any]) -> tuple[str, Dict[str, Any], str]:
        """Extract function name, parsed arguments, and tool_call_id from OpenAI tool_call."""
        import json
        call_id = call_payload.get("id", "")
        func = call_payload.get("function", {})
        name = func.get("name", "")
        raw_args = func.get("arguments", {})
        if isinstance(raw_args, str):
            try:
                args = json.loads(raw_args)
            except Exception:
                args = {}
        else:
            args = raw_args or {}
        return name, args, call_id
