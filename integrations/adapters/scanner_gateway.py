"""
OpenClone Security Scanner Gateway Adapter
Unified discovery, configuration validation, and execution gating for external scanners:
- SEC-002: Nuclei (vulnerability templates)
- SEC-005: Semgrep (SAST)
- SEC-007: Trivy (CVE & container supply chain)
- SEC-008: TruffleHog (secret detection)
- SEC-010: ClamAV (antivirus)
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class ScannerGatewayAdapter:
    """Gateway for discovering, verifying, and executing external security scanners."""

    SUPPORTED_SCANNERS = {
        "semgrep": {"id": "SEC-005", "type": "SAST", "license": "LGPL-2.1"},
        "trivy": {"id": "SEC-007", "type": "SUPPLY_CHAIN", "license": "Apache-2.0"},
        "trufflehog": {"id": "SEC-008", "type": "SECRET_SCANNER", "license": "GPL-3.0"},
        "nuclei": {"id": "SEC-002", "type": "DAST_TEMPLATES", "license": "MIT"},
        "clamav": {"id": "SEC-010", "type": "ANTIVIRUS", "license": "GPL-2.0"},
    }

    def __init__(self, lockfile_path: Optional[Path] = None):
        self.lockfile_path = lockfile_path or (
            Path(__file__).resolve().parent.parent.parent / "security" / "scanners.lock.json"
        )

    def is_lockfile_pinned(self) -> bool:
        """Verify that security/scanners.lock.json exists and contains pinned scanner hashes."""
        if not self.lockfile_path.exists():
            return False
        try:
            data = json.loads(self.lockfile_path.read_text(encoding="utf-8"))
            return "scanners" in data and len(data["scanners"]) > 0
        except Exception:
            return False

    def list_available_scanners(self) -> List[Dict[str, Any]]:
        """List registered external scanners with their classification and license."""
        results = []
        for name, meta in self.SUPPORTED_SCANNERS.items():
            results.append({
                "name": name,
                "integration_id": meta["id"],
                "category": meta["type"],
                "license": meta["license"],
                "execution_policy": "ISOLATED_SANDBOX_REQUIRED",
            })
        return results

    def inspect_scanner(self, scanner_name: str) -> Dict[str, Any]:
        """Retrieve details and execution constraints for a specific scanner."""
        sname = scanner_name.lower().strip()
        if sname not in self.SUPPORTED_SCANNERS:
            return {
                "found": False,
                "error": f"Scanner '{scanner_name}' is not registered. Registered: {list(self.SUPPORTED_SCANNERS.keys())}",
            }
        meta = self.SUPPORTED_SCANNERS[sname]
        return {
            "found": True,
            "name": sname,
            "integration_id": meta["id"],
            "type": meta["type"],
            "license": meta["license"],
            "pinned_in_lockfile": self.is_lockfile_pinned(),
            "requires_authorization": True,
        }
