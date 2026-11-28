# Changelog Automation Specification

**Version:** 2.0.0  
**Classification:** Release Automation  
**Status:** IMPLEMENTED  

---

## 1. Overview

OpenClone utilizes `git-cliff` with a tailored configuration file (`cliff.toml`) to automatically parse Git commit history according to Conventional Commits and render structured, versioned changelogs for human maintainers and automated release notes.

Configuration file: `cliff.toml`

---

## 2. Conventional Commit Classification

Commit messages are parsed using regex patterns into designated release categories:

| Conventional Commit Prefix | Section Title | Description |
| :--- | :--- | :--- |
| `feat:` | Features | New architectural capabilities, engines, or agents |
| `fix:` | Bug Fixes | Fixes for runtime, governance, or CLI regressions |
| `perf:` | Performance Improvements | Execution speedups, caching, SQLite query optimizations |
| `refactor:` | Refactoring | Code reorganization preserving public interfaces |
| `style:` | Code Style | Formatting, linting, whitespace adjustments |
| `test:` | Testing | New unit, integration, or smoke test coverage |
| `docs:` | Documentation | Updates to specifications, guides, or API references |
| `chore:` | Chores & Maintenance | Dependency bumps, script maintenance, tooling updates |
| `ci:` | Continuous Integration | Workflow modifications and runner updates |
| `security:` | Security Hardening | Cryptographic, sandbox, or permission enhancements |
| `revert:` | Reverts | Reversals of prior commits |

---

## 3. Usage & Invocation

### Generating Changelog Locally

```bash
# Generate full changelog to stdout
git-cliff

# Update CHANGELOG.md in-place
git-cliff --output CHANGELOG.md

# Preview changes for the upcoming unreleased version
git-cliff --unreleased
```

### GitHub Actions Integration

In `.github/workflows/release.yml`, `git-cliff` executes prior to release publication:

```yaml
- name: Generate Release Notes
  uses: orhun/git-cliff-action@v3
  with:
    config: cliff.toml
    args: --latest --strip header
  env:
    OUTPUT: RELEASE_NOTES.md
```
