# Human-Crafted Design System
## Foundational Token Architecture & Visual Invariants

This document establishes the canonical token architecture, spacing rhythm, and interaction contracts for user interfaces engineered within OpenClone.

---

## 1. Spatial Grid & Spacing Rhythm

OpenClone adopts a strict **8-point spatial grid** (with a 4-point half-step for micro-adjustments). Arbitrary pixel values (e.g., `margin-top: 13px`) are strictly prohibited.

```css
:root {
  --space-0: 0px;
  --space-1: 4px;   /* Micro-gap (icon + label, border-radius) */
  --space-2: 8px;   /* Tight padding (button inline padding, tag spacing) */
  --space-3: 12px;  /* Compact spacing (input padding, card internal gap) */
  --space-4: 16px;  /* Standard base unit (card padding, list item gaps) */
  --space-6: 24px;  /* Medium layout gap (grid columns, section sub-headers) */
  --space-8: 32px;  /* Large layout gap (card grid gaps, module separation) */
  --space-12: 48px; /* Section spacing on tablet/mobile */
  --space-16: 64px; /* Section spacing on desktop (desktop section rhythm) */
  --space-24: 96px; /* Hero top/bottom desktop breathing room */
}
```

---

## 2. Modular Typography Scale

Based on the **Major Third (1.250)** scale for web applications and dashboards, ensuring crisp hierarchy and readability:

```css
:root {
  --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-family-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;     /* 12px - Metadata, timestamps, badge labels */
  --text-sm: 0.875rem;    /* 14px - Secondary copy, table body, helper text */
  --text-base: 1.000rem;  /* 16px - Standard body text, inputs, button labels */
  --text-lg: 1.125rem;    /* 18px - Lead copy, subsection titles */
  --text-xl: 1.250rem;    /* 20px - Card headings, modal titles */
  --text-2xl: 1.500rem;   /* 24px - Section headings (H3) */
  --text-3xl: 1.875rem;   /* 30px - Page titles (H2) */
  --text-4xl: 2.250rem;   /* 36px - Hero headlines (H1) */
  --text-5xl: 3.000rem;   /* 48px - Display / Marketing hero statements */

  /* Line Heights */
  --leading-tight: 1.20;
  --leading-snug: 1.35;
  --leading-normal: 1.50;
  --leading-relaxed: 1.65;
}
```

---

## 3. Surface & Elevation Hierarchy

To prevent the "flat card ocean" typical of AI designs, OpenClone establishes a **5-tier surface hierarchy**:

```
+-----------------------------------------------------------------------------------+
| Tier 5: Modal & Drawer Overlay  (Z: 1000)  |  --surface-overlay                   |
| Tier 4: Popover & Dropdown Menu (Z: 500)   |  --surface-popover                   |
| Tier 3: Floating Card / Raised  (Z: 100)   |  --surface-elevated                  |
| Tier 2: Standard Container / S2 (Z: 10)    |  --surface-2 (Sidebar, Table Header) |
| Tier 1: Base Canvas Ground     (Z: 0)     |  --surface-1 (Main App Canvas)       |
+-----------------------------------------------------------------------------------+
```

```css
:root {
  /* Dark Theme Tokens (Default) */
  --surface-base: #0c0e12;
  --surface-1: #12151b;
  --surface-2: #181c24;
  --surface-elevated: #202632;
  --surface-overlay: rgba(12, 14, 18, 0.85);

  /* Border Tokens */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-default: rgba(255, 255, 255, 0.14);
  --border-strong: rgba(255, 255, 255, 0.25);
  --border-focus: #3b82f6;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.25);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.35), 0 2px 4px -2px rgba(0, 0, 0, 0.25);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.45), 0 4px 6px -4px rgba(0, 0, 0, 0.35);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.55), 0 8px 10px -6px rgba(0, 0, 0, 0.45);
}
```

---

## 4. Interaction Timing & Motion Invariants

Human-crafted UI feels snappy and tactile. Interactions must avoid slow, floaty tweening:

- **Button Press / Click State**: `100ms ease-out` (immediate tactile feedback, 1px depression).
- **Hover Transitions**: `150ms ease-out` in, `120ms ease-out` out.
- **Modal / Flyout In**: `200ms cubic-bezier(0.16, 1, 0.3, 1)` (decelerate).
- **Modal / Flyout Out**: `150ms cubic-bezier(0.7, 0, 0.84, 0)` (accelerate out).
- **Focus Ring**: Instant (`transition: none`), `outline: 2px solid var(--border-focus)`, `outline-offset: 2px`.
