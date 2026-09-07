# Agent Skills — Global Engineering Pack (Claude Code)

Pack version: **5.0.0** | Protocol: **A2A 1.0** | Adapter: `adapters/claude/`

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

---

## Mandatory Rules (Always-On)

Before ANY action, read and follow `core/rules/code.md`. Key constraints:

- **META-RULE**: Before finalizing any response or executing a command, verify the action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission. (In Claude Code: this includes bash commands and tool calls.)
- Do NOT create a commit unless the user explicitly confirms that specific commit action.
- Do NOT push commits, create tags, or publish releases unless the user explicitly confirms.
- NEVER commit `.dev.vars`, `.env`, or other local environment files; verify `git status` and keep them in `.gitignore`.
- Repo-local rules override these defaults when they are explicitly present.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards, templates, and workflows when they exist.
- Do not invent repository conventions, paths, or branching models not present in the active codebase.
- Prefer no comment over comments that merely restate the code.
- Keep code comments implementation-focused and within 3 lines, unless a longer comment is required for doc comments, file headers, or tooling directives.

Full rules: `core/rules/code.md`

---

## Policy-as-Code (Claude Code)

Before executing any state-changing bash command or tool call:

1. Identify the active role (default: `agent-coordinator` if none assigned).
2. Map the operation to an action ID using `core/policies/mcp-tool-map.yaml`.
3. Check the role's entry in `core/policies/action-boundaries.yaml`:
   - `allowed` → proceed
   - `requires_approval` → pause and confirm with user
   - `denied` → refuse and explain
4. Classify any output data with `core/policies/data-classification.yaml` before sharing.

You can run the policy check script manually:

```bash
AGENT_SKILLS_ROOT=$(pwd) AGENT_ACTIVE_ROLE=<role> CURSOR_TOOL_NAME=<tool> \
  python3 core/scripts/hooks/check-policy.py
```

---

## Role System

When the user assigns a Role:

1. Read `core/roles/role-standard.md` first.
2. Read `core/roles/<role-name>.md` for the specific role.
3. Follow the **SKILL TOOLBOX LOCK**: Only use Primary Skills from the role's Skill Toolbox. Supporting Skills require collaboration context. Skills outside the Toolbox require explicit user permission.
4. Follow the **BOUNDARY LOCK**: If a task falls outside the role's core responsibilities, politely decline and recommend the appropriate role.

Available roles: `core/roles/README.md`

---

## A2A 1.0 (Claude Code)

When operating as an AI agent under this pack:

1. **Discover agents** via `core/a2a/.well-known/agent-registry.json` and per-role `core/a2a/registry/<role>.agent-card.json`. Regenerate with:
   ```bash
   python3 core/scripts/generate-a2a-registry.py
   ```
2. **Output structured JSON contracts** from `core/contracts/schemas/` for cross-role handoffs — not prose-only.
3. **Use full A2A lifecycle** via `agent-a2a-protocol` skill:
   - Submit: `a2a-task.json` (`state: submitted`, UUID v4 `task_id`)
   - Stream: `a2a-task-progress.json` SSE events while `working`
   - Complete: `a2a-artifact.json` + `a2a-task-status.json`
   - Cancel: set `state: canceled` with `cancel_reason`
4. **Delegate** with `agent-delegation` / workflow `/agent-a2a-delegation` when work crosses role boundaries.
5. **Obey Policy-as-Code**: check `action-boundaries.yaml`, `data-classification.yaml`, and `mcp-tool-map.yaml` before state-changing actions.
6. **Coordinator pattern**: when acting as Agent Coordinator, publish `coordination-plan.json` and issue per-phase `a2a-task.json` with `assignee_agent_card` from registry.
7. **PromptOps & memory**: use `agent-prompt-lifecycle` and `agent-semantic-memory` for long-running or multi-session work.

Adapter reference: `adapters/claude/CLAUDE_ADAPTER.md`

---

## Skills

Core skills live under `core/skills/` organized by taxonomy:

- `core/skills/agent/` — A2A protocol, context management, memory, orchestration, quality gates
- `core/skills/foundation/` — commit, review, test, navigate, troubleshoot, write
- `core/skills/backend/` — API endpoints, events, service clients, scaffolding
- `core/skills/frontend/` — UI components, pages, API client, testing, design system
- `core/skills/platform/` — deployment, runtime debug, telemetry, Cloudflare, AWS
- `core/skills/commerce/` — checkout, payment, catalog, fulfillment
- `core/skills/security-data/` — secrets, database, security audit, pipelines
- `core/skills/documentation/` — technical docs, llms.txt, tech radar
- `core/skills/education/` — learning plans, exercises, grading

Overlay-specific skills live under `overlays/` and load only when the active repository needs them.

Skills index: `core/skills/README.md`

---

## Workflows

When executing a workflow from `core/workflows/`:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time.
3. Mark each step as `[x]` and explain the result before moving to the next.
4. Respect the `Role:` tag on each step — that role owns the step.

Available workflows: `core/workflows/README.md`

---

## Validation

Run before treating any pack change as complete:

```bash
python3 core/scripts/validate-all.py
python3 core/scripts/generate-a2a-registry.py
```

---

## Quick Reference

| Need | Go to |
|------|-------|
| Rules (always-on) | `core/rules/code.md` |
| Policy check script | `core/scripts/hooks/check-policy.py` |
| Role standard | `core/roles/role-standard.md` |
| All roles | `core/roles/README.md` |
| All skills | `core/skills/README.md` |
| All workflows | `core/workflows/README.md` |
| A2A registry | `core/a2a/.well-known/agent-registry.json` |
| Agent cards | `core/a2a/registry/<role>.agent-card.json` |
| Antigravity adapter | `adapters/antigravity/ANTIGRAVITY.md` |
| Cursor/Kiro hooks | `adapters/cursor/README.md` |
| Kiro steering | `.kiro/steering/agent-skills.md` |
| Kilo Code rules | `.kilocode/rules/agent-skills.md` |
| Codex adapter | `core/codex/README.md` |
| Claude adapter | `adapters/claude/CLAUDE_ADAPTER.md` |
| Action boundaries | `core/policies/action-boundaries.yaml` |
| MCP tool map | `core/policies/mcp-tool-map.yaml` |
| Overlay index | `overlays/README.md` |

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
