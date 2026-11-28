"""Diagram Generator for OpenClone Reverse Engineering.

Generates Mermaid Entity-Relationship (ER) and C4 Container diagrams from reconstructed
data models, route endpoints, and architectural components.
"""
from __future__ import annotations

import re
from typing import List

from src.openclone.reverse_engineering.models import ApiEndpoint, EntityModel


class DiagramGenerator:
    """Generates deterministic Mermaid diagrams from reverse-engineered architecture models."""

    @staticmethod
    def sanitize_identifier(name: str) -> str:
        """Sanitize an entity or table name for Mermaid syntax."""
        clean = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        return clean.upper()

    @classmethod
    def generate_er_diagram(cls, entities: List[EntityModel]) -> str:
        """Generate a valid Mermaid erDiagram from discovered entity models and foreign keys."""
        if not entities:
            return "erDiagram\n    SYSTEM_EMPTY {\n        string status \"No entities discovered\"\n    }"

        lines = ["erDiagram"]
        seen_relations = set()

        # 1. Output relationships
        for ent in entities:
            src_name = cls.sanitize_identifier(ent.name)
            for fk in ent.foreign_keys:
                tgt = fk.get("target_table")
                if tgt:
                    tgt_name = cls.sanitize_identifier(tgt)
                    rel_key = f"{src_name}_{tgt_name}"
                    if rel_key not in seen_relations:
                        col = fk.get("column", "relates_to")
                        lines.append(f"    {tgt_name} ||--o{{ {src_name} : \"{col}\"")
                        seen_relations.add(rel_key)

        # 2. Output entity attributes
        for ent in entities:
            ent_name = cls.sanitize_identifier(ent.name)
            lines.append(f"    {ent_name} {{")
            if ent.primary_key:
                lines.append(f"        string {ent.primary_key} PK")
            for col in ent.columns:
                if col != ent.primary_key:
                    clean_col = re.sub(r"[^a-zA-Z0-9_]", "_", col)
                    lines.append(f"        string {clean_col}")
            if not ent.columns and not ent.primary_key:
                lines.append("        string id PK")
            lines.append("    }")

        return "\n".join(lines)

    @classmethod
    def generate_c4_diagram(
        cls,
        project_name: str,
        endpoints: List[ApiEndpoint],
        entities: List[EntityModel],
        pattern: str = "Layered Architecture",
    ) -> str:
        """Generate a Mermaid C4 Container diagram from endpoints and entities."""
        clean_proj = re.sub(r"[^a-zA-Z0-9_]", "_", project_name)
        lines = [
            "C4Context",
            f"    title System Architecture Diagram for {project_name}",
            f"    Enterprise_Boundary(b0, \"{project_name} Boundary\") {{",
            f"        System(client, \"Client / Consumer\", \"Web Browser or External Service\")",
            f"        System(api, \"Application Service\", \"Pattern: {pattern}. Exposes {len(endpoints)} endpoints.\")",
            f"        SystemDb(db, \"Database & Storage\", \"Stores {len(entities)} persistent entities.\")",
            "    }",
            "    Rel(client, api, \"Uses / Calls\", \"HTTP / REST / JSON\")",
            "    Rel(api, db, \"Reads / Writes\", \"SQL / ORM\")",
        ]
        return "\n".join(lines)
