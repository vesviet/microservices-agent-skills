# Packs

Packs describe how to assemble the portable core with zero or more overlays for a target team. Each pack has a `manifest.yaml` that declares which `core` and `overlays/` to include, along with 2026 governance metadata.

## Available Packs (13)

| Pack | Manifest | Composition | Capabilities |
|------|----------|-------------|-------------|
| `global-engineering` | [manifest.yaml](global-engineering/manifest.yaml) | `core` only | All general engineering |
| `vesviet-team` | [manifest.yaml](vesviet-team/manifest.yaml) | `core` + `overlays/vesviet-content` | Content, GEO/AEO, Hugo |
| `lease-team` | [manifest.yaml](lease-team/manifest.yaml) | `core` + `overlays/lease-content` + `overlays/seo-publishing` | Content, GEO/AEO, 5-Pillar |
| `mdg-team` | [manifest.yaml](mdg-team/manifest.yaml) | `core` + `overlays/laravel-filament` + `overlays/maydiengiaisaigon` | Laravel 13, Filament v4, PHP 8.4 |
| `icm-team` | [manifest.yaml](icm-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/icm-main` | Astro v6+, Cloudflare Workers |
| `obj-team` | [manifest.yaml](obj-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/obj-configurator` | Astro, R3F v9, WebGPU |
| `golf-team` | [manifest.yaml](golf-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/golf-icm` | Astro v6+, Cloudflare, SEO |
| `sport-team` | [manifest.yaml](sport-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/sport-icm` | Astro v6+, Cloudflare, SEO |
| `ecommerce-team` | [manifest.yaml](ecommerce-team/manifest.yaml) | `core` + `overlays/go-microservices` + `overlays/ecommerce-microservices` | Go 1.25, Kratos v3, ConnectRPC |
| `data-analyst-team` | [manifest.yaml](data-analyst-team/manifest.yaml) | `core` + `overlays/data-analyst-stack` | DuckDB, dbt 1.9, Iceberg, Metabase |
| `content-sprint-team` | [manifest.yaml](content-sprint-team/manifest.yaml) | `core` + `overlays/seo-publishing` | GEO/AEO, AI Overviews, publishing cadence |
| `donthan-team` | [manifest.yaml](donthan-team/manifest.yaml) | `core` + `overlays/donthan-web` | Frontend, UX, livestream, PWA |
| `retail-warehouse-team` | [manifest.yaml](retail-warehouse-team/manifest.yaml) | `core` + `overlays/retail-data-warehouse` (incl. `learning/` track) | DuckDB Single-Writer, MISA AMIS ERP, Blind Recount, PII Masking, dbt 1.9/Iceberg/Kafka learning roadmap |

## 2026 Manifest Schema (v2)

All manifests follow `schema_version: "2"` with these fields:

```yaml
schema_version: "2"          # Manifest format version (decoupled from pack version)

name: my-team                # Pack slug (snake_case)
description: "..."           # One-line description

version: 4.0.0               # Pack content version (SemVer)

tags: []                     # Searchable capability tags
author: user
maintained_by: platform-team
license: MIT                 # SPDX identifier (EU CRA SBOM compliance)
homepage: https://github.com/vesviet/agent-skills

compatibility:
  min_pack_version: "4.0.0" # Oldest host that can load this manifest
  max_pack_version: "5.x"   # "x" = open-ended minor/patch
  requires_schema: "2"      # Parser must support schema_version 2+

includes:                    # Load order: core first, stack overlay, then project overlay
  - core
  - overlays/stack-overlay
  - overlays/project-overlay

capabilities:                # agentskills.io capability taxonomy
  - code-generation
  - backend
  - seo

data_classification: internal  # public | internal | confidential | restricted

activation:                  # IDE/agent auto-load conditions
  strategy: marker_first     # marker_first | always | explicit
  always: false              # true only for global-engineering
  markers:                   # Repo root files that trigger auto-load
    - go.mod
  glob_patterns:             # Edit patterns that trigger auto-load
    - "**/*.go"
  exclude_patterns:
    - "vendor/**"

governance:                  # Compliance declarations
  eu_ai_act_tier: minimal_risk  # unacceptable | high_risk | limited_risk | minimal_risk
  audit_logging: required
  audit_format: otel-json
  retention_days: 90
  secret_handling: env_only  # env_only | vault | runtime_injection | denied
  human_oversight:
    required: true
    gate_actions:            # Actions requiring human approval before execution
      - run_migration
      - push_to_production
      - modify_secrets
  data_policy: core/policies/data-classification.yaml
  action_policy: core/policies/action-boundaries.yaml
  review_cadence: quarterly
```

## Schema Versioning

| `schema_version` | What Changed |
|-----------------|--------------|
| `"1"` | Original format: name, description, version, tags, author, maintained_by, includes |
| `"2"` | Added: schema_version, license, homepage, compatibility, capabilities, data_classification, activation, governance |

When the manifest field structure changes (field rename, removal, or new required field), bump `schema_version`. **The pack `version` and `schema_version` change independently.**

## Pack Authoring Rules

- always include `core` as the first entry in `includes`
- list stack overlays before project-specific overlays
- all new packs MUST declare `schema_version: "2"` and `governance` block
- `data_classification` must reflect the most sensitive data the pack touches
- `eu_ai_act_tier: minimal_risk` applies to all internal engineering tooling packs
- validate after editing: `python3 core/scripts/validate-packs.py`

## Pack Discovery (2026)

Packs are discovered by AI agents via:

1. **IDE activation**: `activation.markers` + `activation.glob_patterns` in manifest (Cursor, VS Code, Kiro)
2. **A2A Agent Cards**: `core/a2a/.well-known/agent-registry.json` — agents look up role → toolbox → pack
3. **`/.well-known/agent-skills/index.json`**: Web-exposed canonical discovery endpoint (AAIF standard)
4. **`llms.txt`**: LLM-readable manifest index at repo root

MCP tool discovery is dynamic (JSON-RPC `tools/list`) and does not use static manifests.

## Standard 2026 Alignment

All 14 pack manifests follow `schema_version: "2"` and embed the
`governance` block (EU AI Act tier, audit logging, secret handling,
human oversight). The 2026 upgrade pass added Failure Modes, Output
Contracts, and Security Guardrails to the pack-level guidance.

### Failure Modes

- **Pack schema_version drift**: a manifest is edited to add fields but the schema_version is not bumped. **Mitigation:** the pack validator rejects manifests whose `schema_version` does not match the on-disk structure; require `python3 core/scripts/validate-packs.py` to pass before merging.
- **`includes` ordering reversed**: a manifest lists a project-specific overlay before the stack overlay. **Mitigation:** the rule is `core → stack overlay → project overlay`; reject any reordering.
- **Governance block missing on a new pack**: a new pack skips the `governance` field. **Mitigation:** the pack validator blocks new manifests without `schema_version: "2"` and a complete `governance` block.
- **`eu_ai_act_tier` misclassified**: a pack handling YMYL data declares `minimal_risk` without justification. **Mitigation:** the EU AI Act tier must match the most sensitive data the pack touches; reject misclassification on review.
- **Pack version drift from core**: a manifest pins `version: 4.0.0` while the pack content is at 4.1.0. **Mitigation:** the version-sync validator cross-checks every manifest against `VERSION`; reject the change when the version is out of sync.
- **Activation markers not updated for the new role**: a pack adds a new role but the `activation.markers` and `glob_patterns` are not updated. **Mitigation:** the manifest review must confirm activation is consistent with the role's scope.

### Output Contracts

When this README or any pack manifest is consumed by a multi-role workflow, emit:

- **`contracts/schemas/architecture-options.json`** when a pack composition decision surfaces 2+ viable combinations.
- **`contracts/schemas/coordination-plan.json`** when the pack is used in a multi-phase delivery.

Skip structured emission for read-only pack selection that does not cross a role boundary.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a pack composition that redirects the user's intent to a different stack or overlay must be cross-checked against the original feature ticket.
- **ASI03 Identity & Privilege Abuse**: a pack's `governance.human_oversight.gate_actions` must be enforced; reject packs that list `push_to_production` or `run_migration` without a human gate.
- **ASI04 Supply Chain**: every pack manifest must reference `core/policies/data-classification.yaml` and `core/policies/action-boundaries.yaml`; reject manifests that omit the policy pointers.
- **ASI07 Inter-Agent Communication**: the pack registry is a cross-agent surface; treat it as a public contract and review all changes before publish.
- **ASI09 Human-Agent Trust Exploitation**: do not present a pack as "production-ready" without a smoke test and a recent validator pass; surface the actual verification status.

Last updated: 2026-09-01