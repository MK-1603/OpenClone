"""Discovery module for Google Stitch Skills.
Recursively inspects integrations/stitch and catalogues all skills with their
upstream metadata, allowed tools, resources, and dependencies.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Dict, List, Optional


@dataclass
class StitchSkillDescriptor:
    """Detailed catalog descriptor for a Stitch skill."""
    id: str
    upstream_id: str
    display_name: str
    plugin_group: str
    description: str
    skill_dir: Path
    skill_md_path: Path
    allowed_tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    has_scripts: bool = False
    has_resources: bool = False
    has_examples: bool = False
    has_references: bool = False
    mcp_required: bool = False
    status: str = "REGISTERED"

    def to_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "upstream_id": self.upstream_id,
            "display_name": self.display_name,
            "plugin_group": self.plugin_group,
            "description": self.description,
            "skill_dir": str(self.skill_dir),
            "skill_md_path": str(self.skill_md_path),
            "allowed_tools": self.allowed_tools,
            "dependencies": self.dependencies,
            "has_scripts": self.has_scripts,
            "has_resources": self.has_resources,
            "has_examples": self.has_examples,
            "has_references": self.has_references,
            "mcp_required": self.mcp_required,
            "status": self.status,
        }


class StitchDiscovery:
    """Discovers all Stitch skills within the integration package."""

    PLUGIN_GROUPS = {
        "design": "stitch-design",
        "build": "stitch-build",
        "utilities": "stitch-utilities",
    }

    KNOWN_DEPENDENCIES = {
        "stitch-code-to-design": [
            "stitch-extract-static-html",
            "stitch-extract-design-md",
            "stitch-upload-to-stitch",
        ],
        "stitch-generate-design": ["stitch-manage-design-system"],
        "stitch-react-components": ["stitch-design-md"],
        "stitch-react-vite-dashboard": ["stitch-design-md"],
        "stitch-stitch-loop": ["stitch-site-md", "stitch-generate-design"],
    }

    def __init__(self, root: Optional[Path] = None):
        if root is None:
            # Root is integrations/stitch
            self.root = Path(__file__).resolve().parents[1]
        else:
            self.root = root

    def discover_all(self) -> Dict[str, StitchSkillDescriptor]:
        """Discover and index all skills across design, build, and utilities."""
        catalog: Dict[str, StitchSkillDescriptor] = {}

        for group_dir, plugin_group in self.PLUGIN_GROUPS.items():
            skills_dir = self.root / group_dir / "skills"
            if not skills_dir.exists():
                continue

            for item in sorted(skills_dir.iterdir()):
                if not item.is_dir():
                    continue

                skill_md = item / "SKILL.md"
                if not skill_md.exists():
                    continue

                descriptor = self._parse_skill(item, skill_md, plugin_group)
                catalog[descriptor.id] = descriptor
                # Also index by upstream identifier
                catalog[descriptor.upstream_id] = descriptor

        return catalog

    def _parse_skill(
        self,
        skill_dir: Path,
        skill_md: Path,
        plugin_group: str,
    ) -> StitchSkillDescriptor:
        raw_text = skill_md.read_text(encoding="utf-8")
        metadata: Dict[str, str] = {}
        allowed_tools: List[str] = []

        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                in_tools = False
                for line in frontmatter_text.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("allowed-tools:"):
                        in_tools = True
                        continue
                    if in_tools:
                        if stripped.startswith("-"):
                            tool_name = stripped.lstrip("-").strip().strip('"').strip("'")
                            allowed_tools.append(tool_name)
                        elif stripped and ":" in stripped:
                            in_tools = False

                    if not in_tools and ":" in stripped:
                        k, v = stripped.split(":", 1)
                        metadata[k.strip()] = v.strip().strip('"').strip("'")

        folder_name = skill_dir.name
        upstream_id = metadata.get("name", folder_name)

        # Standard internal ID: prefix with stitch- if not already
        if upstream_id.startswith("stitch::"):
            internal_id = "stitch-" + upstream_id[len("stitch::"):]
        elif not folder_name.startswith("stitch-"):
            internal_id = f"stitch-{folder_name}"
        else:
            internal_id = folder_name

        display_name = folder_name.replace("-", " ").title()
        description = metadata.get("description", "")
        if not description:
            # Fallback to first line in markdown header
            for line in raw_text.splitlines():
                if line.startswith("# "):
                    display_name = line.lstrip("# ").strip()
                    break

        mcp_required = any("stitch" in t.lower() for t in allowed_tools) or "mcp" in description.lower()
        has_scripts = (skill_dir / "scripts").exists()
        has_resources = (skill_dir / "resources").exists()
        has_examples = (skill_dir / "examples").exists()
        has_references = (skill_dir / "references").exists() or (skill_dir / "reference").exists()

        dependencies = self.KNOWN_DEPENDENCIES.get(internal_id, [])

        return StitchSkillDescriptor(
            id=internal_id,
            upstream_id=upstream_id,
            display_name=display_name,
            plugin_group=plugin_group,
            description=description,
            skill_dir=skill_dir,
            skill_md_path=skill_md,
            allowed_tools=allowed_tools,
            dependencies=dependencies,
            has_scripts=has_scripts,
            has_resources=has_resources,
            has_examples=has_examples,
            has_references=has_references,
            mcp_required=mcp_required,
            status="REGISTERED",
        )
