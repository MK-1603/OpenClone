# OpenClone — PROJECT.md-Only Project Intelligence & IDE Build Workflow
**Portable specification-to-build system | Master prompt for ChatGPT, Claude, and AI coding IDEs**
**Version 2.0.0**

---

# 1. Product direction — important correction

OpenClone must support a workflow that starts with **only a `PROJECT.md` file**.

The user does NOT need to:
- clone the OpenClone repository;
- install OpenClone locally;
- add OpenClone as a dependency to the target project;
- copy the OpenClone source tree into the project;
- run an OpenClone backend or dashboard;
- install every OpenClone skill or security tool before planning.

Instead:

1. The user gives `PROJECT.md` to ChatGPT or Claude.
2. ChatGPT/Claude analyzes and improves the specification.
3. The AI produces a complete, portable project instruction package and a master build prompt.
4. The user opens their own project folder in Antigravity, Claude Code, Codex, Qwen Code, Kiro, Kilo Code, Cursor, or another IDE.
5. The user provides the generated files and build prompt to that IDE agent.
6. The IDE agent inspects the actual target project and builds it phase by phase.
7. The agent runs relevant tests and security checks, optionally using Strix and other tools through their official documented installation or API routes.
8. The agent verifies the requirements and produces a completion report.

OpenClone is the **methodology, reusable standards, and prompt-generation workflow**. The generated project package is portable. The target IDE agent is the implementation executor.

Do not make generated projects depend on the OpenClone repository being present.

---

# 2. The product experience

```text
                  USER
                   |
                   v
          Existing PROJECT.md
                   |
                   v
          CHATGPT / CLAUDE
                   |
          +--------+---------+
          |                  |
          v                  v
    Analyze & Improve   Identify Gaps
          |                  |
          +--------+---------+
                   |
                   v
          PROJECT SPEC PACKAGE
          1. PROJECT.md
          2. BUILD_PROMPT.md
          3. AGENT_INSTRUCTIONS.md
          4. IMPLEMENTATION_PLAN.md
          5. SECURITY_PLAN.md
          6. ACCEPTANCE_MATRIX.md
                   |
                   v
            USER OPENS IDE
                   |
       +-----------+------------+
       |           |            |
       v           v            v
  Antigravity  Claude Code   Codex / Qwen
       |           |            |
       +-----------+------------+
                   |
                   v
          TARGET PROJECT REPO
                   |
                   v
         INSPECT → PLAN → BUILD
                   |
                   v
       TEST → SECURITY → REVIEW
                   |
                   v
        FIX → RETEST → VERIFY
                   |
                   v
         COMPLETE PROJECT REPORT
```

The project package must be usable with any verified coding agent. IDE-specific files are generated only when needed.

---

# 3. Input and output contract

## Input

Required:
- `PROJECT.md` (existing specification or rough project brief).

Optional:
- existing target repository files or tree;
- UI screenshots, diagrams, API docs, schemas;
- preferred technology stack;
- constraints, deployment target, budget, deadlines;
- existing issues or known bugs.

## Required output package

| File | Purpose | Required |
|---|---|---|
| `PROJECT.md` | Complete, normalized product and technical specification | Yes |
| `BUILD_PROMPT.md` | Main end-to-end prompt for the selected IDE agent | Yes |
| `AGENT_INSTRUCTIONS.md` | Portable project-specific execution rules | Yes |
| `IMPLEMENTATION_PLAN.md` | Phased milestones, dependencies, and tasks | Yes |
| `SECURITY_PLAN.md` | Threats, controls, security tools, and test checkpoints | For software with meaningful security scope |
| `ACCEPTANCE_MATRIX.md` | Requirement-to-test-to-evidence mapping | Yes |
| `DECISIONS.md` or ADR files | Important decisions, assumptions, and trade-offs | When needed |
| `IDE_ADAPTER.md` | IDE-specific setup instructions | Only for the selected IDE if needed |

The package must be self-contained. It may link to official tool repositories and documentation, but must not require cloning OpenClone.
