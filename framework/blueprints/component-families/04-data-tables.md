# Component Family 04: Data Presentation & Complex Tables
**Registry ID Range:** `C-0401` to `C-0406`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Data tables power dense operational dashboards, financial logs, and inventory consoles. They require sorting, multi-column filtering, pagination, column visibility toggles, and layout-matched shimmer states without layout shift.

## 2. Headless Foundation & Styling
- **Headless Engine:** `@tanstack/react-table` + `@radix-ui/react-dropdown-menu`.
- **Styling Architecture:**
  - Obsidian surface `#09090b` with hairline row borders `rgba(255, 255, 255, 0.06)`.
  - Monospace font with `font-variant-numeric: tabular-nums` for numeric alignment.

## 3. TypeScript Prop Contract
```typescript
import { ColumnDef } from "@tanstack/react-table";

export interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  isLoading?: boolean;
  onRowClick?: (row: TData) => void;
  filterColumnKey?: string;
  searchPlaceholder?: string;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Table structure with empty body.
- `LOADING`: Renders 5-row matched skeleton shimmer with identical cell widths.
- `EMPTY`: Displays zero-state message with "Add Record" action.
- `SUCCESS`: Rendered data rows with row hover highlight (`#141418`).
- `ERROR`: Displays error boundary with "Retry Fetch" button.
- `PARTIAL`: Shows cached rows with non-intrusive revalidating indicator.

## 5. WCAG 2.2 AAA Accessibility
- Semantic `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` elements.
- Column headers include `aria-sort="ascending|descending|none"`.
- Keyboard navigation: Full Arrow-key and Tab navigability between cells.
