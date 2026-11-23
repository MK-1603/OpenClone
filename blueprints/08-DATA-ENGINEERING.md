# Blueprint 08: Data Engineering & Ingestion Pipelines

**Project Family:** `data_engineering_and_data_science`  
**Primary Project Type:** `etl_pipeline`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `containers_cloud`, `on_premises`

---

## 1. Goals & Scope
- Batch and real-time data pipelines moving data from disparate sources to lakehouses, data warehouses, or analytical databases.
- Enforces strict schema contracts, idempotent retries, dead-letter queue (DLQ) isolation, data lineage, and privacy/GDPR compliance.

## 2. Classification Rules
- Matched when the focus is data ingestion, transformation (dbt, Spark), orchestration (Airflow, Dagster), or lakehouse storage (Parquet, Iceberg).

## 3. Intake Questions & Required Information
1. Source data systems: relational DB change data capture (CDC), REST APIs, event streams.
2. Ingestion cadence: streaming, micro-batch, or scheduled daily batch.
3. Destination storage: BigQuery, Snowflake, ClickHouse, PostgreSQL, or S3 lakehouse.
4. Data quality SLAs and schema evolution handling (backward/forward compatibility).

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `03-DATA-INTEGRITY`, `04-SECURITY-CONTROLS`, `10-TESTING-AND-QA`, `16-TELEMETRY-AND-OBSERVABILITY`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-003`, `E-004`, `E-010`.

## 5. Specialist Workforce
- `data-engineer`: Pipeline DAG authoring, transformations, and connector integration.
- `database-architect`: Storage schema design, partition pruning, and indexing.
- `devops-engineer`: Pipeline scheduling, cluster sizing, and alerting.

## 6. Verification & Delivery Artifacts
- Pipeline DAG definition with idempotent execution tests.
- Data quality validation suite (Great Expectations / soda-core).
- Data lineage documentation and disaster recovery replay runbook.
