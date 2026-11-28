# OpenClone OpenAI Provider Modernization — GPT-4o to GPT-6 Migration Audit & Plan

**Document Version:** 1.0.0  
**Status:** AUDITED / IN IMPLEMENTATION  
**Target Module:** `src/openclone/mie/providers/openai.py` & `src/openclone/mie/registry.py`  
**Governing Standard:** OpenClone Universal AI Engineering Framework  
**Date:** November 2026  

---

## 1. Executive Summary & Objective

OpenClone's Model Intelligence Engine (MIE) was initially baselined with legacy frontier models, including OpenAI's `gpt-4o` and `gpt-4o-mini`. As OpenAI establishes the **GPT-6 family** (`gpt-6.2-astra`, `gpt-6.2-sol`, `gpt-6.1-terra`, `gpt-6-luna`), OpenClone requires a full architectural modernization across:
1. Canonical model registry and capability metadata.
2. Provider HTTP adapter with native **Responses API** (`/v1/responses`) support alongside `/v1/chat/completions`.
3. Parameter modernization (adopting `reasoning.effort`, removing invalid `temperature`/`top_p` on reasoning tiers).
4. Task-based intelligent routing policies (defaulting general intelligence to `gpt-6.2-sol` and advanced engineering to `gpt-6.2-astra`).
5. Multimodal vision input handling for `gpt-6.1-terra`.
6. Backward-compatible legacy migration shims so existing workflows referencing `gpt-4o` transparently alias to compatible GPT-6 tiers without breaking.

---

## 2. Complete GPT-4o Repository Audit

A repository-wide audit identified 23 core occurrences across 9 files (excluding decoupled upstream copyleft sandboxes):

| File Path | Line(s) | Exact Match Text | Classification | Migration Action |
|---|---|---|---|---|
| `src/openclone/mie/providers/openai.py` | 49 | `model: str = "gpt-4o"` | **Active Runtime Default** | Upgrade default to `gpt-6.2-sol`. |
| `src/openclone/mie/providers/openai.py` | 128 | `return ["gpt-4o", "gpt-4o-mini", "o1", "o3-mini"]` | **Active Runtime Registry** | Update to `["gpt-6.2-sol", "gpt-6.2-astra", "gpt-6.1-terra", "gpt-6-luna", "o1", "o3-mini"]`. |
| `src/openclone/mie/registry.py` | 80–103 | `model_id="gpt-4o"` | **Active Registry Record** | Retain as legacy entry; add full GPT-6 catalog. |
| `src/openclone/mie/registry.py` | 105–125 | `model_id="gpt-4o-mini"` | **Active Registry Record** | Retain as legacy entry; designate `gpt-6-luna` as modern lightweight replacement. |
| `src/openclone/mie/hosts/base.py` | 98 | `native_model_affinity=["claude-3-5-sonnet", "gpt-4o"]` (Cursor) | **Host Affinity Config** | Upgrade to include `gpt-6.2-sol`. |
| `src/openclone/mie/hosts/base.py` | 114 | `native_model_affinity=["gpt-4o", "o1", "o3-mini"]` (Codex) | **Host Affinity Config** | Upgrade to `["gpt-6.2-sol", "gpt-6.2-astra", "o3-mini"]`. |
| `src/openclone/mie/hosts/base.py` | 130 | `native_model_affinity=["gpt-4o", "claude-3-5-sonnet"]` (Kiro) | **Host Affinity Config** | Upgrade to include `gpt-6.2-sol`. |
| `src/openclone/mie/hosts/base.py` | 146 | `native_model_affinity=["gpt-4o", "o1"]` (ChatGPT) | **Host Affinity Config** | Upgrade to `["gpt-6.2-sol", "gpt-6.2-astra"]`. |
| `assessments/model-intelligence/MIE-BASELINE.md` | 90, 96, 183 | Provider taxonomy & fallback examples | **Baseline Spec** | Update primary OpenAI models to GPT-6 series. |
| `docs/alternatives/PROVIDER_AND_MODEL_ALTERNATIVES.md` | 11–12 | OpenAI fallback alternatives | **Architecture Docs** | Update catalog references to GPT-6.2 series. |
| `docs/alternatives/ALTERNATIVES_CATALOGUE.md` | 17 | `OpenAI GPT-4o / o3-mini` | **Architecture Docs** | Modernize to `OpenAI GPT-6.2 Sol / Astra`. |
| `docs/integrations/compatibility-matrix.md` | 27 | `OpenAI (GPT-4o, o1, o3)` | **Architecture Docs** | Modernize to `OpenAI (GPT-6 series, o-series)`. |
| `docs/reference/AI_ENGINEERING_CATALOGUE.md` | 23 | Historical VLM topic summary | **Historical Reference** | Preserve historical context; add GPT-6.1 Terra. |
| `tests/test_mie.py` | 64, 200, 229, 233, 314 | Pytest fixture assertions | **Test Fixtures** | Modernize to test GPT-6 models while maintaining legacy alias tests. |

---

## 3. Target GPT-6 Model Catalogue

| Model Name | Canonical Model ID | Family | Context Window | Max Output | Reasoning Support | Vision / Multimodal | Primary Workload |
|---|---|---|---|---|---|---|---|
| **GPT-6.2 Astra** | `gpt-6.2-astra` | GPT-6 | 256,000 | 128,000 | Yes (`low`, `medium`, `high`) | Yes | Advanced engineering, architectural design, complex bug RCA. |
| **GPT-6.2 Sol** | `gpt-6.2-sol` | GPT-6 | 256,000 | 32,768 | Yes (Auto) | Yes | **General-purpose intelligence default**, workflow orchestration, full-stack code. |
| **GPT-6.1 Terra** | `gpt-6.1-terra` | GPT-6 | 256,000 | 16,384 | Standard | Yes (Enhanced) | Visual reasoning, UI screenshots, DOM layout, computer-use. |
| **GPT-6 Luna** | `gpt-6-luna` | GPT-6 | 128,000 | 16,384 | No | No | High-speed scaffolding, linting, unit test boilerplate, low cost. |

---

## 4. Default Routing & Fallback Policy

```
[Inbound Engineering Task]
            │
   [Task Classifier]
            │
            ├─(Visual / UI Screenshot)──────────> gpt-6.1-terra
            │
            ├─(Deep Architecture / Security)────> gpt-6.2-astra (reasoning.effort: high)
            │
            ├─(Scaffolding / Quick Boilers)─────> gpt-6-luna
            │
            └─(General Intelligence / Default)──> gpt-6.2-sol (Primary Default)
                                                      │
                                                      ├── If Rate Limited / Outage:
                                                      ▼
                                                [Fallback Chain]
                                                1. gpt-6.2-astra (if available)
                                                2. claude-3-7-sonnet (cross-provider)
                                                3. gemini-2.0-flash (cross-provider)
```

---

## 5. API Modernization: Responses API & Chat Completions

1. **Responses API Support (`/v1/responses`):**
   - Implements native endpoint calling when `use_responses_api=True` or when `reasoning_effort` is configured.
   - Structured payload:
     ```json
     {
       "model": "gpt-6.2-astra",
       "input": [{"role": "user", "content": "..."}],
       "reasoning": {"effort": "high"},
       "max_output_tokens": 16384
     }
     ```
2. **Chat Completions Compatibility (`/v1/chat/completions`):**
   - Preserved for OpenAI-compatible endpoints (Groq, vLLM, OpenRouter, Azure).
   - Parameter cleaning: Strips `temperature` and `top_p` for reasoning models (`gpt-6.2-astra`, `o1`, `o3-mini`).
3. **Multimodal Payload Adapter:**
   - Supports text strings, image URLs, and base64 data URIs transparently.
4. **Structured Output:**
   - Supports `response_format: {"type": "json_schema", "json_schema": ...}`.
