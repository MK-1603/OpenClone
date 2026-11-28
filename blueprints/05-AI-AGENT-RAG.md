# Blueprint 05: AI Agent & RAG System

**Project Family:** `ai_engineering`  
**Primary Project Type:** `rag_knowledge_system`, `autonomous_agent_system`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `containers_cloud`, `web_browser`

---

## 1. Goals & Scope
- Generative AI applications utilizing Retrieval-Augmented Generation (RAG), vector embeddings, semantic search, autonomous tool-calling agents, and prompt guardrails.
- Enforces strict protection against indirect prompt injection, data leakage, hallucinated citations, and uncontrolled agent loops.

## 2. Classification Rules
- Matched when the project incorporates LLM API calls, vector databases (Chroma, Qdrant, Pinecone), embeddings, semantic chunking, tool-calling loops, or multi-agent orchestration.

## 3. Intake Questions & Required Information
1. Model selection: GPT-6.2 Astra / Sol, Claude 3.7 Sonnet, Gemini 2.5 Pro, local Ollama.
2. Embedding strategy: chunk size, overlap, embedding model, vector similarity metric.
3. Ingestion source: PDFs, markdown, HTML, internal databases, API feeds.
4. Tool boundaries: read-only tools vs. write/action tools requiring human approval.
5. Evaluation framework: golden test questions, citation precision, groundedness metrics.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `00-GOVERNANCE`, `01-SPECIFICATION`, `02-ARCHITECTURE`, `03-DATA-INTEGRITY`, `04-SECURITY-CONTROLS`, `29-AI-GOVERNANCE`, `30-AGENT-RULES-AND-VERIFICATION`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-003`, `E-004`, `E-029`, `E-030`.

## 5. Specialist Workforce
- `ai-engineer`: Prompt engineering, context assembly, and model adapter integration.
- `rag-specialist`: Document chunking, hybrid search (dense + sparse BM25), and re-ranking.
- `eval-engineer`: Golden dataset benchmarking, citation recall, and regression gates.
- `security-engineer`: Indirect prompt injection defense and secret scrubber verification.

## 6. Verification & Delivery Artifacts
- Evaluation benchmark report proving zero prompt injection bypasses.
- RAG citation precision report across golden benchmark questions.
- Deterministic token budgeting and circuit breaker test suite.
