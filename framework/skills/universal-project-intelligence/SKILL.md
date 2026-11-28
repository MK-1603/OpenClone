---
name: universal-project-intelligence
description: Analyzes project ideas, PRDs, or codebases; performs multi-label classification across 14 engineering disciplines (ENG-01 to ENG-14); evaluates technology alternatives; and generates complete governed project packages.
version: 2.0.0
---

# Universal Project Intelligence Skill

## Purpose
Enables coding agents to understand natural-language project requests, extract requirements, classify project archetypes, assemble minimum effective workforce teams, evaluate technology stacks, and generate complete 8-layer governed project specifications.

## Applicable Disciplines
- ENG-01 Artificial Intelligence
- ENG-02 Machine Learning
- ENG-03 Data Science & Data Engineering
- ENG-04 AI Model Engineering
- ENG-05 Software Application Engineering
- ENG-06 Backend & API Engineering
- ENG-07 Enterprise Software Engineering
- ENG-08 SaaS & Cloud Service Engineering
- ENG-09 DevOps & Cloud Engineering
- ENG-10 Automation & Integration Engineering
- ENG-11 Cybersecurity Engineering
- ENG-12 Specialized Technology Engineering
- ENG-13 Software Quality Engineering
- ENG-14 UI/UX & Product Engineering

## Workflow Procedure
1. **Understand & Classify:** Run `python -m src.openclone.cli intelligence classify "<prompt>"` or use MCP tool `openclone_classify_project`.
2. **Evaluate Technology:** Run `python -m src.openclone.cli intelligence tech-eval "<prompt>"` or use MCP tool `openclone_evaluate_technology`.
3. **Route Governance & Workforce:** Compute deterministic domain activation and minimum effective workforce via `openclone_route_project`.
4. **Generate Project Package:** Run `python -m src.openclone.cli intelligence generate "<prompt>" --out <dir>` or use MCP tool `openclone_generate_package`.
5. **Human Approval:** Inspect generated `PROJECT.md` and obtain human owner approval before initiating code implementation.
