# OpenClone Project-Type Checklist Packs
**Version:** 1.0.0  
**Scope:** Conditional checklist extensions activated based on project classification.

---

## 1. Project Packs Matrix

| Pack Identifier | Target Architecture | Activation Triggers | Specialized Engineering Checks |
|---|---|---|---|
| **`WEB_SAAS`** | Multi-tenant SaaS | `project_type == WEB_SAAS` or multi-user web product | Tenant RLS isolation, subscription billing webhook idempotency, cross-tenant leak tests. |
| **`STATIC_WEBSITE`** | Jamstack / Marketing | `project_type == STATIC_WEBSITE` | Core Web Vitals (LCP < 2.5s), canonical meta tags, zero horizontal overflow on mobile. |
| **`MOBILE_APP`** | iOS & Android | `project_type == MOBILE_APP` (React Native/Flutter/Native)| App lifecycle, offline local storage, universal deep links, touch target minimums (44px). |
| **`API_PLATFORM`** | Developer API | `project_type == API_PLATFORM` | OpenAPI 3.1 specification, tiered rate limiting, API key rotation, idempotency headers. |
| **`ECOMMERCE`** | Commerce & Payments | `project_type == ECOMMERCE` or payment cart | Atomic inventory reservation under concurrency, cart state machine, payment reconciliation. |
| **`AI_AGENT_PLATFORM`** | Generative AI / Agents | `project_type == AI_AGENT_PLATFORM` or features include AI | Prompt versioning, indirect injection defense, tool sandboxing, token budgeting, RAG evals. |
| **`REALTIME_COLLABORATIVE`**| WebSockets / Streaming | `project_type == REALTIME_COLLABORATIVE` | Heartbeats, automatic reconnection, presence state expiry, concurrent edit conflict resolution. |
| **`DATA_ANALYTICS`** | Data Engineering | `project_type == DATA_ANALYTICS` | Idempotent ingestion pipelines, data schema validation, dead-letter queues, transformation tests. |
| **`DESKTOP_APP`** | Electron / Tauri | `project_type == DESKTOP_APP` | Code signing (macOS/Windows/Linux), secure auto-update verification, local filesystem sandboxing. |
| **`LIBRARY_SDK`** | Open Source Package | `project_type == LIBRARY_SDK` | Exported type stubs, semantic versioning enforcement, backward-compatibility regression tests. |

---

## 2. Extension Architecture

New project packs can be registered in `src/openclone/lifecycle/catalogue.py` under `PROJECT_TYPE_PACKS` without modifying the core state machine or verification engine.
