# Concept 10: Multi-Tool Adapter Ecosystem (Primary Specification)

## 1. Core Principle
OpenClone is provider-neutral and IDE-agnostic. Work is orchestrated using standardized work-unit contracts (`schemas/work-unit.schema.json`) that bridge to external tools like Claude Code, Cursor, Antigravity, OpenHands, and OpenCode.

## 2. Invariants
1. **Tool Independence:** The core control plane operates purely on local files, state databases, and standard CLI calls.
2. **Adapter Contract:** Adapters translate OpenClone lifecycle events into native tool configurations without violating the root permission rules.
