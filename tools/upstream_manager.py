#!/usr/bin/env python3
"""
OpenClone Upstream Repository Manager & Audit Engine
Clones, verifies, audits, and registers the 27 upstream GitHub repositories.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List

REPO_ROOT = Path(__file__).resolve().parent.parent
DEV_UPSTREAM = REPO_ROOT / ".openclone-dev" / "upstream"

UPSTREAM_INVENTORY: List[Dict[str, Any]] = [
    # UI/UX & Frontend Design (11)
    {
        "id": "UI-001",
        "name": "design-md-chrome",
        "category": "ui-ux",
        "canonical_url": "https://github.com/bergside/design-md-chrome",
        "parent_url": "https://github.com/bergside/design-md-chrome",
        "subpath": "",
        "expected_type": ["DESIGN_SYSTEM", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-002",
        "name": "shadcn-ui",
        "category": "ui-ux",
        "canonical_url": "https://github.com/shadcn-ui/ui",
        "parent_url": "https://github.com/shadcn-ui/ui",
        "subpath": "",
        "expected_type": ["DESIGN_SYSTEM", "LIBRARY"],
    },
    {
        "id": "UI-003",
        "name": "interface-design",
        "category": "ui-ux",
        "canonical_url": "https://github.com/Dammyjay93/interface-design",
        "parent_url": "https://github.com/Dammyjay93/interface-design",
        "subpath": "",
        "expected_type": ["DESIGN_SYSTEM", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-004",
        "name": "Unstop-UI",
        "category": "ui-ux",
        "canonical_url": "https://github.com/Mohit-Raj-Singh/Unstop-UI",
        "parent_url": "https://github.com/Mohit-Raj-Singh/Unstop-UI",
        "subpath": "",
        "expected_type": ["DESIGN_SYSTEM", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-005",
        "name": "anthropic-frontend-design",
        "category": "ui-ux",
        "canonical_url": "https://github.com/anthropics/skills/tree/main/skills/frontend-design",
        "parent_url": "https://github.com/anthropics/skills",
        "subpath": "skills/frontend-design",
        "expected_type": ["SKILL_SOURCE", "DESIGN_SYSTEM"],
    },
    {
        "id": "UI-006",
        "name": "taste-skill",
        "category": "ui-ux",
        "canonical_url": "https://github.com/Leonxlnx/taste-skill",
        "parent_url": "https://github.com/Leonxlnx/taste-skill",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "DESIGN_SYSTEM"],
    },
    {
        "id": "UI-007",
        "name": "hallmark",
        "category": "ui-ux",
        "canonical_url": "https://github.com/nutlope/hallmark",
        "parent_url": "https://github.com/nutlope/hallmark",
        "subpath": "",
        "expected_type": ["DESIGN_SYSTEM", "APPLICATION"],
    },
    {
        "id": "UI-008",
        "name": "ui-ux-pro-max-skill",
        "category": "ui-ux",
        "canonical_url": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        "parent_url": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-009",
        "name": "frontend-design-skills",
        "category": "ui-ux",
        "canonical_url": "https://github.com/flitzrrr/frontend-design-skills",
        "parent_url": "https://github.com/flitzrrr/frontend-design-skills",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-010",
        "name": "impeccable",
        "category": "ui-ux",
        "canonical_url": "https://github.com/pbakaus/impeccable",
        "parent_url": "https://github.com/pbakaus/impeccable",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "UI-011",
        "name": "typography-skills",
        "category": "ui-ux",
        "canonical_url": "https://github.com/jpoindexter/typography-skills",
        "parent_url": "https://github.com/jpoindexter/typography-skills",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "DESIGN_SYSTEM"],
    },

    # Security & Vulnerability Engineering (12)
    {
        "id": "SEC-001",
        "name": "strix",
        "category": "security",
        "canonical_url": "https://github.com/usestrix/strix",
        "parent_url": "https://github.com/usestrix/strix",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "APPLICATION"],
    },
    {
        "id": "SEC-002",
        "name": "nuclei",
        "category": "security",
        "canonical_url": "https://github.com/projectdiscovery/nuclei",
        "parent_url": "https://github.com/projectdiscovery/nuclei",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-003",
        "name": "codex-security",
        "category": "security",
        "canonical_url": "https://github.com/openai/codex-security",
        "parent_url": "https://github.com/openai/codex-security",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "SEC-004",
        "name": "security-audit-skill",
        "category": "security",
        "canonical_url": "https://github.com/cloudflare/security-audit-skill",
        "parent_url": "https://github.com/cloudflare/security-audit-skill",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "SECURITY_SCANNER"],
    },
    {
        "id": "SEC-005",
        "name": "semgrep",
        "category": "security",
        "canonical_url": "https://github.com/semgrep/semgrep",
        "parent_url": "https://github.com/semgrep/semgrep",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-006",
        "name": "claude-code-security-review",
        "category": "security",
        "canonical_url": "https://github.com/anthropics/claude-code-security-review",
        "parent_url": "https://github.com/anthropics/claude-code-security-review",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "SECURITY_SCANNER"],
    },
    {
        "id": "SEC-007",
        "name": "trivy",
        "category": "security",
        "canonical_url": "https://github.com/aquasecurity/trivy",
        "parent_url": "https://github.com/aquasecurity/trivy",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-008",
        "name": "trufflehog",
        "category": "security",
        "canonical_url": "https://github.com/trufflesecurity/trufflehog",
        "parent_url": "https://github.com/trufflesecurity/trufflehog",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-009",
        "name": "skillspector",
        "category": "security",
        "canonical_url": "https://github.com/NVIDIA/skillspector",
        "parent_url": "https://github.com/NVIDIA/skillspector",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-010",
        "name": "clamav",
        "category": "security",
        "canonical_url": "https://github.com/Cisco-Talos/clamav",
        "parent_url": "https://github.com/Cisco-Talos/clamav",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "CLI_TOOL"],
    },
    {
        "id": "SEC-011",
        "name": "bla",
        "category": "security",
        "canonical_url": "https://github.com/qybaihe/bla",
        "parent_url": "https://github.com/qybaihe/bla",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "SEC-012",
        "name": "pyrit",
        "category": "security",
        "canonical_url": "https://github.com/microsoft/pyrit",
        "parent_url": "https://github.com/microsoft/pyrit",
        "subpath": "",
        "expected_type": ["SECURITY_SCANNER", "LIBRARY"],
    },

    # Software Development & Engineering (4)
    {
        "id": "ENG-001",
        "name": "hue",
        "category": "software-engineering",
        "canonical_url": "https://github.com/cloudera/hue",
        "parent_url": "https://github.com/cloudera/hue",
        "subpath": "",
        "expected_type": ["APPLICATION", "FRAMEWORK"],
    },
    {
        "id": "ENG-002",
        "name": "superpowers",
        "category": "software-engineering",
        "canonical_url": "https://github.com/obra/superpowers",
        "parent_url": "https://github.com/obra/superpowers",
        "subpath": "",
        "expected_type": ["SKILL_SOURCE", "CLI_TOOL"],
    },
    {
        "id": "ENG-003",
        "name": "improve",
        "category": "software-engineering",
        "canonical_url": "https://github.com/shadcn/improve",
        "parent_url": "https://github.com/shadcn/improve",
        "subpath": "",
        "expected_type": ["CLI_TOOL", "KNOWLEDGE_REFERENCE"],
    },
    {
        "id": "ENG-004",
        "name": "TokenEconomizer",
        "category": "software-engineering",
        "canonical_url": "https://github.com/microsoft/TokenEconomizer",
        "parent_url": "https://github.com/microsoft/TokenEconomizer",
        "subpath": "",
        "expected_type": ["LIBRARY", "KNOWLEDGE_REFERENCE"],
    },
]


def run_git_cmd(args: List[str], cwd: Path) -> str:
    res = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        return ""
    return res.stdout.strip()


def detect_license(checkout_path: Path) -> Dict[str, str]:
    candidates = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md", "LICENSE-MIT", "LICENSE-APACHE"]
    found_file = None
    for c in candidates:
        p = checkout_path / c
        if p.exists() and p.is_file():
            found_file = p
            break

    if not found_file:
        for f in checkout_path.glob("LICEN*"):
            if f.is_file():
                found_file = f
                break

    if not found_file:
        return {"spdx_id": "UNKNOWN", "file": "NONE", "status": "BLOCKED_LICENSE_REVIEW"}

    content = found_file.read_text(encoding="utf-8", errors="replace")
    spdx = "UNKNOWN"
    c_lower = content.lower()
    if "apache license" in c_lower and "version 2.0" in c_lower:
        spdx = "Apache-2.0"
    elif "mit license" in c_lower or "permission is hereby granted, free of charge" in c_lower:
        spdx = "MIT"
    elif "gnu general public license" in c_lower:
        if "version 3" in c_lower or "gplv3" in c_lower:
            spdx = "GPL-3.0"
        elif "version 2" in c_lower:
            spdx = "GPL-2.0"
        else:
            spdx = "GPL"
    elif "gnu lesser general public license" in c_lower:
        spdx = "LGPL-2.1"
    elif "affero general public license" in c_lower:
        spdx = "AGPL-3.0"
    elif "bsd" in c_lower and "clause" in c_lower:
        spdx = "BSD"
    elif "mozilla public license" in c_lower:
        spdx = "MPL-2.0"

    status = "REVIEWED" if spdx != "UNKNOWN" else "BLOCKED_LICENSE_REVIEW"
    return {"spdx_id": spdx, "file": found_file.name, "status": status}


def detect_tech_stack(checkout_path: Path) -> Dict[str, Any]:
    languages = []
    frameworks = []
    entry_points = []
    pkg_managers = []

    if (checkout_path / "package.json").exists():
        languages.append("JavaScript/TypeScript")
        pkg_managers.append("npm/pnpm/yarn")
        try:
            pj = json.loads((checkout_path / "package.json").read_text(encoding="utf-8", errors="ignore"))
            if "scripts" in pj:
                entry_points.extend(list(pj["scripts"].keys())[:5])
        except Exception:
            pass

    if (checkout_path / "pyproject.toml").exists() or (checkout_path / "requirements.txt").exists() or (checkout_path / "setup.py").exists():
        languages.append("Python")
        pkg_managers.append("pip/poetry/uv")

    if (checkout_path / "go.mod").exists():
        languages.append("Go")
        pkg_managers.append("go modules")

    if (checkout_path / "Cargo.toml").exists():
        languages.append("Rust")
        pkg_managers.append("cargo")

    if (checkout_path / "CMakeLists.txt").exists():
        languages.append("C/C++")
        pkg_managers.append("cmake")

    # Skills / Rules
    has_skills = len(list(checkout_path.glob("**/SKILL.md"))) > 0
    has_cursorrules = (checkout_path / ".cursorrules").exists()
    has_prompts = len(list(checkout_path.glob("**/prompt*.md"))) > 0

    return {
        "languages": list(set(languages)) if languages else ["Markdown/Other"],
        "package_managers": list(set(pkg_managers)) if pkg_managers else ["None"],
        "entry_points": entry_points,
        "has_skills": has_skills,
        "has_cursorrules": has_cursorrules,
        "has_prompts": has_prompts,
    }


def clone_or_inspect(entry: Dict[str, Any]) -> Dict[str, Any]:
    cat = entry["category"]
    eid = entry["id"]
    target_dir = DEV_UPSTREAM / cat / eid
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    parent_url = entry["parent_url"]
    is_cloned = target_dir.exists() and (target_dir / ".git").exists()

    clone_status = "CLONED"
    clone_error = ""

    if not is_cloned:
        print(f"[{eid}] Cloning {parent_url} into {target_dir}...")
        cmd = ["git", "clone", "--depth", "1", parent_url, str(target_dir)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            clone_status = "FAILED"
            clone_error = res.stderr.strip()
            print(f"[{eid}] FAILED: {clone_error}")
            return {
                **entry,
                "clone_status": clone_status,
                "clone_error": clone_error,
                "commit_sha": "NONE",
                "default_branch": "NONE",
                "commit_date": "NONE",
                "license": {"spdx_id": "UNKNOWN", "status": "BLOCKED"},
                "tech_stack": {},
            }

    # Inspect git details
    commit_sha = run_git_cmd(["rev-parse", "HEAD"], target_dir)
    default_branch = run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], target_dir)
    commit_date = run_git_cmd(["log", "-1", "--format=%cd", "--date=short"], target_dir)

    # Subpath handling (e.g. UI-005)
    audit_target = target_dir
    if entry.get("subpath"):
        audit_target = target_dir / entry["subpath"]
        if not audit_target.exists():
            audit_target = target_dir

    lic = detect_license(audit_target)
    tech = detect_tech_stack(audit_target)

    return {
        **entry,
        "clone_status": "CLONED",
        "clone_error": "",
        "commit_sha": commit_sha,
        "default_branch": default_branch,
        "commit_date": commit_date,
        "license": lic,
        "tech_stack": tech,
    }


def main():
    print(f"--- Starting Upstream Repositories Intake Audit (27 Repositories) ---")
    DEV_UPSTREAM.mkdir(parents=True, exist_ok=True)
    results = []

    for entry in UPSTREAM_INVENTORY:
        res = clone_or_inspect(entry)
        results.append(res)

    out_file = REPO_ROOT / ".openclone-dev" / "audit_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Intake completed. Results saved to {out_file}")


if __name__ == "__main__":
    main()
