# Existing Project First: Brownfield Audit Specification

**Operating Rule:** Never begin by replacing an existing user interface. Respect and extend what is already working.

---

## 1. Pre-Implementation Audit Checklist

Before writing new components or modifying styles in an existing repository, inspect:

1. **Framework & Dependencies:**
   * React, Next.js, Vue, Nuxt, Svelte, Astro, HTML/CSS.
   * Component libraries (Radix, shadcn/ui, MUI, Chakra, Tailwind UI).
   * Bundler and routing setup (`vite.config`, `next.config`, `app/` vs `pages/`).
2. **Design Tokens & Theme Invariants:**
   * Existing CSS variables (`--primary`, `--background`, `--font-sans`).
   * Tailwind configuration theme colors, spacing scales, border radii.
3. **Typography & Font Loading:**
   * Already loaded fonts. Do not inject redundant Google Fonts links if the project already bundles self-hosted typography.
4. **Existing Navigation & Interaction Models:**
   * Global navbars, sidebars, mobile drawer patterns.
   * Breadcrumbs, persistent footers, authentication shells.
5. **Accessibility & Responsive Baseline:**
   * Keyboard focus rings, color contrast levels, existing ARIA conventions.

---

## 2. The 5-Point Change Classification

Classify every proposed frontend change into one of four categories:

* **PRESERVE:** Core brand colors, functional user flows, working responsive navigation, existing authentication states, business data tables.
* **MODIFY:** Component styling to improve hierarchy, alignment fixes, font scale normalization, contrast improvements.
* **REMOVE:** Gratuitous visual clutter, duplicate cards, floating background blobs, non-functional icons.
* **ADD:** Missing responsive layouts, missing error/loading states, required new feature interfaces.

*Never delete working product features under the guise of aesthetic minimalism.*
