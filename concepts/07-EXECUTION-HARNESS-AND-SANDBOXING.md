# Concept 07: Execution Harness & Sandboxing (Primary Specification)

## 1. Core Principle
Local execution must be strictly governed to prevent accidental damage, runaway processes, and credential leakage.

## 2. Invariants
1. **Allowlisted Binaries:** Only executables declared in `.aisdf/policy.json` (`allowed_executables`) may be invoked.
2. **Secret Redaction:** Standard output and error streams are filtered through redaction regexes before evidence logging.
3. **Execution Timeouts:** Commands enforce strict timeouts to prevent hanging processes.
