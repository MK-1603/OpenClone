# Agency Agents Ecosystem Integration Specification
**Subsystem:** OpenClone External Specialist Workforce Engine  
**Authority:** OpenClone Architecture & Integration Core  
**Upstream Repository:** `https://github.com/msitarzewski/agency-agents`  
**License:** MIT (Copyright (c) Michael Sitarzewski)  
**Status:** `VERIFIED` | **Maturity:** `L3_VERIFIED`  
**Version:** 1.0.0  

---

## 1. Executive Summary & Integration Purpose

OpenClone integrates the **Agency Agents** open-source ecosystem as a first-class **External Specialist Workforce**. The integration provides access to specialized AI personas across 14 industry divisions while strictly preserving their original identity, tone, personality, mission, critical rules, workflow methodologies, and deliverable standards.

OpenClone provides the deterministic engineering environment:
* **Separation of Concerns:** External Agency Agents supply domain expertise and specialized workflows; OpenClone provides deterministic governance, model intelligence routing, permission enforcement, dependency DAG sequencing, and audit logging.
* **Non-Dilution Principle:** External agent definitions are never compressed into generic system prompts or stripped of domain constraints.
* **Catalog Distinctness:** Native OpenClone workers (72 fixed core engineering roles) and external Agency Agents are explicitly distinguished to prevent registry pollution.

---

## 2. Upstream Repository Audit & Provenance

* **Repository:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
* **Author / Creator:** Michael Sitarzewski
* **Upstream License:** MIT License (Permissive open source)
* **Integration Manifest:** `framework/workforce/external/agency-agents/WORKFORCE-001.manifest.json`
* **Local Catalog Storage:** `framework/workforce/external/agency-agents/`
* **Division Configuration:** `framework/workforce/external/agency-agents/divisions.json`

---

## 3. Discovered Professional Divisions

The integration indexes the 14 official divisions defined by the Agency Agents schema:

| Division Slug | Label | Lucide Icon | Brand Color | Specialization Focus |
|---|---|---|---|---|
| `engineering` | Engineering | `Code` | `#3B82F6` | Distributed architecture, API contracts, backend logic, frontend UI, DevOps. |
| `design` | Design | `Palette` | `#EC4899` | Design systems, WCAG 2.2 AA accessibility, visual storytelling, finish-gate QA. |
| `product` | Product | `Compass` | `#F59E0B` | Opportunity discovery, feature specification architecture, trend research. |
| `project-management` | Project Management | `Kanban` | `#8B5CF6` | Milestone stewardship, timeline tracking, agile sprint coordination. |
| `testing` | Testing | `CheckSquare` | `#14B8A6` | Reality checking, edge-case discovery, deterministic evidence collection. |
| `marketing` | Marketing | `Megaphone` | `#10B981` | Growth loops, content creation, SEO strategy, audience engagement. |
| `sales` | Sales | `TrendingUp` | `#EF4444` | Discovery interviews, solution qualification, enterprise deal structuring. |
| `paid-media` | Paid Media | `Target` | `#F97316` | Performance marketing, conversion tracking, PPC campaign optimization. |
| `support` | Support | `Headphones` | `#06B6D4` | User analytics, customer success workflows, ticket resolution telemetry. |
| `finance` | Finance | `DollarSign` | `#22C55E` | Financial modeling, unit economics (CAC/LTV), cloud infrastructure budgets. |
| `spatial-computing` | Spatial Computing | `Glasses` | `#6366F1` | XR interface architecture, visionOS engineering, spatial interaction physics. |
| `game-development` | Game Development | `Gamepad2` | `#A855F7` | Multi-engine gameplay loops (Unity, Unreal, Godot), procedural level design. |
| `academic` | Academic & Research | `GraduationCap` | `#D97706` | Literature synthesis, cognitive psychology models, empirical research. |
| `specialized` | Specialized Roles | `Sparkles` | `#64748B` | Cross-functional agents, MCP tool building, multi-agent meta orchestration. |

---

## 4. Agent Anatomy & Identity Preservation

Every agent profile parsed by OpenClone preserves the original 7 core dimensions without abbreviation:

1. **YAML Metadata:** `name`, `description`, `color`, `emoji`, `vibe`, `division`, `upstream_repo`, `license`.
2. **Identity & Memory:** Professional background, historical pattern recognition, mental models, and perspective.
3. **Core Mission:** Definitive statements of goals and target outcomes.
4. **Expertise & Competencies:** Specific technical capabilities, protocols, and domain strengths.
5. **Critical Rules & Boundaries:** Non-negotiable architectural and domain constraints.
6. **Workflow Process:** Numbered, sequential problem-solving methodologies.
7. **Expected Deliverables:** Concrete templates, schemas, and verification criteria.

---

## 5. Execution Model & Model Intelligence Engine (MIE) Binding

An external agent is executed through an **`ExecutionContract`** that binds it to OpenClone's local control plane:

```
[Agency Agent Definition]
         +
[OpenClone Project Context (PROJECT.md)]
         +
[Task Prompt & Requirements]
         v
[AgencyExecutionAdapter]
         |
         +--> Task Category Classification
         +--> Model Intelligence Engine (MIE) Routing
         |      - Architecture / Security -> GPT-6.2 Astra (Reasoning)
         |      - Visual / UI -> GPT-6.1 Terra / GPT-6.2 Sol
         |      - General Tasks -> GPT-6.2 Sol / Claude 3.7 Sonnet
         |      - Scaffolding -> GPT-6 Luna
         +--> Least-Privilege Action Boundaries
         +--> Sensitive Action Approval Gates (write, execute, deploy)
         v
[Deterministic Execution DAG via topo()]
```

---

## 6. UX Pro Specialist Integration

OpenClone's central UI/UX quality engine (**UX Pro**) directly incorporates 8 dedicated Agency Agents specialists:
* **UI Designer:** Semantic design tokens, component architecture, responsive breakpoints.
* **UX Researcher:** User mental models, heuristic evaluation, friction analysis.
* **UX Architect:** Task journey mapping, navigation hierarchy, information architecture.
* **Brand Guardian:** Logo geometry, color harmony, typography guidelines, brand voice.
* **Visual Storyteller:** Narrative hero composition, conceptual illustration layout.
* **UI Finish-Gate Reviewer:** Visual QA scorecard, contrast verification, zero-slop audit.
* **Whimsy Injector:** Restrained micro-interactions, delight moments, completion animations.
* **Inclusive Visuals Specialist:** Universal iconography, cultural color semantics, global accessibility.

### Recommended 5-Stage UI/UX Team Workflow:
1. **UX Researcher:** Synthesizes user needs and cognitive friction points.
2. **UX Architect:** Establishes user flows and wireframe blocks.
3. **UI Designer:** Engineers design tokens, component variants, and typography scales.
4. **Frontend Developer:** Implements accessible production components and 14 states.
5. **UI Finish-Gate Reviewer:** Inspects rendered layouts, checks contrast (4.5:1), and issues final sign-off.

---

## 7. Security & Governance Policy

* **Least Privilege:** Agency Agents are initialized with read/observe permissions (`observe`, `plan`, `design`).
* **Human Approval Gates:** Actions in `SENSITIVE_ACTIONS` (`write`, `execute`, `external_access`, `destructive_change`, `deploy`, `security_test`) strictly require human cryptographic approval recorded in OpenClone's hash-chained ledger.
* **Untrusted Code Execution:** Agents operate in standard sandboxes without direct unsanctioned host or network access.
* **Secret Redaction:** OpenClone's automated redaction engine filters API keys, private tokens, and passwords from prompts, agent thoughts, and logs.

---

## 8. CLI & MCP Tool Interface

### CLI Commands:
```bash
# List all discovered divisions
openclone agency divisions

# Search specialist agents across divisions
openclone agency list --division design
openclone agency list --query "architect"

# Show complete unredacted agent profile
openclone agency show ui-designer

# Assemble specialist teams
openclone agency team --type ui_ux --name "E-Commerce App"
openclone agency team --type website --name "SaaS Marketing"

# Check upstream catalog synchronization
openclone agency sync
```

### Model Context Protocol (MCP) Tools:
* `openclone_workforce_status`: High-level metrics for native and external agents.
* `openclone_discover_agents`: Search and filter catalog by query, division, or capability.
* `openclone_get_agent_profile`: Retrieve full personality, rules, workflow, and deliverables.
* `openclone_assemble_team`: Assemble multi-agent specialist teams with execution order.
