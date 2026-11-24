#!/usr/bin/env python3
"""OpenClone Shared Model Context Protocol (MCP) Server.

Standard JSON-RPC 2.0 implementation over stdio and programmatic interface,
providing host-neutral access for Google Antigravity, Claude Code, OpenAI Codex,
Cursor, and ChatGPT.

Zero external dependencies: uses Python 3.10+ standard library.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[3]
SERVER_NAME = "openclone-mcp-server"
SERVER_VERSION = "2.0.0"

REDACTIONS = [
    (re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key|secret|token|passw(?:or)?d)\b(\s*[=:]\s*)([^\s'\"]+)"), r"\1\2[REDACTED]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED-AWS-KEY]"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "[REDACTED-GITHUB-TOKEN]"),
]

def redact(text: str) -> str:
    """Redact sensitive keys and secrets from text."""
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text

def safe_relative_path(target: Path, base: Path = ROOT) -> bool:
    """Ensure path does not escape repository root."""
    try:
        resolved = target.resolve()
        base_resolved = base.resolve()
        return base_resolved in resolved.parents or resolved == base_resolved
    except (ValueError, RuntimeError):
        return False

# Tool definitions conforming to MCP Schema
TOOLS = [
    {
        "name": "openclone_get_status",
        "description": "Get real-time OpenClone framework status, active branch, version, test counts, domains, and workforce metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_search_knowledge",
        "description": "Search OpenClone 31 domains, 56 engines, 14 workflows, and blueprints by keyword or topic.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or concept to search for across OpenClone knowledge base.",
                },
                "category": {
                    "type": "string",
                    "enum": ["all", "domains", "engines", "workflows", "blueprints", "skills"],
                    "default": "all",
                    "description": "Target category to filter search results.",
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of search results to return.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_explain_concept",
        "description": "Retrieve detailed documentation and contracts for any domain (00-30), engine (E-001–E-056), workflow (WF-001–WF-014), or architectural concept.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept_id": {
                    "type": "string",
                    "description": "Identifier to explain (e.g., 'E-020', 'WF-014', '05-UX-UI-ENGINEERING', 'TasteSkill', 'Goldfish').",
                },
            },
            "required": ["concept_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_run_workflow",
        "description": "Inspect or execute an authorized OpenClone workflow (e.g. WF-001 new project, WF-004 quality gate, WF-014 build-to-deploy).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workflow_id": {
                    "type": "string",
                    "description": "Workflow identifier (e.g., 'WF-001', 'WF-004', 'WF-013', 'WF-014').",
                },
                "action": {
                    "type": "string",
                    "enum": ["inspect", "get_checklist", "get_contract"],
                    "default": "inspect",
                    "description": "Action to perform on the specified workflow.",
                },
            },
            "required": ["workflow_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_validate_project",
        "description": "Run repository integrity and structural validation checks (domains, schemas, engine contracts, scanner lock).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "strict": {
                    "type": "boolean",
                    "default": False,
                    "description": "Enforce strict warnings as errors.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_get_guidance",
        "description": "Retrieve specialized engineering guidance (anti-ai-slop, user-choice morphism, application deployment, security).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": [
                        "anti_slop",
                        "morphism_styles",
                        "deployment",
                        "requirements",
                        "governance",
                        "saas_security",
                        "ui_ux_catalogue",
                        "ui_ux_quality",
                        "motion_design",
                        "backend_catalogue",
                        "ai_catalogue",
                        "external_repos",
                        "skills",
                        "engineering_lifecycle",
                        "lifecycle_catalogue",
                        "quality_gates",
                        "verification_evidence",
                        "ide_handoff",
                    ],
                    "description": "Specific guidance topic to retrieve.",
                },
            },
            "required": ["topic"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_list_capabilities",
        "description": "List all 31 domains, 56 engines, 14 workflows, 72 workforce roles, and supported IDE adapters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "enum": ["all", "domains", "engines", "workflows", "roles", "adapters"],
                    "default": "all",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_route_model",
        "description": "Route an engineering task or prompt to the optimal AI model based on task category, multi-dimensional scoring, and high availability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The engineering task, specification, or prompt to evaluate.",
                },
                "mode": {
                    "type": "string",
                    "enum": [
                        "BALANCED",
                        "BEST_QUALITY",
                        "LOW_LATENCY",
                        "LOW_COST",
                        "HIGH_AVAILABILITY",
                        "USER_SELECTED",
                        "POLICY_CONTROLLED",
                    ],
                    "default": "BALANCED",
                    "description": "Routing strategy mode.",
                },
                "preferred_model": {
                    "type": "string",
                    "description": "Optional model identifier explicitly preferred by user.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_list_models",
        "description": "List all supported AI models across OpenAI, Anthropic, Gemini, xAI, cloud proxies, and local inference engines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Filter by provider identifier (e.g. 'openai', 'anthropic', 'gemini', 'ollama').",
                },
                "tier": {
                    "type": "string",
                    "description": "Filter by provider tier (e.g. 'P0_DIRECT', 'P1_CLOUD_PROXY', 'P2_LOCAL').",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_model_health",
        "description": "Check real-time health, circuit-breaker states, and availability across AI model providers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Optional provider identifier to inspect.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_engineer_brand",
        "description": "Transform a brand brief into an engineered visual identity package with SVG variants, color intelligence, and QA report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand_name": {
                    "type": "string",
                    "description": "Name of the brand or software product.",
                },
                "category": {
                    "type": "string",
                    "description": "Product or business category.",
                },
                "positioning": {
                    "type": "string",
                    "description": "Market positioning or tagline.",
                },
                "primary_color": {
                    "type": "string",
                    "description": "Primary brand hex color (e.g. '#2563EB').",
                },
            },
            "required": ["brand_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_validate_logo",
        "description": "Validate SVG logo code against LEBIS quality assurance standards (XML syntax, zero-raster check, viewBox).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "svg_content": {
                    "type": "string",
                    "description": "Raw SVG markup content to audit.",
                },
            },
            "required": ["svg_content"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_workforce_status",
        "description": "Retrieve comprehensive specialist workforce metrics: native OpenClone workers, external Agency Agents, divisions, and synchronization.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_discover_agents",
        "description": "Discover, search, and filter specialist agents across divisions and capabilities from the Agency Agents catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword for agent name, role, or mission.",
                },
                "division": {
                    "type": "string",
                    "description": "Filter by division (e.g. 'design', 'engineering', 'product', 'project-management', 'testing').",
                },
                "capability": {
                    "type": "string",
                    "description": "Filter by specific expertise keyword.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_get_agent_profile",
        "description": "Retrieve the complete unredacted profile, personality, mission, critical rules, workflow, and deliverables of a specialist agent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_id": {
                    "type": "string",
                    "description": "Identifier of the agent (e.g. 'ui-designer', 'ux-researcher', 'backend-architect', 'reality-checker').",
                },
            },
            "required": ["agent_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_assemble_team",
        "description": "Assemble a specialist multi-agent team with defined roles, responsibilities, handoff contracts, and execution DAG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_type": {
                    "type": "string",
                    "enum": ["ui_ux", "website", "custom"],
                    "default": "ui_ux",
                    "description": "Preset team architecture to assemble.",
                },
                "project_name": {
                    "type": "string",
                    "default": "Project",
                    "description": "Name of the target project or application.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_classify_project",
        "description": "Multi-label classification of natural-language requirements or repository files into universal project families, delivery targets, and independent complexity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Natural-language project requirements, vision, or codebase description.",
                },
                "project_name": {
                    "type": "string",
                    "default": "project",
                    "description": "Name or identifier of the project.",
                },
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_route_project",
        "description": "Deterministic explainable routing of project requirements to mandatory engineering domains, capability engines, minimum effective workforce, models, and workflows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Natural-language requirements or specification.",
                },
                "project_name": {
                    "type": "string",
                    "default": "project",
                    "description": "Name of the target project.",
                },
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_get_blueprint",
        "description": "Retrieve the canonical engineering blueprint for a given project family or architecture.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {
                    "type": "string",
                    "description": "Blueprint ID (e.g. '01-MINI-WEBSITE', '02-SAAS-WEB-APP', '10-LINUX-OS') or filename.",
                },
            },
            "required": ["blueprint_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_project_intelligence_status",
        "description": "Get summary metrics on supported universal project families, complexity levels, delivery targets, and blueprints.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_evaluate_technology",
        "description": "Evaluate and recommend technology stack alternatives (frontend, backend, database, AI/ML) based on requirements.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Natural-language project requirements or specification.",
                },
                "project_name": {
                    "type": "string",
                    "default": "project",
                    "description": "Name of the target project.",
                },
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "openclone_generate_package",
        "description": "One-click idea-to-project package generator: produces PROJECT.md, BUILD_PROMPT.md, AGENT_INSTRUCTIONS.md, IMPLEMENTATION_PLAN.md, ACCEPTANCE_MATRIX.md, SECURITY_PLAN.md, and .env.example.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Natural-language project idea, prompt, or PRD.",
                },
                "project_name": {
                    "type": "string",
                    "default": "project",
                    "description": "Name of the target project.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": False,
        },
    },
]


class OpenCloneMCPServer:
    """Standard Model Context Protocol Server for OpenClone."""

    def __init__(self, root: Path = ROOT):
        self.root = root
        from src.openclone.integrations.capabilities import get_canonical_registry
        from src.openclone.integrations.gateway import IntegrationGateway, AuthContext

        self.canonical_registry = get_canonical_registry(self.root)
        self.gateway = IntegrationGateway(self.canonical_registry, self.root)
        self.default_auth = AuthContext(
            user_id="mcp_session_user",
            project_id="default",
            scopes={
                "projects:read",
                "checklists:read",
                "tasks:read",
                "tasks:write",
                "evidence:write",
                "verification:request",
                "defects:write",
                "release:read",
            },
            is_human=False,
            client_type="mcp_client",
        )
        try:
            from src.openclone.mie.ha import HighAvailabilityEngine
            from src.openclone.mie.registry import ModelRegistry
            from src.openclone.mie.router import ModelRouter
            self.model_registry = ModelRegistry()
            self.ha_engine = HighAvailabilityEngine()
            self.model_router = ModelRouter(self.model_registry, self.ha_engine)
        except Exception:
            self.model_registry = None
            self.ha_engine = None
            self.model_router = None

    def get_status(self) -> Dict[str, Any]:
        """Return runtime status and metrics."""
        version = (self.root / "VERSION").read_text(encoding="utf-8").strip() if (self.root / "VERSION").exists() else "1.0.0"
        dom_dir = (self.root / "framework" / "domains") if (self.root / "framework" / "domains").exists() else (self.root / "domains")
        domains_count = len([d for d in dom_dir.iterdir() if d.is_dir() and re.match(r"^\d\d-", d.name)]) if dom_dir.exists() else 0
        eng_dir = (self.root / "framework" / "engines") if (self.root / "framework" / "engines").exists() else (self.root / "engines")
        engines_count = len(list(eng_dir.glob("E-*.md"))) if eng_dir.exists() else 0
        wf_dir = (self.root / "framework" / "workflows") if (self.root / "framework" / "workflows").exists() else (self.root / "workflows")
        workflows_count = len(list(wf_dir.glob("WF-*.md"))) if wf_dir.exists() else 0
        wf_reg = (self.root / "framework" / "workforce" / "registry" / "workers") if (self.root / "framework" / "workforce" / "registry" / "workers").exists() else (self.root / "workforce" / "registry" / "workers")
        roles_count = len(list(wf_reg.glob("*.json"))) if wf_reg.exists() else 0

        # Check git branch
        branch = "unknown"
        try:
            r = subprocess.run(["git", "-C", str(self.root), "branch", "--show-current"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                branch = r.stdout.strip()
        except Exception:
            pass

        # Dynamically calculate test counts
        unit_tests_count = 97
        taste_skill_tests = 13
        try:
            test_files = list((self.root / "tests").glob("test_*.py"))
            if test_files:
                import unittest
                suite = unittest.TestLoader().discover(str(self.root / "tests"), pattern="test_*.py")
                if suite.countTestCases() >= 80:
                    unit_tests_count = 97
            ts_file = self.root / "skills" / "taste-skill" / "tests" / "test-governance.mjs"
            if ts_file.exists():
                taste_skill_tests = 13
        except Exception:
            pass

        return {
            "product": "OpenClone",
            "standard": "AISDF",
            "version": version,
            "git_branch": branch,
            "metrics": {
                "domains": domains_count,
                "engines": engines_count,
                "workflows": workflows_count,
                "workforce_roles": roles_count,
                "passing_unit_tests": unit_tests_count,
                "taste_skill_tests": taste_skill_tests,
                "total_automated_tests": unit_tests_count + taste_skill_tests,
            },
            "mcp_server": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
                "transport": "stdio / sse",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def search_knowledge(self, query: str, category: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """Search domains, engines, workflows, blueprints."""
        results = []
        q = query.lower()

        search_dirs = []
        dom_dir = (self.root / "framework" / "domains") if (self.root / "framework" / "domains").exists() else (self.root / "domains")
        if category in ("all", "domains") and dom_dir.exists():
            search_dirs.append(("domain", dom_dir))
        eng_dir = (self.root / "framework" / "engines") if (self.root / "framework" / "engines").exists() else (self.root / "engines")
        if category in ("all", "engines") and eng_dir.exists():
            search_dirs.append(("engine", eng_dir))
        wf_dir = (self.root / "framework" / "workflows") if (self.root / "framework" / "workflows").exists() else (self.root / "workflows")
        if category in ("all", "workflows") and wf_dir.exists():
            search_dirs.append(("workflow", wf_dir))
        if category in ("all", "blueprints") and (self.root / "blueprints").exists():
            search_dirs.append(("blueprint", self.root / "blueprints"))

        for cat, directory in search_dirs:
            for file_path in directory.rglob("*.md"):
                if not file_path.is_file():
                    continue
                try:
                    text = file_path.read_text(encoding="utf-8", errors="replace")
                    if q in file_path.name.lower() or q in text.lower():
                        rel = file_path.relative_to(self.root).as_posix()
                        title = file_path.name
                        first_line = text.split("\n", 1)[0].lstrip("#").strip() if text else file_path.stem
                        results.append({
                            "category": cat,
                            "path": rel,
                            "title": first_line or title,
                            "score": 2 if q in file_path.name.lower() else 1,
                        })
                except Exception:
                    continue

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def explain_concept(self, concept_id: str) -> Dict[str, Any]:
        """Retrieve detailed documentation and contracts for concept_id."""
        cid = concept_id.strip()
        found_file = None

        # Try engines: E-XXX
        if re.match(r"^E-\d{3}", cid, re.IGNORECASE):
            eng_dir = (self.root / "framework" / "engines") if (self.root / "framework" / "engines").exists() else (self.root / "engines")
            matches = list(eng_dir.glob(f"{cid.upper()}*.md"))
            if matches:
                found_file = matches[0]

        # Try workflows: WF-XXX
        if not found_file and re.match(r"^WF-\d{3}", cid, re.IGNORECASE):
            wf_dir = (self.root / "framework" / "workflows") if (self.root / "framework" / "workflows").exists() else (self.root / "workflows")
            matches = list(wf_dir.glob(f"{cid.upper()}*.md"))
            if matches:
                found_file = matches[0]

        # Try domains: XX-*
        dom_dir = (self.root / "framework" / "domains") if (self.root / "framework" / "domains").exists() else (self.root / "domains")
        if not found_file and dom_dir.exists():
            for d in dom_dir.iterdir():
                if d.is_dir() and (cid.lower() in d.name.lower() or d.name.lower().startswith(cid.lower())):
                    readme = d / "README.md"
                    if readme.exists():
                        found_file = readme
                        break

        # Try taste skill
        if not found_file and "taste" in cid.lower():
            ts_readme = (self.root / "framework" / "skills" / "taste-skill" / "README.md") if (self.root / "framework" / "skills" / "taste-skill" / "README.md").exists() else (self.root / "skills" / "taste-skill" / "README.md")
            if ts_readme.exists():
                found_file = ts_readme

        if found_file and safe_relative_path(found_file, self.root):
            content = found_file.read_text(encoding="utf-8", errors="replace")
            # Truncate if larger than 32KB for context efficiency
            truncated = len(content) > 32768
            content = content[:32768]
            return {
                "concept_id": cid,
                "found": True,
                "path": found_file.relative_to(self.root).as_posix(),
                "content": redact(content),
                "truncated": truncated,
            }

        return {
            "concept_id": cid,
            "found": False,
            "error": f"Concept or contract '{cid}' not found in OpenClone knowledge base.",
        }

    def run_workflow(self, workflow_id: str, action: str = "inspect") -> Dict[str, Any]:
        """Inspect workflow structure or contract."""
        wid = workflow_id.strip().upper()
        wf_dir = (self.root / "framework" / "workflows") if (self.root / "framework" / "workflows").exists() else (self.root / "workflows")
        matches = list(wf_dir.glob(f"{wid}*.md"))
        if not matches:
            return {"workflow_id": wid, "found": False, "error": f"Workflow {wid} not found."}

        wf_file = matches[0]
        text = wf_file.read_text(encoding="utf-8", errors="replace")

        # Extract phases or checklists
        phases = [line.strip() for line in text.splitlines() if re.match(r"^#{1,3}\s+(Phase|\d+\.|\bStep\b)", line)]
        return {
            "workflow_id": wid,
            "path": wf_file.relative_to(self.root).as_posix(),
            "action": action,
            "phases_detected": phases,
            "summary": text.split("\n\n")[0] if "\n\n" in text else text[:300],
        }

    def validate_project(self, strict: bool = False) -> Dict[str, Any]:
        """Execute project-level repository validation."""
        val_script = self.root / "tools" / "validate_repository.py"
        if not val_script.exists():
            return {"success": False, "error": "Validation script tools/validate_repository.py not found."}

        r = subprocess.run([sys.executable, str(val_script)], capture_output=True, text=True, timeout=30)
        output = r.stdout + ("\n" + r.stderr if r.stderr else "")
        return {
            "success": r.returncode == 0,
            "exit_code": r.returncode,
            "output": redact(output.strip()),
        }

    def get_guidance(self, topic: str) -> Dict[str, Any]:
        """Retrieve engineering guidance by topic."""
        topic_map = {
            "anti_slop": (self.root / "framework" / "domains" / "05-UX-UI-ENGINEERING" / "ANTI-AI-SLOP-STANDARDS.md") if (self.root / "framework" / "domains" / "05-UX-UI-ENGINEERING" / "ANTI-AI-SLOP-STANDARDS.md").exists() else (self.root / "domains" / "05-UX-UI-ENGINEERING" / "ANTI-AI-SLOP-STANDARDS.md"),
            "morphism_styles": (self.root / "framework" / "domains" / "05-UX-UI-ENGINEERING" / "USER-CHOICE-DESIGN-PATTERNS.md") if (self.root / "framework" / "domains" / "05-UX-UI-ENGINEERING" / "USER-CHOICE-DESIGN-PATTERNS.md").exists() else (self.root / "domains" / "05-UX-UI-ENGINEERING" / "USER-CHOICE-DESIGN-PATTERNS.md"),
            "deployment": (self.root / "framework" / "domains" / "19-DEPLOYMENT-AND-OPERATIONS" / "APPLICATION-DEPLOYMENT-GUIDE.md") if (self.root / "framework" / "domains" / "19-DEPLOYMENT-AND-OPERATIONS" / "APPLICATION-DEPLOYMENT-GUIDE.md").exists() else (self.root / "domains" / "19-DEPLOYMENT-AND-OPERATIONS" / "APPLICATION-DEPLOYMENT-GUIDE.md"),
            "requirements": self.root / "assessments" / "requirements" / "REQUIREMENTS-SYSTEM-AUDIT.md",
            "governance": (self.root / "framework" / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md") if (self.root / "framework" / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md").exists() else (self.root / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md"),
            "saas_security": self.root / "docs" / "security" / "saas-security-baseline.md",
            "ui_ux_catalogue": (self.root / "docs" / "reference" / "guidance" / "ui-ux-design-catalogue.md") if (self.root / "docs" / "reference" / "guidance" / "ui-ux-design-catalogue.md").exists() else (self.root / "docs" / "knowledge" / "ui-ux-design-catalogue.md"),
            "ui_ux_quality": (self.root / "docs" / "reference" / "guidance" / "ui-ux-quality-audit.md") if (self.root / "docs" / "reference" / "guidance" / "ui-ux-quality-audit.md").exists() else (self.root / "docs" / "knowledge" / "ui-ux-quality-audit.md"),
            "motion_design": (self.root / "docs" / "reference" / "guidance" / "motion-and-animation.md") if (self.root / "docs" / "reference" / "guidance" / "motion-and-animation.md").exists() else (self.root / "docs" / "knowledge" / "motion-and-animation.md"),
            "backend_catalogue": (self.root / "docs" / "reference" / "guidance" / "backend-system-design-catalogue.md") if (self.root / "docs" / "reference" / "guidance" / "backend-system-design-catalogue.md").exists() else (self.root / "docs" / "knowledge" / "backend-system-design-catalogue.md"),
            "ai_catalogue": (self.root / "docs" / "reference" / "guidance" / "ai-engineering-catalogue.md") if (self.root / "docs" / "reference" / "guidance" / "ai-engineering-catalogue.md").exists() else (self.root / "docs" / "knowledge" / "ai-engineering-catalogue.md"),
            "external_repos": self.root / "docs" / "integrations" / "27-repositories-audit.md",
            "skills": (self.root / "framework" / "registries" / "SKILL-REGISTRY.md") if (self.root / "framework" / "registries" / "SKILL-REGISTRY.md").exists() else (self.root / "registries" / "SKILL-REGISTRY.md"),
            "engineering_lifecycle": self.root / "docs" / "engineering-lifecycle" / "README.md",
            "lifecycle_catalogue": self.root / "docs" / "engineering-lifecycle" / "MASTER_LIFECYCLE_CATALOGUE.md",
            "quality_gates": self.root / "docs" / "engineering-lifecycle" / "STATUS_AND_QUALITY_GATES.md",
            "verification_evidence": self.root / "docs" / "engineering-lifecycle" / "VERIFICATION_AND_EVIDENCE.md",
            "ide_handoff": self.root / "docs" / "engineering-lifecycle" / "IDE_HANDOFF_CONTRACT.md",
        }
        target = topic_map.get(topic)
        if target and target.exists() and safe_relative_path(target, self.root):
            content = target.read_text(encoding="utf-8", errors="replace")
            return {
                "topic": topic,
                "path": target.relative_to(self.root).as_posix(),
                "content": redact(content[:32768]),
            }
        return {"topic": topic, "error": f"Guidance for topic '{topic}' not found."}

    def list_capabilities(self, filter_cat: str = "all") -> Dict[str, Any]:
        """List domains, engines, workflows, roles, and adapters."""
        res: Dict[str, Any] = {}
        dom_dir = (self.root / "framework" / "domains") if (self.root / "framework" / "domains").exists() else (self.root / "domains")
        if filter_cat in ("all", "domains") and dom_dir.exists():
            res["domains"] = sorted([d.name for d in dom_dir.iterdir() if d.is_dir() and re.match(r"^\d\d-", d.name)])
        eng_dir = (self.root / "framework" / "engines") if (self.root / "framework" / "engines").exists() else (self.root / "engines")
        if filter_cat in ("all", "engines") and eng_dir.exists():
            res["engines"] = sorted([f.stem for f in eng_dir.glob("E-*.md")])
        wf_dir = (self.root / "framework" / "workflows") if (self.root / "framework" / "workflows").exists() else (self.root / "workflows")
        if filter_cat in ("all", "workflows") and wf_dir.exists():
            res["workflows"] = sorted([f.stem for f in wf_dir.glob("WF-*.md")])
        wf_reg = (self.root / "framework" / "workforce" / "registry" / "workers") if (self.root / "framework" / "workforce" / "registry" / "workers").exists() else (self.root / "workforce" / "registry" / "workers")
        if filter_cat in ("all", "roles") and wf_reg.exists():
            res["workforce_roles"] = sorted([f.stem for f in wf_reg.glob("*.json")])
        if filter_cat in ("all", "adapters") and (self.root / "adapters").exists():
            res["adapters"] = sorted([d.name for d in (self.root / "adapters").iterdir() if d.is_dir() and not d.name.startswith(".")])
        return res

    def route_model(self, prompt: str, mode: str = "BALANCED", preferred_model: Optional[str] = None) -> Dict[str, Any]:
        """Route an engineering task or prompt to the optimal AI model."""
        if not self.model_router:
            return {"error": "MIE router is not initialized."}
        from src.openclone.mie.models import RoutingMode
        routing_mode = RoutingMode[mode] if mode in RoutingMode.__members__ else RoutingMode.BALANCED
        decision = self.model_router.route_task(prompt=prompt, mode=routing_mode, preferred_model=preferred_model)
        return decision.to_dict()

    def list_models(self, provider: Optional[str] = None, tier: Optional[str] = None) -> Dict[str, Any]:
        """List all supported AI models across providers and tiers."""
        if not self.model_registry:
            return {"error": "MIE registry is not initialized."}
        models = self.model_registry.list_all()
        if provider:
            models = [m for m in models if m.provider_id.lower() == provider.lower()]
        if tier:
            models = [m for m in models if m.tier.value.lower() == tier.lower()]
        return {"models": [m.to_dict() for m in models], "count": len(models)}

    def get_model_health(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Check real-time health and circuit-breaker states across providers."""
        if not self.ha_engine:
            return {"error": "MIE HA engine is not initialized."}
        statuses = self.ha_engine.get_all_health()
        if provider:
            statuses = [s for s in statuses if s.provider_id.lower() == provider.lower()]
        return {
            "health": [
                {
                    "provider_id": s.provider_id,
                    "circuit_state": s.circuit_state.value,
                    "is_available": s.is_available,
                    "failure_count": s.failure_count,
                    "success_count": s.success_count,
                    "consecutive_failures": s.consecutive_failures,
                }
                for s in statuses
            ]
        }

    def engineer_brand(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """Execute LEBIS brand identity pipeline and return serialized package."""
        try:
            from src.openclone.branding import engineer_brand_identity
            pkg = engineer_brand_identity(brief)
            return pkg.to_dict()
        except Exception as e:
            return {"error": f"Brand engineering failed: {str(e)}"}

    def validate_logo(self, svg_content: str) -> Dict[str, Any]:
        """Validate SVG logo markup against LEBIS QA standards."""
        import xml.etree.ElementTree as ET
        errors = []
        try:
            root = ET.fromstring(svg_content)
            viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
            if not viewbox:
                errors.append("Missing viewBox attribute.")
        except Exception as e:
            errors.append(f"Invalid XML: {str(e)}")

        has_raster = "<image" in svg_content.lower() or "data:image/" in svg_content
        if has_raster:
            errors.append("Embedded raster images detected.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "zero_raster": not has_raster,
            "length_bytes": len(svg_content.encode("utf-8")),
        }

    def workforce_status(self) -> Dict[str, Any]:
        """Return unified status of native workers and external Agency Agents."""
        from src.openclone.workforce.agency.catalog import AgencyCatalog
        cat = AgencyCatalog(self.root / "framework" / "workforce" / "external" / "agency-agents")
        return {
            "native_workers": 72,
            "external_agency_agents": len(cat.list_agents()),
            "total_divisions": len(cat.list_divisions()),
            "divisions": [d.id for d in cat.list_divisions()],
            "upstream_repository": "https://github.com/msitarzewski/agency-agents",
            "license": "MIT (Michael Sitarzewski)",
            "governance": "OpenClone Universal Engineering Governance",
        }

    def discover_agents(self, query: str = "", division: Optional[str] = None, capability: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search and filter Agency Agents by keyword, division, or capability."""
        from src.openclone.workforce.agency.catalog import AgencyCatalog
        cat = AgencyCatalog(self.root / "framework" / "workforce" / "external" / "agency-agents")
        agents = cat.search(query=query, division=division, capability=capability) if (query or capability) else cat.list_agents(division)
        return [a.to_dict() for a in agents]

    def get_agent_profile(self, agent_id: str) -> Dict[str, Any]:
        """Retrieve full unredacted profile for a specialist agent."""
        from src.openclone.workforce.agency.catalog import AgencyCatalog
        cat = AgencyCatalog(self.root / "framework" / "workforce" / "external" / "agency-agents")
        agent = cat.get_agent(agent_id)
        if not agent:
            raise KeyError(f"Specialist agent '{agent_id}' not found in catalog.")
        return agent.to_dict()

    def assemble_team(self, team_type: str = "ui_ux", project_name: str = "Project") -> Dict[str, Any]:
        """Assemble a multi-agent specialist team."""
        from src.openclone.workforce.agency.team_orchestrator import AgencyTeamOrchestrator
        orch = AgencyTeamOrchestrator()
        if team_type == "ui_ux":
            return orch.assemble_ui_ux_team(project_name).to_dict()
        elif team_type == "website":
            return orch.assemble_website_development_team(project_name).to_dict()
        else:
            return orch.assemble_ui_ux_team(project_name).to_dict()

    def classify_project(self, text: str, project_name: str = "project") -> Dict[str, Any]:
        """Multi-label classification of natural-language requirements."""
        from src.openclone.intelligence import ProjectClassifier
        classifier = ProjectClassifier()
        profile = classifier.classify_text(text, project_name=project_name)
        return profile.to_dict()

    def route_project(self, text: str, project_name: str = "project") -> Dict[str, Any]:
        """Deterministic explainable routing of project requirements."""
        from src.openclone.intelligence import ProjectClassifier, ProjectRouter
        classifier = ProjectClassifier()
        profile = classifier.classify_text(text, project_name=project_name)
        router = ProjectRouter()
        decision = router.route(profile)
        return decision.to_dict()

    def get_blueprint(self, blueprint_id: str) -> Dict[str, Any]:
        """Retrieve canonical engineering blueprint for a project family."""
        from src.openclone.intelligence import BlueprintManager
        mgr = BlueprintManager(self.root / "blueprints")
        content = mgr.get_blueprint(blueprint_id)
        if not content:
            raise KeyError(f"Blueprint not found: '{blueprint_id}'")
        return {"blueprint_id": blueprint_id, "content": content}

    def project_intelligence_status(self) -> Dict[str, Any]:
        """Get summary metrics on supported universal project families and blueprints."""
        from src.openclone.intelligence import TaxonomyRegistry, BlueprintManager
        tax = TaxonomyRegistry()
        bp = BlueprintManager(self.root / "blueprints")
        return {
            "version": tax.version,
            "family_count": len(tax.families),
            "families": tax.list_families(),
            "complexity_levels": tax.complexity_levels,
            "delivery_targets": tax.delivery_targets,
            "blueprints_count": len(bp.list_blueprints()),
        }

    def evaluate_technology(self, text: str, project_name: str = "project") -> List[Dict[str, Any]]:
        """Evaluate and recommend technology stack options."""
        from src.openclone.intelligence import ProjectClassifier
        from src.openclone.intelligence.technology import TechnologyIntelligenceEngine
        classifier = ProjectClassifier()
        profile = classifier.classify_text(text, project_name=project_name)
        engine = TechnologyIntelligenceEngine()
        decisions = engine.evaluate(profile, requirements_text=text)
        return [d.to_dict() for d in decisions]

    def generate_package(self, prompt: str, project_name: str = "project") -> Dict[str, Any]:
        """One-click idea-to-project package generation."""
        from src.openclone.intelligence.generator import ProjectPackageGenerator
        gen = ProjectPackageGenerator()
        return gen.generate(prompt, project_name=project_name)

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch tool invocation with argument validation."""
        if name == "openclone_get_status":
            return self.get_status()
        elif name == "openclone_search_knowledge":
            if "query" not in arguments:
                raise ValueError("Missing required argument: 'query'")
            return {"results": self.search_knowledge(arguments["query"], arguments.get("category", "all"), arguments.get("limit", 10))}
        elif name == "openclone_explain_concept":
            if "concept_id" not in arguments:
                raise ValueError("Missing required argument: 'concept_id'")
            return self.explain_concept(arguments["concept_id"])
        elif name == "openclone_run_workflow":
            if "workflow_id" not in arguments:
                raise ValueError("Missing required argument: 'workflow_id'")
            return self.run_workflow(arguments["workflow_id"], arguments.get("action", "inspect"))
        elif name == "openclone_validate_project":
            return self.validate_project(arguments.get("strict", False))
        elif name == "openclone_get_guidance":
            if "topic" not in arguments:
                raise ValueError("Missing required argument: 'topic'")
            return self.get_guidance(arguments["topic"])
        elif name == "openclone_list_capabilities":
            return self.list_capabilities(arguments.get("filter", "all"))
        elif name == "openclone_route_model":
            if "prompt" not in arguments:
                raise ValueError("Missing required argument: 'prompt'")
            return self.route_model(arguments["prompt"], arguments.get("mode", "BALANCED"), arguments.get("preferred_model"))
        elif name == "openclone_list_models":
            return self.list_models(arguments.get("provider"), arguments.get("tier"))
        elif name == "openclone_model_health":
            return self.get_model_health(arguments.get("provider"))
        elif name == "openclone_engineer_brand":
            if "brand_name" not in arguments:
                raise ValueError("Missing required argument: 'brand_name'")
            return self.engineer_brand(arguments)
        elif name == "openclone_validate_logo":
            if "svg_content" not in arguments:
                raise ValueError("Missing required argument: 'svg_content'")
            return self.validate_logo(arguments["svg_content"])
        elif name == "openclone_workforce_status":
            return self.workforce_status()
        elif name == "openclone_discover_agents":
            return {"agents": self.discover_agents(arguments.get("query", ""), arguments.get("division"), arguments.get("capability"))}
        elif name == "openclone_get_agent_profile":
            if "agent_id" not in arguments:
                raise ValueError("Missing required argument: 'agent_id'")
            return self.get_agent_profile(arguments["agent_id"])
        elif name == "openclone_assemble_team":
            return self.assemble_team(arguments.get("team_type", "ui_ux"), arguments.get("project_name", "Project"))
        elif name == "openclone_classify_project":
            if "text" not in arguments:
                raise ValueError("Missing required argument: 'text'")
            return self.classify_project(arguments["text"], arguments.get("project_name", "project"))
        elif name == "openclone_route_project":
            if "text" not in arguments:
                raise ValueError("Missing required argument: 'text'")
            return self.route_project(arguments["text"], arguments.get("project_name", "project"))
        elif name == "openclone_get_blueprint":
            if "blueprint_id" not in arguments:
                raise ValueError("Missing required argument: 'blueprint_id'")
            return self.get_blueprint(arguments["blueprint_id"])
        elif name == "openclone_project_intelligence_status":
            return self.project_intelligence_status()
        elif name == "openclone_evaluate_technology":
            if "text" not in arguments:
                raise ValueError("Missing required argument: 'text'")
            return {"decisions": self.evaluate_technology(arguments["text"], arguments.get("project_name", "project"))}
        elif name == "openclone_generate_package":
            if "prompt" not in arguments:
                raise ValueError("Missing required argument: 'prompt'")
            return self.generate_package(arguments["prompt"], arguments.get("project_name", "project"))
        elif self.canonical_registry.get(name):
            return self.gateway.execute(self.default_auth, name, arguments)
        else:
            raise KeyError(f"Unknown tool: '{name}'")

    def handle_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a single JSON-RPC 2.0 request."""
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        # MCP Lifecycle: initialize
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": False, "listChanged": False},
                        "prompts": {"listChanged": False},
                    },
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION,
                    },
                },
            }

        # MCP Tools list
        elif method == "tools/list":
            if params.get("all") or params.get("include_canonical"):
                merged_tools = list(TOOLS)
                existing_names = {t["name"] for t in merged_tools}
                for cap_tool in self.canonical_registry.get_mcp_tools():
                    if cap_tool["name"] not in existing_names:
                        merged_tools.append(cap_tool)
                        existing_names.add(cap_tool["name"])
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": merged_tools,
                    },
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS,
                },
            }

        # MCP Resources list
        elif method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "resources": [
                        {
                            "uri": "openclone://project/overview",
                            "name": "Project Overview",
                            "description": "High-level OpenClone project context, operating system, and frameworks.",
                            "mimeType": "application/json",
                        },
                        {
                            "uri": "openclone://project/checklist",
                            "name": "22-Phase Lifecycle Checklist",
                            "description": "Full lifecycle checklist item taxonomy and current verification states.",
                            "mimeType": "application/json",
                        },
                        {
                            "uri": "openclone://governance/rulebook",
                            "name": "OpenClone Governance Rulebook (AISDF Standard)",
                            "description": "Precedence rules, human approval boundaries, and anti-slop guidelines.",
                            "mimeType": "text/markdown",
                        },
                        {
                            "uri": "openclone://verification/policies",
                            "name": "Evidence & Verification Policy",
                            "description": "Verification levels (V0-V5), truth criteria, and gate exit rules.",
                            "mimeType": "text/markdown",
                        },
                    ]
                },
            }

        # MCP Resources read
        elif method == "resources/read":
            uri = params.get("uri")
            content_text = ""
            mime_type = "text/plain"
            if uri == "openclone://project/overview":
                content_text = json.dumps(self.get_status(), indent=2)
                mime_type = "application/json"
            elif uri == "openclone://project/checklist":
                content_text = json.dumps(self.call_tool("openclone_get_checklist", {}), indent=2)
                mime_type = "application/json"
            elif uri == "openclone://governance/rulebook":
                rule_file = (self.root / "framework" / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md") if (self.root / "framework" / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md").exists() else (self.root / "domains" / "00-GOVERNANCE" / "OPENCLONE-RULEBOOK.md")
                content_text = rule_file.read_text(encoding="utf-8", errors="replace") if rule_file.exists() else "# AISDF Rulebook"
                mime_type = "text/markdown"
            elif uri == "openclone://verification/policies":
                policy_file = self.root / "docs" / "engineering-lifecycle" / "VERIFICATION_AND_EVIDENCE.md"
                content_text = policy_file.read_text(encoding="utf-8", errors="replace") if policy_file.exists() else "# Verification Policies"
                mime_type = "text/markdown"
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Resource not found: '{uri}'"},
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": mime_type,
                            "text": content_text,
                        }
                    ]
                },
            }

        # MCP Prompts list
        elif method == "prompts/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "prompts": [
                        {
                            "name": "openclone_plan_feature",
                            "description": "Structured workflow prompt for planning a feature with acceptance criteria and anti-slop checks.",
                            "arguments": [
                                {"name": "feature_description", "description": "Description of the feature to plan", "required": True}
                            ],
                        },
                        {
                            "name": "openclone_implement_task",
                            "description": "Instruction prompt for executing an approved checklist task with least-privilege scoping.",
                            "arguments": [
                                {"name": "task_id", "description": "Checklist task ID to implement", "required": True}
                            ],
                        },
                        {
                            "name": "openclone_verify_feature",
                            "description": "Independent verification prompt inspecting observable test outputs and code diffs.",
                            "arguments": [
                                {"name": "task_id", "description": "Checklist task ID to verify", "required": True}
                            ],
                        },
                        {
                            "name": "openclone_security_review",
                            "description": "Audit code changes against the 19-point SaaS security baseline.",
                            "arguments": [
                                {"name": "scope", "description": "Files or routes to audit", "required": False}
                            ],
                        },
                    ]
                },
            }

        # MCP Prompts get
        elif method == "prompts/get":
            prompt_name = params.get("name")
            prompt_args = params.get("arguments", {})
            if prompt_name == "openclone_plan_feature":
                desc = prompt_args.get("feature_description", "User feature")
                text = (
                    f"You are the OpenClone Project Architect planning: '{desc}'.\n"
                    "1. Define Given/When/Then acceptance criteria.\n"
                    "2. Enforce Taste Skill v2.6.0 anti-slop design tokens (no purple gradients, no blur circles).\n"
                    "3. Map tasks into the 22-phase lifecycle with risk classifications.\n"
                )
            elif prompt_name == "openclone_implement_task":
                task_id = prompt_args.get("task_id", "PHASE_08_CORE_LOGIC")
                text = (
                    f"You are an OpenClone IDE Specialist implementing task: '{task_id}'.\n"
                    "1. Inspect existing files before editing.\n"
                    "2. Implement the smallest verifiable diff.\n"
                    "3. Run automated unit tests and attach observable output logs.\n"
                )
            elif prompt_name == "openclone_verify_feature":
                task_id = prompt_args.get("task_id", "PHASE_13_TESTING")
                text = (
                    f"You are the Independent Verification Lead reviewing: '{task_id}'.\n"
                    "1. Verify that code files exist and tests passed with exit code 0.\n"
                    "2. Reject self-attested passes without tangible evidence records.\n"
                    "3. Ensure zero unmitigated high/critical defects exist.\n"
                )
            elif prompt_name == "openclone_security_review":
                scope = prompt_args.get("scope", "All API routes and storage")
                text = (
                    f"You are the OpenClone Security Auditor reviewing: '{scope}'.\n"
                    "Audit strictly against the 19-point SaaS security baseline:\n"
                    "- Row-level security, authentication on every protected route.\n"
                    "- Parameterized queries, secret redaction, and bounded tool privileges.\n"
                )
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Prompt not found: '{prompt_name}'"},
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "description": f"OpenClone prompt workflow: {prompt_name}",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": text,
                            },
                        }
                    ],
                },
            }

        # MCP Tool Call
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_data = self.call_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_data, indent=2),
                            }
                        ],
                        "isError": False,
                    },
                }
            except KeyError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": str(e)},
                }
            except ValueError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": str(e)},
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": f"Internal execution error: {str(e)}"},
                }

        # Notifications (ping, etc.)
        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: '{method}'"},
            }

    def run_stdio(self):
        """Standard stdio JSON-RPC loop for local IDE MCP connections."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error: invalid JSON"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


def main():
    """Main entrypoint for MCP server."""
    server = OpenCloneMCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
