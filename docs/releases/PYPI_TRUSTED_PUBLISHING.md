# PyPI Trusted Publishing Architecture

**Version:** 2.0.0  
**Classification:** Release Engineering & Supply Chain Security  
**Status:** IMPLEMENTED  

---

## 1. Overview

OpenClone employs PyPI Trusted Publishing via OpenID Connect (OIDC) to eliminate static, long-lived API tokens in continuous integration. This mitigates supply-chain credential theft and restricts wheel and source distribution publication strictly to authorized GitHub Actions workflows running on tagged release commits.

Workflow file: `.github/workflows/release.yml`

---

## 2. Authentication & Trust Model

```
+-------------------------------------------------------------------------------+
|                             GitHub Actions Runner                             |
|                                                                               |
|  1. Request OIDC Token (actions/id-token permission)                          |
|  2. GitHub OIDC Provider issues short-lived JWT containing:                   |
|     - repository: "MK-1603/OpenClone"                                         |
|     - ref: "refs/tags/v*"                                                     |
|     - environment: "pypi"                                                     |
+------------------------------------+------------------------------------------+
                                     |
                                     | 3. Exchange JWT with PyPI
                                     v
+-------------------------------------------------------------------------------+
|                            PyPI Warehouse Registry                            |
|                                                                               |
|  4. Validate JWT Claims against PyPI Trusted Publisher Configuration         |
|  5. Mint temporary (15-minute) publish token                                  |
|  6. Accept wheel & sdist upload from pypa/gh-action-pypi-publish              |
+-------------------------------------------------------------------------------+
```

---

## 3. GitHub Actions Configuration

The workflow enforces mandatory security attributes:

```yaml
permissions:
  contents: write
  id-token: write  # Mandatory for PyPI Trusted Publishing OIDC exchange

jobs:
  pypi-publish:
    name: Upload Release to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/openclone
    steps:
      - name: Publish package distributions to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: dist/
          verbose: true
```

---

## 4. Environment Protection Rules

To prevent unauthorized or accidental production releases:
1. The `pypi` GitHub Environment requires mandatory manual review from designated repository maintainers before the job executes.
2. Deployment is restricted strictly to Git tags matching `v*` on the `main` branch.
3. Version parity is deterministically verified between Git tag name, `pyproject.toml`, and `src/openclone/__init__.py`.
