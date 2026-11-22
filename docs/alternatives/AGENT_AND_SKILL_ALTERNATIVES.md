# OpenClone — Agent, Skill & Context Alternatives
**Version:** 1.0.0  
**Scope:** Alternatives for skill formats, tool protocols, agent orchestration harnesses, and context budget management.

---

## 1. Skill & Tool Protocol Alternatives

| Capability | Current Primary | Candidate Alternative | Specialist Alternative | Recommendation & Trade-Offs |
|---|---|---|---|---|
| **Skill Specification Format**| OpenClone Markdown Skill Manifest | Antigravity `SKILL.md` | Claude Code `.mcp.json` | Standardized markdown with YAML frontmatter is human-readable and universal |
| **Tool Communication** | Model Context Protocol (MCP) | Direct REST / OpenAPI 3.1 | Subprocess CLI Tool calling | MCP is standard for IDEs (Antigravity, Claude, Cursor); fallback to CLI tools |
| **Agent Orchestration** | Deterministic Python State Machine / DAG | LangGraph / AutoGen | CrewAI | Deterministic Python state machines eliminate hallucinated transitions |
| **Task State Verification** | SHA-256 Approval Digest Binding | Cryptographic JWT claims | Git Signed Commits | Digest binding invalidates approvals whenever tasks change |
| **Context Management** | Relevance Pruning + Sliding Window | LLMLingua (Prompt Compression) | Vector RAG Retrieval | Structured context pruning preserves exact system instructions without loss |
| **Memory Architecture** | Durable File State (`PROGRESS.md`) | SQLite Memory Table | Vector Embeddings (Chroma/Pinecone) | Durable Markdown files survive context resets without external dependencies |

---

## 2. Deterministic Execution vs. Autonomous Swarms

- **Deterministic Code Decides:** State transitions, human approval gates, budget enforcement, tool execution permissions, and evidence verification MUST be implemented in deterministic code.
- **LLMs Propose:** LLMs generate code, suggest architecture, explain errors, and write test scenarios.
- **No Unbounded Agent Swarms:** Infinite delegation, retry storms, and unmonitored worker fan-out are strictly prohibited by OpenClone governance.
