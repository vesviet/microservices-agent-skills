# Vesviet Content Rules

Voice, style, structure, and publishing constraints for the Vesviet portfolio site and Learn site.

## Role Integration

- **`content-writer`**: Must adhere to these rules when drafting content.
- **`seo-analyst`**: Must audit against these rules (frontmatter, GEO/AEO answer-first formats, internal linking) before publish.
- **`reviewer`**: Must enforce AI Governance, Information Gain, and E-E-A-T requirements before code review passes.

## Directory Structure

Content on Vesviet must be organized into these three directories based on purpose:
- **`posts/`**: In-depth technical articles and tutorials.
- **`radar/`**: Periodic Tech Radar newsletters (e.g., industry news, tool updates), filed as `content/radar/YYYY-MM/radar-YYYY-MM-DD[-slug].md`.
- **`series/`**: Linked chains of articles on a specific topic.

Content on Learn adds:
- **`content/docs/`**: Hugo Book layout documentation (`overview.md`, `affiliate-website-report.md`).
- **Deep-research batch reports**: published only on `learn` under `content/posts/deep-research-*.md` with `draft: true` and `noTranslation: true`; never mirrored to `vesviet`.

## Masterclass Twin Model

- Every flagship topic ships as a **Vietnamese twin on `learn`** (research notes, canonical for notes) and an **expanded English masterclass on `vesviet`** (authority site).
- Masterclass quality bar (from the Batch 1–5 deep-research campaign): >20 KB, >2,500 words, production-grade code with zero pseudo-code, standardized Mermaid diagrams, quantitative comparison tables, ≥3 internal links.
- When upgrading a batch: run deep research first (100 rounds → 5 clusters × 20 rounds), publish the report on `learn` as a draft, then upgrade the 20 target posts.
- Batch reports and internal summaries stay `draft: true` — they are process artifacts, not public content.

## Frontmatter Requirements

Every new file must include the following mandatory frontmatter fields to pass the 100% Schema Completeness audit:
```yaml
---
title: "..."
slug: "..."
author: "..."
date: "YYYY-MM-DDTHH:MM:SS+07:00"
lastmod: "YYYY-MM-DDTHH:MM:SS+07:00"
draft: false
description: "..."
tags: ["...", "..."]
categories: ["...", "..."]
cover: 
  image: "images/posts/cover-image.png"
  alt: "..."
ShowToc: true
TocOpen: true
---
```
*Note: Add `mermaid: true` if the post contains Mermaid diagrams.*

## Content Depth & Formatting (GEO/AEO)

- **Answer-First**: The introduction MUST begin with `> **Answer-first:**` followed by a direct, concise answer to the topic's core question in ≤60 words.
- **Content Depth**: All technical articles and pillar posts must target a minimum length of **≥ 1,400 words**. Do not publish thin content (<1,000w) as standalone pages.
- **Tone**: Professional, technical deep-dive. Get straight to the point, no fluff.
- **Alerts**: Use GitHub Markdown Alerts strategically (`> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`) to highlight key information instead of bold text.

## Affiliate Compliance (Learn Site)

- **Link Tagging**: All outbound affiliate links must use `rel="sponsored"`.
- **Disclosures**: A clear affiliate disclosure must be present on any page containing affiliate links, located near the recommendation.

## 2026 Information Gain & E-E-A-T Requirements

To combat the commoditization of AI-generated content, all in-depth articles MUST include explicit Information Gain:
- **Firsthand Experience**: The writer must include real-world anecdotes or "Production Failure" stories to prove human expertise.
- **Expert Quotes & Sourcing**: If applicable, quote Subject Matter Experts (SMEs). Never rely solely on AI-synthesized knowledge.
- **Zero Raw Hallucinations**: Do not inject generic boilerplate phrasing. Every technical claim must be verifiable.

## Assets & Internal Linking

- **Images**: Store all image files in `static/images/` or `assets/images/`.
- **Image Links**: Use absolute root-relative paths in Markdown (e.g., `![Alt Text](/images/filename.png)`).
- **Internal Links**: Use standard Markdown linking pointing directly to the slug (e.g., `[Link Text](/posts/magento-still-worth-investing-2026)`).
- **Cross-Site Twin Links**: Only `learn` → `vesviet`. On `learn`, the Vietnamese article links up to the English flagship with the `> 🇬🇧 **Read the English version of this article on [tanhdev.com](https://tanhdev.com/posts/<slug>/)**` callout. `vesviet` must never link back to `learn.tanhdev.com` (one-way authority flow).
- **Canonical URLs**: Every post declares `canonicalURL` on its own host. Never cross-canonicalize between twins — each twin is canonical on its own site.

## Series & Production Failure Rules

- **Production Failure stories**: Use the standardized template:
  ```markdown
  > 🔥 **[Production Failure]: <Title>**
  > **Symptom:** ...
  > **Root Cause:** ...
  > 📊 **Impact:** ...
  > 📈 **Resolution:** ...
  > *(Source: ...)*
  ```
- **Prerequisite block**: Every series part must open with a `> **Prerequisite:**` blockquote.
- **CTA**: Every series part must close with `🔗 **Next Step:**` linking to the next part.
- **Bilingual Rule**: Use Vietnamese colloquial phrasing where it aids clarity, but keep technical terminology in English (e.g., "Context Window", "Prompt Injection") and provide English equivalents on first mention.

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
  See `See `core/skills/content/write-article/SKILL.md` and the `content-handoff.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/write-article/SKILL.md` and the `content-handoff.json` schema.

Last updated: 2026-09-08
