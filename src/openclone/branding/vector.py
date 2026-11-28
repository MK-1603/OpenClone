"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Vector Engine.

Generates genuine, production-grade, editable SVG vector masters for all
logo variants (Primary, Horizontal, Vertical, Symbol, Monochrome, Favicon, Social).
Category-specific vector geometry derived from mathematical rules.
Zero embedded raster images or fake base64 data URIs.
"""

from __future__ import annotations

import html
from typing import Dict, List, Optional

from src.openclone.branding.geometry import GeometryEngine
from src.openclone.branding.models import (
    ColorSpec,
    GeometryRules,
    LogoCategory,
    LogoConcept,
    LogoVariant,
    TypographySpec,
    VariantGeometry,
    VariantType,
)


class VectorAssetEngine:
    """Renders clean, mathematically constructed SVG vector masters across mark categories."""

    @classmethod
    def render_variants(
        cls,
        brand_name: str,
        tagline: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geometry: Optional[GeometryRules] = None,
        typography: Optional[TypographySpec] = None,
    ) -> List[LogoVariant]:
        """Generate all 8 canonical production variants in pure SVG."""
        if geometry is None:
            geometry = GeometryEngine.calculate_rules()

        variants: List[LogoVariant] = []

        # 1. Primary Full Lockup (900x260)
        prim_geom = geometry.variant_geometries.get(
            VariantType.PRIMARY.value,
            VariantGeometry(
                variant_type=VariantType.PRIMARY,
                width=900,
                height=260,
                view_box="0 0 900 260",
                mark_origin_x=40.0,
                mark_origin_y=45.0,
                mark_scale=1.7,
                text_origin_x=250.0,
                text_origin_y=135.0,
                text_font_size=76.0,
                tagline_origin_x=254.0,
                tagline_origin_y=175.0,
                tagline_font_size=20.0,
            ),
        )
        primary_svg = cls._build_primary_lockup(brand_name, tagline, concept, colors, prim_geom, typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.PRIMARY,
                width=900,
                height=260,
                view_box="0 0 900 260",
                svg_content=primary_svg,
                description="Master full lockup with architectural mark, typographic logotype, and tagline.",
                aspect_ratio=round(900 / 260, 2),
                is_monochrome=False,
                target_background="dark",
            )
        )

        # 2. Horizontal Navbar Lockup (500x120)
        horiz_geom = geometry.variant_geometries.get(
            VariantType.HORIZONTAL.value,
            VariantGeometry(
                variant_type=VariantType.HORIZONTAL,
                width=500,
                height=120,
                view_box="0 0 500 120",
                mark_origin_x=20.0,
                mark_origin_y=15.0,
                mark_scale=0.9,
                text_origin_x=135.0,
                text_origin_y=74.0,
                text_font_size=48.0,
            ),
        )
        horizontal_svg = cls._build_horizontal_lockup(brand_name, concept, colors, horiz_geom, typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.HORIZONTAL,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=horizontal_svg,
                description="Horizontal lockup optimized for headers, navigation bars, and docs.",
                aspect_ratio=round(500 / 120, 2),
                is_monochrome=False,
                target_background="any",
            )
        )

        # 3. Vertical Stacked Lockup (320x360)
        vert_geom = geometry.variant_geometries.get(
            VariantType.VERTICAL.value,
            VariantGeometry(
                variant_type=VariantType.VERTICAL,
                width=320,
                height=360,
                view_box="0 0 320 360",
                mark_origin_x=85.0,
                mark_origin_y=40.0,
                mark_scale=1.5,
                text_origin_x=160.0,
                text_origin_y=260.0,
                text_font_size=44.0,
            ),
        )
        vertical_svg = cls._build_vertical_lockup(brand_name, concept, colors, vert_geom, typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.VERTICAL,
                width=320,
                height=360,
                view_box="0 0 320 360",
                svg_content=vertical_svg,
                description="Centered vertical lockup for badges, splash screens, and posters.",
                aspect_ratio=round(320 / 360, 2),
                is_monochrome=False,
                target_background="dark",
            )
        )

        # 4. Symbol Only Mark (200x200)
        sym_geom = geometry.variant_geometries.get(
            VariantType.SYMBOL_ONLY.value,
            VariantGeometry(
                variant_type=VariantType.SYMBOL_ONLY,
                width=200,
                height=200,
                view_box="0 0 200 200",
                mark_origin_x=25.0,
                mark_origin_y=25.0,
                mark_scale=1.5,
                text_origin_x=0.0,
                text_origin_y=0.0,
                text_font_size=0.0,
            ),
        )
        symbol_svg = cls._build_symbol_only(brand_name, concept, colors, sym_geom)
        variants.append(
            LogoVariant(
                variant_type=VariantType.SYMBOL_ONLY,
                width=200,
                height=200,
                view_box="0 0 200 200",
                svg_content=symbol_svg,
                description="Standalone symbol mark for app icons, avatars, and profile images.",
                aspect_ratio=1.0,
                is_monochrome=False,
                target_background="dark",
            )
        )

        # 5. Monochrome Dark (Single-color white on dark 500x120)
        mono_dark_svg = cls._build_monochrome(brand_name, concept, mode="dark", geom=horiz_geom, typography=typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.MONOCHROME_DARK,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=mono_dark_svg,
                description="Pure monochrome white lockup for dark surfaces, etching, and stamps.",
                aspect_ratio=round(500 / 120, 2),
                is_monochrome=True,
                target_background="dark",
            )
        )

        # 6. Monochrome Light (Single-color black on light 500x120)
        mono_light_svg = cls._build_monochrome(brand_name, concept, mode="light", geom=horiz_geom, typography=typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.MONOCHROME_LIGHT,
                width=500,
                height=120,
                view_box="0 0 500 120",
                svg_content=mono_light_svg,
                description="Pure monochrome black lockup for laser cutting, invoices, and 1-bit print.",
                aspect_ratio=round(500 / 120, 2),
                is_monochrome=True,
                target_background="light",
            )
        )

        # 7. Favicon (32x32)
        favicon_svg = cls._build_favicon(brand_name, concept, colors)
        variants.append(
            LogoVariant(
                variant_type=VariantType.FAVICON,
                width=32,
                height=32,
                view_box="0 0 32 32",
                svg_content=favicon_svg,
                description="Micro-scaled 32x32 pixel-grid tuned vector favicon.",
                aspect_ratio=1.0,
                is_monochrome=False,
                target_background="any",
            )
        )

        # 8. Social Preview / OpenGraph Banner (1280x640)
        soc_geom = geometry.variant_geometries.get(
            VariantType.SOCIAL_PREVIEW.value,
            VariantGeometry(
                variant_type=VariantType.SOCIAL_PREVIEW,
                width=1280,
                height=640,
                view_box="0 0 1280 640",
                mark_origin_x=100.0,
                mark_origin_y=180.0,
                mark_scale=2.8,
                text_origin_x=440.0,
                text_origin_y=310.0,
                text_font_size=108.0,
                tagline_origin_x=448.0,
                tagline_origin_y=375.0,
                tagline_font_size=32.0,
            ),
        )
        social_svg = cls._build_social_preview(brand_name, tagline, concept, colors, soc_geom, typography)
        variants.append(
            LogoVariant(
                variant_type=VariantType.SOCIAL_PREVIEW,
                width=1280,
                height=640,
                view_box="0 0 1280 640",
                svg_content=social_svg,
                description="1280x640 GitHub social preview and OpenGraph card with architectural grid.",
                aspect_ratio=2.0,
                is_monochrome=False,
                target_background="dark",
            )
        )

        return variants

    # --- Parametric Symbol Synthesis By Category ---

    @classmethod
    def render_symbol_glyph(
        cls,
        brand_name: str,
        concept: LogoConcept,
        x: float,
        y: float,
        scale: float,
        color1: str,
        color2: str,
        stroke_color: str,
    ) -> str:
        """Render category-specific vector symbol based on the chosen concept."""
        cat = concept.category

        # Extract initials for lettermark / monogram marks
        parts = [p for p in brand_name.split() if p]
        initials = "".join([p[0] for p in parts])[:2].upper()
        if not initials:
            initials = brand_name[:2].upper()

        if cat == LogoCategory.GEOMETRIC_MARK:
            return cls._render_monogram_glyph(initials, x, y, scale, color1, color2, stroke_color)
        elif cat == LogoCategory.EMBLEM:
            return cls._render_emblem_glyph(x, y, scale, color1, color2, stroke_color)
        elif cat == LogoCategory.WORDMARK:
            return cls._render_wordmark_glyph(x, y, scale, color1, color2, stroke_color)
        else:
            # Default COMBINATION_MARK / ABSTRACT_SYMBOL: Isometric Hexagon Prism with Code Glyph
            return cls._render_hexagon_glyph(x, y, scale, color1, color2, stroke_color)

    @staticmethod
    def _render_hexagon_glyph(
        x: float,
        y: float,
        scale: float,
        color1: str,
        color2: str,
        stroke_color: str,
    ) -> str:
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

    @staticmethod
    def _render_monogram_glyph(
        initials: str,
        x: float,
        y: float,
        scale: float,
        color1: str,
        color2: str,
        stroke_color: str,
    ) -> str:
        """Render geometric monogram glyph with intersecting structural planes."""
        safe_init = html.escape(initials)
        return f"""
        <g transform="translate({x}, {y}) scale({scale})">
            <!-- Structural background diamond/rotated square -->
            <rect x="15" y="15" width="70" height="70" rx="16" transform="rotate(45 50 50)" fill="{color1}" opacity="0.92" />
            <!-- Inner geometric facet accent -->
            <path d="M50,15 L85,50 L50,85 Z" fill="{color2}" opacity="0.35" />
            <!-- Dynamic precision border line -->
            <rect x="20" y="20" width="60" height="60" rx="12" transform="rotate(45 50 50)" 
                  fill="none" stroke="{stroke_color}" stroke-width="2.5" opacity="0.8" />
            <!-- Central monogram letters -->
            <text x="50" y="59" text-anchor="middle" font-family="'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif" 
                  font-size="30" font-weight="900" letter-spacing="-0.5" fill="{stroke_color}">
                {safe_init}
            </text>
        </g>
        """.strip()

    @staticmethod
    def _render_emblem_glyph(
        x: float,
        y: float,
        scale: float,
        color1: str,
        color2: str,
        stroke_color: str,
    ) -> str:
        """Render engineering crest & verification seal glyph."""
        return f"""
        <g transform="translate({x}, {y}) scale({scale})">
            <!-- Outer concentric seal -->
            <circle cx="50" cy="50" r="44" fill="{color1}" opacity="0.95" />
            <!-- Inner ring -->
            <circle cx="50" cy="50" r="38" fill="none" stroke="{color2}" stroke-width="2.5" stroke-dasharray="6,3" />
            <!-- Core architectural node circle -->
            <circle cx="50" cy="50" r="28" fill="{color2}" opacity="0.4" />
            <!-- Architectural cross-hair markers -->
            <path d="M50,12 L50,22 M50,78 L50,88 M12,50 L22,50 M78,50 L88,50" 
                  stroke="{stroke_color}" stroke-width="3" stroke-linecap="round" />
            <!-- Core verified checkmark glyph -->
            <path d="M38,50 L46,58 L63,41" 
                  fill="none" stroke="{stroke_color}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        """.strip()

    @staticmethod
    def _render_wordmark_glyph(
        x: float,
        y: float,
        scale: float,
        color1: str,
        color2: str,
        stroke_color: str,
    ) -> str:
        """Render precision typographic terminal glyph."""
        return f"""
        <g transform="translate({x}, {y}) scale({scale})">
            <rect x="10" y="15" width="80" height="70" rx="14" fill="{color1}" />
            <path d="M25,35 L40,50 L25,65" fill="none" stroke="{color2}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="48" y1="65" x2="72" y2="65" stroke="{stroke_color}" stroke-width="5" stroke-linecap="round" />
        </g>
        """.strip()

    # --- Variant SVG Builders ---

    @classmethod
    def _build_primary_lockup(
        cls,
        brand_name: str,
        tagline: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geom: VariantGeometry,
        typography: Optional[TypographySpec] = None,
    ) -> str:
        glyph = cls.render_symbol_glyph(
            brand_name=brand_name,
            concept=concept,
            x=geom.mark_origin_x,
            y=geom.mark_origin_y,
            scale=geom.mark_scale,
            color1=colors.primary_hex,
            color2=colors.accent_hex,
            stroke_color="#FFFFFF",
        )
        safe_name = html.escape(brand_name)
        safe_tagline = html.escape(tagline)
        font_family = typography.primary_fallback_stack if typography else "'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif"

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{geom.view_box}" width="100%" height="100%">
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
    <text x="{geom.text_origin_x}" y="{geom.text_origin_y}" font-family="{font_family}" 
          font-size="{geom.text_font_size}" font-weight="800" letter-spacing="-1.5" fill="#FFFFFF">
        {safe_name}
    </text>
    
    <!-- Tagline -->
    <text x="{geom.tagline_origin_x}" y="{geom.tagline_origin_y}" font-family="{font_family}" 
          font-size="{geom.tagline_font_size}" font-weight="500" letter-spacing="1.2" fill="{colors.accent_hex}">
        {safe_tagline}
    </text>
</svg>"""

    @classmethod
    def _build_horizontal_lockup(
        cls,
        brand_name: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geom: VariantGeometry,
        typography: Optional[TypographySpec] = None,
    ) -> str:
        glyph = cls.render_symbol_glyph(
            brand_name=brand_name,
            concept=concept,
            x=geom.mark_origin_x,
            y=geom.mark_origin_y,
            scale=geom.mark_scale,
            color1=colors.primary_hex,
            color2=colors.accent_hex,
            stroke_color="#FFFFFF",
        )
        safe_name = html.escape(brand_name)
        font_family = typography.primary_fallback_stack if typography else "'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif"

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{geom.view_box}" width="100%" height="100%">
    <rect width="100%" height="100%" fill="transparent" />
    {glyph}
    <text x="{geom.text_origin_x}" y="{geom.text_origin_y}" font-family="{font_family}" 
          font-size="{geom.text_font_size}" font-weight="800" letter-spacing="-1" fill="#FFFFFF">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_vertical_lockup(
        cls,
        brand_name: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geom: VariantGeometry,
        typography: Optional[TypographySpec] = None,
    ) -> str:
        glyph = cls.render_symbol_glyph(
            brand_name=brand_name,
            concept=concept,
            x=geom.mark_origin_x,
            y=geom.mark_origin_y,
            scale=geom.mark_scale,
            color1=colors.primary_hex,
            color2=colors.accent_hex,
            stroke_color="#FFFFFF",
        )
        safe_name = html.escape(brand_name)
        font_family = typography.primary_fallback_stack if typography else "'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif"

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{geom.view_box}" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" rx="16" />
    {glyph}
    <text x="{geom.text_origin_x}" y="{geom.text_origin_y}" text-anchor="middle" font-family="{font_family}" 
          font-size="{geom.text_font_size}" font-weight="800" letter-spacing="-1" fill="#FFFFFF">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_symbol_only(
        cls,
        brand_name: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geom: VariantGeometry,
    ) -> str:
        glyph = cls.render_symbol_glyph(
            brand_name=brand_name,
            concept=concept,
            x=geom.mark_origin_x,
            y=geom.mark_origin_y,
            scale=geom.mark_scale,
            color1=colors.primary_hex,
            color2=colors.accent_hex,
            stroke_color="#FFFFFF",
        )
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{geom.view_box}" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" rx="24" />
    {glyph}
</svg>"""

    @classmethod
    def _build_monochrome(
        cls,
        brand_name: str,
        concept: LogoConcept,
        mode: str = "dark",
        geom: Optional[VariantGeometry] = None,
        typography: Optional[TypographySpec] = None,
    ) -> str:
        bg = "#000000" if mode == "dark" else "#FFFFFF"
        fg = "#FFFFFF" if mode == "dark" else "#000000"
        x = geom.mark_origin_x if geom else 20.0
        y = geom.mark_origin_y if geom else 15.0
        scale = geom.mark_scale if geom else 0.9
        tx = geom.text_origin_x if geom else 135.0
        ty = geom.text_origin_y if geom else 74.0
        fs = geom.text_font_size if geom else 48.0
        glyph = cls.render_symbol_glyph(brand_name, concept, x, y, scale, fg, fg, bg)
        safe_name = html.escape(brand_name)
        font_family = typography.primary_fallback_stack if typography else "'Plus Jakarta Sans', 'Inter', sans-serif"

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 120" width="100%" height="100%">
    <rect width="100%" height="100%" fill="{bg}" />
    {glyph}
    <text x="{tx}" y="{ty}" font-family="{font_family}" 
          font-size="{fs}" font-weight="800" fill="{fg}">
        {safe_name}
    </text>
</svg>"""

    @classmethod
    def _build_favicon(
        cls,
        brand_name: str,
        concept: LogoConcept,
        colors: ColorSpec,
    ) -> str:
        cat = concept.category
        if cat == LogoCategory.GEOMETRIC_MARK:
            # Monogram letter tuned for 32x32
            initial = brand_name[0].upper() if brand_name else "O"
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
    <rect x="2" y="2" width="28" height="28" rx="6" fill="{colors.primary_hex}" />
    <text x="16" y="23" text-anchor="middle" font-family="'Plus Jakarta Sans', 'Inter', sans-serif" 
          font-size="18" font-weight="900" fill="#FFFFFF">{initial}</text>
</svg>"""
        elif cat == LogoCategory.EMBLEM:
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
    <circle cx="16" cy="16" r="14" fill="{colors.primary_hex}" />
    <circle cx="16" cy="16" r="10" fill="none" stroke="{colors.accent_hex}" stroke-width="1.5" />
    <path d="M12,16 L15,19 L21,13" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" />
</svg>"""
        else:
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
    <polygon points="16,2 29,9 29,23 16,30 3,23 3,9" fill="{colors.primary_hex}" />
    <path d="M12,14 L8,16 L12,18 M20,14 L24,16 L20,18" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" />
</svg>"""

    @classmethod
    def _build_social_preview(
        cls,
        brand_name: str,
        tagline: str,
        concept: LogoConcept,
        colors: ColorSpec,
        geom: VariantGeometry,
        typography: Optional[TypographySpec] = None,
    ) -> str:
        glyph = cls.render_symbol_glyph(
            brand_name=brand_name,
            concept=concept,
            x=geom.mark_origin_x,
            y=geom.mark_origin_y,
            scale=geom.mark_scale,
            color1=colors.primary_hex,
            color2=colors.accent_hex,
            stroke_color="#FFFFFF",
        )
        safe_name = html.escape(brand_name)
        safe_tagline = html.escape(tagline)
        font_family = typography.primary_fallback_stack if typography else "'Plus Jakarta Sans', 'Inter', sans-serif"

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{geom.view_box}" width="{geom.width}" height="{geom.height}">
    <rect width="100%" height="100%" fill="{colors.neutral_dark_hex}" />
    <!-- Fine geometric backdrop grid -->
    <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="1" opacity="0.3"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)" />
    
    <!-- Accent Watermark Backdrop -->
    <circle cx="950" cy="320" r="280" fill="{colors.primary_hex}" opacity="0.08" />
    
    <!-- Primary Symbol -->
    {glyph}
    
    <!-- Typographic Title -->
    <text x="{geom.text_origin_x}" y="{geom.text_origin_y}" font-family="{font_family}" 
          font-size="{geom.text_font_size}" font-weight="800" letter-spacing="-2" fill="#FFFFFF">
        {safe_name}
    </text>
    
    <!-- Tagline -->
    <text x="{geom.tagline_origin_x}" y="{geom.tagline_origin_y}" font-family="{font_family}" 
          font-size="{geom.tagline_font_size}" font-weight="500" letter-spacing="1.5" fill="{colors.accent_hex}">
        {safe_tagline}
    </text>
    
    <!-- Frame border -->
    <rect x="2" y="2" width="{geom.width - 4}" height="{geom.height - 4}" fill="none" stroke="#334155" stroke-width="2" rx="8" />
</svg>"""
