# Mobile Physical Device Lab Integration

**Version:** 2.0.0  
**Classification:** Testing & Hardware Integration Guide  
**Status:** IMPLEMENTED  

---

## 1. Overview

OpenClone provides a unified test execution abstraction for mobile applications running across physical devices, tethered emulators, and cloud device farms (such as Firebase Test Lab or AWS Device Farm).

Module implementation: `src/openclone/testing/mobile/adapter.py`

---

## 2. Supported Providers & Adapters

| Adapter Class | Target Infrastructure | Discovery Mechanism |
| :--- | :--- | :--- |
| `LocalAdbDeviceLabAdapter` | Physical Android devices and emulators connected via USB/TCP | `adb devices -l` subprocess querying |
| `FirebaseTestLabAdapter` | Google Cloud Firebase Test Lab Matrix | `gcloud firebase test android run` CLI |
| `IosSimulatorDeviceLabAdapter` | Apple macOS CoreSimulator environments | `xcrun simctl list devices` |

---

## 3. Data Models

### 3.1 DeviceInfo
Encapsulates discovered hardware capabilities and status:
- `device_id`: Serial identifier (e.g., `emulator-5554`, `RFCW10ABCDE`).
- `platform`: Operating system (`android`, `ios`).
- `model`: Device model string (e.g., `Pixel 7 Pro`, `iPhone 15`).
- `os_version`: OS revision string (e.g., `14.0`, `17.2`).
- `status`: Device availability state (`online`, `offline`, `unauthorized`, `busy`).

### 3.2 DeviceTestResult
Captures execution outcomes:
- `test_id`: Identifier of executed test case.
- `device_id`: Device serial where test ran.
- `passed`: Boolean indicator of test success.
- `duration_seconds`: Execution duration.
- `output_log`: Detailed stdout/stderr and logcat output.
- `artifact_paths`: Paths to recorded screenshots, video captures, or crash dumps.

---

## 4. Execution Workflow

1. **Discovery:** The adapter queries available tethered devices using platform tools.
2. **Readiness Verification:** Verifies device authorization status and battery/storage health.
3. **App Installation:** Deploys target APK/AAB or IPA bundle via `adb install -r`.
4. **Test Runner Launch:** Dispatches instrumentation tests (Espresso, Flutter Driver, Appium).
5. **Artifact Harvesting:** Pulls screenshots and device logs into the test report directory.

---

## 5. Programmatic Example

```python
from openclone.testing.mobile.adapter import LocalAdbDeviceLabAdapter

adapter = LocalAdbDeviceLabAdapter(adb_path="adb")

# Discover all online Android devices
devices = adapter.list_devices()
print(f"Found {len(devices)} available device(s):")
for dev in devices:
    print(f"- {dev.model} ({dev.device_id}) [OS: {dev.os_version}]")

# Execute a mobile test suite on a specific device
if devices:
    result = adapter.run_test(
        device_id=devices[0].device_id,
        test_suite_path="build/app/outputs/apk/debug/app-debug.apk"
    )
    print(f"Test Run Result: {'PASSED' if result.passed else 'FAILED'}")
    print(f"Duration: {result.duration_seconds}s")
```
