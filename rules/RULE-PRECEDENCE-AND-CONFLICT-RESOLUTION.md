# Rule Precedence and Conflict Resolution Standard
**Version:** 1.0.0 | **Status:** RATIFIED | **Canonical Identity:** OpenClone

---

## 1. Core Hierarchy

In any OpenClone execution context, configuration directives, constraints, and instructions are resolved according to the following strict 4-tier precedence:

```
+-----------------------------------------------------------+
| 1. Project Rule (AGENTS.md, host-specific project rules)  |  (HIGHEST)
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
| 2. Project State (.openclone/config.yaml, active plans)   |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
| 3. Global Installation (~/.openclone/config.yaml, global) |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
| 4. Framework Defaults (framework/rules/*, built-in specs) |  (LOWEST)
+-----------------------------------------------------------+
```

Formula:  
`project rule > project .openclone > ~/.openclone global > framework defaults`

---

## 2. Conflict Resolution Invariants

1. **Local Trumps Global:** A repository-specific `AGENTS.md` or `.cursor/rules/` rule always overrides global defaults.
2. **Deterministic Over LLM:** Programmatic rules and schema validations strictly override LLM assertions.
3. **Safety Non-Negotiables:** Higher-privilege rules (e.g. security policies) cannot be weakened by lower-tier preferences.
