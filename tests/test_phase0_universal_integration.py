"""Integration tests for Phase 0 Universal Capabilities, MCP exposure, and REST dispatch (Stage 5)."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.openclone.integrations.capabilities import (
    CapabilityCategory,
    RiskClassification,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import AuthContext, IntegrationGateway
from src.openclone.integrations.openapi import dispatch_rest_request, generate_openapi_spec
from src.openclone.mcp.server import OpenCloneMCPServer


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def registry(repo_root: Path):
    return get_canonical_registry(repo_root)


@pytest.fixture
def gateway(registry, repo_root: Path):
    return IntegrationGateway(registry, repo_root)


def test_phase0_capabilities_registered(registry):
    caps = registry.list_capabilities()
    cap_ids = {c.id for c in caps}

    assert "openclone_ingest_documents" in cap_ids
    assert "openclone_generate_clarifications" in cap_ids
    assert "openclone_answer_clarification" in cap_ids
    assert "openclone_recommend_ide" in cap_ids
    assert "openclone_generate_platform_template" in cap_ids


def test_mcp_tool_exposure_of_phase0_capabilities(registry):
    server = OpenCloneMCPServer(registry.root)
    resp = server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {"all": True}})
    tools = resp["result"]["tools"]
    tool_names = {t["name"] for t in tools}

    assert "openclone_ingest_documents" in tool_names
    assert "openclone_generate_clarifications" in tool_names
    assert "openclone_recommend_ide" in tool_names
    assert "openclone_generate_platform_template" in tool_names


def test_gateway_execution_phase0_capabilities(gateway, tmp_path: Path):
    auth = gateway.authenticate_token("test-valid-token")

    # 1. Recommend IDE
    res_ide = gateway.execute(
        auth,
        "openclone_recommend_ide",
        {"requirements_text": "Building a Python FastAPI service with autonomous agents and Redis."},
    )
    assert res_ide["primary_recommendation"] is not None
    assert "platform_id" in res_ide["primary_recommendation"]

    # 2. Generate Clarifications
    res_clarif = gateway.execute(
        auth,
        "openclone_generate_clarifications",
        {"requirements_text": "A basic task planner without specified database or scale."},
    )
    assert res_clarif["total_questions"] >= 1
    assert "questions" in res_clarif

    # 3. Generate Platform Template (Windsurf)
    res_tmpl = gateway.execute(
        auth,
        "openclone_generate_platform_template",
        {"platform_id": "windsurf", "workspace_path": str(tmp_path)},
    )
    assert res_tmpl["status"] == "CONNECTED"
    assert (tmp_path / ".windsurfrules").exists()

    # 4. Ingest Documents
    sample_file = tmp_path / "sample_reqs.txt"
    sample_file.write_text("Requirement: Fast payment gateway\nWorkload: 100000 DAU", encoding="utf-8")
    res_ingest = gateway.execute(
        auth,
        "openclone_ingest_documents",
        {"document_paths": [str(sample_file)]},
    )
    assert res_ingest["total_documents"] == 1
    assert res_ingest["total_evidence_items"] >= 1

    # 5. Answer Clarification
    res_ans = gateway.execute(
        auth,
        "openclone_answer_clarification",
        {"question_id": "CLARIF-SCALE-001", "answer": "100,000 DAU with PostgreSQL"},
    )
    assert res_ans["question_id"] == "CLARIF-SCALE-001"
    assert res_ans["status"] in ("RECORDED", "UNKNOWN_QUESTION")


def test_phase0_mcp_direct_tool_call(registry):
    server = OpenCloneMCPServer(registry.root)
    call_resp = server.handle_request({
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/call",
        "params": {
            "name": "openclone_recommend_ide",
            "arguments": {"requirements_text": "Python FastAPI and Vue web app"},
        },
    })
    assert not call_resp.get("result", {}).get("isError", True)
    import json
    data = json.loads(call_resp["result"]["content"][0]["text"])
    assert "primary_recommendation" in data


def test_openapi_dispatch_phase0_endpoints(gateway):
    auth = gateway.authenticate_token("test-valid-token")
    spec = generate_openapi_spec(gateway.registry)

    assert "/capabilities/openclone_recommend_ide" in spec["paths"]
    assert "/capabilities/openclone_generate_clarifications" in spec["paths"]

    # Dispatch REST call
    res = dispatch_rest_request(
        gateway,
        auth,
        "POST",
        "/v1/capabilities/openclone_recommend_ide",
        {"requirements_text": "Fast Kotlin Spring microservices"},
    )
    assert res is not None
    assert "primary_recommendation" in res
