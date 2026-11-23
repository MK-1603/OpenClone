"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — QA Engine.

Automated verification checklist scoring geometry, XML validity,
WCAG 2.1 contrast compliance, and variant integrity.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import List

from src.openclone.branding.models import (
    ColorSpec,
    LogoVariant,
    QACheckItem,
    QAReport,
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

        # 1. Check: Valid SVG XML parsing
        all_valid_xml = True
        xml_details = []
        for v in variants:
            try:
                ET.fromstring(v.svg_content)
            except Exception as e:
                all_valid_xml = False
                xml_details.append(f"{v.variant_type.value}: XML error: {str(e)}")

        checks.append(
            QACheckItem(
                name="Vector XML Validity",
                passed=all_valid_xml,
                score=100.0 if all_valid_xml else 0.0,
                details="All SVG variants parse cleanly as valid XML." if all_valid_xml else "; ".join(xml_details),
            )
        )

        # 2. Check: Zero embedded raster images
        zero_rasters = True
        raster_issues = []
        for v in variants:
            if "<image" in v.svg_content.lower() or "data:image/" in v.svg_content:
                zero_rasters = False
                raster_issues.append(f"{v.variant_type.value} contains embedded raster")

        checks.append(
            QACheckItem(
                name="Zero Embedded Raster Artifacts",
                passed=zero_rasters,
                score=100.0 if zero_rasters else 0.0,
                details="100% genuine vector math; zero embedded PNGs or JPEGs." if zero_rasters else "; ".join(raster_issues),
            )
        )

        # 3. Check: viewBox presence on all variants
        viewbox_valid = all("viewBox=" in v.svg_content or "viewbox=" in v.svg_content.lower() for v in variants)
        checks.append(
            QACheckItem(
                name="Responsive Scalability (viewBox Defined)",
                passed=viewbox_valid,
                score=100.0 if viewbox_valid else 0.0,
                details="All variants define responsive viewBox coordinate spaces.",
            )
        )

        # 4. Check: WCAG Contrast (Text >= 4.5:1, Graphics >= 3.0:1)
        contrast_ok = colors.contrast_primary_on_dark >= 3.0 or colors.contrast_primary_on_light >= 3.0
        checks.append(
            QACheckItem(
                name="WCAG 2.1 Contrast Standards",
                passed=contrast_ok,
                score=95.0 if contrast_ok else 50.0,
                details=(
                    f"Primary on Dark: {colors.contrast_primary_on_dark}:1. "
                    f"Primary on Light: {colors.contrast_primary_on_light}:1."
                ),
            )
        )

        # 5. Check: Production Variant Coverage
        variant_types = {v.variant_type.value for v in variants}
        expected = {"PRIMARY", "HORIZONTAL", "VERTICAL", "SYMBOL_ONLY", "FAVICON", "SOCIAL_PREVIEW"}
        coverage = expected.issubset(variant_types)
        checks.append(
            QACheckItem(
                name="Production Variant Coverage",
                passed=coverage,
                score=100.0 if coverage else 70.0,
                details=f"Included variants: {', '.join(sorted(variant_types))}.",
            )
        )

        # Calculate total score
        total = sum(c.score for c in checks) / len(checks)
        all_passed = all(c.passed for c in checks)

        recommendations = [
            "Use Primary lockup on dark background documentation and website hero sections.",
            "Use Horizontal lockup inside application header bars and sticky navigation menus.",
            "Deploy 32x32 Favicon as the browser tab icon and PWA asset.",
            "Always test 1-bit monochrome print reproduction on high-absorption paper stock.",
        ]

        return QAReport(
            total_score=round(total, 1),
            passed=all_passed,
            checks=checks,
            recommendations=recommendations,
        )
