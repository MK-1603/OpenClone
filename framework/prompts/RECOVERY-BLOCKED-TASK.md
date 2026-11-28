# Protocol Prompt — Blocked Task & Failure Recovery

You are executing the **OpenClone Blocked Task Recovery Protocol** when a task encounters execution errors, failing tests, permission denials, or missing dependencies.

---

## 1. Objective
Systematically diagnose, isolate, remediate, and verify failures without breaking existing functionality or violating governance boundaries.

## 2. Mandatory Diagnostic Sequence

### Step 1: Capture Concrete Evidence
- Capture the exact terminal stdout, stderr, exit code, and stack trace.
- Identify the exact failing file path, function name, and line number.
- Do NOT guess the cause; rely strictly on observable error logs.

### Step 2: Classify the Failure Category
- **Category A — Syntax / Type Error:** Linter, TypeScript compiler, or import failure.
- **Category B — Missing Dependency / Package:** Uninstalled module or incompatible package version.
- **Category C — Logic / Assertion Failure:** Code returned unexpected output or violated test expectation.
- **Category D — Environment / Network / Permission Block:** Missing credentials, port conflict, or sandbox file permission boundary.

### Step 3: Minimal Root-Cause Remediation
1. Formulate the smallest contiguous code or configuration change that fixes the root cause.
2. Apply the fix.
3. Immediately re-run the exact failing test or command to prove remediation.
4. Run the entire test suite to guarantee zero collateral regressions.

### Step 4: Resolution Logging
Log the resolution in `PROGRESS.md`:
- **Issue:** [Brief summary of failure]
- **Root Cause:** [Why it failed]
- **Remediation:** [What was changed]
- **Evidence:** [Passing test output]
