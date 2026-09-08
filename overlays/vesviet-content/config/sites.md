# Vesviet Content Sites

Site roots, corpus inventory, and cross-site authority rules for the two Hugo twins.
Snapshot: 2026-09-08. Canonical indexes: `learn/plan/CONTENT_INDEX.md` and
`vesviet/reports/CONTENT_INDEX.md` — regenerate those before updating this file.

## Site Roots

| Site | Repo path (workspace-relative) | Public host | Language | Role |
|------|-------------------------------|-------------|----------|------|
| Vesviet (portfolio flagship) | `vesviet/` | `https://tanhdev.com/` | `en` | Authority site: expanded English masterclasses, tech radar, consulting conversion (`hire.md`) |
| Learn (notes / research) | `learn/` | `https://learn.tanhdev.com/` | `vi` | Vietnamese twin: research notes, series library, deep-research batch reports |

Both sites use Hugo + PaperMod. `learn` additionally runs a Hugo Book layout under `content/docs/`.

## Corpus Inventory (2026-09-08)

| Corpus | Vesviet | Learn |
|--------|---------|-------|
| Posts | 66 | 86 (7 internal reports `draft: true`) |
| Series dirs | 25 | 25 |
| Series files | 246 | 259 (218+ chapters) |
| Radar editions | 26 (2026-04 → 2026-09) | — |
| Docs | — | 3 (Hugo Book) |
| Total content files | 367 | 440 |

## Masterclass Twin Model

- Each flagship topic ships as a Vietnamese twin on `learn` (canonical notes) and an
  expanded English masterclass on `vesviet` (authority).
- Batch 1–5 deep research (5 × 100 rounds) has upgraded 70 posts on `learn` and the
  mirrored flagships on `vesviet` to masterclass standard: >20 KB, >2,500 words,
  production-grade code, standardized Mermaid, quantitative tables.
- Deep-research reports live only on `learn` as `draft: true` posts
  (`deep-research-100-rounds-report.md`, batches 3/4/5) — never publish on `vesviet`.

## Cross-Site Authority Flow (one-way)

- `learn` → `vesviet` only. 90 learn files link up to the English flagship via the
  `> 🇬🇧 Read the English version...` callout.
- `vesviet` → `learn` links are FORBIDDEN (0 occurrences as of snapshot; keep it that way).
- `canonicalURL` frontmatter always points at the file's own host — learn posts
  canonicalize to `learn.tanhdev.com`, vesviet posts to `tanhdev.com`.

## Publishing Notes

- Keep site roots and publishing notes here instead of in the global core.
- Answer-first coverage targets: vesviet 61/66 posts, learn 69/86 posts (drafts exempt).
- Radar is vesviet-only (`content/radar/YYYY-MM/`), monthly editions.
