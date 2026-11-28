# User-Choice Design Patterns
## Supporting Glassmorphism, UI Morphism, Brutalism & Swiss Minimalism without AI Slop

A central principle of OpenClone and Taste Skill is:
**We do not dogmatically ban aesthetic styles. We ban unprompted, unmotivated, uncrafted generic AI slop.**

When a user explicitly requests a specific aesthetic—such as **Glassmorphism**, **Neumorphism** ("UI morphism"), **Brutalism**, or **Swiss Minimalism**—or when a product's brand strategy genuinely demands it, the framework treats the style as **`REQUIRED`** or **`JUSTIFIED`**. 

This document defines the exact tokens, CSS rules, accessibility fallbacks, and engineering specifications for executing these styles at a human-crafted, professional standard.

---

## 1. Glassmorphism & Translucent Depth

### When is it Allowed?
- **AI Slop (`UNNECESSARY` / `PROHIBITED`)**: An agent randomly throws `backdrop-filter: blur(12px)` and `background: rgba(255,255,255,0.05)` on every card on a standard B2B SaaS landing page without contrast consideration.
- **Human-Crafted Craft (`REQUIRED` / `JUSTIFIED`)**:
  - The user explicitly requested glass or translucent UI morphism.
  - The application is an OS-level control center, a floating HUD, a media-rich player, or a translucent modal overlay where seeing the underlying canvas provides spatial orientation.

### Engineering Specification:
```css
/* Canonical Human-Crafted Glassmorphism Tokens */
:root {
  --glass-surface-base: rgba(18, 20, 26, 0.72);
  --glass-surface-elevated: rgba(26, 30, 40, 0.82);
  --glass-border-hairline: rgba(255, 255, 255, 0.12);
  --glass-border-specular: rgba(255, 255, 255, 0.24);
  --glass-blur-radius: 16px;
  --glass-saturation: 180%;
  --glass-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.36), 0 1px 2px 0 rgba(0, 0, 0, 0.18);
}

.surface-glass {
  background: var(--glass-surface-base);
  backdrop-filter: blur(var(--glass-blur-radius)) saturate(var(--glass-saturation));
  -webkit-backdrop-filter: blur(var(--glass-blur-radius)) saturate(var(--glass-saturation));
  border: 1px solid var(--glass-border-hairline);
  box-shadow: var(--glass-shadow);
  border-radius: 12px;
}

/* Specular Top Edge Light Reflection */
.surface-glass-sheen {
  position: relative;
}
.surface-glass-sheen::before {
  content: "";
  position: absolute;
  top: 0;
  left: 12px;
  right: 12px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--glass-border-specular), transparent);
  pointer-events: none;
}
```

### Accessibility & Contrast Invariants:
1. **Backing Contrast Scrim**: Text placed over glass MUST achieve **WCAG 2.2 AA (>= 4.5:1 for body, >= 3:1 for large text)** under all underlying scroll content. If background images are dynamic, an opaque or 85%+ tint underlayer is mandatory.
2. **Fallback for Unsupported Browsers**:
   ```css
   @supports not (backdrop-filter: blur(1px)) {
     .surface-glass {
       background: #14171f; /* Solid fallback surface */
       border: 1px solid rgba(255, 255, 255, 0.15);
     }
   }
   ```
3. **Contrast Preference Respect**:
   ```css
   @media (prefers-contrast: more) {
     .surface-glass {
       background: #0f1117 !important;
       border: 2px solid #ffffff !important;
       backdrop-filter: none !important;
     }
   }
   ```

---

## 2. Neumorphism & Soft UI Morphism

### When is it Allowed?
- **AI Slop (`PROHIBITED`)**: Low-contrast gray-on-gray forms where input fields have no visible borders and focus states are completely indistinguishable.
- **Human-Crafted Craft (`REQUIRED` / `JUSTIFIED`)**:
  - The user explicitly requests soft UI or neumorphic tactile controls.
  - Hardware controller interfaces, audio synthesizers, or IoT device dashboards where tactile physical realism is the core aesthetic.

### Engineering Specification:
```css
:root {
  --neu-base: #e0e5ec;
  --neu-shadow-dark: rgba(163, 177, 198, 0.65);
  --neu-shadow-light: rgba(255, 255, 255, 0.85);
  --neu-focus-ring: #2563eb;
}

.neu-button {
  background: var(--neu-base);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  box-shadow: 6px 6px 12px var(--neu-shadow-dark),
              -6px -6px 12px var(--neu-shadow-light);
  color: #1e293b;
  font-weight: 500;
  transition: box-shadow 150ms ease-out, transform 150ms ease-out;
}

.neu-button:active {
  box-shadow: inset 4px 4px 8px var(--neu-shadow-dark),
              inset -4px -4px 8px var(--neu-shadow-light);
  transform: translateY(1px);
}

/* Mandatory WCAG Focus Ring */
.neu-button:focus-visible {
  outline: 2px solid var(--neu-focus-ring);
  outline-offset: 3px;
}
```

---

## 3. Swiss / International Typographic Style

### Characteristics:
- Asymmetric grid layouts based on strict 12-column divisions.
- Typography as the primary visual element (Helvetica Neue, Inter, Neue Haas Grotesk).
- High information density, flush-left rag-right text, zero decorative ornaments.
- Ideal for: Financial portals, developer dashboards, technical documentation.

---

## 4. Industrial & Brutalist Interfaces

### Characteristics:
- High contrast borders (`border: 2px solid #000000` or `#ffffff`).
- Monospace typographic accents for metadata, timestamps, and status codes.
- High-saturation spot colors used strictly for functional signaling (warning yellow, system green, alert red).
- Zero soft dropshadows; strict directional hard shadows (`box-shadow: 4px 4px 0 #000000`).
- Ideal for: Security terminals, developer command centers, crypto/Web3 developer tooling.

---

## 5. Evaluation Matrix Summary

| Aesthetic Style | Unprompted AI Default | User-Requested / Justified Context | Taste Skill Slop Gate Action |
|---|---|---|---|
| **Glassmorphism** | `UNNECESSARY` | `REQUIRED` or `JUSTIFIED` | Allow if requested; enforce WCAG AA contrast scrim |
| **Neumorphism** | `PROHIBITED` | `REQUIRED` | Allow if requested; mandate visible borders & focus ring |
| **Purple/Indigo Gradients** | `PROHIBITED` | `JUSTIFIED` | Flagged; replace with trade-tailored brand palette |
| **Floating Blur Blobs** | `PROHIBITED` | `UNNECESSARY` | Remove; replace with structured surface hierarchy |
| **Swiss Minimalist** | `OPTIONAL` | `REQUIRED` | Fully supported; verify 8pt rhythm & type contrast |
| **Industrial / Brutalist** | `OPTIONAL` | `REQUIRED` | Fully supported; verify accessibility and hard shadows |
