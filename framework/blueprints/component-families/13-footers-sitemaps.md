# Component Family 13: Footers & Sitemap Links
**Registry ID Range:** `C-1301` to `C-1303`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Footers conclude the page experience with complete sitemap links, legal disclosures, system status indicators, and dark/light theme selectors.

## 2. Headless Foundation & Styling
- **Pattern:** 4-Column Responsive Grid with top hairline divider (`border-t border-white/10`).

## 3. TypeScript Prop Contract
```typescript
export interface FooterLinkGroup {
  title: string;
  links: Array<{ label: string; href: string; external?: boolean }>;
}

export interface FooterProps {
  groups: FooterLinkGroup[];
  copyrightYear?: number;
  systemStatus?: { label: string; status: "operational" | "degraded" };
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Rendered sitemap links with static copyright text.
- `SUCCESS`: Live status pulse dot displaying current operational health.

## 5. WCAG 2.2 AAA Accessibility
- Semantic `<footer>` landmark.
- Link contrast ratio exceeds 7:1 against base ground (`text-zinc-400` on `#09090b`).
