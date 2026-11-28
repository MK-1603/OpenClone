"""Automated verification suite for OpenClone VS Code Extension and Gateway Integration."""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from src.openclone.integrations.rest import OpenCloneRESTGateway


def test_vscode_extension_manifest_structure():
    """Verify package.json contains all required VS Code contribution points."""
    manifest_path = Path("extensions/vscode/package.json")
    assert manifest_path.exists(), "extensions/vscode/package.json must exist"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["name"] == "openclone-vscode"
    assert manifest["version"] == "2.0.0"

    contributes = manifest.get("contributes", {})
    
    # 1. Activity Bar Container
    containers = contributes.get("viewsContainers", {}).get("activitybar", [])
    assert any(c["id"] in ["openclone-chat", "openclone-explorer"] for c in containers), "Must register openclone container"

    # 2. Webview Chat View
    views = contributes.get("views", {}).get("openclone-chat", []) or contributes.get("views", {}).get("openclone-explorer", [])
    assert any(v["id"] == "openclone.chatView" and v.get("type") == "webview" for v in views), \
        "Must register openclone.chatView webview"
    assert any(v["id"] == "openclone.statusView" for v in views), "Must register statusView"
    assert any(v["id"] == "openclone.planView" for v in views), "Must register planView"
    assert any(v["id"] == "openclone.workersView" for v in views), "Must register workersView"

    # 3. Context Menu Actions
    menus = contributes.get("menus", {}).get("editor/context", [])
    assert any(m["command"] == "openclone.explainSelection" for m in menus), "Must have explainSelection menu item"
    assert any(m["command"] == "openclone.debugSelection" for m in menus), "Must have debugSelection menu item"
    assert any(m["command"] == "openclone.refactorSelection" for m in menus), "Must have refactorSelection menu item"


def test_vscode_webview_assets_integrity():
    """Verify HTML, CSS, and JS assets for the Webview exist and have strict CSP."""
    html_provider_path = Path("extensions/vscode/src/chatViewProvider.js")
    css_path = Path("extensions/vscode/media/chatView.css")
    js_path = Path("extensions/vscode/media/chatView.js")

    assert html_provider_path.exists()
    assert css_path.exists()
    assert js_path.exists()

    provider_content = html_provider_path.read_text(encoding="utf-8")
    assert "Content-Security-Policy" in provider_content
    assert "nonce-" in provider_content
    assert "default-src 'none'" in provider_content

    css_content = css_path.read_text(encoding="utf-8")
    assert "#D4AF37" in css_content, "Must include restrained gold accent #D4AF37"
    assert "--oc-bg" in css_content


def test_gateway_chat_and_intelligence_endpoints():
    """Verify REST Gateway endpoints powering the extension."""
    gw = OpenCloneRESTGateway()

    # Health check
    health = gw.dispatch("GET", "/api/v1/health")
    assert health["status"] == "healthy"
    assert health["version"] == "2.0.0"

    # Models catalog (MIE)
    models = gw.dispatch("GET", "/api/v1/models")
    assert models["total"] >= 10
    assert any(m["provider_id"] in ["gemini", "openai", "anthropic"] for m in models["models"])

    # Agents workforce (72 contracts)
    agents = gw.dispatch("GET", "/api/v1/agents")
    assert agents["total"] == 72

    # Providers connectivity
    providers = gw.dispatch("GET", "/api/v1/providers")
    assert len(providers["providers"]) >= 4

    # Chat execution
    chat_resp = gw.dispatch("POST", "/api/v1/chat", {
        "message": "Inspect the project structure",
        "context": {
            "activeFile": "src/openclone/integrations/rest.py",
            "language": "python"
        }
    })
    assert chat_resp["status"] == "success"
    assert "reply" in chat_resp
    assert len(chat_resp["reply"]) > 20

    # Approvals handling
    approval_resp = gw.dispatch("POST", "/api/v1/approvals", {
        "digest": "sha256:abcdef1234567890abcdef1234567890",
        "action": "approve"
    })
    assert approval_resp["status"] == "RECORDED"
    assert approval_resp["action"] == "approve"
