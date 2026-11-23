# OpenClone Model Intelligence Engine (MIE) — Architectural Baseline & Specification

**Document Version:** 1.0.0  
**Status:** SPECIFIED / IN PROGRESS  
**Target Subsystem:** `src/openclone/mie/`  
**Governance Standard:** OpenClone Universal AI Engineering Framework  
**Date:** November 2026  

---

## 1. Executive Summary & Problem Statement

OpenClone provides a deterministic, instruction-first software engineering platform governed by 31 knowledge domains, 56 deterministic engines, and 72 specialized workforce roles. Until now, model interactions within OpenClone were handled either externally by host AI IDEs (Antigravity, Claude Code, Cursor) or through external CLI worker subroutines.

As modern AI engineering scales, enterprise teams require:
1. **Multi-Provider Resilience**: Freedom from single-provider outages, rate-limit choke points, and latency spikes across OpenAI, Anthropic, Google Gemini, xAI, cloud hyperscalers (Bedrock, Vertex AI, Azure AI Foundry), and local inference engines (Ollama, vLLM).
2. **Context-Aware Task Routing**: Automatic alignment between task nature (e.g., formal security audits, deep reasoning, massive-context log ingestion, fast syntax scaffolding) and model architectural strengths.
3. **High Availability with Deterministic Governance**: Real-time circuit breaking (`CLOSED`, `OPEN`, `HALF_OPEN`), bounded exponential backoff with jitter, transparent same-model provider failover, and governed model fallback.
4. **Zero External Dependency Core**: A standard-library-first Python implementation (`urllib.request`, `json`, `sqlite3`, `dataclasses`) ensuring zero dependency bloat, high portability, and zero supply-chain friction.
5. **Privacy-Preserving Auditability**: Strict secret redaction, telemetry without prompt leakage, and ledger audit logging integrated into OpenClone's SQLite state store.

This document establishes the architectural baseline, gap analysis, component specifications, and validation gates for the **OpenClone Model Intelligence Engine (MIE)**.

---

## 2. Baseline Inventory & Gap Analysis

An audit of the current OpenClone repository (`MK-1603/OpenClone`, commit `24ea96d`) yields the following baseline:

| Subsystem / Component | Current Implementation State | MIE Requirement | Gap Analysis |
|---|---|---|---|
| **Host Integrations** (`src/openclone/runtime/adapters/`) | Worker adapters exist for Subprocess, HTTP, Docker, and WASM. | Host adapters for AI IDEs (Claude Code, Antigravity, Cursor, Codex, ChatGPT). | Current adapters govern worker process lifecycle, not LLM completion routing. |
| **Tool Gateway** (`src/openclone/integrations/gateway.py`) | Deterministic tool execution with permission enforcement and budget validation. | Model tool-calling schema transformation (JSON Schema format across OpenAI, Anthropic, Gemini). | Gateway provides tool execution; MIE must bridge model tool-calls to gateway actions. |
| **MCP Server** (`src/openclone/mcp/server.py`) | Exposes 11 tools (`get_guidance`, `search_knowledge`, `execute_workflow`, etc.). | Expose MIE tools: `openclone_route_model`, `openclone_list_models`, `openclone_model_health`. | Missing MIE tool endpoints in MCP server. |
| **Model Registry** | None. Model selection hardcoded or deferred to developer host. | Dynamic registry with discovery, context limits, pricing, modalities, and maturity status. | New core component required: `src/openclone/mie/registry.py`. |
| **Task Classifier** | None. Relies on human-assigned worker roles or workflow descriptors. | Deterministic classification across 14 engineering task categories with complexity & reasoning estimation. | New core component required: `src/openclone/mie/classifier.py`. |
| **Scoring & Routing** | None. | Multi-dimensional scoring (correctness, quality, reliability, latency, cost, tool execution) across 7 routing modes. | New core component required: `src/openclone/mie/evaluator.py` & `src/openclone/mie/router.py`. |
| **High Availability & Circuit Breakers** | None for LLM calls. | Tri-state circuit breakers, same-model failover, fallback chains, exponential retry with jitter. | New core component required: `src/openclone/mie/ha.py`. |
| **Provider Adapters** | None. | Native HTTP adapters for OpenAI, Anthropic, Google Gemini, xAI, Ollama. Zero external SDK dependencies. | New package required: `src/openclone/mie/providers/`. |
| **Telemetry & Cost Accounting** | General workforce telemetry in SQLite ledger. | Token usage, cost estimation, p50/p95 latency metrics with guaranteed zero prompt leakage. | New core component required: `src/openclone/mie/telemetry.py`. |

---

## 3. Host Environments vs. Model Providers

A foundational design tenet of MIE is the **strict separation between Host AI Coding Environments and Model API Providers**:

```
+-----------------------------------------------------------------------------------------+
|                                HOST AI CODING ENVIRONMENTS                               |
|   Claude Code (CLI)  |  Google Antigravity (IDE)  |  Cursor IDE  |  OpenAI Codex/ChatGPT |
+-----------------------------------------------------------------------------------------+
                                             |
                                   (Model Routing Intent /
                                   MCP Tool Invocations)
                                             v
+-----------------------------------------------------------------------------------------+
|                         OPENCLONE MODEL INTELLIGENCE ENGINE (MIE)                        |
|                                                                                         |
|  [Task Classifier]  -->  [Capability Registry]  -->  [Scoring Engine]                   |
|                                                             |                           |
|                                                    [Multi-Mode Router]                  |
|                                                             |                           |
|                                                 [High Availability (HA)]                 |
|                                                 - Circuit Breakers (Tri-State)          |
|                                                 - Exponential Backoff & Jitter          |
|                                                 - Same-Model Provider Failover          |
|                                                 - Cross-Model Fallback Chain            |
+-----------------------------------------------------------------------------------------+
                                             |
                       (Standardized Zero-Dependency HTTP Dispatch)
                                             v
+-----------------------------------------------------------------------------------------+
|                                   MODEL API PROVIDERS                                   |
|                                                                                         |
|  Tier 0 (Direct API):     OpenAI API  |  Anthropic API  |  Google Gemini API  | xAI API  |
|  Tier 1 (Cloud / Proxy):  AWS Bedrock |  GCP Vertex AI  |  Azure AI Foundry   | OpenRouter
|  Tier 2 & Local:          Ollama Local|  vLLM Local     |  Groq API           | Mistral  |
+-----------------------------------------------------------------------------------------+
```

Host AI environments invoke MIE either via direct Python library invocation (`src.openclone.mie`), CLI commands (`openclone route ...`), or Model Context Protocol (MCP) server tools (`openclone_route_model`).

---

## 4. Provider Taxonomy & Priority Matrix

| Tier | Provider Identifier | Target Endpoint Type | Authentication Mechanism | Supported Flagship Models | Conformance Status |
|---|---|---|---|---|---|
| **P0** | `openai` | Direct REST API (`api.openai.com/v1`) | `Bearer $OPENAI_API_KEY` | `gpt-4o`, `gpt-4o-mini`, `o1`, `o3-mini` | `IMPLEMENTED` |
| **P0** | `anthropic` | Direct REST API (`api.anthropic.com/v1`) | `x-api-key $ANTHROPIC_API_KEY` | `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku` | `IMPLEMENTED` |
| **P0** | `gemini` | Direct REST API (`generativelanguage.googleapis.com/v1beta`) | `key=$GEMINI_API_KEY` or ADC Bearer | `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash` | `IMPLEMENTED` |
| **P0** | `xai` | Direct REST API (`api.x.ai/v1`) | `Bearer $XAI_API_KEY` | `grok-2`, `grok-2-mini` | `IMPLEMENTED` |
| **P1** | `bedrock` | AWS SigV4 REST API | IAM Access Keys / IAM Role | Claude models, Llama models | `PLANNED` |
| **P1** | `vertex` | Google Cloud REST API | Google ADC OAuth2 Token | Gemini models, Claude on Vertex | `PLANNED` |
| **P1** | `azure` | Azure OpenAI REST API | `api-key $AZURE_OPENAI_KEY` | GPT-4o, o1 | `PLANNED` |
| **P1** | `openrouter` | OpenAI-compatible REST API | `Bearer $OPENROUTER_API_KEY` | Universal multi-model catalog | `IMPLEMENTED` |
| **P2** | `ollama` | Local REST API (`localhost:11434/api`) | None (Local Loopback) | `llama3.3`, `qwen2.5-coder`, `deepseek-r1` | `IMPLEMENTED` |
| **P2** | `vllm` | OpenAI-compatible REST API (`localhost:8000/v1`)| Bearer token (optional) | Self-hosted open weights | `IMPLEMENTED` |
| **P2** | `groq` | OpenAI-compatible REST API (`api.groq.com/openai/v1`) | `Bearer $GROQ_API_KEY` | `llama-3.3-70b-versatile`, `mixtral-8x7b` | `IMPLEMENTED` |

---

## 5. Task Intelligence Taxonomy (14 Categories)

MIE classifies every engineering instruction into one of 14 deterministic categories, mapping them to required capabilities:

1. `ARCHITECTURE_DESIGN`: Broad system design, ADRs, trade-off analysis. Requires high reasoning, large context, strong architectural synthesis.
2. `FRONTEND_UI`: UI components, CSS, React/Vue/HTML, responsive layout, accessibility (a11y). Requires strong design aesthetic, DOM understanding.
3. `BACKEND_API`: REST/gRPC/GraphQL endpoints, business logic, middleware, protocol handling.
4. `DATABASE_DATA`: SQL generation, schema migrations, query optimization, indexing, ORM models.
5. `SECURITY_AUDIT`: Vulnerability discovery, OWASP checks, static security review, remediation logic.
6. `REFACTORING`: Code simplification, anti-slop removal, dead code elimination, architectural alignment.
7. `TEST_ENGINEERING`: Unit tests, integration tests, mock generation, edge-case coverage.
8. `DEVOPS_INFRA`: Dockerfiles, CI/CD pipelines, Kubernetes manifests, Terraform/HCL scripts.
9. `DEBUGGING_RCA`: Error traceback diagnosis, root cause analysis, log parsing, fix verification.
10. `DOCUMENTATION_SPECS`: READMEs, API specifications, user manuals, markdown architecture guides.
11. `FAST_SCAFFOLDING`: Rapid boilerplate generation, CRUD templates, file stubs.
12. `CODE_REVIEW`: Pull request review, style compliance, regression risk identification.
13. `ML_DATA_SCIENCE`: Data analysis pipelines, PySpark, model training scripts, visualization.
14. `GENERAL_ORCHESTRATION`: Multi-step workflow synthesis, agent task delegation, instruction parsing.

---

## 6. Multi-Dimensional Scoring Engine

Model selection is evaluated dynamically via 6 weighted criteria:

$$\text{Score} = \sum_{i=1}^6 w_i \cdot s_i$$

| Dimension | Weight | Definition & Metrics |
|---|---|---|
| **Task Suitability & Correctness ($s_1$)** | 30% | Alignment with task requirements (reasoning depth, context capacity, coding benchmarks). |
| **Code Quality & Idiomatic Output ($s_2$)** | 20% | Conformity with modern idioms, zero halluncinations, anti-slop compliance. |
| **Provider Reliability & Health ($s_3$)** | 20% | Historical uptime, current circuit-breaker state, error rate under 1%. |
| **Latency & TTFT ($s_4$)** | 10% | Time-to-first-token and tokens-per-second execution speed. |
| **Cost Efficiency & Token Value ($s_5$)** | 10% | Combined input and output price per 1M tokens relative to budget. |
| **Tool Execution & Schema Adherence ($s_6$)** | 10% | Precision of JSON Schema parameter generation in function calling. |

---

## 7. Multi-Mode Routing Strategies

1. `BEST_QUALITY`: Maximizes task suitability and code quality regardless of cost. Ideal for architecture, security audits, and mission-critical refactors.
2. `BALANCED` (Default): Optimizes balanced utility across quality, cost, and latency.
3. `LOW_LATENCY`: Prioritizes fast TTFT and high tokens-per-second (e.g. Groq, Flash models). Ideal for autocomplete, interactive chat, or fast scaffolding.
4. `LOW_COST`: Selects the lowest-cost model meeting minimum capability thresholds. Ideal for bulk documentation, simple test generation, and basic log audits.
5. `HIGH_AVAILABILITY`: Prioritizes active healthy providers with lowest error rates and robust fallback redundancy.
6. `USER_SELECTED`: Uses developer's explicitly requested model while validating health and configuring backup fallback.
7. `POLICY_CONTROLLED`: Enforces strict organizational constraints (e.g., "no external data transmission", "on-premise only", "spend cap per prompt").

---

## 8. High Availability Architecture (Circuit Breaker & Fallback)

```
[Request Inbound]
       │
       ▼
[Circuit Breaker Check] ──(State == OPEN)──> [Trip to Same-Model Failover / Backup]
       │ (State == CLOSED or HALF_OPEN)
       ▼
[Execute HTTP Request via Provider Adapter]
       ├─── SUCCESS ───> [Record Success, Update Latency Telemetry, Return Output]
       │
       └─── FAILURE (5xx / 429 / Timeout / ConnectionError)
                 │
                 ▼
       [Update Circuit Breaker Error Counter]
                 │
                 ├── Retries Remaining? ─── YES ──> [Exponential Backoff with Jitter] ──> Loop
                 │
                 └── Retries Exhausted or CB Trips to OPEN:
                           │
                           ▼
                 [Failover Phase 1: Same-Model Alternative Provider]
                 (e.g., Anthropic Direct -> AWS Bedrock -> GCP Vertex)
                           │
                           └── If Failover Fails / Unavailable:
                                     │
                                     ▼
                           [Failover Phase 2: Cross-Model Fallback Chain]
                           (e.g., Claude 3.5 Sonnet -> GPT-4o -> Gemini 1.5 Pro)
```

### Tri-State Circuit Breaker Rules
- **`CLOSED`**: All traffic passes to primary provider. Failures are tracked over a sliding 60-second window.
- **`OPEN`**: Tripped when failure rate exceeds 50% (min 5 requests) or 3 consecutive 5xx/timeouts occur. Traffic is immediately redirected to backup provider.
- **`HALF_OPEN`**: After a cooldown window (default 30 seconds), a trial probe request is permitted. If successful, state reverts to `CLOSED`; if failed, state resets to `OPEN` with doubled cooldown.

---

## 9. Security, Privacy & Audit Ledger

1. **Zero Prompt Persistence**: Prompts and completions are processed in memory and never written to logs or disk without explicit user authorization.
2. **Deterministic Secret Redaction**: All API keys, authorization tokens, and credentials are scrubbed using the OpenClone safe redaction pattern before any telemetry logging.
3. **Audit Ledger Integration**: All routing decisions, provider selections, token usage numbers, and fallback transitions are written to OpenClone's SQLite ledger with cryptographic hash chaining (`workforce.sqlite3` / `mie.sqlite3`).

---

## 10. Phased Implementation Roadmap

- **Phase 1 (MIE Core)**: Dataclasses, BaseProvider contract, Registry, TaskClassifier, Evaluator, Router, HA Engine (`CLOSED`/`OPEN`/`HALF_OPEN`), and Telemetry.
- **Phase 2 (Providers)**: Native zero-dependency HTTP adapters for OpenAI, Anthropic, Gemini, xAI, and Ollama.
- **Phase 3 (Hosts & Tools)**: Host IDE adapters (Claude Code, Antigravity, Cursor, etc.) and MCP tools integration.
- **Phase 4 (Validation)**: Comprehensive test suite (`tests/test_mie_*.py`) with mock fixtures, verifying zero external dependency requirement, circuit breaker dynamics, and routing algorithms.
