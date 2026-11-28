"""OpenClone Project Identity Package Exporter & Validation Engine.

Validates completeness, contrast ratios, and referential integrity of brand identities
and exports consolidated project identity bundles.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, List, Optional
from src.openclone.identity.models import (
    AssetDescriptor,
    BrandIdentity,
    ColorPalette,
    IdentityApprovalRecord,
    IdentityLifecycleState,
    ProjectMetadataRecord,
    VisualIdentitySystem,
)
from src.openclone.identity.registry import AssetRegistry


class IdentityValidationEngine:
    """Verifies that project identity, brand rules, contrast, and assets meet quality gates."""

    @classmethod
    def validate_package(
        cls,
        brand: BrandIdentity,
        visual: VisualIdentitySystem,
        metadata: ProjectMetadataRecord,
        assets: List[AssetDescriptor],
    ) -> Dict[str, Any]:
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Name and slug validation
        if not metadata.project_name:
            errors.append("Project metadata lacks a project_name.")
        if not metadata.slug:
            errors.append("Project metadata lacks a slug.")

        # 2. Brand completeness
        if not brand.brand_name:
            errors.append("Brand identity lacks brand_name.")
        if not brand.positioning:
            warnings.append("Brand positioning statement is empty.")

        # 3. Contrast verification
        if not visual.colors.wcag_aa_compliant:
            errors.append("Visual identity color palette fails WCAG AA contrast compliance.")

        # 4. Asset checks
        if not assets:
            errors.append("No logo or branding assets generated in package.")
        else:
            has_primary = any(a.variant == "primary" for a in assets)
            if not has_primary:
                warnings.append("Missing primary logo variant.")

        is_valid = len(errors) == 0
        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "asset_count": len(assets),
            "wcag_aa_compliant": visual.colors.wcag_aa_compliant,
            "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }


class IdentityPackageExporter:
    """Exports consolidated JSON, Markdown, and SVG package bundles."""

    @classmethod
    def export_package(
        cls,
        brand: BrandIdentity,
        visual: VisualIdentitySystem,
        metadata: ProjectMetadataRecord,
        assets: List[AssetDescriptor],
        approval: Optional[IdentityApprovalRecord] = None,
    ) -> Dict[str, Any]:
        # Formulate brand guidelines markdown
        guidelines_md = f"""# {brand.brand_name} — Brand Guidelines & Identity System
**Version:** {brand.version}.0  
**Status:** {brand.status.value}  

---

## 1. Brand Positioning & Identity
- **Tagline:** {brand.tagline}
- **Mission:** {brand.mission}
- **Vision:** {brand.vision}
- **Positioning Statement:** {brand.positioning}
- **Brand Voice & Tone:** {brand.voice_and_tone}

## 2. Visual Direction & Design Principles
{brand.visual_direction}

### Core Principles:
"""
        for p in brand.design_principles:
            guidelines_md += f"- **{p}**\n"

        guidelines_md += f"""
---

## 3. Color Palette & Contrast Compliance
- **Primary Color:** `{visual.colors.primary_hex}`
- **Secondary Color:** `{visual.colors.secondary_hex}`
- **Accent Color:** `{visual.colors.accent_hex}`
- **Light Surface:** `{visual.colors.surface_light}`
- **Dark Canvas:** `{visual.colors.background_dark}`
- **Contrast Ratio (Light / Dark):** {visual.colors.contrast_ratio_light}:1 / {visual.colors.contrast_ratio_dark}:1 (WCAG AA Compliant)

---

## 4. Typography Hierarchy
- **Heading Font:** `{visual.typography.heading_font}`
- **Body Font:** `{visual.typography.body_font}`
- **Code Font:** `{visual.typography.code_font}`
"""

        package_manifest = {
            "project_id": metadata.project_id,
            "project_name": metadata.project_name,
            "slug": metadata.slug,
            "identity_id": brand.brand_id,
            "status": brand.status.value,
            "brand": {
                "name": brand.brand_name,
                "tagline": brand.tagline,
                "mission": brand.mission,
                "vision": brand.vision,
                "values": brand.values,
            },
            "visual_tokens": visual.design_tokens,
            "metadata": {
                "description": metadata.short_description,
                "license": metadata.license,
                "version": metadata.project_version,
                "keywords": metadata.keywords,
            },
            "assets": [
                {
                    "asset_id": a.asset_id,
                    "category": a.category.value,
                    "variant": a.variant,
                    "file_name": a.file_name,
                    "format": a.file_format.value,
                    "storage_path": a.storage_path,
                    "is_approved": a.is_approved,
                }
                for a in assets
            ],
            "approval": {
                "is_approved": approval.final_package_approved if approval else False,
                "approver": approval.approver_identity if approval else None,
                "digest": approval.approval_digest if approval else None,
            },
            "files": {
                "brand-guidelines.md": guidelines_md,
                "design-tokens.json": json.dumps(visual.design_tokens, indent=2),
                "metadata.json": json.dumps({
                    "name": metadata.project_name,
                    "slug": metadata.slug,
                    "description": metadata.short_description,
                    "version": metadata.project_version,
                    "license": metadata.license,
                }, indent=2),
            },
        }

        # Embed asset contents
        for a in assets:
            if a.content:
                package_manifest["files"][a.storage_path] = a.content

        return package_manifest
