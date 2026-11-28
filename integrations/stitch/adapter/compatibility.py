"""Compatibility layer for Google Stitch Skills.
Handles dual-namespace resolution (stitch::* vs stitch-*), tool naming
transformations across IDEs, and frontmatter mapping.
"""
import re
from typing import Dict, List, Optional, Tuple


class StitchCompatibility:
    """Normalizes identifiers and tools between Stitch and OpenClone."""

    # Tool mapping across agent environments
    TOOL_NAME_MAP: Dict[str, str] = {
        "webfetch": "web_fetch",
        "bash": "run_command",
        "Bash": "run_command",
        "Read": "read_file",
        "Write": "write_file",
        "list_tools": "mcp_list_tools",
    }

    @classmethod
    def normalize_identifier(cls, skill_id: str) -> str:
        """Converts an upstream or aliased identifier to standard internal format.
        
        Example:
            'stitch::generate-design' -> 'stitch-generate-design'
            'generate-design' -> 'stitch-generate-design'
            'stitch-generate-design' -> 'stitch-generate-design'
        """
        cleaned = skill_id.strip()
        if cleaned.startswith("stitch::"):
            cleaned = "stitch-" + cleaned[len("stitch::"):]
        elif not cleaned.startswith("stitch-") and not cleaned.startswith("remotion") and not cleaned.startswith("shadcn"):
            cleaned = f"stitch-{cleaned}"
        return cleaned

    @classmethod
    def to_upstream_identifier(cls, skill_id: str) -> str:
        """Converts internal identifier back to canonical upstream format.
        
        Example:
            'stitch-generate-design' -> 'stitch::generate-design'
        """
        if skill_id.startswith("stitch-"):
            suffix = skill_id[len("stitch-"):]
            # Certain upstream skills use stitch:: and others do not
            if suffix in [
                "generate-design", "manage-design-system", "extract-design-md",
                "extract-static-html", "code-to-design", "upload-to-stitch",
                "react-components", "react-native"
            ]:
                return f"stitch::{suffix}"
            return suffix
        return skill_id

    @classmethod
    def map_tool(cls, tool_name: str) -> str:
        """Maps an upstream tool name to OpenClone tool equivalent."""
        return cls.TOOL_NAME_MAP.get(tool_name, tool_name)

    @classmethod
    def is_mcp_pattern(cls, tool_pattern: str) -> bool:
        """Checks if tool requirement represents a dynamic MCP namespace."""
        return "stitch*" in tool_pattern or "shadcn*" in tool_pattern
