# Content Manager Governance Standards & Quality Protocols

This reference document defines the operational governance standards for [`content-manager`](../content-manager.md), covering Top 10 SERP Information Gain evaluation, Expert Authenticity verification, 3-tier content decay triage, safe multi-channel distribution, and anti-slop publishing gates.

---

## 1. Top 10 SERP Information Gain Differential Matrix

Modern generative search engines (Google AI Overviews, SearchGPT, Perplexity) reward primary sources and discard commodity rewrites. Merely compiling or paraphrasing existing search results ("skyscraper content") produces zero non-commodity value, resulting in algorithmic devaluation or extraction suppression.

### 1.1 The 5 Information Gain Vectors

Before commissioning or approving any content piece, Content Managers must verify that the content delivers net-new value across at least one (and preferably multiple) of the **Five Information Gain Vectors**:

| Vector | Operational Description | Concrete Example | Rejection Criteria If Missing |
| :--- | :--- | :--- | :--- |
| **Vector 1: Primary Data & Benchmarks** | Original, unreleased measurements, production telemetry, or stress-test metrics. | Running 1M requests through an Envoy proxy vs HAProxy under identical CPU constraints. | Reject if statistics are merely cited from third-party aggregators without original test runs. |
| **Vector 2: Proprietary Architecture** | Custom workflows, in-house architectural blueprints, or specialized integration patterns. | Documenting a zero-trust multi-cluster Kubernetes service mesh deployment pattern. | Reject if the architecture diagram is a generic redraw of official vendor docs. |
| **Vector 3: Counter-Consensus Analysis** | Defensible challenge to common industry assumptions backed by empirical trade-offs. | Explaining why Microservices introduced 4x cloud latency and arguing for a Modular Monolith. | Reject if the article presents only standard industry cheerleading without trade-off analysis. |
| **Vector 4: Production Postmortems** | Real-world failure modes, edge-case breakdowns, and remediation logs. | Teardown of a memory leak in Go runtime garbage collection under high alloc rates. | Reject if all scenarios are sanitized toy examples without real-world edge cases. |
| **Vector 5: Interactive Assets & Tools** | Calculators, interactive MDX widgets, reproduction repositories, or config generators. | An interactive subnet calculator embedded directly into the article body. | Reject if complex quantitative concepts are described only with static descriptive prose. |

### 1.2 Information Gain Scoring Matrix (0–100 Rubric)

The Content Manager scores candidate briefs and final drafts against this 100-point differential rubric:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   INFORMATION GAIN SCORING (0-100)                     │
├───────────────────────────────────┬────────────────────────────────────┤
│ Dimension                         │ Maximum Points                     │
├───────────────────────────────────┼────────────────────────────────────┤
│ 1. Novel Data / Telemetry         │ 30 points                          │
│ 2. Counter-Consensus Perspective  │ 25 points                          │
│ 3. Firsthand Empirical Proof      │ 25 points                          │
│ 4. Structural Utility & Formats   │ 20 points                          │
└───────────────────────────────────┴────────────────────────────────────┘
```

- **90–100 (Exceptional):** Major primary benchmark or authoritative postmortem; introduces industry-first data points or architecture.
- **75–89 (Strong - Minimum Approval Threshold):** Distinct empirical data, verifiable trade-offs, and novel angles exceeding all top 10 search competitors.
- **50–74 (Moderate - Revision Required):** Contains minor proprietary insight but largely mirrors top-10 SERP structure. Sent back for deeper SME extraction.
- **<50 (Zero / Low Gain - Outright Rejection):** Generic skyscraper rewrite that paraphrases existing search results. Blocked at the commission or approve gate.

---

## 2. Expert Authenticity Verification Protocol

Search engines and readers demand verifiable E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness). The Content Manager enforces strict verification to eliminate synthetic personas, AI hallucinated quotes, and unverified bylines.

### 2.1 SME Credential Verification Checklist

Before publishing content under an author or expert byline, the Content Manager must confirm:

1. **Identity & Digital Footprint:**
   - Active, verifiable professional presence across independent platforms (LinkedIn, GitHub/GitLab, Google Scholar, personal domain, or registered corporate directory).
   - Documented track record in the specific technical or business domain discussed (e.g., published papers, merged open-source code, conference speaking).
2. **Schema.org Person Binding:**
   - Author entity explicitly bound to Schema.org `Person` markup.
   - At least two valid, verified external profile URLs mapped in the `sameAs` array.
3. **Interview Transcript & Audio Provenance:**
   - For internal SME collaboration, raw transcripts (or audio recordings) must be archived in internal editorial records.
   - Every direct quote or attributed architectural decision must trace directly to a timestamped line in the SME transcript.
4. **Anti-Synthetic Persona Prohibition:**
   - Prohibit fictitious author personas, stock-photo profile avatars, and pseudonym bylines pretending to hold real-world engineering credentials.
   - If an article is co-written with AI, transparently disclose AI assistance while assigning authorship to the supervising human expert.

---

## 3. Three-Tier Content Decay Monitoring System

High-performing content deteriorates over time due to algorithmic search shifts, generative engine citation drops, and technological staleness. Content Managers must classify and remediate decaying URLs according to three distinct tiers.

### 3.1 Decay Tier Definitions

```
┌────────────────────────────────────────────────────────────────────────┐
│                     3-TIER CONTENT DECAY TRIAGE                        │
├─────────────────────────┬─────────────────────────┬────────────────────┤
│ Tier 1: Algorithmic     │ Tier 2: GEO Citation    │ Tier 3: Factual    │
│ - Organic Rank Drops >3 │ - AI Citations -15%     │ - Data >18 Mo Old  │
│ - Impressions -25% MoM  │ - Lost AI Overview Slot │ - Deprecated APIs  │
└─────────────────────────┴─────────────────────────┴────────────────────┘
```

1. **Tier 1: Algorithmic SERP Decay:**
   - *Detection:* Google Search Console shows an average position drop >3 spots or a sustained >25% MoM drop in organic search impressions over 60 days.
   - *Root Cause:* Competitor content out-optimizing intent, or search algorithms re-evaluating topical freshness.
2. **Tier 2: Generative Engine / GEO Citation Decay:**
   - *Detection:* Citations in Google AI Overviews, SearchGPT, or Perplexity decline by ≥15% over a rolling 30-day window; AI engines begin citing competing URLs for primary query fan-outs.
   - *Root Cause:* Answer-first structure degraded, schema broken, or facts superseded by more recent competitor benchmarks.
3. **Tier 3: Factual & Temporal Decay:**
   - *Detection:* Article references statistics older than 18 months, documents deprecated CLI commands/APIs, or contains broken external outbound links.
   - *Root Cause:* Natural technological evolution and codebase version updates.

### 3.2 Four-Tier Triage Action Plan

| Triage Action | Trigger Threshold | Execution SLA | Assigned Workflow |
| :--- | :--- | :--- | :--- |
| **Action 1: Quick Patch** | Tier 3 decay isolated to broken links or minor CLI syntax updates. | ≤15 business days | Writer updates broken commands and timestamps. |
| **Action 2: Structural Rewrite** | Tier 1 or Tier 2 decay on a mission-critical pillar URL (>25% drop). | ≤30 business days | Full re-briefing: update benchmarks, restructure for BLUF, fresh SME interview. |
| **Action 3: Consolidation / 301** | Two cannibalizing URLs split traffic with neither ranking in Top 5. | ≤20 business days | Merge best assets into primary pillar; 301-redirect secondary URL. |
| **Action 4: Decommission (410)** | Obsolete technology with near-zero traffic and no topical authority value. | ≤10 business days | Remove URL, return HTTP 410 Gone, prune internal links. |

---

## 4. Safe Multi-Channel Distribution & Semantic Drift Prevention

Pillar technical content is frequently repurposed into short-form assets (LinkedIn posts, X/Twitter threads, newsletters, video scripts). During format compression, there is severe risk of **Semantic Drift** — where crucial engineering trade-offs, security warnings, configuration prerequisites, or failure modes are omitted to create punchy social copy.

### 4.1 Format Conversion Guidelines

| Source Format | Repurposed Target | Allowed Reductions | Forbidden Reductions (Semantic Drift) |
| :--- | :--- | :--- | :--- |
| **Deep-Dive Article** | **LinkedIn Post** | Omit detailed code blocks; summarize setup steps. | **Never omit** the primary architectural trade-off or downside. |
| **Deep-Dive Article** | **X / Twitter Thread** | Break narrative into sequential modular tweets. | **Never present** an optimization without stating boundary conditions. |
| **Deep-Dive Article** | **Executive Summary** | Focus on business impact, cost, and team velocity. | **Never omit** security caveats or migration dependencies. |
| **Deep-Dive Article** | **Video Script** | Visualize architecture; use spoken conversational tone. | **Never state** claims as absolute truth without prerequisite context. |

### 4.2 Semantic Drift Prevention Checklist

Before clearing any repurposed asset for distribution, the Content Manager verifies:

- [ ] **Trade-Off Preservation:** Does the short-form variant explicitly state when *not* to use the recommended pattern?
- [ ] **Prerequisite Fidelity:** Are hardware, software, and version constraints accurately summarized?
- [ ] **Security & Failure Safeguards:** Are critical warnings (e.g., "Do not run in production without rate limiting") retained?
- [ ] **Canonical Attribution:** Does the social asset or external newsletter link back to the canonical pillar URL using proper UTM tracking?
- [ ] **Zero Fabricated Claims:** Are all statistics in the repurposed copy directly sourced from the verified pillar article?

---

## 5. Anti-Slop Commission & Approve Gates

The Content Manager operates two mandatory quality checkpoints that frame the editorial lifecycle:

### 5.1 Gate 1: Commission Gate (Pre-Drafting)
Before assigning any brief to Content Writer:
1. Confirm the topic has an explicit `unique_angle` that cannot be replicated by prompting an off-the-shelf LLM.
2. Flag `boilerplate_risk` for introductory or definitional topics ("What is...", "Getting Started with...").
3. Mandate at least one non-negotiable substance element (original telemetry, internal SME quote, production postmortem).
4. If a brief cannot satisfy these requirements, reject the topic or escalate to Researcher.

### 5.2 Gate 2: Approve Gate (Pre-Publishing)
Before signing off on any draft:
1. Verify the Writer's Anti-Slop Gate is fully documented with `gate_passed: true`.
2. Spot-check the lead paragraph: reject if it opens with generic context-setting ("In today's fast-paced world...").
3. Spot-check the conclusion: reject if it merely restates the introduction without an actionable takeaway.
4. Verify the Non-Commodity Score meets or exceeds 75/100 against top 10 search competitors.

---

Last updated: 2026-09-05
