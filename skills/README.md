# OpenClone Canonical Portable Agent Skills
## Host-Independent Capabilities for Universal AI Engineering

This directory houses canonical, portable Agent Skills conforming to the universal Agent Skills specification (`SKILL.md`). These skills are directly discoverable and executable across supported hosts (Google Antigravity, Claude Code, OpenAI Codex, Cursor, and other compatible AI coding environments).

---

## 1. Directory of Portable Skills

| Skill Directory | Purpose | Primary Disciplines |
|---|---|---|
| [`universal-project-intelligence/`](universal-project-intelligence/) | Multi-label project classification across 14 disciplines, technology evaluation, and package generation | ENG-01 through ENG-14 |
| [`product-discovery/`](product-discovery/) | Problem validation, stakeholder interviews, user journeys, and scope boundary definitions | ENG-14, ENG-05 |
| [`requirements-engineering/`](requirements-engineering/) | Functional requirements (FR), non-functional requirements (NFR), and acceptance criteria | ENG-01 through ENG-14 |
| [`architecture-design/`](architecture-design/) | Component boundaries, data lifecycle, API contracts, and technology stack evaluation | ENG-02, ENG-06, ENG-12 |
| [`ui-ux-engineering/`](ui-ux-engineering/) | Mandatory Responsive UI Engineering Standard (320px–1440px+), touch targets, WCAG AA accessibility | ENG-14, ENG-05 |
| [`secure-engineering/`](secure-engineering/) | Zero-trust access, secret scanning, token redaction, environment isolation, and fail-closed gates | ENG-11 |
| [`testing-verification/`](testing-verification/) | Deterministic unit tests, integration testing, secret auditing, and independent verification | ENG-13 |
| [`taste-skill/`](taste-skill/) | Anti-AI-slop visual tokens, morphism styling, typography scales, and clean aesthetic standards | ENG-14 |

---

## 2. Multi-Host Portability

These skills use standard Markdown frontmatter and step-by-step procedures:
- In **Google Antigravity**: Loaded natively via root `plugin.json` (`agy plugin install https://github.com/MK-1603/OpenClone`).
- In **Claude Code**: Loaded through marketplace installation (`/plugin marketplace add MK-1603/OpenClone`).
- In **OpenAI Codex**: Discovered via portable `plugin.json` and `.agents/plugins/marketplace.json`.
- In **Cursor / VS Code**: Referenced directly or executed via OpenClone MCP tools.
