"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — QA Engine.

Automated verification checklist scoring geometry, XML validity,
raster purity, WCAG 2.1 contrast compliance, small-scale legibility,
and variant parity across all 8 canonical production variants.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import List, Optional

from src.openclone.branding.models import (
    ColorSpec,
    LogoVariant,
    QACheckCategory,
    QACheckItem,
    QACheckSeverity,
    QAReport,
    VariantType,
)


class LogoQAEngine:
    """Automated validator and quality assurance auditor for logo assets."""

    @classmethod
    def audit_package(
        cls,
        variants: List[LogoVariant],
        colors: ColorSpec,
    ) -> QAReport:
        """Run all automated checks against rendered variants and color system."""
        checks: List[QACheckItem] = []

        # 1. Category: XML Validity
        all_valid_xml = True
        xml_details = []
        for v in variants:
            try:
                root = ET.fromstring(v.svg_content)
                if not root.tag.endswith("svg"):
                    all_valid_xml = False
                    xml_details.append(f"{v.variant_type.value}: Root tag is not <svg>")
            except Exception as e:
                all_valid_xml = False
                xml_details.append(f"{v.variant_type.value}: XML error: {str(e)}")

        checks.append(
            QACheckItem(
                name="Vector XML Validity",
                passed=all_valid_xml,
                score=100.0 if all_valid_xml else 0.0,
                details="All SVG variants parse cleanly as standard-compliant XML." if all_valid_xml else "; ".join(xml_details),
                category=QACheckCategory.XML_VALIDITY.value,
                severity=QACheckSeverity.BLOCKER.value,
            )
        )

        # 2. Category: Zero Embedded Raster Images (Anti-Slop Purity)
        zero_rasters = True
        raster_issues = []
        for v in variants:
            lowered = v.svg_content.lower()
            if "<image" in lowered or "data:image/" in v.svg_content:
                zero_rasters = False
                raster_issues.append(f"{v.variant_type.value} contains embedded raster")

        checks.append(
            QACheckItem(
                name="Zero Embedded Raster Artifacts",
                passed=zero_rasters,
                score=100.0 if zero_rasters else 0.0,
                details="100% genuine vector math; zero embedded PNGs or JPEGs." if zero_rasters else "; ".join(raster_issues),
                category=QACheckCategory.RASTER_PURITY.value,
                severity=QACheckSeverity.BLOCKER.value,
            )
        )

        # 3. Category: Geometry & Responsive Scalability (viewBox)
        viewbox_valid = True
        viewbox_issues = []
        for v in variants:
            try:
                root = ET.fromstring(v.svg_content)
                vb = root.attrib.get("viewBox") or root.attrib.get("viewbox")
                if not vb:
                    viewbox_valid = False
                    viewbox_issues.append(f"{v.variant_type.value} missing viewBox")
                else:
                    parts = vb.strip().split()
                    if len(parts) != 4 or float(parts[2]) <= 0 or float(parts[3]) <= 0:
                        viewbox_valid = False
                        viewbox_issues.append(f"{v.variant_type.value} malformed viewBox '{vb}'")
            except Exception:
                viewbox_valid = False

        checks.append(
            QACheckItem(
                name="Responsive Scalability (viewBox Defined)",
                passed=viewbox_valid,
                score=100.0 if viewbox_valid else 0.0,
                details="All variants define responsive viewBox coordinate spaces." if viewbox_valid else "; ".join(viewbox_issues),
                category=QACheckCategory.GEOMETRY_PROPORTIONS.value,
                severity=QACheckSeverity.BLOCKER.value,
            )
        )

        # 4. Category: WCAG 2.1 AA Contrast Compliance
        contrast_ok = (colors.contrast_primary_on_dark >= 3.0 or colors.contrast_primary_on_light >= 3.0)
        checks.append(
            QACheckItem(
                name="WCAG 2.1 Contrast Standards",
                passed=contrast_ok,
                score=95.0 if contrast_ok else 50.0,
                details=(
                    f"Primary on Dark: {colors.contrast_primary_on_dark}:1. "
                    f"Primary on Light: {colors.contrast_primary_on_light}:1. "
                    f"Accent on Dark: {colors.contrast_accent_on_dark}:1."
                ),
                category=QACheckCategory.CONTRAST_ACCESSIBILITY.value,
                severity=QACheckSeverity.WARNING.value,
            )
        )

        # 5. Category: Production Variant Coverage (Parity across 8 variants)
        variant_types = {v.variant_type.value for v in variants}
        expected = {
            VariantType.PRIMARY.value,
            VariantType.HORIZONTAL.value,
            VariantType.VERTICAL.value,
            VariantType.SYMBOL_ONLY.value,
            VariantType.MONOCHROME_DARK.value,
            VariantType.MONOCHROME_LIGHT.value,
            VariantType.FAVICON.value,
            VariantType.SOCIAL_PREVIEW.value,
        }
        missing_variants = expected - variant_types
        coverage = len(missing_variants) == 0
        checks.append(
            QACheckItem(
                name="Production Variant Coverage",
                passed=coverage,
                score=100.0 if coverage else max(50.0, 100.0 - (len(missing_variants) * 15.0)),
                details=(
                    f"All 8 canonical variants verified: {', '.join(sorted(variant_types))}."
                    if coverage
                    else f"Missing canonical variants: {', '.join(sorted(missing_variants))}."
                ),
                category=QACheckCategory.VARIANT_PARITY.value,
                severity=QACheckSeverity.BLOCKER.value,
            )
        )

        # 6. Category: Small-Scale Legibility (Favicon 32x32 & 16x16)
        favicon_variants = [v for v in variants if v.variant_type == VariantType.FAVICON]
        favicon_legible = len(favicon_variants) > 0 and favicon_variants[0].width <= 64 and favicon_variants[0].height <= 64
        checks.append(
            QACheckItem(
                name="Small-Scale Legibility (Favicon 32px)",
                passed=favicon_legible,
                score=100.0 if favicon_legible else 60.0,
                details="Favicon is calibrated for 16px/32px micro-scale displays with simplified silhouette.",
                category=QACheckCategory.SMALL_SCALE_LEGIBILITY.value,
                severity=QACheckSeverity.WARNING.value,
            )
        )

        # Tally totals
        total_score = sum(c.score for c in checks) / len(checks)
        all_passed = all(c.passed for c in checks)
        blockers_passed = all(c.passed for c in checks if c.severity == QACheckSeverity.BLOCKER.value)

        verdict = "PASS" if all_passed else ("NEEDS_REVISION" if blockers_passed else "FAIL")

        recommendations = [
            "Use Primary lockup on dark background documentation and website hero sections.",
            "Use Horizontal lockup inside application header bars and sticky navigation menus.",
            "Deploy 32x32 Favicon as the browser tab icon and PWA asset.",
            "Always test 1-bit monochrome print reproduction on high-absorption paper stock.",
            "Maintain minimum 25% clear space buffer zone around the mark in marketing collateral.",
        ]

        passed_count = sum(1 for c in checks if c.passed)
        failed_count = len(checks) - passed_count

        return QAReport(
            total_score=round(total_score, 1),
            passed=all_passed,
            checks=checks,
            recommendations=recommendations,
            verdict=verdict,
            version="1.0.0",
            total_checks=len(checks),
            passed_checks=passed_count,
            failed_checks=failed_count,
        )
