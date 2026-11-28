# Adaptive Layout Matrix v2.0
## CSS Container Queries (`@container`), Subgrid & Fluid Viewport Engineering

**Domain:** `05-UX-UI-ENGINEERING`  
**Standard ID:** `ALM-02`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Beyond Viewport Media Queries: Container Queries

In modern component-based architecture, widgets (such as metric cards, data tables, or bento tiles) are placed into varied parent layouts: a 12-column full-width canvas, a 4-column sidebar, or a 6-column modal.

Relying strictly on viewport media queries (`@media (min-width: 768px)`) breaks components when a desktop viewport places a widget inside a narrow drawer. **Adaptive Layout Matrix v2.0 mandates CSS Container Queries (`@container`)**:
- Layout shifts must be dictated by the component's immediate container width, NOT the window width.
- Every major structural wrapper defines `container-type: inline-size`.

```css
/* Container Query Example */
.card-wrapper {
  container-type: inline-size;
  container-name: bento-card;
}

@container bento-card (max-width: 420px) {
  .bento-card-content {
    flex-direction: column;
    gap: 0.75rem;
  }
}
```

---

## 2. The 6-Tier Responsive Breakpoint Matrix

| Tier | Breakpoint Name | Viewport Width | Typical Hardware Target | Layout Paradigm |
|---|---|:---:|---|---|
| **Tier 1** | Mobile Compact | `320px–479px` | iPhone SE, small Android phones | Single column, sticky bottom navigation, 44px tap targets |
| **Tier 2** | Mobile Standard | `480px–767px` | iPhone 15/16 Pro, Galaxy S24 | Fluid single column, compact header, collapsible drawers |
| **Tier 3** | Tablet Portrait | `768px–1023px` | iPad Mini, 10" Tablets | 2-column bento grids, collapsed navigation rail |
| **Tier 4** | Tablet Landscape | `1024px–1279px` | iPad Pro 11", small laptops | 3-column bento grids, persistent navigation rail |
| **Tier 5** | Desktop Standard | `1280px–1599px` | MacBook Pro 14"/16", FHD Monitors | Full 12-column grid, dual workspace panes |
| **Tier 6** | Ultrawide / 4K | `1600px–3840px` | 27"+ Studio Displays, Ultrawide | Centered max-width canvas (`max-w-7xl`), zero horizontal stretching |

---

## 3. Dynamic Viewport Units (`dvh` / `svh`)

To eliminate the classic mobile Safari bug where browser navigation bars clip bottom content:
- Use `100dvh` (Dynamic Viewport Height) for full-screen hero sections and modal dialogs.
- Never use fixed `100vh` on mobile-targeted layouts.
- Zero horizontal overflow (`overflow-x: hidden`) strictly enforced across all 6 tiers.
