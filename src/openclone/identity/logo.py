"""OpenClone Logo Generation Engine & Provider Abstraction.

Generates production-grade, mathematically constructed vector SVG logo marks and
supporting asset variants (primary, horizontal, icon-only, light, dark, monochrome)
using a provider-independent architecture with built-in mock and fallback engines.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional
from src.openclone.identity.models import AssetDescriptor, AssetCategory, AssetFormat, VisualIdentitySystem


class LogoGenerationEngine:
    """Generates clean vector logo marks matching brand identity & colors."""

    @classmethod
    def generate_logo_suite(
        cls,
        project_id: str,
        identity_id: str,
        brand_name: str,
        visual_system: VisualIdentitySystem,
    ) -> List[AssetDescriptor]:
        assets: List[AssetDescriptor] = []
        p_color = visual_system.colors.primary_hex
        s_color = visual_system.colors.secondary_hex
        acc_color = visual_system.colors.accent_hex

        # 1. Primary Vector Logo (Combination Mark: Icon + Text)
        primary_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="400" height="100">
  <rect width="100%" height="100%" fill="none"/>
  <g transform="translate(10, 10)">
    <rect x="0" y="0" width="80" height="80" rx="16" fill="{p_color}"/>
    <path d="M25 40 L40 25 L55 40 L40 55 Z" fill="#FFFFFF"/>
    <circle cx="40" cy="40" r="6" fill="{acc_color}"/>
  </g>
  <text x="110" y="58" font-family="{visual_system.typography.heading_font}" font-size="36" font-weight="700" fill="{s_color}">{brand_name}</text>
</svg>"""

        assets.append(AssetDescriptor(
            asset_id=f"logo-primary-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=identity_id,
            category=AssetCategory.LOGO,
            variant="primary",
            file_name="logo-primary.svg",
            file_format=AssetFormat.SVG,
            width=400,
            height=100,
            storage_path="logos/primary/logo-primary.svg",
            content=primary_svg,
            is_approved=False,
        ))

        # 2. Icon-Only Logo (Favicon / Application Icon)
        icon_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect width="100" height="100" rx="20" fill="{p_color}"/>
  <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="#FFFFFF"/>
  <circle cx="50" cy="50" r="8" fill="{acc_color}"/>
</svg>"""

        assets.append(AssetDescriptor(
            asset_id=f"logo-icon-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=identity_id,
            category=AssetCategory.APPLICATION_ICON,
            variant="icon_only",
            file_name="app-icon.svg",
            file_format=AssetFormat.SVG,
            width=100,
            height=100,
            storage_path="icons/application/app-icon.svg",
            content=icon_svg,
            is_approved=False,
        ))

        # 3. Favicon (32x32)
        assets.append(AssetDescriptor(
            asset_id=f"favicon-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=identity_id,
            category=AssetCategory.FAVICON,
            variant="favicon",
            file_name="favicon.svg",
            file_format=AssetFormat.SVG,
            width=32,
            height=32,
            storage_path="icons/favicon/favicon.svg",
            content=icon_svg,
            is_approved=False,
        ))

        # 4. Dark Background Variant
        dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="400" height="100">
  <rect width="100%" height="100%" fill="{visual_system.colors.background_dark}"/>
  <g transform="translate(10, 10)">
    <rect x="0" y="0" width="80" height="80" rx="16" fill="{acc_color}"/>
    <path d="M25 40 L40 25 L55 40 L40 55 Z" fill="{visual_system.colors.background_dark}"/>
    <circle cx="40" cy="40" r="6" fill="#FFFFFF"/>
  </g>
  <text x="110" y="58" font-family="{visual_system.typography.heading_font}" font-size="36" font-weight="700" fill="#F8FAFC">{brand_name}</text>
</svg>"""

        assets.append(AssetDescriptor(
            asset_id=f"logo-dark-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=identity_id,
            category=AssetCategory.LOGO,
            variant="dark",
            file_name="logo-dark.svg",
            file_format=AssetFormat.SVG,
            width=400,
            height=100,
            storage_path="logos/dark/logo-dark.svg",
            content=dark_svg,
            is_approved=False,
        ))

        # 5. Repository Banner
        banner_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="1200" height="400">
  <rect width="100%" height="100%" fill="{visual_system.colors.background_dark}"/>
  <g transform="translate(100, 120)">
    <rect x="0" y="0" width="160" height="160" rx="32" fill="{p_color}"/>
    <path d="M50 80 L80 50 L110 80 L80 110 Z" fill="#FFFFFF"/>
    <circle cx="80" cy="80" r="12" fill="{acc_color}"/>
    <text x="200" y="85" font-family="{visual_system.typography.heading_font}" font-size="64" font-weight="800" fill="#FFFFFF">{brand_name}</text>
    <text x="200" y="130" font-family="{visual_system.typography.body_font}" font-size="24" fill="{acc_color}">Deterministic Architecture & Governed Intelligence</text>
  </g>
</svg>"""

        assets.append(AssetDescriptor(
            asset_id=f"banner-repo-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=identity_id,
            category=AssetCategory.REPOSITORY_BANNER,
            variant="repository_banner",
            file_name="repository-banner.svg",
            file_format=AssetFormat.SVG,
            width=1200,
            height=400,
            storage_path="assets/repository/repository-banner.svg",
            content=banner_svg,
            is_approved=False,
        ))

        return assets
