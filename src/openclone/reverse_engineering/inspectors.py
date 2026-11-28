"""Polyglot Domain Inspectors for Reverse Engineering."""
from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from src.openclone.reverse_engineering.models import (
    ApiEndpoint,
    DependencyItem,
    EntityModel,
    EvidenceRef,
    EvidenceType,
    SecurityFinding,
    SymbolInfo,
)


IGNORED_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "venv", ".venv", "env",
    "__pycache__", ".pytest_cache", ".aisdf", ".openclone", "dist", "build",
}

LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".sql": "sql",
    ".java": "java",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".html": "html",
    ".css": "css",
}


class RepositoryInspector:
    """Inspects filesystem tree, file counts, and languages under strict path confinement."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self) -> Dict[str, Any]:
        files_by_lang: Dict[str, int] = {}
        loc_by_lang: Dict[str, int] = {}
        total_files = 0
        total_loc = 0
        all_files: List[Path] = []

        if not self.root.exists() or not self.root.is_dir():
            return {
                "total_files": 0,
                "total_loc": 0,
                "languages": {},
                "files": [],
            }

        for p in self.root.rglob("*"):
            if not p.is_file():
                continue
            # Path confinement check
            try:
                resolved = p.resolve()
                if self.root not in resolved.parents and resolved != self.root:
                    continue
            except Exception:
                continue

            if any(part in IGNORED_DIRS for part in p.parts):
                continue

            total_files += 1
            all_files.append(p)
            ext = p.suffix.lower()
            lang = LANGUAGE_EXTENSIONS.get(ext, "other")
            files_by_lang[lang] = files_by_lang.get(lang, 0) + 1

            try:
                # File size safety threshold (skip files > 2MB for LOC count)
                if p.stat().st_size <= 2 * 1024 * 1024:
                    lines = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                    total_loc += lines
                    loc_by_lang[lang] = loc_by_lang.get(lang, 0) + lines
            except Exception:
                pass

        return {
            "total_files": total_files,
            "total_loc": total_loc,
            "languages": loc_by_lang,
            "files": all_files,
        }


class ManifestInspector:
    """Extracts direct dependencies across Python, Node.js, Rust, and Go ecosystems."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self) -> List[DependencyItem]:
        deps: List[DependencyItem] = []

        # 1. Python: pyproject.toml
        pyproject = self.root / "pyproject.toml"
        if pyproject.is_file():
            try:
                content = pyproject.read_text(encoding="utf-8")
                # Look for dependencies = [...]
                in_deps = False
                for line in content.splitlines():
                    trimmed = line.strip()
                    if trimmed.startswith("dependencies = ["):
                        in_deps = True
                        continue
                    if in_deps:
                        if trimmed.startswith("]"):
                            in_deps = False
                            continue
                        dep_str = trimmed.strip('",\'')
                        if dep_str and not dep_str.startswith("#"):
                            m = re.match(r"^([a-zA-Z0-9_\-\.]+)([<>=!~].*)?$", dep_str)
                            name = m.group(1) if m else dep_str
                            constraint = m.group(2) if m and m.group(2) else "*"
                            deps.append(DependencyItem(
                                name=name,
                                version_constraint=constraint,
                                ecosystem="python",
                                evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(pyproject.relative_to(self.root))),
                            ))
            except Exception:
                pass

        # 2. Python: requirements.txt
        reqs = self.root / "requirements.txt"
        if reqs.is_file():
            try:
                for line in reqs.read_text(encoding="utf-8").splitlines():
                    t = line.strip()
                    if t and not t.startswith("#") and not t.startswith("-"):
                        m = re.match(r"^([a-zA-Z0-9_\-\.]+)([<>=!~].*)?$", t)
                        name = m.group(1) if m else t
                        constraint = m.group(2) if m and m.group(2) else "*"
                        deps.append(DependencyItem(
                            name=name,
                            version_constraint=constraint,
                            ecosystem="python",
                            evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(reqs.relative_to(self.root))),
                        ))
            except Exception:
                pass

        # 3. Node.js: package.json
        pkg_json = self.root / "package.json"
        if pkg_json.is_file():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                for k, v in data.get("dependencies", {}).items():
                    deps.append(DependencyItem(
                        name=k,
                        version_constraint=str(v),
                        ecosystem="npm",
                        is_dev=False,
                        evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(pkg_json.relative_to(self.root))),
                    ))
                for k, v in data.get("devDependencies", {}).items():
                    deps.append(DependencyItem(
                        name=k,
                        version_constraint=str(v),
                        ecosystem="npm",
                        is_dev=True,
                        evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(pkg_json.relative_to(self.root))),
                    ))
            except Exception:
                pass

        # 4. Rust: Cargo.toml
        cargo = self.root / "Cargo.toml"
        if cargo.is_file():
            try:
                in_deps = False
                for line in cargo.read_text(encoding="utf-8").splitlines():
                    t = line.strip()
                    if t.startswith("[dependencies]"):
                        in_deps = True
                        continue
                    if t.startswith("[") and in_deps:
                        in_deps = False
                    if in_deps and "=" in t:
                        parts = t.split("=", 1)
                        deps.append(DependencyItem(
                            name=parts[0].strip(),
                            version_constraint=parts[1].strip().strip('"\''),
                            ecosystem="cargo",
                            evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(cargo.relative_to(self.root))),
                        ))
            except Exception:
                pass

        # 5. Go: go.mod
        go_mod = self.root / "go.mod"
        if go_mod.is_file():
            try:
                in_require = False
                for line in go_mod.read_text(encoding="utf-8").splitlines():
                    t = line.strip()
                    if t.startswith("require ("):
                        in_require = True
                        continue
                    if in_require and t.startswith(")"):
                        in_require = False
                        continue
                    if (in_require and t and not t.startswith("//")) or t.startswith("require "):
                        clean = t.replace("require", "").strip()
                        parts = clean.split()
                        if len(parts) >= 2:
                            deps.append(DependencyItem(
                                name=parts[0],
                                version_constraint=parts[1],
                                ecosystem="go",
                                evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(go_mod.relative_to(self.root))),
                            ))
            except Exception:
                pass

        # 6. Java: pom.xml
        pom = self.root / "pom.xml"
        if pom.is_file():
            try:
                import xml.etree.ElementTree as ET
                tree = ET.fromstring(pom.read_text(encoding="utf-8"))
                ns = ""
                if tree.tag.startswith("{"):
                    ns = tree.tag.split("}")[0] + "}"
                for dep in tree.findall(f".//{ns}dependency"):
                    gid = dep.find(f"{ns}groupId")
                    aid = dep.find(f"{ns}artifactId")
                    ver = dep.find(f"{ns}version")
                    if aid is not None and aid.text:
                        name = f"{gid.text}:{aid.text}" if gid is not None and gid.text else aid.text
                        constraint = ver.text if ver is not None and ver.text else "*"
                        deps.append(DependencyItem(
                            name=name,
                            version_constraint=constraint,
                            ecosystem="maven",
                            evidence=EvidenceRef(EvidenceType.DEPENDENCY_MANIFEST, str(pom.relative_to(self.root))),
                        ))
            except Exception:
                pass

        return deps


class AstInspector:
    """Performs deep AST symbol extraction and cyclomatic complexity analysis."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self, files: List[Path]) -> List[SymbolInfo]:
        symbols: List[SymbolInfo] = []

        for p in files:
            rel_path = str(p.relative_to(self.root).as_posix()) if self.root in p.parents else p.name
            ext = p.suffix.lower()

            if ext == ".py":
                symbols.extend(self._parse_python(p, rel_path))
            elif ext in (".js", ".jsx", ".ts", ".tsx"):
                symbols.extend(self._parse_javascript_typescript(p, rel_path))

        return symbols

    def _parse_python(self, p: Path, rel_path: str) -> List[SymbolInfo]:
        results: List[SymbolInfo] = []
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content, filename=str(p))

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Compute function complexity
                    complexity = 1
                    for sub in ast.walk(node):
                        if isinstance(sub, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                            complexity += 1
                    params = [a.arg for a in node.args.args]
                    doc = ast.get_docstring(node)
                    results.append(SymbolInfo(
                        name=node.name,
                        symbol_type="function",
                        path=rel_path,
                        line_start=node.lineno,
                        line_end=getattr(node, "end_lineno", node.lineno),
                        complexity=complexity,
                        parameters=params,
                        docstring=doc,
                    ))
                elif isinstance(node, ast.ClassDef):
                    results.append(SymbolInfo(
                        name=node.name,
                        symbol_type="class",
                        path=rel_path,
                        line_start=node.lineno,
                        line_end=getattr(node, "end_lineno", node.lineno),
                        complexity=1,
                        parameters=[getattr(b, "id", "") for b in node.bases if hasattr(b, "id")],
                        docstring=ast.get_docstring(node),
                    ))
        except Exception:
            pass
        return results

    def _parse_javascript_typescript(self, p: Path, rel_path: str) -> List[SymbolInfo]:
        results: List[SymbolInfo] = []
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            for i, line in enumerate(lines, 1):
                t = line.strip()
                # Class detection
                class_m = re.match(r"^(?:export\s+)?class\s+([A-Za-z0-9_]+)", t)
                if class_m:
                    results.append(SymbolInfo(
                        name=class_m.group(1),
                        symbol_type="class",
                        path=rel_path,
                        line_start=i,
                        line_end=i,
                    ))
                # Function detection
                fn_m = re.match(r"^(?:export\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\((.*?)\)", t)
                if fn_m:
                    results.append(SymbolInfo(
                        name=fn_m.group(1),
                        symbol_type="function",
                        path=rel_path,
                        line_start=i,
                        line_end=i,
                        parameters=[x.strip() for x in fn_m.group(2).split(",") if x.strip()],
                    ))
        except Exception:
            pass
        return results


class DataModelInspector:
    """Discovers database schemas from SQL DDL and ORM definitions."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self, files: List[Path]) -> List[EntityModel]:
        entities: List[EntityModel] = []

        for p in files:
            rel = str(p.relative_to(self.root).as_posix()) if self.root in p.parents else p.name
            ext = p.suffix.lower()

            # 1. SQL DDL files
            if ext == ".sql":
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    matches = re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_\.\"]+)\s*\((.*?)\);", content, re.IGNORECASE | re.DOTALL)
                    for m in matches:
                        t_name = m.group(1).replace('"', '').split('.')[-1]
                        body = m.group(2)
                        cols = []
                        fks = []
                        pk = None
                        for col_def in body.split(","):
                            clean_col = col_def.strip()
                            if clean_col and not clean_col.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "INDEX")):
                                col_name = clean_col.split()[0].replace('"', '')
                                cols.append(col_name)
                                if "PRIMARY KEY" in clean_col.upper():
                                    pk = col_name
                        # Extract foreign keys
                        fk_matches = re.finditer(r"FOREIGN\s+KEY\s*\(\s*([a-zA-Z0-9_\"]+)\s*\)\s*REFERENCES\s+([a-zA-Z0-9_\"]+)\s*\(\s*([a-zA-Z0-9_\"]+)\s*\)", body, re.IGNORECASE)
                        for fkm in fk_matches:
                            fks.append({
                                "column": fkm.group(1).replace('"', ''),
                                "target_table": fkm.group(2).replace('"', ''),
                                "target_column": fkm.group(3).replace('"', ''),
                            })
                        entities.append(EntityModel(
                            name=t_name,
                            columns=cols,
                            primary_key=pk,
                            foreign_keys=fks,
                            relationships=fks,
                            source_path=rel,
                            orm_type="raw_sql",
                        ))
                except Exception:
                    pass

            # 2. Python ORM: SQLAlchemy / Django
            elif ext == ".py":
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    if "Base" in content or "models.Model" in content:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                base_names = [getattr(b, "id", getattr(b, "attr", "")) for b in node.bases]
                                if any(b in ("Base", "Model", "DeclarativeBase") for b in base_names):
                                    cols = []
                                    fks = []
                                    pk = None
                                    for item in node.body:
                                        if isinstance(item, ast.Assign):
                                            for target in item.targets:
                                                if isinstance(target, ast.Name):
                                                    cols.append(target.id)
                                                    unparsed = ast.unparse(item.value)
                                                    if "primary_key=True" in unparsed:
                                                        pk = target.id
                                                    if "ForeignKey(" in unparsed:
                                                        fk_m = re.search(r"ForeignKey\(['\"]([^'\"]+)['\"]\)", unparsed)
                                                        if fk_m:
                                                            parts = fk_m.group(1).split(".")
                                                            fks.append({
                                                                "column": target.id,
                                                                "target_table": parts[0],
                                                                "target_column": parts[1] if len(parts) > 1 else "id",
                                                            })
                                    entities.append(EntityModel(
                                        name=node.name,
                                        columns=cols,
                                        primary_key=pk,
                                        foreign_keys=fks,
                                        relationships=fks,
                                        source_path=rel,
                                        orm_type="sqlalchemy/django",
                                    ))
                except Exception:
                    pass

        return entities


class ApiRouteInspector:
    """Discovers REST endpoints from web frameworks (FastAPI, Flask, Express)."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self, files: List[Path]) -> List[ApiEndpoint]:
        endpoints: List[ApiEndpoint] = []

        for p in files:
            rel = str(p.relative_to(self.root).as_posix()) if self.root in p.parents else p.name
            ext = p.suffix.lower()

            if ext == ".py":
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    # FastAPI / Flask decorator pattern: @app.get("/path") or @router.post("/path")
                    pattern = re.compile(r"@(?:app|router|blueprint)\.(get|post|put|delete|patch|options)\s*\(\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
                    lines = content.splitlines()
                    for i, line in enumerate(lines, 1):
                        m = pattern.search(line)
                        if m:
                            verb = m.group(1).upper()
                            route = m.group(2)
                            # Peek next lines for def name
                            handler = "anonymous"
                            for j in range(i, min(i + 5, len(lines))):
                                fn_m = re.match(r"^(?:async\s+)?def\s+([a-zA-Z0-9_]+)", lines[j].strip())
                                if fn_m:
                                    handler = fn_m.group(1)
                                    break
                            endpoints.append(ApiEndpoint(
                                method=verb,
                                path=route,
                                handler_name=handler,
                                line_number=i,
                                source_path=rel,
                            ))
                except Exception:
                    pass

            elif ext in (".js", ".ts"):
                try:
                    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                    # Express pattern: app.get('/path', handler) or router.post('/path', handler)
                    pattern = re.compile(r"(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
                    for i, line in enumerate(lines, 1):
                        m = pattern.search(line)
                        if m:
                            endpoints.append(ApiEndpoint(
                                method=m.group(1).upper(),
                                path=m.group(2),
                                handler_name="express_handler",
                                line_number=i,
                                source_path=rel,
                            ))
                except Exception:
                    pass

        return endpoints


class SecurityInspector:
    """Discovers hardcoded credentials and security vulnerabilities."""

    SECRET_PATTERNS = [
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
        (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub Personal Access Token"),
        (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "OpenAI Secret Key"),
        (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "Private Key Header"),
        (re.compile(r"(?i)\b(password|secret|token)\s*=\s*['\"][A-Za-z0-9_@#$%^&*!-]{8,}['\"]"), "Hardcoded Secret String"),
    ]

    def __init__(self, root: Path):
        self.root = root.resolve()

    def inspect(self, files: List[Path]) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []
        finding_count = 1

        for p in files:
            rel = str(p.relative_to(self.root).as_posix()) if self.root in p.parents else p.name
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                for i, line in enumerate(lines, 1):
                    # Check for plaintext secrets
                    for pat, desc in self.SECRET_PATTERNS:
                        if pat.search(line):
                            findings.append(SecurityFinding(
                                finding_id=f"SEC-{finding_count:03d}",
                                severity="CRITICAL",
                                description=f"Confirmed Plaintext Secret: {desc}",
                                path=rel,
                                line=i,
                                is_confirmed_vulnerability=True,
                                evidence_type=EvidenceType.SOURCE_CODE_EVIDENCE,
                            ))
                            finding_count += 1
            except Exception:
                pass

        return findings
