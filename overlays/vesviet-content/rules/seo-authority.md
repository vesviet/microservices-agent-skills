# SEO Authority Rules 2027

SEO-specific authority and citation rules for the `vesviet`/`learn` twins,
split out from `link-topology.md` (which owns site structure). The core
GEO/AEO/AI-citation standard lives in `core/skills/content/optimize-seo`;
this rule adds the twin-corpus specifics.

## Role Integration

- **`seo-analyst`**: owns these rules in audits and briefs.
- **`content-writer`**: must implement the on-page requirements when drafting.

## Twin SEO Model (Authority Split)

- `tanhdev.com` (vesviet, `en`): the **citation target** — English masterclasses that AI engines (AI Overviews, Perplexity, ChatGPT) quote. Hosts the strongest E-E-A-T signals: author entity, 17+ years experience proof, consulting conversion.
- `learn.tanhdev.com` (learn, `vi`): the **research corpus + Vietnamese market layer**. Serves Vietnamese queries and feeds authority up to the flagship.
- One-way flow `learn → vesviet` only (see `link-topology.md`); 0 links from `vesviet` to `learn.tanhdev.com`.

## Canonical & Duplication Rules (2026-2027 spam policy)

- Each twin is canonical on its own host (`canonicalURL` on own domain). Never cross-canonicalize twins — both are legitimate localized assets, not duplicates.
- NEVER near-duplicate publish: the English twin must add measurable information gain (expanded benchmarks, extra failure cases, English-market context) over the Vietnamese twin. Translation-only mirrors violate scaled-content-abuse policy.
- No page-per-query-variant sprawl: one canonical URL per intent; use FAQ blocks for query fan-out.

## AI Citation Readiness (GEO 2027)

- **Citation-ready sentences**: tight, factual, ≤25 words, self-contained (numbers + conditions + source) — these are what AI engines quote.
- **Entity consistency**: identical author facts (`Lê Tuấn Anh`, Go backend architect, 17+ years) across both hosts, `hire.md`, about pages, and schema.org `Person` markup.
- **Citation measurement**: per engine, multiple runs, logged over dates — never conclude from a single run (LLM recommendations are unstable).
- **Honest fact density**: over-claiming to sound citable is a suppression risk (Counter-GEO detection); keep numbers honest.
- **AI-bot crawlability**: `robots.txt` must permit OAI-SearchBot, PerplexityBot, ClaudeBot, BingBot — audit on every release.

## On-Page Technical SEO

- Answer-first block within the first screen; H2 mirrored to natural-language queries; `## FAQ` with `### Question?` subheads when present.
- Schema.org JSON-LD: `TechArticle` + `Person` author on every post; `FAQPage` when FAQ present; `BreadcrumbList` on series.
- Internal links: ≥3 per post; flagship posts link within their cluster (hub-and-spoke, `link-topology.md`).
- hreflang: declare `vi`/`en` alternates between twin pairs at the site level; keep `noTranslation: true` on Vietnamese-only internals (deep-research reports).

## Authority KPI Targets

- Flagship posts: answer-first compliance 100%, ≥3 verifiable data points per 500 words, ≥1 Mermaid diagram, ≥3 internal links.
- Corpus: 0 orphan pages, 0 broken internal links, 0 reverse-authority links.
- Track per-engine citation presence monthly (logged runs), Search Console impressions/CTR weekly.

## Failure Modes

- **Translation-only twin published**: the English twin adds no new information gain. **Mitigation:** the duplication rule requires measurable gain; reject the publish.
- **Single-run citation conclusion**: the team reports "cited/not cited" from one check. **Mitigation:** the measurement rule requires multiple logged runs per engine.
- **AI-bot blocked**: `robots.txt` regresses and blocks an AI crawler. **Mitigation:** the crawlability audit runs every release; flag as Blocking finding.
- **Cross-canonicalized twins**: a twin points `canonicalURL` at the other host. **Mitigation:** the canonical rule forbids it; reject the frontmatter.

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
