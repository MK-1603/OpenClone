# Contributing to OpenClone

Thank you for your interest in contributing to **OpenClone** (canonical framework standard: **AISDF** — AI Software Development Framework). We welcome contributions from human software engineers and AI-assisted workflows that adhere to rigorous engineering standards.

---

## 1. Ground Rules & Code of Conduct

1. **Be Respectful:** All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).
2. **Truthful Maturity:** Never claim a feature, adapter, test, or security control is complete without tangible code and reproducible test evidence.
3. **No Unmonitored AI Slop:** Generated code must follow [Taste Skill v2.6.0](domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md) anti-slop guidelines and strict least-privilege security boundaries.
4. **Deterministic Decision Authority:** AI models propose; human maintainers and deterministic validation engines decide.

---

## 2. Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ (for Taste Skill governance tests)
- Git

### Initializing Environment
```bash
# Clone the repository
git clone https://github.com/MK-1603/OpenClone.git
cd OpenClone

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 3. Pull Request Guidelines

### Step 1: Open an Issue First
Before submitting non-trivial pull requests, open an issue detailing:
- The concrete problem or requirement.
- Why existing capabilities in the 31 domains or 56 engines are insufficient.
- The proposed architectural changes.

### Step 2: Create a Focused Branch
Branch from `main` using descriptive naming conventions:
- `feature/<short-name>`
- `fix/<short-name>`
- `docs/<short-name>`

### Step 3: Run Full Verification Suite
All pull requests must pass the local verification suite prior to submission:
```bash
# 1. Run repository structural integrity check (domains, engines, schemas)
python tools/validate_repository.py

# 2. Run all unit and integration tests (78 passing tests)
python -m unittest discover -s tests -v

# 3. Run Taste Skill governance validation (13 tests)
node skills/taste-skill/tests/test-governance.mjs

# 4. Run Skill Engine verification
python tools/skill_engine.py verify
```

### Step 4: Submit Pull Request
Fill out the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md) completely, including:
- Task ID and description.
- Affected domains and files.
- Exact commands and test execution output.
- Security and backward-compatibility impact.

---

## 4. Coding Conventions

- **Code Style:** Clean, typed Python following PEP 8. Type hints are mandatory on all public interfaces.
- **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat(...)`: New user-facing or platform capability.
  - `fix(...)`: Bug fix or error resolution.
  - `docs(...)`: Documentation and markdown additions.
  - `test(...)`: Unit, integration, or governance tests.
  - `refactor(...)`: Code change that neither fixes a bug nor adds a feature.
- **Zero Secrets Policy:** Never commit secrets, API keys, private tokens, or proprietary customer data. All sample configs must use synthetic data.
