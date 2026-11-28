# Anti-AI-Slop Standards
## The OpenClone Manifesto on Human-Crafted UI Engineering

AI-generated interfaces often look unmistakably generic. When asked to create a webpage, modern LLMs default to an identical cocktail of visual clichés. OpenClone establishes an uncompromising line: **We reject AI Slop in favor of intentional, human-crafted design systems.**

---

## 1. The Anatomy of AI Slop vs Human Craft

| Design Dimension | Generic AI Slop (What We Reject) | Human-Crafted Excellence (What We Enforce) |
|---|---|---|
| **Color Palettes** | Default indigo/purple gradients (`#6366f1` to `#a855f7`) on dark backgrounds everywhere. | Palettes tailored to the specific industry and trade (coffee shop gets warm umber and raw cream; dev tool gets obsidian with terminal amber). |
| **Surfaces & Cards** | Generic, illegible 2024 translucent cards with unmanaged text contrast and rounded-2xl cartoon borders. | **Precision 2026 Glassmorphism & Dark Luxury:** Obsidian neutral ground (`#09090b`), multi-stop backdrop blur (`blur-20px saturate-180%`), 1px top-edge specular highlights, and 7:1 WCAG contrast scrims. |
| **Backgrounds** | Random, floating amorphous gradient blobs (`blur(100px)`) drifting aimlessly behind content. | Solid, intentional background tones or subtle architectural grids and quiet SVG ground patterns. |
| **Typography** | Generic sans-serif with massive, low-contrast headings and two-word buzzword titles ("Unleash Potential"). | Scaled modular typography (Major Third) with plain, concrete, truthful copywriting ("Track API latency in real time"). |
| **Icons & Imagery** | Decorative 3D cartoon icons, floating glowing orbs, and fake generated product mockups. | Genuine vector brand marks, authentic interface fragments (real code diffs, real pipeline boards), and credited archive photographs. |
| **Statistics** | Invented circular progress counters or fake metric strips ("99.9% Satisfaction", "10M+ Users"). | Real, verifiable system metrics or clean explanatory content tiles when metrics do not yet exist. |
| **Micro-Interactions** | Over-animated floating cards, slow 500ms bouncy hover transitions, and continuous spinning elements. | Quiet, instant micro-interactions: 1px button step on press, 150ms ease-out hover lift, immediate visible focus rings. |
| **Whitespace** | Random empty pockets or suffocated dense clumps caused by unmanaged grid items. | Systematic 8-point spatial rhythm (8px, 16px, 24px, 32px, 48px, 64px) providing rhythm and breath. |

---

## 2. The Five Governance Classifications

Every visual pattern introduced into an OpenClone project must be evaluated against this classification ladder:

1. **`REQUIRED`**: Mandatory by explicit user prompt, project design token definition, or accessibility standard (e.g., high-contrast focus rings, semantic form labels, 44px tap targets).
2. **`JUSTIFIED`**: Defended by concrete product domain evidence (e.g., a data visualization dashboard requiring multi-series color differentiation; an audio tool requiring tactile sliders).
3. **`OPTIONAL`**: Tasteful enhancement that adds clarity without introducing cognitive load or performance overhead (e.g., subtle 1px border dividers).
4. **`UNNECESSARY`**: Decorative visual noise that distracts from the core user task (e.g., unprompted floating blurred background blobs, repetitive pill badges).
5. **`PROHIBITED`**: Dangerous or low-quality patterns that violate accessibility, performance, or credibility (e.g., illegible text on un-scrimmed glass, fake testimonial carousels, uncancelable auto-animations).

---

## 3. Removal-First Protocol (The Janitor Rule)

When auditing or upgrading an existing interface (brownfield engineering), agents MUST follow a **Removal-First** workflow:

1. **`REMOVE` First**: Identify and eliminate visual noise, redundant container cards, dead widgets, and duplicate buttons before writing new code.
2. **`PRESERVE` What Works**: Do not touch working layout systems, established brand typography, or verified accessibility hooks simply to impose personal agent preference.
3. **`MODIFY` with Restraint**: Tighten padding, elevate typography contrast, and refine border colors to match the design token scale.
4. **`ADD` Last**: Introduce new components only when the task's acceptance criteria strictly require them.

---

## 4. Accessibility as a Non-Negotiable Baseline

Human-crafted software is inclusive software. OpenClone treats WCAG 2.2 Level AA compliance not as an afterthought, but as an inviolable gate:
- **Contrast**: Minimum 4.5:1 for normal text; 3:1 for large text and interface components.
- **Keyboard Navigation**: Complete tab-walk coverage with an unambiguous, visible 2px focus ring that is never hidden behind sticky headers.
- **Touch Targets**: Minimum 44x44 CSS pixels for all interactive targets on touchscreen and mobile viewports.
- **Motion Restraint**: Full conformance with `prefers-reduced-motion: reduce`. When enabled, all non-essential transform and opacity transitions must be bypassed.
