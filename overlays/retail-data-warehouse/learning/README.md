# Data Engineering Learning Track (Rabity)

Personal learning subtree merged from the former `overlays/data-engineer-rabity`
overlay. Structured 10-phase self-study roadmap for the `data-engineer` role,
scoped to Rabity's data engineering practice, hosted inside the retail
data-warehouse overlay since both share the same DuckDB/Lakehouse toolchain.

## Scope

- **Learner:** Rabity
- **Base Role:** `core/roles/data-engineer.md`
- **Goal:** SQL fundamentals → production-grade data engineering (Lakehouse, Streaming, Observability)
- **Horizon:** ~25 weeks (continuous thereafter for portfolio)

## 2026 Toolchain

| Phase | Tool | 2026 Version |
|-------|------|-------------|
| 3 | DuckDB | Latest + Iceberg extension |
| 4 | ETL/ELT | dbt Core **1.9** (microbatch incremental strategy) |
| 5 | Airflow | 2.9+ |
| 6 | dbt modeling | dbt Core 1.9 + Kimball, Star Schema |
| 7 | Kafka | Confluent/Redpanda 2026 |
| 8 | Lakehouse | **Apache Iceberg** (REST Catalog) + Delta Lake + Spark 3.5 |
| 9 | Observability | Great Expectations v1 + dbt tests |

## Files

- `learning-conventions.md` — session protocol, phase gates, output standards, skill unlock map
- `phase-roadmap.md` — per-phase curriculum, deliverables, exit criteria
- `progress.md` — phase completion tracker (agent reads this to enforce gates)

## Activation

```
Role: data-engineer
Overlay: overlays/retail-data-warehouse (learning/ subtree)
```

Last updated: 2026-09-08
