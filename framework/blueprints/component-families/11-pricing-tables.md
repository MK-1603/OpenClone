# Component Family 11: Pricing Tables & Feature Tiers
**Registry ID Range:** `C-1101` to `C-1103`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Pricing tables structure commercial tiers (Free, Pro, Enterprise), billing cadence toggles (Monthly/Annual), and feature comparison matrices.

## 2. Headless Foundation & Styling
- **Engine:** `@radix-ui/react-switch` + `@radix-ui/react-accordion`.
- **Card Highlight:** Featured tier features a machined cyan/purple specular top highlight (`via-cyan-400/30`).

## 3. TypeScript Prop Contract
```typescript
export interface PricingTier {
  id: string;
  name: string;
  priceMonthly: number;
  priceAnnual: number;
  description: string;
  features: string[];
  ctaLabel: string;
  highlighted?: boolean;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Renders default monthly pricing cards.
- `LOADING`: Shimmer skeletons covering price figures and feature lists.
- `SUCCESS`: Animated price switch with annual discount badge.

## 5. WCAG 2.2 AAA Accessibility
- Pricing switch uses `role="switch"` with clear checked status.
- Feature items use semantic lists `<ul>` with accessible checkmark icons.
