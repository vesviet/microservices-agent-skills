---
trigger: always_on
glob: "**"
description: "Context and rules for the microservices e-commerce project."
---

# ROLE: SENIOR FULLSTACK ENGINEER (10+ YRS EXP)

# Microservices Project Context

## Project Overview
This is a comprehensive, production-grade e-commerce microservices platform.
- **Status**: ~88% Complete, Production-Ready.
- **Tech Stack**: Go 1.25+ (Kratos Framework), Next.js/React, local k3d/k3s Kubernetes cluster, Dapr (Service Mesh), Consul (Service Discovery), PostgreSQL, Redis, Elasticsearch.
- **Architecture**: Clean Architecture, Domain-Driven Design (DDD), Event-Driven Architecture.

## Service Registry
### Core Business
- **auth**: Authentication & Authorization (OAuth2, JWT).
- **user**: Admin user management & RBAC.
- **customer**: Customer profiles, segments, GDPR.
- **catalog**: Product catalog (EAV pattern, 25k+ SKUs).
- **order**: Order management, cart, checkout.
- **payment**: Multi-gateway payment processing.

### Operations & Logistics
- **warehouse**: Inventory management, stock reservations.
- **fulfillment**: Order processing, pick/pack/ship.
- **shipping**: Multi-carrier shipping integration.
- **location**: Geographic data & delivery zones.

### Growth & Intelligence
- **pricing**: Dynamic pricing engine & rules.
- **promotion**: Discount campaigns & coupons.
- **loyalty-rewards**: Points & rewards system.
- **review**: Product reviews & ratings.
- **search**: AI-powered product search & discovery.
- **analytics**: Business intelligence & metrics.
- **notification**: Multi-channel notifications (Email, SMS).

### Infrastructure & Frontend
- **gateway**: API Gateway (routing, security).
- **common**: Shared Go libraries & utilities (`gitlab.com/ta-microservices/common`).
- **frontend**: Customer-facing Next.js application.
- **admin**: Admin dashboard (React/Vite).

## Key Documentation Locations
- **Architecture**: `docs/SYSTEM_ARCHITECTURE_OVERVIEW.md`
- **Codebase Index**: `docs/CODEBASE_INDEX.md`
- **Business Workflows**: `docs/workflow/*.md` (Critical for understanding logic).
- **API Specs**: `docs/openapi/` or `api/` folder in each service.
- **Status & Roadmap**: `docs/workflow/PROJECT_STATUS.md`
- **Review**: `docs/TEAM_LEAD_CODE_REVIEW_GUIDE.md`

## Development Standards
- **Entry Points**: `cmd/<service>/main.go` or `cmd/server/main.go`.
- **Domain Logic**: `internal/biz/` (Clean Architecture).
- **Data Access**: `internal/data/` (Repositories).
- **API Layer**: `internal/service/` (gRPC/HTTP implementation).
- **Proto definitions**: `api/<service>/v1/`.
- **Migrations**: `migrations/` (Goose).
- **Common Lib Use**: Prefer `gitlab.com/ta-microservices/common` for shared logic.
- **CRITICAL — Check Before Creating**: Before proposing to add ANY new code to `common` or to any service, ALWAYS thoroughly search the existing `common` library first (grep all packages: `data/`, `utils/`, `repository/`, `client/`, `events/`, `outbox/`, `worker/`, `registry/`, `config/`). Many interfaces and utilities already exist — import them instead of duplicating. This applies to: transaction managers, cache helpers, event publishers, gRPC factories, outbox patterns, etc.
- **Commenting Rules**: Do not use "P-0" or "[ ]" format in code comments. Keep code explanation comments to a maximum of 3 lines.
