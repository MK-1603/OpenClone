# Component Family 07: Modals, Drawers & Dialogs
**Registry ID Range:** `C-0701` to `C-0704`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Modal dialogs and sliding drawers present focused interactive workspaces without losing background orientation. They mandate strict keyboard focus trapping, background blur scrims, and Escape-key dismissal.

## 2. Headless Foundation & Styling
- **Headless Primitive:** `@radix-ui/react-dialog` + `vaul` (mobile slide drawer).
- **Styling Architecture:**
  - Backdrop Scrim: `fixed inset-0 bg-black/60 backdrop-blur-sm`.
  - Dialog Surface: `fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#121215] border border-white/10 rounded-xl p-6 shadow-2xl`.

## 3. TypeScript Prop Contract
```typescript
export interface ModalDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Rendered off-DOM or with `display: none`.
- `LOADING`: Content replaced by modal-body shimmer skeleton.
- `SUCCESS`: Rendered modal with auto-focused first interactive control.
- `ERROR`: Dialog displays inline error banner with retry option.
- `PARTIAL`: Stale content displayed with non-blocking saving spinner.

## 5. WCAG 2.2 AAA Accessibility
- Automatic focus trap inside dialog when open.
- Focus returns to initiating trigger element upon closure.
- Closes on `Escape` key press; title linked via `aria-labelledby`.
