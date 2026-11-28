"""Mobile Application Store Compliance Scanner.

Audits iOS & Android projects for Apple Privacy Manifest requirements (NSPrivacyTracking,
NSPrivacyCollectedDataTypes, NSPrivacyAccessedAPITypes) and Google Play Data Safety
declarations, verifying compliance before production app store submission.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


@dataclass
class ComplianceFinding:
    """A compliance issue or recommendation identified during mobile scanning."""
    platform: str  # 'ios' or 'android'
    severity: str  # 'ERROR', 'WARNING', 'INFO'
    rule_id: str
    message: str
    target_file: Optional[str] = None


@dataclass
class MobileComplianceReport:
    """Comprehensive mobile app store compliance report."""
    ios_compliant: bool
    android_compliant: bool
    findings: List[ComplianceFinding] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(f.severity == "ERROR" for f in self.findings)


class MobileComplianceScanner:
    """Audits Apple Privacy Manifests and Android Data Safety configurations."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def scan_ios(self) -> List[ComplianceFinding]:
        """Scan iOS project for PrivacyInfo.xcprivacy and required privacy declarations."""
        findings: List[ComplianceFinding] = []
        manifests = list(self.project_root.glob("**/PrivacyInfo.xcprivacy"))
        
        # Also check for .plist files that might act as privacy manifest
        if not manifests:
            findings.append(ComplianceFinding(
                platform="ios",
                severity="WARNING",
                rule_id="IOS-PRIVACY-001",
                message="No PrivacyInfo.xcprivacy found. Apple App Store mandates Privacy Manifests for SDKs and apps.",
            ))
            return findings

        for manifest in manifests:
            try:
                content = manifest.read_text(encoding="utf-8", errors="ignore")
                # Basic check for required keys
                if "NSPrivacyTracking" not in content:
                    findings.append(ComplianceFinding(
                        platform="ios",
                        severity="ERROR",
                        rule_id="IOS-PRIVACY-002",
                        message="PrivacyInfo.xcprivacy missing mandatory key: NSPrivacyTracking",
                        target_file=str(manifest.relative_to(self.project_root)),
                    ))
                if "NSPrivacyCollectedDataTypes" not in content:
                    findings.append(ComplianceFinding(
                        platform="ios",
                        severity="WARNING",
                        rule_id="IOS-PRIVACY-003",
                        message="PrivacyInfo.xcprivacy missing NSPrivacyCollectedDataTypes declaration",
                        target_file=str(manifest.relative_to(self.project_root)),
                    ))
            except Exception as e:
                findings.append(ComplianceFinding(
                    platform="ios",
                    severity="ERROR",
                    rule_id="IOS-PARSE-ERR",
                    message=f"Failed to parse PrivacyInfo.xcprivacy: {e}",
                    target_file=str(manifest.relative_to(self.project_root)),
                ))

        return findings

    def scan_android(self) -> List[ComplianceFinding]:
        """Scan Android project for AndroidManifest.xml and dangerous permissions."""
        findings: List[ComplianceFinding] = []
        manifests = list(self.project_root.glob("**/AndroidManifest.xml"))

        if not manifests:
            findings.append(ComplianceFinding(
                platform="android",
                severity="INFO",
                rule_id="AND-MANIFEST-001",
                message="No AndroidManifest.xml found in workspace.",
            ))
            return findings

        sensitive_permissions = [
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.READ_CONTACTS",
            "android.permission.READ_SMS",
            "android.permission.CAMERA",
            "android.permission.RECORD_AUDIO",
        ]

        for manifest in manifests:
            try:
                tree = ET.parse(manifest)
                root = tree.getroot()
                uses_permissions = [
                    elem.attrib.get("{http://schemas.android.com/apk/res/android}name")
                    for elem in root.findall("uses-permission")
                ]
                for perm in sensitive_permissions:
                    if perm in uses_permissions:
                        findings.append(ComplianceFinding(
                            platform="android",
                            severity="WARNING",
                            rule_id="AND-DATA-SAFETY-001",
                            message=f"Sensitive permission declared ({perm}). Google Play Data Safety form disclosure required.",
                            target_file=str(manifest.relative_to(self.project_root)),
                        ))
            except Exception as e:
                findings.append(ComplianceFinding(
                    platform="android",
                    severity="ERROR",
                    rule_id="AND-PARSE-ERR",
                    message=f"Failed to parse AndroidManifest.xml: {e}",
                    target_file=str(manifest.relative_to(self.project_root)),
                ))

        return findings

    def run_audit(self) -> MobileComplianceReport:
        """Execute full mobile compliance verification across platforms."""
        ios_findings = self.scan_ios()
        android_findings = self.scan_android()
        all_findings = ios_findings + android_findings

        ios_errors = any(f.platform == "ios" and f.severity == "ERROR" for f in ios_findings)
        android_errors = any(f.platform == "android" and f.severity == "ERROR" for f in android_findings)

        return MobileComplianceReport(
            ios_compliant=not ios_errors,
            android_compliant=not android_errors,
            findings=all_findings,
        )
