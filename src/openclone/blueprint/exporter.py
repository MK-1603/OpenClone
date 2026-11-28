"""OpenClone Universal Product Blueprint Exporter & Manifest Compiler.

Compiles the complete consolidated Product Blueprint bundle containing:
- Information architecture sitemap
- Complete page inventory & wireframe specs
- Component interaction contracts
- API & database integration maps
- Application states, responsive, and accessibility checklists
- Complete traceability network
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from src.openclone.blueprint.models import ProductBlueprintPackage


class ProductBlueprintExporter:
    """Exports consolidated JSON and Markdown blueprint bundles."""

    @classmethod
    def export_blueprint(cls, package: ProductBlueprintPackage) -> Dict[str, Any]:
        # Compile Sitemap Markdown
        sitemap_md = f"""# {package.project_name} — Product Information Architecture & Sitemap
**Version:** {package.version}  
**Status:** {package.validation_status}  
**Completeness Score:** {package.completeness_score * 100}%  

---

## 1. Application Page Inventory ({len(package.pages)} Pages)
"""
        for p in package.pages:
            sitemap_md += f"### `{p.slug}` — {p.title} (`{p.category.value}`)\n"
            sitemap_md += f"- **Purpose:** {p.purpose}\n"
            sitemap_md += f"- **Layout:** `{p.layout.value}` | **Roles:** {', '.join(p.user_roles)}\n"
            sitemap_md += f"- **Components:** {', '.join(p.required_components)}\n"
            if p.api_dependencies:
                sitemap_md += f"- **API Endpoints:** {', '.join(p.api_dependencies)}\n"
            sitemap_md += "\n"

        sitemap_md += f"""
---

## 2. User Journeys ({len(package.journeys)} Key Pathways)
"""
        for j in package.journeys:
            sitemap_md += f"### {j.title} (Actor: `{j.actor_role}`)\n"
            sitemap_md += f"- **Goal:** {j.goal}\n"
            for step in j.steps:
                sitemap_md += f"  {step.order}. **{step.user_action}** $\\rightarrow$ *{step.system_response}* (`{step.target_page_id}`)\n"
            sitemap_md += "\n"

        manifest = {
            "blueprint_id": package.blueprint_id,
            "project_id": package.project_id,
            "project_name": package.project_name,
            "version": package.version,
            "created_at": package.created_at,
            "validation_status": package.validation_status,
            "completeness_score": package.completeness_score,
            "summary": {
                "page_count": len(package.pages),
                "journey_count": len(package.journeys),
                "component_count": len(package.components),
                "api_count": len(package.apis),
                "database_entity_count": len(package.database_entities),
                "traceability_link_count": len(package.traceability_links),
            },
            "files": {
                "sitemap.md": sitemap_md,
                "page-inventory.json": json.dumps([p.__dict__ for p in package.pages], indent=2, default=str),
                "user-journeys.json": json.dumps([j.__dict__ for j in package.journeys], indent=2, default=str),
                "component-interactions.json": json.dumps([c.__dict__ for c in package.components], indent=2, default=str),
                "api-contracts.json": json.dumps([a.__dict__ for a in package.apis], indent=2, default=str),
                "database-schema.json": json.dumps([d.__dict__ for d in package.database_entities], indent=2, default=str),
                "application-states.json": json.dumps([s.__dict__ for s in package.states], indent=2, default=str),
                "traceability-matrix.json": json.dumps([t.__dict__ for t in package.traceability_links], indent=2, default=str),
            },
        }

        return manifest
