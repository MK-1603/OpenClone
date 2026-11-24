---
id: design-system-engineering
name: Design System Engineering Skill
version: 1.0.0
category: design
description: Design tokens (color, type, space, elevation), theme architecture, component primitives, variants, states, and design governance.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/design-system-engineering/SKILL.md
triggers:
  - design system
  - design tokens
  - tokens
  - color palette
  - theme
  - dark mode
  - light mode
  - component library
  - typography scale
  - spacing tokens
  - ui components
  - variants
  - primitives
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 12
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Design token contract defined (color, spacing, radius, typography)
  - Theme switching & semantic color mapping specified
  - Component primitive variant matrix documented
finish_gates:
  - Token consistency audit pass (zero hardcoded ad-hoc values)
  - Component state coverage verified (hover, active, focus, disabled)
  - Theme switching verified without layout shift or contrast break
verification:
  - Automated token schema validator
  - Component variant & accessibility test pass
---

# Design System Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `design` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `design-systems-engineer`, `ui-designer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Establish maintainable, scalable, accessible, and mathematically harmonious design systems. Design System Engineering bridges raw design intent with deterministic production code through semantic design tokens, systematic component primitives, extensible theme architectures, and rigorous design governance.

### Boundaries
- **In Scope:** Design tokens (colors, type, spacing, elevation, radius, borders, motion), theme architecture (light, dark, high contrast, brand), component primitives & composites, variant architectures, interactive component states, token naming conventions, and visual regression testing.
- **Out of Scope:** High-level user journeys (governed by `ux-pro`) and anti-slop art direction (governed by `taste-skill`).

---

## 2. REQUIRED EXPERTISE DOMAINS

### A. Design Tokens Architecture
1. **Tiered Token Structure:**
   - **Global / Raw Tokens:** Primitive values without semantic context (e.g., `palette-zinc-900: #0E0E0E`, `scale-space-4: 16px`).
   - **Semantic / Alias Tokens:** Intent-driven tokens binding meaning to primitives (e.g., `surface-base: var(--palette-zinc-900)`, `space-inset-md: var(--scale-space-4)`).
   - **Component Tokens:** Scoped variables for specific component parts (e.g., `btn-primary-bg: var(--color-primary-base)`).
2. **Token Categories:**
   - **Color:** Backgrounds, surfaces, borders, text, brand accents, and semantic statuses (info, success, warning, error).
   - **Typography:** Font families, weights, sizes, line heights, letter spacing, and tabular numeral settings.
   - **Spacing & Sizing:** Consistent 4px or 8px grid increments (e.g., 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px).
   - **Radius & Borders:** Subtle curves (`sm: 4px`, `md: 6px`, `lg: 8px`, `full: 9999px`) and hairline borders (`1px solid var(--border-subtle)`).
   - **Shadows & Elevation:** Purposeful layered shadows matching light source height without excessive blur.
   - **Z-Index Layering:** Explicit, non-colliding layers (e.g., `base: 0`, `elevated: 10`, `dropdown: 20`, `sticky: 30`, `modal-backdrop: 40`, `modal: 50`, `toast: 60`, `tooltip: 70`).

### B. Theme Architecture
1. **Light & Dark Theme Parity:** Both modes must maintain equal visual contrast, legible hierarchy, and consistent interactive feedback.
2. **CSS Variables & Runtime Switching:** Implement themes using root-level CSS custom properties or `[data-theme]` attributes to enable zero-flash switching (`next-themes` or native classes).
3. **Contrast-Preserving Inversion:** Dark themes must use deep charcoal (`#0A0A0A` / `#0E0E0E`) with soft contrast surfaces (`#161616` / `#1F1F1F`), never harsh pure black with glaring pure white text.

### C. Typography System
1. **Proportional Type Scale:** Major Third (`1.250`) or Perfect Fourth (`1.333`) scale.
2. **Semantic Font Roles:**
   - **Display / Heading:** Bold, confident, tightened letter-spacing (`-0.02em` to `-0.03em`).
   - **Body / Content:** Highly legible at `14px-16px`, relaxed line height (`1.5-1.6`), normal tracking.
   - **Monospace / Code:** Technical data, tokens, and code snippets with tabular numerals.
3. **Fluid Typography:** Use CSS `clamp()` for responsive headings that scale smoothly without abrupt jumps.

### D. Component System & Primitives
1. **Primitive vs. Composite Components:**
   - **Primitives:** Button, Input, Checkbox, Badge, Avatar, Card, Tooltip, Icon.
   - **Composites:** Data Table, Modal Dialog, Navigation Sidebar, Metric Card, Filter Bar.
2. **Variant Architecture:** Enforce strict TypeScript prop contracts for variants (e.g., `variant: "primary" | "secondary" | "outline" | "ghost" | "danger"`, `size: "sm" | "md" | "lg"`).
3. **Complete State Coverage:** Every interactive component must define styles for:
   - `default`
   - `hover`
   - `active / pressed`
   - `focus-visible` (visible ring, minimum 2px offset)
   - `disabled` (opacity reduction, `pointer-events-none`)
   - `loading` (spinner or skeleton overlay)

### E. Design Governance
1. **Zero Ad-Hoc Styling:** Prohibit arbitrary pixel values (`p-[17px]`, `text-[#3482a1]`) in feature code. All styles must reference design tokens or Tailwind theme classes.
2. **Component Versioning & Deprecation:** Maintain backward-compatible component APIs. Mark deprecated props with `@deprecated` docstrings and clear migration instructions.

### F. Platform & Framework Adaptation
- Support Tailwind CSS v4 / v3, CSS Modules, vanilla CSS, and design token integration in React, Next.js, Vue, or Flutter.

---

## 3. MANDATORY DESIGN SYSTEM DELIVERABLES

When implementing or upgrading a design system, document:
1. **Design Tokens Dictionary (JSON/CSS)**
2. **Semantic Color & Contrast Matrix**
3. **Typography Scale Specification**
4. **Spacing & Elevation Token Map**
5. **Component Primitives Contract & Variant Table**
6. **Theme Configuration Strategy**
