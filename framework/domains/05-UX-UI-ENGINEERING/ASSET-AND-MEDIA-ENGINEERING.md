# Asset & Media Engineering Standard
## Modern Raster Optimization (AVIF/WebP), Vector SVG Standards & Iconography

**Domain:** `05-UX-UI-ENGINEERING`  
**Standard ID:** `AME-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Vector SVG Standards (Extending LEBIS)

Building upon OpenClone's Logo Engineering & Brand Identity System (LEBIS):
- All vector icons and logos must feature explicit `viewBox="0 0 W H"` attributes.
- Remove redundant fixed `width` and `height` attributes to enable fluid CSS scaling.
- Sanitize SVGs to strip XML declarations, comments, and inline `style` tags.
- Iconography standard: **Lucide React** (`strokeWidth={1.5}` or `2.0`).

---

## 2. Modern Raster Asset Pipeline

For photographic imagery, product previews, and avatars:
1. **Next-Gen Formats:** Always generate both **AVIF** and **WebP** formats with automatic fallback:
   ```html
   <picture>
     <source srcset="/assets/hero.avif" type="image/avif" />
     <source srcset="/assets/hero.webp" type="image/webp" />
     <img src="/assets/hero.jpg" alt="Product Console Interface" width="1200" height="675" loading="lazy" decoding="async" />
   </picture>
   ```
2. **Explicit Dimensions:** Every `<img>` tag must include explicit `width` and `height` aspect attributes to eliminate Cumulative Layout Shift (CLS).
3. **Responsive `srcset`:** Provide scaled widths (`390w`, `768w`, `1200w`, `1920w`) for responsive download optimization.
