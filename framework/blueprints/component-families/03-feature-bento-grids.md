# Component Family 03: Feature Grids & Bento Layouts
**Registry ID Range:** `C-0301` to `C-0305`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Bento grids arrange modular product capabilities into asymmetric, visually engaging card clusters. Every card features independent surface elevations, subtle top specular highlights, and micro-hover zoom interactions.

## 2. Headless Foundation & Styling
- **Grid Architecture:** CSS Grid utilizing `@container` queries for fluid card restructuring:
  ```css
  .bento-container {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 1.5rem;
  }
  @container (max-width: 768px) {
    .bento-container { grid-template-columns: 1fr; }
  }
  ```

## 3. TypeScript Prop Contract
```typescript
export interface BentoCardProps {
  colSpan?: 3 | 4 | 6 | 8 | 12;
  title: string;
  description: string;
  icon?: React.ComponentType<{ className?: string }>;
  graphicSlot?: React.ReactNode;
  badge?: string;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Renders card outlines with semantic headings.
- `LOADING`: Multi-card shimmer skeleton preserving exact column spans.
- `SUCCESS`: Interactive cards with 2px hover lift (`transform: translateY(-2px)`).
- `EMPTY`: Renders default feature highlights.
- `ERROR`: Resilient fallback display of static feature text.

## 5. WCAG 2.2 AAA Accessibility
- Semantic `<article>` or `<li>` list structure.
- Focus-visible outlines around interactive cards.
- Hover animations automatically disabled under `@media (prefers-reduced-motion)`.
