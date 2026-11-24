"""Mobile Physical Device Lab Integration Adapter.

Provides provider-neutral hardware test execution contracts and a local
Android Debug Bridge (ADB) execution harness for running real-device tests,
collecting logs, capturing screenshots, and recording test evidence.
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("openclone.testing.mobile")


@dataclass
class DeviceInfo:
    """Hardware device descriptor."""
    device_id: str
    platform: str  # 'android' or 'ios'
    model: str
    os_version: str
    status: str  # 'online', 'offline', 'unauthorized'
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
    """Local Android physical device testing harness using ADB."""

    def __init__(self, adb_path: Optional[str] = None):
        self.adb = adb_path or shutil.which("adb") or "adb"

    def is_available(self) -> bool:
        """Verify ADB binary is installed and operational."""
        try:
            res = subprocess.run([self.adb, "version"], capture_output=True, text=True, timeout=5)
            return res.returncode == 0
        except Exception:
            return False

    def list_devices(self) -> List[DeviceInfo]:
        """Query attached Android physical devices via ADB."""
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

    def take_screenshot(self, device_id: str, local_path: Path) -> bool:
        """Capture screenshot from physical device and save locally."""
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            cmd = f"{self.adb} -s {device_id} exec-out screencap -p"
            with open(local_path, "wb") as f:
                res = subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.PIPE, timeout=15)
            return res.returncode == 0
        except Exception as e:
            logger.error("Screenshot capture failed on %s: %s", device_id, e)
            return False
