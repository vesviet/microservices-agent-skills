# Agent Skills - Global Engineering Pack

This repository contains a reusable, language-agnostic engineering skill pack for software delivery.

## Mandatory Rules (Always-On)

Before ANY action, you MUST read and follow the rules in `core/rules/code.md`. Key constraints:

- **META-RULE**: Before finalizing any response or executing a command, verify the action against `core/rules/code.md`. If any step violates a rule, halt and ask the user for permission.
- Do NOT create a commit unless the user explicitly confirms.
- Do NOT push, tag, or publish unless the user explicitly confirms.
- NEVER commit `.dev.vars`, `.env`, or other local environment files; verify `git status` and keep them in `.gitignore`.
- Repo-local rules override these defaults when they are explicitly present.
- Ensure all code changes pass local linters, tests, and build checks before committing.
- Do NOT expose secrets, credentials, or sensitive values in any user-visible artifact.
- Do NOT mention agents, AI workflow, or internal process metadata in commits, changelogs, or release notes.
- Prefer repo-local standards over defaults when they exist.
- Prefer no comment over comments that merely restate the code; keep each code comment implementation-focused and within 3 lines unless a longer doc comment, file header, or tooling directive is required.

Full rules: `core/rules/code.md`

## Role System

When the user assigns you a Role, you MUST:

1. Read `core/roles/role-standard.md` first.
2. Read the specific role file from `core/roles/<role-name>.md`.
3. Follow the **SKILL TOOLBOX LOCK**: Only use Primary Skills listed in your role's Skill Toolbox. Supporting Skills require collaboration context. Skills outside the Toolbox require explicit user permission.
4. Follow the **BOUNDARY LOCK**: If a task falls outside your role's core responsibilities, politely decline and recommend the appropriate role.

Available roles: `core/roles/README.md`

## A2A 1.0 & Antigravity (pack 5.0.0)

When operating as an AI agent (like **Antigravity**) under this pack, you MUST:

1. **Read the Antigravity adapter**: `adapters/antigravity/ANTIGRAVITY.md` and apply `.antigravity/rules.md` from `adapters/antigravity/rules.template.md` in the active project.
2. **Discover agents** via `core/a2a/.well-known/agent-registry.json` and per-role `*.agent-card.json` (regenerate with `python3 core/scripts/generate-a2a-registry.py`).
3. **Output Structured JSON Contracts** from `core/contracts/schemas/` — not prose-only handoffs.
4. **Use full A2A lifecycle** (`agent-a2a-protocol` skill): `a2a-task.json` → stream `a2a-task-progress.json` → `a2a-artifact.json` / `a2a-task-status.json`; support cancel and UUID v4 task IDs.
5. **Delegate** with `agent-delegation` / workflow `/agent-a2a-delegation` when work crosses role boundaries.
6. **Obey Policy-as-Code**: `core/policies/action-boundaries.yaml`, `data-classification.yaml`, and `mcp-tool-map.yaml` before state-changing actions.
7. **PromptOps & memory**: use `agent-prompt-lifecycle` and `agent-semantic-memory` when Coordinator or Technical Lead owns durable sessions (see `core/prompts/golden/`).
8. **Cursor hooks** (optional): `adapters/cursor/hooks.template.json` for runtime policy advisory checks.

## Skills

Core skills are organized under `core/skills/` by taxonomy:

- `core/skills/agent/`
- `core/skills/foundation/`
- `core/skills/meetings-analysis/`
- `core/skills/repo-ops/`
- `core/skills/content/`
- `core/skills/backend/`
- `core/skills/frontend/`
- `core/skills/platform/`
- `core/skills/commerce/`
- `core/skills/security-data/`
- `core/skills/mmo/`
- `core/skills/documentation/`
- `core/skills/education/`

Optional repo-specific skills live under `overlays/` and should only be loaded when the active repository actually needs them.

## Workflows

When executing a workflow from `core/workflows/`, you MUST:

1. Output a markdown checklist `[ ]` for ALL steps.
2. Process only ONE step at a time.
3. Mark each step as `[x]` and explain the result before moving to the next.
4. Respect the `Role:` tag on each step - that role owns the step.

Available workflows: `core/workflows/README.md`

## Quick Reference

| Need | Go to |
|------|-------|
| Rules (always-on) | `core/rules/code.md` |
| Role standard | `core/roles/role-standard.md` |
| All roles | `core/roles/README.md` |
| All skills | `core/skills/README.md` |
| All workflows | `core/workflows/README.md` |
| A2A registry | `core/a2a/.well-known/agent-registry.json` |
| Antigravity adapter | `adapters/antigravity/ANTIGRAVITY.md` |
| Cursor/Kiro hooks | `adapters/cursor/README.md` |
| Kiro steering | `.kiro/steering/agent-skills.md` |
| Kilo Code rules | `.kilocode/rules/agent-skills.md` |
| Codex adapter | `core/codex/README.md` |
| Claude adapter | `adapters/claude/CLAUDE_ADAPTER.md` |
| Action boundaries | `core/policies/action-boundaries.yaml` |
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
