# OpenClone (AISDF) 1.0 Quick Start

Requirements: Python 3.10+. Zero third-party runtime dependencies required for the core control plane.

## 0. Installation Options
You can use OpenClone directly from source or install it into your active Python environment:
```bash
# Option A: Direct execution from source
python openclone.py <command>
# (or legacy: python aisdf.py <command>)

# Option B: Editable pip installation
pip install -e .
openclone <command>
```

## 1. Verify Environment and Test Suite
```bash
python tools/validate_repository.py
python -m unittest discover -s tests -v
```

## 2. Initialize a Governed Project
**In a real terminal** (approvals require a human at a keyboard), create a project workspace and register yourself as approver:
```bash
python openclone.py init --project ../demo --name "Demo" --owner "Your Name"
```

## 3. Plan Tasks
Ingest a task plan and validate the dependency DAG:
```bash
python openclone.py plan --project ../demo --tasks examples/tasks.example.json
```

## 4. Human Approval (Digest-Bound)
Approve a task. The approval is cryptographically bound to the SHA-256 digest of the task specification:
```bash
python openclone.py approve --project ../demo --task-id DISC-001 --approver "Your Name"
```

## 5. Transition to Ready
Transition the task to `READY` (re-verifies human approval digest and ensures all dependencies have succeeded):
```bash
python openclone.py transition --project ../demo --task-id DISC-001 --to READY
```

## 6. Governed Execution and Evidence Recording
Record the completed work:
- For human-assisted execution:
  ```bash
  python openclone.py complete --project ../demo --task-id DISC-001 --actor "Your Name" --result SUCCEEDED --evidence report.md
  ```
- For automated execution (tasks with action `execute`):
  Ensure the binary is registered in `../demo/.aisdf/policy.json` under `allowed_executables`, then execute:
  ```bash
  python openclone.py run --project ../demo --task-id ID
  ```

## 7. State & Ledger Integrity Verification
Inspect the current state and audit the SHA-256 hash-chain of all historical events:
```bash
python openclone.py status --project ../demo
python openclone.py verify-ledger --project ../demo
```

## 8. Workspace Diagnostics & Migration
Run deep pre-flight health diagnostics or upgrade an existing project database:
```bash
python openclone.py doctor --project ../demo
python openclone.py upgrade --project ../demo --actor "Your Name"
```

## 9. Release Gate & Assurance
Record required checks, export independent reviewer package, add findings, and evaluate the release gate:
```bash
python openclone.py check run --project ../demo --id unit-tests --tool py -- python -m unittest
python openclone.py gate --project ../demo
```

*Note for CI/automation:* Add `--non-interactive` to human commands. Non-interactive approvals are recorded as weaker assurance and the default release gate policy refuses them for sensitive actions (`write`, `execute`, `deploy`).

Full command reference: `runtime/README.md`. Rules and enforcement details: `docs/framework/RULES-AND-ENFORCEMENT.md`. Upgrade guide: `UPGRADE.md`. Multi-tool adapter compatibility: `adapters/COMPATIBILITY.md`.
