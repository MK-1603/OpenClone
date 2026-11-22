# OpenClone — Decision & Fallback Runtime Policy
**Version:** 1.0.0  
**Scope:** Criteria, automatic triggers, and governance rules for activating fallbacks or migrating core dependencies.

---

## 1. When to Keep the Current Implementation

Keep the primary choice when:
1. It meets all functional and non-functional requirements.
2. It is actively maintained with a clean security record.
3. It has no material defect in performance, UX, latency, or operational cost.
4. The engineering cost of switching outweighs the measurable benefit.

---

## 2. When to Switch or Migrate

A formal migration is authorized only when:
1. A critical requirement cannot be satisfied by the current option.
2. The current option is abandoned upstream or introduces an unfixable CVE.
3. Measured reliability, latency, or cost is materially worse than the candidate.
4. The alternative provides a verified advantage and an automated migration script exists.

---

## 3. Fallback Activation Triggers & Rules

| Trigger Class | Specific Threshold | Automatic Action | Human Notification |
|---|---|---|---|
| **API Provider Outage** | 3 consecutive HTTP 5xx or connection timeouts | Failover to secondary provider (e.g. Anthropic $\rightarrow$ OpenAI) | Logged in session report with cost difference note |
| **Rate Limit Breach** | HTTP 429 received with `Retry-After` > 60 seconds | Switch to alternate model tier or secondary provider | Surface retry status in CLI / chat UI |
| **Model Incompatibility**| Model rejects structured output or tool calling | Fallback to capable frontier model | Record model limitation in task audit |
| **Security Advisory** | Critical CVE announced in core pinned scanner | Pin updated release SHA in `scanners.lock.json` | Security alert logged; PR generated |
| **Tool Execution Error** | Subprocess timeout or permission block | Fall back to manual instruction prompt | Print exact manual CLI command for human review |

---

## 4. Privacy & Governance Safeguards During Failover

- Failover must **NEVER** route requests to a provider that stores, trains on, or exfiltrates user prompts unless the user explicitly selected that model.
- Switching to a higher-cost model must stay within the project's allocated token budget.
