# Motion & Animation Engineering Guide
**Physics Easing, Microinteractions, View Transitions, and Accessibility Standards**  
*OpenClone Global Design Intelligence | Engineering Purposeful Continuity*

---

## 1. Principles of Purposeful Motion

Motion in software interfaces serves three vital functions:
1. **Spatial Continuity**: Orienting users as contexts change (e.g., expanding a card into a detail view).
2. **Immediate Feedback**: Confirming physical touch, clicks, and state changes (<150ms).
3. **Hierarchy & Attention**: Guiding the user's eye to primary updates without jarring disruption.

> 🚫 **Anti-Slop Rule**: Never add continuous spinning badges, random floating background blobs, or unprompted entrance wobbles. If an animation does not explain a state change or provide feedback, remove it.

---

## 2. Timing, Easing & Performance Budgets

### Standard Timing Tokens
- **Micro-Interactions** (Button hover, checkbox toggle, chip press): `100ms – 150ms`
- **Component Expansions** (Dropdown menus, accordions, tooltips): `200ms – 250ms`
- **Page / Modal Transitions** (Dialog backdrop, drawer slide, route change): `300ms – 400ms`
- **Complex Orchestrations** (Staggered list load, data chart reveal): `400ms – 600ms` max

### Physical Easing Curves
```css
:root {
  /* Snappy entry: Fast start with gentle deceleration */
  --ease-out-quad: cubic-bezier(0.25, 1, 0.5, 1);
  /* Smooth natural movement: Human hand deceleration */
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  /* Tactile spring effect for micro-interactions */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### The 60fps / 120fps Compositor Rule
To eliminate layout thrashing and dropped frames:
- **Animate ONLY `transform` and `opacity`**.
- Never animate `width`, `height`, `margin`, `padding`, `top`, `left`, or `border-width`.
- Use `will-change: transform` sparingly on active animating surfaces only.

---

## 3. Reduced-Motion Accessibility (`prefers-reduced-motion`)

Every animated component MUST provide an instantaneous, non-animated fallback for users with vestibular disorders:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 4. Interaction Patterns

1. **Button Hover & Active Press**:
   ```css
   .btn-tactile {
     transition: transform 120ms var(--ease-out-quad), box-shadow 120ms ease;
   }
   .btn-tactile:hover {
     transform: translateY(-1px);
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
   }
   .btn-tactile:active {
     transform: translateY(1px);
     box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
   }
   ```
2. **Skeleton Shimmer Loading**:
   Subtle light gradient moving across gray base with low opacity (0.04 to 0.08) at 1.5s loop.
3. **View Transitions**:
   Using `document.startViewTransition()` to smoothly morph shared elements between routes.
