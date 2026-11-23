# DATA_LIFECYCLE.md — {{PROJECT_NAME}}
**Data Classification, Persistence, Retention, and Migration Policy**  
*Specification:* v1.0.0 | *Status:* LIVING DOCUMENT

---

## 1. Data Classification Matrix

| Data Entity | Classification | Sensitivity | Storage Location | Retention Period | Deletion / Anonymization Policy |
|---|---|---|---|---|---|
| User Credentials | Secret / Auth | High | Hashed (Argon2id/bcrypt) | Account lifetime | Purged within 24h of account deletion |
| Personal Profile (PII) | Confidential | Medium | Primary Database | Account lifetime | Anonymized on account closure |
| Application Telemetry | Internal | Low | Logs / Time-series DB | 30 days | Auto-purged via TTL policy |
| Billing & Audit Events | Restricted | High | Audit Ledger (Encrypted) | 7 years (Statutory) | Immutably preserved |

---

## 2. Persistence & Storage Boundaries

- **Source of Truth**: PostgreSQL / SQLite (ACID compliant).
- **Ephemeral Cache**: In-memory cache / Redis (TTL-bounded, never source of truth).
- **Object Storage**: S3-compatible bucket for user assets with pre-signed URL access.

---

## 3. Migration & Versioning Strategy

- **Up-Migrations**: Atomic transactions; zero destructive column removals in active production.
- **Down-Migrations**: Every schema change must have a reversible rollback script tested in pre-deployment.
- **Data Seeding**: Synthetic test data strictly isolated to test and development environments.

---

## 4. Backup, Recovery & Export

- **Backup Schedule**: Daily automated snapshots with 30-day retention and point-in-time recovery.
- **Portability / GDPR Export**: Endpoints provided for complete JSON export of user-owned records.
- **Data Erasure**: Cryptographic shredding or hard row deletion cascade for GDPR "Right to be Forgotten".
