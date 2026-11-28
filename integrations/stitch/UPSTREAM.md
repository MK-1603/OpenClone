# Upstream Provenance: Google Stitch Skills

## 1. Upstream Metadata

- **Upstream Repository:** `https://github.com/google-labs-code/stitch-skills`
- **Official Branch:** `main`
- **Imported Commit SHA:** `75f4696f162000fb69fca6a31489b5b21d47a506`
- **Upstream Commit Date:** `2026-11-24 13:51:03 -0800`
- **Upstream Author:** J XIA
- **Import Date:** `2026-11-25 22:40:00 +05:30`
- **OpenClone Integration Version:** `1.0.0`
- **License:** Apache License 2.0 (see [LICENSE](LICENSE))

---

## 2. Imported Plugin & Skill Inventory

The upstream repository organizes skills into three plugin suites under the [Agent Skills](https://agentskills.io) open standard:

### A. `stitch-design` (6 Skills)
| Skill Directory | Upstream Identifier | Internal OpenClone ID | Description |
|---|---|---|---|
| `design/skills/code-to-design` | `stitch::code-to-design` | `stitch-code-to-design` | Convert frontend code (React, Vue, Vite, etc.) to Stitch design via extraction, design system, and upload. |
| `design/skills/extract-design-md` | `stitch::extract-design-md` | `stitch-extract-design-md` | Extract comprehensive DESIGN.md token specification from frontend source code. |
| `design/skills/extract-static-html` | `stitch::extract-static-html` | `stitch-extract-static-html` | Extract self-contained static HTML with inlined assets from running servers. |
| `design/skills/generate-design` | `stitch::generate-design` | `stitch-generate-design` | Generate screens from text/images, edit screens, and create design variants. |
| `design/skills/manage-design-system` | `stitch::manage-design-system` | `stitch-manage-design-system` | Upload DESIGN.md tokens and apply cohesive themes to Stitch screens. |
| `design/skills/upload-to-stitch` | `stitch::upload-to-stitch` | `stitch-upload-to-stitch` | Upload local HTML, markdown, and images directly to Stitch bypassing base64 limits. |

### B. `stitch-build` (5 Skills)
| Skill Directory | Upstream Identifier | Internal OpenClone ID | Description |
|---|---|---|---|
| `build/skills/react-components` | `stitch::react-components` | `stitch-react-components` | Convert Stitch screens to modular React components with design token fidelity. |
| `build/skills/react-native` | `stitch::react-native` | `stitch-react-native` | Convert Stitch HTML designs to production-ready React Native components. |
| `build/skills/react-vite-dashboard` | `react-vite-dashboard` | `stitch-react-vite-dashboard` | Convert Stitch screens to React + Vite dashboards with TanStack Query and DESIGN.md. |
| `build/skills/remotion` | `remotion` | `stitch-remotion` | Generate video walkthroughs from Stitch screens using Remotion. |
| `build/skills/shadcn-ui` | `shadcn-ui` | `stitch-shadcn-ui` | Expert guidance for shadcn/ui components and design system integration. |

### C. `stitch-utilities` (5 Skills)
| Skill Directory | Upstream Identifier | Internal OpenClone ID | Description |
|---|---|---|---|
| `utilities/skills/design-md` | `design-md` | `stitch-design-md` | Synthesize semantic DESIGN.md files from Stitch projects or design guidelines. |
| `utilities/skills/enhance-prompt` | `enhance-prompt` | `stitch-enhance-prompt` | Refine vague requirements into high-fidelity UI/UX prompts with professional terminology. |
| `utilities/skills/site-md` | `site-md` | `stitch-site-md` | Synthesize SITE.md architectural constitution for multi-page web applications. |
| `utilities/skills/stitch-loop` | `stitch-loop` | `stitch-loop` | Autonomous multi-page site generation loop with validation and baton passing. |
| `utilities/skills/taste-design` | `taste-design` | `stitch-taste-design` | Generate DESIGN.md specs enforcing anti-generic, high-craft visual standards. |

---

## 3. Preserved Architecture & Integrity

1. **Exact Instruction Preservation:** All upstream `SKILL.md` files are preserved intact. Instructions, guidelines, scripts, resources, and examples are preserved without destructive truncation.
2. **Dual-Identifier Compatibility:** Skills are accessible by both their upstream identifier (e.g. `stitch::generate-design`) and OpenClone's standard kebab-case identifier (`stitch-generate-design`).
3. **Execution Scripts Preserved:** Supporting scripts (`fetch-stitch.sh`, `upload_to_stitch.py`, `validate.js`) are vendor-maintained in their skill directories.
4. **License Compliance:** Apache 2.0 license file is included at the integration root, and upstream copyrights (Google LLC) are preserved.

---

## 4. Upstream Update Procedure

To update the Stitch Skills integration from upstream:

1. Fetch latest changes from `https://github.com/google-labs-code/stitch-skills` into a vendor staging branch or directory.
2. Run `python -m src.openclone.integrations.stitch.adapter.updater --check` to compare commit SHAs and inspect modified files.
3. Synchronize `design/`, `build/`, and `utilities/` skill directories.
4. Run integration and discovery tests:
   ```bash
   pytest tests/test_stitch_skills_integration.py -v
   ```
5. Update `manifest.json` and `UPSTREAM.md` with new commit SHA, date, and diff notes.
