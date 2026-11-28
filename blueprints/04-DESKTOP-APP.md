# Blueprint 04: Desktop Application

**Project Family:** `desktop_engineering`  
**Primary Project Type:** `cross_platform_desktop`, `native_desktop_tool`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `windows`, `macos`, `linux`

---

## 1. Goals & Scope
- Cross-platform desktop software for Windows, macOS, and Linux using Tauri, Electron, or native frameworks.
- Integrates local filesystem access, process management, system tray, native menus, hardware acceleration, and cryptographically verified auto-updates.

## 2. Classification Rules
- Matched when target execution is local desktop OS, utilizing window managers, system tray, native installer packaging (.msi, .dmg, .deb, .AppImage), or local IPC.

## 3. Intake Questions & Required Information
1. Framework selection: Tauri (Rust backend + web frontend) or Electron.
2. Local permissions: filesystem access boundaries, external process execution.
3. Code signing: Apple Developer certificate / notarization, Windows Authenticode.
4. Update mechanism: Sparkle, Tauri updater, or Electron autoUpdater.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `04-SECURITY-CONTROLS`, `10-TESTING-AND-QA`, `13-DEPENDENCY-MANAGEMENT`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-004`, `E-010`, `E-013`, `E-022`.

## 5. Specialist Workforce
- `desktop-engineer`: Native windowing, IPC messaging, and cross-platform builds.
- `security-engineer`: IPC channel validation, context isolation, and code signing.
- `qa-engineer`: Windows/macOS/Linux matrix verification.

## 6. Verification & Delivery Artifacts
- Signed installer bundles (.msi, .dmg, .AppImage).
- Cryptographic update signature verification tests.
- Memory leak and process termination tests.
