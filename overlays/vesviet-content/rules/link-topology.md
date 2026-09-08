# Hub-and-Spoke Internal Link Topology

This rule defines the mandatory internal linking architecture for `vesviet` (and, in adapted form, `learn`) to ensure optimal link equity distribution and eliminate orphan pages.

## Core Principle
All content must be organized into a Hub-and-Spoke architecture. No page should exist in isolation (Zero Orphan Policy).

## The 10 Anchor Pillar Hubs
There are 10 core hubs that anchor the site (all under `content/`):
1. `posts/go-microservices.md` — Go & Microservices Architecture Hub
2. `posts/architecting-21-service-ecommerce-golang-ddd.md` — System Design & E-Commerce Hub
3. `posts/aws-eks-vs-ecs-comparison.md` — Cloud Native & Container Infrastructure Hub
4. `posts/banking-microservices-architecture.md` — FinTech & Core Banking Systems Hub
5. `posts/cloudflare-d1-durable-objects-realtime-cart.md` — Edge Serverless & Cloudflare Hub
6. `posts/deploying-astro-on-cloudflare-full-stack-edge-architecture.md` — AI Frontend & Edge Hub
7. `posts/generative-ui-with-mcp-ai-native-frontend.md` — Generative UI & MCP Engineering Hub
8. `posts/alipay-double-11-architecture-tps.md` — Distributed Systems & High Concurrency Hub
9. `reading-map.md` — Sitewide Curated Learning Directory Hub (6 pillars)
10. `hire.md` — Commercial Architecture Consulting Conversion Hub

## Link Injection Requirements
- **Spokes to Hubs**: Every new series sub-article, daily radar briefing, or standalone post MUST include an internal link pointing up to at least one relevant Anchor Pillar Hub.
- **Hubs to Spokes**: Hub pages must curate and link down to their respective spokes.
- **Cross-Linking**: Use contextually relevant anchor text. Avoid repetitive boilerplate links (e.g., diversify "Hire Me" anchor text with "Consult on Go Microservices").

## Twin Topology (learn)

- On `learn`, the equivalent backbone is `content/series/_index.md` (25-series library index), pillar per-topic `posts/`, and `content/reading-map.md`.
- Vietnamese series parts link laterally to sibling chapters via the standard `🔗 **Next Step:**` CTA and up to the series `_index.md`.
- The **only** sanctioned outbound-from-learn link pattern for twins is the up-to-flagship callout defined in `rules/content-brand.md`.

## One-Way Authority Flow (learn → vesviet)

- Authority flows one direction only: `learn.tanhdev.com` → `tanhdev.com`.
- 0 `learn.tanhdev.com` links may appear in `vesviet/content/**`. Adding one is a gate failure, not a style nit.
- Rationale: `tanhdev.com` is the consolidated E-E-A-T authority site; backlinks from the notes twin would leak equity and duplicate topical signals.

## Orphan Elimination
- The SEO Analyst must run crawler verifications before publishing to ensure **0 orphan pages** remain in the repository.
- Use `vesviet/reports/check_posts.py` as the in-repo verification entry point; refresh `vesviet/content-audit-report.json` after every batch (last full scan predates the Batch 4–5 growth: 275 files scanned vs 367 current).

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

Last updated: 2026-09-08
