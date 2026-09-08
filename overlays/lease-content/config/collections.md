# Lease Content Collections

Astro `src/data` collection trees, schemas, and corpus inventory for the Lease
in Vietnam and Máy Lạnh Treo Tường sites. Snapshot: 2026-09-08. Canonical
corpus index: `leaseinvietnam/plan/CONTENT_INDEX.md` — regenerate it after every
batch, then refresh the counts here.

## Site Roots

| Site | Data path (workspace-relative) | Collections | Loader |
|------|-------------------------------|-------------|--------|
| Lease in Vietnam | `leaseinvietnam/src/data` | `post` (463 MDX), `property` (61 MD) | `glob('**/*.{md,mdx}')` |
| Máy Lạnh Treo Tường | `maylanhtreotuong/src/data` | `post`, `product` | same glob loader |

## Post Layout Convention

- Posts live in **category folders**, not dated folders:
  `src/data/post/<category>/<slug>.mdx`
- 12 categories: `guides` (112), `neighborhood` (69), `living` (50),
  `trust-safety` (41), `property-review` (33), `legal` (33), `market-radar` (25),
  `travel` (24), `market-data` (24), `scam` (20), `neighborhood-comparison` (18),
  `comparisons` (14)
- Use `.mdx` — the `<AnswerFirst>` component and layout imports require it.

## Post Schema (Zod, `src/content/config.ts`)

Required: `title`. Optional: `publishDate`, `updateDate`, `draft`, `excerpt`,
`image`, `category`, `tags`, `author`, `metadata` (canonical/robots/OpenGraph),
`anti_slop_gate` (boolean or `{ gate_passed, slop_sections_flagged,
boilerplate_removed, substance_elements_added }`), `postLayout` enum
(`GuideLayout` | `MarketRadarLayout` | `ScamAlertLayout` | `NeighborhoodLayout`
| `responsive`). The schema uses `.passthrough()` — layout-specific keys are
allowed; copy them from sibling posts using the same layout.

Editorial-gate fields (not schema-enforced but workflow-enforced):
`unique_angle`, `serp_title`, `faq` (frontmatter array), `substance_requirements`.

## Property Schema (Lease)

`title`, `price` (number, `currency` default VND), `bedrooms`, `bathrooms`,
`area`, `location`, `propertyType`, `agentId`, `coordinates {lat,lng}`, `gallery`,
`amenities`, `status`, `floorPlan`, `videoTour`, `tags`, `metadata`.
Houzez-extended fields supported via passthrough.

## 2026 Gate Coverage (leaseinvietnam)

| Gate | Coverage |
|---|---|
| `<AnswerFirst>` component | 463/463 |
| `author` + `publishDate` | 463/463 |
| `faq` block | 462/463 |
| `anti_slop_gate` | 452/463 |
| `unique_angle` | 450/463 |
| `serp_title` | 81/463 (backfill candidate) |
| Property cross-links | 457/463 posts link `/property/*` |

## Author Registry

`src/data/authors.ts` — 16 E-E-A-T persona slugs with verifiable credentials
(lawyers, CPA, MEP engineer, architect, MD). Frontmatter `author:` must
reference one of these slugs.
