# OpenClone 2.0 — Windows Native Executable & Installer Architecture

**Product:** OpenClone — Universal AI Engineering Platform  
**Component:** Windows Packaging & Distribution  
**Executable:** `oc.exe`  
**Installer:** `OpenClone-Setup.exe`  
**Specification:** `packaging/windows/openclone.spec`  
**Installer Definition:** `packaging/windows/openclone_installer.iss`  
**Build Script:** `packaging/windows/build.ps1`  

---

## 1. Executive Summary & Objective

OpenClone is packaged as a native Windows application, replacing `.cmd`-dependent execution with a standalone console executable (`oc.exe`) and a Windows native setup installer (`OpenClone-Setup.exe`).

The installation provides global command availability from any PowerShell or Command Prompt terminal without requiring manual repository navigation, environment activation, or pre-installed Python dependencies on client machines.

---

## 2. Packaging Architecture

```text
                                OPENCLONE SOURCE REPOSITORY
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       ▼                                             ▼
            PyInstaller Specification                     Inno Setup Script
       packaging/windows/openclone.spec         packaging/windows/openclone_installer.iss
                       │                                             │
                       ▼                                             ▼
          BUILD AUTOMATION PIPELINE                     BUILD AUTOMATION PIPELINE
          packaging/windows/build.ps1                  packaging/windows/build.ps1
                       │                                             │
        ┌──────────────┴──────────────┐                              │
        ▼                             ▼                              │
 STANDALONE EXECUTABLE        ONE-FOLDER DISTRIBUTION                │
     dist/oc.exe                 dist/openclone/                     │
   (Single-file CLI)          (Container / Deployment)               │
        │                             │                              │
        └─────────────────────────────┼──────────────────────────────┘
                                      ▼
                           NATIVE WINDOWS INSTALLER
                        installer/OpenClone-Setup.exe
                                      │
           ┌──────────────────────────┴──────────────────────────┐
           ▼                                                     ▼
     PER-MACHINE INSTALLATION                             PER-USER INSTALLATION
    (Run as Administrator)                                (Standard User)
    C:\Program Files\OpenClone\                           %LOCALAPPDATA%\Programs\OpenClone\
    System PATH (HKLM)                                    User PATH (HKCU)
```

---

## 3. Directory & Data Separation Contract

OpenClone strictly separates immutable application binaries from mutable user configurations and workspace states, ensuring zero data loss during upgrades or uninstalls.

| Layer | Filesystem Location | Scope | Mutability | Lifecycle |
| :--- | :--- | :--- | :--- | :--- |
| **Application Binaries** | `C:\Program Files\OpenClone\` (Admin) or `%LOCALAPPDATA%\Programs\OpenClone\` (User) | System / App | Read-Only | Overwritten on upgrade; removed on uninstall |
| **User Configuration** | `%APPDATA%\OpenClone\config.json` | Per-User | Read/Write | Preserved across upgrades; retained on uninstall |
| **User Cache & Runtime** | `%LOCALAPPDATA%\OpenClone\` | Per-User | Read/Write | Preserved across upgrades; retained on uninstall |
| **Workspace Ledger & State** | `<user-project>\.openclone\audit.db` | Per-Project | Read/Write | Bound strictly to user project; never touched by installer |

### Workspace Context Rule
When invoked as `oc inspect`, `oc plan`, `oc run`, or `oc verify` from an arbitrary directory (e.g. `D:\Projects\MyApp`), `oc.exe` resolves `Path.cwd()` as the active workspace root. It **never** forces operations to execute inside `C:\Program Files\OpenClone\`.

---

## 4. Standalone Executable (`dist/oc.exe`)

The executable is compiled using PyInstaller:

1. **Console Mode:** `console=True` preserving standard input, output, stderr, and escape codes.
2. **Bundled Package Resources:**
   - Canonical worker contracts: `src/openclone/workforce/registry/workers/*.json`
   - Project and agent templates: `src/openclone/templates/`
   - Framework validation schemas: `framework/schemas/*.json`
   - Release metadata: `VERSION`, `LICENSE`, `README.md`
3. **Dynamic Protocol & Runtime Dispatch:**
   - Hidden imports covering Model Intelligence Engine (`src.openclone.mie`), Autonomous Execution Engine (`src.openclone.autonomous`), Platform Integrations (`src.openclone.integrations`), Workforce (`src.openclone.runtime.workforce`), and MCP/ACP stdio adapters.
4. **Frozen Runtime Asset Resolution:**
   `RuntimeManager`, `Doctor`, and `InstallationManager` detect `sys._MEIPASS` when running in frozen mode to locate bundled assets without relying on development checkouts.

---

## 5. Windows Native Installer (`installer/OpenClone-Setup.exe`)

The installer is defined in Inno Setup (`packaging/windows/openclone_installer.iss`):

1. **Dual Privilege Mode:** Supports `PrivilegesRequired=lowest` with `PrivilegesRequiredOverridesAllowed=dialog commandline`.
   - Elevated execution installs to `C:\Program Files\OpenClone\`.
   - Standard user execution installs to `%LOCALAPPDATA%\Programs\OpenClone\`.
2. **Defensive PATH Environment Registration:**
   - Checks `NeedsAddPath` before writing to avoid duplicate entries.
   - Appends `{app}` to user PATH (`HKCU\Environment`) or system PATH (`HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`).
   - Preserves existing system and user PATH variables intact.
3. **Safe Uninstallation:**
   - Implements `CurUninstallStepChanged(usPostUninstall)` with `RemoveFromPath` to cleanly strip `{app}` from PATH.
   - Leaves `%APPDATA%\OpenClone` and workspace `.openclone` data untouched.
4. **Start Menu Integration:**
   - Adds Start Menu shortcuts for `OpenClone CLI Terminal` running in `%USERPROFILE%`.
   - Includes standard Add/Remove Programs registration with publisher details and icon.

---

## 6. Build Automation (`packaging/windows/build.ps1`)

The automated PowerShell build script carries out the 8-stage packaging lifecycle:

```powershell
# Build standalone oc.exe and OpenClone-Setup.exe
.\packaging\windows\build.ps1

# Build skipping pre-build unit tests
.\packaging\windows\build.ps1 -SkipTests

# Clean previous build artifacts
.\packaging\windows\build.ps1 -CleanOnly
```

### Build Stages:
1. **[1/8] Python Verification:** Locates valid 64-bit Python $\ge$ 3.10, ignoring WindowsApps execution aliases.
2. **[2/8] Dependency Check:** Verifies and auto-installs `pyinstaller`.
3. **[3/8] Safe Artifact Cleaning:** Removes old `build/`, `dist/oc.exe`, `dist/openclone/`, and `installer/` outputs without deleting source or user data.
4. **[4/8] Test Quality Gate:** Executes automated test suite before building.
5. **[5/8] PyInstaller Build:** Compiles `packaging/windows/openclone.spec` into `dist/oc.exe` and `dist/openclone/`.
6. **[6/8] Binary Validation:** Validates `oc.exe --version` and `oc.exe --help`.
7. **[7/8] SHA-256 Checksums:** Calculates and writes `dist/SHA256SUMS.txt`.
8. **[8/8] Inno Setup Compilation:** Locates `ISCC.exe` across standard locations; compiles `installer/OpenClone-Setup.exe`.

---

## 7. GitHub Actions CI/CD Integration

In `.github/workflows/release.yml`, a dedicated `build-windows-package` job executes on `windows-latest`:
- Provisions Python 3.11 and dependencies.
- Installs Inno Setup via `choco install innosetup --no-progress`.
- Runs `packaging/windows/build.ps1 -SkipTests`.
- Uploads `dist/oc.exe`, `installer/OpenClone-Setup.exe`, and `dist/SHA256SUMS.txt` directly to the GitHub Release.
