---
id: responsive-engineering
name: Responsive Engineering Skill
version: 1.0.0
category: frontend
description: Mobile-first responsive layouts, 11-tier viewport matrix, adaptive navigation, touch targets, container queries, and zero overflow.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/responsive-engineering/SKILL.md
triggers:
  - responsive
  - mobile
  - mobile-first
  - breakpoint
  - viewport
  - touch
  - tablet
  - adaptive
  - overflow
  - drawer
  - sheet
  - hamburger
  - safe area
  - media query
  - flexbox
  - grid
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - desktop-fixed-only
precedence: 14
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Mobile-first breakpoint strategy defined
  - Mobile navigation & drawer architecture specified
  - Complex desktop component adaptations planned (tables, sidebars)
finish_gates:
  - Standard 11-tier viewport matrix verification pass (320px to 1440px+)
  - Zero unintended horizontal overflow verified (overflow-x: hidden enforced)
  - Interactive touch targets meet minimum 44x44px bounding box
verification:
  - Automated viewport matrix inspection
  - Touch-target geometry and overflow checks
---

# Responsive Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `frontend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `frontend-engineer`, `ui-designer`, `frontend-test-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Ensure that digital interfaces adapt naturally, reliably, and ergonomically across all display form factors, screen densities, input modalities, and device capabilities. Responsive Engineering enforces mobile-first development from the very first line of code, eliminating layout breakage, clipped typography, unreachable navigation, and horizontal scrollbars.

### Boundaries
- **In Scope:** Mobile-first layout architecture, fluid grids and flexbox containers, CSS container queries, breakpoint strategies, adaptive component patterns (mobile drawers, collapsible sidebars, card lists), touch ergonomics (44x44px minimum targets), mobile safe areas, virtual keyboard accommodation, and standard 11-tier viewport verification.
- **Out of Scope:** Core application business logic and backend APIs.

---

## 2. REQUIRED EXPERTISE DOMAINS

### A. Mobile-First Layout Engineering
1. **Mobile-First CSS:** Author default styles for the narrowest mobile screen (`320px`), progressively enhancing with min-width media queries (`sm:`, `md:`, `lg:`, `xl:`). Never write desktop-first CSS with overriding max-width media queries.
2. **Fluid Typography & Containers:** Use `clamp()`, percentages, and flex units instead of rigid pixel widths. Container max-widths should be paired with fluid padding (`px-4 sm:px-6 lg:px-8`).
3. **Zero Horizontal Overflow:** Enforce `overflow-x: hidden` on viewport roots and ensure all images and media have `max-width: 100%; height: auto;`.

### B. Adaptive Component Patterns
1. **Adaptive Navigation:**
   - **Mobile (< 768px):** Collapsible off-canvas drawer or bottom navigation bar with semi-transparent backdrop and touch gesture dismiss.
   - **Tablet / Desktop (>= 768px):** Permanent collapsible sidebar with icon rail or full expanded width.
2. **Responsive Data Tables:**
   - Multi-column tables must never break viewport boundaries.
   - Adapt complex tables on mobile by either:
     a) Transforming each row into a distinct, readable stacked card view.
     b) Wrapping the table in a horizontal touch-scrolling container with momentum scroll (`-webkit-overflow-scrolling: touch`).
3. **Responsive Forms & Dialogs:**
   - Full-screen or bottom-sheet presentation on mobile viewports (`max-h-[90vh] overflow-y-auto`).
   - Center-modal card presentation on tablet and desktop.
   - Form inputs stacked vertically on mobile, moving to side-by-side grids on wider screens.

### C. Touch Ergonomics & Device Adaptation
1. **Touch Target Sizing:** All interactive elements (buttons, links, icon toggles, form controls) must provide a minimum tap target of **44x44px** (W3C / Apple HIG / Android guidelines).
2. **Safe Area Insets:** Support mobile device notches and home indicator bars using `env(safe-area-inset-*)` padding.
3. **Virtual Keyboard Handling:** Ensure fixed bottom action bars or modals accommodate virtual keyboard appearance without obscuring focused input fields.

### D. Standard 11-Tier Viewport Verification Matrix

Every user interface must be verified across the following canonical viewports:

| Viewport Width | Device Category | Key Verifications |
|:---:|---|---|
| **320px** | Ultra-compact mobile (SE, small Android) | No overflow, readable fonts, 44px tap targets |
| **360px** | Compact Android mobile | Navigation works, forms fit cleanly |
| **375px** | Standard iPhone (mini / SE) | Layout hierarchy is clean and balanced |
| **390px** | Modern standard iPhone (12/13/14/15) | Touch gestures and cards render properly |
| **414px** | Large legacy mobile (Plus / Max) | Fluid spacing scales cleanly |
| **430px** | Large modern mobile (Pro Max / Plus) | High-density content reads effortlessly |
| **768px** | Standard tablet portrait (iPad) | Multi-column grid transition point |
| **820px** | Large tablet portrait (iPad Air) | Sidebar rail / split-pane activation |
| **1024px** | Compact laptop / Tablet landscape | Full desktop navigation enabled |
| **1280px** | Standard desktop / laptop | Primary desktop layout at standard density |
| **1440px+** | Large widescreen desktop | Max-width constraints prevent over-stretched lines |

---

## 3. FINISH GATES & VERIFICATION

1. **Zero Horizontal Overflow:** Entire document must satisfy `document.documentElement.scrollWidth <= window.innerWidth`.
2. **Navigation Parity:** All features accessible on desktop must remain accessible via mobile navigation.
3. **No Clipped Text:** Text wraps gracefully without truncated letters or unreadable line lengths.
