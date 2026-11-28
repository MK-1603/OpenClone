"""OpenClone Database Migration and Schema Safety Guard.

Analyzes SQL migration scripts before execution, detecting destructive DDL,
table-locking operations, unindexed foreign keys, and missing rollback strategies.
"""
from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import List, Tuple


class MigrationSafetyLevel(str, enum.Enum):
    SAFE = "SAFE"
    WARNING_REQUIRES_REVIEW = "WARNING_REQUIRES_REVIEW"
    DESTRUCTIVE_BLOCKED = "DESTRUCTIVE_BLOCKED"


@dataclass
class MigrationFinding:
    """Security or operational risk detected in a database migration script."""
    finding_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    statement: str
    reason: str
    remediation: str
    line_number: Optional[int] = None


class DatabaseMigrationGuard:
    """Deterministic analyzer inspecting SQL migrations for zero-downtime safety."""

    # Destructive operations that cause irreversible data loss or downtime
    DESTRUCTIVE_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
        (
            re.compile(r"(?i)\bDROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?([a-zA-Z0-9_.\"']+)", re.I),
            "Destructive Table Drop",
            "Dropping a table permanently deletes data and breaks running services. Use expand-and-contract phase deprecation instead.",
        ),
        (
            re.compile(r"(?i)\bDROP\s+DATABASE\s+([a-zA-Z0-9_.\"']+)", re.I),
            "Destructive Database Drop",
            "Dropping an entire database is prohibited through automated migrations.",
        ),
        (
            re.compile(r"(?i)\bTRUNCATE\s+(?:TABLE\s+)?([a-zA-Z0-9_.\"']+)", re.I),
            "Table Truncation",
            "TRUNCATE deletes all rows and cannot be rolled back safely during deployment.",
        ),
        (
            re.compile(r"(?i)\bALTER\s+TABLE\s+[a-zA-Z0-9_.\"']+\s+DROP\s+COLUMN\s+([a-zA-Z0-9_.\"']+)", re.I),
            "Destructive Column Drop",
            "Dropping an active column causes immediate 500 errors on running app instances. Follow expand-and-contract: stop writing, deploy code, then drop in a subsequent release.",
        ),
    ]

    # Operational risks (locking, performance degradation)
    WARNING_PATTERNS: List[Tuple[re.Pattern, str, str, str]] = [
        (
            re.compile(r"(?i)\bFOREIGN\s+KEY\s*\(([a-zA-Z0-9_,\s]+)\)\s*REFERENCES\s+([a-zA-Z0-9_.\"']+)", re.I),
            "Unindexed Foreign Key",
            "Foreign keys without a supporting index cause full table scans and share locks on the referenced table during updates and deletes.",
            "Add a CREATE INDEX CONCURRENTLY on the foreign key column.",
        ),
        (
            re.compile(r"(?i)\bCREATE\s+INDEX\s+(?!CONCURRENTLY\b)", re.I),
            "Non-Concurrent Index Creation",
            "Standard CREATE INDEX locks the table against writes on production PostgreSQL engines.",
            "Use CREATE INDEX CONCURRENTLY to avoid blocking read/write transactions.",
        ),
        (
            re.compile(r"(?i)\bALTER\s+TABLE\s+[a-zA-Z0-9_.\"']+\s+ADD\s+COLUMN\s+[a-zA-Z0-9_.\"']+\s+.*DEFAULT\s+.*\bNOT\s+NULL\b", re.I),
            "Adding NOT NULL with Default",
            "Adding a NOT NULL column with a volatile default can cause a full table rewrite and exclusive lock on legacy database versions.",
            "Add column as nullable, backfill values in batches, then set NOT NULL.",
        ),
    ]

    @classmethod
    def inspect(cls, sql_content: str, allow_destructive: bool = False) -> Tuple[MigrationSafetyLevel, List[MigrationFinding]]:
        """Inspect a SQL migration script and return safety level with findings."""
        findings: List[MigrationFinding] = []
        lines = sql_content.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Skip comment lines
            if stripped.startswith("--") or stripped.startswith("/*"):
                continue

            # Check destructive DDL
            for pattern, name, reason in cls.DESTRUCTIVE_PATTERNS:
                match = pattern.search(line)
                if match:
                    findings.append(MigrationFinding(
                        finding_type=name,
                        severity="CRITICAL",
                        statement=match.group(0),
                        reason=reason,
                        remediation="Adopt zero-downtime expand-and-contract migration strategy.",
                        line_number=idx,
                    ))

            # Check warning patterns
            for pattern, name, reason, remediation in cls.WARNING_PATTERNS:
                match = pattern.search(line)
                if match:
                    findings.append(MigrationFinding(
                        finding_type=name,
                        severity="MEDIUM",
                        statement=match.group(0),
                        reason=reason,
                        remediation=remediation,
                        line_number=idx,
                    ))

        # Check for missing rollback / down indicator if file is large (> 5 statements)
        if len([ln for ln in lines if ln.strip().endswith(";")]) > 5:
            if not any("down" in ln.lower() or "rollback" in ln.lower() for ln in lines):
                findings.append(MigrationFinding(
                    finding_type="Missing Rollback Plan",
                    severity="LOW",
                    statement="-- Missing rollback section",
                    reason="Migration script contains multiple DDL operations but lacks documented rollback instructions.",
                    remediation="Include explicit rollback steps or document why migration is forward-only.",
                ))

        # Determine overall safety level
        has_critical = any(f.severity == "CRITICAL" for f in findings)
        if has_critical and not allow_destructive:
            safety = MigrationSafetyLevel.DESTRUCTIVE_BLOCKED
        elif findings:
            safety = MigrationSafetyLevel.WARNING_REQUIRES_REVIEW
        else:
            safety = MigrationSafetyLevel.SAFE

        return safety, findings
