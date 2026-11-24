---
id: ux-pro
name: UX Pro Skill
version: 1.0.0
category: ux
description: User research, product UX, information architecture, user journeys, interaction design, UX writing, and usability testing.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/ux-pro/SKILL.md
triggers:
  - ux
  - user experience
  - user research
  - user journey
  - task flow
  - usability
  - information architecture
  - wireframe
  - interaction design
  - ux writing
  - empty state
  - onboarding
  - persona
  - user flow
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
  - script-only
precedence: 8
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - User problem definition & target goals approved
  - Primary user journeys & task flows mapped
  - Information architecture & navigation hierarchy specified
  - Mandatory application states identified
finish_gates:
  - Usability walkthrough pass with zero high-friction blockers
  - Error recovery paths verified for all critical inputs
  - Contextual microcopy & validation feedback verified
verification:
  - Task-based usability inspection
  - State completeness audit (initial, loading, empty, error, recovery)
---

# UX Pro — Specialist Engineering Skill
**Version:** `1.0.0` | **Category:** `ux` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `ux-researcher`, `ux-designer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Ensure that digital applications solve concrete user problems through understandable, efficient, consistent, and resilient user experiences. UX Pro governs the structure, journeys, information architecture, interaction states, and feedback loops of the application before and during visual design and coding.

### Boundaries
- **In Scope:** User problem framing, goal definition, information architecture (IA), primary user journeys, critical task decision flows, interaction models (modals, drawers, tables, filters), microcopy and UX writing, application states specification, and usability testing.
- **Out of Scope:** Low-level CSS styling (governed by `taste-skill`), design tokens and theme implementation (governed by `design-system-engineering`), and low-level code implementation (governed by `frontend-engineering`).

---

## 2. REQUIRED EXPERTISE DOMAINS

### A. UX Research & Problem Discovery
1. **User Problem Definition:** Articulate the precise pain point, workflow bottleneck, or unmet need the feature addresses. Distinguish observed user facts from hypotheses and assumptions.
2. **User Personas & Context:** Ground personas in observable user workflows (e.g. Startup Founder, Incident Commander, Operations Analyst). Focus on real-world constraints: time scarcity, cognitive load, environment, and device usage.
3. **Jobs-to-be-Done (JTBD):** Define core jobs in the format: *"When [situation], I want to [action], so I can [expected outcome]."*

### B. Product UX & Value Delivery
1. **Product & User Goal Alignment:** Ensure every screen, view, and control directly advances user task completion without artificial obstacles or deceptive patterns.
2. **Friction Minimization:** Identify and eliminate unnecessary clicks, redundant data inputs, ambiguous options, and dead ends.
3. **Success Criteria:** Establish verifiable completion metrics (e.g., "Create project completed in < 3 steps without consulting documentation").

### C. Information Architecture (IA)
1. **Navigation Structure:** Establish clear, predictable navigation hierarchies (primary sidebar, breadcrumbs, contextual tabs, and global header utilities).
2. **Content Organization:** Group data and controls logically by mental model rather than database schema. Use progressive disclosure to keep views uncluttered while keeping advanced controls discoverable.
3. **Search & Filtering:** Provide predictable search, sorting, and multi-facet filtering with explicit active filter tags and clear-all actions.

### D. User Journey Engineering
1. **Primary Happy Path:** Map the optimal flow from entry to goal completion with minimal cognitive overhead.
2. **Alternative & Recovery Paths:** Explicitly map edge cases, validation errors, partial network failures, and cancellations. Ensure the user can always recover without losing entered state.
3. **First-Time vs. Returning User Experience:** Design meaningful zero-data empty states with actionable onboarding prompts for new users, and dense, efficient command views for returning power users.

### E. Interaction Design
1. **Component Behavioral Contracts:**
   - **Dialogs & Modals:** Used exclusively for focused, interruptive tasks or confirmations. Must trap focus, support Esc to close, and provide explicit Cancel/Confirm actions.
   - **Drawers & Sheets:** Used for contextual inspection, detail views, or mobile navigation. Support touch gestures and backdrop click to dismiss.
   - **Tables & Lists:** Support sorting, pagination/infinite scroll, row selection, bulk actions, and empty states.
   - **Notifications & Toasts:** Transient, non-blocking feedback for background actions. Must never obscure critical interactive buttons.
2. **Predictable Feedback:** Every user interaction must produce immediate visual feedback (e.g., button loading spinners, optimistic updates, toast confirmations).

### F. UX Writing & Microcopy
1. **Action-Oriented Labels:** Use clear verb-first labels (e.g., *"Create Project"*, *"Deploy Staging"*, *"Export CSV"*) instead of ambiguous single words (*"OK"*, *"Submit"*, *"Go"*).
2. **Contextual Form Guidance:** Place instructional placeholder text and helper hints adjacent to inputs. Provide inline validation errors explaining *why* the input failed and *how* to fix it.
3. **Empty States with Intent:** Empty states must never be blank screens. They must explain:
   - What belongs here.
   - Why it is currently empty.
   - The exact primary action to populate it (e.g., *"No tasks created yet. Create your first task to begin tracking."*).

### G. Usability Inspection & Testing
1. **Task-Based Walkthrough:** Verify that a user can complete core tasks without cognitive hesitation or disorientation.
2. **Friction Detection:** Flag multi-step wizards without progress indicators, ambiguous icons without text labels, and destructive actions without confirmation dialogs.

---

## 3. MANDATORY UX DELIVERABLES SPECIFICATION

For applicable tasks and features, the engineer must produce and document:

1. **User Problem Statement & Target Goals**
2. **Information Architecture & Navigation Blueprint**
3. **Primary User Journey & Task Decision Flowchart**
4. **Interaction Specification (Modals, Drawers, Tables, Filters)**
5. **Application States Coverage Matrix** (Initial, Loading, Empty, Error, Success, Recovery)
6. **Usability Acceptance Criteria**

---

## 4. APPLICATION STATES COVERAGE

Every view and component designed under `ux-pro` must explicitly account for these states:
- `INITIAL`: Clean initial state prior to user action.
- `LOADING`: Skeleton screens or scoped spinners (never blocking full-page spinners).
- `SUCCESS`: Verified completion state with clear next actions.
- `EMPTY`: Meaningful zero-data illustration/copy with primary creation CTA.
- `ERROR`: Actionable error message with a direct "Retry" or recovery action.
- `PARTIAL`: Handling of partially loaded or degraded data streams.
- `UNAUTHORIZED / FORBIDDEN`: Clear explanation and permission request workflow.

---

## 5. QUALITY GATES & VERIFICATION

### Pre-Build Gate
- Verify user problem statement and journey map before initiating frontend code.
- Ensure all 6 application states are specified for the target view.

### Finish Gate
- Conduct a task completion walkthrough.
- Verify zero dead ends, clear empty states, and inline error feedback.
