"""OpenClone Project Identity & Asset Generation System (PIAGS) — Data Models.

Defines all core schemas, lifecycle states, naming candidates, brand identity,
visual systems, metadata specifications, asset descriptors, and approval gates.
"""
from __future__ import annotations

import enum
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


class IdentityLifecycleState(str, enum.Enum):
    """Canonical lifecycle states for project identity."""
    DRAFT = "DRAFT"
    GENERATING = "GENERATING"
    PENDING_REVIEW = "PENDING_REVIEW"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    FINAL = "FINAL"


class AssetCategory(str, enum.Enum):
    """Asset domain classifications."""
    LOGO = "LOGO"
    APPLICATION_ICON = "APPLICATION_ICON"
    FAVICON = "FAVICON"
    REPOSITORY_BANNER = "REPOSITORY_BANNER"
    SOCIAL_PREVIEW = "SOCIAL_PREVIEW"
    DOCUMENTATION_COVER = "DOCUMENTATION_COVER"
    MARKETING_GRAPHIC = "MARKETING_GRAPHIC"
    BRAND_TOKEN = "BRAND_TOKEN"


class AssetFormat(str, enum.Enum):
    SVG = "svg"
    PNG = "png"
    ICO = "ico"
    JSON = "json"
    MD = "md"


@dataclass
class NameCandidate:
    name: str
    slug: str
    category: str  # technical, abstract, descriptive, brandable
    rationale: str
    tagline: str
    relevance_score: float = 0.9
    memorability_score: float = 0.9
    pronunciation_score: float = 0.9
    is_selected: bool = False


@dataclass
class BrandIdentity:
    brand_id: str
    brand_name: str
    tagline: str
    positioning: str
    mission: str
    vision: str
    values: List[str]
    personality_traits: List[str]
    voice_and_tone: str
    visual_direction: str
    design_principles: List[str]
    target_audience: str
    status: IdentityLifecycleState = IdentityLifecycleState.DRAFT
    version: int = 1


@dataclass
class ColorPalette:
    primary_hex: str
    secondary_hex: str
    accent_hex: str
    background_light: str = "#FFFFFF"
    background_dark: str = "#0F172A"
    surface_light: str = "#F8FAFC"
    surface_dark: str = "#1E293B"
    text_primary_light: str = "#0F172A"
    text_primary_dark: str = "#F8FAFC"
    contrast_ratio_light: float = 14.5
    contrast_ratio_dark: float = 12.8
    wcag_aa_compliant: bool = True


@dataclass
class TypographySystem:
    heading_font: str = "Inter, -apple-system, sans-serif"
    body_font: str = "Inter, -apple-system, sans-serif"
    code_font: str = "JetBrains Mono, Menlo, monospace"
    base_size_px: int = 16
    scale_ratio: float = 1.25
    hierarchy: Dict[str, str] = field(default_factory=lambda: {
        "h1": "2.441rem (39px)",
        "h2": "1.953rem (31px)",
        "h3": "1.563rem (25px)",
        "body": "1.000rem (16px)",
        "caption": "0.800rem (13px)",
    })


@dataclass
class VisualIdentitySystem:
    identity_id: str
    colors: ColorPalette
    typography: TypographySystem
    border_radius_px: int = 8
    shadow_direction: str = "0 4px 6px -1px rgb(0 0 0 / 0.1)"
    spacing_base_px: int = 4
    design_tokens: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectMetadataRecord:
    project_id: str
    project_name: str
    slug: str
    short_description: str
    full_description: str
    tagline: str
    project_category: str
    project_type: str
    target_audience: str
    primary_problem: str
    primary_solution: str
    key_features: List[str]
    brand_identity_id: str
    logo_asset_id: Optional[str] = None
    primary_color: str = "#2563EB"
    secondary_color: str = "#1E293B"
    technology_stack: List[str] = field(default_factory=list)
    project_version: str = "1.0.0"
    license: str = "MIT"
    keywords: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    status: IdentityLifecycleState = IdentityLifecycleState.DRAFT


@dataclass
class AssetDescriptor:
    asset_id: str
    project_id: str
    identity_id: str
    category: AssetCategory
    variant: str  # primary, horizontal, icon_only, dark, light, favicon
    file_name: str
    file_format: AssetFormat
    width: int
    height: int
    storage_path: str
    content: Optional[str] = None  # SVG XML or metadata payload
    is_approved: bool = False
    version: int = 1
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


@dataclass
class IdentityApprovalRecord:
    approval_id: str
    project_id: str
    identity_id: str
    name_approved: bool = False
    brand_approved: bool = False
    logo_approved: bool = False
    metadata_approved: bool = False
    final_package_approved: bool = False
    approver_identity: str = "human_user"
    approval_timestamp: Optional[str] = None
    approval_digest: Optional[str] = None
    revision_notes: List[str] = field(default_factory=list)
