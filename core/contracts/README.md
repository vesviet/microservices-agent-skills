# Output Contracts

This directory defines machine-readable schemas for structured data exchange between agents, tools, and workflow steps.

## Why Contracts Exist

In 2026, agents must produce outputs that are not just human-readable but **machine-parseable and schema-validated**. When one agent hands off work to another, the receiving agent must be able to trust the format without guessing.

Contracts use JSON Schema (draft 2020-12) and are enforced via native constrained decoding (Structured Outputs) or post-generation validation (Pydantic/Zod).

## Quick Reference

See [`schemas/INDEX.md`](schemas/INDEX.md) for the full schema index with descriptions, ownership table, and cross-reference chain.

## Delivery Chain (Primary Workflow)

```
solution-brief.json          ← Solution Architect (when solution scoping precedes requirements)
  → feature-ticket.json          ← Business Analyst
    → technical-delivery-plan.json  ← Technical Lead
      → implementation-result.json  ← Developer (per slice)
        → code-review-finding.json  ← Reviewer
          → test-report.json        ← QA Engineer
              → pull-request-spec.json  ← Developer / Technical Lead (release package)
            → validation-result.json ← Agent Coordinator (phase gate)
```

## All Schemas (50 total)

### Solution & Governance
- `solution-brief.json` — Solution Architect scoping handoff (build-vs-buy, capability gaps, AI feasibility, compliance)
- `ai-risk-register.json` — AI risk register (NIST AI RMF + 600-1, EU AI Act tier, OWASP ASI alignment)

### Engineering Delivery
- `feature-ticket.json` — Business requirements and AC
- `technical-delivery-plan.json` — Sliced implementation plan from Technical Lead
- `adr-spec.json` — Architecture Decision Record
- `architecture-options.json` — Options analysis before ADR
- `implementation-result.json` — Code change handoff from Developer
- `api-contract-spec.json` — API endpoint definition
- `deployment-plan.json` — General deployment steps
- `edge-deployment-spec.json` — Cloudflare-specific deployment
- `system-design-spec.json` — System Engineer topology, capacity, and AI-infra design
- `aws-infra-spec.json` — AWS Engineer managed-service and IAM infrastructure spec
- `pull-request-spec.json` — Pull Request specification with blast radius, mutation score, execution proof, and review attestations
- `data-pipeline-spec.json` — Data Pipeline Specification (ODCS v3.1.0 compatible data contract, freshness SLA, quality gates, quarantine policy, and compute budget)

### Quality & Review
- `code-review-finding.json` — Full code review with findings matrix
- `test-report.json` — QA test execution report
- `validation-result.json` — Phase gate validation
- `security-audit.json` — Security audit findings
- `performance-audit.json` — Performance profiling report
- `incident-report.json` — SRE incident post-mortem

### Finance, Accounting & Compliance
- `accounting-compliance-review.json` — Vietnam Accounting Specialist accounting-regime, evidence, reconciliation, close, retention, and human-approval handoff; not a tax filing, legal opinion, audit opinion, or authorization for external action
- `period-end-closing-report.json` — Vietnam Accounting Specialist period-end closing report covering subledger reconciliations, closing adjustments, Account 911 zero-balance verification, financial statement package, and immutable HITL sign-off
- `amis-voucher-contract.json` — Retail sales vouchers, delivery notes, and platform fee journal entries prepared for MISA AMIS ERP per VAS 14
- `stock-audit-session.json` — Physical stocktake session lifecycle, barcode scan event streams, tolerance thresholds, and TK 1381/3381 discrepancy suspense accounting

### Design & Content
- `ux-flow-spec.json` — Multi-screen UX flow handoff
- `ui-component-spec.json` — UI component specification
- `content-handoff.json` — Article/content completion handoff
- `content-audit-report.json` — Content audit report and refresh actions
- `documentation-handoff.json` — Technical doc update handoff
- `learning-handoff.json` — Teaching/exercise handoff
- `learning-assessment-report.json` — Teacher assessment report covering student competency evaluation, 4-tier rubric breakdowns with line citations, cognitive error diagnoses, growth mindset feedback, and HITL verification metadata
- `research-report.json` — Research findings
- `data-analysis-report.json` — Data analysis findings
- `schema-migration.json` — Database migration definition

### SEO & Publishing
- `seo-content-brief.json` — SEO keyword brief and content plan
- `seo-audit-report.json` — On-page SEO audit
- `seo-metadata.json` — Page metadata (title, description, OG)
- `seo-weekly-board.json` — Weekly content sprint board
- `series-article.json` — Article series navigation

### A2A Protocol
- `coordination-plan.json` — Multi-agent phase graph
- `a2a-task.json` — A2A task envelope
- `a2a-task-status.json` — Task status update
- `a2a-task-progress.json` — Task progress notification
- `a2a-artifact.json` — Task output artifact
- `a2a-task-cancel.json` — Task cancellation
- `a2a-message.json` — A2A message unit
- `a2a-jsonrpc-envelope.json` — JSON-RPC wrapper
- `a2a-push-notification-config.json` — Push notification config

### Agent Infrastructure
- `agent-card.json` — Agent capability descriptor
- `agent-trace-span.json` — OpenTelemetry trace span

## Usage In Skills

Every skill that produces structured output should reference a contract:

```markdown
## Output Schema

Use: `contracts/schemas/implementation-result.json`
```

## Validation

```bash
# Validate a contract instance (requires ajv-cli)
npx ajv validate -s contracts/schemas/implementation-result.json -d my-output.json
```

The bundled validator verifies JSON parsing, required top-level metadata, and required fields/discriminators in each bundled example. Validate production payloads with a Draft 2020-12 implementation before constrained decoding or cross-system exchange.

## When To Create A New Schema

- when a new handoff type is needed between agents or workflow steps
- when an existing skill output is consumed programmatically
- when a tool server needs a typed input or output contract

## Related

- A2A registry: `core/a2a/.well-known/agent-registry.json`
- Adapters: `adapters/antigravity/ANTIGRAVITY.md`, `adapters/cursor/README.md`

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
