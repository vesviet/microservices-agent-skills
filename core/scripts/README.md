# Validation Scripts

These scripts validate the **core** pack structure and references.

## Running All Validators

```bash
# Standard (sequential, text output)
python3 core/scripts/validate-all.py

# Parallel execution (faster CI)
python3 core/scripts/validate-all.py --parallel

# JSON output (CI step consumption)
python3 core/scripts/validate-all.py --format json

# SARIF 2.1.0 (GitHub Code Scanning)
python3 core/scripts/validate-all.py --format sarif > results.sarif

# Stop on first failure
python3 core/scripts/validate-all.py --fail-fast
```

**Exit codes:** `0` = pass · `1` = fail (rule violations) · `2` = script error

## Available Validators

- `validate-rules.py` — global rules and adapter mirror parity
- `validate-skills.py` — SKILL.md structure, frontmatter, cross-references
- `validate-roles.py` — role definitions and role-to-skill mappings
- `validate-workflows.py` — workflow structure, role ownership, step references
- `validate-packs.py` — pack manifests and includes
- `validate-overlays.py` — overlay directory structure
- `validate-2026-compliance.py` — A2A coverage, coordinator wiring, ai-catalog discovery
- `validate-a2a-compliance.py` — full A2A 1.0 + Antigravity artifacts
- `validate-agent-cards.py` — generated registry vs `agent-card.json`
- `validate-contracts.py` — JSON Schema 2020-12 metadata and bundled examples
- `validate-standardization.py` — ≥90% pack standardization gate
- `validate-version-sync.py` — `VERSION` vs registry, agent cards, adapters, changelog
- `validate-indexes.py` — every skill, schema, role, workflow, overlay, pack is listed in its index
- `validate-policy-consistency.py` — `action-boundaries.yaml` vs role files and MCP tool map
- `validate-skill-ownership.py` — every skill has a Primary owner; workflow steps resolve to tagged-role toolboxes
- `validate-contract-coverage.py` — contract-to-skill emission coverage (advisory warnings)

### Which validator catches which drift

| Symptom | Validator |
| ------- | --------- |
| `VERSION` bumped but registry/cards not regenerated | `validate-version-sync.py` |
| New skill or schema added but index count still old | `validate-indexes.py` |
| Policy profile copy-pasted between roles with wrong tiers | `validate-policy-consistency.py` |
| Role granted a Primary skill its boundaries forbid | `validate-skill-ownership.py` |
| Workflow step names a skill nobody on that step can run | `validate-skill-ownership.py` |
| New workflow added but not listed in README or root index | `validate-indexes.py` |
| Agent coordinator missing A2A delegation section | `validate-2026-compliance.py` |

## Generator Scripts

Generate A2A registry after role edits (also emits canonical `agent.json` + `ai-catalog.json`):

```bash
python3 core/scripts/generate-a2a-registry.py
```

This emits:
- `core/a2a/registry/*.agent-card.json` — per-role A2A agent cards
- `core/a2a/.well-known/agent-registry.json` — internal multi-agent directory
- `core/a2a/.well-known/agent-card.json` — **A2A 1.0 2026 canonical endpoint** (`/.well-known/agent-card.json`)
- `core/a2a/.well-known/ai-catalog.json` — **Google AI Catalog 2026 meta-index**
- `adapters/antigravity/capability-role-map.generated.yaml` — Antigravity routing map

Generate skill dependency graph (Mermaid):

```bash
python3 core/scripts/generate-skill-graph.py
```

## Utility Scripts

Inject `## Output Contracts` into SKILL.md files (cross-platform, no hardcoded paths):

```bash
python3 core/scripts/inject_output_contracts.py           # apply
python3 core/scripts/inject_output_contracts.py --dry-run # preview only

# PowerShell equivalent
.\core\scripts\inject_output_contracts.ps1 -DryRun
```

## Hooks

Hooks run as Cursor/Antigravity `postToolUse` and `preToolUse` hooks:

| Hook | Trigger | Output |
|------|---------|--------|
| `hooks/check-policy.py` | preToolUse | JSON (default) · SARIF · text |
| `hooks/log-trace-span.py` | postToolUse | OTel JSONL span to `core/observability/spans/` |

**check-policy.py output modes:**
```bash
AGENT_ACTIVE_ROLE=backend-developer TOOL_NAME=write python3 core/scripts/hooks/check-policy.py
AGENT_ACTIVE_ROLE=backend-developer TOOL_NAME=write python3 core/scripts/hooks/check-policy.py --format sarif
```

**log-trace-span.py OTel GenAI fields (2026):**
- `gen_ai.request.model` — model identifier (from `AGENT_MODEL` or `GEN_AI_MODEL` env)
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` — token counts
- `gen_ai.finish_reason` — generation finish reason
- W3C Trace Context–compatible `trace_id` (32 hex chars) + `span_id` (16 hex chars)

## 2026 Toolchain Standards

| Layer | Tool | Version |
|-------|------|---------|
| Runtime | `uv` (PEP 723 inline deps) | latest |
| Linting | `ruff` (E, F, I, B, UP, RUF, PTH) | 0.5+ |
| Type checking | `ty` (speed) · `pyright --strict` (ecosystem) | latest |
| JSON Schema | `jsonschema` Draft202012Validator | 4.x |
| Output format | JSON + SARIF 2.1.0 | — |
| Exit codes | 0=pass · 1=fail · 2=error | — |
| Pre-commit | `pre-commit` 4.x (Dependabot-managed) | 4.6+ |
| Secret scan | `gitleaks` v8.x (hook) · `trufflehog` v3 (CI) | — |
| Policy-as-code | `conftest` + OPA Rego | 0.64+ |
| Commit linting | `convco` | latest |

Run from the repository root or using paths directly under `core/scripts/`.

