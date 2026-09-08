# Vesviet Content Overlay

Content + SEO overlay for the `vesviet` (English flagship, tanhdev.com) and `learn` (Vietnamese twin, learn.tanhdev.com) Hugo sites. This overlay is the content/SEO center of gravity for the `vesviet-team` pack: it owns the Technical Article Standard 2027, the twin SEO authority model, and the drafting/auditing skills that implement them.

## Included Components

### Rules
- `rules/content-brand.md`: schema completeness, GEO/AEO Answer-First, 1,400+ word depth, Affiliate Compliance, 2026 Information Gain & E-E-A-T, Masterclass Twin publishing model.
- `rules/technical-article-2027.md`: the 7 Technical Content Gates for engineering articles — answer-first, production-grade code (zero pseudo-code, version-pinned), quantitative depth (≥3 verifiable data points / 500 words), Mermaid visualization, Production Failure reality, trade-off framing, verifiable claims.
- `rules/link-topology.md`: Hub-and-Spoke architecture (10 Anchor Pillar Hubs), one-way `learn → vesviet` authority flow, orphan elimination.
- `rules/seo-authority.md`: twin SEO authority model — canonical/duplication policy (2026-2027 spam rules), AI citation readiness (GEO 2027), entity consistency, on-page technical SEO, per-engine citation KPIs.

### Workflows
- `workflows/content-audit-refresh.md`: 4-sprint remediation for `vesviet` (Schema Repair, Expansion, Topology, Consolidation).
- `workflows/affiliate-publishing.md`: affiliate/hybrid SEO content production for `learn`.
- `workflows/masterclass-batch-upgrade.md`: deep-research batch upgrades (100 rounds → 20 posts) that produced Batches 1–5.
- `workflows/publish-series.md`: bilingual series production across both sites.

### Skills
- `skills/write-vesviet-learn-content` (`content-writer`): drafting skill implementing the 2027 gates, twin model, and affiliate trust requirements.
- `skills/audit-technical-article` (`seo-analyst`): per-gate audit of technical articles against `rules/technical-article-2027.md`, emitting `seo-audit-report.json`.

### Config
- `config/sites.md`: site roots, corpus inventory (vesviet 367 / learn 440 files as of 2026-09-08), twin model, cross-site authority rules.

## Corpus Indexes

The overlay consumes — and must stay consistent with — the per-repo content indexes:

- `learn/plan/CONTENT_INDEX.md`
- `vesviet/reports/CONTENT_INDEX.md`

Regenerate those indexes after every batch upgrade or series change, then update `config/sites.md` with the new counts.

This overlay should be composed with the global core, not copied into the core pack.

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

Last updated: 2026-09-08
