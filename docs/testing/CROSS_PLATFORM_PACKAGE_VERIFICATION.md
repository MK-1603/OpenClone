# Cross-Platform Package Verification

**Version:** 2.0.0  
**Classification:** Quality Assurance & Packaging Verification  
**Status:** IMPLEMENTED  

---

## 1. Overview

Package distributions (both source distributions `.tar.gz` and built wheels `.whl`) must be verified on fresh, clean operating system instances across Linux, macOS, and Windows prior to release.

Workflow file: `.github/workflows/wheel-smoke-test.yml`

---

## 2. Verification Matrix

| Operating System | Architecture | Python Versions | Target Shell |
| :--- | :--- | :--- | :--- |
| **Ubuntu 22.04 LTS** | x86_64 | 3.10, 3.11, 3.12 | bash |
| **macOS 14 (Sonoma)** | Apple Silicon (M1/M2) | 3.10, 3.11, 3.12 | zsh / bash |
| **Windows Server 2022** | x86_64 | 3.10, 3.11, 3.12 | PowerShell Core |

---

## 3. Smoke Test Procedure

For each matrix node, the pipeline executes the following deterministic steps:

1. **Clean Environment Provisioning:** Standard runner initialization with no pre-installed project dependencies.
2. **Artifact Acquisition:** Download built wheel from release build artifacts.
3. **Cross-Platform Wheel Installation:**
   To prevent shell wildcard resolution failures on Windows PowerShell (e.g., `dist/*.whl`), installation uses Python-level globbing:
   ```bash
   python -c "import pathlib, subprocess, sys; whl = list(pathlib.Path('dist').glob('*.whl'))[0]; subprocess.run([sys.executable, '-m', 'pip', 'install', str(whl)], check=True)"
   ```
4. **Import Verification:**
   ```bash
   python -c "import openclone; print('OpenClone version:', openclone.__version__)"
   ```
5. **CLI Entrypoint Smoke Test:**
   ```bash
   openclone --help
   openclone --version
   ```
6. **Subprocess Isolation Check:** Confirm CLI dispatches properly without relying on local repository paths.
