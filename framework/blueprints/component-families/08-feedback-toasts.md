# Component Family 08: Feedback, Alerts & Toasts
**Registry ID Range:** `C-0801` to `C-0803`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Feedback notifications inform users of asynchronous process outcomes (save confirmations, network errors, warnings) without interrupting primary task flows.

## 2. Headless Foundation & Styling
- **Engine:** `sonner` stacked toast engine + semantic HTML alerts.
- **Toast Styling:**
  - Frosted surface: `bg-[#18181b]/95 backdrop-blur-md border border-white/10 text-zinc-100 rounded-lg shadow-xl`.

## 3. TypeScript Prop Contract
```typescript
export interface AlertProps {
  variant: "info" | "success" | "warning" | "destructive";
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
  onClose?: () => void;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Hidden in toast queue.
- `SUCCESS`: Slides in with spring animation and auto-dismiss timer (4000ms).
- `ERROR`: Persistent destructive alert with manual close button.
- `LOADING`: Indeterminate spinner toast during active API transaction.

## 5. WCAG 2.2 AAA Accessibility
- Success toasts announce via `role="status"` and `aria-live="polite"`.
- Critical destructive errors announce via `role="alert"` and `aria-live="assertive"`.
- Does not automatically time out when users are hovering or focusing on the message.
