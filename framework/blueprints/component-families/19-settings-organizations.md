# Component Family 19: Settings & Organization Management
**Registry ID Range:** `C-1901` to `C-1903`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Organization consoles govern team memberships, role-based access control (RBAC) permission matrices, profile preferences, and masked API key management.

## 2. Headless Foundation & Styling
- **Engine:** `@radix-ui/react-tabs` + `@radix-ui/react-checkbox`.
- **Masked Key Styling:** Monospace font with dot mask (`••••••••••••••••`) and reveal eye toggle.

## 3. TypeScript Prop Contract
```typescript
export interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: "owner" | "admin" | "member";
  twoFactorEnabled: boolean;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Active General Settings tab.
- `LOADING`: Tab panel shimmer skeleton.
- `SUCCESS`: Instant tab switching without page reload.
- `ERROR`: Inline validation error on email or key generation.

## 5. WCAG 2.2 AAA Accessibility
- Tabs use `role="tablist"`, `role="tab"`, and `role="tabpanel"` with `aria-controls`.
- Arrow keys switch active tab focus.
