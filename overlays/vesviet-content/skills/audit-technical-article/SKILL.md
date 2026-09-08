---
name: audit-technical-article
description: Audit a technical article or series part on vesviet/learn against the 7 Technical Content Gates 2027 (answer-first, production-grade code, quantitative depth, Mermaid, production failure, trade-off framing, verifiable claims) and emit an seo-audit-report. Use when reviewing or upgrading technical posts and series parts before publish.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Audit Technical Article

Audit Hugo content under `vesviet/content` or `learn/content` against
`overlays/vesviet-content/rules/technical-article-2027.md`. Run after drafting
or batch upgrades, before publish.

## Core Rules

- **Gate 1 Answer-First**: article opens with `> **Answer-first:**` ≤60 words; each H2 opens with a BLUF ≤60 words.
- **Gate 2 Code Grade**: zero pseudo-code; snippets complete, version-pinned, conceptually compiling (imports, error handling, context).
- **Gate 3 Quantitative Depth**: ≥3 verifiable data points per 500 words; comparison tables quantitative; benchmark conditions stated.
- **Gate 4 Diagrams**: Mermaid present for deep-dives; `mermaid: true` in frontmatter; diagrams standalone-readable.
- **Gate 5 Production Reality**: ≥1 Production Failure story or failure-mode analysis; costs of recommended patterns stated.
- **Gate 6 Trade-off Framing**: rejected alternatives named; decision matrix for ≥3-option comparisons; twin adds information gain (not translation-only).
- **Gate 7 Verifiability**: every claim primary-sourced; version-sensitive claims pinned; unsourced numbers marked as own measurements with conditions.
- **Schema**: frontmatter complete (`title`, `author`, `date`, `tags`, `categories`, `cover`); `canonicalURL` on own host.
- **Topology**: ≥3 internal links; on vesviet at least one Anchor Pillar Hub link; zero `learn.tanhdev.com` links from vesviet content.

## Suggested Process

### 1. Load The Article
Read the file and its corpus index entry (`learn/plan/CONTENT_INDEX.md` or `vesviet/reports/CONTENT_INDEX.md`).

### 2. Score Each Gate
Pass/Warn/Fail per gate with the specific line evidence.

### 3. Check Twin Coverage
If the article is a twin, verify the other-language twin covers the same upgrade and adds information gain.

### 4. Emit The Report
Produce `contracts/schemas/seo-audit-report.json` with per-gate scores, projected post-fix score, and Blocking findings.

## Failure Modes

- **Audit skips Gate 2 depth**: code is skimmed but not checked for pseudo-code and invented APIs. **Mitigation:** the Core Rules require zero pseudo-code; read every snippet.
- **Twin coverage assumed**: the English twin is assumed upgraded without opening the file. **Mitigation:** Step 3 requires opening the twin; verify, do not assume.
- **Blocking finding downgraded**: a Gate failure is logged as a warning to ship faster. **Mitigation:** Gates 2, 6, 7 failures are always Blocking.

## Checklist

- [ ] Gate 1: answer-first + per-section BLUF present
- [ ] Gate 2: zero pseudo-code, version-pinned, conceptually compiling snippets
- [ ] Gate 3: ≥3 verifiable data points per 500 words, benchmark conditions stated
- [ ] Gate 4: Mermaid diagrams present and `mermaid: true` set
- [ ] Gate 5: Production Failure story or failure-mode analysis present
- [ ] Gate 6: rejected alternatives named; twin adds information gain
- [ ] Gate 7: claims primary-sourced and version-pinned
- [ ] Frontmatter complete; `canonicalURL` on own host
- [ ] Topology: ≥3 internal links, hub link (vesviet), no reverse-authority links
- [ ] `seo-audit-report.json` emitted with Blocking findings listed

## Related Skills

- **write-vesviet-learn-content**: drafting counterpart that implements these gates
- **optimize-seo**: core GEO/AEO/E-E-A-T audit standard this skill extends
