# Design System Governance & Token Management

**Operating Rule:** Respect existing design systems. Token consistency precedes novelty.

---

## 1. Token Inspection Protocol

Before introducing new styling, the agent must check existing design tokens in this order:

1. **CSS Custom Properties (`:root`):**
   * Inspect existing color tokens: `--bg`, `--ink`, `--surface`, `--accent`, `--border`.
   * Inspect spacing scales: `--space-1`, `--space-2`, `--space-4`.
   * Inspect typography tokens: `--font-sans`, `--font-mono`, `--font-display`.
2. **Tailwind / CSS-in-JS Tokens:**
   * Inspect `tailwind.config.*` for extended colors, font families, and container sizes.
3. **Component Variant Alignment:**
   * Check how buttons, inputs, badges, and modals are structured.
   * If the project uses 4px border radii, never introduce 24px rounded corners in a new section.

---

## 2. Surface Hierarchy Invariants

Create depth through intentional surface layering rather than random blur or shadows:

* **Level 0 (Base Ground):** The viewport canvas background (`--bg`).
* **Level 1 (Surface Canvas):** Cards, content containers, structural sections (`--surface`).
* **Level 2 (Elevated Overlay):** Dropdowns, tooltips, sticky navigation bars, modals (`--surface-elevated`).
* **Border Contrast:** Surfaces must maintain minimum 1.2:1 contrast against adjacent grounds, enforced by crisp 1px borders rather than heavy drop shadows.

---

## 3. Design System Audit Report

Output: `.taste-skill/reports/design-system-audit.md`
Records tokens discovered, tokens reused, tokens deprecated, and brand alignment.
