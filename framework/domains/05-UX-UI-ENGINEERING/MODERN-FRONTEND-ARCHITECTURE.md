# Modern Frontend Architecture Standard
## React 19 Server Components, Next.js 15 App Router & Zero-Waterfall Data Fetching

**Domain:** `05-UX-UI-ENGINEERING`  
**Standard ID:** `MFA-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Architectural Philosophy

Modern web applications engineered with OpenClone leverage **React 19** and **Next.js 15 (App Router)** to maximize runtime speed, eliminate client bundle bloat, and guarantee seamless SEO rendering.

---

## 2. Server Components (RSC) vs Client Components

- **Default to React Server Components (RSC):**
  - All data fetching, database queries, and static layout wrappers execute on the server.
  - Zero JavaScript shipped to client for purely visual layouts.
- **Isolate Client Components (`"use client"`):**
  - Restrict `"use client"` exclusively to leaf nodes that require browser APIs, state hooks (`useState`, `useReducer`), event listeners, or Framer Motion physics.
  - Never place `"use client"` at the route page level.

---

## 3. Streaming Boundaries with `<Suspense>`

To eliminate synchronous data waterfalls and render the visual shell instantly:
- Wrap every independent data-fetching widget in a React `<Suspense>` boundary.
- Assign the corresponding layout-matched skeleton shimmer as the `fallback` prop:
  ```tsx
  import { Suspense } from 'react';
  import { MetricCardSkeleton } from '@/components/ui/metric-card-skeleton';
  import { RevenueMetricCard } from '@/components/dashboard/revenue-metric-card';

  export default function DashboardPage() {
    return (
      <div className="grid grid-cols-12 gap-6">
        <Suspense fallback={<MetricCardSkeleton colSpan={4} />}>
          <RevenueMetricCard />
        </Suspense>
      </div>
    );
  }
  ```

---

## 4. Server Actions & Optimistic Mutations

- Form submissions and user mutations execute via typed **Server Actions**.
- Use React 19 `useActionState` and `useOptimistic` to achieve sub-16ms visual updates with guaranteed rollback protection upon network failure.
