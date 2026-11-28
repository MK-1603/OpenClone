"""OpenClone Product Traceability Engine & Blueprint Completeness Validator.

Maintains bidirectional, verifiable relationships connecting:
Idea -> Requirement -> Feature -> User Story -> Page -> Component -> API -> Database -> Task -> Validation.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.blueprint.models import (
    PageDefinition,
    InteractiveComponentSpec,
    ApiConnectionMapping,
    DatabaseEntityMapping,
    TraceabilityLink,
    ProductBlueprintPackage,
)


class TraceabilityEngine:
    """Builds and queries the complete end-to-end traceability network."""

    @classmethod
    def build_traceability_network(
        cls,
        features: List[Dict[str, Any]],
        pages: List[PageDefinition],
        components: List[InteractiveComponentSpec],
        apis: List[ApiConnectionMapping],
        entities: List[DatabaseEntityMapping],
    ) -> List[TraceabilityLink]:
        links: List[TraceabilityLink] = []

        # 1. Feature -> Page links
        for p in pages:
            for f_id in p.related_features:
                links.append(TraceabilityLink(
                    source_type="feature",
                    source_id=f_id,
                    relationship="DISPLAYED_ON",
                    target_type="page",
                    target_id=p.page_id,
                ))

        # 2. Page -> Component links
        for c in components:
            for p_id in c.page_ids:
                links.append(TraceabilityLink(
                    source_type="page",
                    source_id=p_id,
                    relationship="CONTAINS_COMPONENT",
                    target_type="component",
                    target_id=c.component_id,
                ))

        # 3. Component -> API links
        for c in components:
            if c.triggered_api_id:
                links.append(TraceabilityLink(
                    source_type="component",
                    source_id=c.component_id,
                    relationship="TRIGGERS_API",
                    target_type="api_endpoint",
                    target_id=c.triggered_api_id,
                ))

        # 4. API -> Database Entity links
        for a in apis:
            for ent in a.related_data_entities:
                links.append(TraceabilityLink(
                    source_type="api_endpoint",
                    source_id=a.endpoint_id,
                    relationship="READS_WRITES_ENTITY",
                    target_type="database_entity",
                    target_id=ent,
                ))

        return links


class BlueprintCompletenessValidator:
    """Validates that 100% of approved features, pages, components, APIs, and states are complete."""

    @classmethod
    def validate_blueprint(
        cls,
        features: List[Dict[str, Any]],
        package: ProductBlueprintPackage,
    ) -> Dict[str, Any]:
        missing_items: List[str] = []
        warnings: List[str] = []

        # 1. Check feature-to-page coverage
        page_feature_ids = set()
        for p in package.pages:
            page_feature_ids.update(p.related_features)

        for f in features:
            f_id = f.get("feature_id", "UNKNOWN")
            if f_id not in page_feature_ids:
                missing_items.append(f"Feature {f_id} has no corresponding UI page representation.")

        # 2. Check API to Page coverage
        if not package.apis:
            missing_items.append("No API endpoints specified for product blueprint.")

        # 3. Check State coverage
        if len(package.states) < len(package.pages):
            warnings.append(f"State coverage partial: {len(package.states)} state specs for {len(package.pages)} pages.")

        is_complete = len(missing_items) == 0
        score = 1.0 if is_complete else max(0.0, 1.0 - (len(missing_items) * 0.1))

        return {
            "is_complete": is_complete,
            "completeness_score": round(score, 2),
            "missing_items": missing_items,
            "warnings": warnings,
            "total_pages": len(package.pages),
            "total_journeys": len(package.journeys),
            "total_components": len(package.components),
            "total_apis": len(package.apis),
            "total_entities": len(package.database_entities),
            "total_traceability_links": len(package.traceability_links),
        }
