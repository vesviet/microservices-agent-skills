# Skills Inventory

This directory contains the **portable core** skill inventory for the global engineering pack.

**Counts:** 97 portable core skills under `core/skills/` + 11 overlay skills under `overlays/*/skills/` = **108 total** (run `validate-skills.py` for the live total, and `validate-indexes.py` to confirm this line matches disk).

## Taxonomy

### Agent (22)

Agent operating discipline, orchestration, and agentic web standards:

- `agent-a2a-protocol`
- `agent-context-management`
- `agent-delegation`
- `agent-graph-orchestration`
- `agent-handoff`
- `agent-memory-compaction`
- `agent-model-routing`
- `agent-observability`
- `agent-panel-meeting`
- `agent-prompt-lifecycle`
- `agent-semantic-memory`
- `agent-tool-orchestration`
- `agent-quality-gate`
- `manage-agent-identity`

#### Agent Infrastructure & Agentic Web Standards (8)

Configuration and compliance skills for agentic-ready web presence (MCP, RFC 9727, x402, identity provider (WorkOS, Auth0, Okta)):

- `configure-agent-commerce`
- `configure-agent-headers`
- `configure-agent-skills`
- `configure-mcp`
- `configure-oauth-metadata`
- `debug-identity-provider`
- `manage-api-catalog`
- `manage-auth-md`

### Foundation (12)

Cross-cutting portable skills:

- `accessibility-review`
- `ai-risk-assessment`
- `conduct-research`
- `create-migration`
- `design-review`
- `design-ux-flow`
- `incident-report`
- `performance-profiling`
- `plan-technical-delivery`
- `release-notes`
- `write-product-brief`
- `write-tests`

### Meetings And Analysis (3)

- `meeting-review`
- `analyze-business-requirements`
- `analyze-data`

### Repo Ops (5)

- `navigate-service`
- `troubleshoot-service`
- `review-code`
- `review-service`
- `commit-code`

### Content (4)

- `write-article`
- `repurpose-content`
- `audit-content`
- `optimize-seo`

### MMO (7)

MMO/growth-ops skills with compliance notices; each maps to `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role:

- `generate-mmo-content`
- `analyze-campaign-roi`
- `deploy-mmo-infrastructure`
- `deploy-proxyware-fleet`
- `create-automation-script`
- `manage-mmo-assets`
- `setup-tracking-system`

### Backend (6)

- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `build-mcp-server`
- `implement-structured-outputs`
- `scaffold-new-service`

### Frontend (7)

- `add-ui-component`
- `add-page-route`
- `frontend-testing`
- `implement-webmcp`
- `integrate-api-client`
- `setup-design-system`
- `setup-visual-regression`

> R3F/Three.js cluster (`debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets`) migrated to `overlays/r3f-stack/skills/` in v4.0.0 per the stack-overlay naming rules.

> Note: `create-automation-script` is classified under MMO (`core/skills/mmo/`) — its stealth/CDP automation scripts serve growth-ops workflows, even though the underlying techniques are platform-level. See Domain Cluster Notes below.

### Platform (16)

Delivery, runtime, Cloudflare-specific, cloud, and system infrastructure skills:

- `aws-infrastructure`
- `setup-deployment`
- `setup-gpu-finops`
- `setup-llm-gateway`
- `supply-chain-security`
- `system-design`
- `wrangler`
- `debug-workers-edge`
- `debug-runtime-platform`
- `add-telemetry-instrumentation`
- `cloudflare-email-service`
- `durable-objects`
- `sandbox-sdk`
- `turnstile-spin`
- `web-perf`
- `workers-best-practices`

### Commerce (4)

E-commerce catalog, checkout, payment, and fulfillment:

- `integrate-payment-gateway`
- `handle-checkout-flow`
- `manage-product-catalog`
- `manage-order-fulfillment`

### Security And Data (5)

- `manage-secrets`
- `database-maintenance`
- `manage-vietnam-accounting`
- `security-audit`
- `build-data-pipeline`

### Documentation (3)

- `configure-llms-txt`
- `write-documentation`
- `write-tech-radar`

### Education (3)

Teaching and curriculum:

- `design-learning-plan`
- `create-exercises`
- `grade-and-review`

Overlay-specific skills (site stacks, ICM, content data, R3F) live under `overlays/*/skills/` and are validated together with core.

## Skill Boundaries (quick reference)

| Topic | Primary skill | Escalate to |
| ----- | ------------- | ----------- |
| Deep discovery | `conduct-research` | Researcher role |
| Ad-hoc analysis / dashboards | `analyze-data` | Data Analyst role |
| Pipelines / ETL / warehouse | `build-data-pipeline` | Data Engineer role; analysis-only → `analyze-data` |
| UX flows and specs | `design-ux-flow` | UI/UX Designer |
| Visual / IA critique (no code) | `design-review` | UI/UX or Reviewer |
| a11y conformance | `accessibility-review` | QA + Frontend |
| Generic CI/CD deploy | `setup-deployment` | DevOps Engineer |
| System topology & capacity | `system-design` | System Engineer |
| Cloudflare Workers/Pages | `wrangler` | Cloudflare Engineer |
| MCP server configuration | `configure-mcp` | Cloudflare Engineer |
| Agentic commerce flows | `configure-agent-commerce` | Backend Developer |
| Vietnam accounting controls, reconciliations, or close evidence | `manage-vietnam-accounting` | Vietnam Accounting Specialist; tax position/legal interpretation -> qualified human reviewer |
| Agent-ready web discovery | `configure-agent-headers` + `manage-api-catalog` | Agent Discovery Engineer |

## Backlog (not yet skills)

### Priority 2

- `3d-material-pipeline` (not yet created)
- `product-discovery` (not yet created)

### Priority 3

- `frontend-state-management` (not yet created)

## Naming Rules

- prefer generic names over stack-specific names
- categorize skills under their respective taxonomy folders (agent, foundation, backend, frontend, platform, security-data, documentation, education)
- move stack-specific or org-specific variants into overlays when they are not portable

## Skill Authoring Standard

Every SKILL.md is an [Agent Skills](https://agentskills.io/specification) manifest (the open standard indexed by skills.sh): YAML frontmatter with required `name` and `description`, then a markdown body. The pack layers these baseline sections on top:

1. YAML frontmatter with `name` and `description`.
2. H1 title matching the skill name in title case.
3. One short "Use this skill..." paragraph.
4. `## Core Rules` for non-negotiable constraints.
5. `## Suggested Process` for the normal execution path.
6. `## Checklist` for completion checks.
7. `## Related Skills` with one-line descriptions.

Optional spec fields (`license`, `compatibility`, `metadata`, `allowed-tools`) may be added when they carry real information; do not add per-skill versions — the pack `VERSION` governs all core skills.

Optional body sections such as `## Output Format`, `## When to Use`, `## Deliverable Decision`, or domain-specific guidance are fine when they improve execution; contract-emission guidance must use the canonical `## Output Contracts` heading.

Descriptions should include both what the skill does and when to use it, with specific trigger keywords — agents match requests against this field at startup. Keep skills repo-agnostic by default; put stack-specific assumptions in adapters or overlays.

### References Subdirectory Policy

A skill may add a `references/` subdirectory when the SKILL.md body alone would exceed ~150 lines. Use `references/` for:

- long external-spec excerpts (e.g., `agent-a2a-protocol/references/a2a-spec.md`)
- framework or stack variant guides (e.g., `turnstile-spin/references/{astro,hugo,nextjs-app,nextjs-pages,sveltekit,vanilla-html}.md`)
- deep rules/checklists that the SKILL.md body summarizes (e.g., `durable-objects/references/{rules,testing,workers}.md`)

When you add a `references/` subdirectory:

- keep SKILL.md focused on the trigger conditions, core rules, suggested process, and checklist
- link from SKILL.md to each reference doc by relative path the first time the topic appears (e.g., `See references/rules.md for the full checklist`)
- do not duplicate content between SKILL.md and `references/`
- references are loaded on demand — do not rely on them being read for the skill to start

The validator does not check `references/` content; the structural contract only applies to the SKILL.md file itself.

### Size Guidance

- Aim for SKILL.md between 80 and 200 lines.
- Below ~70 lines is acceptable for tight, scope-narrow skills (e.g., compliance-locked MMO skills) provided all baseline sections are present.
- Above ~200 lines signals a candidate for `references/` extraction; above 500 lines is rejected by the validator.

### Domain Cluster Notes (2026)

- The **MMO cluster** spans multiple taxonomies by design (foundation for content/ROI, platform for infra/automation, security-data for assets/tracking). Their pre-2025.4 drift has been retired; current skills carry Legal & Compliance Notices that map to `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role.
- The **R3F/3D cluster** migrated from `core/skills/frontend/` to `overlays/r3f-stack/skills/` in v4.0.0. The `3d-graphics-engineer` role toolbox resolves via overlay. See `overlays/r3f-stack/README.md` for the migration notes.

## Validation Gate

Run this before treating core skill changes as complete:

```bash
python3 core/scripts/validate-skills.py
```

The validator checks:

- every skill has valid `name` and `description` frontmatter
- Agent Skills spec compliance: hyphen placement in names, no XML tags, no reserved words
- descriptions include both capability and trigger language
- skill names match directory names
- every skill has the baseline sections
- checklists contain enough actionable completion checks
- related skill references point to existing skills
- role and workflow skill references resolve

Skill changes are not done until this check passes.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-02
