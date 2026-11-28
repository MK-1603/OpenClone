# Component Family 06: Forms, Inputs & Multi-Step Wizards
**Registry ID Range:** `C-0601` to `C-0606`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Forms govern transactional interactions, data entry, and multi-step onboarding. They mandate strict schema validation (`zod`), clear error messaging linked via ARIA attributes, and floating label feedback.

## 2. Headless Foundation & Styling
- **Engine:** `react-hook-form` + `zod` + `@radix-ui/react-select`.
- **Styling Architecture:**
  - Base input: `bg-[#09090b] border border-white/10 rounded-lg px-3 py-2 text-zinc-100`.
  - Focus state: `focus-visible:ring-2 focus-visible:ring-white/80 focus-visible:border-transparent`.

## 3. TypeScript Prop Contract
```typescript
import { z } from "zod";
import { UseFormReturn } from "react-hook-form";

export interface FormProps<TSchema extends z.ZodType<any, any>> {
  schema: TSchema;
  defaultValues: z.infer<TSchema>;
  onSubmit: (values: z.infer<TSchema>) => Promise<void>;
  children: (form: UseFormReturn<z.infer<TSchema>>) => React.ReactNode;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Clean form inputs with clear default values.
- `LOADING`: Disabled fields with animated spinner on submit button.
- `SUCCESS`: Inline success validation checkmarks.
- `ERROR`: Inline red highlight with accessible `aria-errormessage`.
- `PARTIAL`: Form state cached in sessionStorage during wizard step progression.

## 5. WCAG 2.2 AAA Accessibility
- Every input has an explicitly linked `<label htmlFor="id">`.
- Error messages are declared with `aria-live="polite"` and linked via `aria-describedby`.
- 44px minimum touch target on submit buttons and select triggers.
