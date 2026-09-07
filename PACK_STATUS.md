# Pack Status (post-5.0.0 standards-2027 upgrade)

**Validators:** 17/17 pass, 0 errors, 0 warnings.
**Catalog:** 34 roles, 107 skills (97 core + 10 overlay), 24 workflows, 50 contracts, 13 packs, 18 overlays.

## 0. Standards-2027 upgrade summary (5.0.0, 2026-09-07)

Grounded in five-track deep research (sources through September 2026):

- **A2A**: well-known URI corrected to `agent-card.json`; v1.0.x wire conventions (SCREAMING_SNAKE_CASE states, unified Part, `google.rpc.Status`, JCS+JWS card signatures, multi-tenancy); protocol floor v1.0.1; governance AAIF/Linux Foundation.
- **MCP**: stateless-era Core Rules (`server/discover`, `_meta`, MRTR, state handles, deprecation guardrails, CIMD before DCR removal after summer 2027); MCP Registry publishing; OWASP MCP Top 10 guardrails; WebMCP downgraded to watch-item.
- **Discovery**: three-tier well-known stack (agent-card.json / api-catalog RFC 9727 / ai-catalog.json) in `manage-api-catalog`.
- **Security**: OWASP AST10 skill-layer standard + 4 new locks (SKILL-PROVENANCE, IDENTITY-FILE-PROTECTION, EGRESS-ALLOWLIST, EXECUTION-TIME-AUTHZ) in `role-standard.md`; SLSA v1.2 tracks + unsigned-undeployable; WIMSE/NHI federation; full EU AI Act 2027-2028 runway.
- **Data**: ODCS v3.1.0 strings; catalog-as-control-plane; Iceberg v4 readiness; DuckDB v2.0; Text-to-SQL prevention recast as architecture (semantic-layer-first, MCP channel, `agent_accessible`); Apache Ossie; agent query costs in FinOps.
- **Platform**: Workers + Static Assets as the only greenfield target; Pages→Workers migration checklist; MCP-on-Workers (`createMcpHandler`); AI Gateway unified control plane; Astro v7 migration notes; `edge-deployment-spec.json` new fields (runtime_capabilities, edge_ai_integration, mcp_handler); OTel GenAI semconvs from dedicated repo (agent + MCP spans).
- **Content/SEO**: GEO/AEO reframed as AI-surface SEO; non-commodity gate; GEO over-optimization guard; repeated citation sampling; Gen AI report as first-class KPI; "Search generative AI features" eligibility check; spam-policy risk rules; llms.txt v2 with honest agents-only scoping; gen-AI visibility fields in `seo-weekly-board.json` + `content-handoff.json`; publish-log conventions extended.
- **Watch-items intentionally not rule-ified**: WebMCP primary spec, AI Catalog adoption votes, Flink Agents, "SLSA for data", AAIF memory WGs.

## 1. Things that pass every check

| Area | Status |
|---|---|
| Skills (97 core + 10 overlay) | 100% have `## Failure Modes` + `## Output Contracts` + `## Security Guardrails (OWASP ASI)` |
| Roles (34) | 100% have `## Failure Modes` + OWASP + contract refs + Last updated footer |
| Policies (3 YAML + 1 hook + 1 README) | `## Failure Modes` not applicable (YAML); README has Failure Modes + Standard 2026 footer |
| Workflows (24 core + overlay) | 100% have `### Failure Modes` + `### Output Contracts` + `### Security Guardrails (OWASP ASI)` |
| Overlay rules | 100% have Standard 2026 footer |
| Overlay READMEs | 100% have Standard 2026 footer |
| Root docs | 100% have Standard 2026 footer |
| Editor boilerplate | 100% have Standard 2026 footer |
| Adapters (3 dirs) | 100% have Standard 2026 footer + Failure Modes + Output Contracts + Security Guardrails |
| `core/adapter-parity.md` + `packs/README.md` | 100% Tier A upgraded |
| `core/*` READMEs (14) | 100% have Standard 2026 footer |
| `.cursorrules` | 100% has Standard 2026 footer |
| VERSION | `5.0.0` consistent across registry, cards, adapters, changelog |
| CHANGELOG | `[5.0.0] - 2026-09-07` entry complete |
| 13 pack manifests | All have version, schema_version, governance, includes, capabilities |
| 34 agent cards | All regenerated, version 5.0.0, A2A 1.0 |
| A2A registry, ai-catalog, agent-card.json | All 5.0.0 / 1.1 |
| Generated artifacts (INDEX, role-skill-index × 2, capability-map) | All consistent |

## 2. Things the validators do NOT check — possible follow-ups

### Tier A (substantive — could improve usability)

| # | Item | Effort | Why optional |
|---|---|---:|---|
| 1 | Extract long role files (frontend-developer 630, business-analyst 621, qa-engineer 521, backend-developer 520, content-manager 520) | 1-2h | Not required by validator; the dense bullet format is appropriate for role files; references/ extraction is a known-quality improvement, not a Standard 2026 gap |
| 2 | Extract `Detailed Schema Descriptions` (404 lines) from `core/contracts/schemas/INDEX.md` | 30m | Same as above — currently a single source of truth; per-schema files would be a search improvement |
| 3 | Add OWASP ASI section to `core/observability/otel-genai.md` | 15m | Currently the OTel GenAI guide references ASI indirectly; explicit section would be consistency |

### Tier B (cosmetic)

| # | Item | Effort | Why optional |
|---|---|---:|---|
| 4 | Add `Last updated: 2026-09-02` to 14 Tier-3 footers (currently `2026-09-01`) | 5m | Cosmetic; the date is the upgrade date, not the file date |
| 5 | Add `version: 4.1.0` field to `capability-role-map.generated.yaml` | 5m | The validator confirms version-sync via other paths; this is decorative |
| 6 | Bump README "Version 4.1.0" intro paragraph to mention 4.1.0's specific wins (already done in this audit) | already done | — |

### Tier C (informational, not upgrade)

| # | Item | Note |
|---|---|---|
| 7 | 6 overlay skills not referenced in any core role's Primary/Supporting toolbox | Expected — overlay skills are loaded by project overlays, not by core roles |
| 8 | 6 schemas never referenced in markdown prose (a2a-jsonrpc-envelope, a2a-message, a2a-push-notification-config, a2a-task-cancel, agent-card, series-article) | Expected — these are wire-format / system schemas referenced by code paths and adapter tables, not by inline prose |
| 9 | 3-line stub READMEs across overlays (e.g. `overlays/ecommerce-microservices/rules/README.md`) | Stub placeholders; no content to upgrade |

## 3. Hard recommendations

**None.** The pack is at 100% Standard 2026 coverage for the four levels (Failure Modes, Output Contracts, Security Guardrails, Standard 2026 footer) across all skill, role, workflow, policy, adapter, root-doc, and overlay file types.

The 5 long role files and the 404-line Detailed Schema Descriptions are quality-of-life improvements, not Standard 2026 gaps. They are flagged for future refactors (e.g. when the file count grows or a reader asks for a single-source-of-truth review).

## 4. What is NOT a gap

- 16/16 validators pass with 0 warnings
- 0 duplicate headers
- 0 broken cross-references
- 0 missing Last updated footers
- 0 missing required sections
- 0 version-sync inconsistencies
- 0 policy inconsistencies
- 0 contract gaps
- 0 skill ownership conflicts
- 0 stale generated artifacts
- 0 dead policies (every action verb is in some role profile or denies by default)

## 5. Questions for User

1. **Tier A follow-ups?** Extract the 5 long role files (1-2h)?
2. **Tier A follow-ups?** Extract `Detailed Schema Descriptions` from INDEX.md (30m)?
3. **Tier B cosmetic?** Refresh Last-updated dates to 2026-09-02 in the 14 footers (5m)?
4. **Commit policy?** Per `core/rules/code.md` META-RULE, no commit without explicit confirmation.

---

*Awaiting user direction.*
