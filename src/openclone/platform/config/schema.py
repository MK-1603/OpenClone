"""Configuration schema definitions and validation for OpenClone."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class UpdateConfig:
    """Update engine configuration."""
    channel: str = "stable"  # stable, beta, nightly
    auto_check: bool = True
    manifest_url: Optional[str] = None
    allow_downgrades: bool = False


@dataclass
class TelemetryConfig:
    """Telemetry and audit logging preferences."""
    audit_ledger_enabled: bool = True
    redact_credentials: bool = True
    local_logging_level: str = "INFO"


@dataclass
class PlatformUserConfig:
    """Root user configuration for OpenClone."""
    version: str = "1.0.0"
    active_profile: str = "default"
    update: UpdateConfig = field(default_factory=UpdateConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    default_approver: Optional[str] = None
    custom_component_paths: List[str] = field(default_factory=list)
    extra_settings: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlatformUserConfig:
        """Create configuration instance from dictionary with validation."""
        version = data.get("version", "1.0.0")
        active_profile = data.get("active_profile", "default")
        
        up_data = data.get("update", {})
        update = UpdateConfig(
            channel=up_data.get("channel", "stable"),
            auto_check=up_data.get("auto_check", True),
            manifest_url=up_data.get("manifest_url"),
            allow_downgrades=up_data.get("allow_downgrades", False),
        )

        tel_data = data.get("telemetry", {})
        telemetry = TelemetryConfig(
            audit_ledger_enabled=tel_data.get("audit_ledger_enabled", True),
            redact_credentials=tel_data.get("redact_credentials", True),
            local_logging_level=tel_data.get("local_logging_level", "INFO"),
        )

        return cls(
            version=version,
            active_profile=active_profile,
            update=update,
            telemetry=telemetry,
            default_approver=data.get("default_approver"),
            custom_component_paths=data.get("custom_component_paths", []),
            extra_settings=data.get("extra_settings", {}),
        )
