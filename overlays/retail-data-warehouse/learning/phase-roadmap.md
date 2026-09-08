# Phase Roadmap — Data Engineer Rabity

Detailed curriculum for each phase of the 10-module data engineering roadmap.
Each phase defines: learning objectives, core tools, hands-on deliverables,
and exit criteria that MUST be satisfied before the next phase is unlocked.

---

## Phase 1 — SQL + Analytics Foundation

**Duration:** 2 tuần  
**Status:** Active

### Objectives

- Write fluent SQL for data extraction, aggregation, and transformation
- Understand window functions, CTEs, subqueries, and joins
- Develop analytical intuition: translate a business question into a SQL query

### Core Tools

- PostgreSQL or DuckDB (local, no install friction)
- DBeaver or psql for query execution
- SQLite as a zero-config sandbox option

### Weekly Focus

| Week | Focus                                                       |
| ---- | ----------------------------------------------------------- |
| 1    | SELECT, WHERE, GROUP BY, JOIN (inner, left, right, full)    |
| 2    | Window functions (ROW_NUMBER, RANK, LAG/LEAD), CTEs, CASE  |

### Hands-On Deliverables

- [ ] 10 SQL exercises with real datasets (e.g., Northwind, Chinook)
- [ ] 1 analytical query solving a business question using CTEs + window functions
- [ ] 1 documented SQL file with comments explaining each clause

### Exit Criteria

- Can write a GROUP BY + HAVING query without reference
- Can write a self-join or multi-table join with correct alias usage
- Can use ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) correctly
- Deliverables committed to `phase-1-sql-foundation/`

---

## Phase 2 — Python Data Stack

**Duration:** 3 tuần  
**Unlocks after:** Phase 1 exit criteria satisfied

### Objectives

- Load, clean, and transform tabular data with pandas
- Produce formatted Excel reports using openpyxl
- Visualize findings with matplotlib / seaborn

### Core Tools

- Python 3.11+, pandas, numpy
- openpyxl, xlsxwriter
- matplotlib, seaborn
- Jupyter Lab or VS Code notebooks

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | pandas basics: read, inspect, filter, sort, groupby                |
| 2    | Data cleaning: dtypes, nulls, duplicates, encoding, string ops     |
| 3    | Excel reporting with openpyxl; matplotlib charts; end-to-end script|

### Hands-On Deliverables

- [ ] 1 data cleaning script that handles nulls, types, and encoding
- [ ] 1 Excel report generated programmatically with styled headers + auto-filter
- [ ] 1 exploratory analysis notebook with at least 3 visualizations
- [ ] Scripts are reusable (no hardcoded paths; use `argparse` or `.env`)

### Exit Criteria

- Can ingest a messy CSV and produce a clean DataFrame with correct dtypes
- Can group by multiple columns and compute aggregations
- Can write a formatted multi-sheet Excel report from code
- Deliverables committed to `phase-2-python-stack/`

---

## Phase 3 — Parquet + DuckDB + Polars

**Duration:** 2 tuần  
**Unlocks after:** Phase 2 exit criteria satisfied

### Objectives

- Understand columnar storage and why Parquet outperforms CSV at scale
- Query Parquet files directly with DuckDB (SQL interface, zero server)
- Process large DataFrames efficiently with Polars (lazy evaluation)

### Core Tools

- DuckDB (Python client + CLI)
- Polars
- PyArrow
- pandas (for comparison benchmarks)

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | Parquet read/write; DuckDB SQL on files; join Parquet + CSV in SQL |
| 2    | Polars: LazyFrame, expressions, groupby; benchmark vs. pandas      |

### Hands-On Deliverables

- [ ] Convert a CSV dataset (>100k rows) to Parquet and query with DuckDB
- [ ] Reproduce a pandas pipeline in Polars with LazyFrame; compare runtime
- [ ] 1 DuckDB script that joins multiple Parquet files and exports result

### Exit Criteria

- Can explain the columnar vs. row-based storage trade-off
- Can run a multi-table SQL query on Parquet files using DuckDB
- Can write a Polars pipeline using `.lazy()` → `.collect()`
- Deliverables committed to `phase-3-parquet-duckdb-polars/`

---

## Phase 4 — ETL / ELT Architecture

**Duration:** 3 tuần  
**Unlocks after:** Phase 3 exit criteria satisfied

### Objectives

- Design and build Extract-Transform-Load pipelines in Python
- Understand ETL vs. ELT trade-offs and when to use each
- Handle incremental loads, idempotency, and pipeline failures

### Core Tools

- Python (scripts, not notebooks)
- SQLite or DuckDB as target warehouse
- pandas / Polars for transformation
- logging module, dotenv

### Weekly Focus

| Week | Focus                                                               |
| ---- | ------------------------------------------------------------------- |
| 1    | Extract: file ingestion, API pulls, schema detection                |
| 2    | Transform: normalizing, enriching, validating, deduplicating        |
| 3    | Load: idempotent upserts, incremental loads, error handling/logging |

### Hands-On Deliverables

- [ ] 1 end-to-end ETL script: CSV → clean → DuckDB table
- [ ] Add incremental load logic (only process new/updated rows)
- [ ] Add structured logging to all pipeline stages
- [ ] 1 architecture diagram (Mermaid) showing the pipeline flow

### Exit Criteria

- Pipeline is idempotent: running twice produces the same result
- All transformation assumptions are logged, not implicit
- Error in extraction stage does not corrupt the load stage
- Deliverables committed to `phase-4-etl-elt/`

---

## Phase 5 — Airflow + Scheduling

**Duration:** 2 tuần  
**Unlocks after:** Phase 4 exit criteria satisfied

### Objectives

- Author Airflow DAGs to orchestrate multi-step pipelines
- Understand task dependencies, retries, and scheduling expressions
- Use Airflow connections and variables for config management

### Core Tools

- Apache Airflow 2.x (local via Docker or Astro CLI)
- Python Operators, BashOperator, PythonOperator
- Airflow UI for monitoring

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | DAG basics: tasks, dependencies, scheduling; convert ETL to a DAG  |
| 2    | Retries, SLAs, Connections, Variables, XCom; monitoring runs       |

### Hands-On Deliverables

- [ ] Convert Phase 4 ETL pipeline into an Airflow DAG
- [ ] Add retry logic and email/Slack alerting on failure
- [ ] Schedule DAG to run on a cron expression

### Exit Criteria

- DAG runs end-to-end in Airflow UI without errors
- Failed task retries correctly without duplicating data
- DAG is parameterized using Airflow Variables (no hardcoded paths)
- Deliverables committed to `phase-5-airflow/`

---

## Phase 6 — Data Warehouse Modeling

**Duration:** 3 tuần  
**Unlocks after:** Phase 5 exit criteria satisfied

### Objectives

- Model analytical schemas using Kimball dimensional modeling (star schema)
- Build dbt models for transformation and documentation
- Understand fact tables, dimension tables, and slowly changing dimensions (SCD)

### Core Tools

- dbt Core (DuckDB or BigQuery adapter)
- DuckDB / BigQuery as warehouse
- dbt docs, dbt test

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | Star schema design: facts, dims, surrogate keys, grain definition  |
| 2    | dbt models: staging, intermediate, mart layers; ref() and source() |
| 3    | dbt tests, documentation, SCD Type 2 implementation               |

### Hands-On Deliverables

- [ ] Design a star schema for a sales dataset (diagram + DDL)
- [ ] Build a dbt project with staging → intermediate → mart layers
- [ ] Add dbt tests (not_null, unique, accepted_values) to all models
- [ ] Generate dbt docs and review the lineage graph

### Exit Criteria

- Star schema design reviewed and grain is correctly defined
- dbt project runs `dbt run` and `dbt test` without errors
- At least one SCD Type 2 dimension is implemented
- Deliverables committed to `phase-6-warehouse-modeling/`

---

## Phase 7 — Streaming / Kafka

**Duration:** 4 tuần  
**Unlocks after:** Phase 6 exit criteria satisfied

### Objectives

- Understand event streaming architecture and when to use it vs. batch
- Produce and consume Kafka messages in Python
- Build a simple stream processing pipeline with Faust or Kafka Streams

### Core Tools

- Apache Kafka (Docker Compose setup)
- kafka-python or confluent-kafka
- Faust (Python stream processing) or ksqlDB
- Schema Registry + Avro (optional, week 3+)

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | Kafka concepts: topics, partitions, consumers, offsets             |
| 2    | Producer + Consumer in Python; commit strategies                   |
| 3    | Stream processing with Faust: stateless transformations            |
| 4    | Stateful processing, windowing, exactly-once semantics             |

### Hands-On Deliverables

- [ ] Kafka up locally via Docker Compose; produce + consume 1000 messages
- [ ] Build a producer that streams real or synthetic event data
- [ ] Build a Faust app that consumes, filters, and writes results to DuckDB
- [ ] Architecture diagram of the streaming pipeline

### Exit Criteria

- Can explain partition assignment and consumer group rebalancing
- Producer + consumer pipeline runs end-to-end without data loss
- Faust app processes events with a windowed aggregation
- Deliverables committed to `phase-7-streaming-kafka/`

---

## Phase 8 — Lakehouse + Big Data

**Duration:** 4 tuần  
**Unlocks after:** Phase 7 exit criteria satisfied

### Objectives

- Understand Lakehouse architecture (Delta Lake, Apache Iceberg)
- Work with Spark for large-scale distributed transformation
- Design storage layers: Bronze → Silver → Gold (Medallion architecture)

### Core Tools

- Apache Spark (PySpark, local mode)
- Delta Lake or Apache Iceberg
- MinIO (S3-compatible local object storage)
- dbt + Spark adapter (optional)

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | PySpark basics: RDD vs DataFrame, transformations, actions         |
| 2    | Delta Lake: ACID transactions, time travel, schema evolution       |
| 3    | Medallion architecture: Bronze → Silver → Gold pipelines           |
| 4    | Optimization: partitioning, Z-ordering, compaction, file sizing    |

### Hands-On Deliverables

- [ ] PySpark pipeline that processes a large CSV into a Delta table
- [ ] Implement Bronze → Silver → Gold layers for a sample dataset
- [ ] Demonstrate Delta time travel by querying a previous table version
- [ ] Architecture document: Lakehouse design decisions and trade-offs

### Exit Criteria

- Delta table supports ACID writes from multiple concurrent Spark jobs
- Medallion pipeline runs end-to-end in local Spark
- Time travel query works correctly
- Deliverables committed to `phase-8-lakehouse/`

---

## Phase 9 — Observability + Data Quality

**Duration:** 2 tuần  
**Unlocks after:** Phase 8 exit criteria satisfied

### Objectives

- Implement data quality checks at pipeline ingestion and transformation layers
- Use Great Expectations or dbt tests for automated validation
- Build pipeline observability: row count checks, freshness alerts, anomaly flags

### Core Tools

- Great Expectations or Soda Core
- dbt tests (schema + data tests)
- Grafana + Prometheus (optional for metrics dashboards)
- Python logging, alerting hooks (Slack / email)

### Weekly Focus

| Week | Focus                                                              |
| ---- | ------------------------------------------------------------------ |
| 1    | Great Expectations: expectation suites, data docs, checkpoints     |
| 2    | Integrating quality checks into Airflow DAGs; freshness + anomaly  |

### Hands-On Deliverables

- [ ] Write a Great Expectations suite for the Phase 4 ETL output
- [ ] Add a checkpoint that blocks the DAG if row counts deviate >10%
- [ ] Add freshness check: alert if source data is >24h stale
- [ ] Document the data quality contract for one dataset

### Exit Criteria

- Quality suite catches a deliberately injected data error
- DAG fails fast on quality gate breach instead of loading bad data
- Freshness alert fires correctly in a simulated staleness scenario
- Deliverables committed to `phase-9-observability/`

---

## Phase 10 — Portfolio Projects

**Duration:** Liên tục (ongoing)  
**Unlocks after:** Phase 9 exit criteria satisfied

### Objectives

- Combine all skills in end-to-end projects that demonstrate production-grade thinking
- Build a public portfolio with documented pipelines and findings
- Practice the full data engineering lifecycle from raw ingestion to stakeholder report

### Project Ideas (pick at least 2)

| Project                       | Skills Demonstrated                                       |
| ----------------------------- | --------------------------------------------------------- |
| E-commerce Sales Pipeline     | ETL, Airflow, dbt, star schema, Excel report              |
| Real-Time Twitter/Reddit Feed | Kafka, Faust, DuckDB, streaming dashboard                 |
| Public Dataset Lakehouse      | PySpark, Delta Lake, Medallion, Spark SQL                 |
| Data Quality Monitor          | Great Expectations, Airflow, observability, alerting      |
| Personal Finance Tracker      | Python, pandas, DuckDB, Parquet, automated weekly reports |

### Portfolio Standards

- Each project MUST have a `README.md` with architecture diagram and data lineage
- All pipelines are reproducible with a single `make run` or `docker-compose up`
- No raw data committed; only schema, scripts, and generated report snapshots
- Document assumptions, known limitations, and future improvements

### Ongoing Deliverables

- [ ] Minimum 2 completed portfolio projects with public documentation
- [ ] Each project linked from a central portfolio `README.md`
- [ ] At least 1 project uses 3+ phases of the skill stack together

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/foundation/create-migration/SKILL.md` and the `deployment-plan.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/create-migration/SKILL.md` and the `deployment-plan.json` schema.

Last updated: 2026-09-01
