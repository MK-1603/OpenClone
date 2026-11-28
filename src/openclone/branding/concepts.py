"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Concept Engine.

Generates distinct, production-grade conceptual identity proposals
across canonical mark categories with quantitative multi-factor scoring
and deterministic selection policies.
"""

from __future__ import annotations

from typing import List, Optional

from src.openclone.branding.models import (
    BrandBrief,
    BrandStrategy,
    ConceptScore,
    ConceptSelectionPolicy,
    LogoCategory,
    LogoConcept,
)


class LogoConceptEngine:
    """Generates and evaluates distinct brand logo concepts with architectural rationale."""

    @classmethod
    def score_concept(
        cls,
        concept: LogoConcept,
        brief: BrandBrief,
        strategy: BrandStrategy,
    ) -> ConceptScore:
        """Calculate quantitative multi-factor score for a concept proposal."""
        # 1. Category Relevance (0 - 100)
        if concept.category in strategy.recommended_categories:
            cat_relevance = 95.0
        elif concept.category in (LogoCategory.COMBINATION_MARK, LogoCategory.GEOMETRIC_MARK):
            cat_relevance = 88.0
        else:
            cat_relevance = 80.0

        # Adjust for domain traits
        traits_lower = [t.lower() for t in brief.personality_traits]
        if concept.category == LogoCategory.GEOMETRIC_MARK and any("precision" in t or "minimal" in t for t in traits_lower):
            cat_relevance = min(100.0, cat_relevance + 5.0)
        elif concept.category == LogoCategory.EMBLEM and any("authority" in t or "security" in t or "rigor" in t for t in traits_lower):
            cat_relevance = min(100.0, cat_relevance + 5.0)

        # 2. Scalability Score (0 - 100)
        # Geometric and combination marks scale exceptionally from 16px to 4K
        if concept.category == LogoCategory.GEOMETRIC_MARK:
            scalability = 96.0
        elif concept.category == LogoCategory.COMBINATION_MARK:
            scalability = 92.0
        elif concept.category == LogoCategory.WORDMARK:
            scalability = 90.0
        elif concept.category == LogoCategory.EMBLEM:
            scalability = 82.0  # Emblems have dense concentric detail
        else:
            scalability = 85.0

        # 3. Complexity / Clarity Score (0 - 100, where higher = cleaner, less cluttered)
        if concept.category == LogoCategory.GEOMETRIC_MARK:
            complexity = 94.0
        elif concept.category == LogoCategory.COMBINATION_MARK:
            complexity = 88.0
        elif concept.category == LogoCategory.EMBLEM:
            complexity = 80.0
        else:
            complexity = 85.0

        # 4. Distinctiveness Score (0 - 100)
        if concept.category == LogoCategory.COMBINATION_MARK:
            distinctiveness = 93.0
        elif concept.category == LogoCategory.EMBLEM:
            distinctiveness = 91.0
        elif concept.category == LogoCategory.GEOMETRIC_MARK:
            distinctiveness = 89.0
        else:
            distinctiveness = 85.0

        # Weighted Composite Score
        composite = (
            (cat_relevance * 0.35)
            + (scalability * 0.25)
            + (complexity * 0.20)
            + (distinctiveness * 0.20)
        )
        composite = round(composite, 2)

        rationale = (
            f"Concept scored {composite}/100. Category fit: {cat_relevance:.0f}%, "
            f"Scalability: {scalability:.0f}%, Simplicity: {complexity:.0f}%, "
            f"Distinctiveness: {distinctiveness:.0f}%."
        )

        return ConceptScore(
            concept_id=concept.concept_id,
            category_relevance=cat_relevance,
            scalability_score=scalability,
            complexity_score=complexity,
            distinctiveness_score=distinctiveness,
            composite_score=composite,
            rationale=rationale,
        )

    @classmethod
    def generate_concepts(
        cls,
        brief: BrandBrief,
        strategy: BrandStrategy,
    ) -> List[LogoConcept]:
        """Generate 3 distinct, non-superficial logo concepts based on strategy."""
        name = brief.brand_name
        initials = "".join([part[0] for part in name.split() if part])[:2].upper()
        if not initials:
            initials = name[:2].upper()

        concepts: List[LogoConcept] = [
            # Concept 1: Combination Mark (Hexagonal Engineering Prism)
            LogoConcept(
                concept_id="CONCEPT-01-PRISM",
                category=LogoCategory.COMBINATION_MARK,
                name="Architectural Hexagon Prism & Code Glyph",
                design_intention=(
                    "Combines an isometric 3D hexagonal framework with an embedded code glyph `</>`, "
                    "signifying foundational software architecture and deterministic control."
                ),
                brand_meaning=(
                    "The outer hexagon symbolizes structural stability and systemic containment; "
                    "the inner code terminal represents developer-first execution and technical clarity."
                ),
                symbol_construction=(
                    "Constructed on an isometric 30-degree isometric grid with 6 symmetric vertices, "
                    "utilizing golden-ratio width facets and optical negative-space carveouts."
                ),
                typography_direction="Modern geometric sans-serif logotype with tight, authoritative kerning.",
                color_direction="Deep cosmic navy (#0B0F19), cobalt blue (#2563EB), and cyber cyan (#38BDF8).",
                strengths=[
                    "Immediately recognizable as an engineering and developer platform.",
                    "Scales seamlessly down to 16px favicon and up to building signage.",
                    "Strong visual weight and brand authority.",
                ],
                limitations=[
                    "Isometric facets require careful rendering in pure flat monochrome print.",
                ],
            ),
            # Concept 2: Geometric Mark (Convergent Monogram)
            LogoConcept(
                concept_id="CONCEPT-02-MONOGRAM",
                category=LogoCategory.GEOMETRIC_MARK,
                name="Convergent Vector Monogram",
                design_intention=(
                    f"A minimalist geometric monogram '{initials}' composed of intersecting structural planes, "
                    "representing multi-agent convergence governed by one engineering baseline."
                ),
                brand_meaning=(
                    "The intersecting paths represent diverse AI models and host IDEs funneling "
                    "into a single, unified pipeline of verifiable software quality."
                ),
                symbol_construction=(
                    "Constructed on a strict 8x8 orthogonal coordinate grid with 45-degree chamfers "
                    "and equalized stroke weights."
                ),
                typography_direction="Neo-grotesque logotype with high x-height and neutral Swiss precision.",
                color_direction="Graphite black (#111827), pure white (#FFFFFF), and precision emerald (#10B981).",
                strengths=[
                    "Ultra-clean, modern tech minimalism with exceptional legibility.",
                    "100% vector-native and flawless single-color reproduction.",
                ],
                limitations=[
                    "Less evocative of code syntax; relies on typography to establish category context.",
                ],
            ),
            # Concept 3: Emblem (Engineering Crest & Seal of Quality)
            LogoConcept(
                concept_id="CONCEPT-03-CREST",
                category=LogoCategory.EMBLEM,
                name="Deterministic Engineering Seal",
                design_intention=(
                    "An enclosed circular emblem featuring concentric verification rings and an "
                    "architectural node core, conveying certification and zero-slop governance."
                ),
                brand_meaning=(
                    "Conveys an institutional standard of software engineering, functioning as a "
                    "tamper-proof seal of approval for enterprise-grade AI software."
                ),
                symbol_construction=(
                    "Concentric Fibonacci circles with 12 radial tick markers denoting lifecycle gates."
                ),
                typography_direction="Upper-case tracking logotype with tabular numbers and monospaced accents.",
                color_direction="Titanium dark grey (#1F2937), platinum silver (#E5E7EB), and amber (#F59E0B).",
                strengths=[
                    "Conveys institutional trustworthiness, compliance, and enterprise permanence.",
                    "Excellent for badge, cert, and security stamp applications.",
                ],
                limitations=[
                    "Higher complexity at micro-resolutions (under 24px) requires symbol simplification.",
                ],
            ),
        ]

        # Score and rank all concepts
        for c in concepts:
            c.score = cls.score_concept(c, brief, strategy)

        # Sort by composite score descending
        sorted_concepts = sorted(concepts, key=lambda x: x.score.composite_score if x.score else 0.0, reverse=True)
        for rank, c in enumerate(sorted_concepts, start=1):
            c.selection_rank = rank

        return concepts

    @classmethod
    def select_concept(
        cls,
        concepts: List[LogoConcept],
        policy: ConceptSelectionPolicy = ConceptSelectionPolicy.HIGHEST_SCORE,
        preferred_category: Optional[LogoCategory] = None,
        manual_concept_id: Optional[str] = None,
    ) -> LogoConcept:
        """Select a single concept according to the designated policy."""
        if not concepts:
            raise ValueError("Cannot select from an empty list of logo concepts.")

        chosen: Optional[LogoConcept] = None

        if policy == ConceptSelectionPolicy.MANUAL_OVERRIDE and manual_concept_id:
            for c in concepts:
                if c.concept_id == manual_concept_id:
                    chosen = c
                    break

        elif policy == ConceptSelectionPolicy.CATEGORY_PREFERENCE and preferred_category:
            for c in concepts:
                if c.category == preferred_category:
                    chosen = c
                    break

        elif policy == ConceptSelectionPolicy.HIGHEST_SCORE:
            chosen = max(concepts, key=lambda x: x.score.composite_score if x.score else 0.0)

        # Default fallback: highest score or first concept
        if not chosen:
            chosen = sorted(concepts, key=lambda x: x.score.composite_score if x.score else 0.0, reverse=True)[0]

        for c in concepts:
            c.is_selected = (c.concept_id == chosen.concept_id)

        return chosen
