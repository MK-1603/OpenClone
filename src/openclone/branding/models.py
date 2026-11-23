"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Data Models.

Defines all core dataclasses, enums, and schemas for brand discovery,
strategy, logo concepts, geometry, typography, color, vector variants, and QA.
Zero external dependencies (Python standard library only).
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class LogoCategory(str, Enum):
    """Canonical logo mark categories."""
    WORDMARK = "WORDMARK"
    LETTERMARK = "LETTERMARK"
    ABSTRACT_SYMBOL = "ABSTRACT_SYMBOL"
    COMBINATION_MARK = "COMBINATION_MARK"
    EMBLEM = "EMBLEM"
    GEOMETRIC_MARK = "GEOMETRIC_MARK"
    MASCOT = "MASCOT"


class VariantType(str, Enum):
    """Standardized production logo variants."""
    PRIMARY = "PRIMARY"
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"
    SYMBOL_ONLY = "SYMBOL_ONLY"
    MONOCHROME_DARK = "MONOCHROME_DARK"
    MONOCHROME_LIGHT = "MONOCHROME_LIGHT"
    FAVICON = "FAVICON"
    SOCIAL_PREVIEW = "SOCIAL_PREVIEW"


@dataclass
class BrandBrief:
    """Input brand brief collected from discovery."""
    brand_name: str
    category: str
    purpose: str
    target_audience: str
    positioning: str
    personality_traits: List[str]
    brand_values: List[str]
    competitors_and_references: List[str] = field(default_factory=list)
    visual_preferences: List[str] = field(default_factory=list)
    design_restrictions: List[str] = field(default_factory=list)
    primary_environments: List[str] = field(default_factory=lambda: ["web", "mobile", "print"])


@dataclass
class BrandStrategy:
    """Strategic visual foundation derived from the brand brief."""
    positioning_statement: str
    brand_archetype: str
    core_attributes: List[str]
    differentiation_factors: List[str]
    visual_direction: str
    recommended_categories: List[LogoCategory]
    typography_direction: str
    color_strategy: str
    documented_assumptions: List[str] = field(default_factory=list)


@dataclass
class LogoConcept:
    """Distinct conceptual identity proposal."""
    concept_id: str
    category: LogoCategory
    name: str
    design_intention: str
    brand_meaning: str
    symbol_construction: str
    typography_direction: str
    color_direction: str
    strengths: List[str]
    limitations: List[str]


@dataclass
class GeometryRules:
    """Mathematical construction guidelines and clearance bounds."""
    grid_unit_px: int = 8
    proportion_ratio_name: str = "Golden Ratio (1.618)"
    proportion_ratio_value: float = 1.618
    clear_space_factor: float = 0.25  # Relative to mark size
    min_digital_width_px: int = 24
    min_print_width_mm: float = 10.0
    symmetry_notes: str = "Bilateral symmetry on primary glyph with intentional optical balancing."


@dataclass
class TypographySpec:
    """Typeface classification, pairings, and licensing."""
    primary_font: str
    primary_classification: str
    secondary_font: str
    secondary_classification: str
    hierarchy_scale: str = "Major Third (1.250)"
    letter_spacing_logotype: str = "-0.02em"
    letter_spacing_tagline: str = "0.08em"
    licensing: str = "Open Font License (OFL) / Apache 2.0 (Permissive Commercial Use)"


@dataclass
class ColorSpec:
    """Complete color system across digital and print representations."""
    primary_hex: str
    secondary_hex: str
    accent_hex: str
    neutral_dark_hex: str
    neutral_light_hex: str
    contrast_primary_on_light: float
    contrast_primary_on_dark: float
    cmyk_primary: str = "C:85 M:50 Y:0 K:0"
    cmyk_secondary: str = "C:0 M:0 Y:0 K:90"
    wcag_compliance: str = "WCAG 2.1 AA Compliant (>= 4.5:1 text, >= 3.0:1 graphics)"


@dataclass
class LogoVariant:
    """Rendered vector variant with metadata."""
    variant_type: VariantType
    width: int
    height: int
    view_box: str
    svg_content: str
    description: str


@dataclass
class QACheckItem:
    """Individual QA validation result."""
    name: str
    passed: bool
    score: float
    details: str


@dataclass
class QAReport:
    """Complete automated brand quality verification report."""
    total_score: float
    passed: bool
    checks: List[QACheckItem]
    recommendations: List[str]
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


@dataclass
class BrandIdentityPackage:
    """Fully engineered brand identity package."""
    brief: BrandBrief
    strategy: BrandStrategy
    concepts: List[LogoConcept]
    selected_concept: LogoConcept
    geometry: GeometryRules
    typography: TypographySpec
    color: ColorSpec
    variants: List[LogoVariant]
    qa_report: QAReport

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brand_name": self.brief.brand_name,
            "category": self.brief.category,
            "strategy": asdict(self.strategy),
            "selected_concept": asdict(self.selected_concept),
            "geometry": asdict(self.geometry),
            "typography": asdict(self.typography),
            "color": asdict(self.color),
            "variants": [
                {
                    "type": v.variant_type.value,
                    "dimensions": f"{v.width}x{v.height}",
                    "description": v.description,
                }
                for v in self.variants
            ],
            "qa_report": {
                "total_score": self.qa_report.total_score,
                "passed": self.qa_report.passed,
                "checks": [asdict(c) for c in self.qa_report.checks],
            },
        }
