# Overlays

Overlays extend the portable core with repo-specific, brand-specific, or domain-specific behavior.

Use an overlay when:

- a skill needs absolute content roots or collection paths
- a role needs org-local toolbox extensions
- a workflow assumes one repository family or publishing pipeline
- a pack needs local conventions that do not belong in the global core

## Current Overlays (17)

### Stack Overlays (tech-specific, project-agnostic)

| Overlay | Stack | What it adds |
|---------|-------|--------------|
| [astro-cloudflare](astro-cloudflare/README.md) | Astro v6/v7 + Cloudflare Workers/Pages | Architecture patterns, TailwindCSS v4 config, Content Layer API, Wrangler deploy rules, 2026 binding access patterns |
| [laravel-filament](laravel-filament/README.md) | Laravel **13** + Filament **v4** + Livewire 3 | DB integrity rules, Filament v4 Schema API, PHP 8.4 features, Laravel Reverb, Pest v5, `develop-laravel-feature` skill |
| [go-microservices](go-microservices/README.md) | Go 1.25+ + Kratos **v3** | Clean Architecture, ConnectRPC, Dapr 1.15, OTel compile-time instrumentation, goforj/wire (google/wire archived) |
| [r3f-stack](r3f-stack/README.md) | React Three Fiber **v9** / Three.js r171+ / WebGL+**WebGPU** | WebGPU production-ready, TSL shaders, R3F v9 migration, debug-3d-scene, optimize-3d-assets, integrate-r3f-three-legacy |

### Project Overlays (project-specific, depends on a stack overlay)

| Overlay | Project | Depends On |
|---------|---------|------------|
| [maydiengiaisaigon](maydiengiaisaigon/README.md) | Máy Điện Giải Sài Gòn e-commerce (Laravel 13, ~20 SKUs) | `laravel-filament` |
| [icm-main](icm-main/README.md) | ICM Factory Direct corporate site (Astro v6+/Cloudflare, B2B sportswear) | `astro-cloudflare` |
| [golf-icm](golf-icm/README.md) | Golf ICM niche catalog (Astro v6+/Cloudflare, golf apparel) | `astro-cloudflare` |
| [sport-icm](sport-icm/README.md) | Sport ICM niche catalog (Astro v6+/Cloudflare, sportswear) | `astro-cloudflare` |
| [obj-configurator](obj-configurator/README.md) | OBJ 3D Configurator (Astro + R3F v9/Three.js r171+, WebGPU) | `astro-cloudflare` |
| [ecommerce-microservices](ecommerce-microservices/README.md) | Ecommerce microservices platform (planned) | `go-microservices` |
| [donthan-web](donthan-web/README.md) | Donthan.com livestream platform (web-first desktop UX) | standalone |

### Content & Domain Overlays (domain-specific, project-agnostic)

| Overlay | Domain | What it adds |
|---------|-------|--------------|
| [vesviet-content](vesviet-content/README.md) | Vesviet / Learn Hugo twin sites (content + SEO) | Technical Article Standard 2027 (7 gates), twin SEO authority + AI-citation rules, hub-and-spoke topology, `write-vesviet-learn-content` + `audit-technical-article` skills, masterclass batch workflow |
| [lease-content](lease-content/README.md) | Lease in Vietnam / Máy Lạnh Treo Tường (Astro) | Content schema, GEO/AEO baselines, `write-leaseinvietnam-maylanhtreotuong-data` skill |
| [seo-publishing](seo-publishing/README.md) | Dual-site SEO sprint | 7-day topic boards, 2026 GEO/AI visibility tracking, cannibalization rules, cadence runbook |
| [ui-design-system](ui-design-system/README.md) | UI design systems | Flow/component handoff conventions |
| [data-analyst-stack](data-analyst-stack/README.md) | DuckDB + Metabase BI + dbt 1.9 + Iceberg | BI metric templates, Metabase spec template, dbt microbatch, Iceberg REST Catalog patterns |
| [retail-data-warehouse](retail-data-warehouse/README.md) | Omnichannel retail platform (DuckDB 1.5+, MISA AMIS, VAS 14, PWA) | DuckDB Single-Writer, MISA AMIS VAS 14 voucher splitting, blind recount physical stocktaking, Decree 13/2023/ND-CP PII masking, plus `learning/` data-engineering track (merged from `data-engineer-rabity`: Iceberg, dbt 1.9, Kafka, Spark) |

## 2026 Critical Migration Notes

| Priority | Action | Overlays Affected |
|----------|--------|-------------------|
| 🚨 P0 | **Laravel 13** — L12 bug fix support ended Aug 13, 2026 | laravel-filament, maydiengiaisaigon |
| 🚨 P0 | **Filament v4** — unified `Schema` API (breaking from v3) | laravel-filament, maydiengiaisaigon |
| 🚨 P0 | **`google/wire` ARCHIVED** → goforj/wire or manual injection | go-microservices, ecommerce-microservices |
| 🟡 P1 | **Astro 6** — Content Layer mandatory, `env` bindings, TailwindCSS v4 | astro-cloudflare, icm-main, golf-icm, sport-icm, obj-configurator |
| 🟡 P1 | **Kratos v3** — import path changed, v2 maintenance-only | go-microservices |
| 🔵 P2 | **WebGPU + R3F v9** — `state.gl` → `state.renderer` | r3f-stack, obj-configurator |

## Overlay Authoring Rules

- keep overlays out of `core/` — portable core must work without any overlay loaded
- an overlay may extend rules, roles, skills, and workflows but must not break core validators
- project overlays MUST declare their stack overlay dependency in their README
- validate overlays together with core: `python3 core/scripts/validate-skills.py`
- declare SKILL.md YAML frontmatter with `name`, `description` for AI agent discoverability

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
