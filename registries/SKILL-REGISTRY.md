# OpenClone Skill Registry

This registry tracks the approved, verified skills integrated into OpenClone. Each skill must declare its identity, version, location, capabilities, and governance gates.

---

| Skill ID | Name | Version | Location | Primary Capabilities | Pre-Build Gate | Finish Gate | Maturity Status |
|---|---|---|---|---|---|---|---|
| `taste-skill` | Taste Skill | `v2.6.0` | [`skills/taste-skill`](file:///skills/taste-skill) | Anti-AI-slop governance, instruction discovery, adaptive design intelligence across 16 domains, brownfield project auditing, removal-first design, layout deal, real photographs, quiet motion | `plan-check.mjs` (`GATE: READY`) | `gate.mjs` (`GATE: PASS`) | `INTEGRATED` |

---

## Skill Details

### `taste-skill` (v2.6.0)
- **Engine Directory**: `skills/taste-skill`
- **Core Directive**: *Instruction First. Context First. Design First. Code Second.*
- **Key Modules**:
  - `scripts/instruction-audit.mjs`: Scans workspace for `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.
  - `scripts/audit-slop.mjs`: Scans code & CSS for AI slop patterns (glassmorphism, blobs, purple gradients, glow).
  - `scripts/plan-check.mjs`: Pre-build gate enforcing `.taste-skill/design-plan.md` before coding.
  - `scripts/gate.mjs`: Browser finish gate with headless Chrome validation across viewports.
- **Product Domains Supported**: SaaS, AI Apps, Developer Tools, Dashboards, Productivity, Finance, Ecommerce, Enterprise, Healthcare, Education, Portfolios, Marketing, Mobile, Admin Panels, Data-Heavy, Documentation.
