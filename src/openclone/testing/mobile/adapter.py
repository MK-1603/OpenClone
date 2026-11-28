"""Mobile Physical Device Lab Integration Adapter.

Provides provider-neutral hardware test execution contracts and a local
Android Debug Bridge (ADB) execution harness for running real-device tests,
collecting logs, capturing screenshots, and recording test evidence.

Capability Scope:
- Static Compliance Scanning: Full support via `MobileComplianceScanner`.
- Physical Android & Emulators: Full support via `LocalAdbDeviceLabAdapter`.
- Physical iOS Hardware: Documented hardware limitation (requires macOS host with Xcode / idb).
- Cloud Device Farms: Interface defined in `BaseDeviceLabAdapter`, requires cloud credentials.
"""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("openclone.testing.mobile")

DEVICE_ID_REGEX = re.compile(r"^[a-zA-Z0-9._:-]+$")


@dataclass
class DeviceInfo:
    """Hardware device descriptor."""
    device_id: str
    platform: str  # 'android' or 'ios'
    model: str
    os_version: str
    status: str  # 'online', 'offline', 'unauthorized', 'device'
    is_emulator: bool = False


@dataclass
class DeviceTestResult:
    """Verifiable execution result of a physical mobile device test."""
    device_id: str
    test_name: str
    passed: bool
    duration_seconds: float
    stdout: str
    stderr: str
    screenshot_path: Optional[str] = None
    logcat_path: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class BaseDeviceLabAdapter:
    """Abstract interface contract for mobile physical device testing."""

    def list_devices(self) -> List[DeviceInfo]:
        raise NotImplementedError

    def install_app(self, device_id: str, package_path: Path) -> bool:
        raise NotImplementedError

    def run_instrumentation_test(
        self,
        device_id: str,
        package_name: str,
        test_runner: str,
        output_dir: Path,
    ) -> DeviceTestResult:
        raise NotImplementedError


class LocalAdbDeviceLabAdapter(BaseDeviceLabAdapter):
    """Local Android physical device testing harness using ADB.
    
    Security Controls:
    - Never executes arbitrary shell commands from untrusted inputs (`shell=False` strictly enforced).
    - Device identifiers are strictly validated against `^[a-zA-Z0-9._:-]+$`.
    - Controlled subprocess execution with mandatory timeouts.
    """

    def __init__(self, adb_path: Optional[str] = None):
        self.adb = adb_path or shutil.which("adb") or "adb"

    def _validate_device_id(self, device_id: str) -> bool:
        """Validate device identifier to prevent command injection."""
        return bool(device_id and DEVICE_ID_REGEX.match(device_id))

    def is_available(self) -> bool:
        """Verify ADB binary is installed and operational."""
        try:
            res = subprocess.run([self.adb, "version"], capture_output=True, text=True, timeout=5)
            return res.returncode == 0
        except Exception:
            return False

    def list_devices(self) -> List[DeviceInfo]:
        """Query attached Android physical devices and emulators via ADB."""
        if not self.is_available():
            logger.warning("ADB binary not available in PATH.")
            return []

        try:
            res = subprocess.run([self.adb, "devices", "-l"], capture_output=True, text=True, timeout=10)
            if res.returncode != 0:
                return []

            devices: List[DeviceInfo] = []
            for line in res.stdout.strip().splitlines()[1:]:
                parts = line.strip().split()
                if len(parts) >= 2:
                    dev_id = parts[0]
                    if not self._validate_device_id(dev_id):
                        logger.warning("Skipping device with invalid identifier: %s", dev_id)
                        continue

                    status = parts[1]
                    model = "Unknown Android"
                    for p in parts[2:]:
                        if p.startswith("model:"):
                            model = p.replace("model:", "")

                    is_emu = "emulator" in dev_id or "generic" in model.lower()
                    devices.append(DeviceInfo(
                        device_id=dev_id,
                        platform="android",
                        model=model,
                        os_version="Android",
                        status=status,
                        is_emulator=is_emu,
                    ))
            return devices
        except Exception as e:
            logger.error("Failed to query ADB devices: %s", e)
            return []

    def get_device_properties(self, device_id: str) -> Dict[str, str]:
        """Query device properties via getprop safely."""
        if not self._validate_device_id(device_id):
            raise ValueError(f"Invalid device identifier: {device_id}")

        try:
            res = subprocess.run(
                [self.adb, "-s", device_id, "shell", "getprop"],
                capture_output=True, text=True, timeout=10
            )
            props = {}
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if ":" in line:
                        k, _, v = line.partition(":")
                        props[k.strip("[] ")] = v.strip("[] \r\n")
            return props
        except Exception as e:
            logger.error("Failed to query device properties on %s: %s", device_id, e)
            return {}

    def install_app(self, device_id: str, package_path: Path) -> bool:
        """Deploy application APK/AAB package to physical hardware."""
        if not self._validate_device_id(device_id):
            raise ValueError(f"Invalid device identifier: {device_id}")

        if not package_path.exists() or not package_path.is_file():
            logger.error("Package file does not exist: %s", package_path)
            return False

        try:
            res = subprocess.run(
                [self.adb, "-s", device_id, "install", "-r", str(package_path)],
                capture_output=True, text=True, timeout=60
            )
            return res.returncode == 0 and "Success" in res.stdout
        except Exception as e:
            logger.error("App installation failed on %s: %s", device_id, e)
            return False

    def take_screenshot(self, device_id: str, local_path: Path) -> bool:
        """Capture screenshot from physical device safely without shell=True."""
        if not self._validate_device_id(device_id):
            raise ValueError(f"Invalid device identifier: {device_id}")

        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(local_path, "wb") as f:
                res = subprocess.run(
                    [self.adb, "-s", device_id, "exec-out", "screencap", "-p"],
                    stdout=f, stderr=subprocess.PIPE, timeout=15
                )
            return res.returncode == 0
        except Exception as e:
            logger.error("Screenshot capture failed on %s: %s", device_id, e)
            return False

    def collect_logcat(self, device_id: str, local_path: Path, max_lines: int = 500) -> bool:
        """Collect recent logcat buffer from hardware device for failure analysis."""
        if not self._validate_device_id(device_id):
            raise ValueError(f"Invalid device identifier: {device_id}")

        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            res = subprocess.run(
                [self.adb, "-s", device_id, "logcat", "-d", "-t", str(max_lines)],
                capture_output=True, text=True, timeout=15
            )
            if res.returncode == 0:
                local_path.write_text(res.stdout, encoding="utf-8")
                return True
            return False
        except Exception as e:
            logger.error("Logcat collection failed on %s: %s", device_id, e)
            return False

    def run_instrumentation_test(
        self,
        device_id: str,
        package_name: str,
        test_runner: str,
        output_dir: Path,
    ) -> DeviceTestResult:
        """Execute Android instrumentation test and harvest outputs."""
        if not self._validate_device_id(device_id):
            raise ValueError(f"Invalid device identifier: {device_id}")

        start_time = time.time()
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            res = subprocess.run(
                [self.adb, "-s", device_id, "shell", "am", "instrument", "-w", f"{package_name}/{test_runner}"],
                capture_output=True, text=True, timeout=180
            )
            duration = time.time() - start_time
            passed = res.returncode == 0 and "FAILURES!!!" not in res.stdout

            logcat_path = output_dir / f"logcat_{device_id}_{int(start_time)}.log"
            self.collect_logcat(device_id, logcat_path)

            screenshot_path = None
            if not passed:
                screenshot_file = output_dir / f"fail_{device_id}_{int(start_time)}.png"
                if self.take_screenshot(device_id, screenshot_file):
                    screenshot_path = str(screenshot_file)

            return DeviceTestResult(
                device_id=device_id,
                test_name=f"{package_name}/{test_runner}",
                passed=passed,
                duration_seconds=duration,
                stdout=res.stdout,
                stderr=res.stderr,
                screenshot_path=screenshot_path,
                logcat_path=str(logcat_path),
            )
        except Exception as e:
            duration = time.time() - start_time
            return DeviceTestResult(
                device_id=device_id,
                test_name=f"{package_name}/{test_runner}",
                passed=False,
                duration_seconds=duration,
                stdout="",
                stderr=str(e),
            )
