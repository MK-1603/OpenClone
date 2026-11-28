# Component Family 01: Navigation & Application Headers
**Registry ID Range:** `C-0101` to `C-0107`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Application headers establish navigation orientation, user identity, workspace context, and global search triggers. The header must maintain a fixed vertical budget (56px–64px) with high-contrast scrims guaranteeing WCAG 2.2 AAA readability over scrolling content.

## 2. Headless Foundation & Styling
- **Headless Primitive:** `@radix-ui/react-navigation-menu`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-dialog` (mobile drawer).
- **Styling Architecture:**
  ```css
  .app-header {
    height: 64px;
    background: rgba(9, 9, 11, 0.8);
    backdrop-filter: blur(16px) saturate(180%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  ```

## 3. TypeScript Prop Contract
```typescript
export interface AppHeaderProps {
  currentRoute: string;
  user?: { name: string; email: string; avatarUrl?: string };
  workspaces: Array<{ id: string; name: string; active: boolean }>;
  onSearchOpen: () => void;
  onWorkspaceChange: (id: string) => void;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Renders logo, search trigger button (`⌘K`), and placeholder navigation slots.
- `LOADING`: Renders header skeleton with shimmering breadcrumb and circular avatar placeholder.
- `EMPTY`: Renders public navigation links without workspace or user controls.
- `SUCCESS`: Full interactive navigation with active route highlights.
- `ERROR`: Reverts to safe fallback navigation with retry banner.
- `PARTIAL`: Renders cached navigation links while background session revalidates.

## 5. WCAG 2.2 AAA Accessibility
- Semantic landmark `<header>` and `<nav aria-label="Main Navigation">`.
- Minimum 44px touch targets on mobile drawer toggle.
- Unmistakable 2px focus ring (`ring-2 ring-white/80 ring-offset-2 ring-offset-zinc-950`).
