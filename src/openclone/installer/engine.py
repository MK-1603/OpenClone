"""Installer transaction engine for OpenClone Global Plugin."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any, Dict, List, Optional

from src.openclone.installer.detector import detect_hosts, get_user_home, HostDetectionResult
from src.openclone.installer.manifest import InstallationManifest


SUPPORTED_HOSTS = {"antigravity", "claude_code", "codex", "cursor", "generic_mcp"}


class InstallerEngine:
    """Orchestrates safe, transactional installation, updates, and uninstallation."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.root = (repo_root or Path(__file__).resolve().parents[3]).resolve()
        self.core_version = "2.0.0"
        self.adapters_dir = self.root / "adapters"

    def _resolve_target_dir(self, target_dir: Optional[Path], scope: str) -> Path:
        """Resolve installation target directory according to scope."""
        if target_dir:
            return target_dir.resolve()
        if scope == "user":
            return get_user_home()
        return Path.cwd().resolve()

    def _check_containment(self, base: Path, target: Path) -> Path:
        """Ensure target path does not escape base directory boundary."""
        resolved = target.resolve()
        try:
            resolved.relative_to(base.resolve())
        except ValueError:
            raise PermissionError(f"Security boundary violation: Path '{target}' escapes '{base}'.")
        return resolved

    def get_adapter_files(self, host_id: str) -> Dict[str, str]:
        """Map canonical relative adapter files for a given host.
        
        Returns a dict of relative destination path -> source text or template.
        """
        files: Dict[str, str] = {}
        if host_id == "antigravity":
            src_rule = self.adapters_dir / "antigravity" / "workspace" / ".agents" / "rules" / "aisdf.md"
            src_skill = self.adapters_dir / "antigravity" / "workspace" / ".agents" / "skills" / "aisdf" / "SKILL.md"
            files[".agents/rules/aisdf.md"] = src_rule.read_text(encoding="utf-8") if src_rule.exists() else "# AISDF Antigravity Rule\n"
            files[".agents/skills/aisdf/SKILL.md"] = src_skill.read_text(encoding="utf-8") if src_skill.exists() else "# AISDF Skill\n"

        elif host_id == "claude_code":
            src_skill = self.adapters_dir / "claude-code" / ".claude" / "skills" / "aisdf" / "SKILL.md"
            files[".claude/skills/aisdf/SKILL.md"] = src_skill.read_text(encoding="utf-8") if src_skill.exists() else "# AISDF Claude Skill\n"
            files[".mcp.json"] = json.dumps({
                "mcpServers": {
                    "openclone": {
                        "command": "python",
                        "args": ["-m", "src.openclone.cli", "mcp"],
                    }
                }
            }, indent=2)

        elif host_id == "codex":
            src_skill = self.adapters_dir / "codex" / ".agents" / "skills" / "aisdf" / "SKILL.md"
            files[".agents/skills/aisdf/SKILL.md"] = src_skill.read_text(encoding="utf-8") if src_skill.exists() else "# AISDF Codex Skill\n"
            files["mcp.json"] = json.dumps({
                "mcpServers": {
                    "openclone": {
                        "command": "python",
                        "args": ["-m", "src.openclone.cli", "mcp"],
                    }
                }
            }, indent=2)

        elif host_id == "cursor":
            src_rule = self.adapters_dir / "cursor" / ".cursor" / "rules" / "aisdf.mdc"
            files[".cursor/rules/aisdf.mdc"] = src_rule.read_text(encoding="utf-8") if src_rule.exists() else "# AISDF Cursor Rule\n"
            files[".cursor/mcp.json"] = json.dumps({
                "mcpServers": {
                    "openclone": {
                        "command": "python",
                        "args": ["-m", "src.openclone.cli", "mcp"],
                    }
                }
            }, indent=2)

        elif host_id == "generic_mcp":
            files["mcp.json"] = json.dumps({
                "mcpServers": {
                    "openclone": {
                        "command": "python",
                        "args": ["-m", "src.openclone.cli", "mcp"],
                    }
                }
            }, indent=2)

        return files

    def install(
        self,
        host_id: str,
        scope: str = "workspace",
        target_dir: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Execute transactional installation of a native host adapter."""
        if host_id not in SUPPORTED_HOSTS:
            raise ValueError(f"Unsupported host '{host_id}'. Supported hosts: {', '.join(sorted(SUPPORTED_HOSTS))}")

        target_base = self._resolve_target_dir(target_dir, scope)
        files_to_install = self.get_adapter_files(host_id)

        if dry_run:
            return {
                "dry_run": True,
                "host_id": host_id,
                "scope": scope,
                "target_dir": str(target_base),
                "planned_files": list(files_to_install.keys()),
            }

        manifest = InstallationManifest.load(target_base)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_dir = target_base / ".openclone" / "backups" / host_id / timestamp

        installed_hashes: Dict[str, str] = {}
        backups: Dict[str, str] = {}
        staged_files: List[Path] = []

        try:
            for rel_path, content in files_to_install.items():
                dest = self._check_containment(target_base, target_base / rel_path)
                
                # If pre-existing, create safety backup
                if dest.exists():
                    bpath = backup_dir / rel_path
                    bpath.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dest, bpath)
                    backups[rel_path] = str(bpath.relative_to(target_base))

                # Stage and write new file
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                staged_files.append(dest)

                # Record hash
                h = hashlib.sha256(dest.read_bytes()).hexdigest()
                installed_hashes[rel_path] = h

            # Commit record to manifest
            manifest.record_install(host_id, scope, installed_hashes, backups)
            manifest.save(target_base)

            return {
                "success": True,
                "host_id": host_id,
                "scope": scope,
                "target_dir": str(target_base),
                "installed_files": list(installed_hashes.keys()),
                "backups_created": len(backups),
                "core_version": self.core_version,
            }

        except Exception as e:
            # Transactional Rollback
            for staged in staged_files:
                if staged.exists():
                    staged.unlink()
            for orig_rel, b_rel in backups.items():
                orig_path = target_base / orig_rel
                b_path = target_base / b_rel
                if b_path.exists():
                    orig_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(b_path, orig_path)
            raise RuntimeError(f"Installation failed for '{host_id}'; rolled back cleanly: {e}")

    def uninstall(
        self,
        host_id: str,
        target_dir: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Safely uninstall a host adapter, removing only OpenClone-owned files."""
        target_base = (target_dir or Path.cwd()).resolve()
        manifest = InstallationManifest.load(target_base)
        rec = manifest.hosts.get(host_id)

        if not rec:
            return {"success": False, "message": f"Host '{host_id}' is not installed in '{target_base}'."}

        if dry_run:
            return {
                "dry_run": True,
                "host_id": host_id,
                "target_dir": str(target_base),
                "files_to_remove": list(rec.installed_files.keys()),
                "backups_to_restore": list(rec.backups.keys()),
            }

        removed = []
        restored = []

        # 1. Remove tracked OpenClone files
        for rel in rec.installed_files.keys():
            dest = target_base / rel
            if dest.exists():
                dest.unlink()
                removed.append(rel)

        # 2. Restore pre-install backups if present
        for orig_rel, b_rel in rec.backups.items():
            orig_path = target_base / orig_rel
            b_path = target_base / b_rel
            if b_path.exists():
                orig_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(b_path, orig_path)
                restored.append(orig_rel)

        manifest.remove_host(host_id)
        manifest.save(target_base)

        return {
            "success": True,
            "host_id": host_id,
            "target_dir": str(target_base),
            "files_removed": removed,
            "backups_restored": restored,
        }

    def rollback(self, host_id: str, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Rollback to previous configuration state using recorded backups."""
        return self.uninstall(host_id, target_dir=target_dir)

    def update(self, host_id: str, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Re-install latest adapter version preserving user workspace."""
        target_base = (target_dir or Path.cwd()).resolve()
        manifest = InstallationManifest.load(target_base)
        scope = manifest.hosts.get(host_id).scope if host_id in manifest.hosts else "workspace"
        return self.install(host_id, scope=scope, target_dir=target_base)

    def status(self, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Report detected hosts and currently installed adapters with integrity checks."""
        target_base = (target_dir or Path.cwd()).resolve()
        detected = detect_hosts(target_base)
        manifest = InstallationManifest.load(target_base)

        installed_info: Dict[str, Any] = {}
        for hid in manifest.hosts.keys():
            integ = manifest.verify_integrity(target_base, hid)
            installed_info[hid] = {
                "scope": manifest.hosts[hid].scope,
                "installed_at": manifest.hosts[hid].installed_at,
                "version": manifest.hosts[hid].core_version,
                "integrity": integ,
            }

        return {
            "workspace_root": str(target_base),
            "core_version": self.core_version,
            "installed_adapters": installed_info,
            "detected_hosts": {
                hid: {
                    "name": res.display_name,
                    "detected": res.detected,
                    "confidence": res.confidence,
                    "cli_found": res.cli_found,
                    "recommended_scope": res.recommended_scope,
                }
                for hid, res in detected.items()
            },
        }

    def doctor(self, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Execute environmental diagnostics and print fix hints."""
        target_base = (target_dir or Path.cwd()).resolve()
        checks: List[Dict[str, Any]] = []

        # 1. Python version >= 3.10
        py_ok = sys.version_info >= (3, 10)
        checks.append({
            "name": "Python Version",
            "passed": py_ok,
            "detail": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "fix_hint": "Install Python 3.10 or higher.",
        })

        # 2. Git CLI
        git_cli = shutil.which("git")
        checks.append({
            "name": "Git Executable",
            "passed": bool(git_cli),
            "detail": git_cli or "Not found",
            "fix_hint": "Install git and ensure it is available in system PATH.",
        })

        # 3. Node.js (for Taste Skill governance tests)
        node_cli = shutil.which("node")
        checks.append({
            "name": "Node.js (Taste Skill Engine)",
            "passed": bool(node_cli),
            "detail": node_cli or "Optional (Node.js >= 18 recommended for Taste Skill)",
            "fix_hint": "Install Node.js 18+ to run Taste Skill visual anti-slop audits.",
        })

        # 4. Workspace Write Permissions
        test_write = target_base / ".openclone" / ".doctor_probe"
        write_ok = False
        try:
            test_write.parent.mkdir(parents=True, exist_ok=True)
            test_write.write_text("probe", encoding="utf-8")
            test_write.unlink()
            write_ok = True
        except Exception:
            write_ok = False

        checks.append({
            "name": "Workspace Write Access",
            "passed": write_ok,
            "detail": str(target_base),
            "fix_hint": "Ensure current user has write permissions in the workspace root.",
        })

        # 5. MCP Server Availability
        mcp_ok = (self.root / "src" / "openclone" / "mcp" / "server.py").exists()
        checks.append({
            "name": "OpenClone MCP Module",
            "passed": mcp_ok,
            "detail": "src/openclone/mcp/server.py",
            "fix_hint": "Ensure openclone repository core modules are intact.",
        })

        all_passed = all(c["passed"] for c in checks if c["name"] != "Node.js (Taste Skill Engine)")
        return {
            "all_healthy": all_passed,
            "checks": checks,
            "summary": f"{sum(1 for c in checks if c['passed'])}/{len(checks)} checks passed.",
        }
