# Learning Conventions — Data Engineer Rabity

Session protocol, phase-gate rules, output standards, and anti-patterns
specific to Rabity's data engineering self-study practice. These extend
`core/roles/data-engineer.md` guardrails with learning-context rules.

## Session Protocol

Every study session MUST follow this structure:

1. **State the phase** — Declare which Phase is active (e.g., `Phase 2: Python Data Stack`)
2. **State the goal** — One sentence describing what will be practiced or built today
3. **Build the thing** — Hands-on only; no passive reading counts as session output
4. **Log the output** — Commit or save the artifact produced (script, notebook, report)
5. **Reflect** — Note one thing learned and one open question

## Phase Gate Rules

- An agent operating in this overlay MUST enforce phase gates.
- A phase is **locked** until all exit criteria in `rules/phase-roadmap.md` are satisfied.
- If a user attempts to skip to a locked phase, the agent MUST surface the unmet exit
  criteria and offer to work through them first.
- The agent MUST NOT silently allow locked-phase content to be treated as current work.

## Output Standards

All hands-on outputs from practice sessions MUST conform to:

| Output Type      | Standard                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Python scripts   | PEP 8, no hardcoded paths, argument-driven via `argparse` or env  |
| SQL files        | `.sql` extension, one statement per file, commented with purpose  |
| Notebooks        | Saved as `.ipynb`, cells executed top-to-bottom, outputs cleared  |
| Data files       | Never committed to version control; add to `.gitignore`           |
| Reports          | Follow `core/roles/data-engineer.md` Output Template             |
| Project folders  | Named `phase-<N>-<slug>/`, e.g., `phase-2-python-stack/`         |

## Skill Unlock Map

Skills become available as phases are completed. The agent enforces this map:

| Phase Unlocked | Skills Activated                                       |
| -------------- | ------------------------------------------------------ |
| 1 complete     | SQL querying, window functions, basic analytics        |
| 2 complete     | pandas, numpy, matplotlib, openpyxl, data cleaning     |
| 3 complete     | DuckDB, Polars, Parquet read/write, Arrow format       |
| 4 complete     | ETL scripting, ELT patterns, pipeline design           |
| 5 complete     | Airflow DAG authoring, scheduling, task dependencies   |
| 6 complete     | Star schema, Kimball modeling, dbt fundamentals        |
| 7 complete     | Kafka producers/consumers, stream processing concepts  |
| 8 complete     | Delta Lake, Iceberg, Spark, Lakehouse architecture     |
| 9 complete     | Great Expectations, dbt tests, observability patterns  |
| 10+ ongoing    | Full stack — portfolio project with all skills active  |

## Anti-Patterns To Reject In Learning Context

- Reading documentation without a corresponding hands-on exercise
- Treating tutorial code as personal output — must be rewritten from scratch
- Skipping the reflection log at session end
- Moving to the next phase without completing the exit-criteria deliverable
- Using AI to generate entire solutions without understanding each step
- Committing raw data files (CSV, Excel, Parquet) to version control
- Leaving notebooks with un-executed or error cells before closing a session

## Progress Tracking Convention

Maintain a `progress.md` file at the overlay root to track phase completion:

```markdown
# Rabity — Data Engineering Progress

| Phase | Status      | Completed On | Notes          |
| ----- | ----------- | ------------ | -------------- |
| 1     | In Progress | —            | Week 1 of 2    |
| 2     | Locked      | —            |                |
...
```

Update this file at the end of each week. The agent will read it to determine
which phases are unlocked when enforcing phase gates.

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
  See `See `core/skills/foundation/create-migration/SKILL.md` and the `schema-migration.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/create-migration/SKILL.md` and the `schema-migration.json` schema.

Last updated: 2026-09-01
