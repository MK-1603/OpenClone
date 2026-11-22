# OpenClone Global Knowledge Catalogues & Standards

This directory consolidates canonical engineering knowledge, architectural taxonomies, visual styling standards, and audit protocols used across the OpenClone framework.

---

## Knowledge Index

| Document | Scope | Contents & Taxonomy |
|---|---|---|
| **[UI/UX Design Catalogue](ui-ux-design-catalogue.md)** | Visual Styling & UI Taxonomy | 86 visual styles, 232 architecture taxonomy entries across 8 layers, component tokens, and CSS variables. |
| **[UI/UX Quality Audit Protocol](ui-ux-quality-audit.md)** | Quality Evaluation & Execution | 11-dimension 100-point weighted quality audit, 6-stage premium design protocol, and anti-slop enforcement. |
| **[Motion & Animation Standards](motion-and-animation.md)** | Animation & Micro-Interactions | Duration tokens (50ms–500ms), physics-based cubic-bezier easing curves, 60fps GPU compositor rules, and WCAG reduced-motion contracts. |
| **[Backend & System Design Catalogue](backend-system-design-catalogue.md)** | Production Backend Architecture | 580 topics across 23 core engineering domains (API protocols, databases, queuing, caching, observability, resilience). |
| **[AI Engineering & Context Catalogue](ai-engineering-catalogue.md)** | Model & Context Management | 1,095 topics across 18 domains (LLM routing, token optimization, prompt engineering, RAG, tool calling, model evaluation). |

---

## Integration with MCP Guidance

All catalogues are queryable at runtime through the OpenClone MCP Server via the `get_guidance` tool:

```json
{
  "topic": "ui_ux_catalogue"
}
```

Supported topics: `saas_security`, `ui_ux_catalogue`, `ui_ux_quality`, `motion_design`, `backend_catalogue`, `ai_catalogue`, `external_repos`, `skills`.
