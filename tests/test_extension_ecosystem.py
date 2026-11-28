"""Comprehensive tests for the OpenClone Global IDE Extension Ecosystem.

Validates:
1. Antigravity plugin manifest, skill, subagent, rules, and hooks structure.
2. VS Code extension manifest, views, commands, and activation events.
3. Antigravity and VS Code adapters (workspace and global installation).
4. Platform manager integration, backup creation, and uninstallation.
"""

import json
from pathlib import Path
import pytest
import shutil
import sys

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.openclone.integrations.adapters.antigravity import AntigravityAdapter
from src.openclone.integrations.adapters.vscode import VSCodeAdapter
from src.openclone.integrations.manager import IntegrationManager


@pytest.fixture
def repo_root():
    """Return the repository root directory."""
    return REPO_ROOT


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project folder."""
    proj = tmp_path / "test_project"
    proj.mkdir()
    (proj / "PROJECT.md").write_text("# Test Project", encoding="utf-8")
    return proj


# ==============================================================================
# SECTION 1: ANTIGRAVITY PLUGIN VERIFICATION
# ==============================================================================

class TestAntigravityPluginPackage:
    """Validate the official Antigravity plugin package files and schemas."""

    def test_plugin_json_schema(self, repo_root):
        plugin_file = repo_root / "plugins" / "openclone-antigravity" / "plugin.json"
        assert plugin_file.exists(), "plugin.json must exist in plugins/openclone-antigravity"
        
        data = json.loads(plugin_file.read_text(encoding="utf-8"))
        assert data.get("name") == "openclone"
        assert data.get("version") == "2.0.0"
        assert "OpenClone" in data.get("description", "")
        assert "OpenClone" in data.get("author", "")
        assert isinstance(data.get("suggestedPrompts"), list)
        assert len(data.get("suggestedPrompts")) > 0

    def test_mcp_config_json(self, repo_root):
        mcp_file = repo_root / "plugins" / "openclone-antigravity" / "mcp_config.json"
        assert mcp_file.exists(), "mcp_config.json must exist in plugins/openclone-antigravity"
        
        data = json.loads(mcp_file.read_text(encoding="utf-8"))
        assert "mcpServers" in data
        assert "openclone" in data["mcpServers"]
        server_cfg = data["mcpServers"]["openclone"]
        assert "command" in server_cfg
        assert "args" in server_cfg

    def test_skill_definition(self, repo_root):
        skill_file = repo_root / "plugins" / "openclone-antigravity" / "skills" / "openclone-engineering" / "SKILL.md"
        assert skill_file.exists(), "Skill definition SKILL.md must exist"
        
        content = skill_file.read_text(encoding="utf-8")
        assert "name: openclone-engineering" in content
        assert "description:" in content
        assert "OpenClone" in content

    def test_subagent_definition(self, repo_root):
        agent_file = repo_root / "plugins" / "openclone-antigravity" / "agents" / "openclone-engineer.md"
        assert agent_file.exists(), "Subagent markdown file must exist"
        
        content = agent_file.read_text(encoding="utf-8")
        assert "OpenClone Autonomous Engineer Agent" in content
        assert "openclone" in content.lower()

    def test_rules_definition(self, repo_root):
        rules_file = repo_root / "plugins" / "openclone-antigravity" / "rules" / "AGENTS.md"
        assert rules_file.exists(), "Governance rules file must exist"
        
        content = rules_file.read_text(encoding="utf-8")
        assert "OpenClone Deterministic Governance Rules" in content
        assert "Deterministic Governance" in content

    def test_assets_and_hooks(self, repo_root):
        logo_file = repo_root / "plugins" / "openclone-antigravity" / "assets" / "logo.svg"
        assert logo_file.exists(), "logo.svg must exist"
        assert "<svg" in logo_file.read_text(encoding="utf-8")

        hooks_file = repo_root / "plugins" / "openclone-antigravity" / "hooks.json"
        assert hooks_file.exists(), "hooks.json must exist"
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
        assert "hooks" in data


# ==============================================================================
# SECTION 2: VS CODE EXTENSION VERIFICATION
# ==============================================================================

class TestVSCodeExtensionPackage:
    """Validate the native VS Code extension package files and schema."""

    def test_package_json_schema(self, repo_root):
        pkg_file = repo_root / "extensions" / "vscode" / "package.json"
        assert pkg_file.exists(), "package.json must exist in extensions/vscode"

        data = json.loads(pkg_file.read_text(encoding="utf-8"))
        assert data.get("name") == "openclone-vscode"
        assert "OpenClone" in data.get("displayName", "")
        assert data.get("version") == "2.0.0"
        assert data.get("main") == "./src/extension.js"
        assert "engines" in data and "vscode" in data["engines"]

    def test_views_and_activitybar(self, repo_root):
        pkg_file = repo_root / "extensions" / "vscode" / "package.json"
        data = json.loads(pkg_file.read_text(encoding="utf-8"))

        contributes = data.get("contributes", {})
        assert "viewsContainers" in contributes
        containers = contributes["viewsContainers"].get("activitybar", [])
        assert any(c.get("id") == "openclone-explorer" for c in containers)

        assert "views" in contributes
        views = contributes["views"].get("openclone-explorer", [])
        view_ids = [v.get("id") for v in views]
        assert "openclone.statusView" in view_ids
        assert "openclone.planView" in view_ids
        assert "openclone.workersView" in view_ids
        assert "openclone.ledgerView" in view_ids

    def test_commands_contribution(self, repo_root):
        pkg_file = repo_root / "extensions" / "vscode" / "package.json"
        data = json.loads(pkg_file.read_text(encoding="utf-8"))

        commands = data.get("contributes", {}).get("commands", [])
        command_ids = [c.get("command") for c in commands]
        assert "openclone.inspect" in command_ids
        assert "openclone.plan" in command_ids
        assert "openclone.run" in command_ids
        assert "openclone.verify" in command_ids
        assert "openclone.connect" in command_ids

    def test_extension_runtime_script(self, repo_root):
        ext_js = repo_root / "extensions" / "vscode" / "src" / "extension.js"
        assert ext_js.exists(), "extension.js entrypoint must exist"
        content = ext_js.read_text(encoding="utf-8")
        assert "function activate(context)" in content
        assert "openclone.inspect" in content
        assert "OpenCloneTreeProvider" in content

    def test_icon_asset(self, repo_root):
        icon_file = repo_root / "extensions" / "vscode" / "resources" / "icon.svg"
        assert icon_file.exists(), "resources/icon.svg must exist"
        assert "<svg" in icon_file.read_text(encoding="utf-8")


# ==============================================================================
# SECTION 3: INTEGRATION ADAPTERS & GLOBAL INSTALLATION
# ==============================================================================

class TestIntegrationAdapters:
    """Validate runtime adapters for Antigravity and VS Code."""

    def test_antigravity_adapter_info(self, temp_project):
        adapter = AntigravityAdapter()
        assert adapter.platform_id == "antigravity"
        assert adapter.display_name == "Google Antigravity IDE"

        disc = adapter.discover(workspace_root=temp_project)
        assert disc.platform_id == "antigravity"
        assert "mcp" in disc.supported_protocols
        assert "skills" in disc.supported_protocols

    def test_antigravity_workspace_install_and_uninstall(self, temp_project):
        adapter = AntigravityAdapter()
        res = adapter.connect(workspace_root=temp_project, is_global=False)
        assert res.get("status") == "CONNECTED"
        assert res.get("scope") == "WORKSPACE"

        # Verify destination files
        dest_plugin = temp_project / ".gemini" / "plugins" / "openclone"
        assert dest_plugin.exists()
        assert (dest_plugin / "plugin.json").exists()
        assert (dest_plugin / "mcp_config.json").exists()

        # Check discovered as configured
        disc = adapter.discover(workspace_root=temp_project)
        assert disc.is_configured is True

        # Disconnect
        un_res = adapter.disconnect(workspace_root=temp_project, is_global=False)
        assert un_res.get("status") == "DISCONNECTED"
        assert not dest_plugin.exists()

    def test_antigravity_global_install(self, temp_project, monkeypatch, tmp_path):
        fake_home = tmp_path / "fake_home"
        fake_home.mkdir()
        monkeypatch.setenv("USERPROFILE", str(fake_home))
        monkeypatch.setenv("HOME", str(fake_home))

        adapter = AntigravityAdapter()
        global_dir = adapter._get_global_plugin_dir()
        assert "plugins" in str(global_dir)

        res = adapter.connect(workspace_root=temp_project, is_global=True)
        assert res.get("status") == "CONNECTED"
        assert res.get("scope") == "GLOBAL"
        assert (global_dir / "plugin.json").exists()

        # Verify disconnect global
        un_res = adapter.disconnect(workspace_root=temp_project, is_global=True)
        assert un_res.get("status") == "DISCONNECTED"
        assert not global_dir.exists()

    def test_vscode_adapter_connect(self, temp_project):
        adapter = VSCodeAdapter()
        assert adapter.platform_id == "vscode"

        res = adapter.connect(workspace_root=temp_project)
        assert res.get("status") == "CONNECTED"

        mcp_file = temp_project / ".vscode" / "mcp.json"
        assert mcp_file.exists()
        data = json.loads(mcp_file.read_text(encoding="utf-8"))
        assert "servers" in data or "mcpServers" in data

        un_res = adapter.disconnect(workspace_root=temp_project)
        assert un_res.get("status") == "DISCONNECTED"

    def test_integration_manager_global_flag(self, temp_project, monkeypatch, tmp_path):
        fake_home = tmp_path / "fake_home"
        fake_home.mkdir()
        monkeypatch.setenv("USERPROFILE", str(fake_home))
        monkeypatch.setenv("HOME", str(fake_home))

        mgr = IntegrationManager(workspace_root=temp_project)
        connect_res = mgr.connect_platform("antigravity", is_global=True)
        assert connect_res.get("status") == "CONNECTED"

        insp = mgr.inspect_platform("antigravity")
        assert insp.get("discovered", {}).get("platform_id") == "antigravity"

        disconnect_res = mgr.disconnect_platform("antigravity", is_global=True)
        assert disconnect_res.get("status") == "DISCONNECTED"
