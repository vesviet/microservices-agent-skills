# Retail Data Warehouse Overlay

Omnichannel retail data warehouse overlay extending `core/roles/data-engineer.md`, `core/roles/data-analyst.md`, `core/roles/vietnam-accounting-specialist.md`, and `core/roles/backend-developer.md`. Establishes the architectural standards, concurrency controls, Vietnamese statutory accounting compliance (VAS 14 / MISA AMIS ERP), physical store stocktake tolerance engine, and PII sanitization (Decree 13/2023/ND-CP) for multi-channel retail operations (physical POS, Shopee, TikTok Shop). Also hosts the Rabity data-engineering learning track (`learning/`).

## Technology Map (2026/2027)

| Layer / Component | Technology & Version | Role & Architectural Purpose |
|:---|:---|:---|
| **Runtime & Language** | Python 3.12+ | Asynchronous event processing, modern type aliases (`type X = ...`), strict domain exception boundaries |
| **API Gateway** | FastAPI (ASGI / Uvicorn) | High-concurrency REST endpoints, async request lifecycle, OpenAPI 3.1 schema auto-generation |
| **OLAP & Analytics** | DuckDB 1.5+ (Single-Writer) | Vectorized in-process analytical engine, Parquet ingestion, Medallion aggregations, summary export marts |
| **OLTP & Queue Buffer** | SQLite (WAL Mode) | High-throughput serialized transactional buffer for POS events, barcode audit scan streams, and draft sessions |
| **Lakehouse Storage** | Medallion Parquet | Structured columnar storage: Bronze (raw immutable), Silver (scrubbed/typed), Gold (business marts) |
| **ERP Integration** | MISA AMIS ERP | Enterprise statutory accounting, automated sales voucher sync, inventory balance and output VAT reconciliation |
| **Edge Mobile Audit** | Vanilla JS Offline PWA | Zero-dependency mobile auditor client for store PDAs/tablets; IndexedDB offline persistence; HID barcode scanner input |

## Base Roles & Scope

- **`data-engineer`** (`core/roles/data-engineer.md`): Owns Lakehouse Medallion pipelines, Parquet partitioning, DuckDB `AsyncCrossProcessLock` single-writer governance, and automated PII scrubbing.
- **`data-analyst`** (`core/roles/data-analyst.md`): Owns Gold analytical marts, semantic metrics calculation, omnichannel sales cohort modeling, and store inventory turnover queries.
- **`vietnam-accounting-specialist`** (`core/roles/vietnam-accounting-specialist.md`): Enforces VAS 14 revenue recognition, 3-tier voucher breakdown, platform fee expense categorization (TK 641), pretax unit price isolation, and MISA AMIS voucher synchronization.
- **`backend-developer`** (`core/roles/backend-developer.md`): Implements FastAPI endpoints, SQLite WAL buffer transactions, background sync workers, and PWA barcode audit ingestion services.

## Architecture & Data Flow Boundaries

```text
[ Physical POS ]     [ Shopee API ]     [ TikTok Shop API ]     [ PWA Stocktake ]
       │                    │                    │                     │
       └────────────────────┼────────────────────┴─────────────────────┘
                            ▼
      ┌─────────────────────────────────────────────────────────┐
      │  OLTP Buffer Layer: SQLite (WAL Mode, High Concurrency) │
      │  - Millisecond writes (<2ms), zero lock contention      │
      │  - Fast local scan event buffering & idempotency dedupe │
      └──────────────────────────┬──────────────────────────────┘
                                 │ Micro-batch CDC / Ingestion
                                 ▼
      ┌─────────────────────────────────────────────────────────┐
      │  Bronze Lakehouse: Raw Partitioned Parquet             │
      │  - Immutable landing zone, encrypted at rest            │
      │  - Zero analyst / AI agent query access                 │
      └──────────────────────────┬──────────────────────────────┘
                                 │ Automated PII Scrubbing (HMAC-SHA256)
                                 ▼
      ┌─────────────────────────────────────────────────────────┐
      │  Silver Lakehouse: Sanitized & Typed Parquet           │
      │  - Customer phone hashed with RETAIL_PII_SALT           │
      │  - Names pseudonymized, addresses generalized (GSO)     │
      └──────────────────────────┬──────────────────────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
┌──────────────────────────────────────┐  ┌────────────────────────────────────┐
│ DuckDB Gold Analytical Marts         │  │ MISA AMIS ERP Sync Worker          │
│ (Single-Writer AsyncCrossProcessLock)│  │ - VAS 14 Delivery Revenue Rec.     │
│ - Daily store sales & cohort trends  │  │ - 3-tier voucher decomposition     │
│ - Stock discrepancy tolerance review │  │ - Pretax unit price isolation      │
│ - Channel margin & fees breakdown    │  │ - Inventory & suspense (1381/3381) │
└──────────────────────────────────────┘  └────────────────────────────────────┘
```

## Key Architectural Principles

1. **OLTP vs. OLAP Segregation**: High-frequency transactional writes (barcode scans, POS checkout events) target SQLite in WAL mode (`PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`). DuckDB is reserved strictly for vectorized analytical queries and batch Parquet aggregations under single-writer governance.
2. **Fail-Closed Concurrency**: Multi-process write locks on DuckDB databases must fail closed. If the distributed lockarbiter (Redis) or OS filelock cannot be acquired within the designated timeout, write operations halt and raise structured incident alerts.
3. **Statutory Accounting Rigor (VAS 14 & Circular 200)**: Revenue is recognized exclusively upon confirmed delivery. E-commerce platform fees are booked as selling expenses (TK 641) without netting against gross revenue (TK 511).
4. **Zero-Trust Customer Privacy (Decree 13/2023/ND-CP)**: Personal identifiable information (PII) is permanently scrubbed at the Bronze-to-Silver lakehouse boundary using salted HMAC-SHA256 and geographic truncation.
5. **Anti-Anchoring Stocktake Integrity**: Physical store stock counting utilizes blind recounts for high-value SKUs and significant variances to prevent confirmation bias.

## Included Rules

- `rules/duckdb-concurrency.md` — Single-Writer governance via `AsyncCrossProcessLock`, retry exponential backoff & jitter, connection lifecycle, OLTP (SQLite WAL) vs OLAP (DuckDB) boundary.
- `rules/amis-accounting-standards.md` — VAS 14 revenue recognition strictly upon delivery, 3-tier voucher decomposition, selling expenses in TK 641, pretax unit price isolation, TK 1561 inventory costing.
- `rules/stocktake-tolerance.md` — Offline Vanilla JS PWA + hardware HID barcode scanner buffering to IndexedDB & SQLite WAL, mathematical variance formulas, blind recount trigger thresholds, multi-tier approval workflow, and variance suspense accounting (TK 1381 / TK 3381).
- `rules/pii-scrubbing.md` — Decree 13/2023/ND-CP compliance at Bronze -> Silver Lakehouse boundary, salted HMAC-SHA256 phone hashing with `RETAIL_PII_SALT`, pseudonymization, and address generalization.

## Learning Subtree (merged from `overlays/data-engineer-rabity`)

- `learning/learning-conventions.md` — session protocol, phase gates, output standards, skill unlock map.
- `learning/phase-roadmap.md` — 10-phase curriculum (SQL → Python → DuckDB/Polars → ETL → Airflow → dbt 1.9 → Kafka → Iceberg Lakehouse → Observability → Portfolio).
- `learning/progress.md` — phase completion tracker; the agent reads it to enforce phase gates.
- Persona-scoped: applies only for Rabity's data engineering self-study practice.

## Platform Index

The overlay targets the `data-warehouse` repo (5-container microservices, ~26k LOC Python). Canonical indexes:
- `data-warehouse/docs/PLATFORM_INDEX.md` — architecture, modules, marts, business rules
- `data-warehouse/CODEBASE_INDEX.md` — deep component inventory + API directory
- `data-warehouse/docs/INDEX.md` — documentation catalog by role

## Activation

```
Role: data-engineer (or vietnam-accounting-specialist, data-analyst, backend-developer)
Overlay: overlays/retail-data-warehouse
```

## Environment Variables

| Variable | Purpose | Default / Example |
|:---|:---|:---|
| `RETAIL_PII_SALT` | Cryptographic pepper/salt for customer phone number HMAC-SHA256 hashing | *Required in production* |
| `DUCKDB_PATH` | File path to DuckDB analytical database | `./store/warehouse.duckdb` |
| `DUCKDB_LOCK_FILE` | Auxiliary filelock path for cross-process synchronization | `./store/warehouse.duckdb.lock` |
| `SQLITE_OLTP_PATH` | File path to SQLite transactional buffer database | `./store/buffer_oltp.db` |
| `REDIS_LOCK_URL` | Redis URL for clustered distributed lockarbiter (fail-closed) | `redis://localhost:6379/0` |
| `AMIS_API_BASE_URL` | MISA AMIS Open API gateway base URL | `https://actopen.misa.vn` |
| `AMIS_APP_ID` | Application identifier registered with MISA AMIS | *Provided by MISA* |
| `AMIS_SECRET_TOKEN` | Bearer/Access token for AMIS ERP voucher synchronization | *Required in production* |

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

<!-- Standard 2026 Alignment: Deterministic execution, Single-Writer DuckDB governance, VAS 14 revenue recognition, Decree 13/2023/ND-CP PII protection. See core/rules/code.md. -->

Last updated: 2026-09-08
