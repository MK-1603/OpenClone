# Blueprint 11: Embedded Systems, Firmware & Robotics

**Project Family:** `embedded_hardware_and_robotics`  
**Primary Project Type:** `rtos_firmware`, `robotics_platform`  
**Maturity Status:** `SPECIFIED`  
**Complexity Level:** `LARGE`  
**Default Delivery Targets:** `embedded_hardware`, `edge_devices`

---

## 1. Goals & Scope
- Microcontroller firmware, real-time operating systems (FreeRTOS, Zephyr), bare-metal C/Rust, peripheral drivers (I2C, SPI, UART, CAN), and robotics control loops.
- Enforces strict memory budgets, zero heap fragmentation in interrupt service routines (ISRs), watchdog safety, and fail-safe hardware states.

## 2. Classification Rules
- Matched when targeting microcontrollers (ARM Cortex-M, ESP32, STM32, RISC-V) or robotics platforms (ROS 2, motor kinematics, sensor fusion).

## 3. Intake Questions & Required Information
1. Target hardware/MCU: STM32F4, ESP32-S3, Nordic nRF52, Raspberry Pi RP2040.
2. Memory constraints: Flash size and SRAM capacity.
3. Real-time deadlines: task cycle frequencies and max interrupt latency.
4. Firmware update: dual-bank OTA, bootloader recovery, cryptographic signature.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `04-SECURITY-CONTROLS`, `14-PERFORMANCE-ENGINEERING`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-004`, `E-014`.

## 5. Specialist Workforce
- `embedded-engineer`: Hardware peripheral drivers, RTOS task priorities, and register I/O.
- `firmware-engineer`: Power management, sleep states, and OTA bootloaders.
- `robotics-engineer`: Control loops, PID tuning, and sensor telemetry.

## 6. Verification & Delivery Artifacts
- Static memory analysis report proving SRAM usage within 80% ceiling.
- Watchdog reboot test evidence under simulated task hang.
- Cryptographic firmware signature verification check.
