# Design-to-Code Pipeline Specification
## Deterministic Figma REST API Extraction, Auto-Layout Mapping & Token Translation

**Domain:** `05-UX-UI-ENGINEERING`  
**Specification ID:** `D2C-01`  
**Governing Standard:** OpenClone Design Intelligence & Experience Engineering (DIEE)  

---

## 1. Overview & Pipeline Flow

The **Design-to-Code Pipeline** translates visual design assets and Figma documents into production-grade React components and design tokens without manual copy-paste errors:

```
[ Figma File / URL ]
         │
         ▼
[ Figma REST API Extraction (GET /v1/files/:key) ]
         │
         ▼
[ Node Classification & Layout Parser ]
   ├── Frames -> Flexbox / Grid Containers
   ├── Text Nodes -> Typography Tokens & Text Components
   └── Vectors -> Optimized SVGs
         │
         ▼
[ Token Mapping Engine (W3C DTCG Format) ]
   ├── Colors -> OKLCH Semantic Tokens
   └── Spacing -> 8-Point Baseline Grid
         │
         ▼
[ Production Code Scaffold (JSX / Tailwind CSS / TypeScript) ]
```

---

## 2. Auto-Layout Translation Rules

1. `LAYOUT_MODE: "VERTICAL"` maps directly to `flex flex-col`.
2. `LAYOUT_MODE: "HORIZONTAL"` maps directly to `flex flex-row`.
3. `itemSpacing` maps to Tailwind `gap-{n}` snapped to the nearest 4px/8px token.
4. `primaryAxisAlignItems: "SPACE_BETWEEN"` maps to `justify-between`.
5. `counterAxisAlignItems: "CENTER"` maps to `items-center`.
6. Bounding frames with `clipsContent: true` map to `overflow-hidden`.
