# 05 — UX/UI Engineering & Human-Crafted Design Systems

## Mission & Philosophy
OpenClone enforces a strict standard for visual and interaction design: **Human-Crafted Craftsmanship over Generic AI Slop.**

When AI coding agents generate interfaces without design constraints, they routinely converge on cliché aesthetics: unprompted purple/indigo gradients, floating ambient background blur blobs, excessive translucent glass panels without contrast, meaningless statistic counters, and identical rounded cards. 

OpenClone bridges this gap by embedding **Taste Skill v2.6.0** (`skills/taste-skill/`) directly into the framework. Every user interface engineered under OpenClone follows the core operating principle:

> **Instruction First. Context First. Design First. Code Second.**

---

## Architectural Pillars

```
+---------------------------------------------------------------------------------------------------------+
|                                    05 — UX/UI ENGINEERING SYSTEM                                        |
+---------------------------------------------------------------------------------------------------------+
| 1. Discovery & Audit        | • Project-Level Instruction Discovery (AGENTS.md, .cursorrules)           |
|                             | • Brownfield Project Token & Dependency Inspection                        |
|                             | • Anti-AI-Slop Code & CSS Pattern Scanner (`scripts/audit-slop.mjs`)       |
+-----------------------------+---------------------------------------------------------------------------+
| 2. Design Strategy          | • 16 Adaptive Product Domain Profiles (DevTools, Healthcare, SaaS, etc.)  |
|                             | • Removal-First Strategy (PRESERVE, MODIFY, REMOVE, ADD)                   |
|                             | • User-Selected Styles (Glassmorphism, Neumorphism, Brutalism, Swiss)      |
+-----------------------------+---------------------------------------------------------------------------+
| 3. Pre-Build Gate           | • Task Scaling (Level 1 Micro-Fix to Level 5 Greenfield App)              |
|                             | • 25-Point Design Plan (`.taste-skill/design-plan.md`)                    |
|                             | • Deterministic Gate Check (`scripts/plan-check.mjs` -> GATE: READY)      |
+-----------------------------+---------------------------------------------------------------------------+
| 4. Implementation           | • 8-Point Spatial Grid, Major Third Typography Scale                      |
|                             | • Semantic 5-Tier Surface Hierarchy (Base, S1, S2, Elevated, Overlay)     |
|                             | • Real Photographs & Genuine Brand SVGs (No Fake Mocks)                  |
+-----------------------------+---------------------------------------------------------------------------+
| 5. Verification & Finish    | • Headless Chrome CDP Verification at 1440, 1024, 768, 390                |
|                             | • WCAG 2.2 AA Contrast & Touch Target Gating (44px min)                   |
|                             | • Real-Browser Finish Gate (`scripts/gate.mjs` -> GATE: PASS)             |
+-----------------------------+---------------------------------------------------------------------------+
```

---

## Navigation & Core Guides

1. [`TASTE-SKILL-GUIDE.md`](file:///TASTE-SKILL-GUIDE.md) — Step-by-step developer and agent guide to executing Taste Skill commands, pre-build gates, and browser verification inside OpenClone.
2. [`USER-CHOICE-DESIGN-PATTERNS.md`](file:///USER-CHOICE-DESIGN-PATTERNS.md) — Comprehensive technical reference for user-chosen styles (Glassmorphism, Neumorphism/UI Morphism, Swiss Minimalism, Brutalism). Details how Taste Skill evaluates them (REQUIRED/JUSTIFIED vs UNNECESSARY) and exact CSS token implementations.
3. [`ANTI-AI-SLOP-STANDARDS.md`](file:///ANTI-AI-SLOP-STANDARDS.md) — The OpenClone Anti-AI-Slop Manifesto. Detailed comparative breakdown of generic AI tropes vs human-crafted UI engineering.
4. [`HUMAN-CRAFTED-DESIGN-SYSTEM.md`](HUMAN-CRAFTED-DESIGN-SYSTEM.md) — Canonical design tokens, typography scales, elevation systems, surface hierarchies, and micro-interaction timing curves.
5. [`LOGO-ENGINEERING-AND-BRAND-IDENTITY.md`](LOGO-ENGINEERING-AND-BRAND-IDENTITY.md) — Complete specification of the Logo Engineering & Brand Identity System (LEBIS), the 10 specialized engines, vector SVG generation, and automated QA gating.

---

## Workforce Roles & Engines

- **Specialist Roles** (`workforce/teams/UX-DESIGN/roles/`):
  - [`UI-DESIGNER.md`](file:///../workforce/teams/UX-DESIGN/roles/UI-DESIGNER.md): Visual systems, interface states, responsive layouts, and token implementations.
  - [`UX-DESIGNER.md`](file:///../workforce/teams/UX-DESIGN/roles/UX-DESIGNER.md): Mental models, user task flows, cognitive load minimization, and wireframe prototypes.
  - [`DESIGN-SYSTEMS-ENGINEER.md`](file:///../workforce/teams/UX-DESIGN/roles/DESIGN-SYSTEMS-ENGINEER.md): Token architectures, component contracts, CSS architecture, and accessibility conformance.
  - [`ACCESSIBILITY-SPECIALIST.md`](file:///../workforce/teams/UX-DESIGN/roles/ACCESSIBILITY-SPECIALIST.md): WCAG 2.2 AA validation, screen reader tree, keyboard focus traps, and contrast audits.
  - [`UX-RESEARCHER.md`](file:///../workforce/teams/UX-DESIGN/roles/UX-RESEARCHER.md): User interviews, usability heuristics, cognitive walkthroughs, and task completion metrics.

- **Capability Engines** (`engines/`):
  - `E-017`: UX Research & Journey Mapping
  - `E-018`: Information Architecture & Navigation
  - `E-019`: Interaction Flow Design
  - `E-020`: UI Design-System & Token Infrastructure
  - `E-021`: Accessibility & Inclusive Design Compliance
