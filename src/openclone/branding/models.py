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


class ConceptSelectionPolicy(str, Enum):
    """Policy rules governing which conceptual proposal is promoted to production."""
    HIGHEST_SCORE = "HIGHEST_SCORE"
    CATEGORY_PREFERENCE = "CATEGORY_PREFERENCE"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"
    DEFAULT_PRIMARY = "DEFAULT_PRIMARY"


class QACheckSeverity(str, Enum):
    """Severity classification for QA check findings."""
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    INFO = "INFO"


class QACheckCategory(str, Enum):
    """Canonical QA audit check categories."""
    XML_VALIDITY = "XML_VALIDITY"
    RASTER_PURITY = "RASTER_PURITY"
    GEOMETRY_PROPORTIONS = "GEOMETRY_PROPORTIONS"
    CONTRAST_ACCESSIBILITY = "CONTRAST_ACCESSIBILITY"
    VARIANT_PARITY = "VARIANT_PARITY"
    SMALL_SCALE_LEGIBILITY = "SMALL_SCALE_LEGIBILITY"


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
class ConceptScore:
    """Multi-factor quantitative evaluation for a logo concept proposal."""
    concept_id: str
    category_relevance: float  # 0.0 - 100.0
    scalability_score: float   # 0.0 - 100.0 (performance from 16px to 4K billboard)
    complexity_score: float    # 0.0 - 100.0 (higher = more optimal simplicity / lower clutter)
    distinctiveness_score: float # 0.0 - 100.0 (differentiation from competitors)
    composite_score: float     # Weighted composite 0.0 - 100.0
    rationale: str = ""


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
    score: Optional[ConceptScore] = None
    selection_rank: int = 1
    is_selected: bool = False


@dataclass
class VariantGeometry:
    """Exact computed coordinate geometry for a specific logo variant."""
    variant_type: VariantType
    width: int
    height: int
    view_box: str
    mark_origin_x: float
    mark_origin_y: float
    mark_scale: float
    text_origin_x: float
    text_origin_y: float
    text_font_size: float
    tagline_origin_x: float = 0.0
    tagline_origin_y: float = 0.0
    tagline_font_size: float = 0.0
    clear_space_box: Dict[str, float] = field(default_factory=dict)


@dataclass
class GeometryRules:
    """Mathematical construction guidelines and clearance bounds."""
    grid_unit_px: int = 8
    proportion_ratio_name: str = "Golden Ratio (1.618)"
    proportion_ratio_value: float = 1.618
    clear_space_factor: float = 0.25  # Relative to mark size
    min_digital_width_px: int = 24
    min_print_width_mm: float = 10.0
    symmetry_notes: str = "Bilateral symmetry along central vertical axis with optical compensation."
    subgrid_unit_px: int = 4
    macro_unit_px: int = 64
    variant_geometries: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TypographySpec:
    """Typeface classification, pairings, and licensing."""
    primary_font: str
    primary_classification: str
    secondary_font: str
    secondary_classification: str
    hierarchy_scale: str = "Major Third (1.250)"
    letter_spacing_logotype: str = "-0.025em"
    letter_spacing_tagline: str = "0.08em"
    licensing: str = "Open Font License (OFL) / Apache 2.0 (Permissive Commercial Use)"
    primary_fallback_stack: str = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    secondary_fallback_stack: str = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    font_weight_logotype: int = 800
    font_weight_tagline: int = 500
    line_height_ratio: float = 1.2
    commercial_license_verified: bool = True


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
    contrast_accent_on_dark: float = 0.0
    contrast_accent_on_light: float = 0.0
    cmyk_primary: str = "C:85 M:50 Y:0 K:0"
    cmyk_secondary: str = "C:0 M:0 Y:0 K:90"
    cmyk_accent: str = "C:60 M:0 Y:5 K:0"
    wcag_compliance: str = "WCAG 2.1 AA Compliant (>= 4.5:1 text, >= 3.0:1 graphics)"
    palette_name: str = "Engineered High-Contrast"
    css_tokens: Dict[str, str] = field(default_factory=dict)
    tailwind_tokens: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogoVariant:
    """Rendered vector variant with metadata."""
    variant_type: VariantType
    width: int
    height: int
    view_box: str
    svg_content: str
    description: str
    aspect_ratio: float = 1.0
    is_monochrome: bool = False
    target_background: str = "dark"  # "dark" | "light" | "any"


@dataclass
class QACheckItem:
    """Individual QA validation result."""
    name: str
    passed: bool
    score: float
    details: str
    category: str = "GENERAL"
    severity: str = "BLOCKER"


@dataclass
class QAReport:
    """Complete automated brand quality verification report."""
    total_score: float
    passed: bool
    checks: List[QACheckItem]
    recommendations: List[str]
    verdict: str = "PASS"  # PASS, NEEDS_REVISION, FAIL
    version: str = "1.0.0"
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0


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
    status: str = "generated"  # draft, generated, validated, human_approved
    design_tokens: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching schema specifications."""
        return {
            "brand_name": self.brief.brand_name,
            "category": self.brief.category,
            "version": self.version,
            "status": self.status,
            "strategy": asdict(self.strategy),
            "concepts": [asdict(c) for c in self.concepts],
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
                "verdict": self.qa_report.verdict,
                "checks": [asdict(c) for c in self.qa_report.checks],
            },
            "design_tokens": self.design_tokens,
        }
