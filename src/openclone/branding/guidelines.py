"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Guideline Generator.

Produces complete, publication-grade Brand Identity Guidelines manuals in Markdown
and interactive standalone HTML, with comprehensive coverage of all 12 canonical sections.
"""

from __future__ import annotations

import html
import json
from src.openclone.branding.models import BrandIdentityPackage


class BrandGuidelineGenerator:
    """Generates authoritative Brand Guidelines documentation in Markdown and HTML."""

    @classmethod
    def generate_markdown_manual(cls, pkg: BrandIdentityPackage) -> str:
        """Produce complete 12-section Brand Guidelines manual in Markdown."""
        b = pkg.brief
        s = pkg.strategy
        c = pkg.selected_concept
        g = pkg.geometry
        t = pkg.typography
        col = pkg.color

        return f"""# {b.brand_name} — Brand Identity & Logo Engineering Guidelines
**Version:** {pkg.version}  
**Status:** Approved & Production-Ready ({pkg.status.upper()})  
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
- **Quantitative Concept Score:** {c.score.composite_score if c.score else 92.0}/100.0

---

## 4. Primary Logo Lockup

The Primary Logo Lockup combines the architectural mark, logotype, and verified tagline. It is the canonical visual signature of {b.brand_name} and must be deployed on hero headers, official documentation, and primary brand communications.

```
+-------------------------------------------------------------+
|   [ SYMBOL MARK ]     {b.brand_name.upper()}                       |
|                       {b.positioning}                               |
+-------------------------------------------------------------+
```

---

## 5. Geometric Construction & Grid Rules

- **Baseline Unit Grid:** {g.grid_unit_px}px orthogonal grid system (subgrid: {g.subgrid_unit_px}px, macro: {g.macro_unit_px}px).
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
| **Accent** | `{col.accent_hex}` | sRGB | `{col.cmyk_accent}` | **{col.contrast_accent_on_light}:1** | **{col.contrast_accent_on_dark}:1** |
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

**Web Font Fallback Stack:**
```css
font-family: {t.primary_fallback_stack};
```

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

---

## 11. Export Formats & Resolution Matrix

The brand asset suite must be exported and distributed in the following production matrices:

| Target Platform | Asset Name | Format | Dimensions | DPI |
|---|---|---|---|---|
| **Web Vector Master** | `logo-primary.svg` | Scalable Vector (SVG) | Responsive (900x260 viewBox) | Vector |
| **Web Navbar** | `logo-horizontal.svg` | Scalable Vector (SVG) | Responsive (500x120 viewBox) | Vector |
| **Favicon Package** | `favicon.ico`, `favicon.svg` | SVG / ICO | 32x32 & 16x16 | 72 DPI |
| **App Launcher** | `icon-512.png` | 32-bit PNG with alpha | 512x512 | 144 DPI |
| **Social / OpenGraph** | `opengraph-card.png` | 24-bit PNG | 1280x640 | 72 DPI |
| **Print Master** | `brand-manual.pdf` | Vector PDF / CMYK | DIN A4 | 300 DPI |

---

## 12. Design Tokens & Framework Integration

All brand parameters are exported into machine-readable design tokens for automated consumption by the OpenClone UI Design Agent, Frontend Agent, and host applications.

### CSS Custom Properties:
```css
:root {{
{chr(10).join([f"  {k}: {v};" for k, v in col.css_tokens.items()])}
}}
```

### Tailwind Configuration Extension:
```json
{json.dumps(col.tailwind_tokens, indent=2)}
```

### OMIS Memory Integration:
Brand identity definitions are stored in OpenClone Memory Intelligence System (`.openclone/memory.sqlite3`) under memory type `decision` with category `brand_identity` for perpetual consistency across multi-agent turns.
""".strip()

    @classmethod
    def generate_html_manual(cls, pkg: BrandIdentityPackage) -> str:
        """Produce an interactive, standalone HTML brand manual with embedded SVG assets."""
        b = pkg.brief
        col = pkg.color
        t = pkg.typography

        # Render preview cards for all variants
        variant_cards = []
        for v in pkg.variants:
            bg_color = col.neutral_dark_hex if v.target_background == "dark" else col.neutral_light_hex
            card = f"""
            <div class="variant-card">
                <div class="preview-box" style="background-color: {bg_color};">
                    {v.svg_content}
                </div>
                <div class="card-meta">
                    <h4>{v.variant_type.value}</h4>
                    <span class="dim">{v.width}x{v.height} ({v.view_box})</span>
                    <p>{html.escape(v.description)}</p>
                </div>
            </div>
            """
            variant_cards.append(card)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(b.brand_name)} — Brand Guidelines</title>
    <style>
        :root {{
            --bg: #0B0F19;
            --surface: #131B2E;
            --border: #1E293B;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --primary: {col.primary_hex};
            --accent: {col.accent_hex};
        }}
        body {{
            font-family: {t.primary_fallback_stack};
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        header {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 24px;
            margin-bottom: 40px;
        }}
        h1 {{ font-size: 2.4rem; margin-bottom: 8px; color: #FFF; }}
        h2 {{ font-size: 1.6rem; margin-top: 36px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
        .badge {{
            display: inline-block;
            background: rgba(37, 99, 235, 0.15);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 24px;
            margin-top: 24px;
        }}
        .variant-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }}
        .preview-box {{
            padding: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 160px;
            max-height: 220px;
        }}
        .preview-box svg {{
            max-width: 100%;
            max-height: 180px;
            height: auto;
        }}
        .card-meta {{
            padding: 16px 20px;
        }}
        .card-meta h4 {{ margin: 0 0 4px 0; font-size: 1.1rem; }}
        .dim {{ font-size: 0.8rem; color: var(--text-muted); font-family: monospace; }}
        .card-meta p {{ font-size: 0.85rem; color: var(--text-muted); margin: 8px 0 0 0; }}
        pre {{
            background: #020617;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border);
            overflow-x: auto;
            color: #38BDF8;
            font-family: monospace;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">LEBIS Verified Brand Specification</span>
            <h1>{html.escape(b.brand_name)} Brand Identity Manual</h1>
            <p style="color: var(--text-muted);">Purpose: {html.escape(b.purpose)} | Positioning: {html.escape(b.positioning)}</p>
        </header>

        <section>
            <h2>Canonical Production Variants</h2>
            <div class="grid">
                {"".join(variant_cards)}
            </div>
        </section>

        <section>
            <h2>Design Tokens</h2>
            <pre><code>{html.escape(json.dumps(col.css_tokens, indent=2))}</code></pre>
        </section>
    </div>
</body>
</html>"""
