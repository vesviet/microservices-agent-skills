---
name: content-audit-refresh
description: 4-Sprint workflow for auditing, repairing schema, expanding content, and enforcing link topology for vesviet.
version: 1.0.0
roles:
  - seo-analyst
  - content-writer
  - content-manager
---

# Content Audit & Refresh Workflow (`vesviet`)

This workflow dictates the 4-sprint operational execution plan for resolving technical content debt on the `vesviet` site.

## 4-Sprint Timeline

### Sprint 1: Schema Repair & GEO Baseline
- **`seo-analyst`**: Identify all files missing mandatory schema fields (`tags`, `categories`, `cover`).
- **`content-writer`**: Add the `> **Answer-first:**` summary blocks to the top 50 performing posts.
- **`content-manager`**: Ensure 100% schema validation passes.

### Sprint 2: Content Refresh & Technical Depth
- **`content-writer`**: Expand all underperforming articles and series sub-articles (currently < 1,400 words).
- **Injection**: Add Go struct code, Kubernetes manifests, system design sequence diagrams, and benchmarks.
- **Verification**: Ensure all target posts now exceed the 1,400+ word baseline.

### Sprint 3: Link Topology & Orphan Elimination
- **`seo-analyst`**: Map remaining orphan pages to the 10 Anchor Pillar Hubs (the original 124-page backlog was cleared in the 2026 campaign; treat any new orphan count as a regression).
- **`content-writer`**: Execute link injections from orphaned spokes up to the Hubs.
- **`content-manager`**: Maintain `reading-map.md` as 6 curated learning paths. Diversify `hire.md` anchor texts.
- **Verification**: Crawler must report 0 orphan pages (entry point: `vesviet/reports/check_posts.py`).

### Sprint 4: Consolidation & Redirects
- **`content-manager`**: Merge thin content (< 1,000w) into parent Series or monthly Tech Radar Digests.
- **`seo-analyst`**: Implement 301 Permanent Redirects via Hugo aliases and Cloudflare `_redirects` file.
- **Verification**: Run `hugo --gc --minify` to confirm zero build warnings or broken aliases.

### Failure Modes

- **Schema repair without GEO baseline**: a Sprint 1 audit focuses on tags and categories but skips the `> **Answer-first:**` block on the top posts. **Mitigation:** the sprint timeline requires both; reject the sprint as incomplete when the answer-first sweep is missing.
- **Content expansion drifts above 1,400 words without depth**: a writer expands to 1,400 words but adds fluff instead of code samples, manifests, sequence diagrams, and benchmarks. **Mitigation:** the Sprint 2 criteria require concrete technical depth; reject the expansion that does not add depth.
- **Orphan mapping skips regression pages**: Sprint 3 only links a subset of newly found orphan pages. **Mitigation:** the verification step requires zero orphan pages; reject the sprint when the count is non-zero.
- **Redirects ship without 301 Permanent status**: Hugo aliases or Cloudflare `_redirects` are added with 302 or no status. **Mitigation:** the verification step requires 301 Permanent; reject the change when the status is wrong.
- **Consolidation loses traffic**: a merge or redirect loses inbound links or canonical authority. **Mitigation:** Step 4 requires a 301 from every old URL to the new one; reject the merge when the redirect map is incomplete.
- **Build warnings after consolidation**: `hugo --gc --minify` reports warnings or broken aliases. **Mitigation:** the verification step requires zero warnings; reject the build that emits warnings.
- **Audit runs on stale corpus snapshot**: the audit uses `content-audit-report.json` from before the latest batch. **Mitigation:** rerun `reports/check_posts.py` first; reject audits whose scanned-file count differs from the live corpus count (367 files as of 2026-09-08).

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/seo-audit-report.json`** from Sprint 1, capturing the four-axis scores per file and the projected post-fix score.
- **`contracts/schemas/coordination-plan.json`** from Sprint 3, capturing the orphan mappings to the 10 Anchor Pillar Hubs.
- **`contracts/schemas/deployment-plan.json`** from Sprint 4, capturing the 301 Permanent redirects and the canonical URL decisions.