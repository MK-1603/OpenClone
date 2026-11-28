# Motion Design & Choreography Framework
## Physics-Based Spring Timing, Staggered Entrances & Accessibility Compliance

**Domain:** `05-UX-UI-ENGINEERING`  
**Standard ID:** `MDC-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Purpose & Philosophy

Motion in OpenClone is functional, purposeful, and grounded in physical mechanics. It exists to communicate state transitions, spatial continuity, and tactile feedback. Unprompted, distracting, or nausea-inducing continuous ambient oscillations are strictly banned.

---

## 2. Duration Tiers & Timing Budgets

Every animation in OpenClone must adhere to three strict duration tiers:

1. **Tier 1 — Micro-Interactions (100ms–150ms):**
   - Button presses, hover lifts, checkbox toggles, tooltips.
   - Purpose: Immediate, crisp tactile confirmation.
2. **Tier 2 — Layout & Drawer Transitions (200ms–250ms):**
   - Modal entrances, accordion expansions, flyout sheet slides, tab switches.
   - Purpose: Smooth visual continuity without perceived latency.
3. **Tier 3 — Page & Hero Entrances (350ms–400ms):**
   - Initial hero load, staggered bento card entrances.
   - Purpose: Confident brand arrival.

---

## 3. Physics Spring Token Matrix

```javascript
export const springTokens = {
  // Snappy: For buttons, switches, and toggles
  snappy: {
    stiffness: 400,
    damping: 30,
    mass: 0.8,
  },
  // Smooth: For dialogs, popovers, and sheets
  smooth: {
    stiffness: 260,
    damping: 24,
    mass: 1.0,
  },
  // Gentle: For layout expansions and accordion bodies
  gentle: {
    stiffness: 180,
    damping: 22,
    mass: 1.2,
  },
};
```

---

## 4. Mandatory Accessibility: `prefers-reduced-motion`

In accordance with WCAG 2.2 AAA (Guideline 2.3.3):
- Every animation MUST be guarded by `@media (prefers-reduced-motion: reduce)` in CSS or Framer Motion `useReducedMotion()`.
- When reduced motion is requested, motion properties (`transform`, `x`, `y`, `scale`) must be converted to instant `opacity: 1` cuts without spatial translation.
- Infinite running loops (such as marquees or pulse animations) must automatically halt.
