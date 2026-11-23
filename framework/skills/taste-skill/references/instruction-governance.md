# Instruction Governance & Precedence Specification

**Operating Rule:** Instruction First. Context First. Design First. Code Second.

An agent must never start generating code before discovering, inspecting, and reconciling all applicable instructions governing the target repository.

---

## 1. Instruction Discovery Scope

The discovery engine inspects the current project and traverses parent directories for:

1. **Repository & Agent Rules:**
   * `AGENTS.md`
   * `CLAUDE.md`
   * `GEMINI.md`
   * `.cursorrules`
   * `.cursor/rules/*.mdc` and `.cursor/rules/*.md`
   * `.github/copilot-instructions.md`
2. **Project & Package Documentation:**
   * `README.md`
   * `PROJECT.md`
   * `package.json` (`description`, dependencies, UI frameworks)
3. **Design System & Component Guidelines:**
   * `DESIGN.md`, `DESIGN-SYSTEM.md`, `STYLEGUIDE.md`
   * `docs/design/`, `docs/components/`, `docs/tokens/`
   * Existing CSS/Tailwind configuration (`tailwind.config.*`, CSS custom properties)
4. **Accessibility & Technical Guidelines:**
   * `a11y.md`, `ACCESSIBILITY.md`, `SECURITY.md`

---

## 2. Instruction Precedence Hierarchy

When rules conflict, resolve them in this strict order:

```text
[ HIGHEST PRECEDENCE ]
1. System / Safety Constraints & Sandboxing Rules
2. Explicit, Current Human Owner Prompt Instructions
3. Project-Specific Instruction Files (AGENTS.md, CLAUDE.md, .cursorrules)
4. Project Source of Truth (PROJECT.md, Design Tokens, Existing Brand Guidelines)
5. Existing Application Architecture & Framework Conventions
6. Taste Skill Defaults & Recommendations
[ LOWEST PRECEDENCE ]
```

### Conflict Resolution Protocols
* **Never Silently Override:** Do not overwrite explicit project design rules with Taste Skill defaults (e.g. if a project dictates dark mode and monospace, do not force light sans-serif palettes).
* **Document and Escalate:** When instructions conflict irreconcilably, record the conflict in `.taste-skill/reports/instruction-audit.md` and request clarification before coding.

---

## 3. Instruction Audit Report

For any task beyond Level 1 (Micro-Fix), generate:
`.taste-skill/reports/instruction-audit.md`

The report must record:
* Discovered instruction files and paths.
* Active rules and constraints identified.
* Identified conflicts and resolutions.
* Approval requirements.
