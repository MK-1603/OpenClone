"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Concept Engine.

Generates distinct, production-grade conceptual identity proposals
across canonical mark categories with clear design intentions and trade-offs.
"""

from __future__ import annotations

from typing import List

from src.openclone.branding.models import BrandBrief, BrandStrategy, LogoCategory, LogoConcept


class LogoConceptEngine:
    """Generates distinct brand logo concepts with architectural rationale."""

    @classmethod
    def generate_concepts(cls, brief: BrandBrief, strategy: BrandStrategy) -> List[LogoConcept]:
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

        return concepts
