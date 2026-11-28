# Component Family 05: Metrics & Analytics Dashboards
**Registry ID Range:** `C-0501` to `C-0505`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Metric cards summarize key operational indicators (KPIs), trends, and system telemetry. They require optical typography for numbers, delta status badges, real-time pulse dots, and SVG mini sparklines.

## 2. Headless Foundation & Styling
- **Pattern:** Machined Specular Card (`bg-[#121215]`) with top specular hairline.
- **Pulse Dot:**
  ```html
  <span class="relative flex h-2 w-2">
    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
  </span>
  ```

## 3. TypeScript Prop Contract
```typescript
export interface MetricCardProps {
  label: string;
  value: string | number;
  delta?: { value: string; positive: boolean; comparisonPeriod: string };
  sparklineData?: number[];
  status?: "healthy" | "warning" | "critical";
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Label with blank value slot.
- `LOADING`: Shimmer loader covering label, big number, and sparkline slot.
- `EMPTY`: Displays "No data recorded" with zero-state icon.
- `SUCCESS`: Rendered numbers with tabular numerals (`font-mono`).
- `ERROR`: Displays warning icon with retry action.
- `PARTIAL`: Stale metric displayed with amber warning indicator.

## 5. WCAG 2.2 AAA Accessibility
- Color is not the sole conveyor of information (trend uses text icon + "+/-" indicator).
- Numbers have a minimum 7:1 contrast ratio against the card ground.
