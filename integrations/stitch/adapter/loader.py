"""Loader module for Google Stitch Skills.
Loads markdown content, instructions, style guides, and supporting code
without modifying or truncating the original upstream authoring.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from .discovery import StitchDiscovery, StitchSkillDescriptor


@dataclass
class LoadedStitchSkill:
    """Complete loaded skill bundle including body and all attached resources."""
    descriptor: StitchSkillDescriptor
    body: str
    frontmatter: Dict[str, Any]
    resources: Dict[str, str] = field(default_factory=dict)
    examples: Dict[str, str] = field(default_factory=dict)
    scripts: Dict[str, Path] = field(default_factory=dict)


class StitchSkillLoader:
    """Loads Stitch skill contents into memory for agent execution."""

    def __init__(self, discovery: Optional[StitchDiscovery] = None):
        self.discovery = discovery or StitchDiscovery()
        self._catalog = self.discovery.discover_all()
        self._cache: Dict[str, LoadedStitchSkill] = {}

    def load(self, skill_id: str) -> LoadedStitchSkill:
        """Load a skill by either internal ID or upstream ID."""
        if skill_id in self._cache:
            return self._cache[skill_id]

        if skill_id not in self._catalog:
            raise KeyError(f"Stitch skill '{skill_id}' is not discovered in catalog.")

        desc = self._catalog[skill_id]
        raw_text = desc.skill_md_path.read_text(encoding="utf-8")

        body = raw_text
        frontmatter: Dict[str, Any] = {}

        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].strip()
                for line in parts[1].splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        frontmatter[k.strip()] = v.strip().strip('"').strip("'")

        # Load resources
        resources: Dict[str, str] = {}
        for res_dir_name in ["resources", "references", "reference"]:
            res_dir = desc.skill_dir / res_dir_name
            if res_dir.exists():
                for f in res_dir.iterdir():
                    if f.is_file() and f.suffix in [".md", ".json", ".txt"]:
                        try:
                            resources[f.name] = f.read_text(encoding="utf-8")
                        except Exception:
                            pass

        # Load examples
        examples: Dict[str, str] = {}
        ex_dir = desc.skill_dir / "examples"
        if ex_dir.exists():
            for f in ex_dir.iterdir():
                if f.is_file():
                    try:
                        examples[f.name] = f.read_text(encoding="utf-8")
                    except Exception:
                        pass

        # Index scripts
        scripts: Dict[str, Path] = {}
        sc_dir = desc.skill_dir / "scripts"
        if sc_dir.exists():
            for f in sc_dir.iterdir():
                if f.is_file():
                    scripts[f.name] = f

        loaded = LoadedStitchSkill(
            descriptor=desc,
            body=body,
            frontmatter=frontmatter,
            resources=resources,
            examples=examples,
            scripts=scripts,
        )

        self._cache[desc.id] = loaded
        self._cache[desc.upstream_id] = loaded
        return loaded
