---
id: ui-ux-engineering
name: UI/UX Engineering Skill
version: 2.0.0
category: design
description: Comprehensive digital product design, UX reasoning, anti-generic design systems, responsive composition, interaction engineering, and visual quality assurance.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/ui-ux-engineering/SKILL.md
triggers:
  - ui
  - ux
  - ui/ux
  - ui-ux
  - design
  - product design
  - user experience
  - user interface
  - visual design
  - design system
  - interaction design
  - information architecture
  - visual review
  - visual qa
  - anti-slop
  - dashboard design
  - landing page design
  - redesign
  - user journey
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
  - script-only
  - database-only
precedence: 9
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Product archetype and primary persona definition approved
  - Information architecture and core user journey mapped
  - Anti-generic design hypothesis and token scale defined
  - Visual density and layout composition strategy established
finish_gates:
  - Anti-generic checklist pass (no repeated AI templates or irrelevant widgets)
  - Responsive matrix verification (320px to 1440px+ without horizontal overflow)
  - 10-state component lifecycle audit (default, hover, focus, active, disabled, loading, empty, error, selected, success)
  - Visual QA scorecard evaluation >= 90.0%
verification:
  - Visual hierarchy and contrast audit
  - Multi-viewport layout inspection
  - Usability and task efficiency walkthrough
---

# UI/UX Engineering — Advanced Product Design & Frontend Craft Skill
**Version:** `2.0.0` | **Category:** `design` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Universal Product Design & Frontend Quality Standard  
**Workforce Alignment:** `ui-ux-designer`, `ux-researcher`, `frontend-developer`, `qa-engineer`

---

## 1. PURPOSE & ARCHITECTURAL OBJECTIVE

The **UI/UX Engineering Skill** transforms OpenClone into an intelligent digital product design and frontend craftsmanship engine. Instead of outputting generic, template-driven user interfaces with predictable AI cliches, this skill governs:
1. **Contextual Product Design:** Tailoring layout, hierarchy, and density to the specific product archetype (Financial Dashboard vs. Developer Tool vs. Enterprise SaaS).
2. **Anti-Generic Design Guardrails:** Actively eliminating boilerplate layout templates, meaningless KPI quartets, and arbitrary decorative glassmorphism.
3. **10-State Interaction Completeness:** Ensuring every component and screen handles default, hover, focus, active, disabled, loading, empty, error, selected, and success states.
4. **Responsive Composition:** Designing concurrently across viewports (mobile-first 320px to 4K ultra-wide 1440px+) with adaptive information restructuring rather than simple shrinking.
5. **Visual Quality Assurance (Visual QA):** Inspecting rendered interfaces using structured visual scoring across 10 deterministic dimensions.

---

## 2. THE 8 INTERNAL CAPABILITY MODULES

```
                       ┌─────────────────────────────────────────┐
                       │       UI/UX ENGINEERING SKILL           │
                       └────────────────────┬────────────────────┘
                                            │
   ┌───────────────────┬────────────────────┼───────────────────┬───────────────────┐
   │                   │                    │                   │                   │
┌──┴───────────────┐ ┌─┴────────────────┐ ┌─┴────────────────┐ ┌─┴────────────────┐ ┌┴─────────────────┐
│ A. Design        │ │ B. UX & Info     │ │ C. Visual Design │ │ D. Design System │ │ E. Interaction    │
│    Intelligence  │ │    Architecture  │ │    Engineering   │ │    Engineering   │ │    Engineering    │
└──┬───────────────┘ └─┬────────────────┘ └─┬────────────────┘ └─┬────────────────┘ └┬─────────────────┘
   │                   │                    │                   │                   │
   └───────────────────┴────────────────────┼───────────────────┴───────────────────┘
                                            │
                     ┌──────────────────────┼──────────────────────┐
                     │                      │                      │
             ┌───────┴──────────────┐ ┌─────┴──────────────┐ ┌─────┴──────────────┐
             │ F. Responsive        │ │ G. Frontend Design │ │ H. Visual Quality  │
             │    Composition       │ │    Implementation  │ │    Assurance (QA)  │
             └──────────────────────┘ └────────────────────┘ └────────────────────┘
```

### Module A: Design Intelligence
- **Product Context Comprehension:** Analyzes domain constraints, user operating velocity, and data criticality before proposing any layout.
- **Persona & Context Analysis:** Identifies core user archetypes (e.g., fast-paced Day Trader vs. Deliberative Security Auditor vs. Casual Consumer).
- **Workflow Intent Alignment:** Eliminates non-essential friction points and establishes clear visual priorities based on task frequency.

### Module B: UX Research & Information Architecture
- **Information Hierarchy:** Establishes predictable visual pathways. Primary actions and critical real-time data take precedence; secondary utilities reside under progressive disclosure.
- **Mental Model Alignment:** Groups data by human workflow rather than backend database tables.
- **Resilient State Architecture:** Enforces mandatory zero-state onboarding, informative error recovery paths, and transparent asynchronous feedback.

### Module C: Visual Design Engineering
- **Intentional Typography Scales:** Uses disciplined type hierarchies (Display, Title, Subtitle, Body, Caption, Monospace Data) with proportional line heights.
- **Harmonious Color Systems:** Establishes purposeful primary, neutral, semantic (success, warning, error, info), and surface ramps with strict WCAG 2.2 AA contrast compliance.
- **Layout Composition & Rhythm:** Leverages 4px/8px baseline grid systems, intentional whitespace, and balanced optical density.

### Module D: Design System Engineering
- **Semantic Token Architecture:** Organizes tokens into Global (base colors/sizes) -> Semantic (surface, text, border, interactive) -> Component tokens.
- **Accessible Theme Matrix:** Supports coherent Light and Dark themes without color inversion artifacts.
- **Component Primitives & Variant Contracts:** Specifies reusable component contracts with standardized variants (size: `sm | md | lg`, variant: `primary | secondary | outline | ghost | danger`).

### Module E: Interaction Engineering
- **Mandatory 10-State Coverage:** Every interactive element must define:
  1. `default`: Rest state.
  2. `hover`: Subtle cursor elevation or brightness change.
  3. `focus`: Visible, accessible outline (minimum 2px ring with distinct contrast).
  4. `active`: Tactical pressed feedback.
  5. `disabled`: Reduced opacity, muted text, disabled cursor (`cursor: not-allowed`).
  6. `loading`: Inline spinner or skeletal pulse; suppresses duplicate clicks.
  7. `empty`: Welcoming, helpful placeholder guiding next action.
  8. `error`: Clear inline validation message with error boundary styling.
  9. `selected`: Highlighting active filters, chosen rows, or toggled tabs.
  10. `success`: Clear affirmative micro-feedback (checkmarks, subtle green accent).
- **Purposeful Micro-interactions:** Animations must communicate cause-and-effect (e.g., expand/collapse, modal entry/exit) under 200ms without slowing user velocity.

### Module F: Responsive Composition
- **11-Tier Viewport Adaptability:** Full support from 320px (compact mobile), 375px, 414px, 640px, 768px, 1024px, 1280px, 1440px, 1920px, to 2560px+.
- **Structural Re-composition:** Complex desktop tables transform into responsive card lists on mobile; dense top-bar utility clusters collapse into bottom sheets or slide-over drawers.
- **Touch-Target Guarantee:** Interactive controls on touch viewports maintain a minimum 44x44px tappable area.

### Module G: Frontend Design Implementation
- **Tech Stack Alignment:** Respects project conventions (React, Next.js, TypeScript, Tailwind CSS, Radix UI, Lucide icons, or native CSS modules).
- **Clean Component Modularization:** Separates presentation tokens, state machines, and API integration. Zero monolithic multi-thousand-line JSX files.

### Module H: Visual Quality Assurance (Visual QA)
- **Rendered Output Inspection:** Validates the compiled interface using browser DOM evaluation or headless snapshots.
- **Defect Detection:** Flags horizontal overflow, text truncation, unstyled focus rings, misaligned baselines, and low-contrast labels.
- **Objective Scorecard:** Computes compliance against the 10-dimension Visual QA Scorecard.

---

## 3. ANTI-GENERIC DESIGN RULES (ZERO AI SLOP)

The skill explicitly rejects repetitive generative template patterns:

| Prohibited AI Slop Pattern | What to Do Instead (Governed Craft) |
| :--- | :--- |
| **Identical 4-Card KPI Row** on every dashboard | Choose visualizations suited to data nature (timeseries, heatmaps, live tabular stream, or activity feeds). |
| **Monotonous Sidebar Layout** across all products | Choose navigation by product type (Top bar with breadcrumbs for enterprise tools; collapsible command dock for creative apps; tab bars for mobile). |
| **Excessive Glassmorphism & Neon Glows** | Use solid surface tokens with crisp borders (1px) and optical elevation shadows. |
| **Meaningless AI Gradient Blobs** | Use intentional neutral surfaces with restrained functional brand accents (e.g. Gold `#D4AF37`, Slate `#1E293B`, Indigo `#4F46E5`). |
| **Empty "Hero Sections"** with buzzword copy | Put immediately actionable workflows and live data front-and-center. |
| **Unconstrained Whitespace** on dense workflows | Apply high-density tabular and compact spacing for data-intensive tools. |

---

## 4. 9-STEP DESIGN THINKING WORKFLOW

```
[1. UNDERSTAND] ──> [2. AUDIT] ──> [3. DEFINE] ──> [4. DESIGN] ──> [5. IMPLEMENT]
                                                                         │
                                                                         ▼
[9. REPORT]     <── [8. VALIDATE] <── [7. IMPROVE] <── [6. INSPECT] <────┘
```

1. **STEP 1 — Understand:** Identify product archetype, primary users, task frequency, and technical boundaries.
2. **STEP 2 — Audit:** Review existing styling, tokens, components, and usability bottlenecks.
3. **STEP 3 — Define:** Draft user journey maps, information architecture, and core interaction models.
4. **STEP 4 — Design:** Establish design tokens (typography, colors, spacing, radius) and component specs.
5. **STEP 5 — Implement:** Translate into clean, modular, accessible frontend code.
6. **STEP 6 — Inspect:** Render in browser/preview; verify DOM structure and layout integrity.
7. **STEP 7 — Improve:** Refine spacing, typography balance, contrast, and interactive feedback.
8. **STEP 8 — Validate:** Execute responsive matrix check, touch-target audit, and WCAG AA test.
9. **STEP 9 — Report:** Emit structured Visual Quality Scorecard and design ledger entry.

---

## 5. DESIGN REFERENCE INTELLIGENCE

The skill ingests user references without blind plagiarism:
- **Screenshots & Wireframes:** Analyzes spatial hierarchy, visual balance, and component arrangement.
- **Reference Websites & Figma Links:** Extracts typographic scale, color palette ratios, and navigation models.
- **Design Descriptions:** Translates aesthetic intent into concrete design tokens while preserving project identity.

---

## 6. PROJECT-SPECIFIC DESIGN MEMORY

Design decisions are stored in project-specific memory (`docs/design/DESIGN_SYSTEM.md` or `.openclone/design_memory.json`):
- Established color ramps and primary brand tokens.
- Approved typography font families and scale ratios.
- Component library conventions and variant names.
- Explicitly rejected patterns (e.g., "Do not use floating action buttons in this app").

---

## 7. VISUAL QA EVALUATION FRAMEWORK & SCORECARD

Evaluates rendered interfaces across 10 deterministic dimensions (0 to 10 points each; Total: 100):

| Dimension | Description | Pass Criteria (>= 8/10) |
| :--- | :--- | :--- |
| **1. UX Clarity** | Task understandability and cognitive load. | Zero ambiguous controls; clear user path. |
| **2. Info Architecture** | Logical structure and hierarchy. | Progressive disclosure; primary data prominent. |
| **3. Visual Hierarchy** | Optical weight and intentional scanning order. | Primary CTAs distinct from secondary utilities. |
| **4. Typography** | Readability, scale discipline, line heights. | Strict typographic scale; consistent tracking. |
| **5. Layout & Spacing** | 4px/8px grid alignment and density balance. | No irregular margins; proportional padding. |
| **6. Token Consistency** | Uniform color, radius, and elevation usage. | Zero hardcoded ad-hoc hex colors or pixel sizes. |
| **7. Responsiveness** | Adaptive composition across 320px–1440px+. | Zero horizontal overflow; touch targets >= 44px. |
| **8. Accessibility** | WCAG 2.2 AA contrast, ARIA, focus rings. | Text contrast >= 4.5:1; visible focus outlines. |
| **9. Interaction States** | 10-state coverage and micro-interactions. | Feedback provided for every state and loading call. |
| **10. Product Fit** | Suitability to specific product archetype. | Appropriate density and visual character. |

---

## 8. CLI & ASSISTANT INVOCATION

The skill is accessible through both the OpenClone CLI and natural language:

```bash
# Structured CLI Commands
oc design audit                   # Audits current interface against anti-slop rules
oc design create-system           # Generates semantic design token architecture
oc design dashboard <theme>       # Generates context-aware dashboard architecture
oc design visual-review           # Evaluates interface against 10-dimension scorecard
```

In the interactive terminal (`oc>`) or VS Code chat:
- `"/design audit"` or `"Audit my dashboard UX"`
- `"/design create-system"` or `"Create a design system for fintech trading"`
- `"/design responsive"` or `"Make this data table responsive for mobile"`
- `"/design visual-review"` or `"Run visual QA on the profile settings page"`
