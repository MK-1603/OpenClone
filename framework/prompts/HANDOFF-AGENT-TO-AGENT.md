# Protocol Prompt — Inter-Agent Handoff (Agent-to-Agent Transfer)

You are executing a **Structured Context Handoff** between OpenClone specialist agents.

---

## 1. Objective
Transfer authoritative project context, completed work units, evidence logs, and active constraints from an outgoing specialist to an incoming specialist with zero loss of state or hallucinations.

## 2. Mandatory Handoff Structure
Every handoff record must be authored in `HANDOFF.md` or output in the chat response using this schema:

```markdown
### 🔄 OPENCLONE INTER-AGENT HANDOFF

- **Source Agent:** [e.g., Software Architect / Frontend Engineer]
- **Target Agent:** [e.g., Backend Engineer / Test Engineer]
- **Timestamp:** [UTC Timestamp]
- **Active Phase:** [e.g., Phase 04 — Implementation]

#### 1. Completed Work Units & Output Files
- [file_path_1] — [brief summary of implementation / evidence]
- [file_path_2] — [brief summary of implementation / evidence]

#### 2. Verification & Test Evidence
- Tests Executed: [e.g., 24 passed | 0 failed]
- Evidence Logs: [file link or terminal output summary]

#### 3. Unresolved Decisions & Open Assumptions
- [Any assumption made that requires verification or human operator confirmation]

#### 4. Explicit Next Steps for Incoming Agent
1. [First action incoming agent must take]
2. [Acceptance criteria for the incoming work unit]
```

## 3. Receiving Agent Directive
The receiving agent must:
1. Verify that the files and evidence cited in the handoff actually exist.
2. Confirm scope boundaries before modifying code.
3. Advance the lifecycle according to the topological execution order.
