# Technical Article Standard 2027

The 2027 quality bar for technical articles on `vesviet` and `learn`. This rule
extends `content-brand.md` with the technical-writing gates that core
`write-article`/`optimize-seo` do not cover for engineering masterclasses.

## Role Integration

- **`content-writer`**: must satisfy every gate below when drafting or upgrading technical posts and series parts.
- **`seo-analyst`**: audits against these gates via the `audit-technical-article` skill before publish.
- **`reviewer`**: enforces the Information Gain and code-verifiability gates in review.

## The 7 Technical Content Gates

### Gate 1 — Answer-First Engineering Summary
- Open with `> **Answer-first:**` (≤60 words) stating the architecture decision, the constraint, and the measured outcome (e.g. "583,000 TPS via peak shaving with RocketMQ multi-tier queues").
- Each H2 section opens with its own BLUF ≤60 words (atomic RAG chunking); no slow-burn intros.

### Gate 2 — Production-Grade Code Only
- Zero pseudo-code. Every snippet is complete, runnable, and version-pinned (e.g. Go 1.26, Kubebuilder v4, Dapr 1.15).
- Code must compile conceptually: correct imports, error handling, context propagation, graceful shutdown where applicable.
- Config files must be real deployable artifacts (Kubernetes manifests, wrangler.toml fragments, Dockerfile stages) — never abstract skeletons.

### Gate 3 — Quantitative Depth
- Minimum 3 verifiable data points per 500 words (benchmark numbers, latency percentiles, throughput, cost figures) with primary sources.
- Comparison tables must be quantitative (p50/p95/p99, allocs/op, TPS, $/req) — not feature checkboxes.
- State the measurement conditions (hardware, dataset size, Go version, flags) for every benchmark.

### Gate 4 — Architecture Visualization
- Mermaid is the diagram standard: sequence diagrams for flows, `graph TD` for topology, C4-style for system context.
- Diagrams must be readable standalone (labeled edges, real component names, no "Service A/B").
- Frontmatter must set `mermaid: true` when diagrams are present.

### Gate 5 — Failure & Production Reality
- Include at least one "Production Failure" story (template in `content-brand.md`) or a concrete failure-mode analysis per deep-dive.
- Cover the operational side: capacity limits, degradation behavior, blast radius, rollback path.
- Never present a pattern as free: state its cost (latency added, complexity, operational burden).

### Gate 6 — Trade-off Framing 2027
- Every architectural recommendation must present the alternative rejected and why (e.g. "OceanBase Multi-Paxos over CockroachDB Raft because of ...").
- Include decision matrices when comparing ≥3 options.
- 2026-2027 spam policy: no near-identical cross-site duplication; the English twin must add measurable new information gain over the Vietnamese twin, not just translation.

### Gate 7 — Verifiable Claims & Anti-Hallucination
- Every technical claim traces to a primary source (official docs, RFC/design paper, conference talk, own benchmarks) — no AI-synthesized facts.
- Version-sensitive claims must pin the version (e.g. "Green Tea GC in Go 1.26", not "new Go GC").
- Numbers that cannot be sourced must be presented as the author's own measurement with conditions stated.

## Masterclass Length Bar

- Flagship deep-dives: >2,500 words / >20 KB (Batch-campaign standard).
- Radar entries and trust pages are exempt from the length bar but not from Gates 1, 6, 7.

## Failure Modes

- **Runnable-check fails**: a snippet uses pseudo-code or invented APIs. **Mitigation:** Gate 2; reject at review.
- **Benchmark without conditions**: a number appears with no hardware/version context. **Mitigation:** Gate 3; reject or mark as own measurement.
- **Version-unpinned claim**: "Kubernetes supports X" without version. **Mitigation:** Gate 7; reject until pinned.
- **Free-lunch pattern**: a pattern is recommended with no cost analysis. **Mitigation:** Gate 5; reject the recommendation.

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
  See `core/skills/content/optimize-seo/SKILL.md` and the `seo-audit-report.json` schema
  for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

Last updated: 2026-09-08
