# OpenClone Windows Code Signing & Executable Trust Guide

## 1. Executive Summary & Root Cause

Windows 11 Smart App Control (SAC) blocks executables when:
1. The binary has **no Authenticode digital signature** (`Status: NotSigned`), or
2. The signature is invalid/expired/revoked, or
3. The executable is not recognized by Microsoft Defender SmartScreen Cloud Intelligence and lacks a trusted code-signing certificate (such as an EV Code Signing Certificate or Microsoft Trusted Signing certificate).

### Pre-Upgrade Audit of `dist/oc.exe`
```powershell
Get-AuthenticodeSignature .\dist\oc.exe | Format-List Status, StatusMessage, SignerCertificate
# Output: Status: NotSigned

(Get-Item .\dist\oc.exe).VersionInfo | Format-List ProductName, CompanyName, FileDescription
# Output: ProductName: [empty], CompanyName: [empty], FileDescription: [empty]
```

**Root Causes Identified:**
- The previous PyInstaller build did not specify a Windows `version_info` resource, producing binaries with blank metadata.
- No code signing step was executed post-compilation.
- No signing architecture existed to bind SHA-256 digests with RFC 3161 timestamps.

---

## 2. Upgrades Implemented

### A. Windows Version & Publisher Metadata
- Created [version_info.txt](file:///d:/New%20folder/OpenClone/packaging/windows/version_info.txt) defining:
  - **Product Name:** `OpenClone`
  - **File Description:** `OpenClone Universal AI Engineering Platform`
  - **Product Version / File Version:** `2.0.0.0`
  - **Original Filename:** `oc.exe`
  - **Company / Publisher:** `OpenClone Contributors`
  - **Copyright:** `Copyright (c) 2026 OpenClone Contributors. Licensed under MIT.`
- Configured [openclone.spec](file:///d:/New%20folder/OpenClone/packaging/windows/openclone.spec) with `version=version_file`.

### B. Dedicated Authenticode Signing Engine
- Implemented [packaging/windows/signing.ps1](file:///d:/New%20folder/OpenClone/packaging/windows/signing.ps1) with:
  - `Find-SignTool`: Auto-locates Windows SDK `signtool.exe` (x64/x86 across Windows 10/11 Kits).
  - `Get-SigningCertificate`: Resolves certificates from Windows Certificate Store (`CurrentUser\My` or `LocalMachine\My`), PFX files, or certificate subject. Filters strictly for valid **Code Signing OID `1.3.6.1.5.5.7.3.3`**.
  - `Invoke-AuthenticodeSign`: Executes `signtool sign /v /fd SHA256 /tr http://timestamp.digicert.com /td SHA256` (with PowerShell `Set-AuthenticodeSignature` fallback).
  - `Test-AuthenticodeSignatureStrict`: Verifies signature validity via `signtool verify /pa /v` and `Get-AuthenticodeSignature`.

### C. Enhanced Automated Build Pipeline
- Upgraded [packaging/windows/build.ps1](file:///d:/New%20folder/OpenClone/packaging/windows/build.ps1) to 11 distinct stages:
  1. Python environment validation
  2. Build dependency check (`PyInstaller`)
  3. Safe artifact cleanup
  4. Test suite quality gate verification
  5. Standalone executable compilation with version resource
  6. Binary validation & VersionInfo inspection
  7. Signing configuration resolution (`-CertThumbprint`, `-PfxPath`, `-RequireSigning`)
  8. Signing of `oc.exe` and bundled binaries (DLLs, `.pyd` modules)
  9. Inno Setup installer compilation (`OpenClone-Setup.exe`) and installer signing
  10. SHA-256 release checksum generation
  11. Comprehensive Build & Trust Report

### D. Protected CI/CD Release Pipeline
- Updated [.github/workflows/release.yml](file:///d:/New%20folder/OpenClone/.github/workflows/release.yml):
  - Injects `WINDOWS_SIGNING_CERT_BASE64` and `WINDOWS_SIGNING_CERT_PASSWORD` securely in GitHub Actions.
  - Automatically cleans up transient PFX files in runner temp storage.
  - Enforces `-RequireSigning` when production certificates are configured.

---

## 3. How to Sign Builds Locally or in Production

### Option 1: Using Windows Certificate Store (Recommended for Dev / Hardware Token)
Install your code-signing certificate into your Windows User Certificate Store, then run:
```powershell
powershell -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -CertThumbprint "<YOUR_SHA1_THUMBPRINT>"
```

### Option 2: Using a Protected PFX Certificate File
```powershell
$env:OPENCLONE_PFX_PATH = "C:\secure\certificates\openclone_codesign.pfx"
$env:OPENCLONE_PFX_PASSWORD = "YourSecurePassword"
powershell -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -RequireSigning
```

### Option 3: Unsigned Development Build
If no code-signing certificate is installed, running the build will explicitly tag the output as:
```
Authenticode Status:   UNSIGNED (Development Build — Not verified for Smart App Control)
Smart App Control:     BLOCKED by SAC (Untrusted/Unsigned Binary)
```

---

## 4. Smart App Control & SmartScreen Considerations

- **Authenticode Signature:** Guarantees tamper-evidence and establishes publisher identity.
- **Smart App Control (Windows 11):** If SAC is set to "Evaluation" or "On", unsigned binaries are instantly blocked. A valid Authenticode signature from a recognized Certificate Authority (DigiCert, Sectigo, etc.) or Microsoft Trusted Signing satisfies the identity gate.
- **Reputation Warming:** Standard Code Signing certificates require initial download volume to build SmartScreen reputation. EV (Extended Validation) certificates or Microsoft Trusted Signing provide immediate reputation.
