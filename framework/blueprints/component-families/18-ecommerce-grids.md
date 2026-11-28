# Component Family 18: E-Commerce Product Grids & Checkouts
**Registry ID Range:** `C-1801` to `C-1804`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
E-Commerce flows feature product cards with instant add-to-cart, flyout cart sheets with optimistic subtotal calculation, quantity steppers, and transparent order summaries.

## 2. Headless Foundation & Styling
- **Engine:** `@radix-ui/react-dialog` (cart drawer) + semantic HTML.
- **Card Surface:** Specular dark luxury product tile (`bg-[#121215]`) with image hover zoom (`scale-105 transition-transform duration-300`).

## 3. TypeScript Prop Contract
```typescript
export interface Product {
  id: string;
  title: string;
  priceCents: number;
  imageUrl: string;
  category: string;
  inStock: boolean;
}

export interface CartItem extends Product {
  quantity: number;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Product grid with cached items.
- `LOADING`: Image card shimmer skeleton with button placeholder.
- `EMPTY`: "Your cart is empty" with "Browse Catalogue" CTA.
- `SUCCESS`: Item added with slide drawer flyout and updated badge.
- `ERROR`: Out-of-stock badge with notify-me email field.

## 5. WCAG 2.2 AAA Accessibility
- Currency formatted with tabular figures.
- Flyout cart announces item additions via `aria-live="polite"`.
- 44px touch targets on quantity buttons.
