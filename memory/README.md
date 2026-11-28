# OpenClone Memory Subsystem

The `memory/` directory houses the persistent memory vault, knowledge indexing, and session memory stores for the OpenClone framework.

## Structure

- **`vault/`**: Persistent encrypted knowledge artifacts, context embeddings, and retrieval records utilized by the `MemoryManager` across multi-turn reasoning and agent workflows.

## Governance & Security

1. **Isolation:** Agent memory stores are isolated per project and workspace.
2. **Redaction:** Sensitive credentials and API tokens are redacted before persistence into memory records.
3. **Immutability:** Core governance checkpoints and memory audit logs are append-only.
