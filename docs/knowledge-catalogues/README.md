# OpenClone Engineering Knowledge Catalogues & Taxonomy
**Version:** 1.0.0  
**Scope:** Canonical software engineering knowledge taxonomies, design systems, and product capability mapping.

---

## 1. Catalogues Index

| Document | Topic Scope | Contents & Taxonomy |
|---|---|---|
| **[UI_DESIGN_CATALOGUE.md](UI_DESIGN_CATALOGUE.md)** | UI & Visual Design | 86 visual styles, 232 architecture taxonomy entries across 8 layers, component tokens. |
| **[ANIMATION_MOTION_CATALOGUE.md](ANIMATION_MOTION_CATALOGUE.md)** | Motion & Animation | 365 motion concepts, duration tokens (50ms–500ms), cubic-bezier easing, 60fps GPU compositor rules. |
| **[BACKEND_SYSTEM_DESIGN_CATALOGUE.md](BACKEND_SYSTEM_DESIGN_CATALOGUE.md)** | Backend & System Design | 580 backend topics across 23 core engineering domains. |
| **[AI_ENGINEERING_CATALOGUE.md](AI_ENGINEERING_CATALOGUE.md)** | AI & LLM Engineering | 1,095 topics across 18 domains (routing, prompt engineering, RAG, agents, security). |
| **[CATALOGUE_TO_PRODUCT_CAPABILITY_MAP.md](CATALOGUE_TO_PRODUCT_CAPABILITY_MAP.md)** | Product Capability Mapping | Explicit classification of catalogue concepts into core, internal, optional, or reference knowledge. |

---

## 2. Product Classification Model

Every concept across the catalogues is assigned an explicit product role:
- `CORE_PRODUCT`: Direct user-facing workbench capability.
- `INTERNAL_ENGINEERING`: Implemented inside OpenClone's governance and execution runtime.
- `OPTIONAL_INTEGRATION`: Available via user-enabled tool or plugin.
- `REFERENCE_KNOWLEDGE`: Architectural design pattern used for planning and guidance.
- `FUTURE_RESEARCH`: Advanced topic under evaluation.
- `OUT_OF_SCOPE`: Deliberately excluded to prevent feature bloat.
