"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Vector Engine.

Generates genuine, production-grade, editable SVG vector masters for all
logo variants (Primary, Horizontal, Vertical, Symbol, Monochrome, Favicon, Social).
Zero embedded raster images or fake base64 data URIs.
"""

from __future__ import annotations

import html
from typing import Dict, List

from src.openclone.branding.models import (
    ColorSpec,
    LogoConcept,
    LogoVariant,
    VariantType,
)


class VectorAssetEngine:
    """Renders clean, mathematically constructed SVG vector masters."""

    @classmethod
    def render_variants(
        cls,
        brand_name: str,
        tagline: str,
        concept: LogoConcept,
        colors: ColorSpec,
    ) -> List[LogoVariant]:
        """Generate all canonical production variants in pure SVG."""
        variants: List[LogoVariant] = []

        # 1. Primary Full Lockup (900x260)
        primary_svg = cls._build_primary_lockup(brand_name, tagline, colors)
        variants.append(
            LogoVariant(
                variant_type=VariantType.PRIMARY,
                width=900,
                height=260,
                view_box="0 0 900 260",
                svg_content=primary_svg,
                description="Master full lockup with isometric mark, typographic logotype, and tagline.",
            )
        )

        # 2. Horizontal Navbar Lockup (500x120)
        horizontal_svg = cls._build_horizontal_lockup(brand_name, colors)
        variants.append(
            LogoVariant(
                variant_type=VariantType.HORIZONTAL,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=horizontal_svg,
                description="Horizontal lockup optimized for headers, navigation bars, and docs.",
            )
        )

        # 3. Vertical Stacked Lockup (320x360)
        vertical_svg = cls._build_vertical_lockup(brand_name, colors)
        variants.append(
            LogoVariant(
                variant_type=VariantType.VERTICAL,
                width=320,
                height=360,
                view_box="0 0 320 360",
                svg_content=vertical_svg,
                description="Centered vertical lockup for badges, splash screens, and posters.",
            )
        )

        # 4. Symbol Only Mark (200x200)
        symbol_svg = cls._build_symbol_only(colors.primary_hex, colors.accent_hex, colors.secondary_hex)
        variants.append(
            LogoVariant(
                variant_type=VariantType.SYMBOL_ONLY,
                width=200,
                height=200,
                view_box="0 0 200 200",
                svg_content=symbol_svg,
                description="Standalone symbol mark for app icons, avatars, and profile images.",
            )
        )

        # 5. Monochrome Dark (Single-color white on dark)
        mono_dark_svg = cls._build_monochrome(brand_name, mode="dark")
        variants.append(
            LogoVariant(
                variant_type=VariantType.MONOCHROME_DARK,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=mono_dark_svg,
                description="Pure monochrome white lockup for dark surfaces, etching, and stamps.",
            )
        )

        # 6. Monochrome Light (Single-color black on light)
        mono_light_svg = cls._build_monochrome(brand_name, mode="light")
        variants.append(
            LogoVariant(
                variant_type=VariantType.MONOCHROME_LIGHT,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=mono_light_svg,
                description="Pure monochrome black lockup for laser cutting, invoices, and 1-bit print.",
            )
        )

        # 7. Favicon (32x32)
        favicon_svg = cls._build_favicon(colors.primary_hex, colors.accent_hex)
        variants.append(
            LogoVariant(
                variant_type=VariantType.FAVICON,
                width=32,
                height=32,
                view_box="0 0 32 32",
                svg_content=favicon_svg,
                description="Micro-scaled 32x32 pixel-grid tuned vector favicon.",
            )
        )

        # 8. Social Preview / OpenGraph Banner (1280x640)
        social_svg = cls._build_social_preview(brand_name, tagline, colors)
        variants.append(
            LogoVariant(
                variant_type=VariantType.SOCIAL_PREVIEW,
                width=1280,
                height=640,
                view_box="0 0 1280 640",
                svg_content=social_svg,
                description="1280x640 GitHub social preview and OpenGraph card with architectural grid.",
            )
        )

        return variants

    # --- SVG Template Builders ---

    @staticmethod
    def _render_hexagon_glyph(x: float, y: float, scale: float, color1: str, color2: str, stroke_color: str) -> str:
        """Render isometric hexagonal prism glyph."""
        return f"""
        <g transform="translate({x}, {y}) scale({scale})">
            <!-- Hexagonal outer frame -->
            <polygon points="50,5 92,27 92,73 50,95 8,73 8,27" fill="{color1}" opacity="0.95" />
            <!-- Inner facet bevels -->
            <polygon points="50,5 92,27 50,50 8,27" fill="{color2}" opacity="0.4" />
            <polygon points="8,27 50,50 50,95 8,73" fill="#000000" opacity="0.25" />
            <polygon points="50,50 92,27 92,73 50,95" fill="{color2}" opacity="0.15" />
            <!-- Code brackets glyph </ > -->
            <path d="M38,42 L28,50 L38,58 M62,42 L72,50 L62,58 M54,38 L46,62" 
                  fill="none" stroke="{stroke_color}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        """.strip()

    @classmethod
    def _build_primary_lockup(cls, brand_name: str, tagline: str, colors: ColorSpec) -> str:
        glyph = cls._render_hexagon_glyph(40, 45, 1.7, colors.primary_hex, colors.accent_hex, "#FFFFFF")
        safe_name = html.escape(brand_name)
        safe_tagline = html.escape(tagline)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="100%" height="100%">
    <defs>
        <linearGradient id="primary-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{colors.primary_hex}" />
            <stop offset="100%" stop-color="{colors.accent_hex}" />
        </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" />
    <!-- Architectural grid pattern -->
    <path d="M0,130 L900,130 M220,0 L220,260" stroke="#1E293B" stroke-width="1" stroke-dasharray="4,4" opacity="0.4" />
    
    <!-- Symbol Mark -->
    {glyph}
    
    <!-- Typographic Logotype -->
    <text x="250" y="135" font-family="'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif" 
          font-size="76" font-weight="800" letter-spacing="-1.5" fill="#FFFFFF">
        {safe_name}
    </text>
    
    <!-- Tagline -->
    <text x="254" y="175" font-family="'Inter', -apple-system, sans-serif" 
          font-size="20" font-weight="500" letter-spacing="1.2" fill="{colors.accent_hex}">
        {safe_tagline}
    </text>
</svg>"""

    @classmethod
    def _build_horizontal_lockup(cls, brand_name: str, colors: ColorSpec) -> str:
        glyph = cls._render_hexagon_glyph(20, 15, 0.9, colors.primary_hex, colors.accent_hex, "#FFFFFF")
        safe_name = html.escape(brand_name)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 120" width="100%" height="100%">
    <rect width="100%" height="100%" fill="transparent" />
    {glyph}
    <text x="135" y="74" font-family="'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif" 
          font-size="48" font-weight="800" letter-spacing="-1" fill="#FFFFFF">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_vertical_lockup(cls, brand_name: str, colors: ColorSpec) -> str:
        glyph = cls._render_hexagon_glyph(85, 40, 1.5, colors.primary_hex, colors.accent_hex, "#FFFFFF")
        safe_name = html.escape(brand_name)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 360" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" rx="16" />
    {glyph}
    <text x="160" y="260" text-anchor="middle" font-family="'Plus Jakarta Sans', 'Inter', sans-serif" 
          font-size="44" font-weight="800" letter-spacing="-1" fill="#FFFFFF">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_symbol_only(cls, color1: str, color2: str, bg: str) -> str:
        glyph = cls._render_hexagon_glyph(25, 25, 1.5, color1, color2, "#FFFFFF")
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{bg}" rx="24" />
    {glyph}
</svg>"""

    @classmethod
    def _build_monochrome(cls, brand_name: str, mode: str = "dark") -> str:
        bg = "#000000" if mode == "dark" else "#FFFFFF"
        fg = "#FFFFFF" if mode == "dark" else "#000000"
        glyph = cls._render_hexagon_glyph(20, 15, 0.9, fg, fg, bg)
        safe_name = html.escape(brand_name)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 120" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{bg}" />
    {glyph}
    <text x="135" y="74" font-family="'Plus Jakarta Sans', 'Inter', sans-serif" 
          font-size="48" font-weight="800" fill="{fg}">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_favicon(cls, color1: str, color2: str) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
    <polygon points="16,2 29,9 29,23 16,30 3,23 3,9" fill="{color1}" />
    <path d="M12,14 L8,16 L12,18 M20,14 L24,16 L20,18" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" />
</svg>"""

    @classmethod
    def _build_social_preview(cls, brand_name: str, tagline: str, colors: ColorSpec) -> str:
        glyph = cls._render_hexagon_glyph(100, 180, 2.8, colors.primary_hex, colors.accent_hex, "#FFFFFF")
        safe_name = html.escape(brand_name)
        safe_tagline = html.escape(tagline)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" />
    <!-- Fine geometric backdrop grid -->
    <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="1" opacity="0.3"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)" />
    
    <!-- Hexagonal Watermark Backdrop -->
    <circle cx="950" cy="320" r="280" fill="{colors.primary_hex}" opacity="0.08" />
    
    <!-- Primary Symbol -->
    {glyph}
    
    <!-- Typographic Title -->
    <text x="440" y="310" font-family="'Plus Jakarta Sans', 'Inter', sans-serif" 
          font-size="108" font-weight="800" letter-spacing="-2" fill="#FFFFFF">
        {safe_name}
    </text>
    
    <!-- Tagline -->
    <text x="448" y="375" font-family="'Inter', sans-serif" 
          font-size="32" font-weight="500" letter-spacing="1.5" fill="{colors.accent_hex}">
        {safe_tagline}
    </text>
    
    <!-- Frame border -->
    <rect x="2" y="2" width="1276" height="636" fill="none" stroke="#334155" stroke-width="2" rx="8" />
</svg>"""
