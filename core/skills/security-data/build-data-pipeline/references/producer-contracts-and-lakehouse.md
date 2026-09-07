# Producer Contracts & Modern Lakehouse Storage — Reference

This reference documents standards and implementation procedures for enforcing Open Data Contract Standard (ODCS v3.1.0) specifications at producer boundaries and managing transactional lakehouse architectures (Apache Iceberg and Delta Lake).

---

## 1. Open Data Contract Standard (ODCS v3.1.0) at Producer Boundary

Modern agentic data architectures replace fragile, undocumented data handoffs with explicit, machine-readable data contracts negotiated between data producers and consumers.

### 1.1 ODCS v3.1.0 Contract Specification
Every ingested dataset must possess an active contract specifying four foundational pillars:

```yaml
# Example: orders-dataset-odcs-v3.yaml
contract_version: "3.0.0"
dataset: "lakehouse.bronze.orders"
owner: "orders-checkout-team"
sla:
  freshness_hours: 1
  availability_pct: 99.9
  latency_p95_minutes: 15
schema:
  type: object
  required: [order_id, customer_id, order_timestamp, gross_amount_usd, status]
  properties:
    order_id:
      type: string
      format: uuid
    customer_id:
      type: string
      format: uuid
    order_timestamp:
      type: string
      format: date-time
    gross_amount_usd:
      type: number
      minimum: 0.00
    status:
      type: string
      enum: [PENDING, PAID, SHIPPED, CANCELLED, REFUNDED]
quality_rules:
  - rule_id: "chk_positive_order_amount"
    assertion: "gross_amount_usd >= 0.0"
    severity: "critical"
  - rule_id: "chk_status_validity"
    assertion: "status IN ('PENDING','PAID','SHIPPED','CANCELLED','REFUNDED')"
    severity: "critical"
```

### 1.2 Invariant Schema Freeze & Ingestion Gate
1. **Pre-Ingestion Validation**: Ingestion workers evaluate raw payloads against the ODCS JSON Schema / Avro descriptor before writing to storage.
2. **Schema Invariance**: Unannounced column drops, type mutations, or nullability relaxations immediately trigger contract violation alerts.
3. **Evolution Protocol**:
   - *Backward-Compatible Changes* (additive nullable fields, optional metadata): Increment minor contract version (`3.0.0` → `3.1.0`); ingested seamlessly.
   - *Breaking Changes* (field removals, type shifts, new non-null constraints): Require major contract version bump (`3.x` → `4.0.0`), dual-read consumer transition periods, and prior approval.

---

## 2. Modern Lakehouse Architecture (Apache Iceberg & Delta Lake)

Data pipelines must organize storage into transactional, ACID-compliant tiers using the Medallion pattern over columnar Parquet files.

### 2.1 Medallion Storage Tiers

| Tier | Purpose | Format & Guarantees | Retention / Lineage |
|---|---|---|---|
| **Bronze** | Raw landing & staging | Parquet / Iceberg append-only with raw payload and ingestion timestamps | Raw audit trail; immutable for 10+ years |
| **Silver** | Conformed, validated, cleansed | Apache Iceberg v3 / Delta Lake; deduplicated, types cast, DQ gates passed | Operational history; time-travel enabled |
| **Gold** | Business metrics & dimensional star schemas | Apache Iceberg / DuckDB aggregates; denormalized for BI and feature stores | Canonical analytical source of truth |

### 2.2 Apache Iceberg v3 Transactional Patterns
- **Hidden Partitioning**: Partition by logical date (e.g. `days(event_time)`) without requiring consumers to add synthetic partition columns to queries.
- **ACID Snapshot Isolation**: All write transactions commit atomically by updating the metadata pointer file (`metadata.json`). Readers query consistent snapshots without locking writers.
- **File Sizing Standards**: Optimize Parquet file sizes between 128 MB and 512 MB to balance scan throughput with query planning latency.

### 2.3 dbt 1.9 Microbatch Incremental Strategy
For high-volume event streams, use dbt 1.9 microbatch models to enable partitioned backfills and granular auto-retries:

```sql
{{ config(
    materialized = 'incremental',
    incremental_strategy = 'microbatch',
    unique_key = 'order_id',
    event_time = 'order_timestamp',
    begin = '2026-01-01 00:00:00',
    batch_size = 'hour'
) }}

SELECT
    order_id,
    customer_id,
    order_timestamp,
    gross_amount_usd,
    status,
    _ingested_at
FROM {{ ref('bronze_orders') }}
WHERE order_timestamp >= {{ var('start_time') }}
  AND order_timestamp < {{ var('end_time') }}
```

### 2.4 EU AI Act Data Lineage & Provenance Compliance
- **10-Year Provenance**: Ingestion pipelines feeding AI/ML features must record complete dbt DAG lineage from raw source to model feature matrices. Retain all metadata snapshots for at least 10 years per EU AI Act governance.
- **Attribute Auditing**: Ingestion pipelines must scrub protected demographic, toxic, or unauthorized attributes before emitting feature datasets.

### 2.5 DuckDB Production Integration
- **Embedded Analytical Processing**: Use DuckDB embedded or via MotherDuck for local transformations, staging diffs, and query workloads up to 100 GB.
- **Resource Constraints**: Always declare thread and memory limits:
  ```sql
  SET max_memory = '4GB';
  SET threads = 4;
  ```
