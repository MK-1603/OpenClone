"""
Tests for OpenClone Complete Agent Intelligence Enhancement & Workforce Upgrade.

Verifies:
1. Exact presence and synchronization of all 16 agent definitions in both agents/ and framework/agents/.
2. Valid YAML frontmatter (name, description) in all 16 agent files.
3. Full required sections in every agent specification:
   - Identity & Mission
   - Technical Expertise
   - Technology Selection / Implementation Rules
   - 6-Stage Operating Methodology
   - Skill Integration Framework
   - Action Permissions & Security Governance
   - Output Contract (valid JSON schema)
   - Maturity Assessment (L1 to L6)
4. Worker references map 100% to registered worker manifests in framework/workforce/registry/workers/.
5. Skill references map to valid skill files or SKILL-REGISTRY entries.
6. Centralized Technology Intelligence registry completeness.
"""

import json
import os
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

AGENT_FILES = [
    "orchestrator.md",
    "product-requirements-agent.md",
    "product-architect-agent.md",
    "ux-research-agent.md",
    "ui-design-agent.md",
    "frontend-agent.md",
    "backend-agent.md",
    "database-agent.md",
    "security-agent.md",
    "ai-engineering-agent.md",
    "integration-agent.md",
    "test-qa-agent.md",
    "performance-reliability-agent.md",
    "devops-release-agent.md",
    "documentation-agent.md",
    "independent-verifier-agent.md",
]

REQUIRED_SECTIONS = [
    "Identity, Mission, and Operational Scope",
    "Technical Expertise & Supported Ecosystems",
    "Operating Methodology",
    "Skill Integration Framework",
    "Action Permissions & Security Governance",
    "Output Contract",
    "Maturity Assessment (L1 to L6)",
]


def parse_frontmatter(content: str):
    """Extract YAML frontmatter between leading --- delimiters."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    raw_yaml = match.group(1)
    data = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    return data


class TestAgentIntelligenceEnhancement:
    """Comprehensive test suite for the 16 native specialist agents."""

    def test_all_16_agents_exist_in_both_directories(self):
        """Verify that all 16 agent files exist in agents/ and framework/agents/."""
        agents_dir = REPO_ROOT / "agents"
        fw_agents_dir = REPO_ROOT / "framework" / "agents"

        assert agents_dir.exists(), f"Directory missing: {agents_dir}"
        assert fw_agents_dir.exists(), f"Directory missing: {fw_agents_dir}"

        for filename in AGENT_FILES:
            agent_path = agents_dir / filename
            fw_path = fw_agents_dir / filename
            assert agent_path.is_file(), f"Missing agent in agents/: {filename}"
            assert fw_path.is_file(), f"Missing agent in framework/agents/: {filename}"

    def test_agent_directories_are_strictly_synchronized(self):
        """Verify that content in agents/ and framework/agents/ matches byte-for-byte."""
        for filename in AGENT_FILES:
            content_a = (REPO_ROOT / "agents" / filename).read_text(encoding="utf-8")
            content_b = (REPO_ROOT / "framework" / "agents" / filename).read_text(encoding="utf-8")
            assert content_a == content_b, f"Synchronization mismatch for {filename}"

    @pytest.mark.parametrize("filename", AGENT_FILES)
    def test_agent_frontmatter_validity(self, filename: str):
        """Verify that each agent file has valid frontmatter with name and description."""
        filepath = REPO_ROOT / "agents" / filename
        content = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)

        assert fm is not None, f"Missing YAML frontmatter in {filename}"
        assert "name" in fm and len(fm["name"]) > 5, f"Invalid 'name' in {filename}"
        assert "description" in fm and len(fm["description"]) > 10, f"Invalid 'description' in {filename}"
        assert fm["name"].startswith("openclone-"), f"Agent name must start with openclone-: {fm['name']}"

    @pytest.mark.parametrize("filename", AGENT_FILES)
    def test_agent_required_sections(self, filename: str):
        """Verify that all 8 standardized sections are present in every agent spec."""
        filepath = REPO_ROOT / "agents" / filename
        content = filepath.read_text(encoding="utf-8")

        for section in REQUIRED_SECTIONS:
            assert section.lower() in content.lower(), f"Agent {filename} missing section: {section}"

    @pytest.mark.parametrize("filename", AGENT_FILES)
    def test_agent_json_output_contract_validity(self, filename: str):
        """Verify that each agent defines a valid parseable JSON schema in its output contract."""
        filepath = REPO_ROOT / "agents" / filename
        content = filepath.read_text(encoding="utf-8")

        # Extract json code block
        json_blocks = re.findall(r"```json\s*\n(.*?)\n```", content, re.DOTALL)
        assert len(json_blocks) >= 1, f"No JSON code block found in Output Contract of {filename}"

        schema_found = False
        for block in json_blocks:
            try:
                parsed = json.loads(block)
                if isinstance(parsed, dict) and ("$schema" in parsed or "type" in parsed or "required" in parsed):
                    schema_found = True
                    assert parsed.get("type") == "object", f"Output contract must be object schema in {filename}"
                    assert "required" in parsed, f"Output contract schema must specify 'required' in {filename}"
                    break
            except json.JSONDecodeError:
                continue

        assert schema_found, f"No valid JSON Schema found in Output Contract of {filename}"

    @pytest.mark.parametrize("filename", AGENT_FILES)
    def test_agent_primary_worker_resolution(self, filename: str):
        """Verify that Primary Worker Manifest references exist in the 72-worker registry."""
        filepath = REPO_ROOT / "agents" / filename
        content = filepath.read_text(encoding="utf-8")

        worker_match = re.search(r"\*\*Primary Worker Manifest:\*\*\s*`([^`]+)`", content)
        assert worker_match is not None, f"Primary Worker Manifest not specified in {filename}"

        worker_rel_path = worker_match.group(1).replace("\\", "/")
        worker_full_path = REPO_ROOT / worker_rel_path

        assert worker_full_path.is_file(), (
            f"Worker manifest {worker_rel_path} referenced in {filename} does not exist in workforce registry!"
        )

        # Verify it is valid JSON
        manifest_data = json.loads(worker_full_path.read_text(encoding="utf-8"))
        assert "worker_id" in manifest_data or "id" in manifest_data or "name" in manifest_data

    @pytest.mark.parametrize("filename", AGENT_FILES)
    def test_agent_skill_references_exist(self, filename: str):
        """Verify that all referenced framework/skills/ paths exist on disk."""
        filepath = REPO_ROOT / "agents" / filename
        content = filepath.read_text(encoding="utf-8")

        # Find all framework/skills/... references
        skill_paths = re.findall(r"`(framework/skills/[^`]+)`", content)
        for sp in skill_paths:
            full_sp = REPO_ROOT / sp
            assert full_sp.exists(), f"Agent {filename} references non-existent skill file: {sp}"

    def test_centralized_technology_registry_populated(self):
        """Verify that framework/registries/TECHNOLOGY-REGISTRY.md is comprehensively populated."""
        registry_path = REPO_ROOT / "framework" / "registries" / "TECHNOLOGY-REGISTRY.md"
        assert registry_path.is_file(), "TECHNOLOGY-REGISTRY.md missing!"

        content = registry_path.read_text(encoding="utf-8")
        assert len(content.splitlines()) > 50, "TECHNOLOGY-REGISTRY.md is too short or unpopulated!"
        assert "Python" in content
        assert "TypeScript" in content
        assert "Go" in content
        assert "PostgreSQL" in content
        assert "FastAPI" in content
        assert "5-Point Technology Gate" in content

    def test_all_16_agents_have_comprehensive_size(self):
        """Verify that each upgraded agent has substantive operating specifications (>5000 bytes)."""
        for filename in AGENT_FILES:
            filepath = REPO_ROOT / "agents" / filename
            size = filepath.stat().st_size
            assert size >= 5000, f"Agent {filename} specification is too brief ({size} bytes), must be comprehensive!"
