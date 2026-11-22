# Concept 08: Memory Architecture & Knowledge Management (Primary Specification)

## 1. Core Principle
Engineering knowledge must be structured, durable, and protected against prompt injection. OpenClone employs a **4-tier memory hierarchy** using an Obsidian-compatible Markdown vault (`memory/vault-template/`).

## 2. Invariants
1. **Strict Metadata:** Every memory note must contain valid YAML frontmatter declaring `memory_type`, `recorded_at`, `authority`, and `source_refs`.
2. **Anti-Injection Scanning:** The `memory-check` scanner flags adversarial instructions in memory notes.
3. **No Secrets:** Credentials, keys, and tokens are prohibited from being saved in project memory.
