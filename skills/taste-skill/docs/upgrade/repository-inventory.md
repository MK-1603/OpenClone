# Taste Skill Repository Inventory & Baseline Audit
**Date:** 2026-11-22  
**Target:** `Leonxlnx/taste-skill` v2.5.1  
**Auditor:** Principal Design Engineer & Developer Tooling Architect

---

## 1. Directory Structure Inventory

The repository is structured as a multi-agent skill package supporting Claude Code, Codex, Cursor, and Antigravity:

```text
taste-skill/
├── .agents/plugins/marketplace.json        # Agent marketplace registration
├── .claude-plugin/marketplace.json         # Claude Code plugin manifest
├── .codex-plugin/plugin.json               # Codex plugin manifest
├── .github/workflows/check-skills.yml      # CI workflow (Node 22: frontmatter, encoding, syntax)
├── assets/                                 # Top-level branding wordmarks and images
├── examples/v2/                            # Screenshot examples from v2 runs
├── install.sh                              # Standalone shell installer
├── README.md                               # Public GitHub documentation
├── CHANGELOG.md                            # Version history (v2.0.0 through v2.5.1)
├── tests/                                  # Repository verification tests
│   ├── frontmatter.mjs                     # YAML frontmatter validator
│   ├── kit-clean.mjs                       # Real browser consistency & layout test harness
│   └── text-encoding.mjs                   # Clean UTF-8 verification
└── skills/taste-skill/                     # Core skill package
    ├── SKILL.md                            # Main skill instructions and stop hooks
    ├── assets/                             # Visual system and web components
    │   ├── backgrounds/                    # CSS/JS backgrounds & canvas shaders
    │   ├── components/                     # Web components (fx-avatar, fx-globe, etc.)
    │   ├── diagrams/                       # Interactive architecture diagram fragments
    │   ├── effects/                        # WebGL shaders and canvas effects
    │   ├── icons/                          # Brand and UI SVG icons
    │   ├── layout/                         # Layout system v4, check.mjs layout checker
    │   ├── moments/                        # Handcrafted scroll & hover moments
    │   ├── motion/                         # Motion design system & data-enter hooks
    │   ├── objects/                        # Rendered 3D objects and dithered sprites
    │   ├── photos/                         # Licensed stand-in photography
    │   ├── scenes/                         # Full-screen 3D scenes (tech/software only)
    │   └── ui/                             # Real product UI fragments and mockups
    ├── library/
    │   ├── palettes.json                   # Curated trade color palettes
    │   └── type.json                       # Curated font pairings from Google Fonts
    ├── references/                         # 21 Markdown design reference manuals
    └── scripts/                            # 12 Operational Node.js ES module scripts
```

---

## 2. Inventory of Existing Scripts

| Script Path | Purpose | Language / Runtime | Dependencies |
|---|---|---|---|
| `scripts/start.mjs` | Deals palettes, Google Fonts, and generates `:root` CSS blocks | Node.js 22 (ESM) | Built-in `fs`, `path`, `url` |
| `scripts/gate.mjs` | Finish gate: blocks build completion if fixable faults or copy tells remain | Node.js 22 (ESM) | Built-in `fs`, `path`, `child_process` |
| `scripts/consistency.mjs` | Headless Chrome browser auditor (11,485 lines) checking layout, text, contrast, buttons, motion, and visuals | Node.js 22 (ESM) | Chrome DevTools Protocol / headless browser |
| `scripts/copy-lint.mjs` | Anti-AI-slop copy auditor detecting chatbot residue, virtue signaling, and repetitive phrasing | Node.js 22 (ESM) | Built-in `fs`, `path` |
| `scripts/perf.mjs` | Web performance and asset load time auditor | Node.js 22 (ESM) | Built-in `fs`, `path` |
| `scripts/shoot.mjs` | Headless screenshot capture utility at 1440, 1024, 768, and 390px widths | Node.js 22 (ESM) | Headless Chrome |
| `scripts/moments.mjs` | Deals and mounts bespoke moments onto sections | Node.js 22 (ESM) | Built-in `fs`, `path` |
| `scripts/photos.mjs` | Curates and places licensed stand-in photography | Node.js 22 (ESM) | Built-in `fs`, `path` |
| `scripts/icons.mjs` | Real product icon resolver and asset manager | Node.js 22 (ESM) | Built-in `fs`, `path` |
| `scripts/effects.mjs` | WebGL shader and canvas effect selector | Node.js 22 (ESM) | Built-in `fs`, `path` |

---

## 3. Inventory of Existing References

| Reference File | Domain Covered |
|---|---|
| `references/system.md` | Core design system rules and CSS variables |
| `references/layout-v4.md` | Screen-by-screen layout rules, edge alignments, and grids |
| `references/gate.md` | Finish gate lifecycle, rounds, waivers, and block conditions |
| `references/copy.md`, `copy-voice.md`, `copy-tells.md`, `copy-moves.md`, `copy-registers.md` | Comprehensive anti-slop copy rules |
| `references/cards.md`, `sections.md`, `sections-library.md` | Section and card composition guidelines |
| `references/motion.md`, `moments.md`, `scenes.md`, `photos.md`, `icons.md`, `diagrams.md`, `effects-*.md` | Visual asset integration specifications |
| `references/perf.md` | Performance constraints and WebGL context limits |

---

## 4. Current Workflow Analysis

1. **Intake:** User prompts the agent with a brief (e.g. "Build a landing page for my devtool").
2. **Setup:** Agent runs `node scripts/start.mjs deal --page software --trade devtool`.
3. **Synthesis:** Agent writes HTML/CSS utilizing `skills/taste-skill/assets/`.
4. **Verification:** Stop hook triggers `node scripts/gate.mjs --hook claude|codex|antigravity`.
5. **Gating:** Headless Chrome runs `consistency.mjs` and `copy-lint.mjs`. If errors exist, the gate exits 1, forcing the agent to fix issues.

---

## 5. Current Gaps Identified

* **No Pre-Build Gate:** The current gate is solely a *finish gate*. An agent can generate 1,000 lines of generic UI code before `gate.mjs` runs.
* **No Instruction Discovery:** The current system does not inspect `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or project-level rules.
* **No Existing Application Audit:** If dropped into a Next.js/Tailwind repo, the skill previously attempted to generate standalone HTML/CSS instead of inspecting the host app.
* **Visual Slop Detection is Purely Reactive:** Slop is caught only after rendering in Chrome, not prevented at the architectural/design planning stage.
* **No Removal-First Rule:** No mechanism exists to analyze existing visual clutter and prune before adding.
* **No Task-Size Differentiation:** A one-line button tweak triggers the same mental model as an entire multi-page site.
