# Skeletons, Loading & Resilient States Engineering Standard
## Elimination of Layout Shifts (CLS < 0.05) and Resilient UI State Architecture

**Domain:** `05-UX-UI-ENGINEERING`  
**Standard ID:** `SRS-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. The Resilient State Imperative

Every dynamic, data-driven component engineered under OpenClone must eliminate jarring visual jumps and layout shifts (Cumulative Layout Shift target: $\text{CLS} < 0.05$). To achieve this, OpenClone mandates a **layout-matched skeleton architecture**:
- Never render a generic gray box.
- Never let content push surrounding elements down upon arrival.
- Always reserve the exact bounding dimensions and aspect ratios of final rendered widgets.

---

## 2. The Mandatory 6-State Framework

For every user-facing route, component, and form, the engineering team must implement and verify:

1. `INITIAL`: Static server-side rendered shell with reserved bounding containers.
2. `LOADING`: Velocity-shimmer skeletons that mirror the exact typography line heights, table row heights, and avatar radiuses of final content.
3. `EMPTY`: Clear, informative zero-data state with a primary call-to-action (e.g. "Create your first project").
4. `SUCCESS`: Interactive, populated user interface with micro-animations.
5. `ERROR`: Localized error boundaries that preserve surrounding navigation and offer one-click retry actions.
6. `PARTIAL`: Graceful display of cached or stale data accompanied by a non-intrusive background sync indicator.

---

## 3. High-Velocity Shimmer CSS Specification

```css
@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

.skeleton-shimmer {
  position: relative;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-md, 8px);
}

.skeleton-shimmer::after {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  transform: translateX(-100%);
  background-image: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0,
    rgba(255, 255, 255, 0.06) 20%,
    rgba(255, 255, 255, 0.12) 60%,
    rgba(255, 255, 255, 0)
  );
  animation: shimmer 1.8s infinite cubic-bezier(0.4, 0, 0.2, 1);
  content: '';
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-shimmer::after {
    animation: none;
    background-image: none;
  }
}
```

---

## 4. Optimistic UI Updates & Rollback Protocol

When user interactions trigger asynchronous state updates (e.g. liking, starring, toggling status, reordering rows):
1. **Immediate Client Mutation:** Update local UI state immediately within 16ms (one frame) using React 19 `useOptimistic`.
2. **Background Dispatch:** Issue server action or API call with idempotency key.
3. **Rollback Safety Net:** If the server rejects the transaction with an HTTP 4xx/5xx or timeout, immediately revert the client state to prior snapshot and trigger a Sonner destructive error toast with retry capability.
