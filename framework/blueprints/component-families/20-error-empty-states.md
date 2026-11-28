# Component Family 20: Error Pages & Empty States
**Registry ID Range:** `C-2001` to `C-2003`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Error and empty states handle unexpected failures (404 Not Found, 500 Server Error, Network Disconnect) and zero-data screens, guiding users back to safety with clear recovery actions.

## 2. Headless Foundation & Styling
- **Pattern:** Centered landmark `<main>` with obsidian card styling, mono error codes (`ERR_CONNECTION_REFUSED`), and primary action buttons.

## 3. TypeScript Prop Contract
```typescript
export interface ErrorPageProps {
  statusCode: number;
  title: string;
  message: string;
  retryAction?: () => void;
  homeUrl?: string;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Rendered error state.
- `LOADING`: Spinning re-connection button during retry attempt.
- `SUCCESS`: Smooth transition back to restored content.

## 5. WCAG 2.2 AAA Accessibility
- Page title `<title>` and `<h1>` clearly identify error code and status.
- Text contrast ratio exceeds 7:1 against base ground.
- Primary CTA button meets 44px minimum tap target.
