# Lease Content Overlay

This overlay contains content-specific extensions for the Lease in Vietnam and May Lanh Treo Tuong Astro content trees, enforcing the 5-Pillar Content Strategy (Intelligence, Information, Insights, Neighborhoods, Integration).

## Included Components

### Rules
- `rules/content-schema.md`: Strict Astro frontmatter schema (`unique_angle`, `anti_slop_gate`), enforcing `<AnswerFirst>` component over blockquotes.
- `rules/seo-baseline.md`: GEO/AEO baseline standards (1,400+ words, answer-first ≤60w, fact density ≥3 data points/500w, minimum 4-8 internal links).
- `rules/affiliate-links.md`: Link cloaking automation (`/go/partner`), placement guidelines (max 2 per article, prohibited in trust/scam content).

### Skills
- `skills/write-leaseinvietnam-maylanhtreotuong-data`: Drafting skill integrating 4 core templates (Market Radar, Guide, Scam Alert, Neighborhood) and E-E-A-T Experience Proof requirements.

### Workflows
- `workflows/publish-lease-content.md`: 6-step content production workflow and 7-day mix guardrails.

### Config
- `config/collections.md`: Site roots, corpus inventory (lease: 463 posts / 61 properties as of 2026-09-08), category-folder convention, Zod schemas, gate coverage, author registry.

## Corpus Index

The overlay consumes — and must stay consistent with — the per-repo content index:

- `leaseinvietnam/plan/CONTENT_INDEX.md`

Regenerate that index after every batch upgrade, then update `config/collections.md` with the new counts.

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
