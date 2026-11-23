"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Guideline Generator.

Produces complete, publication-grade Brand Identity Guidelines manuals in Markdown.
"""

from __future__ import annotations

from src.openclone.branding.models import BrandIdentityPackage


class BrandGuidelineGenerator:
    """Generates authoritative Brand Guidelines documentation."""

    @classmethod
    def generate_markdown_manual(cls, pkg: BrandIdentityPackage) -> str:
        """Produce complete 12-section Brand Guidelines manual."""
        b = pkg.brief
        s = pkg.strategy
        c = pkg.selected_concept
        g = pkg.geometry
        t = pkg.typography
        col = pkg.color

        return f"""# {b.brand_name} — Brand Identity & Logo Engineering Guidelines
**Version:** 1.0.0  
**Status:** Approved & Production-Ready  
**Engineered by:** OpenClone Logo Engineering & Brand Identity System (LEBIS)  

---

## 1. Brand Overview & Mission

{b.brand_name} is an authoritative {b.category} engineered for {b.target_audience}.

> **Core Purpose:** {b.purpose}  
> **Brand Values:** {', '.join(b.brand_values)}  
> **Personality Attributes:** {', '.join(b.personality_traits)}  

---

## 2. Strategic Positioning & Archetype

- **Positioning Statement:** {s.positioning_statement}
- **Brand Archetype:** {s.brand_archetype}
- **Core Differentiation:**
{chr(10).join([f"  - {d}" for d in s.differentiation_factors])}

---

## 3. Logo Concept & Design Intent

- **Concept Name:** {c.name} (`{c.concept_id}`)
- **Logo Category:** `{c.category.value}`
- **Design Intention:** {c.design_intention}
- **Brand Meaning:** {c.brand_meaning}
- **Symbol Construction:** {c.symbol_construction}

---

## 4. Primary Logo Lockup

The Primary Logo Lockup combines the architectural mark, logotype, and verified tagline. It is the canonical visual signature of {b.brand_name} and must be deployed on hero headers, official documentation, and primary brand communications.

```
+-------------------------------------------------------------+
|   [ HEXAGON PRISM ]   {b.brand_name.upper()}                       |
|                       {b.positioning}                               |
+-------------------------------------------------------------+
```

---

## 5. Geometric Construction & Grid Rules

- **Baseline Unit Grid:** {g.grid_unit_px}px orthogonal grid system.
- **Proportion Ratio:** {g.proportion_ratio_name} ($1 : {g.proportion_ratio_value}$).
- **Symmetry & Balance:** {g.symmetry_notes}
- **Clear-Space Rule:** Maintain an exclusion buffer around all edges of the mark equal to at least **{int(g.clear_space_factor * 100)}% of the mark's height** ($X$-height clearance). No text, borders, or graphics may encroach within this zone.
- **Minimum Digital Dimensions:** {g.min_digital_width_px}px width for screen displays.
- **Minimum Physical Dimensions:** {g.min_print_width_mm}mm width for offset or digital print.

---

## 6. Color Intelligence & Accessibility System

All colors are mathematically calculated and verified for WCAG 2.1 accessibility compliance.

| Palette Role | Hex Code | sRGB Formulation | CMYK Formulation | Contrast on Light | Contrast on Dark |
|---|---|---|---|---|---|
| **Primary** | `{col.primary_hex}` | sRGB | `{col.cmyk_primary}` | **{col.contrast_primary_on_light}:1** | **{col.contrast_primary_on_dark}:1** |
| **Secondary** | `{col.secondary_hex}` | sRGB | `{col.cmyk_secondary}` | High | High |
| **Accent** | `{col.accent_hex}` | sRGB | Electric Cyan | High | Extreme |
| **Dark Neutral** | `{col.neutral_dark_hex}` | Canvas | Black/Navy | — | Reference Dark |
| **Light Neutral**| `{col.neutral_light_hex}`| Canvas | Pure White | Reference Light | — |

*Compliance Statement:* {col.wcag_compliance}

---

## 7. Typography System

The typographic system provides clear hierarchy, high micro-scale legibility, and permissive commercial licensing.

| Role | Font Family | Classification | Hierarchy / Scale | License |
|---|---|---|---|---|
| **Primary Logotype** | `{t.primary_font}` | {t.primary_classification} | Title Display (`letter-spacing: {t.letter_spacing_logotype}`) | {t.licensing} |
| **Secondary Tagline**| `{t.secondary_font}` | {t.secondary_classification} | Sub-heading (`letter-spacing: {t.letter_spacing_tagline}`) | Permissive Commercial |
| **Code & Technical** | JetBrains Mono / Fira Code | Monospace | Tabular & Data | SIL Open Font License |

---

## 8. Approved Logo Variations

| Variant | Resolution | Canonical Use Case |
|---|---|---|
| `PRIMARY` | 900x260 | Hero documentation headers, marketing banners, splash pages. |
| `HORIZONTAL` | 500x120 | Desktop navigation bars, sticky headers, documentation sidebars. |
| `VERTICAL` | 320x360 | Mobile splash screens, badge cards, exhibition signage. |
| `SYMBOL_ONLY` | 200x200 | Social avatars, profile pictures, application launcher icons. |
| `MONOCHROME_DARK` | 500x120 | Single-color laser etching, dark fabric embroidery, stencil work. |
| `MONOCHROME_LIGHT`| 500x120 | Black-and-white print, official stationery, invoices. |
| `FAVICON` | 32x32 | Browser tab icons, PWA manifests, IDE window badges. |
| `SOCIAL_PREVIEW` | 1280x640 | GitHub social card, Twitter/LinkedIn OpenGraph card. |

---

## 9. Incorrect Usage & Anti-Slop Rules

To maintain brand dignity, the following treatments are **strictly prohibited**:

1. **NO Generic AI Glow Blobs:** Do not add diffuse neon gradients or purple/cyan fog behind the mark.
2. **NO Aspect Ratio Distortion:** Never stretch, compress, skew, or shear the logo. Always scale proportionally.
3. **NO Unauthorized Palettes:** Do not recolor facets with unapproved random hues.
4. **NO Low-Contrast Canvases:** Do not place the primary logo on mid-tone grey backgrounds where contrast drops below 3.0:1.
5. **NO Dropshadow Clutter:** Do not apply heavy 2000s-era Gaussian drop-shadows.

---

## 10. Vector Master Specifications

All master assets are generated as standard-compliant, editable SVG:
- Vector standard: W3C SVG 1.1 / SVG 2.0 with valid `viewBox`.
- Encoding: UTF-8 without BOM.
- Purity: Zero embedded base64 raster blobs; 100% genuine vector geometry.
- Portability: Renderable across web browsers, Node.js, Python, Figma, and Inkscape.
""".strip()
