---
description: Workflow for SEO Analyst to research search intent, produce a content brief covering traditional search, GEO/AEO, and topical authority — ready for Content Writer to draft from
---

## SEO Keyword Brief Workflow

Use this workflow when a topic or URL needs a structured SEO content brief before drafting begins. The output is a `seo-content-brief.json` that Content Writer and publishers can execute without re-researching keywords or link strategy.

### When To Use

- a new article or landing page needs an SEO brief before writing starts
- a weekly or sprint topic board requires keyword assignment and link targets
- a topic cluster needs pillar–cluster mapping before any content is commissioned
- a user request specifies a target keyword or content gap to fill

### Prerequisites

- the topic or target URL is known
- access to SERP results, People Also Ask, or Search Console data is available
- the site's existing published content is accessible for cannibalization check

### Workflow Steps

#### 1. Frame The Intent

Role: **SEO Analyst**

Use skill: `optimize-seo`

Capture before researching:

- what is the target topic or user request?
- who is the target audience and what stage are they at (awareness, consideration, decision)?
- what is the primary search intent: informational, commercial, navigational, or transactional?
- what is the target site and content type (article, landing page, comparison, FAQ)?
- does this need to feed a sprint deadline or topic board?

#### 2. Research The SERP Landscape

Role: **SEO Analyst**

Use skill: `optimize-seo`

Run at least one SERP scan and one People Also Ask pass:

- identify the top-3 ranking results and their content formats
- extract the main keyword and 2–4 secondary keywords
- note the dominant content format (listicle, guide, comparison, FAQ, how-to)
- check AI Overviews (Google), Perplexity, and ChatGPT for the query — note answer format and cited sources
- document query fan-out: 3–5 related sub-questions the article should cover

Use skill: `conduct-research` when competitor depth or domain authority context is needed.

#### 3. Check Cannibalization And Internal Links

Role: **SEO Analyst**

Before finalizing the keyword:

- scan the site's recent publish history (default: 7-day window when a topic board exists) for keyword conflicts
- if a similar keyword was targeted recently, adjust focus keyword or angle to avoid overlap
- identify 3+ existing site URLs that are strong internal link candidates for this article
- note anchor text rationale and destination path for each

#### 4. Map Topical Authority Position

Role: **SEO Analyst**

Assign the article to the site's topical cluster:

- classify as: pillar, supporting cluster, or supplementary
- if supporting or supplementary, identify the pillar page URL to link to
- document the non-commodity element: what this article adds beyond the current top-3 SERP results
- classify content freshness type: `new_topic` | `evergreen_refresh` | `data_update` | `experience_addition`
- list key entities (brands, people, concepts, locations) that must appear for topical coverage

#### 5. Define E-E-A-T Requirements

Role: **SEO Analyst**

Specify what experience signals the article must contain:

- experience proof type required: original_photo, firsthand_account, documented_test, expert_interview, or case_study
- author entity requirement: link to author profile with Person schema?
- YMYL flag: is this topic in a trust-sensitive domain (financial, health, legal, safety)?
- trust signals required: source citations, contact info, policy page links

#### 6. Specify Structured Data And GEO/AEO Requirements

Role: **SEO Analyst**

Document for the Content Writer:

- schema types recommended: Article (always), FAQPage (when FAQ present), HowTo (when step-by-step), Product (when linking product pages)
- answer-first requirement: opening ≤60 words per H2 section
- answer format per major section: definition, comparison table, numbered steps, or bullet list
- minimum fact density: 3 verifiable data points per 500 words
- AI bot crawlability: flag if robots.txt blocks OAI-SearchBot, PerplexityBot, ClaudeBot, or BingBot

Note: schema implementation is escalated to Frontend — SEO Analyst specifies types, Frontend deploys JSON-LD.

#### 7. Write The On-Page Spec

Role: **SEO Analyst**

Produce the on-page requirements that Content Writer will follow:

- primary keyword (with search volume estimate if available)
- 2–4 secondary keywords
- title tag draft (≤60 chars, primary keyword near front)
- meta description draft (≤160 chars, primary keyword, CTA)
- URL slug recommendation
- suggested H2 structure (mirroring natural language queries: "How to...", "What is...")
- FAQ block: at least 3 questions from People Also Ask when applicable
- minimum word count target (default: 1,400+)
- 3+ internal links with anchor text

#### 8. Produce And Deliver The Brief

Role: **SEO Analyst**

Use skill: `optimize-seo`

Emit `seo-content-brief.json` conforming to the pack schema.

Confirm:

- all required fields populated
- internal link targets are real URLs on the site
- cannibalization check result documented
- E-E-A-T requirements clearly stated for Content Writer to implement
- no ranking guarantees — recommendations are tied to observable SERP gaps only

Hand off the brief to Content Writer for drafting.

### Checklist

- [ ] topic, audience, and intent framed
- [ ] SERP landscape researched — top results and AI search format noted
- [ ] primary and secondary keywords defined
- [ ] cannibalization check completed — no keyword conflict in recent publishes
- [ ] 3+ internal link candidates identified with anchor rationale
- [ ] topical authority position assigned (pillar, cluster, supplementary)
- [ ] non-commodity value documented
- [ ] E-E-A-T requirements specified
- [ ] GEO/AEO requirements specified (answer-first, fact density, schema types)
- [ ] on-page spec complete: title, meta, slug, H2 structure, FAQ, word count
- [ ] seo-content-brief.json emitted and handed off to Content Writer

### Related Workflows

- [content-publishing](content-publishing.md)
- [troubleshooting](troubleshooting.md)

### Related Skills

- **optimize-seo**: Research keywords, audit on-page elements, produce SEO briefs
- **conduct-research**: Deeper domain or competitor research when SERP scan is insufficient
- **analyze-data**: Formal GSC/CTR tables and AI citation tracking when baselines are needed

### Failure Modes

- **Brief without intent**: a brief is produced without a clear search intent (informational, commercial, navigational, transactional). **Mitigation:** the brief must declare the intent and the primary keyword before the H2 outline is written.
- **Cannibalization ignored**: the brief targets a primary keyword that is already covered by another URL. **Mitigation:** resolve the conflict by consolidation, intent differentiation, canonical, 301-redirect, or anchor cleanup before publishing the brief.
- **YMYL without E-E-A-T**: a YMYL-adjacent brief is shipped without the experience proof and author entity requirements. **Mitigation:** require the E-E-A-T gate for YMYL; require human expert review.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/seo-content-brief.json`** — capture the H2 outline, the answer-first guidance, the FAQ, the internal link targets, the word-count band, the GEO/AEO fields, the schema requirements, and the E-E-A-T gates.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a brief may reframe the user goal through off-target keyword recommendations. **Mitigation:** cross-check the brief against the source feature ticket; reject reframed goals.
- **ASI03 Identity & Privilege Abuse**: every YMYL-adjacent brief must require the SME sign-off; reject briefs that target YMYL topics without the E-E-A-T gate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a brief as "guaranteed to rank" without evidence; surface the residual risk and the actual ranking baseline honestly.

