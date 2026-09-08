---
name: masterclass-batch-upgrade
description: Deep-research-driven batch upgrade of 20 architecture posts per batch on the learn/vesviet twin sites, following the Batch 1-5 campaign pattern.
version: 1.0.0
roles:
  - seo-analyst
  - content-writer
  - reviewer
  - content-manager
---

# Masterclass Batch Upgrade Workflow (`learn` + `vesviet`)

This workflow reproduces the deep-research-driven upgrade campaign that produced
Batches 1–5 (70 posts upgraded to masterclass standard). One batch = 100 research
rounds = 5 clusters × 20 rounds = 20 upgraded posts.

## Preconditions

- Target batch list defined (20 posts, numbered e.g. 71–90 for Batch 6).
- Content indexes refreshed: `learn/plan/CONTENT_INDEX.md`, `vesviet/reports/CONTENT_INDEX.md`.

## 5-Step Production Workflow

### Step 1: Deep Research (100 rounds) (`seo-analyst` + research)
- Partition 100 rounds into 5 technical clusters (20 rounds each) mapped 1:1 to groups of 4 target posts.
- Each round captures: experimental results, algorithms, distributed models, complexity analysis, and performance benchmarks, all traceable to primary sources.

### Step 2: Publish Batch Report (`content-writer`)
- Write `learn/content/posts/deep-research-batch-N-100-rounds-report.md` (Vietnamese, `draft: true`, `noTranslation: true`).
- Structure: overview table (5 clusters → 4 posts each), then per-cluster round-by-round notes.
- The report stays on `learn` only; never mirror to `vesviet`.

### Step 3: Upgrade 20 Posts (`content-writer`)
For each target post:
- Enforce masterclass bar: >20 KB, >2,500 words, production-grade code (zero pseudo-code), standardized Mermaid diagrams, quantitative comparison tables.
- Pass the 7 Technical Content Gates (`rules/technical-article-2027.md`): per-section BLUF, version-pinned code, ≥3 verifiable data points per 500 words with benchmark conditions, Production Failure story, rejected-alternative framing, primary-sourced claims.
- Keep `> **Answer-first:**` block; extend, never rewrite, published substance.
- Keep `canonicalURL` on the file's own host; twins never cross-canonicalize.

### Step 4: Sync English Flagships (`content-writer`)
- Mirror the upgraded substance into the `vesviet` twin posts as an expanded English masterclass that adds information gain beyond translation (2026-2027 spam policy).
- Verify: Answer-first intact, hub links intact, zero `learn.tanhdev.com` references on `vesviet`.

### Step 5: Audit & Index Refresh (`reviewer` + `seo-analyst`)
- Run `audit-technical-article` per post: per-gate scores, Blocking findings for Gate 2/6/7 failures.
- Refresh both corpus indexes with new counts, batch table row, and compliance snapshot.
- Rerun `vesviet/reports/check_posts.py`; update `content-audit-report.json`.

### Failure Modes

- **Research rounds not traceable**: a round cites a benchmark without a primary source. **Mitigation:** Step 1 requires traceable rounds; reject the round and re-research before drafting.
- **Batch report published**: the `deep-research-batch-N` post ships with `draft: false`. **Mitigation:** Step 2 pins `draft: true`; reject the publish toggle (internal artifact).
- **Upgrade rewrites instead of extends**: an editor replaces published substance and breaks inbound anchor equity. **Mitigation:** Step 3 requires extend-only; reject the diff when canonical sections are removed.
- **Pseudo-code in masterclass**: an upgraded post keeps placeholder snippets. **Mitigation:** Step 3 requires production-grade code; reject the post until snippets compile conceptually.
- **Twin drift after sync**: the English flagship misses the upgraded substance or loses Answer-first/hub links. **Mitigation:** Step 4 verification gates the sync; reject when coverage is partial.
- **Reverse authority link introduced**: the sync adds a `learn.tanhdev.com` link into `vesviet` content. **Mitigation:** Step 4 verification rejects any occurrence; remove before merge.
- **Stale corpus indexes**: the batch ships without refreshing both CONTENT_INDEX files. **Mitigation:** Step 5 makes the refresh mandatory; reject the batch close when indexes are stale.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/research-report.json`** from Step 1, capturing the 100-round cluster map, citations, and the YMYL flag.
- **`contracts/schemas/content-handoff.json`** from Steps 3–4 per post, capturing the masterclass gate verdict (word count, code grade, Mermaid count, internal links).
- **`contracts/schemas/seo-audit-report.json`** from Step 5 (via `audit-technical-article`), capturing the 7-gate scores, post-upgrade compliance scores, and the refreshed corpus counts.
