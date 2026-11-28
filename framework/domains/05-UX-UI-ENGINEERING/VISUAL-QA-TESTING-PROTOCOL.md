# Visual Quality Assurance & Testing Protocol
## Automated Playwright Visual Snapshot Regression Testing Across Multi-Viewport Tiers

**Domain:** `05-UX-UI-ENGINEERING`  
**Protocol ID:** `VQA-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Overview & Purpose

Visual Quality Assurance (VQA) provides automated, deterministic regression protection against unintended visual drift, layout overflow, broken styling, or typographic misalignment.

Every user-facing application built with OpenClone must export and execute automated **Playwright Visual Snapshot fixtures** across four standardized viewport dimensions:
1. **Desktop Large:** `1440x900`
2. **Tablet Landscape:** `1024x768`
3. **Tablet Portrait:** `768x1024`
4. **Mobile Standard:** `390x844`

---

## 2. Playwright Visual Regression Harness

```typescript
import { test, expect } from '@playwright/test';

const viewports = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'tablet-landscape', width: 1024, height: 768 },
  { name: 'tablet-portrait', width: 768, height: 1024 },
  { name: 'mobile', width: 390, height: 844 },
];

for (const vp of viewports) {
  test(`Visual Regression: Dashboard Route on ${vp.name} (${vp.width}px)`, async ({ page }) => {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    await page.goto('/dashboard');
    
    // Wait for network idle and font loading
    await page.waitForLoadState('networkidle');
    await page.evaluate(() => document.fonts.ready);
    
    // Assert zero horizontal overflow
    const hasHorizontalScroll = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(hasHorizontalScroll).toBe(false);
    
    // Visual comparison with 0.1% strict threshold
    await expect(page).toHaveScreenshot(`dashboard-${vp.name}.png`, {
      maxDiffPixelRatio: 0.001,
      animations: 'disabled',
    });
  });
}
```

---

## 3. Pre-Flight Visual Verification Gate

Before an engineering task can declare completion:
- [x] All 4 viewport snapshots pass within the 0.001 diff threshold.
- [x] Zero horizontal overflow (`scrollWidth <= clientWidth`) on every route.
- [x] All image elements have rendered (`naturalWidth > 0`).
- [x] Font loading is verified without Flash of Unstyled Text (FOUT).
