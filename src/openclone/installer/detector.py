"""Host detection subsystem for OpenClone Global Plugin."""

from dataclasses import dataclass, field
from pathlib import Path
import os
import shutil
from typing import Dict, List, Optional


@dataclass
class HostDetectionResult:
    """Detection findings for a candidate AI coding host."""
    host_id: str
    display_name: str
    detected: bool
    confidence: float  # 0.0 to 1.0
    cli_found: bool = False
    cli_path: Optional[str] = None
    user_config_path: Optional[str] = None
    workspace_marker_found: bool = False
    supported_scopes: List[str] = field(default_factory=lambda: ["workspace"])
    recommended_scope: str = "workspace"
    notes: str = ""


def get_user_home() -> Path:
    """Resolve cross-platform user home directory."""
    return Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or Path.home()).resolve()


def detect_hosts(workspace_root: Optional[Path] = None) -> Dict[str, HostDetectionResult]:
    """Detect presence and configuration locations of supported AI hosts."""
    root = (workspace_root or Path.cwd()).resolve()
    home = get_user_home()
    results: Dict[str, HostDetectionResult] = {}

    # 1. Google Antigravity
    agy_cli = shutil.which("agy")
    agy_user_dirs = [
        home / ".gemini" / "antigravity",
        home / "AppData" / "Local" / "Google" / "Antigravity",
        home / ".config" / "antigravity",
    ]
    agy_user_dir = next((str(p) for p in agy_user_dirs if p.exists()), None)
    agy_ws_marker = (root / ".agents").exists() or (root / "plugin.json").exists()

    agy_detected = bool(agy_cli or agy_user_dir or agy_ws_marker)
    agy_confidence = 0.0
    if agy_cli:
        agy_confidence += 0.5
    if agy_user_dir:
        agy_confidence += 0.3
    if agy_ws_marker:
        agy_confidence += 0.2

    results["antigravity"] = HostDetectionResult(
        host_id="antigravity",
        display_name="Google Antigravity",
        detected=agy_detected,
        confidence=min(1.0, agy_confidence),
        cli_found=bool(agy_cli),
        cli_path=agy_cli,
        user_config_path=agy_user_dir,
        workspace_marker_found=agy_ws_marker,
        supported_scopes=["user", "workspace"],
        recommended_scope="user" if agy_cli else "workspace",
        notes="Supports direct GitHub plugin installation via 'agy plugin install <URL>' and workspace rules.",
    )

    # 2. Claude Code
    claude_cli = shutil.which("claude")
    claude_user_dir = home / ".claude"
    claude_user_path = str(claude_user_dir) if claude_user_dir.exists() else None
    claude_ws_marker = (root / ".claude").exists() or (root / "CLAUDE.md").exists() or (root / ".mcp.json").exists()

    claude_detected = bool(claude_cli or claude_user_path or claude_ws_marker)
    claude_confidence = 0.0
    if claude_cli:
        claude_confidence += 0.5
    if claude_user_path:
        claude_confidence += 0.3
    if claude_ws_marker:
        claude_confidence += 0.2

    results["claude_code"] = HostDetectionResult(
        host_id="claude_code",
        display_name="Claude Code",
        detected=claude_detected,
        confidence=min(1.0, claude_confidence),
        cli_found=bool(claude_cli),
        cli_path=claude_cli,
        user_config_path=claude_user_path,
        workspace_marker_found=claude_ws_marker,
        supported_scopes=["user", "workspace"],
        recommended_scope="workspace",
        notes="Supports marketplace plugin installation and workspace .claude/ skills + .mcp.json.",
    )

    # 3. OpenAI Codex
    codex_cli = shutil.which("codex")
    codex_user_dir = home / ".codex"
    codex_user_path = str(codex_user_dir) if codex_user_dir.exists() else None
    codex_ws_marker = (root / ".codex").exists() or (root / "mcp.json").exists()

    codex_detected = bool(codex_cli or codex_user_path or codex_ws_marker)
    codex_confidence = 0.0
    if codex_cli:
        codex_confidence += 0.5
    if codex_user_path:
        codex_confidence += 0.3
    if codex_ws_marker:
        codex_confidence += 0.2

    results["codex"] = HostDetectionResult(
        host_id="codex",
        display_name="OpenAI Codex",
        detected=codex_detected,
        confidence=min(1.0, codex_confidence),
        cli_found=bool(codex_cli),
        cli_path=codex_cli,
        user_config_path=codex_user_path,
        workspace_marker_found=codex_ws_marker,
        supported_scopes=["user", "workspace"],
        recommended_scope="workspace",
        notes="Supports plugin marketplace addition and workspace mcp.json integration.",
    )

    # 4. Cursor
    cursor_cli = shutil.which("cursor")
    cursor_user_dirs = [
        home / ".cursor",
        home / "AppData" / "Roaming" / "Cursor",
        home / "Library" / "Application Support" / "Cursor",
    ]
    cursor_user_dir = next((str(p) for p in cursor_user_dirs if p.exists()), None)
    cursor_ws_marker = (root / ".cursor").exists() or (root / ".cursorrules").exists()

    cursor_detected = bool(cursor_cli or cursor_user_dir or cursor_ws_marker)
    cursor_confidence = 0.0
    if cursor_cli:
        cursor_confidence += 0.5
    if cursor_user_dir:
        cursor_confidence += 0.3
    if cursor_ws_marker:
        cursor_confidence += 0.2

    results["cursor"] = HostDetectionResult(
        host_id="cursor",
        display_name="Cursor",
        detected=cursor_detected,
        confidence=min(1.0, cursor_confidence),
        cli_found=bool(cursor_cli),
        cli_path=cursor_cli,
        user_config_path=cursor_user_dir,
        workspace_marker_found=cursor_ws_marker,
        supported_scopes=["workspace"],
        recommended_scope="workspace",
        notes="Supports .cursor/rules/ and .cursor/mcp.json for workspace-level governance.",
    )

    # 5. Generic MCP Client
    results["generic_mcp"] = HostDetectionResult(
        host_id="generic_mcp",
        display_name="Generic MCP Client",
        detected=True,
        confidence=1.0,
        cli_found=True,
        cli_path=shutil.which("python") or "python",
        user_config_path=None,
        workspace_marker_found=False,
        supported_scopes=["workspace"],
        recommended_scope="workspace",
        notes="Standard stdio MCP server accessible via 'python -m src.openclone.mcp.server'.",
    )

    return results
