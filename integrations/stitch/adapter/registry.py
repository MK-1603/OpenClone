"""Registry module for Google Stitch Skills in OpenClone.
Bridges discovered Stitch skills into OpenClone's canonical SkillRegistry
defined in src/openclone/skills/engine.py.
"""
from pathlib import Path
from typing import List, Optional

from src.openclone.skills.engine import Skill, SkillMaturity, SkillRegistry
from .discovery import StitchDiscovery


def register_stitch_skills(registry: Optional[SkillRegistry] = None) -> List[str]:
    """Register all 16 Stitch skills into the provided or global SkillRegistry.
    
    Returns list of registered skill IDs.
    """
    if registry is None:
        registry = SkillRegistry()

    discovery = StitchDiscovery()
    catalog = discovery.discover_all()
    registered_ids = []

    # Plugin group priorities
    PRECEDENCE_MAP = {
        "stitch-design": 12,
        "stitch-build": 14,
        "stitch-utilities": 15,
    }

    # Triggers per skill
    TRIGGERS_MAP = {
        "stitch-code-to-design": ["code to design", "migrate to stitch", "upload frontend", "html to design"],
        "stitch-extract-design-md": ["extract design md", "extract tokens", "design system extraction"],
        "stitch-extract-static-html": ["extract static html", "standalone html", "inline assets"],
        "stitch-generate-design": ["stitch generate", "generate design", "screen variants", "edit screen"],
        "stitch-manage-design-system": ["manage design system", "stitch tokens", "upload design md"],
        "stitch-upload-to-stitch": ["upload to stitch", "upload assets", "stitch upload"],
        "stitch-react-components": ["stitch to react", "react components", "stitch react", "sync stitch"],
        "stitch-react-native": ["stitch to react native", "react native components", "mobile stitch"],
        "stitch-react-vite-dashboard": ["react vite dashboard", "vite stitch", "dashboard components"],
        "stitch-remotion": ["remotion", "walkthrough video", "video from screens"],
        "stitch-shadcn-ui": ["shadcn", "shadcn-ui", "shadcn components", "radix ui"],
        "stitch-design-md": ["design-md", "design spec", "design markdown", "semantic tokens"],
        "stitch-enhance-prompt": ["enhance prompt", "ui keywords", "refine prompt", "stitch prompt"],
        "stitch-site-md": ["site-md", "site constitution", "multipage spec", "site architecture"],
        "stitch-stitch-loop": ["stitch-loop", "autonomous site generation", "multipage website loop"],
        "stitch-taste-design": ["taste-design", "anti-slop design", "curated palette", "typography tokens"],
    }

    for descriptor in catalog.values():
        internal_id = descriptor.id
        if internal_id in registry.skills:
            continue

        rel_path = f"integrations/stitch/{descriptor.skill_dir.parent.parent.name}/skills/{descriptor.skill_dir.name}/SKILL.md"

        skill_obj = Skill(
            id=internal_id,
            name=f"Stitch: {descriptor.display_name}",
            version="1.0.0",
            category="design",
            description=descriptor.description,
            triggers=TRIGGERS_MAP.get(internal_id, [descriptor.display_name.lower()]),
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=PRECEDENCE_MAP.get(descriptor.plugin_group, 15),
            required_actions=[
                f"Verify Stitch operational prerequisites for {descriptor.display_name}",
                "Follow upstream Google Stitch specification without instruction truncation",
                "Enforce OpenClone anti-generic design standards and secret redaction",
            ],
            dependencies=descriptor.dependencies,
            conflicts=[],
            supported_environments=["antigravity", "codex", "claude-code", "cursor", "cli"],
            pre_build_gates=["Stitch prerequisite check", "Design token verification"],
            finish_gates=["Visual QA verification", "Component modularity validation"],
            verification=["Stitch integration test suite"],
            path=rel_path,
            fallback_paths=[str(descriptor.skill_md_path)],
            maturity=SkillMaturity.L5_VERIFIED,
        )

        registry.register(skill_obj)
        registered_ids.append(internal_id)

    return registered_ids
