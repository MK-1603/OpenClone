"""Dependency validation for Google Stitch Skills.
Evaluates local runtime capabilities (Python, Node.js, Git), MCP connectivity,
and inter-skill prerequisite chains.
"""
from dataclasses import dataclass, field
import os
import shutil
import sys
from typing import Dict, List, Optional
from .discovery import StitchDiscovery, StitchSkillDescriptor


@dataclass
class SkillDependencyReport:
    """Readiness assessment for a specific Stitch skill."""
    skill_id: str
    is_ready: bool
    missing_prerequisites: List[str] = field(default_factory=list)
    missing_system_tools: List[str] = field(default_factory=list)
    mcp_available: bool = False
    details: Dict[str, any] = field(default_factory=dict)


class StitchDependencyValidator:
    """Validates operational requirements for all Stitch skills."""

    def __init__(self, discovery: Optional[StitchDiscovery] = None):
        self.discovery = discovery or StitchDiscovery()
        self._catalog = self.discovery.discover_all()

    def check_system_environment(self) -> Dict[str, bool]:
        """Check presence of common host tools."""
        return {
            "python": sys.version_info >= (3, 10),
            "git": shutil.which("git") is not None,
            "node": shutil.which("node") is not None,
            "npm": shutil.which("npm") is not None,
            "curl": shutil.which("curl") is not None,
            "bash": shutil.which("bash") is not None,
        }

    def validate_skill(self, skill_id: str, mcp_connected: bool = False) -> SkillDependencyReport:
        """Validate readiness of an individual skill."""
        if skill_id not in self._catalog:
            return SkillDependencyReport(
                skill_id=skill_id,
                is_ready=False,
                missing_prerequisites=[f"Skill '{skill_id}' is not in catalog"],
            )

        desc = self._catalog[skill_id]
        missing_prereqs = []
        missing_tools = []
        env = self.check_system_environment()

        # Check Node.js if skill has package.json or validation script
        if (desc.skill_dir / "package.json").exists() or (desc.skill_dir / "scripts" / "validate.js").exists():
            if not env["node"] or not env["npm"]:
                missing_tools.append("Node.js / npm (required for build validation scripts)")

        # Check Python if skill has python scripts
        if (desc.skill_dir / "scripts" / "upload_to_stitch.py").exists():
            if not env["python"]:
                missing_tools.append("Python 3.10+ (required for upload_to_stitch.py)")

        # Check MCP dependency
        if desc.mcp_required and not mcp_connected:
            missing_prereqs.append("Google Stitch MCP server connection (API Key required)")

        # Check inter-skill dependencies
        for dep in desc.dependencies:
            if dep not in self._catalog:
                missing_prereqs.append(f"Required dependent skill '{dep}' is missing")

        is_ready = len(missing_prereqs) == 0 and len(missing_tools) == 0

        return SkillDependencyReport(
            skill_id=desc.id,
            is_ready=is_ready,
            missing_prerequisites=missing_prereqs,
            missing_system_tools=missing_tools,
            mcp_available=mcp_connected,
            details={
                "upstream_id": desc.upstream_id,
                "plugin_group": desc.plugin_group,
            },
        )

    def validate_all(self, mcp_connected: bool = False) -> Dict[str, SkillDependencyReport]:
        """Validate all discovered skills."""
        results = {}
        for skill_id in set(desc.id for desc in self._catalog.values()):
            results[skill_id] = self.validate_skill(skill_id, mcp_connected=mcp_connected)
        return results
