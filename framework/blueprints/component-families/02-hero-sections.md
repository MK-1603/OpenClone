# Component Family 02: Hero Sections & Value Propositions
**Registry ID Range:** `C-0201` to `C-0206`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Hero sections communicate core value propositions, product identity, and primary calls-to-action within the first viewport screen. In compliance with Taste Skill and Dark Luxury standards, heroes eliminate ambiguous blur blobs in favor of machined specular borders, high-contrast typography, and real UI previews.

## 2. Headless Foundation & Styling
- **Pattern:** CSS 12-Column Grid with Specular Highlights.
- **Top-Edge Studio Lighting:**
  ```css
  .specular-hero-card {
    position: relative;
    background: #121215;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
  }
  .specular-hero-card::before {
    content: '';
    position: absolute;
    inset-inline: 0;
    top: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  }
  ```

## 3. TypeScript Prop Contract
```typescript
export interface HeroSectionProps {
  headline: string;
  subheadline: string;
  primaryAction: { label: string; href: string; onClick?: () => void };
  secondaryAction?: { label: string; href: string };
  badge?: { label: string; href?: string };
  previewComponent?: React.ReactNode;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Fast static SSR render of text and primary CTA.
- `LOADING`: Text shimmer skeleton with reserved preview aspect ratio.
- `SUCCESS`: Complete interactive hero with micro-step CTA button lifts.
- `ERROR`: Fallback static hero copy with primary contact CTA.
- `PARTIAL`: Static text displayed while interactive demo canvas loads in background.

## 5. WCAG 2.2 AAA Accessibility
- Headline uses semantic `<h1>` with optical tracking (`tracking-tight`).
- Contrast ratio between text and background exceeds 7:1.
- All CTA buttons meet the 44px minimum touch target requirement.
