# OpenClone — UI/UX & Design Alternatives
**Version:** 1.0.0  
**Scope:** Alternatives for design tokens, component primitives, typography, animation, and visual review.

---

## 1. UI Component & Design System Matrix

| Capability | Current Primary | Fallback Candidate | Specialist Alternative | Recommendation |
|---|---|---|---|---|
| **Component Primitives** | `shadcn/ui` (Tailwind + Radix) | Headless UI / Radix Primitives | Park UI (Ark UI / Panda CSS) | Keep `shadcn/ui` as primary; copy-paste architecture avoids lock-in |
| **CSS Framework** | Tailwind CSS v3 / v4 | CSS Modules + PostCSS | Vanilla CSS Variables + Open Props | Tailwind CSS is industry standard; fallback to raw CSS variables |
| **Design Tokens** | CSS Custom Properties (`:root`, `.dark`) | Style Dictionary | Tailwind Config Theme Tokens | Native CSS Custom Properties have zero runtime cost and instant reactivity |
| **Typography System** | Modular Scales (Major Third / Perfect Fourth) | Tailwind Typography Plugin | Typescale.com Web Scales | Define 6-level typography scale in CSS tokens with fluid sizing |
| **Iconography** | Lucide Icons (React / SVG) | Phosphor Icons | Tabler Icons / Heroicons | Lucide is clean, tree-shakeable, and consistent; fallback to Phosphor |
| **Data Visualization** | Recharts / Visx (React) | Chart.js | Apache ECharts | Recharts for declarative dashboard charts; ECharts for high data volume |
| **Tables & Data Grids** | TanStack Table v8 (Headless) | AG Grid Community | Simple Semantic HTML Tables | TanStack Table provides full sorting, filtering, and pagination headless |
| **Dialogs & Overlays** | Radix Dialog / Portal | Native HTML `<dialog>` Element | Floating UI | Radix handles focus trapping and aria-modal attributes correctly |
| **Toast & Notifications** | Sonner | React Hot Toast | Custom Notification Store | Sonner has smooth physics, stacking, and keyboard dismissal |
| **Animation & Motion** | Native CSS Transitions + Web Animations API | Framer Motion / Motion | GSAP (Greensock) | Prefer native CSS transitions + spring easing curves; avoid bundle bloat |
| **Visual Regression** | Playwright Screenshot Diffing | BackstopJS | Percy / Applitools (SaaS) | Playwright provides deterministic headless browser screenshot diffing |
| **Accessibility Audit** | Axe-core / Lighthouse CLI | Pa11y | WAVE Web Accessibility Tool | Axe-core automated tests in CI; manual keyboard verification |

---

## 2. Motion & Physics Easing Guidelines

- **Default Choice:** Native CSS `transition` and `animation` utilizing physics-derived cubic-bezier easing tokens:
  ```css
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  ```
- **When to Use Framer Motion:** Only in complex layout orchestration, exit animations, or drag gestures.
- **Accessibility Gate:** Every animation MUST respect `@media (prefers-reduced-motion: reduce)`.
