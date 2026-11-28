"""Comprehensive test suite for OpenClone Platform Management Ecosystem."""
import json
import os
import tempfile
from pathlib import Path

import pytest

from src.openclone.platform.config.manager import ConfigurationManager
from src.openclone.platform.config.schema import PlatformUserConfig, UpdateConfig
from src.openclone.platform.installation.detector import detect_installation_mode, InstallationInfo
from src.openclone.platform.installation.manager import PlatformInstallationManager
from src.openclone.platform.runtime.manager import RuntimeManager
from src.openclone.platform.runtime.toolchains import ToolchainInspector
from src.openclone.platform.updates.channels import ReleaseChannel
from src.openclone.platform.updates.manifest import ReleaseManifest, ReleaseArtifact, verify_file_sha256
from src.openclone.platform.updates.engine import UpdateEngine
from src.openclone.platform.rollback.manager import RollbackManager
from src.openclone.platform.compatibility.engine import CompatibilityEngine, CompatibilityLevel
from src.openclone.platform.components.manifest import ComponentManifest
from src.openclone.platform.components.manager import ComponentManager
from src.openclone.platform.diagnostics.doctor import PlatformDoctor


class TestPlatformConfig:
    """Tests for ConfigurationManager, schema validation, and persistence."""

    def test_default_config_creation(self, tmp_path):
        cfg_path = tmp_path / "config.json"
        mgr = ConfigurationManager(config_path=cfg_path)
        cfg = mgr.load_config()
        assert cfg.version == "1.0.0"
        assert cfg.update.channel == "stable"
        assert cfg_path.exists()

    def test_dot_notation_get_and_set(self, tmp_path):
        cfg_path = tmp_path / "config.json"
        mgr = ConfigurationManager(config_path=cfg_path)
        assert mgr.get_setting("update.channel") == "stable"
        mgr.set_setting("update.channel", "beta")
        assert mgr.get_setting("update.channel") == "beta"
        
        # Verify persistence on disk
        mgr_reloaded = ConfigurationManager(config_path=cfg_path)
        assert mgr_reloaded.get_setting("update.channel") == "beta"

    def test_corrupted_config_recovery(self, tmp_path):
        cfg_path = tmp_path / "config.json"
        cfg_path.write_text("{invalid json", encoding="utf-8")
        mgr = ConfigurationManager(config_path=cfg_path)
        cfg = mgr.load_config()
        assert cfg.version == "1.0.0"  # Graceful fallback to default
        assert (tmp_path / "backups").exists()  # Backup created


class TestPlatformInstallationAndRuntime:
    """Tests for installation mode detection and runtime manager."""

    def test_installation_detection(self):
        info = detect_installation_mode()
        assert isinstance(info, InstallationInfo)
        assert info.mode in ("python-pip", "python-pipx", "python-venv", "source-checkout", "standalone-binary", "portable")
        assert Path(info.executable_path).exists()

    def test_runtime_manager_python_info(self):
        rt = RuntimeManager()
        info = rt.get_python_info()
        assert "version" in info
        assert "executable" in info
        assert Path(info["executable"]).exists()

    def test_toolchain_inspector(self):
        tools = ToolchainInspector.inspect_all()
        assert "python" in tools
        assert tools["python"].available is True
        assert "git" in tools


class TestPlatformUpdatesAndRollback:
    """Tests for release manifests, update engine, and rollback recovery."""

    def test_release_channel_normalization(self):
        assert ReleaseChannel.normalize("BETA") == ReleaseChannel.BETA
        assert ReleaseChannel.normalize("nightly") == ReleaseChannel.NIGHTLY
        assert ReleaseChannel.normalize("unknown") == ReleaseChannel.STABLE

    def test_release_manifest_parsing(self, tmp_path):
        dummy_file = tmp_path / "test.whl"
        dummy_file.write_bytes(b"package content")
        import hashlib
        expected_sha = hashlib.sha256(b"package content").hexdigest()

        manifest_data = {
            "product": "openclone",
            "version": "1.1.0",
            "channel": "stable",
            "published_at": "2026-11-25T12:00:00Z",
            "min_python_version": "3.10.0",
            "artifacts": [
                {
                    "filename": "test.whl",
                    "os": "windows",
                    "arch": "x64",
                    "distribution_type": "wheel",
                    "sha256": expected_sha,
                    "size_bytes": len(b"package content"),
                    "url": "https://example.com/test.whl",
                }
            ],
        }
        manifest = ReleaseManifest.from_dict(manifest_data)
        assert manifest.version == "1.1.0"
        assert len(manifest.artifacts) == 1
        
        art = manifest.find_artifact_for_system("windows", "x64")
        assert art is not None
        assert art.filename == "test.whl"

        # Verify sha256 check
        assert verify_file_sha256(dummy_file, expected_sha) is True
        assert verify_file_sha256(dummy_file, "0000000000000000000000000000000000000000000000000000000000000000") is False

    def test_update_engine_check(self, tmp_path):
        cfg_path = tmp_path / "config.json"
        mgr = ConfigurationManager(config_path=cfg_path)
        engine = UpdateEngine(config_manager=mgr)

        manifest_data = {
            "product": "openclone",
            "version": "2.0.0",
            "channel": "stable",
            "published_at": "2026-11-25T12:00:00Z",
            "min_python_version": "3.10.0",
            "artifacts": [
                {
                    "filename": "openclone-2.0.0.whl",
                    "os": "any",
                    "arch": "any",
                    "distribution_type": "wheel",
                    "sha256": "a" * 64,
                    "size_bytes": 1000,
                    "url": "https://example.com/test.whl",
                }
            ],
        }
        res = engine.check_for_updates(manifest_override=manifest_data)
        assert res.update_available is True
        assert res.latest_version == "2.0.0"

    def test_rollback_manager(self, tmp_path):
        backup_root = tmp_path / "backups"
        rb = RollbackManager(backup_root=backup_root)
        snapshot = rb.create_snapshot("1.0.0", {"reason": "test"})
        assert snapshot.exists()
        
        snapshots = rb.list_snapshots()
        assert len(snapshots) >= 1
        assert snapshots[0]["version"] == "1.0.0"

        restored = rb.restore_latest_snapshot()
        assert restored["success"] is True


class TestCompatibilityEngine:
    """Tests for multi-dimensional compatibility engine."""

    def test_compatible_system(self):
        rep = CompatibilityEngine.evaluate(min_python_version="3.10.0")
        assert rep.is_compatible is True
        assert rep.level == CompatibilityLevel.FULLY_COMPATIBLE

    def test_incompatible_python_requirement(self):
        rep = CompatibilityEngine.evaluate(min_python_version="99.0.0")
        assert rep.is_compatible is False
        assert rep.level == CompatibilityLevel.INCOMPATIBLE

    def test_incompatible_os_requirement(self):
        rep = CompatibilityEngine.evaluate(target_os="non_existent_os")
        assert rep.is_compatible is False
        assert rep.level == CompatibilityLevel.INCOMPATIBLE


class TestComponentManager:
    """Tests for component manifest and lifecycle management."""

    def test_component_manifest_validation(self):
        data = {
            "id": "test-pack",
            "name": "Test Tool Pack",
            "version": "1.0.0",
            "publisher": "OpenClone",
            "description": "Test component",
            "category": "tool-pack",
            "min_platform_version": "1.0.0",
            "permissions": ["filesystem:read:workspace", "subprocess:exec"],
        }
        cm = ComponentManifest.from_dict(data)
        assert cm.id == "test-pack"
        warnings = cm.validate_permissions()
        assert len(warnings) == 0

    def test_component_lifecycle(self, tmp_path):
        comp_dir = tmp_path / "components"
        mgr = ComponentManager(components_dir=comp_dir)
        
        # Create a mock component folder
        src_comp = tmp_path / "mock_src"
        src_comp.mkdir()
        manifest_data = {
            "id": "mock-plugin",
            "name": "Mock Plugin",
            "version": "1.0.0",
            "publisher": "Tester",
            "description": "A mock plugin",
            "category": "skill",
            "min_platform_version": "1.0.0",
        }
        (src_comp / "component.json").write_text(json.dumps(manifest_data), encoding="utf-8")

        # Install
        inst_res = mgr.install_from_dir(src_comp)
        assert inst_res["success"] is True

        # List
        items = mgr.list_components()
        assert len(items) == 1
        assert items[0]["id"] == "mock-plugin"
        assert items[0]["enabled"] is True

        # Disable
        assert mgr.set_enabled("mock-plugin", False) is True
        items = mgr.list_components()
        assert items[0]["enabled"] is False

        # Enable
        assert mgr.set_enabled("mock-plugin", True) is True
        items = mgr.list_components()
        assert items[0]["enabled"] is True

        # Remove
        assert mgr.remove_component("mock-plugin") is True
        assert len(mgr.list_components()) == 0


class TestPlatformDoctor:
    """Tests for environmental platform doctor."""

    def test_doctor_runs_all_checks(self):
        doc = PlatformDoctor()
        checks = doc.run_all_checks()
        assert len(checks) >= 8
        categories = {c.category for c in checks}
        assert "Installation" in categories
        assert "Runtime" in categories
        assert "Platform" in categories
