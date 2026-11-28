# OpenClone Master Alternatives Catalogue
**Version:** 1.0.0  
**Scope:** Comprehensive reference for primary choices, fallbacks, and candidate alternatives across all software engineering disciplines.

---

## 1. Executive Summary

This catalogue details the primary and alternative technologies supported across the OpenClone platform. OpenClone maintains strict architectural boundaries: one preferred implementation is standard, while credible alternatives and fallback procedures are maintained for critical failure paths.

---

## 2. Core Capability Area Matrix

| Area | Capability | Current Primary | Primary Role | Tested / Preferred Fallback | Specialist Alternative |
|---|---|---|---|---|---|
| **AI Models** | Frontier Code Generation | Claude 3.5 / 3.7 Sonnet | `PRIMARY` | OpenAI GPT-6.2 Sol / Astra / o3-mini | DeepSeek-R1 (Local / Ollama) |
| **Model Routing** | Provider Failover | Direct Provider Adapters | `PRIMARY` | LiteLLM Proxy | Portkey / Cloudflare Gateway |
| **UI Components** | Primitives & Tokens | `shadcn/ui` + Tailwind CSS | `PRIMARY` | Radix Primitives + CSS Variables | Park UI (Ark UI) / Mantine |
| **Visual Governance** | Anti-AI-Slop & Quality | Taste Skill v2.6.0 | `PRIMARY` | Stylelint + ESLint Custom Rules | Biome + Custom AST Guards |
| **Design Critique** | Visual Post-Build Review | `hallmark` + 100-pt Audit | `PRIMARY` | Playwright Visual Regression | BackstopJS / Percy |
| **Static Security (SAST)** | AST / Rule Vulnerability Scan | Semgrep CE | `PRIMARY` | CodeQL (GitHub Actions) | Bandit (Python) / Slither |
| **Secret Scanning** | Git / Repo Secret Detection | TruffleHog OSS | `PRIMARY` | Gitleaks | detect-secrets |
| **Dynamic Security (DAST)** | Penetration Testing | Strix (Docker Isolated) | `SPECIALIST` | Nuclei (ProjectDiscovery) | OWASP ZAP (Baseline) |
| **Control Plane** | Task DAG & State Machine | SQLite3 + Python DAG | `PRIMARY` | PostgreSQL + Temporal | In-Memory Deterministic Engine |
| **Tool Protocol** | AI Tool & Service Interop | MCP (JSON-RPC 2.0 stdio/SSE) | `PRIMARY` | REST / OpenAPI Schemas | CLI Subprocess Adapters |
| **Session Continuity** | Context & Amnesia Defense | Goldfish (`PROGRESS.md`) | `PRIMARY` | Git Commit Audit Trail | Agent Memory Vault (JSON) |

---

## 3. Alternative Selection & Migration Rules

1. **Failure Triggers:** A switch from Primary to Fallback occurs automatically or via configuration upon:
   - Upstream service outage or persistent 5xx errors (> 3 consecutive attempts).
   - API rate limit or quota exhaustion.
   - Severe security vulnerability or licensing change in primary library.
2. **Privacy & Security Parity:** Any fallback activated must strictly adhere to the same privacy, encryption, and credential safety standards as the primary.
