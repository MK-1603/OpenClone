# OpenClone Brand Assets

**OpenClone** — Open-source AI Software Development Framework (AISDF) · v1.0.0
**Tagline:** Engineering Intelligence, Openly.

## Brand concept
The symbol is a geometric **OC monogram** built on a hexagon (engineering / structure):
- **O** — the hexagonal ring is the open core.
- **C** — the right side is left open; two **mirrored gold terminals** (top and bottom) form the "C" and signal *openness* and extensibility.
- **Modular core** — the isometric cube in the centre is a reusable component / building block (blueprints, agents, skills, adapters).
Flat vector construction only: no gradients, shadows or glow.

## Colour palette
| Name | HEX | Use |
|---|---|---|
| Gold | `#FACC15` | Accent: terminals, "C" in wordmark, gold icon background |
| Near-black | `#0B0B0B` | Dark backgrounds, wordmark on light |
| White | `#FFFFFF` | Wordmark on dark, light backgrounds |
| Silver (optional) | `#A1A1AA` | Cube shaded face, tagline on dark |

## Typography
- **Wordmark:** Space Grotesk Bold (700), converted to outlines — no font install needed. The "C" is gold.
- **Tagline / supporting:** Inter Medium (outlined in logo files). Use Inter for UI and documentation.
- Spelling is always **OpenClone** (capital O and C). Tagline is exactly *Engineering Intelligence, Openly.*

## Which logo where
| Background | Use |
|---|---|
| Dark / near-black | `logo/dark/openclone-logo-dark.*`, `logo/symbol/openclone-symbol-dark.*`, `lockups/*-dark.*` |
| White / light | `logo/light/openclone-logo-light.*`, `logo/symbol/openclone-symbol-light.*`, `lockups/*-light.*` |
| Gold | `extensions/*-gold` icon (mark is near-black) |

Lockups: **horizontal** = symbol + wordmark + tagline; **stacked** = symbol over wordmark over tagline. Use the primary logo (no tagline) when the logo is small.
The dark-theme PNGs are white on transparent — they look blank on white viewers; that is expected.

## Extension / platform icons
`extensions/png/<size>/openclone-extension-{dark,light,gold}-<size>.png` — sizes 16, 32, 48, 64, 128, 256, 512 (scalable masters in `extensions/svg/`).
| Size | Typical use |
|---|---|
| 16 | Browser toolbar / favicon, editor tab |
| 32 | Retina toolbar, Windows taskbar, editor sidebar |
| 48 | Browser extension management page, Chrome store listing |
| 64 / 128 | Extension store icon (Chrome Web Store 128), VS Code marketplace listing |
| 256 / 512 | Marketplace banners, docs, repository social assets |

`extensions/favicon/` — favicon-16/32/48.png, `favicon.ico` (16/32/48, PNG-encoded) and `favicon.svg`.
`app-icons/` — 512 and 1024 px full-bleed square on near-black (platforms/GitHub apply their own rounding/circle mask; the mark sits in the safe zone). Also `openclone-app.svg`.

**Optical sizing:** at 32 px and below the PNGs use a slightly heavier ring, larger cube and a larger mark (`openclone-extension-dark-small.svg` is the master for this). Geometry is otherwise identical to the main symbol.

## Clear space and minimum size
- **Clear space:** keep at least **½ the symbol cube width ≈ ⅙ of the symbol height** free on every side; for stacked/horizontal lockups use the cap-height of the "O" as the minimum margin.
- **Minimum size:** symbol 16 px (use the small-size icon variant ≤32 px); primary logo 96 px wide; stacked logo 96 px wide; tagline lockups 200 px wide (below this, use the primary logo).
- Do not recolour, stretch, rotate, outline, add effects, or place the light logo on dark backgrounds.

## Source and export formats
- **SVG** (editable, `viewBox`, no raster, text outlined): `logo/`, `extensions/svg/`, `app-icons/`, `source/`
- **PNG**: transparent for all logos and symbols; extension icons and app icons are opaque background-specific.
- **ICO**: `extensions/favicon/favicon.ico`
- `source/build.py` regenerates everything (needs `cairosvg`, `fonttools`, `uharfbuzz`, `pillow`, Space Grotesk and Inter fonts). `source/design-tokens.json` holds the numbers.
- `previews/` are presentation boards composed from the individual assets, not deliverables.

## Known limitations
- Space Grotesk was obtained from the Google Fonts repository (SIL OFL 1.1); text is outlined, so no font ships in this package.
- Not generated: PDF, EPS, `.ai`/`.fig` files (SVG is the editable source). ICO contains 16/32/48 only.
- No trademark/similarity search was run; the mark is original but should be checked before legal registration.
