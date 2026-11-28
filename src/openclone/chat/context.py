"""Project Context Intelligence Collector for OpenClone Runtime."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProjectContextCollector:
    """Extracts bounded, high-signal workspace intelligence to ground AI responses."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def gather_context(self) -> Dict[str, Any]:
        """Collect workspace structure, Git metrics, and detected technology stack."""
        ws = self.workspace_root
        context: Dict[str, Any] = {
            "workspace_path": str(ws),
            "workspace_name": ws.name,
            "git": self._gather_git_info(),
            "tech_stack": self._detect_tech_stack(),
            "has_openclone": (ws / "PROJECT.md").exists() or (ws / "openclone.py").exists(),
            "documentation_summary": self._collect_bounded_docs(),
        }
        return context

    def _gather_git_info(self) -> Dict[str, Any]:
        """Inspect Git repository state accurately."""
        ws = self.workspace_root
        info = {
            "is_git": False,
            "branch": "unknown",
            "commit": None,
            "clean": False,
            "tracked_count": 0,
            "modified_count": 0,
            "untracked_count": 0,
        }

        try:
            r_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ws, capture_output=True, text=True, timeout=5)
            if r_top.returncode == 0 and r_top.stdout.strip():
                info["is_git"] = True
                r_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ws, capture_output=True, text=True, timeout=5)
                b = r_branch.stdout.strip()
                if not b:
                    r_head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ws, capture_output=True, text=True, timeout=5)
                    b = f"detached-{r_head.stdout.strip()}" if r_head.returncode == 0 else "unknown"
                info["branch"] = b

                r_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ws, capture_output=True, text=True, timeout=5)
                if r_commit.returncode == 0:
                    info["commit"] = r_commit.stdout.strip()

                r_files = subprocess.run(["git", "ls-files"], cwd=ws, capture_output=True, text=True, timeout=10)
                if r_files.returncode == 0 and r_files.stdout.strip():
                    info["tracked_count"] = len(r_files.stdout.strip().splitlines())

                r_status = subprocess.run(["git", "status", "--porcelain"], cwd=ws, capture_output=True, text=True, timeout=5)
                if r_status.returncode == 0:
                    lines = [l.strip() for l in r_status.stdout.strip().splitlines() if l.strip()]
                    info["clean"] = len(lines) == 0
                    info["untracked_count"] = sum(1 for l in lines if l.startswith("??"))
                    info["modified_count"] = len(lines) - info["untracked_count"]
        except Exception:
            pass

        return info

    def _detect_tech_stack(self) -> List[str]:
        """Detect primary programming languages and frameworks in workspace."""
        ws = self.workspace_root
        stack = []

        if (ws / "pyproject.toml").exists() or (ws / "setup.py").exists() or (ws / "requirements.txt").exists():
            stack.append("Python")
        if (ws / "package.json").exists():
            stack.append("Node.js/TypeScript" if (ws / "tsconfig.json").exists() else "Node.js/JavaScript")
        if (ws / "pubspec.yaml").exists():
            stack.append("Flutter/Dart")
        if (ws / "go.mod").exists():
            stack.append("Go")
        if (ws / "Cargo.toml").exists():
            stack.append("Rust")
        if (ws / "pom.xml").exists() or (ws / "build.gradle").exists():
            stack.append("Java/JVM")

        return stack or ["Generic Software Project"]

    def _collect_bounded_docs(self, max_bytes: int = 3072) -> Dict[str, str]:
        """Read bounded excerpt of key project documentation without reading sensitive files."""
        ws = self.workspace_root
        docs = {}

        candidate_files = ["PROJECT.md", "README.md", "ARCHITECTURE.md"]
        for fname in candidate_files:
            fpath = ws / fname
            if fpath.exists() and fpath.is_file():
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")[:max_bytes]
                    docs[fname] = content
                except Exception:
                    pass

        return docs

    def format_system_prompt(self) -> str:
        """Produce a bounded, high-signal system instruction block."""
        ctx = self.gather_context()
        git_info = ctx["git"]
        git_summary = f"Git: branch '{git_info['branch']}', status {'clean' if git_info['clean'] else 'dirty'}, tracked files {git_info['tracked_count']}" if git_info["is_git"] else "Git: not initialized"

        doc_blocks = []
        for name, text in ctx["documentation_summary"].items():
            doc_blocks.append(f"--- Document: {name} ---\n{text[:1000]}...")

        docs_text = "\n".join(doc_blocks) if doc_blocks else "No primary project definition documents found."

        return f"""You are OpenClone, a senior autonomous AI software engineering assistant and control plane.
Product Identity: OpenClone — Universal AI Engineering Platform.
Tagline: Build with Any AI. Governed by One Engineering Standard.

Current Workspace Context:
- Path: {ctx['workspace_path']}
- Name: {ctx['workspace_name']}
- Stack: {', '.join(ctx['tech_stack'])}
- {git_summary}

Project Overview:
{docs_text}

Operating Standards:
1. Provide accurate, professional, senior-engineer guidance.
2. Separate discussion/planning from actual file modification.
3. Operating under Extension-First Universal AI Engineering Architecture:
   • Accessible via VS Code Extension and Antigravity Plugin.
   • Governed by deterministic quality gates and SHA-256 audit ledger evidence.
4. Never hallucinate test passes, fake verifications, or claim modifications happened unless verified.
"""
