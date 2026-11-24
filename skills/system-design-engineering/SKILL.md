---
id: system-design-engineering
name: System Design & Capacity Engineering
version: 1.0.0
description: End-to-end system design fundamentals, capacity estimation, C4 architecture diagrams, trade-off analysis, and 20 real-world system design case studies.
precedence: 30
category: architecture
triggers:
  - "system design"
  - "capacity estimation"
  - "back-of-the-envelope"
  - "architecture trade-offs"
  - "c4 diagram"
  - "scalability architecture"
  - "system architecture"
negative_triggers:
  - "css styling"
  - "font size"
pre_build_gates:
  - "Verify functional and non-functional requirements with explicit SLA/SLO boundaries."
  - "Calculate back-of-the-envelope capacity (RPS, storage, bandwidth, cache RAM, workers)."
  - "Validate Monolith-First Rule before introducing distributed microservices."
finish_gates:
  - "Produce formal Architecture Decision Record (ADR) with revisit triggers."
  - "Generate valid Mermaid C4 Context, Container, Component, or Sequence diagrams."
  - "Verify failure modes, single points of failure (SPOF), and disaster recovery plans."
maturity: L4_TESTED
---

# System Design & Capacity Engineering

## 1. Overview
The `system-design-engineering` skill governs system-level architecture analysis, back-of-the-envelope capacity calculations, scalability evaluation, and formal ADR generation.

## 2. Core Pillars
1. **Requirements & Quality Attributes:** Explicitly decouple functional requirements from non-functional quality attributes (Availability, Latency, Durability, Scalability, Cost).
2. **Back-of-the-Envelope Calculations:** Deterministically calculate RPS, peak surge (3x multiplier), storage growth, network bandwidth, and Pareto 80/20 cache sizing.
3. **Monolith-First Rule:** Start with a Modular Monolith. Microservices require measurable write scale (>10k WPS) or independent organizational bounded contexts.
4. **C4 Modeling:** Document architecture across Context, Container, Component, and Deployment perspectives.
5. **Real-World Case Studies:** Reference OpenClone's 20 production case studies (`CS-01` to `CS-20`).

## 3. Implementation Engine
- `src/openclone/system_design/capacity.py` (`CapacityEstimator`)
- `src/openclone/system_design/decision_engine.py` (`SystemDesignDecisionEngine`, `ADRGenerator`)
- `src/openclone/system_design/case_studies.py` (`SystemDesignCatalogue`)
- `src/openclone/system_design/diagrams.py` (`SystemDiagramGenerator`)
