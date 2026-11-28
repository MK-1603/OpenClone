# Component Family 14: AI Chat, Prompts & Streaming Interfaces
**Registry ID Range:** `C-1401` to `C-1404`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
AI conversational surfaces require auto-expanding omnibars, streaming markdown message bubbles, collapsible thinking accordions, and real-time token/cost counters.

## 2. Headless Foundation & Styling
- **Engine:** `@radix-ui/react-collapsible` + auto-resizing textarea.
- **Bubble Surface:**
  - User bubble: `bg-zinc-800 text-zinc-100 rounded-2xl rounded-tr-sm px-4 py-3`.
  - Assistant bubble: `bg-[#121215] border border-white/10 rounded-2xl rounded-tl-sm px-4 py-3`.

## 3. TypeScript Prop Contract
```typescript
export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  streaming?: boolean;
  thoughtProcess?: string;
  tokenCount?: number;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Empty chat timeline with starter suggestion chips.
- `LOADING`: Streaming cursor pulse with thought accordion.
- `SUCCESS`: Formatted markdown with copy-to-clipboard code blocks.
- `ERROR`: Inline error retry pill with regenerate action.

## 5. WCAG 2.2 AAA Accessibility
- Screen reader announcements for new assistant responses via `aria-live="polite"`.
- Code blocks include accessible language headers and copy confirmation status.
