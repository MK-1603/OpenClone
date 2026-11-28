#!/usr/bin/env python3
"""OpenClone brand asset generator.
Generates every SVG / PNG / ICO in OpenClone-Brand-Assets from one parametric master symbol.
Requires: cairosvg, fonttools, uharfbuzz, pillow. Fonts: Space Grotesk (variable TTF), Inter (OTF).
"""
import math, os, io, struct, json, shutil, sys
import cairosvg, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "OpenClone-Brand-Assets")
FONT_SG = os.environ.get("SG_FONT", os.path.join(HERE, "fonts", "SG.ttf"))
FONT_INTER = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

GOLD, BLACK, WHITE, SILVER = "#FACC15", "#0B0B0B", "#FFFFFF", "#A1A1AA"

def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

# ------------------------------------------------------------------ symbol
CX = CY = 128
R = 112  # hexagon circumradius (vertex)

THEMES = {
    # body = open "O/C" ring body, term = the two mirrored terminals,
    # cube = (top, left, right)
    "dark":  dict(body=WHITE, term=GOLD,  cube=(WHITE, SILVER, GOLD)),
    "light": dict(body=BLACK, term=GOLD,  cube=(BLACK, SILVER, GOLD)),
    "gold":  dict(body=BLACK, term=BLACK, cube=(WHITE, BLACK, BLACK)),
}

def hexpt(r, k):
    a = math.radians(-90 + 60 * k)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

def symbol_polys(theme, small=False):
    """Return [(id, points, color)] for the master symbol in a 256x256 box."""
    T = 46 if small else 40          # ring thickness measured at vertices
    gap = 6 if small else 9          # gap between body and terminals (along edge)
    c = 48 if small else 44          # cube radius
    th = THEMES[theme]
    ri = R - T
    O = [hexpt(R, k) for k in range(6)]
    I = [hexpt(ri, k) for k in range(6)]
    polys = []
    # open body: edges 3->4, 4->5, 5->0 (bottom -> left -> top), mitred joins
    body = [O[3], O[4], O[5], O[0], I[0], I[5], I[4], I[3]]
    polys.append(("body", body, th["body"]))
    def terminal(k0, k1):
        ux, uy = O[k1][0] - O[k0][0], O[k1][1] - O[k0][1]
        L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
        o0 = (O[k0][0] + ux * gap, O[k0][1] + uy * gap)
        i0 = (I[k0][0] + ux * gap, I[k0][1] + uy * gap)
        return [o0, O[k1], I[k1], i0]
    polys.append(("terminal-top", terminal(0, 1), th["term"]))      # top -> upper right
    polys.append(("terminal-bottom", terminal(3, 2), th["term"]))   # bottom -> lower right (mirror)
    # modular core: isometric cube
    T_, UR, LR, B, LL, UL = [hexpt(c, k) for k in range(6)]
    ctr = (CX, CY)
    ct, cl, cr = th["cube"]
    polys.append(("cube-top", [T_, UR, ctr, UL], ct))
    polys.append(("cube-left", [UL, ctr, B, LL], cl))
    polys.append(("cube-right", [UR, LR, B, ctr], cr))
    return polys

def poly_d(pts):
    return "M" + " L".join(f"{n(x)} {n(y)}" for x, y in pts) + " Z"

def centroid(polys):
    A = Cx = Cy = 0.0
    for _, pts, _c in polys:
        a = cx_ = cy_ = 0.0
        for i in range(len(pts)):
            x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
            cr = x0 * y1 - x1 * y0
            a += cr; cx_ += (x0 + x1) * cr; cy_ += (y0 + y1) * cr
        a /= 2
        A += a; Cx += cx_ / 6; Cy += cy_ / 6
    return Cx / A, Cy / A

def symbol_group(theme, small=False, transform=""):
    items = "".join(f'<path id="oc-{i}" d="{poly_d(p)}" fill="{c}"/>' for i, p, c in symbol_polys(theme, small))
    t = f' transform="{transform}"' if transform else ""
    return f'<g id="openclone-symbol"{t}>{items}</g>'

# symbol tight bbox in master coordinates
BX0, BX1 = CX - R * math.cos(math.radians(30)), CX + R * math.cos(math.radians(30))
BY0, BY1 = CY - R, CY + R
SYM_W, SYM_H = BX1 - BX0, BY1 - BY0   # ~194 x 224

# ------------------------------------------------------------------ text outlines
def _static(path, wght, tmp):
    tt = TTFont(path)
    if "fvar" in tt:
        tt = instantiateVariableFont(tt, {"wght": wght})
        tt.save(tmp)
        return tmp
    return path

_cache = {}
def load(path, wght=None):
    key = (path, wght)
    if key not in _cache:
        p = _static(path, wght, os.path.join(HERE, f"_tmp_{os.path.basename(path)}_{wght}.ttf")) if wght else path
        tt = TTFont(p)
        blob = hb.Blob.from_file_path(p)
        _cache[key] = (tt, hb.Font(hb.Face(blob)), tt.getGlyphSet(), tt.getGlyphOrder(), tt["head"].unitsPerEm)
    return _cache[key]

def layout(fontkey, text, tracking_em=0.0):
    """Return (glyphs[(idx,name,x)], width_in_em)"""
    tt, font, gs, order, upem = load(*fontkey)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    x = 0.0; glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyphs.append((info.cluster, order[info.codepoint], x + pos.x_offset))
        x += pos.x_advance + tracking_em * upem
    return glyphs, (x - tracking_em * upem) / upem

def text_paths(fontkey, text, size, ox, oy, tracking_em=0.0):
    """Outlined text -> list of (char_index, path_d)."""
    tt, font, gs, order, upem = load(*fontkey)
    glyphs, _ = layout(fontkey, text, tracking_em)
    s = size / upem
    out = []
    for idx, name, gx in glyphs:
        pen = SVGPathPen(gs, ntos=n)
        gs[name].draw(TransformPen(pen, (s, 0, 0, -s, ox + gx * s, oy)))
        d = pen.getCommands()
        if d:
            out.append((idx, d))
    return out

def text_width(fontkey, text, size, tracking_em=0.0):
    return layout(fontkey, text, tracking_em)[1] * size

SG_BOLD = (FONT_SG, 700)
INTER_M = (FONT_INTER, None)
WORD, TAGLINE = "OpenClone", "Engineering Intelligence, Openly."
assert WORD == "OpenClone" and TAGLINE == "Engineering Intelligence, Openly."

# ------------------------------------------------------------------ lockups
def word_group(theme, size, ox, oy):
    col = WHITE if theme == "dark" else BLACK
    parts = text_paths(SG_BOLD, WORD, size, ox, oy, tracking_em=-0.01)
    main = " ".join(d for i, d in parts if i != 4)   # everything except C
    c = " ".join(d for i, d in parts if i == 4)
    return f'<g id="wordmark" aria-label="OpenClone"><path d="{main}" fill="{col}"/><path d="{c}" fill="{GOLD}"/></g>'

def tag_group(theme, width, ox, oy):
    col = SILVER if theme == "dark" else BLACK
    op = "" if theme == "dark" else ' fill-opacity="0.72"'
    tr = 0.035
    w1 = text_width(INTER_M, TAGLINE, 1.0, tr)
    size = width / w1
    d = " ".join(dd for _, dd in text_paths(INTER_M, TAGLINE, size, ox, oy, tr))
    return f'<g id="tagline" aria-label="Engineering Intelligence, Openly."><path d="{d}" fill="{col}"{op}/></g>', size

def svg_wrap(w, h, body, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(w)} {n(h)}" width="{n(w)}" height="{n(h)}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')

PAD = 16
WS = 143            # wordmark font size (cap height ~100 units)
CAPH = 0.70 * WS
GAP_SYM = 52

def logo_primary(theme):
    wmw = text_width(SG_BOLD, WORD, WS, -0.01)
    H = SYM_H
    sym = symbol_group(theme, transform=f"translate({n(PAD - BX0)} {n(PAD - BY0)})")
    base = PAD + H / 2 + CAPH / 2
    wm = word_group(theme, WS, PAD + SYM_W + GAP_SYM, base)
    W = PAD * 2 + SYM_W + GAP_SYM + wmw
    return svg_wrap(W, H + 2 * PAD, sym + wm, "OpenClone")

def logo_horizontal(theme):
    """symbol left, wordmark + tagline right"""
    wmw = text_width(SG_BOLD, WORD, WS, -0.01)
    H = SYM_H
    sym = symbol_group(theme, transform=f"translate({n(PAD - BX0)} {n(PAD - BY0)})")
    tagw, _ = wmw, 0
    tag_cap = 0.727
    # tagline sized to match wordmark width; compute its size first
    _, tsize = tag_group(theme, wmw, 0, 0)
    block = CAPH + 0.26*WS + 22 + tsize * tag_cap
    top = PAD + H / 2 - block / 2
    wm_base = top + CAPH
    tag_base = wm_base + 0.26*WS + 22 + tsize * tag_cap
    x0 = PAD + SYM_W + GAP_SYM
    wm = word_group(theme, WS, x0, wm_base)
    tg, _ = tag_group(theme, wmw, x0, tag_base)
    W = PAD * 2 + SYM_W + GAP_SYM + wmw
    return svg_wrap(W, H + 2 * PAD, sym + wm + tg, "OpenClone - Engineering Intelligence, Openly.")

def logo_stacked(theme):
    wmw = text_width(SG_BOLD, WORD, WS, -0.01)
    scale = 1.25
    sw, sh = SYM_W * scale, SYM_H * scale
    W = PAD * 2 + wmw
    sx = (W - sw) / 2
    sym = symbol_group(theme, transform=f"translate({n(sx - BX0 * scale)} {n(PAD - BY0 * scale)}) scale({scale})")
    wm_base = PAD + sh + 44 + CAPH
    wm = word_group(theme, WS, PAD, wm_base)
    _, tsize = tag_group(theme, wmw, 0, 0)
    tag_base = wm_base + 0.24 * WS + 20 + tsize * 0.727
    tg, _ = tag_group(theme, wmw, PAD, tag_base)
    H = tag_base + tsize * 0.25 + PAD
    return svg_wrap(W, H, sym + wm + tg, "OpenClone - Engineering Intelligence, Openly.")

def symbol_only(theme):
    pad = 24
    S = max(SYM_W, SYM_H) + 2 * pad
    tx = (S - SYM_W) / 2 - BX0
    ty = (S - SYM_H) / 2 - BY0
    return svg_wrap(S, S, symbol_group(theme, transform=f"translate({n(tx)} {n(ty)})"), "OpenClone symbol")

def extension_icon(theme, small=False, mark_frac=0.64, radius=0.22):
    S = 512
    polys = symbol_polys(theme, small)
    ccx, ccy = centroid(polys)
    # optical centring: move halfway from bbox-centre toward the visual centroid offset
    dx = (CX - ccx) * 0.5
    k = S * mark_frac / SYM_H
    tx = S / 2 - CX * k + dx * k
    ty = S / 2 - CY * k
    bg = {"dark": BLACK, "light": WHITE, "gold": GOLD}[theme]
    border = ""
    if theme == "light":
        border = f'<rect x="3" y="3" width="506" height="506" rx="{n(S*radius-3)}" fill="none" stroke="{BLACK}" stroke-opacity="0.14" stroke-width="6"/>'
    body = (f'<rect id="background" width="512" height="512" rx="{n(S*radius)}" fill="{bg}"/>{border}'
            + symbol_group(theme, small, transform=f"translate({n(tx)} {n(ty)}) scale({n(k)})"))
    return svg_wrap(S, S, body, f"OpenClone extension icon ({theme})")

def app_icon(small=False):
    # full-bleed square (platform applies its own mask), mark inside safe zone
    S = 512
    polys = symbol_polys("dark", small)
    ccx, _ = centroid(polys)
    dx = (CX - ccx) * 0.5
    k = S * 0.58 / SYM_H
    tx = S / 2 - CX * k + dx * k; ty = S / 2 - CY * k
    body = f'<rect id="background" width="512" height="512" fill="{BLACK}"/>' + symbol_group("dark", small, transform=f"translate({n(tx)} {n(ty)}) scale({n(k)})")
    return svg_wrap(S, S, body, "OpenClone app icon")

# ------------------------------------------------------------------ IO helpers
def w(path, data, mode="w"):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(data)
    return p

def png_bytes(svg, width=None, height=None):
    return cairosvg.svg2png(bytestring=svg.encode(), output_width=width, output_height=height)

def ico_bytes(pngs):
    """pngs: list of (size, png_bytes) -> ICO with PNG-encoded entries"""
    head = struct.pack("<HHH", 0, 1, len(pngs))
    entries = b""; data = b""; off = 6 + 16 * len(pngs)
    for s, b in pngs:
        entries += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(b), off)
        data += b; off += len(b)
    return head + entries + data

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    svgs = {}

    # --- logos
    for th in ("light", "dark"):
        s = logo_primary(th); svgs[f"logo/{th}/openclone-logo-{th}.svg"] = s
        w(f"logo/{th}/openclone-logo-{th}.svg", s)
        w(f"logo/{th}/openclone-logo-{th}.png", png_bytes(s, width=2400), "wb")
        s = symbol_only(th); w(f"logo/symbol/openclone-symbol-{th}.svg", s)
        w(f"logo/symbol/openclone-symbol-{th}.png", png_bytes(s, 1024, 1024), "wb")
        s = logo_horizontal(th); w(f"logo/lockups/openclone-horizontal-{th}.svg", s)
        w(f"logo/lockups/openclone-horizontal-{th}.png", png_bytes(s, width=2400), "wb")
        s = logo_stacked(th); w(f"logo/lockups/openclone-stacked-{th}.svg", s)
        w(f"logo/lockups/openclone-stacked-{th}.png", png_bytes(s, width=1600), "wb")

    # --- extension icons
    sizes = [16, 32, 48, 64, 128, 256, 512]
    for th in ("dark", "light", "gold"):
        master = extension_icon(th)
        w(f"extensions/svg/openclone-extension-{th}.svg", master)
        for sz in sizes:
            svg = extension_icon(th, small=(sz <= 32), mark_frac=0.70 if sz <= 32 else 0.64)
            w(f"extensions/png/{sz}/openclone-extension-{th}-{sz}.png", png_bytes(svg, sz, sz), "wb")
    # small-size optical master (documented)
    w("extensions/svg/openclone-extension-dark-small.svg", extension_icon("dark", small=True, mark_frac=0.70))

    # --- favicon
    fav = {}
    for sz in (16, 32, 48):
        svg = extension_icon("dark", small=True, mark_frac=0.72, radius=0.2)
        b = png_bytes(svg, sz, sz); fav[sz] = b
        w(f"extensions/favicon/favicon-{sz}.png", b, "wb")
    w("extensions/favicon/favicon.ico", ico_bytes(sorted(fav.items())), "wb")
    w("extensions/favicon/favicon.svg", extension_icon("dark", small=True, mark_frac=0.72, radius=0.2))

    # --- app icons
    a = app_icon()
    w("app-icons/openclone-app-512.png", png_bytes(a, 512, 512), "wb")
    w("app-icons/openclone-app-1024.png", png_bytes(a, 1024, 1024), "wb")
    w("app-icons/openclone-app.svg", a)

    # --- source
    w("source/openclone-symbol-master-dark.svg", symbol_only("dark"))
    w("source/openclone-symbol-master-light.svg", symbol_only("light"))
    w("source/design-tokens.json", json.dumps({
        "colors": {"gold": GOLD, "nearBlack": BLACK, "white": WHITE, "silver": SILVER},
        "fonts": {"wordmark": "Space Grotesk Bold 700 (outlined)", "tagline": "Inter Medium (outlined)", "ui": "Inter"},
        "symbol": {"grid": "256x256", "hexCircumradius": R, "ringThickness": 40, "ringThicknessSmall": 46,
                   "cubeRadius": 44, "cubeRadiusSmall": 48, "gap": 9, "gapSmall": 6},
        "clearSpace": "1x = height of the symbol cube (72 units on the 256 grid) / ~ 1/3 symbol height",
        "minSize": {"symbolPx": 16, "primaryLogoWidthPx": 96, "stackedLogoWidthPx": 96}
    }, indent=2))
    shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "source", "build.py"))
    print("built")

if __name__ == "__main__":
    main()
