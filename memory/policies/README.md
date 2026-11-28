# Memory Policies

Deterministic security and governance policies:
1. **Scope Isolation:** Project A cannot query or mutate Project B memory records.
2. **Secret Redaction:** Multi-pass regex filtering redacts API keys and credentials before persistence.
3. **Retention Limits:** Configurable TTL and automated consolidation of redundant episodic records.
