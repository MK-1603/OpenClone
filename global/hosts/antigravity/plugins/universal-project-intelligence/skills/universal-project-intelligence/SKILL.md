---
name: universal-project-intelligence
description: Classify any software project across 12 canonical project families, route requirements to engineering domains, compose specialist teams, and select MIE model intelligence.
---

# Universal Project Intelligence Skill

## Purpose
Guide the AI agent during the project intake and planning phase to understand the complete architectural nature of any software system before code generation begins.

## Operating Flow
1. **Intake & Multi-Label Classification:**
   - Call `openclone_classify_project` with project requirements or inspect repository manifests.
   - Determine primary family/type, secondary types, supporting types, delivery targets, and independent complexity.
2. **Domain & Capability Routing:**
   - Call `openclone_route_project` to map classification to canonical domains (`00-GOVERNANCE` to `30-AGENT-RULES-AND-VERIFICATION`) and capability engines (`E-001` to `E-056`).
3. **Workforce Assembly:**
   - Review minimum effective team composition.
   - Note native agents, external specialists, IDE agents, and human fallback boundaries.
4. **Blueprint Guidance:**
   - Call `openclone_get_blueprint` to fetch canonical guidelines for the detected project family.
5. **PROJECT.md Authoring:**
   - Populate canonical `PROJECT.md` with multi-label metadata and conditional domain profiles.
   - Stop for human approval before code implementation.
