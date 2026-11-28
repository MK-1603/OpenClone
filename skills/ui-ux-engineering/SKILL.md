---
name: ui-ux-engineering
description: Ultra-premium, modern 2026 UI/UX Engineering Standard. Enforces Glassmorphism, Dark Luxury (Linear/Vercel aesthetic), Spatial UI, Taste Skill anti-slop rules, 8-point typography scales, WCAG 2.2 AAA accessibility, and fluid responsive layouts (320px-1440px+).
version: 2.0.0
---

# Modern UI/UX Engineering Skill (2026 Standard)

## Purpose & Vision
Elevate web and mobile application interfaces from dated, generic "AI-generated" boilerplate into **cutting-edge, human-crafted digital experiences**. This standard combines **Glassmorphism**, **Dark Luxury**, and **Spatial UI** with uncompromising WCAG 2.2 AAA accessibility and mathematical typographic precision.

---

## 1. Modern Aesthetic Archetypes (2026 Design Systems)

### A. Dark Luxury / Obsidian Precision (Linear / Vercel Standard)
- **Base Canvas:** Deep obsidian neutral (`#09090b` or `#08090a`), never muddy washed-out gray.
- **Surface Elevation Hierarchy:**
  - Base Ground: `#09090b`
  - Layer 1 (Cards, Sections): `#121215` with `border: 1px solid rgba(255, 255, 255, 0.06)`
  - Layer 2 (Elevated, Modals): `#18181b` with `border: 1px solid rgba(255, 255, 255, 0.1)`
  - Hover Highlight: `#202024` with 150ms ease-out transition.
- **Top-Edge Specular Lighting (The Machined Bevel):**
  Card headers feature a subtle 1px specular highlight simulating overhead studio lighting:
  ```css
  /* Tailwind: relative overflow-hidden before:absolute before:inset-x-0 before:top-0 before:h-px before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent */
  .specular-card {
    position: relative;
    background: #121215;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
  }
  .specular-card::before {
    content: '';
    position: absolute;
    inset-inline: 0;
    top: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.22), transparent);
  }
  ```

---

### B. High-End Frosted Glassmorphism & Spatial Depth
Forget cheap 2024 blurred blobs. Modern glassmorphism uses **multi-stop translucent scrims** with high contrast and tactile borders:
```css
/* Premium Glassmorphic Surface */
.glass-surface {
  background: rgba(18, 18, 22, 0.65);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: 
    0 4px 24px -1px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}
```
* **Contrast Scrim Rule:** Any text rendered on a glass surface must have an underlying contrast scrim (`rgba(0,0,0,0.5)` or high-contrast token) guaranteeing a minimum **7:1 WCAG contrast ratio**.

---

### C. Tactile Micro-Interactions & Hardware Feel
- **Button Micro-Step:** On hover, buttons lift 1px (`transform: translateY(-1px)`). On active click, buttons depress 1px (`transform: translateY(1px)`) with crisp tactile feedback.
- **Keyboard Shortcut Badges:** Native command chips (`⌘K`, `⇧P`, `Esc`) styled with subtle border insets:
  ```html
  <kbd class="px-1.5 py-0.5 text-xs font-mono bg-white/[0.06] border border-white/[0.12] rounded text-zinc-300 shadow-sm">⌘K</kbd>
  ```
- **Pulsing Status Dots:** Real-time health indicators using dual-ring pulse animations:
  ```html
  <span class="relative flex h-2 w-2">
    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
  </span>
  ```

---

### D. Modern Skeleton Shimmer Loaders
Replace static gray boxes with fluid velocity shimmers:
```css
@keyframes shimmer {
  100% { transform: translateX(100%); }
}
.skeleton-shimmer {
  position: relative;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.04);
}
.skeleton-shimmer::after {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  transform: translateX(-100%);
  background-image: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0,
    rgba(255, 255, 255, 0.06) 20%,
    rgba(255, 255, 255, 0.1) 60%,
    rgba(255, 255, 255, 0)
  );
  animation: shimmer 2s infinite;
  content: '';
}
```

---

## 2. Mathematical Typography Scale (Fluid 8-Point)

Use fluid modular scales with CSS `clamp()` so titles scale seamlessly from mobile (390px) to ultra-wide (1440px+):

| Level | Desktop Size | Mobile Size | Line Height | Tracking | Weight |
|---|---|---|---|---|---|
| **Display Hero** | `clamp(2.5rem, 5vw + 1rem, 4.5rem)` | 36px | 1.05 | `-0.03em` | Bold (700) |
| **Heading 1** | `clamp(2rem, 3vw + 0.75rem, 3rem)` | 28px | 1.15 | `-0.025em` | SemiBold (600) |
| **Heading 2** | `24px` | 20px | 1.25 | `-0.02em` | SemiBold (600) |
| **Heading 3** | `18px` | 16px | 1.35 | `-0.01em` | Medium (500) |
| **Body (Default)**| `15px` | 15px | 1.6 | `0` | Regular (400) |
| **Caption/Meta** | `12px` | 12px | 1.5 | `+0.01em` | Medium (500) |

- **Font Pairing Standard:**
  - Interface & Headings: `Geist Sans`, `Inter`, or `Plus Jakarta Sans`.
  - Metrics, Code & Data: `Geist Mono` or `JetBrains Mono`.

---

## 3. Responsive Breakpoints & Mobile Touch Targets

1. **Touch Target Guarantee:** All clickable elements (buttons, inputs, dropdown items, icon triggers) must measure **at least 44x44 CSS pixels** on touchscreens (`min-h-[44px] min-w-[44px]`).
2. **Safe-Area Insets:** Always bind bottom action bars and sticky navigation to device safe areas:
   ```css
   padding-bottom: max(16px, env(safe-area-inset-bottom));
   ```
3. **Zero Horizontal Overflow:** Strict containment:
   ```css
   body, #__next, main { overflow-x: hidden; width: 100%; max-width: 100vw; }
   ```

---

## 4. What We Strictly Reject (Anti-AI-Slop 2026 Checklist)
- ❌ Do NOT use floating, unattached ambient blur circles (`blur-3xl bg-indigo-500/20`).
- ❌ Do NOT use neon cartoon glow borders around cards (`box-shadow: 0 0 25px #8b5cf6`).
- ❌ Do NOT generate generic 3-column feature cards with colorful floating icons.
- ❌ Do NOT write buzzword headings ("Empower Your Tomorrow", "Unleash Innovation"). Write concrete, truthful copy ("Monitor Postgres query latency in real time").
