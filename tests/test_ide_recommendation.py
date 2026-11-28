"""Unit and integration tests for IDE Recommendation Engine and Windsurf Adapter (Stage 4)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.openclone.integrations.adapters.windsurf import WindsurfAdapter
from src.openclone.intelligence.ide_recommendation import (
    IdeRecommendationEngine,
    PlatformID,
)
from src.openclone.intelligence.project_intelligence import ProjectIntelligenceArchitect


def test_windsurf_adapter_discovery(tmp_path: Path):
    adapter = WindsurfAdapter()
    disc = adapter.discover(workspace_root=tmp_path)
    assert disc.platform_id == "windsurf"
    assert disc.display_name == "Windsurf AI Editor"
    assert "mcp" in disc.supported_protocols
    assert "rules" in disc.supported_protocols


def test_windsurf_adapter_connect_and_disconnect(tmp_path: Path):
    adapter = WindsurfAdapter()
    res_conn = adapter.connect(workspace_root=tmp_path)
    assert res_conn["status"] == "CONNECTED"

    # Verify generated files
    mcp_file = tmp_path / ".codeium" / "windsurf" / "mcp_config.json"
    rules_file = tmp_path / ".windsurfrules"
    assert mcp_file.exists()
    assert rules_file.exists()

    # Validate JSON in mcp_config
    mcp_data = json.loads(mcp_file.read_text(encoding="utf-8"))
    assert "openclone" in mcp_data["mcpServers"]

    # Verify inspect
    insp = adapter.inspect(workspace_root=tmp_path)
    assert insp["has_rules"] is True
    assert insp["status"] == "CONFIGURED"

    # Verify disconnect
    res_disc = adapter.disconnect(workspace_root=tmp_path)
    assert res_disc["status"] == "DISCONNECTED"
    assert not mcp_file.exists()
    assert not rules_file.exists()


def test_windsurf_adapter_preserves_existing_config_and_rules(tmp_path: Path):
    adapter = WindsurfAdapter()
    codeium_dir = tmp_path / ".codeium" / "windsurf"
    codeium_dir.mkdir(parents=True, exist_ok=True)
    mcp_file = codeium_dir / "mcp_config.json"
    rules_file = tmp_path / ".windsurfrules"

    # Pre-existing user config and rules
    mcp_file.write_text(json.dumps({"mcpServers": {"user_server": {"command": "node"}}}, indent=2), encoding="utf-8")
    rules_file.write_text("# My Custom Project Rules\n- Never touch production secrets", encoding="utf-8")

    res = adapter.connect(workspace_root=tmp_path)
    assert res["status"] == "CONNECTED"

    # Verify user config preserved alongside openclone
    mcp_data = json.loads(mcp_file.read_text(encoding="utf-8"))
    assert "user_server" in mcp_data["mcpServers"]
    assert "openclone" in mcp_data["mcpServers"]

    # Verify backup exists
    assert (codeium_dir / "mcp_config.json.bak").exists()
    assert (tmp_path / ".windsurfrules.bak").exists()

    # Verify user rules preserved
    rules_data = rules_file.read_text(encoding="utf-8")
    assert "My Custom Project Rules" in rules_data
    assert "OpenClone Deterministic Governance Rules" in rules_data


def test_ide_recommendation_engine_scoring():
    engine = IdeRecommendationEngine()
    
    # Python + FastAPI prompt should favor Windsurf / Cursor / Antigravity
    recs = engine.evaluate(requirements_text="Python FastAPI microservices with autonomous agent workflows and Redis.")
    assert len(recs) >= 4
    primary = next(r for r in recs if r.is_primary)
    assert primary.match_score >= 0.85
    platforms = [r.platform_id for r in recs]
    assert PlatformID.WINDSURF in platforms
    assert PlatformID.ANTIGRAVITY in platforms


def test_ide_recommendation_engine_jvm_scoring():
    engine = IdeRecommendationEngine()
    recs = engine.evaluate(requirements_text="Enterprise Spring Boot 3 Kotlin microservices with JVM GC tuning.")
    jb_rec = next(r for r in recs if r.platform_id == PlatformID.JETBRAINS)
    assert jb_rec.match_score >= 0.90
    assert any("JVM" in r for r in jb_rec.rationale)


def test_pia_integration_with_ide_recommendations():
    pia = ProjectIntelligenceArchitect()
    res = pia.execute_new(
        prompt="Build a full-stack Python and React platform.",
        project_name="FullStackPlatform",
    )

    assert "ide_recommendations" in res
    assert len(res["ide_recommendations"]) > 0
    top_ide = res["ide_recommendations"][0]
    assert top_ide["match_score"] > 0.7
    assert len(top_ide["rationale"]) > 0
