"""Stitch Skills Integration Adapter for OpenClone.
Provides discovery, loading, compatibility, MCP communication, and orchestration
for Google Stitch skills.
"""
from .discovery import StitchDiscovery, StitchSkillDescriptor
from .loader import StitchSkillLoader
from .compatibility import StitchCompatibility
from .dependencies import StitchDependencyValidator
from .mcp_client import StitchMCPClient
from .orchestration import StitchDesignOrchestrator
from .registry import register_stitch_skills

__all__ = [
    "StitchDiscovery",
    "StitchSkillDescriptor",
    "StitchSkillLoader",
    "StitchCompatibility",
    "StitchDependencyValidator",
    "StitchMCPClient",
    "StitchDesignOrchestrator",
    "register_stitch_skills",
]
