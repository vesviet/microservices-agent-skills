# Rabity — Data Engineering Progress

Track phase completion here. Update at the end of each week.  
The agent reads this file to enforce phase gates.

## Phase Status

| Phase | Module                       | Duration | Status      | Completed On | Notes |
| ----- | ---------------------------- | -------- | ----------- | ------------ | ----- |
| 1     | SQL + Analytics Foundation   | 2 tuần   | In Progress | —            |       |
| 2     | Python Data Stack            | 3 tuần   | Locked      | —            |       |
| 3     | Parquet + DuckDB + Polars    | 2 tuần   | Locked      | —            |       |
| 4     | ETL/ELT Architecture         | 3 tuần   | Locked      | —            |       |
| 5     | Airflow + Scheduling         | 2 tuần   | Locked      | —            |       |
| 6     | Data Warehouse Modeling      | 3 tuần   | Locked      | —            |       |
| 7     | Streaming / Kafka            | 4 tuần   | Locked      | —            |       |
| 8     | Lakehouse + Big Data         | 4 tuần   | Locked      | —            |       |
| 9     | Observability + Data Quality | 2 tuần   | Locked      | —            |       |
| 10    | Portfolio Projects            | Liên tục | Locked      | —            |       |

## Legend

| Status      | Meaning                                          |
| ----------- | ------------------------------------------------ |
| Locked      | Exit criteria of previous phase not yet satisfied |
| In Progress | Currently active; exit criteria not yet complete  |
| Done        | All exit criteria satisfied; next phase unlocked  |

## Exit Criteria Log

Use this section to record when specific exit criteria are met.

### Phase 1

- [ ] Can write GROUP BY + HAVING without reference
- [ ] Can write a self-join or multi-table join with correct alias usage
- [ ] Can use ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) correctly
- [ ] Deliverables committed to `phase-1-sql-foundation/`
