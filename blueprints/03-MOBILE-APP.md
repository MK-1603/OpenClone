# Blueprint 03: Mobile Application (Native & Cross-Platform)

**Project Family:** `mobile_engineering`  
**Primary Project Type:** `cross_platform_mobile`, `native_android`, `native_ios`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `android`, `ios`

---

## 1. Goals & Scope
- Touch-optimized mobile application for iOS and Android devices, tablets, and foldables.
- Manages native device lifecycle (foreground, background, suspended), offline storage cache, biometric authentication, push notifications, and app store release guidelines.

## 2. Classification Rules
- Matched when target devices are smartphones, tablets, or wearables, or when tech stack involves Flutter, React Native, Swift/SwiftUI, or Kotlin/Compose.

## 3. Intake Questions & Required Information
1. Target platform: iOS, Android, or unified cross-platform (Flutter / React Native).
2. Offline mode requirements: local SQLite / Hive / Room cache with optimistic updates and background sync.
3. Native device APIs: camera, geolocation, biometric auth, Bluetooth, file system.
4. Deep linking: universal links (iOS) and App Links (Android).
5. State management: Riverpod, Bloc, Redux, Zustand.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `05-DESIGN-SYSTEMS`, `07-ACCESSIBILITY-AND-INCLUSION`, `10-TESTING-AND-QA`, `14-PERFORMANCE-ENGINEERING`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-005`, `E-007`, `E-010`, `E-014`.

## 5. Specialist Workforce
- `mobile-engineer`: Core application logic, native bridging, and platform lifecycle.
- `android-specialist` / `ios-specialist`: OS-specific configurations, permissions, and app packaging.
- `ui-designer`: Mobile touch targets (min 48x48dp), safe area insets, and haptic feedback.

## 6. Tool & Model Allocation
- **Primary Model:** `gpt-6.2-sol` for state management and UI widget composition.
- **Visual Model:** `gpt-6.1-terra` for mobile screenshot layout auditing.

## 7. Verification & Delivery Artifacts
- Signed APK/AAB for Android; Xcode archive/IPA for iOS.
- Automated widget tests and device orientation tests.
- Offline-to-online network reconnection test evidence.
