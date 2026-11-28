# Website Floorplan Engine (WFE)
## Mathematical Spatial Compilation & Responsive Route Topology Specification

**Domain:** `05-UX-UI-ENGINEERING`  
**Subsystem ID:** `WFE-01`  
**Framework Alignment:** AISDF Engine `E-018` (Information Architecture) & `E-020` (UI Design System)  
**Schema Definition:** [`framework/schemas/website-floorplan.schema.json`](../../schemas/website-floorplan.schema.json)  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Mission and Architectural Purpose

The **Website Floorplan Engine (WFE)** is OpenClone's deterministic spatial layout compiler. It bridges high-level user requirements (`PROJECT.md`) and user journey mapping (`E-017`) with concrete, production-ready frontend component scaffolding.

Traditional AI coding agents generate interfaces ad-hoc, resulting in arbitrary section heights, chaotic vertical rhythms, inconsistent content density, and broken mobile viewports. WFE eliminates this by treating page and application layout as an exact **spatial floorplan**:
1. **Mathematical Section Aspect Ratios:** Every section conforms to defined viewport ratio budgets (e.g. Hero = $1.0\times\text{viewport height}$ on desktop; Bento Feature Grid = $1.2\times\text{viewport height}$).
2. **Deterministic Grid Coordinates:** Assigns explicit CSS Grid / Flexbox spatial areas across an 8-point baseline grid.
3. **Density Calibrations:** Enforces strict content density tiers (High-Density Console, Balanced SaaS, Spacious Marketing).
4. **Responsive Route Topologies:** Generates viewport-specific adaptations from mobile (`390px`) to ultrawide (`1920px+`) before writing any JSX or CSS.

---

## 2. Floorplan Hierarchy & Zone Architecture

Every route compiled by WFE consists of standardized spatial zones:

```
+---------------------------------------------------------------------------------------------------------+
| ZONE 1: APPLICATION HEADER & NAVIGATION (Sticky / Glassmorphic Scrim, Height: 56px-64px)                 |
+---------------------------------------------------------------------------------------------------------+
| ZONE 2: PRIMARY VIEWPORT HERO / CONTEXT BANNER (Aspect Ratio: 16:9 or Full Viewport 100dvh)            |
+---------------------------------------------------------------------------------------------------------+
| ZONE 3: INTERACTIVE WORKSPACE / FEATURE BENTO (12-Column Responsive Grid, 24px Gutter)                 |
|   ┌───────────────────────────────────────────────┬─────────────────────────────────────────────────┐   |
|   │ PRIMARY PANE (Span 8)                         │ SECONDARY CONTEXT PANE (Span 4)                 │   |
|   │ • Data Table / Metric Visualizer              │ • Command Palette / Activity Feed / Action Deck │   |
|   └───────────────────────────────────────────────┴─────────────────────────────────────────────────┘   |
+---------------------------------------------------------------------------------------------------------+
| ZONE 4: AUXILIARY TILES & VALUE PROPOSITIONS (Bento Cards with 1px Specular Lighting)                   |
+---------------------------------------------------------------------------------------------------------+
| ZONE 5: PERSISTENT FOOTER & STATUS TELEMETRY (Metadata, Legal, System Health Pulse, Height: 48px-120px) |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Floorplan Compilation Algorithm

When compiling a route, WFE executes the following 5-step pipeline:

1. **Intake & Archetype Mapping:** Ingests route requirements and maps them to one of 8 product domain profiles (DevTools, Healthcare, Fintech, SaaS Dashboard, Consumer, Creative, E-Commerce, Data Platform).
2. **Zonal Partitioning:** Allocates vertical and horizontal screen real estate based on information priority.
3. **Aspect Ratio & Height Budgeting:** Computes maximum and minimum container bounds using CSS `min()`, `max()`, and `clamp()`.
4. **Component Family Binding:** Cross-references `framework/registries/COMPONENT-REGISTRY.md` to assign specific, vetted primitives (e.g. TanStack Table for data grids, CMDK for command bars).
5. **Contract Emission:** Emits machine-readable `floorplan.json` conforming to `website-floorplan.schema.json` and human-readable wireframe markdown.

---

## 4. Pre-Build Gate: WFE Validation

Before the frontend agent is authorized to write component source code, the compiled floorplan must clear the **WFE Pre-Build Gate**:
- [x] All primary user tasks have an assigned spatial coordinate.
- [x] Header and navigation do not exceed 64px vertical footprint.
- [x] 12-column grid collapses cleanly to 4 columns on mobile (`<768px`) and 1 column on small phones (`<480px`).
- [x] Zero elements depend on fixed pixel widths that exceed `320px`.
- [x] Every interactive zone has an assigned component family from the registry.
