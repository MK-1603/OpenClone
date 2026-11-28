# Concept 08: Memory Architecture & Knowledge Management (Primary Specification)

## 1. Core Principle
Engineering knowledge must be structured, durable, and protected against prompt injection. OpenClone employs a **4-tier memory hierarchy** using an Obsidian-compatible Markdown vault (`memory/vault-template/`).

## 2. Invariants
1. **Strict Metadata:** Every memory note must contain valid YAML frontmatter declaring `memory_type`, `recorded_at`, `authority`, and `source_refs`.
2. **Anti-Injection Scanning:** The `memory-check` scanner flags adversarial instructions in memory notes.
3. **No Secrets:** Credentials, keys, and tokens are prohibited from being saved in project memory.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Semantic Vector RAG & Knowledge Graph
In large enterprises with thousands of past projects, markdown search alone cannot retrieve nuanced historical design rationales. The alternate model provides **Dynamic Vector & Graph Retrieval**.

## 2. How the Alternate Operates
1. **Embedding Pipeline:** Notes and decision records are chunked and embedded via local embedding models into a vector store (e.g. SQLite-VSS, pgvector, or Chroma).
2. **Knowledge Graph Triples:** Architectural entities (`ServiceA` -> `communicates_with` -> `ServiceB`) are stored in an RDF/property graph.
3. **Hybrid RAG Recall:** At prompt generation time, OpenClone queries both graph relationships and semantic embeddings to inject relevant historical lessons.

## 3. Trade-Off Analysis
* **Strengths:** High retrieval accuracy across massive historical codebases.
* **Risks:** Higher computational overhead and potential embedding drift over time.
