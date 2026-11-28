# Component Family 09: Command Palettes & Global Search
**Registry ID Range:** `C-0901` to `C-0903`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Command palettes provide global keyboard-driven navigation (`⌘K` / `Ctrl+K`), fuzzy action filtering, and quick shortcuts across the entire application ecosystem.

## 2. Headless Foundation & Styling
- **Engine:** `cmdk` + `@radix-ui/react-dialog`.
- **Keyboard Chip:**
  ```html
  <kbd class="px-1.5 py-0.5 text-xs font-mono bg-white/[0.06] border border-white/[0.12] rounded text-zinc-300 shadow-sm">⌘K</kbd>
  ```

## 3. TypeScript Prop Contract
```typescript
export interface CommandItem {
  id: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
  shortcut?: string;
  onSelect: () => void;
  group?: string;
}

export interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  items: CommandItem[];
  placeholder?: string;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Rendered closed with active keyboard shortcut listener.
- `LOADING`: Renders search bar with pulsing skeleton results.
- `EMPTY`: Renders "No results found for query" with helpful suggestions.
- `SUCCESS`: Rendered group list with keyboard arrow navigation.

## 5. WCAG 2.2 AAA Accessibility
- Uses `role="combobox"` with `aria-expanded` and `aria-autocomplete="list"`.
- Keyboard arrow keys navigate items; `Enter` executes; `Escape` closes.
