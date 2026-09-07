---
name: build-data-pipeline
description: Design and implement transactional lakehouse pipelines (Iceberg/Delta), enforce ODCS v3.1.0 data contracts at producer boundaries, integrate Great Expectations/dbt-expectations quality gates, and isolate invalid records in DLQ quarantine with deterministic replayability. Use when the work requires an owned, repeatable data pipeline.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests]
---

# Build Data Pipeline

Use this skill when building or maintaining repeatable data infrastructure: ingestion pipelines, lakehouses, transformation models, quality gates, dead-letter quarantine, or orchestration. For one-off analytical queries, use `analyze-data` instead.

## When to Use

- implementing transactional lakehouse pipelines with Apache Iceberg or Delta Lake
- enforcing Open Data Contract Standard (ODCS v3.1.0) at producer perimeters
- establishing automated data quality gates using Great Expectations or dbt-expectations
- routing poisoned or non-conformant records into Dead-Letter Queue (DLQ) quarantine stores
- authoring idempotent transformations, dbt microbatch models, or deterministic replay runbooks
- building streaming or microbatch pipelines with Kafka and Airflow DAGs

## Core Rules

- treat all source inputs as **read-only** — never modify upstream files or producer sources
- enforce **ODCS v3.1.0 data contracts** at producer boundaries before persisting into storage
- implement the **Medallion architecture**: immutable Bronze landing, conformed Silver, aggregated Gold
- cast columns to explicit types; never allow untyped string states as the final schema
- pipelines must be **idempotent**: running twice must produce identical results via `MERGE INTO` natural keys
- isolate poisoned records in **DLQ quarantine** with metadata; trip circuit-breaker if error rate exceeds 1.0%
- enforce **EU AI Act lineage tracking**: retain dbt DAG provenance for 10+ years; audit for toxic or biased attributes
- deploy **DuckDB** embedded for <100 GB analytical workloads with explicit memory limits (`SET max_memory = '4GB'`); for DuckDB v2.0 (October 2026) targets, treat the **storage format v2.0.0 as breaking** — plan re-export of persisted datasets, and prefer the Quack/`CONNECT` server mode only for governed multi-tenant deployments
- **Catalog as control plane (2027)**: coordinate transactions, policies, and credentials at the catalog layer — Iceberg REST catalog protocol (server-side scan planning, ETag freshness, `Idempotency-Key` retried commits, credential vending), Polaris/Unity Catalog/Snowflake Horizon federation; the table format is no longer the governance locus
- **Iceberg v4 readiness**: spec v4 is a metadata restructuring (relative paths, adaptive metadata tree) with foundations already in 1.11.0 — prepare low-risk upgrade runbooks, never data rewrites; use Variant type + shredding as the canonical semi-structured ingestion path; Spark floor is 4.1+ (3.4 deprecated); Flink 2.3 sinks support deletion vectors and Variant
- **Native table encryption**: use Iceberg 1.11 table encryption (KMS integration, automatic key rotation, manifest-list encryption) as the zero-trust enforcement layer instead of storage-only controls
- mask or aggregate PII before emitting any output or logging; classify with `data-classification.yaml`
- log row counts and drift before and after every transformation step
- wire DLQ quarantine triggers to contract SLA fields (freshness/latency thresholds) instead of ad-hoc thresholds; publish OpenLineage events with explicit lineage facets for impact analysis
- detailed specifications, schemas, and runbooks are maintained in [`references/producer-contracts-and-lakehouse.md`](references/producer-contracts-and-lakehouse.md) and [`references/quality-gates-dlq-and-replayability.md`](references/quality-gates-dlq-and-replayability.md)

## Suggested Process

### 1. Ingest & Validate Producer Contract
Ingest source events and evaluate raw payloads against the ODCS v3.1.0 contract schema. Reject unannounced breaking schema shifts at the boundary.

### 2. Lakehouse Bronze Staging & Schema Verification
Stage raw inputs into Bronze Iceberg/Parquet tables with immutable audit trails (`_ingested_at`, `_source_file`, `trace_id`).

### 3. Silver Layer Transformation & Automated DQ Gates
Apply cleaning, deduplication, and type casting. Run Great Expectations and dbt-expectations assertion suites (nullability, uniqueness, foreign keys).

### 4. DLQ Quarantine & Error Routing
Route contract-failing or malformed records into structured DLQ quarantine. Halt ingestion and notify on-call if error rate exceeds 1.0%.

### 5. Gold Layer Modeling & Metric Publishing
Build business aggregates and dimensional models. Configure dbt 1.9 microbatch strategies and publish clean tables to the semantic layer.

### 6. Emit Pipeline Spec & Monitor
Validate output against contract specifications. Record lineage, execution benchmarks, and verify deterministic replayability.

## Inputs

- Producer schema contracts ODCS v3.1.0 YAML or JSON Schema)
- Raw source data (Kafka streams, object storage Parquet/CSV, REST APIs, database CDC)
- Business transformation requirements and SLA parameters

## Role Boundaries

| Role | Owns |
| ---- | ---- |
| Data Engineer | Pipeline topology, ODCS enforcement, Iceberg storage, DLQ quarantine, replayability |
| Solution Architect | System architecture, storage technology selection, cross-system boundaries |
| Data Analyst | Semantic layer metrics, business queries, ad-hoc exploratory reports |
| QA Engineer | Test automation, failure injection testing, mutation validation |

## Checklist

- [ ] source files and upstream databases treated as strictly read-only
- [ ] ODCS v3.1.0 producer contracts validated and enforced at ingestion perimeter
- [ ] Medallion architecture (Bronze → Silver → Gold) implemented on Apache Iceberg or Delta Lake
- [ ] column types explicitly cast after cleaning; no unvalidated string schemas retained
- [ ] automated quality gates (Great Expectations/dbt-expectations) configured for critical assertions
- [ ] non-conformant records routed to DLQ quarantine without silent drops
- [ ] circuit-breaker trips and halts pipeline when DLQ error rate exceeds 1.0%
- [ ] deterministic replayability verified using idempotent `MERGE INTO` on natural keys
- [ ] EU AI Act 10-year lineage metadata recorded across the dbt DAG
- [ ] PII masked and classified per `data-classification.yaml` before handoff
- [ ] pipeline outputs match `contracts/schemas/data-pipeline-spec.json` and `contracts/schemas/data-analysis-report.json`

## Related Skills

- **analyze-data**: Query and explore data without owning production pipeline infrastructure
- **database-maintenance**: Operational storage maintenance, Iceberg compaction, and index tuning
- **create-migration**: Manage relational database schema migrations
- **security-audit**: Audit pipeline data flow for PII exposure and access control
- **write-documentation**: Document pipeline runbooks, schemas, and data dictionaries
- **review-code**: Review transformation logic, concurrency, and SQL performance
- **commit-code**: Safely commit pipeline definitions to version control

## Output Contracts

When emitting pipeline specifications for downstream consumers, orchestrators, or data analyst roles, emit:

- `contracts/schemas/data-pipeline-spec.json` — complete pipeline definition, ODCS contract version, freshness SLA, quality gates, and quarantine policy.
- `contracts/schemas/data-analysis-report.json` — summary of ingested row counts, validation results, and quality metrics when cross-role handoff is required.

## Failure Modes

- **Contract violation crash**: unannounced upstream schema changes crash the pipeline. Mitigation: enforce ODCS v3.1.0 pre-ingestion validation; route non-conforming payloads to DLQ quarantine.
- **Silent data corruption**: untracked transformation defects propagate downstream. Mitigation: run automated Great Expectations suites with critical gate thresholds.
- **DLQ overflow**: unbounded poison records exhaust storage without remediation. Mitigation: enforce circuit-breaker halting at 1.0% error rate and alert engineers.
- **Non-idempotent replay**: re-running a pipeline creates duplicate records. Mitigation: require idempotent `MERGE INTO` operations on immutable natural keys.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: classify PII with `data-classification.yaml`; restrict database credentials to least-privilege roles; mask sensitive fields.
- **ASI04 Supply Chain**: validate versions of connectors, dbt packages, and ingestion libraries against approved dependency manifests.
- **ASI05 RCE Guard**: parameterize all dynamic SQL and file paths; never format queries directly from raw external payloads.
- **ASI07 Inter-Agent Communication**: emit structured contracts (`data-pipeline-spec.json`) so consuming analyst and ML roles share identical definitions.
- **ASI09 Human-Agent Trust Exploitation**: disclose residual ingestion risks, data lineage provenance, and quality validation metrics truthfully.
