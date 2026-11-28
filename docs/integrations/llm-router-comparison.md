# External LLM Router & Gateway Comparison
**Technical Evaluation of 8 Open-Source Router Candidates**  
**Specification:** v1.0.0 | **Authority:** Evaluative Architecture Record

---

## 1. Executive Summary & Selection Architecture

OpenClone evaluates multi-model routing candidates to fulfill two requirements without compromising supply-chain integrity:
1. **Model Agnosticism**: Prevent vendor lock-in across OpenAI, Anthropic, Gemini, Grok, Qwen, DeepSeek, and local inference engines.
2. **Deterministic Governance**: Ensure streaming, cancellation, token budgeting, tool calling, and secret redaction operate predictably.

### Architectural Decision (ADR-ROUTER-001)
> **Decision**: OpenClone implements a **thin, zero-dependency, normalized internal provider contract** (`OpenClone ProviderAdapter`) backed by direct official provider APIs and local runtimes (Ollama/vLLM), rather than vendoring third-party proxy daemons. For users requiring external dynamic multi-provider routing, OpenClone provides standardized adapter hooks conforming to the OpenRouter/OpenAI-compatible specification.

---

## 2. Candidate Evaluation Matrix

The eight evaluated open-source router repositories:

| Repository Candidate | Upstream URL | Primary Language | License | Tool Calling | Streaming | Recommendation / Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Devansh-365/freellm** | `github.com/Devansh-365/freellm` | Python | MIT | Partial | Yes | **Research Reference**: Useful token-tracking heuristics; unpinned dependencies prevent vendoring. |
| **kaiser-data/free-llm-proxy-router** | `github.com/kaiser-data/free-llm-proxy-router` | Python / FastAPI | MIT | No | Yes | **Research Reference**: High latency overhead for coding-agent streaming; adapter candidate only. |
| **nabinkhadka/free-llm-api** | `github.com/nabinkhadka/free-llm-api` | TypeScript | Apache-2.0 | Partial | Yes | **Optional External Daemon**: Best suited for standalone local Docker container deployment. |
| **YeomanYe/free-llm-router** | `github.com/YeomanYe/free-llm-router` | Go | MIT | No | Yes | **Research Reference**: Fast compilation, but lacks strict JSON-RPC structured error normalization. |
| **alienz-dev/llm-router** | `github.com/alienz-dev/llm-router` | Rust | MIT | Yes | Yes | **Top External Candidate**: Excellent concurrency and low memory footprint; recommended for high-load edge deployments. |
| **MajidAsghariTabrizi/free-best-router**| `github.com/MajidAsghariTabrizi/free-best-router` | Python | GPL-3.0 | No | No | **Rejected for Core**: GPL-3.0 license incompatibility with OpenClone MIT framework; lacks streaming. |
| **tashfeenahmed/freellmapi** | `github.com/tashfeenahmed/freellmapi` | JavaScript | MIT | No | Yes | **Research Reference**: Lacks function/tool-calling preservation required by coding agents. |
| **Gmagl/omniroute** | `github.com/Gmagl/omniroute` | Python | Apache-2.0 | Yes | Yes | **Secondary Compatible**: Comprehensive model catalog; excessive dependency weight for core distribution. |

---

## 3. Normalized Provider Contract

OpenClone standardizes model dispatch through the internal interface:

```python
class ProviderAdapter(Protocol):
    id: str
    display_name: str

    def validate_configuration(self) -> ValidationResult: ...
    def list_models(self) -> list[ModelDescriptor]: ...
    def get_capabilities(self, model: str) -> CapabilitySet: ...
    def generate(self, request: InferenceRequest) -> InferenceResponse: ...
    def stream(self, request: InferenceRequest) -> Iterator[InferenceChunk]: ...
    def cancel(self, request_id: str) -> bool: ...
    def normalize_error(self, error: Exception) -> NormalizedError: ...
```

### Capability Declarations
Every connected model declares explicit support states:
- `text_generation`: `SUPPORTED` | `UNSUPPORTED`
- `function_calling`: `SUPPORTED` | `UNSUPPORTED`
- `structured_json`: `SUPPORTED` | `UNSUPPORTED`
- `vision_multimodal`: `SUPPORTED` | `UNSUPPORTED`
- `streaming`: `SUPPORTED` | `UNSUPPORTED`

OpenClone **never** silently downgrades a function-calling request to plain text or routes large-context codebases to models with insufficient verified context windows.

---

## 4. Routing Policies & Safe Fallback

OpenClone enforces five deterministic routing policies:

1. **Manual Selection**: Strict adherence to the model specified in task metadata or user prompt.
2. **Approved Fallback**: Primary route with explicit, pre-authorized secondary route upon HTTP 429 (Rate Limit) or 503 (Unavailable). *Cross-provider fallback requires explicit user configuration to prevent unauthorized data egress.*
3. **Local-Only**: Forces inference through loopback sockets (`localhost:11434` for Ollama, `localhost:8000` for vLLM) ensuring zero network egress.
4. **Capability-Gated**: Filters candidate models strictly by declared capabilities (e.g., verifying `function_calling` before dispatching workflow tasks).
5. **Economic / Free-Tier**: Prioritizes verified free quotas (e.g., Google AI Studio, OpenRouter free-tier), with automatic cutoff at zero-cost boundaries.
