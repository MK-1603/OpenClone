---
id: accessibility-engineering
name: Accessibility Engineering Skill
version: 1.0.0
category: accessibility
description: Semantic HTML, WCAG 2.2 AA standards, keyboard navigation, focus trapping, screen reader landmarks, color contrast, and reduced motion.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/accessibility-engineering/SKILL.md
triggers:
  - accessibility
  - a11y
  - wcag
  - aria
  - screen reader
  - keyboard navigation
  - focus trap
  - contrast
  - color contrast
  - reduced motion
  - semantic html
  - landmark
  - alt text
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 16
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Semantic HTML heading & landmark hierarchy mapped
  - Color contrast ratio pre-flight check (4.5:1 text, 3:1 controls)
  - Modal focus trap & keyboard navigation strategy specified
finish_gates:
  - WCAG 2.2 AA compliance verified with zero critical defects
  - Full keyboard-only walkthrough verified (no keyboard traps)
  - prefers-reduced-motion media query verified across animations
verification:
  - Automated axe-core / a11y linter checks
  - Screen reader landmark & accessibility tree audit
---

# Accessibility Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `accessibility` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `accessibility-specialist`, `frontend-engineer`, `frontend-test-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Ensure all software interfaces are fully usable, perceptible, operable, and understandable by people with diverse sensory, motor, cognitive, and physical capabilities. Accessibility is not an afterthought or checklist; it is an intrinsic engineering discipline embedded into component semantics, keyboard navigation, screen reader affordances, and visual contrast.

### Boundaries
- **In Scope:** Semantic HTML, WCAG 2.2 Level AA compliance, WAI-ARIA Authoring Practices (APG), keyboard navigation & focus management, modal focus trapping, visible focus indicators, color contrast & color-blindness independence, screen reader announcements & live regions, and reduced-motion support.
- **Out of Scope:** Server-side backend business logic.

---

## 2. REQUIRED EXPERTISE DOMAINS

### A. Semantic HTML Engineering
1. **First Rule of ARIA:** Use native HTML elements (`<button>`, `<a>`, `<input>`, `<dialog>`, `<nav>`, `<main>`) whenever possible. Never attach click handlers to unstyled `<div>` or `<span>` elements without proper role, tabIndex, and keyboard handlers.
2. **Heading Hierarchy:** Maintain an unbroken, logical heading structure (`H1` -> `H2` -> `H3`). Never skip heading levels purely for styling purposes.
3. **Landmark Regions:** Provide distinct semantic landmarks (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`) to allow screen reader users to jump effortlessly between page regions.

### B. Keyboard Accessibility & Focus Governance
1. **Full Keyboard Operability:** Every interactive control must be reachable and operable using `Tab`, `Shift+Tab`, `Enter`, `Space`, and Arrow keys.
2. **Visible Focus Rings:** Never remove CSS focus outlines (`outline: none` is strictly prohibited unless replaced by a custom high-visibility focus ring with minimum 2px width and 2px offset).
3. **Focus Trapping:** When a modal dialog opens, focus must be trapped within the modal. Background elements must be inert (`aria-hidden="true"`). Pressing `Escape` must close the modal and return focus to the trigger button.
4. **Skip Navigation Links:** Provide a visible-on-focus "Skip to main content" link at the very top of every page.

### C. Screen Reader Affordances & ARIA
1. **Accessible Names:** Every interactive icon button must have an accessible name via `aria-label` (e.g. `<button aria-label="Close dialog">`) or visually hidden text.
2. **Live Regions:** Use `aria-live="polite"` for dynamic content updates (e.g., search results count, async toast notifications) so screen readers announce changes without interrupting active speech.
3. **Form Error Association:** Explicitly associate error messages with their respective inputs using `aria-invalid="true"` and `aria-describedby="input-error-id"`.

### D. Visual Accessibility & Contrast
1. **Contrast Ratios (WCAG 2.2 AA):**
   - Normal text (< 18pt or < 14pt bold): Minimum **4.5:1** contrast against surface.
   - Large text (>= 18pt or >= 14pt bold): Minimum **3.0:1** contrast.
   - User interface components & graphical boundaries: Minimum **3.0:1** contrast.
2. **Color Independence:** Never use color as the sole indicator of status, priority, or action. Pair color with text labels, icons, or patterns (e.g. a green dot must be accompanied by the text "Active").

### E. Motion & Cognitive Accessibility
1. **Reduced Motion Support:** All CSS transitions and animations must respect `@media (prefers-reduced-motion: reduce)`:
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```
2. **No Flashing Content:** Content must not flash more than 3 times in any 1-second period (seizure risk prevention).

---

## 3. FINISH GATES & VERIFICATION

1. **Automated Axe / Linter Check:** Zero automated WCAG 2.2 AA violations.
2. **Keyboard-Only Walkthrough:** Complete end-to-end user workflows using exclusively the keyboard.
3. **Screen Reader Verification:** Test with NVDA, VoiceOver, or Orca; verify all controls announce their name, role, and current state.
