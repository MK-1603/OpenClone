"""OpenClone Agency Agents Integration — Dynamic Catalog Engine.

Discovers, parses, indexes, searches, and synchronizes the external
Agency Agents specialist workforce while preserving full original identities.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.workforce.agency.models import (
    AgencyAgentProfile,
    AgencyDivision,
    AgentSource,
    SyncReport,
)


class AgencyCatalog:
    """Central registry for external Agency Agents catalog within OpenClone."""

    def __init__(self, catalog_root: Optional[Path] = None):
        self.root = catalog_root or self._find_catalog_root()
        self._divisions: Dict[str, AgencyDivision] = {}
        self._agents: Dict[str, AgencyAgentProfile] = {}
        self._revision_hashes: Dict[str, str] = {}
        self.load()

    def _find_catalog_root(self) -> Path:
        """Locate the root directory containing external Agency Agents."""
        repo_root = Path(__file__).resolve().parents[4]
        candidate = repo_root / "framework" / "workforce" / "external" / "agency-agents"
        if candidate.is_dir():
            return candidate
        return candidate

    def load(self) -> None:
        """Discover divisions and parse all specialist agent markdown files."""
        self._divisions.clear()
        self._agents.clear()
        self._load_divisions()
        self._load_agents()

    def _load_divisions(self) -> None:
        """Load divisions from divisions.json or directory layout."""
        divisions_file = self.root / "divisions.json"
        if divisions_file.is_file():
            try:
                data = json.loads(divisions_file.read_text(encoding="utf-8"))
                for div_id, meta in data.items():
                    if div_id.startswith("_") or not isinstance(meta, dict):
                        continue
                    self._divisions[div_id] = AgencyDivision(
                        id=div_id,
                        label=meta.get("label", div_id.replace("-", " ").title()),
                        icon=meta.get("icon", "Folder"),
                        color=meta.get("color", "#64748B"),
                        description=meta.get("description", f"Specialists for {div_id}"),
                    )
            except Exception:
                pass

        # Also discover any division subdirectories on disk
        if self.root.is_dir():
            for p in self.root.iterdir():
                if p.is_dir() and not p.name.startswith("."):
                    div_id = p.name
                    if div_id not in self._divisions:
                        self._divisions[div_id] = AgencyDivision(
                            id=div_id,
                            label=div_id.replace("-", " ").title(),
                            icon="Folder",
                            color="#3B82F6",
                            description=f"Specialist agents for {div_id}",
                        )

    def _load_agents(self) -> None:
        """Scan and parse agent markdown files across all divisions."""
        if not self.root.is_dir():
            return

        for p in sorted(self.root.glob("*/*.md")):
            if p.name.startswith(".") or p.name.lower() == "readme.md":
                continue
            profile = self.parse_agent_file(p)
            if profile:
                self._agents[profile.id] = profile
                file_hash = hashlib.sha256(p.read_bytes()).hexdigest()
                self._revision_hashes[profile.id] = file_hash

        # Update agent counts per division
        for div in self._divisions.values():
            div.agent_count = sum(1 for a in self._agents.values() if a.division == div.id)

    @classmethod
    def parse_agent_file(cls, path: Path) -> Optional[AgencyAgentProfile]:
        """Parse an upstream agent markdown file, extracting YAML frontmatter and sections."""
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            return None

        frontmatter, body = cls._extract_frontmatter(content)
        division = path.parent.name
        slug = path.stem

        name = frontmatter.get("name") or slug.replace("-", " ").title()
        desc = frontmatter.get("description") or ""
        color = frontmatter.get("color") or "#3B82F6"
        emoji = frontmatter.get("emoji") or "🤖"
        vibe = frontmatter.get("vibe") or ""

        # Extract structured sections
        identity_memory = cls._extract_section(body, ["Identity & Memory", "Identity", "Role Statement"])
        mission = cls._extract_section(body, ["Core Mission", "Mission"])
        expertise = cls._extract_bullet_list(body, ["Expertise & Competencies", "Expertise", "Competencies"])
        critical_rules = cls._extract_bullet_list(body, ["Critical Rules", "Critical Rules & Boundaries", "Rules"])
        workflow_steps = cls._extract_numbered_list(body, ["Workflow Process", "Workflow", "Process"])
        deliverables = cls._extract_bullet_list(body, ["Technical Deliverables", "Deliverables"])
        communication_style = cls._extract_section(body, ["Communication Style & Success Metrics", "Communication Style"])

        return AgencyAgentProfile(
            id=slug,
            name=name,
            division=division,
            description=desc,
            color=color,
            emoji=emoji,
            vibe=vibe,
            source=AgentSource.EXTERNAL_AGENCY,
            source_file=str(path.as_posix()),
            identity_memory=identity_memory,
            mission=mission,
            expertise=expertise,
            critical_rules=critical_rules,
            workflow_steps=workflow_steps,
            deliverables=deliverables,
            communication_style=communication_style,
            raw_content=content,
        )

    @staticmethod
    def _extract_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
        """Extract YAML frontmatter without external pyyaml dependency."""
        data: Dict[str, str] = {}
        if not content.startswith("---"):
            return data, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return data, content

        fm_text = parts[1].strip()
        body = parts[2].strip()

        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                data[k] = v

        return data, body

    @staticmethod
    def _extract_section(text: str, headings: List[str]) -> str:
        """Extract text under a specific markdown heading until the next heading."""
        for h in headings:
            pattern = rf"(?:^|\n)#+\s+{re.escape(h)}[^\n]*\n([\s\S]*?)(?=\n#+\s+|\Z)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    @classmethod
    def _extract_bullet_list(cls, text: str, headings: List[str]) -> List[str]:
        """Extract bullet items (- ...) under specified heading."""
        section = cls._extract_section(text, headings)
        if not section:
            return []
        items = []
        for line in section.splitlines():
            line = line.strip()
            if line.startswith("-") or line.startswith("*"):
                cleaned = line.lstrip("-* ").strip()
                if cleaned:
                    items.append(cleaned)
        return items

    @classmethod
    def _extract_numbered_list(cls, text: str, headings: List[str]) -> List[str]:
        """Extract numbered or step items under specified heading."""
        section = cls._extract_section(text, headings)
        if not section:
            return []
        items = []
        for line in section.splitlines():
            line = line.strip()
            if re.match(r"^\d+\.\s+", line) or line.startswith("-"):
                cleaned = re.sub(r"^\d+\.\s+", "", line).lstrip("-* ").strip()
                if cleaned:
                    items.append(cleaned)
        return items

    # Public Discovery & Search APIs
    def list_divisions(self) -> List[AgencyDivision]:
        """Return all discovered divisions."""
        return list(self._divisions.values())

    def get_division(self, div_id: str) -> Optional[AgencyDivision]:
        """Get division metadata by ID."""
        return self._divisions.get(div_id)

    def list_agents(self, division: Optional[str] = None) -> List[AgencyAgentProfile]:
        """List all agents, optionally filtered by division."""
        if division:
            return [a for a in self._agents.values() if a.division == division]
        return list(self._agents.values())

    def get_agent(self, agent_id: str) -> Optional[AgencyAgentProfile]:
        """Retrieve full agent profile by ID or slug."""
        return self._agents.get(agent_id)

    def search(
        self,
        query: str,
        division: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> List[AgencyAgentProfile]:
        """Multi-criteria search across agent profiles, missions, and expertise."""
        terms = [t.lower() for t in query.split() if len(t) > 2]
        candidates = self.list_agents(division)
        results: List[Tuple[AgencyAgentProfile, int]] = []

        for agent in candidates:
            score = 0
            searchable = (
                f"{agent.name} {agent.division} {agent.description} "
                f"{agent.vibe} {agent.mission} {' '.join(agent.expertise)} "
                f"{' '.join(agent.deliverables)}"
            ).lower()

            if capability and any(capability.lower() in exp.lower() for exp in agent.expertise):
                score += 15

            for term in terms:
                if term in agent.name.lower():
                    score += 10
                elif term in searchable:
                    score += 3

            if score > 0 or not terms:
                results.append((agent, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results]

    def synchronize(self, source_directory: Optional[Path] = None) -> SyncReport:
        """Compare local catalog with external directory to detect new, modified, or removed agents."""
        src = source_directory or self.root
        new_agents: List[str] = []
        modified_agents: List[str] = []
        removed_agents: List[str] = []
        scanned_count = 0

        current_files = {p.stem: p for p in src.glob("*/*.md") if not p.name.startswith(".")}
        scanned_count = len(current_files)

        for slug, p in current_files.items():
            content_hash = hashlib.sha256(p.read_bytes()).hexdigest()
            if slug not in self._agents:
                new_agents.append(slug)
            elif self._revision_hashes.get(slug) != content_hash:
                modified_agents.append(slug)

        for slug in self._agents:
            if slug not in current_files:
                removed_agents.append(slug)

        return SyncReport(
            synced_at=json.dumps({"ts": "now"}),
            upstream_url="https://github.com/msitarzewski/agency-agents",
            total_scanned=scanned_count,
            new_agents=new_agents,
            modified_agents=modified_agents,
            removed_agents=removed_agents,
            conflicts_detected=[],
            status="IN_SYNC" if not (new_agents or modified_agents or removed_agents) else "CHANGES_PENDING",
        )
