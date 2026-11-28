"""OpenClone Project Identity Orchestrator.

Orchestrates the entire Project Identity & Asset Generation System (PIAGS)
integrating naming, brand strategy, visual systems, vector logos, metadata,
asset registration, validation, approval, and package export.
"""
from __future__ import annotations

import hashlib
import time
import uuid
from typing import Any, Dict, List, Optional

from src.openclone.identity.models import (
    AssetDescriptor,
    BrandIdentity,
    IdentityApprovalRecord,
    IdentityLifecycleState,
    NameCandidate,
    ProjectMetadataRecord,
    VisualIdentitySystem,
)
from src.openclone.identity.naming import ProjectNamingEngine
from src.openclone.identity.brand import BrandIntelligenceEngine
from src.openclone.identity.visual import VisualIdentityBuilder
from src.openclone.identity.logo import LogoGenerationEngine
from src.openclone.identity.registry import AssetRegistry
from src.openclone.identity.exporter import IdentityValidationEngine, IdentityPackageExporter


class ProjectIdentityOrchestrator:
    """Master coordinator of project branding, naming, visual identity, and asset export."""

    def __init__(self):
        self.registry = AssetRegistry()

    def generate_project_identity(
        self,
        prompt: str,
        project_name: Optional[str] = None,
        category: str = "Developer Platform",
        target_audience: str = "Software Engineers",
        selected_name: Optional[str] = None,
        primary_color: str = "#2563EB",
        secondary_color: str = "#0F172A",
        accent_color: str = "#38BDF8",
        auto_approve: bool = False,
    ) -> Dict[str, Any]:
        """Generate a complete, cohesive, validated project identity suite."""
        project_id = f"proj-{uuid.uuid4().hex[:8]}"

        # 1. Naming Intelligence
        name_candidates = ProjectNamingEngine.generate_candidates(
            prompt=prompt,
            category=category,
            target_audience=target_audience,
        )

        final_name = selected_name or (project_name if project_name and project_name != "OpenCloneProject" else name_candidates[0].name)
        slug = final_name.lower().replace(" ", "-")

        # 2. Brand Intelligence
        brand = BrandIntelligenceEngine.create_brand_identity(
            brand_name=final_name,
            category=category,
            target_audience=target_audience,
            purpose=prompt,
        )

        # 3. Visual Identity
        visual = VisualIdentityBuilder.build_visual_system(
            primary_hex=primary_color,
            secondary_hex=secondary_color,
            accent_hex=accent_color,
        )

        # 4. Logo & Supporting Assets
        assets = LogoGenerationEngine.generate_logo_suite(
            project_id=project_id,
            identity_id=brand.brand_id,
            brand_name=final_name,
            visual_system=visual,
        )

        # Register assets
        for a in assets:
            self.registry.register_asset(a)

        # 5. Project Metadata Record
        metadata = ProjectMetadataRecord(
            project_id=project_id,
            project_name=final_name,
            slug=slug,
            short_description=brand.positioning[:140],
            full_description=brand.positioning,
            tagline=brand.tagline,
            project_category=category,
            project_type=category,
            target_audience=target_audience,
            primary_problem=prompt,
            primary_solution=brand.mission,
            key_features=["Intelligent Orchestration", "Deterministic Architecture", "Governed Assets"],
            brand_identity_id=brand.brand_id,
            logo_asset_id=assets[0].asset_id if assets else None,
            primary_color=primary_color,
            secondary_color=secondary_color,
            keywords=[w.lower() for w in final_name.split() if len(w) > 2],
        )

        # 6. Validation
        validation = IdentityValidationEngine.validate_package(
            brand=brand,
            visual=visual,
            metadata=metadata,
            assets=assets,
        )

        # 7. Approval
        approval = IdentityApprovalRecord(
            approval_id=f"appr-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            identity_id=brand.brand_id,
            name_approved=auto_approve,
            brand_approved=auto_approve,
            logo_approved=auto_approve,
            metadata_approved=auto_approve,
            final_package_approved=auto_approve,
            approver_identity="human_user" if auto_approve else "pending",
            approval_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if auto_approve else None,
            approval_digest=hashlib.sha256(f"{final_name}:{brand.brand_id}".encode()).hexdigest() if auto_approve else None,
        )

        if auto_approve:
            brand.status = IdentityLifecycleState.APPROVED
            metadata.status = IdentityLifecycleState.APPROVED
            for a in assets:
                a.is_approved = True

        # 8. Export Package
        package = IdentityPackageExporter.export_package(
            brand=brand,
            visual=visual,
            metadata=metadata,
            assets=assets,
            approval=approval,
        )

        return {
            "status": "APPROVED" if auto_approve else "PENDING_REVIEW",
            "project_id": project_id,
            "project_name": final_name,
            "name_candidates": [c.__dict__ for c in name_candidates],
            "brand": brand.__dict__,
            "visual_system": {
                "identity_id": visual.identity_id,
                "colors": visual.colors.__dict__,
                "typography": visual.typography.__dict__,
                "tokens": visual.design_tokens,
            },
            "metadata": metadata.__dict__,
            "assets": [a.__dict__ for a in assets],
            "validation": validation,
            "approval": approval.__dict__,
            "package": package,
        }
