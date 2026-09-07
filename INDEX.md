# Agent-Skills Master Index & Router

> **Location:** `core/` & `overlays/` | **Version:** `5.0.0` (A2A 1.0 + Antigravity)
> **Total Catalog:** **34 Roles** | **107 Skills** (97 Core + 10 Overlays) | **24 Workflows** | **50 Data Contracts**

---

## ⚡ Fast Invocation Protocol (`@<role>` & `@<skill>`)

When you mention `@<role>` and/or `@<skill>` in chat, Antigravity resolves them immediately using this index:

```markdown
# Single Role + Skill Example
@writer @research_and_writing - Viết bài hướng dẫn về Antigravity 2.0

# Developer Example
@backend @add_api_endpoint - Tạo REST API endpoint quản lý user orders

# Swarm Coordinator Example
@coordinator @a2a - Phối hợp @frontend và @backend hoàn thiện tính năng checkout
```

### Resolution Rules
1. **Role Matching:** `@<role>` resolves by exact name (e.g., `@content-writer`) or common alias (e.g., `@writer` → `content-writer`, `@be` → `backend-developer`).
2. **Skill Matching:** `@<skill>` resolves by exact name (e.g., `@conduct-research`), snake_case (e.g., `@conduct_research`), or composite alias (e.g., `@research_and_writing` → `conduct-research` + `write-article`).
3. **Automatic Loading:** The agent loads `core/roles/<role>.md` and all resolved `core/skills/<cat>/<skill>/SKILL.md` before executing.
4. **Contract Output:** Structured outputs must validate against `core/contracts/schemas/<schema>.json`.

---

## 🎭 Role Directory (34 Roles)

| Role Slug | Title | Common Aliases | Primary Skills | Role File |
|:---|:---|:---|:---|:---|
| **`@3d-graphics-engineer`** | 3D Graphics Engineer | `@3d`, `@r3f`, `@threejs` | `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets` *(+8 more)* | [`core/roles/3d-graphics-engineer.md`](./core/roles/3d-graphics-engineer.md) |
| **`@agent-coordinator`** | Agent Coordinator | `@coordinator`, `@swarm-coordinator` | `agent-a2a-protocol`, `agent-delegation`, `agent-graph-orchestration` *(+16 more)* | [`core/roles/agent-coordinator.md`](./core/roles/agent-coordinator.md) |
| **`@agent-discovery-engineer`** | Agent Discovery Engineer | `@discovery`, `@agent-discovery` | `manage-auth-md`, `configure-oauth-metadata`, `debug-identity-provider` *(+9 more)* | [`core/roles/agent-discovery-engineer.md`](./core/roles/agent-discovery-engineer.md) |
| **`@ai-systems-engineer`** | AI Systems Engineer | `@ai`, `@ml`, `@llm` | `setup-llm-gateway`, `setup-gpu-finops`, `implement-structured-outputs` *(+12 more)* | [`core/roles/ai-systems-engineer.md`](./core/roles/ai-systems-engineer.md) |
| **`@aws-engineer`** | AWS Engineer | `@aws`, `@cloud` | `aws-infrastructure`, `setup-deployment`, `add-telemetry-instrumentation` *(+9 more)* | [`core/roles/aws-engineer.md`](./core/roles/aws-engineer.md) |
| **`@backend-developer`** | Backend Developer | `@backend`, `@be`, `@backend-dev` | `add-api-endpoint`, `add-event-handler`, `add-service-client` *(+14 more)* | [`core/roles/backend-developer.md`](./core/roles/backend-developer.md) |
| **`@business-analyst`** | Business Analyst | `@ba`, `@business` | `analyze-business-requirements`, `ai-risk-assessment`, `agent-delegation` *(+5 more)* | [`core/roles/business-analyst.md`](./core/roles/business-analyst.md) |
| **`@cloudflare-engineer`** | Cloudflare Engineer | `@cloudflare`, `@cf`, `@workers` | `wrangler`, `durable-objects`, `turnstile-spin` *(+18 more)* | [`core/roles/cloudflare-engineer.md`](./core/roles/cloudflare-engineer.md) |
| **`@content-manager`** | Content Manager | — | `audit-content`, `repurpose-content`, `optimize-seo` *(+9 more)* | [`core/roles/content-manager.md`](./core/roles/content-manager.md) |
| **`@content-writer`** | Content Writer | `@writer`, `@copywriter`, `@author`, `@article-writer`, `@blog-writer` | `write-article`, `repurpose-content`, `audit-content` *(+7 more)* | [`core/roles/content-writer.md`](./core/roles/content-writer.md) |
| **`@data-analyst`** | Data Analyst | `@da`, `@data-analytics` | `analyze-data`, `analyze-business-requirements`, `build-data-pipeline` *(+5 more)* | [`core/roles/data-analyst.md`](./core/roles/data-analyst.md) |
| **`@data-engineer`** | Data Engineer | `@de`, `@data-eng` | `build-data-pipeline`, `database-maintenance`, `create-migration` *(+9 more)* | [`core/roles/data-engineer.md`](./core/roles/data-engineer.md) |
| **`@devops-engineer`** | DevOps Engineer | `@devops`, `@infra`, `@infrastructure` | `setup-deployment`, `debug-runtime-platform`, `add-telemetry-instrumentation` *(+12 more)* | [`core/roles/devops-engineer.md`](./core/roles/devops-engineer.md) |
| **`@ecommerce-engineer`** | Ecommerce Engineer | `@ecommerce`, `@ecom` | `integrate-payment-gateway`, `handle-checkout-flow`, `manage-product-catalog` *(+13 more)* | [`core/roles/ecommerce-engineer.md`](./core/roles/ecommerce-engineer.md) |
| **`@frontend-developer`** | Frontend Developer | `@frontend`, `@fe`, `@frontend-dev`, `@ui-developer` | `add-ui-component`, `add-page-route`, `integrate-api-client` *(+15 more)* | [`core/roles/frontend-developer.md`](./core/roles/frontend-developer.md) |
| **`@mmo-engineer`** | MMO Engineer | `@mmo`, `@affiliate`, `@growth` | `deploy-mmo-infrastructure`, `setup-tracking-system`, `create-automation-script` *(+7 more)* | [`core/roles/mmo-engineer.md`](./core/roles/mmo-engineer.md) |
| **`@mobile-engineer`** | Mobile Engineer | `@mobile`, `@flutter`, `@react-native` | `add-ui-component`, `integrate-api-client`, `write-tests` *(+9 more)* | [`core/roles/mobile-engineer.md`](./core/roles/mobile-engineer.md) |
| **`@product-manager`** | Product Manager | `@pm`, `@prod-mgr`, `@product-owner`, `@po` | `write-product-brief`, `meeting-review`, `analyze-business-requirements` *(+10 more)* | [`core/roles/product-manager.md`](./core/roles/product-manager.md) |
| **`@project-manager`** | Project Manager | `@pjm`, `@proj-mgr`, `@scrum-master` | `meeting-review`, `agent-delegation`, `agent-graph-orchestration` *(+8 more)* | [`core/roles/project-manager.md`](./core/roles/project-manager.md) |
| **`@qa-engineer`** | QA Engineer | `@qa`, `@tester`, `@test-engineer` | `write-tests`, `frontend-testing`, `agent-quality-gate` *(+9 more)* | [`core/roles/qa-engineer.md`](./core/roles/qa-engineer.md) |
| **`@researcher`** | Researcher | `@research`, `@deep-research` | `conduct-research`, `analyze-business-requirements`, `agent-delegation` *(+7 more)* | [`core/roles/researcher.md`](./core/roles/researcher.md) |
| **`@reviewer`** | Reviewer | `@code-reviewer`, `@pr-reviewer` | `review-code`, `review-service`, `configure-mcp` *(+7 more)* | [`core/roles/reviewer.md`](./core/roles/reviewer.md) |
| **`@security-engineer`** | Security Engineer | `@security`, `@sec`, `@appsec`, `@secops` | `security-audit`, `manage-secrets`, `supply-chain-security` *(+10 more)* | [`core/roles/security-engineer.md`](./core/roles/security-engineer.md) |
| **`@seo-analyst`** | SEO Analyst | `@seo`, `@seo-specialist`, `@seo-expert` | `optimize-seo`, `configure-agent-headers`, `configure-mcp` *(+7 more)* | [`core/roles/seo-analyst.md`](./core/roles/seo-analyst.md) |
| **`@solution-architect`** | Solution Architect | `@architect`, `@solution-arch`, `@solutions-architect` | `write-tech-radar`, `meeting-review`, `conduct-research` *(+9 more)* | [`core/roles/solution-architect.md`](./core/roles/solution-architect.md) |
| **`@sre`** | Site Reliability Engineer | `@reliability` | `debug-runtime-platform`, `troubleshoot-service`, `add-telemetry-instrumentation` *(+8 more)* | [`core/roles/sre.md`](./core/roles/sre.md) |
| **`@system-engineer`** | System Engineer | `@sysadmin`, `@system`, `@systems-engineer` | `system-design`, `performance-profiling`, `debug-runtime-platform` *(+17 more)* | [`core/roles/system-engineer.md`](./core/roles/system-engineer.md) |
| **`@task-planner`** | Task Planner | `@planner`, `@task-scheduler` | `design-ux-flow`, `plan-technical-delivery`, `meeting-review` *(+5 more)* | [`core/roles/task-planner.md`](./core/roles/task-planner.md) |
| **`@teacher`** | Teacher | `@instructor`, `@educator`, `@mentor` | `design-learning-plan`, `create-exercises`, `grade-and-review` *(+6 more)* | [`core/roles/teacher.md`](./core/roles/teacher.md) |
| **`@technical-architect`** | Technical Architect | `@tech-architect`, `@enterprise-architect` | `system-design`, `agent-panel-meeting`, `meeting-review` *(+12 more)* | [`core/roles/technical-architect.md`](./core/roles/technical-architect.md) |
| **`@technical-lead`** | Technical Lead | `@lead`, `@tech-lead`, `@engineering-lead` | `plan-technical-delivery`, `review-code`, `meeting-review` *(+18 more)* | [`core/roles/technical-lead.md`](./core/roles/technical-lead.md) |
| **`@technical-writer`** | Technical Writer | `@tech-writer`, `@doc-writer`, `@docs`, `@documentation-writer` | `write-documentation`, `release-notes`, `configure-llms-txt` *(+10 more)* | [`core/roles/technical-writer.md`](./core/roles/technical-writer.md) |
| **`@ui-ux-designer`** | UI/UX Designer | `@designer`, `@ui`, `@ux`, `@ui-ux`, `@uiux` | `design-ux-flow`, `design-review`, `meeting-review` *(+6 more)* | [`core/roles/ui-ux-designer.md`](./core/roles/ui-ux-designer.md) |
| **`@vietnam-accounting-specialist`** | Vietnam Accounting Specialist | `@accounting`, `@accountant`, `@ke-toan`, `@vietnam-accounting` | `manage-vietnam-accounting`, `analyze-business-requirements`, `analyze-data` *(+4 more)* | [`core/roles/vietnam-accounting-specialist.md`](./core/roles/vietnam-accounting-specialist.md) |

---

## 🛠️ Skill Directory (107 Skills)

### Category: `agent` (22 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@agent-a2a-protocol`** | Implement the full A2A 1.0 task lifecycle including Agent Card discovery, JSON-RPC invoke/stream, ta... | [`core/skills/agent/agent-a2a-protocol/SKILL.md`](./core/skills/agent/agent-a2a-protocol/SKILL.md) |
| **`@agent-context-management`** | Manage working context across long or multi-step agent tasks by tracking user intent, current phase,... | [`core/skills/agent/agent-context-management/SKILL.md`](./core/skills/agent/agent-context-management/SKILL.md) |
| **`@agent-delegation`** | Delegate scoped sub-tasks from a supervisor agent to specialist worker agents using structured A2A t... | [`core/skills/agent/agent-delegation/SKILL.md`](./core/skills/agent/agent-delegation/SKILL.md) |
| **`@agent-graph-orchestration`** | Model multi-phase delivery as a directed graph with parallel branches, phase gates, and A2A delegati... | [`core/skills/agent/agent-graph-orchestration/SKILL.md`](./core/skills/agent/agent-graph-orchestration/SKILL.md) |
| **`@agent-handoff`** | Produce concise agent handoffs, status updates, and completion summaries that preserve phase state, ... | [`core/skills/agent/agent-handoff/SKILL.md`](./core/skills/agent/agent-handoff/SKILL.md) |
| **`@agent-memory-compaction`** | Compact long-running agent conversation context into a minimal working state by preserving goals, co... | [`core/skills/agent/agent-memory-compaction/SKILL.md`](./core/skills/agent/agent-memory-compaction/SKILL.md) |
| **`@agent-model-routing`** | Select the most cost-effective model for each task or sub-task based on complexity, risk tier, and b... | [`core/skills/agent/agent-model-routing/SKILL.md`](./core/skills/agent/agent-model-routing/SKILL.md) |
| **`@agent-observability`** | Trace agent reasoning chains, tool call sequences, context injections, and token costs to enable deb... | [`core/skills/agent/agent-observability/SKILL.md`](./core/skills/agent/agent-observability/SKILL.md) |
| **`@agent-panel-meeting`** | Orchestrate a 6-round, multi-role cross-examination panel meeting to debate architecture, code, or f... | [`core/skills/agent/agent-panel-meeting/SKILL.md`](./core/skills/agent/agent-panel-meeting/SKILL.md) |
| **`@agent-prompt-lifecycle`** | Manage prompt assets through their full lifecycle including versioning, evaluation against golden da... | [`core/skills/agent/agent-prompt-lifecycle/SKILL.md`](./core/skills/agent/agent-prompt-lifecycle/SKILL.md) |
| **`@agent-quality-gate`** | Run and interpret repository quality gates for agent-delivered changes, including validators, lint, ... | [`core/skills/agent/agent-quality-gate/SKILL.md`](./core/skills/agent/agent-quality-gate/SKILL.md) |
| **`@agent-semantic-memory`** | Read from and write to persistent memory stores so agents retain codebase patterns, past fixes, and ... | [`core/skills/agent/agent-semantic-memory/SKILL.md`](./core/skills/agent/agent-semantic-memory/SKILL.md) |
| **`@agent-tool-orchestration`** | Plan and sequence agent tool use by choosing the smallest reliable tool, controlling work phase by p... | [`core/skills/agent/agent-tool-orchestration/SKILL.md`](./core/skills/agent/agent-tool-orchestration/SKILL.md) |
| **`@configure-agent-commerce`** | Implements agentic commerce standards — x402 and Stripe's Machine Payments Protocol (MPP) for HTTP 4... | [`core/skills/agent/configure-agent-commerce/SKILL.md`](./core/skills/agent/configure-agent-commerce/SKILL.md) |
| **`@configure-agent-headers`** | Exposes well-known agentic endpoints via RFC 8288 HTTP Link headers and optional DNS-AID SVCB record... | [`core/skills/agent/configure-agent-headers/SKILL.md`](./core/skills/agent/configure-agent-headers/SKILL.md) |
| **`@configure-agent-skills`** | Creates and manages the agentskills.io manifest index at `/.well-known/agent-skills/index.json`, exp... | [`core/skills/agent/configure-agent-skills/SKILL.md`](./core/skills/agent/configure-agent-skills/SKILL.md) |
| **`@configure-mcp`** | Sets up the full MCP presence for a web service — experimental Server Card discovery, WebMCP browser... | [`core/skills/agent/configure-mcp/SKILL.md`](./core/skills/agent/configure-mcp/SKILL.md) |
| **`@configure-oauth-metadata`** | Configures well-known OAuth 2.0 and OpenID Connect discovery endpoints (`oauth-protected-resource`, ... | [`core/skills/agent/configure-oauth-metadata/SKILL.md`](./core/skills/agent/configure-oauth-metadata/SKILL.md) |
| **`@debug-identity-provider`** | Diagnoses and resolves failures reported by WorkOS Agentic Registration scanners, `isitagentready.co... | [`core/skills/agent/debug-identity-provider/SKILL.md`](./core/skills/agent/debug-identity-provider/SKILL.md) |
| **`@manage-agent-identity`** | Manages the full lifecycle of Non-Human Identities (NHI) for AI agent sessions — including provision... | [`core/skills/agent/manage-agent-identity/SKILL.md`](./core/skills/agent/manage-agent-identity/SKILL.md) |
| **`@manage-api-catalog`** | Use when publishing and maintaining RFC 9727 API Catalog registries for automated API discovery by a... | [`core/skills/agent/manage-api-catalog/SKILL.md`](./core/skills/agent/manage-api-catalog/SKILL.md) |
| **`@manage-auth-md`** | Use when creating, updating, or auditing the /auth.md file at the repository or domain root to ensur... | [`core/skills/agent/manage-auth-md/SKILL.md`](./core/skills/agent/manage-auth-md/SKILL.md) |

### Category: `backend` (6 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-api-endpoint`** | Add or modify a service endpoint by updating the local API contract, boundary validation, handler fl... | [`core/skills/backend/add-api-endpoint/SKILL.md`](./core/skills/backend/add-api-endpoint/SKILL.md) |
| **`@add-event-handler`** | Add or modify event publishers, consumers, or subscriber flows by following the repo's event contrac... | [`core/skills/backend/add-event-handler/SKILL.md`](./core/skills/backend/add-event-handler/SKILL.md) |
| **`@add-service-client`** | Add or modify a service-to-service client or downstream integration by following the repo's transpor... | [`core/skills/backend/add-service-client/SKILL.md`](./core/skills/backend/add-service-client/SKILL.md) |
| **`@build-mcp-server`** | Scaffolds and implements a new Model Context Protocol (MCP) server. Use when exposing new backend to... | [`core/skills/backend/build-mcp-server/SKILL.md`](./core/skills/backend/build-mcp-server/SKILL.md) |
| **`@implement-structured-outputs`** | Implements strict constrained decoding and validation for LLM responses. Use when enforcing JSON Sch... | [`core/skills/backend/implement-structured-outputs/SKILL.md`](./core/skills/backend/implement-structured-outputs/SKILL.md) |
| **`@scaffold-new-service`** | Bootstrap a new service or bounded component from repo-local templates and conventions. Use when cre... | [`core/skills/backend/scaffold-new-service/SKILL.md`](./core/skills/backend/scaffold-new-service/SKILL.md) |

### Category: `commerce` (4 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@handle-checkout-flow`** | Design and implement the end-to-end checkout flow including cart management, tax and shipping calcul... | [`core/skills/commerce/handle-checkout-flow/SKILL.md`](./core/skills/commerce/handle-checkout-flow/SKILL.md) |
| **`@integrate-payment-gateway`** | Integrate or extend a payment gateway (Stripe, VNPay, PayPal, Momo, etc.) into an e-commerce applica... | [`core/skills/commerce/integrate-payment-gateway/SKILL.md`](./core/skills/commerce/integrate-payment-gateway/SKILL.md) |
| **`@manage-order-fulfillment`** | Implement and manage the post-purchase order lifecycle including order status management, packing, s... | [`core/skills/commerce/manage-order-fulfillment/SKILL.md`](./core/skills/commerce/manage-order-fulfillment/SKILL.md) |
| **`@manage-product-catalog`** | Build or maintain a product catalog including product creation, variant management (size, color, SKU... | [`core/skills/commerce/manage-product-catalog/SKILL.md`](./core/skills/commerce/manage-product-catalog/SKILL.md) |

### Category: `content` (4 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@audit-content`** | Run a structured content refresh cycle on an existing published piece — audit current performance an... | [`core/skills/content/audit-content/SKILL.md`](./core/skills/content/audit-content/SKILL.md) |
| **`@optimize-seo`** | Research search intent, define keywords, produce SEO content briefs, audit on-page elements, optimiz... | [`core/skills/content/optimize-seo/SKILL.md`](./core/skills/content/optimize-seo/SKILL.md) |
| **`@repurpose-content`** | Extract and format micro-content variants (social threads, newsletters, short video scripts) from a ... | [`core/skills/content/repurpose-content/SKILL.md`](./core/skills/content/repurpose-content/SKILL.md) |
| **`@write-article`** | Plan, research, outline, and draft long-form articles and blog posts with explicit evidence discipli... | [`core/skills/content/write-article/SKILL.md`](./core/skills/content/write-article/SKILL.md) |

### Category: `documentation` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@configure-llms-txt`** | Create and maintain the llms.txt and llms-full.txt files for a domain or project, making documentati... | [`core/skills/documentation/configure-llms-txt/SKILL.md`](./core/skills/documentation/configure-llms-txt/SKILL.md) |
| **`@write-documentation`** | Draft or update technical documentation by following the repo's existing doc structure, audience nee... | [`core/skills/documentation/write-documentation/SKILL.md`](./core/skills/documentation/write-documentation/SKILL.md) |
| **`@write-tech-radar`** | Draft or update a technology radar entry by summarizing context, trade-offs, recommendation, and ado... | [`core/skills/documentation/write-tech-radar/SKILL.md`](./core/skills/documentation/write-tech-radar/SKILL.md) |

### Category: `education` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@create-exercises`** | Design educational assignments, practice tests, and quizzes following designated curriculum matrices... | [`core/skills/education/create-exercises/SKILL.md`](./core/skills/education/create-exercises/SKILL.md) |
| **`@design-learning-plan`** | Create a structured, curriculum-aligned learning plan or syllabus following ZPD pathways, SMART obje... | [`core/skills/education/design-learning-plan/SKILL.md`](./core/skills/education/design-learning-plan/SKILL.md) |
| **`@grade-and-review`** | Evaluate learner work and provide constructive feedback on the designated grading scale. Use when gr... | [`core/skills/education/grade-and-review/SKILL.md`](./core/skills/education/grade-and-review/SKILL.md) |

### Category: `foundation` (12 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@accessibility-review`** | Audit UI for keyboard navigation, focus order, screen-reader labels, color contrast, motion preferen... | [`core/skills/foundation/accessibility-review/SKILL.md`](./core/skills/foundation/accessibility-review/SKILL.md) |
| **`@ai-risk-assessment`** | Assess AI/ML system risks using NIST AI RMF 1.0 (Govern/Map/Measure/Manage) and NIST AI 600-1 GenAI ... | [`core/skills/foundation/ai-risk-assessment/SKILL.md`](./core/skills/foundation/ai-risk-assessment/SKILL.md) |
| **`@conduct-research`** | Execute iterative, deeply-verified research to discover, validate, and synthesize complex informatio... | [`core/skills/foundation/conduct-research/SKILL.md`](./core/skills/foundation/conduct-research/SKILL.md) |
| **`@create-migration`** | Create safe schema or data migrations by following the repo's local migration tool, naming rules, ro... | [`core/skills/foundation/create-migration/SKILL.md`](./core/skills/foundation/create-migration/SKILL.md) |
| **`@design-review`** | Review UX flows, visual hierarchy, interaction patterns, and design-system alignment against specs a... | [`core/skills/foundation/design-review/SKILL.md`](./core/skills/foundation/design-review/SKILL.md) |
| **`@design-ux-flow`** | Design or refine a UX flow by defining user goals, preserved behavior, screen states, interaction ru... | [`core/skills/foundation/design-ux-flow/SKILL.md`](./core/skills/foundation/design-ux-flow/SKILL.md) |
| **`@incident-report`** | Capture, structure, and communicate an incident from triage through resolution and prevention. Use w... | [`core/skills/foundation/incident-report/SKILL.md`](./core/skills/foundation/incident-report/SKILL.md) |
| **`@performance-profiling`** | Investigate latency, throughput, memory, and contention issues by baselining, profiling hot paths, a... | [`core/skills/foundation/performance-profiling/SKILL.md`](./core/skills/foundation/performance-profiling/SKILL.md) |
| **`@plan-technical-delivery`** | Turn architecture decisions and requirements into a delivery-ready technical plan with slices, quali... | [`core/skills/foundation/plan-technical-delivery/SKILL.md`](./core/skills/foundation/plan-technical-delivery/SKILL.md) |
| **`@release-notes`** | Draft, structure, and review release notes for a software change so that users, operators, and downs... | [`core/skills/foundation/release-notes/SKILL.md`](./core/skills/foundation/release-notes/SKILL.md) |
| **`@write-product-brief`** | Write or refine a product brief that makes user value, business outcome, preserved behavior, affecte... | [`core/skills/foundation/write-product-brief/SKILL.md`](./core/skills/foundation/write-product-brief/SKILL.md) |
| **`@write-tests`** | Add or update tests by following repo-local test conventions, choosing the right test scope, isolati... | [`core/skills/foundation/write-tests/SKILL.md`](./core/skills/foundation/write-tests/SKILL.md) |

### Category: `frontend` (7 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-page-route`** | Add or modify a page, screen, or route by following the repo's navigation, data-loading, layout, and... | [`core/skills/frontend/add-page-route/SKILL.md`](./core/skills/frontend/add-page-route/SKILL.md) |
| **`@add-ui-component`** | Add or evolve a reusable UI component by following the repo's design system, composition patterns, a... | [`core/skills/frontend/add-ui-component/SKILL.md`](./core/skills/frontend/add-ui-component/SKILL.md) |
| **`@frontend-testing`** | Add or improve frontend test coverage by choosing the right UI test scope, reusing local tooling, an... | [`core/skills/frontend/frontend-testing/SKILL.md`](./core/skills/frontend/frontend-testing/SKILL.md) |
| **`@implement-webmcp`** | Exposes browser context, DOM state, and client-side actions to AI agents via WebMCP. Use when enabli... | [`core/skills/frontend/implement-webmcp/SKILL.md`](./core/skills/frontend/implement-webmcp/SKILL.md) |
| **`@integrate-api-client`** | Connect frontend code to backend APIs by following the repo's request, caching, auth, error-handling... | [`core/skills/frontend/integrate-api-client/SKILL.md`](./core/skills/frontend/integrate-api-client/SKILL.md) |
| **`@setup-design-system`** | Configure a scalable design system, styling framework, and component architecture for a frontend pro... | [`core/skills/frontend/setup-design-system/SKILL.md`](./core/skills/frontend/setup-design-system/SKILL.md) |
| **`@setup-visual-regression`** | Configure automated visual diffing for UI components and pages. Use when establishing pixel-level re... | [`core/skills/frontend/setup-visual-regression/SKILL.md`](./core/skills/frontend/setup-visual-regression/SKILL.md) |

### Category: `meetings-analysis` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@analyze-business-requirements`** | Analyze and write business requirements by making actors, business rules, state transitions, excepti... | [`core/skills/meetings-analysis/analyze-business-requirements/SKILL.md`](./core/skills/meetings-analysis/analyze-business-requirements/SKILL.md) |
| **`@analyze-data`** | Explore analytical datasets using DuckDB/Polars, query canonical Semantic Metric Catalogs to elimina... | [`core/skills/meetings-analysis/analyze-data/SKILL.md`](./core/skills/meetings-analysis/analyze-data/SKILL.md) |
| **`@meeting-review`** | Run a structured multi-perspective review of a topic, proposal, code area, bug, feature, or risky ch... | [`core/skills/meetings-analysis/meeting-review/SKILL.md`](./core/skills/meetings-analysis/meeting-review/SKILL.md) |

### Category: `mmo` (7 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@analyze-campaign-roi`** | Analyze S2S conversion data, monitor ad account die-rates, and calculate campaign ROI based on proxy... | [`core/skills/mmo/analyze-campaign-roi/SKILL.md`](./core/skills/mmo/analyze-campaign-roi/SKILL.md) |
| **`@create-automation-script`** | Build Playwright/Puppeteer automation scripts that connect via CDP to Anti-Detect browsers or use C+... | [`core/skills/mmo/create-automation-script/SKILL.md`](./core/skills/mmo/create-automation-script/SKILL.md) |
| **`@deploy-mmo-infrastructure`** | Deploy and manage proxy pools (Residential/4G) and Anti-Detect Browser orchestration environments (v... | [`core/skills/mmo/deploy-mmo-infrastructure/SKILL.md`](./core/skills/mmo/deploy-mmo-infrastructure/SKILL.md) |
| **`@deploy-proxyware-fleet`** | Containerize and orchestrate massive fleets of passive income nodes (Honeygain, EarnApp, Pawns.app) ... | [`core/skills/mmo/deploy-proxyware-fleet/SKILL.md`](./core/skills/mmo/deploy-proxyware-fleet/SKILL.md) |
| **`@generate-mmo-content`** | Use AI APIs to procedurally generate landing pages, creatives, and spin content for large-scale camp... | [`core/skills/mmo/generate-mmo-content/SKILL.md`](./core/skills/mmo/generate-mmo-content/SKILL.md) |
| **`@manage-mmo-assets`** | Manage and share MMO assets (Business Managers, Via, Pixels/Datasets, Anti-Detect profiles) using Ro... | [`core/skills/mmo/manage-mmo-assets/SKILL.md`](./core/skills/mmo/manage-mmo-assets/SKILL.md) |
| **`@setup-tracking-system`** | Configure advanced privacy-first tracking including Server-to-Server (S2S) postbacks, Meta Conversio... | [`core/skills/mmo/setup-tracking-system/SKILL.md`](./core/skills/mmo/setup-tracking-system/SKILL.md) |

### Category: `overlay/golf-icm` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-golf-feature`** | Develop features for the Golf ICM niche catalog — an Astro v5 golf apparel site on Cloudflare Pages.... | [`overlays/golf-icm/skills/develop-golf-feature/SKILL.md`](./overlays/golf-icm/skills/develop-golf-feature/SKILL.md) |

### Category: `overlay/icm-main` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-icm-feature`** | Develop features for the ICM Factory Direct main site — an Astro v5 B2B manufacturing catalog on Clo... | [`overlays/icm-main/skills/develop-icm-feature/SKILL.md`](./overlays/icm-main/skills/develop-icm-feature/SKILL.md) |

### Category: `overlay/laravel-filament` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-laravel-feature`** | Develop features in a Laravel 13 + Filament v4 + Livewire 3 monolith. Use when adding admin resource... | [`overlays/laravel-filament/skills/develop-laravel-feature/SKILL.md`](./overlays/laravel-filament/skills/develop-laravel-feature/SKILL.md) |

### Category: `overlay/lease-content` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@write-leaseinvietnam-maylanhtreotuong-data`** | Draft or update Astro Content Collection Markdown/MDX for the Lease in Vietnam and Máy Lạnh Treo Tườ... | [`overlays/lease-content/skills/write-leaseinvietnam-maylanhtreotuong-data/SKILL.md`](./overlays/lease-content/skills/write-leaseinvietnam-maylanhtreotuong-data/SKILL.md) |

### Category: `overlay/maydiengiaisaigon` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-mdg-feature`** | Develop features for the Máy Điện Giải Sài Gòn Laravel 13 + Filament v4 e-commerce. Use when adding ... | [`overlays/maydiengiaisaigon/skills/develop-mdg-feature/SKILL.md`](./overlays/maydiengiaisaigon/skills/develop-mdg-feature/SKILL.md) |

### Category: `overlay/obj-configurator` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-obj-feature`** | Develop features for the OBJ 3D Product Configurator — an Astro + React Three Fiber app with Three.j... | [`overlays/obj-configurator/skills/develop-obj-feature/SKILL.md`](./overlays/obj-configurator/skills/develop-obj-feature/SKILL.md) |

### Category: `overlay/r3f-stack` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@debug-3d-scene`** | Debug 3D scene behavior by tracing scene graph structure, transforms, raycasting, decals, materials,... | [`overlays/r3f-stack/skills/debug-3d-scene/SKILL.md`](./overlays/r3f-stack/skills/debug-3d-scene/SKILL.md) |
| **`@integrate-r3f-three-legacy`** | Integrate or migrate between React Three Fiber and legacy imperative Three.js code by controlling sc... | [`overlays/r3f-stack/skills/integrate-r3f-three-legacy/SKILL.md`](./overlays/r3f-stack/skills/integrate-r3f-three-legacy/SKILL.md) |
| **`@optimize-3d-assets`** | Optimize 3D assets and rendering inputs by reviewing model formats, geometry density, texture memory... | [`overlays/r3f-stack/skills/optimize-3d-assets/SKILL.md`](./overlays/r3f-stack/skills/optimize-3d-assets/SKILL.md) |

### Category: `overlay/vesviet-content` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@write-vesviet-learn-content`** | Draft or update Hugo Markdown for the Vesviet portfolio site or the Learn notes site. Use when creat... | [`overlays/vesviet-content/skills/write-vesviet-learn-content/SKILL.md`](./overlays/vesviet-content/skills/write-vesviet-learn-content/SKILL.md) |

### Category: `platform` (16 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-telemetry-instrumentation`** | Add or update logging, metrics, and tracing by following the repo's observability patterns and OpenT... | [`core/skills/platform/add-telemetry-instrumentation/SKILL.md`](./core/skills/platform/add-telemetry-instrumentation/SKILL.md) |
| **`@aws-infrastructure`** | Provision, configure, and optimize AWS managed services following IaC-first discipline. Use when pro... | [`core/skills/platform/aws-infrastructure/SKILL.md`](./core/skills/platform/aws-infrastructure/SKILL.md) |
| **`@cloudflare-email-service`** | Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing).... | [`core/skills/platform/cloudflare-email-service/SKILL.md`](./core/skills/platform/cloudflare-email-service/SKILL.md) |
| **`@debug-runtime-platform`** | Investigate deployment, environment, runtime, and rollout issues that are not purely application-cod... | [`core/skills/platform/debug-runtime-platform/SKILL.md`](./core/skills/platform/debug-runtime-platform/SKILL.md) |
| **`@debug-workers-edge`** | Diagnose Cloudflare Pages and Workers failures at the edge — 5xx, binding errors, Wrangler deploy fa... | [`core/skills/platform/debug-workers-edge/SKILL.md`](./core/skills/platform/debug-workers-edge/SKILL.md) |
| **`@durable-objects`** | Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, m... | [`core/skills/platform/durable-objects/SKILL.md`](./core/skills/platform/durable-objects/SKILL.md) |
| **`@sandbox-sdk`** | Builds secure, isolated code execution environments on Cloudflare Workers using the Cloudflare Sandb... | [`core/skills/platform/sandbox-sdk/SKILL.md`](./core/skills/platform/sandbox-sdk/SKILL.md) |
| **`@setup-deployment`** | Add or update deployment source-of-truth configuration for a service or component. Use when a change... | [`core/skills/platform/setup-deployment/SKILL.md`](./core/skills/platform/setup-deployment/SKILL.md) |
| **`@setup-gpu-finops`** | Configure GPU telemetry, DCGM metrics, and Kubecost to attribute AI compute costs to specific namesp... | [`core/skills/platform/setup-gpu-finops/SKILL.md`](./core/skills/platform/setup-gpu-finops/SKILL.md) |
| **`@setup-llm-gateway`** | Configure a centralized LLM proxy gateway for token routing, budgeting, and failover. Use when deplo... | [`core/skills/platform/setup-llm-gateway/SKILL.md`](./core/skills/platform/setup-llm-gateway/SKILL.md) |
| **`@supply-chain-security`** | Implement software supply chain security by generating SBOMs (CycloneDX/SPDX), enforcing SLSA build ... | [`core/skills/platform/supply-chain-security/SKILL.md`](./core/skills/platform/supply-chain-security/SKILL.md) |
| **`@system-design`** | Design, specify, and document complex system architectures covering compute, network, storage, middl... | [`core/skills/platform/system-design/SKILL.md`](./core/skills/platform/system-design/SKILL.md) |
| **`@turnstile-spin`** | Implements end-to-end Cloudflare Turnstile CAPTCHA protection — widget creation, managed siteverify ... | [`core/skills/platform/turnstile-spin/SKILL.md`](./core/skills/platform/turnstile-spin/SKILL.md) |
| **`@web-perf`** | Analyzes web page performance using Chrome DevTools MCP — measuring Core Web Vitals (LCP, INP, CLS),... | [`core/skills/platform/web-perf/SKILL.md`](./core/skills/platform/web-perf/SKILL.md) |
| **`@workers-best-practices`** | Reviews and authors Cloudflare Workers code against production best practices — covering async patte... | [`core/skills/platform/workers-best-practices/SKILL.md`](./core/skills/platform/workers-best-practices/SKILL.md) |
| **`@wrangler`** | Deploys, develops, and manages Cloudflare Workers and their bindings — KV, R2, D1, Vectorize, Hyperd... | [`core/skills/platform/wrangler/SKILL.md`](./core/skills/platform/wrangler/SKILL.md) |

### Category: `repo-ops` (5 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@commit-code`** | Validate and package a finished change into a clean commit by following repo-local validation, gener... | [`core/skills/repo-ops/commit-code/SKILL.md`](./core/skills/repo-ops/commit-code/SKILL.md) |
| **`@navigate-service`** | Navigate and understand an unfamiliar service by mapping its entrypoints, core flows, dependencies, ... | [`core/skills/repo-ops/navigate-service/SKILL.md`](./core/skills/repo-ops/navigate-service/SKILL.md) |
| **`@review-code`** | Review a diff since a fixed point along two separate axes — Standards (does the code follow this rep... | [`core/skills/repo-ops/review-code/SKILL.md`](./core/skills/repo-ops/review-code/SKILL.md) |
| **`@review-service`** | Review an entire service for release readiness. Use for full-service audits, production-readiness ch... | [`core/skills/repo-ops/review-service/SKILL.md`](./core/skills/repo-ops/review-service/SKILL.md) |
| **`@troubleshoot-service`** | Troubleshoot build, startup, runtime, dependency, and configuration issues by isolating the failing ... | [`core/skills/repo-ops/troubleshoot-service/SKILL.md`](./core/skills/repo-ops/troubleshoot-service/SKILL.md) |

### Category: `security-data` (5 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@build-data-pipeline`** | Design and implement transactional lakehouse pipelines (Iceberg/Delta), enforce ODCS v3.1.0 data con... | [`core/skills/security-data/build-data-pipeline/SKILL.md`](./core/skills/security-data/build-data-pipeline/SKILL.md) |
| **`@database-maintenance`** | Plan and execute operational data store and modern lakehouse maintenance, including Apache Iceberg/D... | [`core/skills/security-data/database-maintenance/SKILL.md`](./core/skills/security-data/database-maintenance/SKILL.md) |
| **`@manage-secrets`** | Add, update, rotate, or review secret handling by following the repo's source-of-truth, access-contr... | [`core/skills/security-data/manage-secrets/SKILL.md`](./core/skills/security-data/manage-secrets/SKILL.md) |
| **`@manage-vietnam-accounting`** | Prepare and review Vietnam accounting controls, accounting-regime evidence, reconciliations, invoice... | [`core/skills/security-data/manage-vietnam-accounting/SKILL.md`](./core/skills/security-data/manage-vietnam-accounting/SKILL.md) |
| **`@security-audit`** | Review code, configuration, and service behavior for security risks by checking trust boundaries, se... | [`core/skills/security-data/security-audit/SKILL.md`](./core/skills/security-data/security-audit/SKILL.md) |

---

## 🔀 Composite & Short Skill Aliases Matrix

| Mention / Shortcut | Resolves To Core Skills | Typical Role |
|:---|:---|:---|
| **`@a2a`** | `agent-a2a-protocol` | Active `@role` |
| **`@a2a_protocol`** | `agent-a2a-protocol` | Active `@role` |
| **`@accounting`** | `manage-vietnam-accounting` | Active `@role` |
| **`@add_api_endpoint`** | `add-api-endpoint` | Active `@role` |
| **`@add_event_handler`** | `add-event-handler` | Active `@role` |
| **`@add_page_route`** | `add-page-route` | Active `@role` |
| **`@add_service_client`** | `add-service-client` | Active `@role` |
| **`@add_ui_component`** | `add-ui-component` | Active `@role` |
| **`@agent_delegation`** | `agent-delegation` | Active `@role` |
| **`@analyze_business_requirements`** | `analyze-business-requirements` | Active `@role` |
| **`@analyze_data`** | `analyze-data` | Active `@role` |
| **`@api`** | `add-api-endpoint` | Active `@role` |
| **`@audit_content`** | `audit-content` | Active `@role` |
| **`@aws_infra`** | `aws-infrastructure` | Active `@role` |
| **`@aws_infrastructure`** | `aws-infrastructure` | Active `@role` |
| **`@build_data_pipeline`** | `build-data-pipeline` | Active `@role` |
| **`@build_mcp_server`** | `build-mcp-server` | Active `@role` |
| **`@business_requirements`** | `analyze-business-requirements` | Active `@role` |
| **`@conduct_research`** | `conduct-research` | Active `@role` |
| **`@content_audit`** | `audit-content` | Active `@role` |
| **`@create_api`** | `add-api-endpoint` | Active `@role` |
| **`@create_migration`** | `create-migration` | Active `@role` |
| **`@data_pipeline`** | `build-data-pipeline` | Active `@role` |
| **`@database`** | `database-maintenance` | Active `@role` |
| **`@db_maintenance`** | `database-maintenance` | Active `@role` |
| **`@deep_research`** | `conduct-research` | Active `@role` |
| **`@delegation`** | `agent-delegation` | Active `@role` |
| **`@deploy`** | `setup-deployment` | Active `@role` |
| **`@deployment`** | `setup-deployment` | Active `@role` |
| **`@design_system`** | `setup-design-system` | Active `@role` |
| **`@docs`** | `write-documentation` | Active `@role` |
| **`@documentation`** | `write-documentation` | Active `@role` |
| **`@e2e_tests`** | `write-tests` | Active `@role` |
| **`@event_handler`** | `add-event-handler` | Active `@role` |
| **`@frontend_testing`** | `frontend-testing` | Active `@role` |
| **`@graph_orchestration`** | `agent-graph-orchestration` | Active `@role` |
| **`@handoff`** | `agent-handoff` | Active `@role` |
| **`@implement_structured_outputs`** | `implement-structured-outputs` | Active `@role` |
| **`@instrumentation`** | `add-telemetry-instrumentation` | Active `@role` |
| **`@manage_secrets`** | `manage-secrets` | Active `@role` |
| **`@mcp_server`** | `build-mcp-server` | Active `@role` |
| **`@migration`** | `create-migration` | Active `@role` |
| **`@model_routing`** | `agent-model-routing` | Active `@role` |
| **`@new_endpoint`** | `add-api-endpoint` | Active `@role` |
| **`@optimize_seo`** | `optimize-seo` | Active `@role` |
| **`@orchestration`** | `agent-graph-orchestration` | Active `@role` |
| **`@page_route`** | `add-page-route` | Active `@role` |
| **`@perf`** | `performance-profiling` | Active `@role` |
| **`@performance`** | `performance-profiling` | Active `@role` |
| **`@performance_profiling`** | `performance-profiling` | Active `@role` |
| **`@product_brief`** | `write-product-brief` | Active `@role` |
| **`@quality_gate`** | `agent-quality-gate` | Active `@role` |
| **`@repurpose_content`** | `repurpose-content` | Active `@role` |
| **`@research`** | `conduct-research` | Active `@role` |
| **`@research-and-writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@research_and_writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@research_writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@scaffold_new_service`** | `scaffold-new-service` | Active `@role` |
| **`@scaffold_service`** | `scaffold-new-service` | Active `@role` |
| **`@secrets`** | `manage-secrets` | Active `@role` |
| **`@security`** | `security-audit` | Active `@role` |
| **`@security_audit`** | `security-audit` | Active `@role` |
| **`@semantic_memory`** | `agent-semantic-memory` | Active `@role` |
| **`@seo`** | `optimize-seo` | Active `@role` |
| **`@seo_optimization`** | `optimize-seo` | Active `@role` |
| **`@service_client`** | `add-service-client` | Active `@role` |
| **`@setup_deployment`** | `setup-deployment` | Active `@role` |
| **`@setup_design_system`** | `setup-design-system` | Active `@role` |
| **`@setup_visual_regression`** | `setup-visual-regression` | Active `@role` |
| **`@structured_outputs`** | `implement-structured-outputs` | Active `@role` |
| **`@supply_chain`** | `supply-chain-security` | Active `@role` |
| **`@tech_radar`** | `write-tech-radar` | Active `@role` |
| **`@telemetry`** | `add-telemetry-instrumentation` | Active `@role` |
| **`@test_report`** | `write-tests` | Active `@role` |
| **`@tests`** | `write-tests` | Active `@role` |
| **`@tool_orchestration`** | `agent-tool-orchestration` | Active `@role` |
| **`@ui_component`** | `add-ui-component` | Active `@role` |
| **`@unit_tests`** | `write-tests` | Active `@role` |
| **`@vietnam_accounting`** | `manage-vietnam-accounting` | Active `@role` |
| **`@visual_regression`** | `setup-visual-regression` | Active `@role` |
| **`@workers_best_practices`** | `workers-best-practices` | Active `@role` |
| **`@wrangler`** | `wrangler` | Active `@role` |
| **`@write_article`** | `write-article` | Active `@role` |
| **`@write_article_vietnamese`** | `write-article` | Active `@role` |
| **`@write_doc`** | `write-documentation` | Active `@role` |
| **`@write_docs`** | `write-documentation` | Active `@role` |
| **`@write_documentation`** | `write-documentation` | Active `@role` |
| **`@write_product_brief`** | `write-product-brief` | Active `@role` |
| **`@write_tech_radar`** | `write-tech-radar` | Active `@role` |
| **`@write_tests`** | `write-tests` | Active `@role` |
| **`@writing`** | `write-article` | Active `@role` |

---

## 🔄 Workflows (24 Workflows)

| Workflow | Title | File |
|:---|:---|:---|
| **`/add-new-feature`** | add-new-feature | [`core/workflows/add-new-feature.md`](./core/workflows/add-new-feature.md) |
| **`/agent-a2a-delegation`** | agent-a2a-delegation | [`core/workflows/agent-a2a-delegation.md`](./core/workflows/agent-a2a-delegation.md) |
| **`/bug-fix`** | bug-fix | [`core/workflows/bug-fix.md`](./core/workflows/bug-fix.md) |
| **`/build-deploy`** | build-deploy | [`core/workflows/build-deploy.md`](./core/workflows/build-deploy.md) |
| **`/code-review`** | code-review | [`core/workflows/code-review.md`](./core/workflows/code-review.md) |
| **`/content-audit`** | content-audit | [`core/workflows/content-audit.md`](./core/workflows/content-audit.md) |
| **`/content-publishing`** | content-publishing | [`core/workflows/content-publishing.md`](./core/workflows/content-publishing.md) |
| **`/curriculum-delivery`** | curriculum-delivery | [`core/workflows/curriculum-delivery.md`](./core/workflows/curriculum-delivery.md) |
| **`/data-migration`** | data-migration | [`core/workflows/data-migration.md`](./core/workflows/data-migration.md) |
| **`/data-pipeline-incident`** | data-pipeline-incident | [`core/workflows/data-pipeline-incident.md`](./core/workflows/data-pipeline-incident.md) |
| **`/dependency-upgrade`** | dependency-upgrade | [`core/workflows/dependency-upgrade.md`](./core/workflows/dependency-upgrade.md) |
| **`/feature-delivery`** | feature-delivery | [`core/workflows/feature-delivery.md`](./core/workflows/feature-delivery.md) |
| **`/hotfix-production`** | hotfix-production | [`core/workflows/hotfix-production.md`](./core/workflows/hotfix-production.md) |
| **`/period-end-closing`** | period-end-closing | [`core/workflows/period-end-closing.md`](./core/workflows/period-end-closing.md) |
| **`/qa-validation`** | qa-validation | [`core/workflows/qa-validation.md`](./core/workflows/qa-validation.md) |
| **`/refactoring`** | refactoring | [`core/workflows/refactoring.md`](./core/workflows/refactoring.md) |
| **`/revert-deployment`** | revert-deployment | [`core/workflows/revert-deployment.md`](./core/workflows/revert-deployment.md) |
| **`/security-incident-response`** | security-incident-response | [`core/workflows/security-incident-response.md`](./core/workflows/security-incident-response.md) |
| **`/seo-content-lifecycle`** | seo-content-lifecycle | [`core/workflows/seo-content-lifecycle.md`](./core/workflows/seo-content-lifecycle.md) |
| **`/seo-keyword-brief`** | seo-keyword-brief | [`core/workflows/seo-keyword-brief.md`](./core/workflows/seo-keyword-brief.md) |
| **`/service-review-release`** | service-review-release | [`core/workflows/service-review-release.md`](./core/workflows/service-review-release.md) |
| **`/setup-new-service`** | setup-new-service | [`core/workflows/setup-new-service.md`](./core/workflows/setup-new-service.md) |
| **`/tech-repo-review`** | tech-repo-review | [`core/workflows/tech-repo-review.md`](./core/workflows/tech-repo-review.md) |
| **`/troubleshooting`** | troubleshooting | [`core/workflows/troubleshooting.md`](./core/workflows/troubleshooting.md) |

---

## 📑 Data Contracts & Schemas (50 Schemas)

| Schema File | Schema Title | Path |
|:---|:---|:---|
| `a2a-artifact.json` | A2A Task Artifact | [`core/contracts/schemas/a2a-artifact.json`](./core/contracts/schemas/a2a-artifact.json) |
| `a2a-jsonrpc-envelope.json` | A2A JSON-RPC 2.0 Envelope | [`core/contracts/schemas/a2a-jsonrpc-envelope.json`](./core/contracts/schemas/a2a-jsonrpc-envelope.json) |
| `a2a-message.json` | A2A Message | [`core/contracts/schemas/a2a-message.json`](./core/contracts/schemas/a2a-message.json) |
| `a2a-push-notification-config.json` | A2A Push Notification Config | [`core/contracts/schemas/a2a-push-notification-config.json`](./core/contracts/schemas/a2a-push-notification-config.json) |
| `a2a-task-cancel.json` | A2A Task Cancel Request | [`core/contracts/schemas/a2a-task-cancel.json`](./core/contracts/schemas/a2a-task-cancel.json) |
| `a2a-task-progress.json` | A2A Task Progress Event | [`core/contracts/schemas/a2a-task-progress.json`](./core/contracts/schemas/a2a-task-progress.json) |
| `a2a-task-status.json` | A2A Task Status | [`core/contracts/schemas/a2a-task-status.json`](./core/contracts/schemas/a2a-task-status.json) |
| `a2a-task.json` | A2A Task Delegation | [`core/contracts/schemas/a2a-task.json`](./core/contracts/schemas/a2a-task.json) |
| `accounting-compliance-review.json` | Vietnam Accounting Compliance Review | [`core/contracts/schemas/accounting-compliance-review.json`](./core/contracts/schemas/accounting-compliance-review.json) |
| `adr-spec.json` | Architecture Decision Record | [`core/contracts/schemas/adr-spec.json`](./core/contracts/schemas/adr-spec.json) |
| `agent-card.json` | A2A Agent Card | [`core/contracts/schemas/agent-card.json`](./core/contracts/schemas/agent-card.json) |
| `agent-trace-span.json` | Agent Trace Span | [`core/contracts/schemas/agent-trace-span.json`](./core/contracts/schemas/agent-trace-span.json) |
| `ai-risk-register.json` | AI Risk Register | [`core/contracts/schemas/ai-risk-register.json`](./core/contracts/schemas/ai-risk-register.json) |
| `amis-voucher-contract.json` | AMIS Accounting Voucher Contract | [`core/contracts/schemas/amis-voucher-contract.json`](./core/contracts/schemas/amis-voucher-contract.json) |
| `api-contract-spec.json` | API Contract Specification | [`core/contracts/schemas/api-contract-spec.json`](./core/contracts/schemas/api-contract-spec.json) |
| `architecture-options.json` | Architecture Options Brief | [`core/contracts/schemas/architecture-options.json`](./core/contracts/schemas/architecture-options.json) |
| `aws-infra-spec.json` | AWS Infrastructure Specification | [`core/contracts/schemas/aws-infra-spec.json`](./core/contracts/schemas/aws-infra-spec.json) |
| `code-review-finding.json` | Code Review Finding | [`core/contracts/schemas/code-review-finding.json`](./core/contracts/schemas/code-review-finding.json) |
| `content-audit-report.json` | Content Audit Report | [`core/contracts/schemas/content-audit-report.json`](./core/contracts/schemas/content-audit-report.json) |
| `content-handoff.json` | Content Handoff | [`core/contracts/schemas/content-handoff.json`](./core/contracts/schemas/content-handoff.json) |
| `coordination-plan.json` | Coordination Plan | [`core/contracts/schemas/coordination-plan.json`](./core/contracts/schemas/coordination-plan.json) |
| `data-analysis-report.json` | Data Analysis Report | [`core/contracts/schemas/data-analysis-report.json`](./core/contracts/schemas/data-analysis-report.json) |
| `data-pipeline-spec.json` | Data Pipeline Specification | [`core/contracts/schemas/data-pipeline-spec.json`](./core/contracts/schemas/data-pipeline-spec.json) |
| `deployment-plan.json` | Deployment Plan | [`core/contracts/schemas/deployment-plan.json`](./core/contracts/schemas/deployment-plan.json) |
| `documentation-handoff.json` | Documentation Handoff | [`core/contracts/schemas/documentation-handoff.json`](./core/contracts/schemas/documentation-handoff.json) |
| `edge-deployment-spec.json` | Edge Deployment Specification | [`core/contracts/schemas/edge-deployment-spec.json`](./core/contracts/schemas/edge-deployment-spec.json) |
| `feature-ticket.json` | Feature Ticket Specification | [`core/contracts/schemas/feature-ticket.json`](./core/contracts/schemas/feature-ticket.json) |
| `implementation-result.json` | Implementation Result | [`core/contracts/schemas/implementation-result.json`](./core/contracts/schemas/implementation-result.json) |
| `incident-report.json` | Incident Report | [`core/contracts/schemas/incident-report.json`](./core/contracts/schemas/incident-report.json) |
| `learning-assessment-report.json` | Learning Assessment Report | [`core/contracts/schemas/learning-assessment-report.json`](./core/contracts/schemas/learning-assessment-report.json) |
| `learning-handoff.json` | Learning Handoff | [`core/contracts/schemas/learning-handoff.json`](./core/contracts/schemas/learning-handoff.json) |
| `performance-audit.json` | Performance Audit Result | [`core/contracts/schemas/performance-audit.json`](./core/contracts/schemas/performance-audit.json) |
| `period-end-closing-report.json` | Period-End Closing Report | [`core/contracts/schemas/period-end-closing-report.json`](./core/contracts/schemas/period-end-closing-report.json) |
| `pull-request-spec.json` | Pull Request Specification | [`core/contracts/schemas/pull-request-spec.json`](./core/contracts/schemas/pull-request-spec.json) |
| `research-report.json` | Research Report Specification | [`core/contracts/schemas/research-report.json`](./core/contracts/schemas/research-report.json) |
| `schema-migration.json` | Schema Migration Plan | [`core/contracts/schemas/schema-migration.json`](./core/contracts/schemas/schema-migration.json) |
| `security-audit.json` | Security Audit Report | [`core/contracts/schemas/security-audit.json`](./core/contracts/schemas/security-audit.json) |
| `seo-audit-report.json` | SEO Audit Report | [`core/contracts/schemas/seo-audit-report.json`](./core/contracts/schemas/seo-audit-report.json) |
| `seo-content-brief.json` | SEO Content Brief | [`core/contracts/schemas/seo-content-brief.json`](./core/contracts/schemas/seo-content-brief.json) |
| `seo-metadata.json` | SEO Metadata | [`core/contracts/schemas/seo-metadata.json`](./core/contracts/schemas/seo-metadata.json) |
| `seo-weekly-board.json` | SEO Weekly Board | [`core/contracts/schemas/seo-weekly-board.json`](./core/contracts/schemas/seo-weekly-board.json) |
| `series-article.json` | Series Article | [`core/contracts/schemas/series-article.json`](./core/contracts/schemas/series-article.json) |
| `solution-brief.json` | Solution Brief | [`core/contracts/schemas/solution-brief.json`](./core/contracts/schemas/solution-brief.json) |
| `stock-audit-session.json` | Stock Audit Session Contract | [`core/contracts/schemas/stock-audit-session.json`](./core/contracts/schemas/stock-audit-session.json) |
| `system-design-spec.json` | System Design Specification | [`core/contracts/schemas/system-design-spec.json`](./core/contracts/schemas/system-design-spec.json) |
| `technical-delivery-plan.json` | Technical Delivery Plan | [`core/contracts/schemas/technical-delivery-plan.json`](./core/contracts/schemas/technical-delivery-plan.json) |
| `test-report.json` | QA Test Report | [`core/contracts/schemas/test-report.json`](./core/contracts/schemas/test-report.json) |
| `ui-component-spec.json` | UI Component Specification | [`core/contracts/schemas/ui-component-spec.json`](./core/contracts/schemas/ui-component-spec.json) |
| `ux-flow-spec.json` | UX Flow Specification | [`core/contracts/schemas/ux-flow-spec.json`](./core/contracts/schemas/ux-flow-spec.json) |
| `validation-result.json` | Validation Result | [`core/contracts/schemas/validation-result.json`](./core/contracts/schemas/validation-result.json) |