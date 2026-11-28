# OpenClone Website Floorplan Engine (WFE) — Phase 0 Architecture Assessment & Baseline

**Feature ID:** WFE  
**Subsystem Name:** Website Floorplan Engine  
**Target Package:** `src/openclone/floorplan/`  
**Governing Domain:** `framework/domains/05-UX-UI-ENGINEERING/`  
**Date:** November 2026  
**Status:** PHASE 0 REVIEW / PENDING APPROVAL  

---

## 1. Executive Summary & Problem Statement

Modern AI coding agents generate web pages, routes, navigation menus, and components opportunistically and reactively. When prompted with application requirements, agents frequently jump straight to writing page code, inventing routes on the fly, creating duplicate navigation hierarchies, fracturing shared layouts, and producing disconnected or unreachable dead-end pages. This failure mode represents a primary manifestation of **AI Slope** in web engineering.

The **Website Floorplan Engine (WFE)** introduces an immutable, deterministic structural planning layer between product requirements analysis and UI wireframing/implementation.

### Core Operating Principle
> **Plan the structure before building the interface.**

WFE guarantees that:
- Every page exists for a documented business requirement.
- Navigation flows represent complete, bi-directional user journeys.
- Shared layouts and components are structurally planned before code is written.
- Multi-device responsive transformations (desktop $\leftrightarrow$ tablet $\leftrightarrow$ mobile) are defined structurally, not patched after the fact with ad-hoc CSS.
- The approved floorplan acts as a versioned, immutable contract consumed downstream by Information Architecture, Wireframing, UI/UX Design, Software Architecture, and Implementation.

---

## 2. Inventory & Audit of Existing OpenClone Capabilities

An inspection of the OpenClone repository (`MK-1603/OpenClone`, branch `feature/website-floorplan-engine`) reveals established capabilities that WFE must extend rather than duplicate:

| OpenClone Capability | Current Repository Implementation | WFE Reuse & Integration Point |
|---|---|---|
| **Domain 03: Requirements Engineering** (`framework/domains/03-REQUIREMENTS-ENGINEERING/`) | Defines functional requirements (`FR-*`), NFRs (`NFR-*`), and acceptance criteria via `E-012`, `E-014`, `E-015`. | Upstream input: WFE ingests approved functional requirements and extracts required user capabilities. |
| **Domain 05: UX/UI Engineering** (`framework/domains/05-UX-UI-ENGINEERING/`) | Houses Taste Skill v2.6.0, Anti-Slop Standards, Design Systems, and LEBIS. | Canonical home: WFE serves as the structural floorplan foundation of Domain 05. |
| **Information Architecture Engine** (`framework/engines/E-018-information-architecture.md`) | Defines content and navigation hierarchy contracts. | WFE implements the concrete structural engine that generates the page tree and navigation taxonomy specified in `E-018`. |
| **Interaction Flow Engine** (`framework/engines/E-019-interaction-flow-design.md`) | Governs interaction flows and user transitions. | WFE produces the user journey state transitions consumed by `E-019`. |
| **UI Design System Engine** (`framework/engines/E-020-ui-design-system.md`) | Defines component tokens and design systems. | WFE provides the component placement matrix mapping shared components across layouts. |
| **Planning Workflows** (`framework/workflows/WF-013`, `WF-015`) | `WF-013` governs existing project assessment and implementation planning; `WF-015` governs portable project specifications. | WFE integrates as Stage 4 (Website Structural Planning) in the unified engineering lifecycle. |
| **Specialist Workforce** (`framework/workforce/registry/workers/`) | Features 72 specialist roles, including `frontend-architect`, `ux-designer`, and `design-systems-engineer`. | Primary accountability assigned to `frontend-architect` (routes, layouts, components) and `ux-designer` (spatial composition, responsive flows). |
| **Schema Validation** (`framework/schemas/`) | 12 JSON Schema Draft 2020-12 files validated in CI. | Introduces `website-floorplan.schema.json` ensuring machine-readable contract compliance. |
| **MCP Server** (`src/openclone/mcp/server.py`) | Exposes 12 tools for status, knowledge, MIE model routing, and LEBIS brand engineering. | Exposes `openclone_generate_floorplan` and `openclone_validate_floorplan`. |
| **Audit Ledger** (`src/openclone/runtime/workforce.py`) | Hash-chained SQLite ledger (`workforce.sqlite3`). | Records floorplan approvals and revision digests for drift detection. |

---

## 3. Capability Gap Analysis: What is Genuinely Missing

While OpenClone possesses deep requirements elicitation (`E-012`) and visual UI token governance (Taste Skill, `E-020`), the repository currently lacks:

1. **No Structural Bridge Between `FR-*` and Route Code:** Requirements jump directly from specification to file implementation without an intermediate spatial and route blueprint.
2. **No Framework-Agnostic Route Hierarchy Model:** No data structure represents nested, dynamic, protected, and role-based routes independently of Next.js or React Router.
3. **No Page-by-Page Region Composition Model:** No structural specification identifies headers, main content areas, sidebars, modals, drawers, and state variants (empty, loading, error).
4. **No Component Placement Matrix:** No mechanism tracks which reusable components belong to which pages/layouts, leading to duplicate component creation.
5. **No Responsive Transformation Engine:** Responsive planning is currently deferred to CSS media queries rather than planned structural transformations (e.g. desktop sidebar $\to$ mobile bottom navigation drawer).
6. **No Dead-End Navigation Validator:** No automated check verifies that every page has a valid return path and that no dead-end or unreachable routes exist.
7. **No Versioned Floorplan Schema with Change Impact Analysis:** No mechanism calculates the downstream impact of removing a page or modifying a shared layout.

---

## 4. Architectural Ownership & Positioning

### Recommended Domain Placement
WFE logically belongs to **Domain 05 (`05-UX-UI-ENGINEERING`)** as its foundational structural planning pillar, bridging Domain 03 (`REQUIREMENTS-ENGINEERING`) with Domain 08 (`SOFTWARE-ARCHITECTURE`).

```
[ Domain 03: Requirements Engineering ]
  - Functional Requirements (FR-*)
  - User Personas & Permissions
  - Scope Ceilings & Non-Goals
                 │
                 ▼
[ WFE: Website Floorplan Engine (Domain 05) ]  <── THIS FEATURE
  - Page Hierarchy & Sitemaps
  - Route Structure (Protected, Dynamic, Nested)
  - Page-by-Page Layout Regions
  - Shared Layout Identification
  - Component Placement Matrix
  - Navigation & User Journey Flows
  - Multi-Device Responsive Transformations
  - Deterministic Structural Validation
                 │
                 ├───────────────────────────────┐
                 ▼                               ▼
[ Wireframe & UI/UX Design ]        [ Software Architecture (Domain 08) ]
  - Low-Fidelity Wireframes           - Framework Route Code & Middleware
  - Taste Skill Visual Styling        - Component Directory Organization
  - High-Fidelity UI Components       - State Management & API Client Boundaries
```

### Responsibility Boundaries
- **Requirements Analysis (`E-012`):** Defines *what* capabilities users need.
- **Website Floorplan (`WFE`):** Defines *how* pages, routes, layouts, and components are structured to satisfy those capabilities.
- **UI/UX Engineering (`Domain 05`):** Defines *how* the interface looks, feels, and interacts visually.
- **Software Architecture (`Domain 08`):** Defines *how* code, servers, APIs, and state containers are implemented technically.

---

## 5. Floorplan Data Model & Entity Schema

The floorplan is represented as a structured, versioned JSON document (`floorplan.json`) conforming to `website-floorplan.schema.json` (Draft 2020-12):

```
+---------------------------------------------------------------------------------+
|                               FLOORPLAN ROOT                                    |
|  - floorplan_id: str             - version: int         - status: FloorplanStatus|
|  - project_id: str               - created_at: str      - digest: str           |
+---------------------------------------------------------------------------------+
        │                 │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼                 ▼
   [ PAGES ]         [ ROUTES ]        [ LAYOUTS ]      [ COMPONENTS ]    [ NAVIGATION ]
   - page_id         - route_id        - layout_id      - component_id    - nav_id
   - name            - path            - name           - name            - label
   - category        - type            - shared_regions - category        - target_route
   - access_level    - auth_required   - pages_using    - pages_used_in   - user_roles
   - layout_ref      - dynamic_params  - responsive     - properties      - return_path
   - req_refs        - layout_ref      - dependencies   - dependencies    - children
        │                                                                       │
        └───────────────────────────────┬───────────────────────────────────────┘
                                        ▼
                            [ RESPONSIVE RULES ]
                            - device: DESKTOP | TABLET | MOBILE
                            - structural_transformations: List[Transform]
```

### Lifecycle States
`DRAFT` $\to$ `GENERATED` $\to$ `UNDER_REVIEW` $\to$ `APPROVED` $\to$ `SUPERSEDED` $\to$ `ARCHIVED`.

---

## 6. Deterministic Validation Engine (Zero AI Hallucination)

WFE rejects the practice of relying on LLM self-evaluation to verify structural consistency. The validation engine performs deterministic Python-based checks across 8 categories:

1. **Requirement Coverage Check:** Every `FR-*` must map to at least one page. Every page must link to at least one requirement. Unmapped requirements or unjustified pages raise errors.
2. **Route Integrity Check:** Validates route uniqueness, dynamic parameter syntax (`:id`), catch-alls, and parent-child route continuity.
3. **Navigation Dead-End Check:** Validates graph reachability from public entrypoints. Flags unreachable orphan pages and pages lacking a return path.
4. **Layout Reference Check:** Ensures every page references a valid layout and that shared layouts are assigned consistently.
5. **Component Dependency Check:** Verifies component hierarchy, detects circular component nesting, and flags orphan components without page assignments.
6. **Access & Role Consistency Check:** Validates that protected pages reside under authenticated routes and cannot be leaked through public navigation bars.
7. **Responsive Parity Check:** Ensures structural transformations are defined for Desktop ($>1024\text{px}$), Tablet ($768\text{px} - 1024\text{px}$), and Mobile ($<768\text{px}$).
8. **Anti-Slop Complexity Check:** Flags unnecessary page nesting ($>4$ levels deep) or excessive component fragmentation.

---

## 7. Artifact Strategy & Output Organization

Rather than scattering ten uncoordinated files across the repository, WFE consolidates deliverables into a clean, cohesive project artifact directory (`.openclone/floorplan/`):

1. **`floorplan.json`:** The authoritative machine-readable contract containing all entities, dependencies, and validation states.
2. **`FLOORPLAN.md`:** The compiled human-readable specification compiling all 10 primary views:
   - *View 1:* Website Sitemap
   - *View 2:* Page Hierarchy Diagram (`mermaid flowchart TD`)
   - *View 3:* Route Structure Table
   - *View 4:* Page-by-Page Layout Specifications
   - *View 5:* Shared Layout Specifications
   - *View 6:* Component Placement Matrix
   - *View 7:* Navigation & User Flow Diagram (`mermaid stateDiagram-v2`)
   - *View 8:* Multi-Device Responsive Layout Specifications
   - *View 9:* Requirement-to-Structure Traceability Matrix
   - *View 10:* Validation Report & Approval Summary
3. **`validation-report.json`:** Structured findings for CI/CD gating.

---

## 8. Proposed Module Organization

All WFE code will live cleanly inside `src/openclone/floorplan/` with zero external dependencies:

```
src/openclone/floorplan/
├── __init__.py           # Public API facade
├── models.py             # Dataclasses & enums (Page, Route, Layout, Component, etc.)
├── engine.py             # Central coordinator & lifecycle manager
├── planner.py            # Requirements interpretation & structural synthesis
├── navigation.py         # Navigation graph construction & dead-end detection
├── responsive.py         # Multi-device structural transformation rules
├── validator.py          # Deterministic 8-category validation engine
├── impact.py             # Change impact analysis & revision management
├── artifacts.py          # Markdown, Mermaid, and JSON artifact compilation
└── cli.py                # Command-line interface (`openclone floorplan ...`)
```

---

## 9. Phase-by-Phase Implementation Roadmap

- **Phase 0:** Repository Intelligence & Baseline Audit (This Document) $\leftarrow$ **CURRENT STOP POINT**
- **Phase 1:** Architecture Contracts, Schemas & Formal Specification (`website-floorplan.schema.json`, Domain 05 docs)
- **Phase 2:** Core Data Models, Serialization & Revision Infrastructure (`models.py`, `engine.py`)
- **Phase 3:** Structural Planning & Requirement Synthesis Engine (`planner.py`, `navigation.py`, `responsive.py`)
- **Phase 4:** Deterministic Structural Validation Engine (`validator.py`)
- **Phase 5:** Change Impact Analysis & Version Management (`impact.py`)
- **Phase 6:** Lifecycle Integration, MCP Tools & CLI Interface (`src/openclone/mcp/server.py`, `cli.py`)
- **Phase 7:** Comprehensive Verification Suite & Testing (`tests/test_floorplan.py`)

---

## 10. Risk Analysis & Mitigation

| Risk | Severity | Mitigation Strategy |
|---|---|---|
| **AI Slope / Hallucinated Pages** | Critical | Strict requirement traceability. Every page must link to an explicit `FR-*` from `PROJECT.md`. Unmapped pages fail validation. |
| **Framework Overfitting** | High | Abstract route and component models. WFE defines structural semantics, delegating Next.js/Vue/Svelte specifics to downstream adapters. |
| **Silent Mutation of Approved Plans** | Critical | SHA-256 digest binding. Approved floorplans are frozen; any edits create a reviewable draft revision requiring re-approval. |
| **Navigation Dead-Ends & Leaks** | High | Deterministic directed-graph traversal algorithm detects unreachable nodes and missing return paths. |
| **Repository File Clutter** | Medium | Consolidates all 10 required views into `.openclone/floorplan/FLOORPLAN.md` and `floorplan.json`. |

---

## 11. Decisions Requiring Human Approval

Before proceeding to Phase 1, the following architectural decisions are submitted to the human owner for explicit authorization:

1. **Domain Placement:** Ratification of Domain 05 (`05-UX-UI-ENGINEERING`) as the canonical governing domain for WFE.
2. **Artifact Strategy:** Authorization of `.openclone/floorplan/` housing `floorplan.json` (machine contract) and `FLOORPLAN.md` (consolidated human-readable view).
3. **Requirement Traceability Gate:** Enforcing that unmapped pages or requirements without structural coverage block approval.
4. **Approval to Proceed:** Formal authorization to begin Phase 1 (Contracts, Schemas & Domain Documentation).
