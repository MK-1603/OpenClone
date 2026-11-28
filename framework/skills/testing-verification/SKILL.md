---
name: testing-verification
description: Conducts deterministic unit testing, integration verification, secret scanning, repository validation, and independent verification review.
version: 2.0.0
---

# Testing & Verification Skill

## Purpose
Ensures truthful evidence-backed verification before declaring any task, milestone, or release complete.

## Key Steps
1. Execute unit and integration tests (python -m pytest tests/).
2. Run repository secret scanner (python tools/scan_secrets.py).
3. Validate repository links and schemas (python tools/validate_repository.py).
4. Verify responsive layout across all 6 target breakpoints.
5. Record exact command outputs, exit codes, and test pass counts.
