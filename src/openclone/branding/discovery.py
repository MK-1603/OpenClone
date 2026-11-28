"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Discovery Engine.

Collects, validates, and evaluates brand briefs; identifies missing
strategic context and explicitly documents assumptions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src.openclone.branding.models import BrandBrief


class BrandDiscoveryEngine:
    """Ingests and validates brand briefs for visual identity engineering."""

    REQUIRED_FIELDS = [
        "brand_name",
        "category",
        "purpose",
        "target_audience",
        "positioning",
    ]

    @classmethod
    def evaluate_brief(cls, raw: Dict[str, Any]) -> Tuple[BrandBrief, List[str], float]:
        """Validate input dictionary, document assumptions for missing info, and return BrandBrief."""
        assumptions: List[str] = []
        missing_fields: List[str] = []

        for field_name in cls.REQUIRED_FIELDS:
            val = raw.get(field_name)
            if not val or not str(val).strip():
                missing_fields.append(field_name)

        if "brand_name" in missing_fields:
            raise ValueError("Brand brief must contain a valid 'brand_name'.")

        # Provide explicit documented assumptions if non-critical parameters are missing
        category = raw.get("category", "Software Engineering Framework")
        if "category" in missing_fields:
            assumptions.append("Category not explicitly stated; assumed 'Software Engineering Framework'.")

        purpose = raw.get("purpose", f"Empower users in {category}.")
        if "purpose" in missing_fields:
            assumptions.append(f"Business purpose inferred from category: '{purpose}'.")

        audience = raw.get("target_audience", "Developers, engineering managers, and technical teams.")
        if "target_audience" in missing_fields:
            assumptions.append("Target audience defaulted to professional software developers and technical leads.")

        positioning = raw.get("positioning", f"Premium, trustworthy, and disciplined {category}.")
        if "positioning" in missing_fields:
            assumptions.append(f"Market positioning defaulted to premium and reliable tier.")

        traits = raw.get("personality_traits") or ["Precision", "Authority", "Modern", "Reliable"]
        if not raw.get("personality_traits"):
            assumptions.append("Personality traits defaulted to: Precision, Authority, Modern, Reliable.")

        values = raw.get("brand_values") or ["Engineering Rigor", "Open Standards", "Zero Fluff", "High Performance"]
        if not raw.get("brand_values"):
            assumptions.append("Brand values defaulted to: Engineering Rigor, Open Standards, Zero Fluff.")

        competitors = raw.get("competitors_and_references", [])
        preferences = raw.get("visual_preferences", ["Geometric", "High Contrast", "Vector Sharpness"])
        restrictions = raw.get("design_restrictions", ["No generic AI purple gradient blobs", "No illegible thin scripts"])
        environments = raw.get("primary_environments", ["web", "mobile", "terminal", "dark-mode-ide"])

        brief = BrandBrief(
            brand_name=raw["brand_name"].strip(),
            category=category.strip(),
            purpose=purpose.strip(),
            target_audience=audience.strip(),
            positioning=positioning.strip(),
            personality_traits=[t.strip() for t in traits],
            brand_values=[v.strip() for v in values],
            competitors_and_references=competitors,
            visual_preferences=preferences,
            design_restrictions=restrictions,
            primary_environments=environments,
        )

        # Completeness calculation
        total_eval_points = 10.0
        points_scored = 10.0 - (len(missing_fields) * 1.5)
        completeness = max(30.0, min(100.0, points_scored * 10.0))

        return brief, assumptions, completeness
