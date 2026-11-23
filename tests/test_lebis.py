"""Unit and integration test suite for OpenClone Logo Engineering & Brand Identity System (LEBIS).

Tests cover:
- Brand Discovery Engine & brief completeness scoring
- Brand Strategy Engine & visual positioning
- Multi-category Logo Concept proposals
- Mathematical Geometry & clear-space calculations
- Typography & permissive licensing validation
- Color Intelligence & WCAG 2.1 contrast calculations
- Vector SVG Asset Engine (pure vectors, zero embedded rasters)
- Logo Quality Assurance Engine audit scoring
- Brand Guideline manual generation
- MCP Server tool endpoints
- JSON Schema Draft 2020-12 conformance
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import jsonschema
import pytest

from src.openclone.branding import (
    BrandDiscoveryEngine,
    BrandGuidelineGenerator,
    BrandIdentityPackage,
    BrandStrategyEngine,
    ColorIntelligenceEngine,
    GeometryEngine,
    LogoCategory,
    LogoConceptEngine,
    LogoQAEngine,
    LogoVariant,
    TypographyEngine,
    VariantType,
    VectorAssetEngine,
    engineer_brand_identity,
)
from src.openclone.mcp.server import OpenCloneMCPServer

ROOT = Path(__file__).resolve().parents[1]


# ============================================================================
# 1. DISCOVERY & STRATEGY TESTS
# ============================================================================

def test_brand_discovery_complete_brief():
    raw = {
        "brand_name": "AetherCloud",
        "category": "Edge Computing Platform",
        "purpose": "Decentralized serverless compute",
        "target_audience": "DevOps and Cloud Architects",
        "positioning": "Ultra-low latency serverless infrastructure",
        "personality_traits": ["Fast", "Resilient", "Precise"],
        "brand_values": ["Zero Downtime", "Open Source"],
    }
    brief, assumptions, completeness = BrandDiscoveryEngine.evaluate_brief(raw)
    assert brief.brand_name == "AetherCloud"
    assert completeness >= 90.0
    assert len(assumptions) == 0


def test_brand_discovery_missing_name_raises():
    with pytest.raises(ValueError):
        BrandDiscoveryEngine.evaluate_brief({"category": "DevTools"})


def test_brand_discovery_with_assumptions():
    raw = {"brand_name": "KubeGuard"}
    brief, assumptions, completeness = BrandDiscoveryEngine.evaluate_brief(raw)
    assert brief.brand_name == "KubeGuard"
    assert len(assumptions) > 0
    assert completeness <= 70.0


def test_brand_strategy_formulation():
    raw = {
        "brand_name": "KubeGuard",
        "category": "Kubernetes Security",
        "purpose": "Automated cluster protection",
        "target_audience": "SecOps Teams",
        "positioning": "Zero-trust Kubernetes runtime governance",
        "personality_traits": ["Authority", "Governed", "Rigorous"],
        "brand_values": ["Compliance", "Integrity"],
    }
    brief, assumptions, _ = BrandDiscoveryEngine.evaluate_brief(raw)
    strategy = BrandStrategyEngine.formulate(brief, assumptions)
    assert "Architect" in strategy.brand_archetype or "Ruler" in strategy.brand_archetype
    assert LogoCategory.COMBINATION_MARK in strategy.recommended_categories


# ============================================================================
# 2. LOGO CONCEPT ENGINE TESTS
# ============================================================================

def test_logo_concept_generation():
    raw = {
        "brand_name": "OpenClone",
        "category": "AI Framework",
        "purpose": "Build with Any AI. Governed by One Engineering Standard.",
        "target_audience": "Developers",
        "positioning": "Universal Engineering Operating System",
        "personality_traits": ["Rigorous", "Precise", "Authoritative"],
        "brand_values": ["Deterministic Truth", "Anti-Slop"],
    }
    brief, assumptions, _ = BrandDiscoveryEngine.evaluate_brief(raw)
    strategy = BrandStrategyEngine.formulate(brief, assumptions)
    concepts = LogoConceptEngine.generate_concepts(brief, strategy)

    assert len(concepts) == 3
    # Check concept diversity across categories
    categories = {c.category for c in concepts}
    assert LogoCategory.COMBINATION_MARK in categories
    assert LogoCategory.GEOMETRIC_MARK in categories
    assert LogoCategory.EMBLEM in categories

    for c in concepts:
        assert len(c.design_intention) > 20
        assert len(c.brand_meaning) > 20
        assert len(c.strengths) >= 2
        assert len(c.limitations) >= 1


# ============================================================================
# 3. GEOMETRY, TYPOGRAPHY & COLOR TESTS
# ============================================================================

def test_geometry_calculations():
    rules = GeometryEngine.calculate_rules(grid_unit_px=8)
    assert rules.grid_unit_px == 8
    assert rules.proportion_ratio_value == pytest.approx(1.618, 0.001)

    bounds = GeometryEngine.compute_clear_space_box(width=100.0, height=80.0, clear_space_factor=0.25)
    assert bounds["origin_x"] == -25.0
    assert bounds["origin_y"] == -20.0
    assert bounds["padded_width"] == 150.0
    assert bounds["padded_height"] == 120.0


def test_typography_engine():
    spec = TypographyEngine.prescribe_typography()
    assert "Plus Jakarta Sans" in spec.primary_font or "Inter" in spec.primary_font
    assert "Open Font License" in spec.licensing or "OFL" in spec.licensing


def test_color_intelligence_contrast():
    # White on Black contrast is 21.0:1
    contrast = ColorIntelligenceEngine.calculate_contrast_ratio("#FFFFFF", "#000000")
    assert contrast >= 20.0

    # Cobalt blue (#2563EB) on dark background (#0B0F19)
    colors = ColorIntelligenceEngine.generate_palette(primary_hex="#2563EB", secondary_hex="#0B0F19")
    assert colors.contrast_primary_on_dark >= 3.0
    assert "C:" in colors.cmyk_primary


# ============================================================================
# 4. VECTOR ENGINE & QA AUDIT TESTS
# ============================================================================

def test_vector_engine_and_qa_pipeline():
    raw = {
        "brand_name": "PrismCode",
        "category": "Developer Tooling",
        "purpose": "Refactor codebase with mathematical certainty",
        "target_audience": "Senior Software Engineers",
        "positioning": "Deterministic refactoring framework",
        "personality_traits": ["Precision", "Structure", "Clarity"],
        "brand_values": ["No AI Slop", "Code Quality"],
        "primary_color": "#2563EB",
        "secondary_color": "#0B0F19",
        "accent_color": "#38BDF8",
    }
    pkg = engineer_brand_identity(raw)
    assert isinstance(pkg, BrandIdentityPackage)
    assert len(pkg.variants) == 8

    # Verify all variants are clean, valid XML with zero embedded rasters
    for v in pkg.variants:
        root = ET.fromstring(v.svg_content)
        assert root.tag.endswith("svg")
        assert "viewBox" in root.attrib or "viewbox" in root.attrib.lower()
        assert "<image" not in v.svg_content.lower()
        assert "data:image/" not in v.svg_content

    # Verify QA audit passed
    assert pkg.qa_report.passed is True
    assert pkg.qa_report.total_score >= 90.0


def test_qa_engine_flags_bad_svg():
    bad_svg = "<svg><image href='data:image/png;base64,xxxx' /></svg>"
    fake_variant = LogoVariant(
        variant_type=VariantType.PRIMARY,
        width=100,
        height=100,
        view_box="0 0 100 100",
        svg_content=bad_svg,
        description="Fake raster",
    )
    colors = ColorIntelligenceEngine.generate_palette()
    report = LogoQAEngine.audit_package([fake_variant], colors)
    assert report.passed is False
    raster_check = [c for c in report.checks if "Raster" in c.name][0]
    assert raster_check.passed is False


def test_guideline_generator():
    raw = {
        "brand_name": "TestCorp",
        "category": "Security Platform",
        "purpose": "Defend cloud architectures",
        "target_audience": "Enterprise CISO",
        "positioning": "Autonomous cloud compliance",
        "personality_traits": ["Authoritative", "Rock-Solid"],
        "brand_values": ["Zero Compromise"],
    }
    pkg = engineer_brand_identity(raw)
    manual = BrandGuidelineGenerator.generate_markdown_manual(pkg)
    assert "# TestCorp — Brand Identity & Logo Engineering Guidelines" in manual
    assert "## 1. Brand Overview & Mission" in manual
    assert "## 5. Geometric Construction & Grid Rules" in manual
    assert "## 9. Incorrect Usage & Anti-Slop Rules" in manual


# ============================================================================
# 5. MCP SERVER & SCHEMA CONFORMANCE TESTS
# ============================================================================

def test_mcp_server_brand_tools():
    server = OpenCloneMCPServer()

    # 1. openclone_engineer_brand
    res = server.call_tool("openclone_engineer_brand", {
        "brand_name": "OpenVector",
        "category": "Vector Graphics Engine",
    })
    assert "brand_name" in res
    assert res["brand_name"] == "OpenVector"
    assert "variants" in res
    assert len(res["variants"]) >= 6
    assert res["qa_report"]["passed"] is True

    # 2. openclone_validate_logo
    valid_svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='#000'/></svg>"
    audit_res = server.call_tool("openclone_validate_logo", {"svg_content": valid_svg})
    assert audit_res["valid"] is True
    assert audit_res["zero_raster"] is True


def test_schemas_conformance():
    brand_schema = json.loads((ROOT / "framework" / "schemas" / "brand-specification.schema.json").read_text(encoding="utf-8"))
    logo_schema = json.loads((ROOT / "framework" / "schemas" / "logo-specification.schema.json").read_text(encoding="utf-8"))

    jsonschema.Draft202012Validator.check_schema(brand_schema)
    jsonschema.Draft202012Validator.check_schema(logo_schema)

    # Validate instance
    sample_brief = {
        "brand_name": "OpenClone",
        "category": "Universal AI Software Engineering Framework",
        "purpose": "Build with Any AI. Governed by One Engineering Standard.",
        "target_audience": "Software engineers and autonomous AI coding agents.",
        "positioning": "Build with Any AI. Governed by One Engineering Standard.",
        "personality_traits": ["Engineering Rigor", "Authority"],
        "brand_values": ["Deterministic Truth", "Zero AI Slop"],
    }
    jsonschema.validate(instance=sample_brief, schema=brand_schema)
