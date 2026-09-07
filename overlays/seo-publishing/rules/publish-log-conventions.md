# Publish Log & AI Visibility Tracking

Conventions for post-publish operational tracking. Once an article is published, the `content-writer` or `seo-analyst` must log it to ensure technical implementation and visibility tracking occurs.

## 1. Publish Log Data Points

For every published article, record:
- **Date Published**
- **Target Keyword & Search Intent**
- **Live URL Slug**
- **Pillar/Cluster Mapping**
- **Internal Links Used** (Source and Target)
- **Gen-AI impressions (first week)** — from Search Console's Generative AI report (worldwide since 2026-08-31); fill in ~7 days after publish

## 2. Schema Implementation Hand-off

- The `seo-analyst` must define the JSON-LD schema requirements (e.g., `Article`, `Review`, `RealEstateListing`, `FAQPage`) in the `seo-metadata.json`.
- The **Frontend Developer** is strictly responsible for implementing this JSON-LD schema into the codebase or CMS template based on the Analyst's spec.

## 3. Weekly AI Visibility Tracking (Rollup)

Traditional SEO tracking (Google Search Console impressions/clicks) is no longer sufficient. 
- **Weekly Task:** The `seo-analyst` must conduct a Weekly Rollup tracking **AI Visibility** across:
  1. **Search Console Generative AI report** (AI Overviews + AI Mode impressions, pages, countries, devices) — first-class KPI alongside classic Performance and Discover
  2. Google AI Overviews / AI Mode citation presence
  3. Perplexity AI Search
  4. ChatGPT / SearchGPT
- **Repeated sampling rule**: LLM brand recommendations are unstable across repeated queries — never conclude cited/not-cited from a single run; log multiple runs across different dates before drawing conclusions
- **Eligibility gate**: verify once that the site is included in "Search generative AI features" in Search Console (an opt-in gate for AI Overviews/AI Mode display)
- **Attribution hygiene**: parse `chatgpt.com` / `perplexity.ai` referrers in analytics; treat third-party AI-rank trackers with skepticism (none have access to Google internal metrics)
- **Feedback Loop:** If visibility is low, adjust `fact density` and `answer-first` structural rules for the next sprint — do NOT resort to information-distorting rewrites (they are now a detection target)

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
  See `See `core/skills/content/optimize-seo/SKILL.md` and the `seo-metadata.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/optimize-seo/SKILL.md` and the `seo-metadata.json` schema.

Last updated: 2026-09-01
