# PROJECT.md — NoteDigest (OpenClone Governed AI SaaS)

> **Document status:** APPROVED  
> **Project ID:** `NOTEDIGEST-001`  
> **Project name:** `NoteDigest`  
> **Project type:** `AI_PRODUCTIVITY_SAAS`  
> **Owner / maintainer:** `MK-1603`  
> **Governance Standard:** `OpenClone v2.0 (AISDF)`  
> **License:** `MIT`

---

## 1. Executive Summary

NoteDigest is a lightweight, high-performance meeting and text summarization utility governed by the OpenClone software engineering platform. It transforms raw, unstructured transcripts, emails, and notes into structured executive digests featuring categorized decisions, assigned action items with deadlines, open questions, and discussion topics.

---

## 2. Problem Statement

### 2.1 The Problem
Engineers, students, and project managers frequently capture unstructured text during meetings, calls, and group chats. Locating critical decisions and assigned deliverables requires re-reading long transcripts, leading to missed deadlines and unclear accountability.

### 2.2 Target Users
- **Software Engineers & Team Leads:** Extracting action items and architecture decisions from technical design syncs.
- **Project Shepherds & Scrum Masters:** Translating meeting logs into backlog work items.
- **Solo Builders:** Generating structured records of brainstorms and research notes.

### 2.3 Proposed Solution
A deterministic, rule-assisted extraction engine that parses text without hallucinations, structures action items with clear ownership and deadlines, and outputs clean, publication-ready Markdown and JSON.

---

## 3. Scope Boundaries & Non-Goals

### In Scope
- Pure Python deterministic pattern & rule-based text extraction engine.
- Structured data models (`DigestResult`, `ActionItem`, `Decision`, `KeyPoint`).
- Publication-quality Markdown report generation.
- JSON output serialization for programmatic API integration.
- CLI interface (`python -m notedigest.cli`).
- OpenClone LEBIS-engineered vector brand identity and assets.
- Comprehensive unit test suite with 100% pass rate.

### Out of Scope (Non-Goals)
- Audio transcription or voice bot recording (focuses exclusively on post-transcript text).
- Direct third-party SaaS API connectors (Slack, Jira, Asana) in Phase 1.
- Cloud hosting infrastructure or multi-tenant database clusters.

---

## 4. Architecture & Technical Specification

```
NoteDigest Architecture
=======================
Input Text / Transcript
        ↓
  NoteExtractor (Pattern & Rule Analysis)
        ├── Action Items & Deadlines (@Owner, TODO, [ ])
        ├── Key Decisions (DECIDED, Agreed)
        ├── Open Questions (?)
        └── Discussion Key Points
        ↓
 NoteDigestEngine (Synthesis & Structuring)
        ↓
Output Interfaces:
  ├── Markdown Report (GitHub Flavored MD)
  ├── JSON Payload
  └── CLI Console Output
```

- **Runtime:** Python 3.10+ (Standard Library first: `re`, `dataclasses`, `json`, `argparse`).
- **Zero Heavy Dependencies:** Runs anywhere with standard Python without requiring external packages.
- **Brand Identity:** Engineered via OpenClone LEBIS (Royal Blue `#2563EB`, SVG mark & lockups).

---

## 5. Verification & Governance Evidence

- **Unit Tests:** `tests/test_digest.py` (6 passing tests, 0 failures).
- **Execution DAG:** Governed by OpenClone `tasks.json` (DESIGN → BUILD → VERIFY).
- **Audit Ledger:** Cryptographic tamper-evident SQLite ledger tracking approvals and transitions.
- **Status:** `IMPLEMENTED_VERIFIED`.
