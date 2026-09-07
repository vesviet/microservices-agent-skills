## Data Engineer Review Checklist

This reference checklist provides detailed engineering, lakehouse architecture, data contract, and governance criteria for data engineering to meet 2027 Agentic SWE and Modern Data standards.

### 1. Open Data Contract Standard (ODCS v3.1.0) & Boundary Enforcement
- **Machine-Readable Contract Specification**: Pipeline contracts are formally declared using Open Data Contract Standard v3 (`contracts/schemas/data-pipeline-spec.json`) covering dataset grain, schema invariants, freshness SLAs, quality gates, and quarantine policies.
- **Producer Boundary Gate Enforcement**: Automated schema validation runs at producer boundaries; invalid or non-compliant payloads fail closed prior to ingestion into Bronze/raw lakehouse tables.
- **Strict SemVer Schema Evolution**: Schema mutations adhere to Semantic Versioning: additive nullable columns represent minor version bumps; breaking changes (column removal, type alterations, nullability changes) require major version increments with dual-write transition periods.
- **Freshness SLA Instrumentation**: Latency objectives (P95 and P99 ingestion latency) are instrumented and monitored with automated threshold alerting.
- **Executable Quality Assertions**: Data contracts define unambiguous quality assertions (null rate ceilings, uniqueness constraints, value range checks, foreign key referential integrity) executed automatically during pipeline runs.
- **Contract Ownership & Lineage**: Every dataset declares explicit producer and consumer owners, SLA tier, and upstream/downstream lineage graphs.

### 2. Modern Lakehouse Architecture (Iceberg v3 & Delta Lake)
- **Table Format Standardization**: Lakehouse tables adopt Apache Iceberg v3 or Delta Lake formats, eliminating proprietary storage lock-in and unversioned file directories.
- **Row-Level Delete Optimization**: Iceberg v3 position deletes and equality deletes are managed and compacted to prevent read-path performance degradation during high-churn CDC workloads.
- **Partition Evolution Without Rewrites**: Partition schemes evolve dynamically (e.g., migrating from daily to hourly partitioning) using Iceberg metadata evolution without requiring multi-terabyte historical data rewrites.
- **REST Catalog Federation**: Catalog access is standardized via REST Catalog specifications (Polaris, Unity Catalog) ensuring consistent ACID transactions across heterogeneous compute engines (Spark, Trino, DuckDB).
- **Automated Table Lifecycle Maintenance**: Scheduled maintenance procedures automate small-file compaction (`rewrite_data_files`), historical snapshot expiration, and orphan file vacuuming to maintain query performance and prune obsolete storage.
- **Multi-Dimensional Clustering**: High-cardinality filter columns and access keys utilize Z-order or Hilbert curve clustering to optimize data layout for partition pruning and file skipping.

### 3. Idempotency, Deterministic Upsert MERGE & WAP Protocol
- **Deterministic Upsert MERGE Semantics**: All table updates utilize atomic SQL `MERGE` statements keyed on natural business keys (`MERGE INTO target USING source ON target.id = source.id ...`), completely eliminating blind appends and duplicate records.
- **Cryptographic Row Deduplication**: Deterministic row hashes (`SHA256(composite_primary_keys)`) are computed at ingestion to detect and discard duplicate records across pipeline retries and overlapping batches.
- **Write-Audit-Publish (WAP) Pattern**: Pipeline writes are staged into isolated Iceberg metadata branches or staging partitions; automated data contract and quality test suites execute against the branch, fast-forwarding to the production main branch only upon 100% pass.
- **Watermark & Event-Time Windowing**: Streaming and micro-batch ingestion pipelines implement explicit watermark windows to process late-arriving or out-of-order records deterministically without dropping data.
- **Zero-State Invariance on Retry**: Re-executing any pipeline DAG, historical backfill, or recovery slice against the same source data produces identical lakehouse state without row-count inflation or duplicate side effects.

### 4. Circuit Breakers & Dead-Letter Queue (DLQ) Quarantine
- **Automated Anomaly Circuit Breakers**: Pipelines deploy automated circuit breakers that immediately halt downstream data promotion when record-level error rates exceed defined safety thresholds (>2%).
- **Isolated DLQ Quarantine Routing**: Malformed, schema-mismatched, or unparsable records are automatically routed to isolated Dead-Letter Queues (DLQ) or quarantine tables, preventing corrupt records from polluting Silver and Gold layers.
- **Comprehensive Diagnostic Metadata**: Every quarantined record is enriched with ingestion timestamp, pipeline execution ID, source identifier, raw unparsed payload, and machine-readable validation error code.
- **Replayability & Self-Healing Utilities**: Dedicated backfill and replay scripts exist to reprocess remediated DLQ records post-schema fix without duplicating valid records or requiring manual database surgery.
- **Quarantine Surge Alerting**: Real-time alerting monitors DLQ arrival velocity to detect upstream producer schema drift or corruption before downstream SLA breach.

### 5. Unified Semantic Layer & AI Agent MCP Endpoints
- **Centralized Metric Code Definitions**: Key business metrics and dimensions are authored as code in centralized Semantic Layers (dbt MetricFlow, Cube) to establish a single source of truth across all analytics tools.
- **Logical to Physical Decoupling**: Business stakeholders and analytical consumers query logical metrics, dimensions, and semantic views rather than direct physical lakehouse tables.
- **Agent-Facing MCP Tool Servers**: Semantic metrics are exposed to autonomous AI agents via standardized Model Context Protocol (MCP) server endpoints (`build-mcp-server`, `configure-mcp`), replacing fragile raw SQL generation.
- **Stateless & Token-Budgeted Execution**: Agent MCP endpoints enforce stateless query execution, strict token expenditure limits, query complexity quotas, and concurrency throttling.
- **Machine-Verifiable Metric Dictionaries**: MCP endpoints provide machine-readable metadata catalogs, column descriptions, and semantic lineage graphs enabling autonomous agent discovery.

### 6. Data FinOps & Resource Governance
- **Mandatory Partition Pruning**: Query execution plans, dbt transformations, and analytical views require explicit partition key and clustering key predicates, preventing unpartitioned full table scans.
- **Compute Warehouse Auto-Suspend**: Virtual compute warehouses and query engines configure aggressive auto-suspend timers (e.g., 60-second idle limit) and auto-scaling boundaries.
- **Query Timeout & Slot Ceilings**: Hard query runtime ceilings and compute slot allocations are enforced to prevent runaway queries and runaway cloud billing spikes.
- **Granular Cost Attribution Tagging**: All pipeline jobs, transformations, and warehouse sessions are tagged with `project`, `environment`, `owner`, and `cost_center` metadata for cost-per-query tracking.
- **Storage Lifecycle Tiering**: Automated storage tiering transitions cold historical partitions from hot NVMe/SSD object tiers to low-cost archival storage classes.

### 7. Zero-Trust Governance & OWASP ASI Compliance
- **Non-Human Identity (NHI) Least-Privilege**: Automated pipeline runners, orchestrators, and ETL services authenticate via dedicated, short-lived service principals with least-privilege scoping; shared superuser accounts are strictly prohibited.
- **Column-Level & Row-Level Security**: Sensitive attributes and tenant-specific rows are restricted via Column-Level Security (CLS) and Row-Level Security (RLS) policies at the catalog layer.
- **Dynamic Data Masking (DDM)**: PII, confidential attributes, and customer credentials are dynamically masked for non-privileged roles and staging environments per `data-classification.yaml`.
- **OWASP ASI03 Privilege Escalation Defense**: Lakehouse query engines and agent-facing MCP interfaces enforce strict permission boundaries preventing agents from escalating privileges or escaping analytical sandboxes.
- **OWASP ASI06 Context Poisoning Defense**: Ingestion pipelines feeding RAG vector stores and semantic search databases sanitize and validate external text, documents, and prompts against indirect prompt injections.

### 8. AI/ML Data Supply Chain & Vector Operations
- **Vector Ingestion & Embedding Freshness**: Document chunking, embedding generation, and vector database upserts operate via versioned pipelines with explicit freshness SLAs; vector store staleness is treated as a data quality incident.
- **Bidirectional Document Provenance**: Embedded chunks in vector stores maintain bidirectional lineage links back to source record IDs, document versions, and ingestion run timestamps.
- **Feature Store Parity & Invariance**: Feature calculation logic for batch training (offline) and real-time inference (online) is defined once and shared, eliminating training-serving skew.
- **Point-in-Time Correctness**: Training datasets and historical feature backfills use Iceberg time-travel queries and snapshot joins to prevent future-data leakage.
- **Feature Catalog Registration**: All engineered features are cataloged with data types, entity keys, freshness SLAs, ownership, and upstream data lineage.
