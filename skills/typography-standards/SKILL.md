---
name: typography-standards
description: Typographic scales, optical hierarchy, vertical rhythm, readability, line-height, and font pairing.
version: 1.0.0
---

# Typography Standards Skill

## Overview
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
  --space-12: 48px; /* Section spacing on tablet/mobile
... Full design system reference in framework/domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md
