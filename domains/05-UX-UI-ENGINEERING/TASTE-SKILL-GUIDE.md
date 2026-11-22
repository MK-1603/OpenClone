# Taste Skill Integration & Execution Guide
## Anti-AI-Slop Governance & Adaptive Design Intelligence in OpenClone

Taste Skill v2.6.0 is OpenClone's canonical design engineering system. It prevents coding agents from immediately generating raw HTML/CSS without instruction discovery, brownfield inspection, visual slop analysis, and pre-build plan validation.

---

## 1. The Mandatory 5-Phase Lifecycle

Any agent or contributor designing or updating user interfaces MUST progress sequentially through these 5 phases:

```
[Phase 1: Discover & Audit]
  ├── node skills/taste-skill/scripts/instruction-audit.mjs
  └── node skills/taste-skill/scripts/audit-slop.mjs <target-dir>
          ↓
[Phase 2: Context & Adaptive Domain Selection]
  ├── Select from 16 Product Profiles (references/adaptive-design-intelligence.md)
  └── Apply Removal-First Taxonomy (PRESERVE, MODIFY, REMOVE, ADD)
          ↓
[Phase 3: Plan & Pre-Build Gate]
  ├── Create .taste-skill/design-plan.md (Level 1–5 scaled)
  └── node skills/taste-skill/scripts/plan-check.mjs
      Must output: `GATE: READY`
          ↓
[Phase 4: Governed Implementation]
  ├── Apply Design System Tokens (references/design-system-governance.md)
  └── Use Real UI Fragments, Real Photographs & Authentic SVG Marks
          ↓
[Phase 5: Real-Browser Verification & Finish Gate]
  ├── node skills/taste-skill/scripts/consistency.mjs <url>
  └── node skills/taste-skill/scripts/gate.mjs <url>
      Must output: `GATE: PASS`
```

---

## 2. CLI Tooling Reference

All Taste Skill scripts are pure Node.js 22 ESM (`.mjs`) built-ins requiring zero external npm runtime packages.

### 2.1 Instruction Discovery
```bash
node skills/taste-skill/scripts/instruction-audit.mjs [workspace-path]
```
- Discovers `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.cursor/rules/`, `.github/copilot-instructions.md`, component docs, and design tokens.
- Audits local and parent-directory inherited instructions.
- Enforces precedence: User Prompt > AGENTS.md > Project Design Tokens > Taste Skill Defaults.
- Writes detailed findings to `.taste-skill/reports/instruction-audit.md`.

### 2.2 Static Anti-AI-Slop Scanner
```bash
node skills/taste-skill/scripts/audit-slop.mjs [path-to-files]
```
- Scans `.html`, `.css`, `.jsx`, `.tsx`, `.vue`, `.svelte` files for cliché AI slop:
  - Excessive, unprompted glassmorphism (`backdrop-filter: blur()`).
  - Ambient background blur blobs (`filter: blur(80px)`).
  - Generic purple/indigo gradients (`from-purple-600 to-indigo-600`).
  - Neon glow box-shadows (`box-shadow: 0 0 20px #8b5cf6`).
  - Repetitive rounded cards and decorative badges.
- Classifies each pattern as: `REQUIRED`, `JUSTIFIED`, `OPTIONAL`, `UNNECESSARY`, or `PROHIBITED`.
- Outputs severity (`Critical`, `High`, `Medium`, `Low`), code snippet, and action (`REMOVE`, `REDUCE`, `KEEP`).

### 2.3 Pre-Build Gate & Plan Validator
```bash
node skills/taste-skill/scripts/plan-check.mjs [.taste-skill/design-plan.md]
```
- Deterministically validates that `.taste-skill/design-plan.md` has been authored and satisfies requirements for the specified task scale:
  - **Task Level 1–2 (Micro-fixes / Component updates)**: Lightweight 5-section plan.
  - **Task Level 3–5 (New pages / Redesigns / Full apps)**: Full 25-point comprehensive design plan.
- Emits:
  - `GATE: READY` — Proceed to code synthesis.
  - `GATE: PLAN_REQUIRED` — No plan found; coding blocked.
  - `GATE: PLAN_INVALID` — Plan missing required sections; lists exact missing points.

### 2.4 Browser Consistency & Finish Gate
```bash
node skills/taste-skill/scripts/consistency.mjs index.html --page software
node skills/taste-skill/scripts/gate.mjs index.html
```
- Renders the built interface in real headless Chrome over HTTP at `1440` (desktop), `1024` (tablet landscape), `768` (tablet portrait), and `390` (mobile phone).
- Checks contrast (WCAG 2.2 AA), tap target sizes (44px min), layout overflows, text collisions, font loading, and reduced motion compliance.
- Emits `GATE: PASS`, `GATE: FAIL`, `GATE: OPEN`, or `GATE: SETUP`.

---

## 3. Integrating with OpenClone Workflows

When implementing tasks assigned to the UX/UI team:
1. Work is orchestrated under `05-UX-UI-ENGINEERING`.
2. The agent executes `instruction-audit.mjs` and `plan-check.mjs`.
3. In human-approval workflows (`WF-004` and `WF-013`), the output of `plan-check.mjs` is bound to the task digest via `aisdf.py plan`.
4. Independent reviewers in EGM (`WF-009`) verify that no code was introduced without clearing the pre-build gate.
