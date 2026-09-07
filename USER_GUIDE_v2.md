# Agent-Skills User Guide (A2A 1.0 + Antigravity)

> Pack version **5.0.0**. This guide covers the core concepts of the multi-agent system. For the full A2A lifecycle and Antigravity adapter setup, see `adapters/antigravity/ANTIGRAVITY.md`.
>
> **Note:** The filename keeps its `_v2` suffix for link stability; it will be renamed to `USER_GUIDE.md` at the next major version.

Welcome to the **Agent-Skills** ecosystem (pack 5.0.0). This system transforms standard AI coding assistants into an **Autonomous Swarm Environment**. Instead of having one general AI try to do everything, you now have a team of highly specialized, policy-driven "Virtual Employees" that can talk to each other using strict Data Contracts.

### What is new in 5.0.0 (Standard 2026)

Every skill, role, and workflow in the pack now carries:

- **`## Failure Modes`** — concrete failure scenarios with mitigations. Skills have 4-6 items; roles have 4-6; workflows have 3-5.
- **`## Output Contracts`** — explicit names of the JSON schemas the artifact emits (`feature-ticket.json`, `a2a-task.json`, `incident-report.json`, etc.). The machine-readable contract is named instead of implied.
- **`## Security Guardrails (OWASP ASI)`** — present on every security-sensitive skill, role, and workflow, with explicit references to ASI01-ASI10 items.

Policies: `action-boundaries.yaml` is now fail-closed — every previously-unclassified infra/deploy verb (`apply_iac`, `drop_storage_volume`, `terminate_instance`, etc.) carries an explicit `denied` placement for non-owner roles. `mcp-tool-map.yaml` now covers Python `uv` / `poetry` / `pipx`, Docker, `kubectl delete` / `rollout`, the GitHub CLI, and `npx`. `check-policy.py` supports `--emit-audit` (OCSF 99001 audit event per decision) and `AGENT_ACTIVE_ROLE_LEVEL=read_only` to downgrade any non-allowed verdict to denied for observe-only sessions.

The `## Standard 2026 Alignment` footer is appended to every prose file in the pack (root docs, adapters, overlay rules, overlay READMEs) so the pattern is visible at every level.

---

## 1. Core Concepts

- **Policy-as-Code:** Agents cannot run destructive commands (like dropping databases or pushing to production) without explicit permission. This is governed by `core/policies/action-boundaries.yaml`.
- **A2A Delegation:** Agents can spin up sub-agents to do specialized work (e.g., a Backend Developer asking a Data Engineer to write a complex SQL migration).
- **Structured Contracts:** Agents no longer pass information via messy text. Handoffs between roles (e.g., UX Designer → Frontend Developer) are done via strict **JSON Schemas** (Data Contracts).

---

## 2. How to Trigger an Agent

To get the best results, you must explicitly invoke the agent by its **Role Name** and provide the necessary context.

### The "Golden" Prompt Structure:
> *"Act as the `@<role-name>`. [State your objective]. Ensure you follow your role guidelines and output the necessary JSON contract if applicable."*

### ✅ Example 1: Creating a UI Component
> *"Act as the `@ui-ux-designer`. I need a new Product Card for the E-commerce site. Please generate the `ui-component-spec.json` contract for this component."*
>
> *(After the UX agent replies with the JSON)*
> 
> *"Now act as the `@frontend-developer`. Read the `ui-component-spec.json` generated above and implement the React component."*

### ✅ Example 2: Backend Development
> *"Act as the `@backend-developer`. We need a new endpoint to fetch User Orders. Please define the API contract using `api-contract-spec.json`, then implement the Express route."*

### ✅ Example 3: Bug Fixing with Agent Coordinator (Auto-delegation)
When a QA Agent finds a bug (e.g., `test-report.json` says "failed"), you don't need to fix it manually. Wake up the Coordinator to manage the fix end-to-end:
> *"Act as the `@agent-coordinator`. Read `test-report.json`. Use A2A to call `@backend-developer` to fix the Prisma error, then call `@qa-engineer` to re-test. Do not stop until the report status is 'passed'."*

---

## 3. A2A Delegation (Agent-to-Agent)

You don't need to micromanage everything. Agents know when a task is out of their depth and can delegate it.

**How it works:**
If you ask the `@reviewer` to audit a large Pull Request containing a tricky authentication flow, the Reviewer will:
1. Review the general code quality.
2. Realize auth is involved and trigger an **A2A Task**.
3. Delegate the auth snippet to the `@security-engineer`.
4. The Security Engineer returns a `security-audit.json`.
5. The Reviewer merges the findings and presents the final report to you.

*Tip: You can force an agent to delegate by saying: "Act as `@technical-lead`. Plan this feature and delegate the slices to the frontend and backend agents."*

---

## 4. The JSON Contracts

Whenever an agent finishes a major phase of work, it should generate a JSON contract to ensure the next agent in the pipeline understands exactly what to do.

Here are the core contracts available in `core/contracts/schemas/`:

| Contract File | Used By | Purpose |
|---------------|---------|---------|
| `feature-ticket.json` | PM / BA | Requirements ticket: rules, preserved/changed behavior, AC, optional analytics_request and seo_content_request. |
| `ux-flow-spec.json` | UI/UX Designer | Multi-screen flows, transitions, API needs, component refs. |
| `ui-component-spec.json`| UI/UX Designer | Per-component states, props, events, and copy for Frontend. |
| `implementation-result.json` | Frontend / Backend / 3D | Per-slice code change summary for Lead, Coordinator, Reviewer, Writer. |
| `api-contract-spec.json`| Backend Dev | Defines REST/gRPC endpoints for Frontend consumption. |
| `performance-audit.json` | Frontend / 3D | Profiling and perf budget evidence (supplements implementation-result). |
| `schema-migration.json` | Data Engineer | Defines DB changes and rollback scripts safely. |
| `data-analysis-report.json` | Data Analyst | Metrics, findings, lineage, and recommendations for stakeholders. |
| `seo-content-brief.json` | SEO Analyst | Keywords, intent, outline, and internal links before drafting. |
| `seo-audit-report.json` | SEO Analyst | On-page audit issues and metadata recommendations. |
| `seo-metadata.json` | SEO Analyst / Content Writer | Publish-ready title, meta, slug, and keywords. |
| `seo-weekly-board.json` | SEO Analyst / Task Planner | 7-day dual-site topic board and publish status. |
| `content-handoff.json` | Content Writer | Article path, research passes, claims, and publish status. |
| `test-report.json` | QA Engineer | Logs test results, bugs, and release recommendations. |
| `performance-audit.json`| 3D / Frontend | Logs FPS, memory, and bundle size metrics. |
| `security-audit.json` | Security Eng | Logs vulnerabilities and assigns CVE mitigation tasks. |
| `deployment-plan.json` | DevOps | Defines environment rollout and rollback strategy. |
| `incident-report.json` | SRE | Logs post-mortem findings and action items. |
| `architecture-options.json` | Technical Architect | Structured options before an ADR is accepted. |
| `adr-spec.json` | Technical Architect | Records why a technical decision was made. |
| `technical-delivery-plan.json` | Technical Lead | Implementation slices, gates, and readiness. |
| `documentation-handoff.json` | Technical Writer | Published doc paths and verified sources. |
| `agent-card.json` | All roles | A2A discovery manifest (see `core/a2a/registry/`). |
| `a2a-task.json` | Coordinator / delegators | Submit delegated work (UUID task_id). |
| `a2a-task-progress.json` | Worker | SSE streaming progress events. |
| `a2a-task-status.json` | Coordinator | Get/list/cancel task state. |
| `a2a-artifact.json` | Worker | Validated deliverable for a task. |
| `coordination-plan.json` | Agent Coordinator | Multi-phase graph state. |
| `research-report.json` | Researcher | Research synthesis; `depth_mode` deep (10+ rounds) or scoped (3+ with waiver); includes `recommended_next_roles`. |
| `edge-deployment-spec.json` | Cloudflare Engineer | Wrangler, bindings, DNS/cache notes, deploy and rollback for Cloudflare Pages/Workers. |
| `learning-handoff.json` | Teacher | MOET-aligned plans, exercises, evaluations (grades 6–9). |

---

## 5. Security & Action Boundaries

You are protected by `core/policies/action-boundaries.yaml`.

- **Frontend & UX Agents:** Can read/write files and run dev servers. They are **DENIED** from modifying secrets or running DB migrations.
- **Backend & Data Agents:** Can run migrations (with user approval), but are **DENIED** from pushing directly to production.
- **Content Writers:** Are **DENIED** from running builds or installing dependencies.

*If an agent tries to execute a denied tool, the system will automatically block it and ask you for manual override permission.*

---

## 6. Pro-Tips for Daily Usage

1. **Don't let them skip the JSON:** If an agent gives you a wall of text instead of a JSON contract, tell it: *"Please output this as a valid `[name-of-contract].json`."*
2. **Combine Packs:** If you are working on the Go Microservices, tell the agent: *"Use the `ecommerce-team` pack and the `go-microservices` overlay."*
3. **Use the Planner:** If you have a massive idea but don't know where to start, say: *"Act as `@task-planner`. Break this idea down into a step-by-step Execution Plan."*

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

Last updated: 2026-09-01
