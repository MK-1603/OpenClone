# Mobile Physical Device Lab & Testing Standards

**Canonical Guide: Physical Device Verification vs. Synthetic Emulation**  
*OpenClone Global Engineering Standard | ENG-14 & Mobile Compliance*

---

## 1. Principles of Real-Device Verification

Synthetic emulators, Chromium viewports, and simulated mobile profiles do not accurately reproduce:
- Thermal throttling, memory constraints, and aggressive OS background process termination.
- Hardware sensor latency, gyroscope drift, and GPS accuracy.
- Native keyboard occlusion, viewport resizing (`window.visualViewport`), and IME composition.
- Biometric authentication flows (FaceID / TouchID / Android BiometricPrompt).
- Network interface transitions (Wi-Fi to 5G, captive portals, packet loss).

Physical device testing is **mandatory** before any mobile or responsive web application is declared `L5_VERIFIED` or released to production.

---

## 2. Platform Testing Matrices

### 2.1 Android Testing Baseline
- **Operating System Tiers:** Android 11, 13, and 14+.
- **Screen Densities & Aspect Ratios:** Foldables (inner vs outer screen), high-DPI compact (Pixel 8), budget/entry devices (720p).
- **OEM Variations:** Stock Android (AOSP/Pixel), One UI (Samsung), and MIUI/HyperOS (Xiaomi).

### 2.2 iOS Testing Baseline
- **Operating System Tiers:** iOS 16, 17, and 18+.
- **Form Factors:** Dynamic Island devices (iPhone 14 Pro+), notch devices (iPhone 13), home-button devices (iPhone SE).
- **iPadOS:** Stage Manager, split-view multitasking, and keyboard accessory interaction.

---

## 3. Mandatory Physical Device Test Procedures

### 3.1 Orientation & Safe Area Layout
- Rotate device through portrait, landscape-left, and landscape-right.
- Verify safe area insets: content must never clip into the notch, dynamic island, or home indicator bar (`env(safe-area-inset-top)` / `env(safe-area-inset-bottom)`).
- Ensure zero unexpected horizontal scrollbars (`overflow-x: hidden`).

### 3.2 Touch Target & Haptic Accessibility
- All primary interactive elements must meet the minimum 44×44pt (iOS) / 48×48dp (Android) touch target boundary.
- Tap targets must have at least 8px spacing to prevent accidental mis-taps.
- System font scaling (Dynamic Type on iOS / Font Scale on Android) must be tested up to 200% without text clipping or truncated labels.

### 3.3 Network Transition & Offline Handling
- **Airplane Mode Transition:** App must gracefully show an offline banner without crashing or showing blank screens.
- **Flaky Connection (3G / 500ms latency):** Spinners, optimistic UI updates, and retry buttons must function deterministically.
- **Token Expiry on Reconnection:** Expired sessions must route to authentication without data loss.

### 3.4 Camera, Filesystem & Permissions
- Verify runtime permission requests: rationale must be clearly presented before the system permission dialog.
- Test "Don't Allow" / Deny state: app must gracefully fallback and explain how to enable permissions via device settings.

---

## 4. Evidence Capture and Defect Reporting

When reporting a mobile defect or logging verification evidence:
1. **Device Metadata:** Brand, exact Model number, OS version, and build number.
2. **Network State:** Wi-Fi / Cellular (5G/LTE), proxy status, VPN active.
3. **Reproduction Steps:** Step-by-step from clean app launch.
4. **Visual Evidence:** Screen recording or screenshot highlighting the defect.
5. **System Log / Crash Report:** Native logcat or iOS sysdiagnose attached to the ticket.
