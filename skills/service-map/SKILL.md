---
name: service-map
description: Quick-reference map of all microservices — locations, ports, dependencies, gRPC clients, event consumers, GitOps config, and where to find things
---

# Service Map Skill

Use this skill as a **quick-reference index** before working on any service. It tells you exactly where things are, what depends on what, and how GitOps is configured.

## When to Use
- Before navigating to any service code
- When asked to find where logic/config lives
- When checking inter-service dependencies
- When working on GitOps/deployment configuration
- When asked "where does X happen?" or "what service handles Y?"

---

## Workspace Layout

```
d:\microservices\                     # Root workspace
├── .agent/skills/                    # Agent skills (this file)
├── common/                           # Shared Go library (gitlab.com/ta-microservices/common)
├── docs/                             # Platform documentation
├── gitops/                           # GitOps repo (Kustomize + ArgoCD) ← DEPLOYMENT CONFIG
├── argocd/                           # ArgoCD Helm charts (legacy, being migrated to gitops/)
├── gitlab-ci-templates/              # Shared CI templates
├── k8s/                              # Raw K8s manifests (legacy)
├── git-all.sh                        # Script to git pull all repos
├── microservices.code-workspace      # VS Code workspace file
│
│── # ─── Core Business Services (13) ───
├── auth/                             # Authentication & authorization
├── user/                             # User profiles & RBAC
├── customer/                         # Customer profiles & addresses
├── catalog/                          # Product catalog & EAV attributes
├── pricing/                          # Dynamic pricing & tax
├── promotion/                        # Campaigns & coupons
├── checkout/                         # Cart & checkout orchestration
├── order/                            # Order lifecycle management
├── payment/                          # Payment processing & gateways
├── warehouse/                        # Inventory & stock management
├── fulfillment/                      # Picking, packing, shipping workflow
├── shipping/                         # Shipping methods, rates, tracking
├── return/                           # Returns & exchanges
│
│── # ─── Platform Services (5) ───
├── gateway/                          # API Gateway (Go, Chi router)
├── search/                           # Elasticsearch-powered search
├── analytics/                        # Business analytics & metrics
├── review/                           # Product reviews & ratings
├── common-operations/                # Task orchestration & MinIO file ops
│
│── # ─── Operational Services (5) ───
├── notification/                     # Email, SMS, push notifications
├── location/                         # Location tree (Country→Ward)
├── loyalty-rewards/                  # Points, tiers, rewards
├── admin/                            # Admin panel (React + Vite + Ant Design)
└── frontend/                         # Customer frontend (Next.js)
```

---

## Service Registry

### Go Backend Services

| # | Service | Directory | Module | HTTP | gRPC | Binaries |
|---|---------|-----------|--------|------|------|----------|
| 1 | Auth | `auth/` | `gitlab.com/ta-microservices/auth` | 8000 | 9000 | auth, migrate, worker |
| 2 | User | `user/` | `gitlab.com/ta-microservices/user` | 8001 | 9001 | user, migrate |
| 3 | Customer | `customer/` | `gitlab.com/ta-microservices/customer` | 8003 | 9003 | customer, migrate, worker |
| 4 | Catalog | `catalog/` | `gitlab.com/ta-microservices/catalog` | 8015 | 9015 | catalog, migrate, worker |
| 5 | Pricing | `pricing/` | `gitlab.com/ta-microservices/pricing` | 8002 | 9002 | pricing, migrate, worker |
| 6 | Promotion | `promotion/` | `gitlab.com/ta-microservices/promotion` | 8011 | 9011 | promotion, migrate, worker |
| 7 | Checkout | `checkout/` | `gitlab.com/ta-microservices/checkout` | 8010 | 9010 | server, migrate, worker |
| 8 | Order | `order/` | `gitlab.com/ta-microservices/order` | 8004 | 9004 | order, migrate, worker |
| 8 | Payment | `payment/` | `gitlab.com/ta-microservices/payment` | 8005 | 9005 | payment, migrate, worker |
| 9 | Warehouse | `warehouse/` | `gitlab.com/ta-microservices/warehouse` | 8006 | 9006 | warehouse, migrate, worker |
| 10 | Return | `return/` | `gitlab.com/ta-microservices/return` | 8013 | 9013 | return, migrate |
| 11 | Fulfillment | `fulfillment/` | `gitlab.com/ta-microservices/fulfillment` | 8008 | 9008 | fulfillment, migrate, worker |
| 11 | Shipping | `shipping/` | `gitlab.com/ta-microservices/shipping` | 8012 | 9012 | shipping, migrate, worker |
| 12 | Gateway | `gateway/` | `gitlab.com/ta-microservices/gateway` | 80 | — | gateway |
| 13 | Search | `search/` | `gitlab.com/ta-microservices/search` | 8017 | 9017 | search, migrate, worker, dlq-worker |
| 14 | Analytics | `analytics/` | `gitlab.com/ta-microservices/analytics` | 8019 | 9019 | server, migrate |
| 15 | Review | `review/` | `gitlab.com/ta-microservices/review` | 8016 | 9016 | review, migrate |
| 16 | Common Ops | `common-operations/` | `gitlab.com/ta-microservices/common-operations` | 8018 | 9018 | operations, worker |
| 17 | Notification | `notification/` | `gitlab.com/ta-microservices/notification` | 8009 | 9009 | notification, worker |
| 18 | Location | `location/` | `gitlab.com/ta-microservices/location` | 8007 | 9007 | location, migrate |
| 19 | Loyalty | `loyalty-rewards/` | `gitlab.com/ta-microservices/loyalty-rewards` | 8014 | 9014 | loyalty-rewards, migrate, worker |

### Frontend Services

| Service | Directory | Tech Stack | Port |
|---------|-----------|------------|------|
| Admin | `admin/` | React + Vite + Ant Design | 3001 |
| Frontend | `frontend/` | Next.js | 3000 |

---

## Service-to-Service Dependencies (gRPC Clients)

Shows which services each service calls via gRPC. Look in `internal/client/` for implementations.

| Service | Calls (gRPC Clients) |
|---------|---------------------|
| **auth** | — (no outbound calls) |
| **user** | — |
| **customer** | — |
| **catalog** | customer, pricing, promotion, warehouse |
| **pricing** | catalog, customer, warehouse |
| **checkout** | catalog, customer, order, payment, pricing, promotion, shipping, warehouse |
| **promotion** | catalog, customer, pricing, review, shipping |
| **order** | catalog, customer, notification, payment, pricing, promotion, shipping, user, warehouse |
| **payment** | customer, order |
| **return** | order, shipping |
| **fulfillment** | order, warehouse |
| **shipping** | catalog |
| **search** | catalog, catalog-visibility, pricing, warehouse |
| **loyalty-rewards** | customer, notification, order |
| **warehouse** | catalog, notification, user |
| **notification** | — |
| **location** | — |
| **analytics** | — |
| **review** | — |
| **common-ops** | notification (via event) |

---

## Event-Driven Communication (Dapr PubSub)

Shows which events each service consumes. Look in `internal/data/eventbus/` for consumer implementations.

| Service | Event Consumers |
|---------|----------------|
| **customer** | auth_consumer, order_consumer |
| **catalog** | price_consumer, stock_consumer |
| **pricing** | promo_consumer, stock_consumer |
| **order** | fulfillment_consumer, payment_consumer, shipping_consumer, warehouse_consumer |
| **payment** | return_consumer |
| **fulfillment** | order_status_consumer, picklist_status_consumer |
| **shipping** | package_status_consumer |
| **search** | cms_consumer, price_consumer, product_consumer, promotion_consumer, stock_consumer |
| **notification** | order_status_consumer, system_error_consumer |
| **warehouse** | fulfillment_status_consumer, order_status_consumer, product_created_consumer, return_consumer |

### Services with NO event consumers (publish only or no events):
- auth, user, promotion, location, analytics, review, common-operations, gateway

---

## Standard Go Service File Structure

When looking for specific functionality, use this guide:

| What You Need | Where to Find It |
|---------------|-----------------|
| **API endpoints** (proto definitions) | `api/<service>/v1/*.proto` |
| **API endpoint handlers** (HTTP/gRPC) | `internal/service/*.go` |
| **Business logic & rules** | `internal/biz/**/*.go` ← **MOST IMPORTANT** |
| **Domain entities & repo interfaces** | `internal/biz/<entity>/<entity>.go` |
| **Database queries & models** | `internal/data/postgres/*.go` |
| **Database models (GORM structs)** | `internal/data/model/*.go` or `internal/model/*.go` |
| **gRPC clients to other services** | `internal/client/*_client.go` |
| **Event consumers (Dapr PubSub)** | `internal/data/eventbus/*_consumer.go` |
| **Event publishers** | `internal/events/*.go` or `internal/biz/events/*.go` |
| **Background workers & cron jobs** | `internal/worker/**/*.go` |
| **HTTP/gRPC server setup** | `internal/server/http.go`, `internal/server/grpc.go` |
| **Middleware** | `internal/middleware/*.go` |
| **Config definition** | `internal/config/config.go` |
| **Config values** | `configs/config.yaml` |
| **Wire DI setup** | `cmd/<service>/wire.go` (DO NOT EDIT `wire_gen.go`) |
| **Database migrations** | `migrations/*.sql` (Goose format) |
| **Dapr subscriptions** | `dapr/subscription.yaml` |
| **CI pipeline** | `.gitlab-ci.yml` |
| **Dockerfile** | `Dockerfile` |
| **OpenAPI spec** | `openapi.yaml` |
| **Tests** | `internal/biz/**/*_test.go`, `test/` |

---

## Shared Common Library

**Location**: `common/` (module: `gitlab.com/ta-microservices/common`)

| Package | Purpose |
|---------|---------|
| `client/` | gRPC client factory, circuit breaker, service registry |
| `config/` | Config loader |
| `constants/` | Shared constants & event topics |
| `errors/` | Standard error types |
| `events/` | Dapr PubSub publisher/consumer, event validation |
| `grpc/` | gRPC error mapper |
| `idempotency/` | Event processing idempotency |
| `middleware/` | Auth, rate limiting, context helpers |
| `observability/` | Health checks, metrics |
| `repository/` | Base repository with pagination, filtering |
| `security/` | Password hashing, PII masking, filename sanitization |
| `utils/` | Cache, crypto, CSV, context, database, file, http, image, json, math, retry, uuid |
| `validation/` | Input validation, business rules |
| `worker/` | Base worker, continuous worker, event worker |

---

## GitOps Configuration

### Two GitOps Repos

| Repo | Directory | Purpose | Status |
|------|-----------|---------|--------|
| **gitops** | `gitops/` | Kustomize-based GitOps (NEW) | ✅ Active |
| **argocd** | `argocd/` | Helm-based ArgoCD charts (LEGACY) | 🔄 Being migrated |

### gitops/ Structure (Primary — Kustomize-based)

```
gitops/
├── bootstrap/                    # Root ArgoCD Applications
├── environments/
│   ├── dev/                      # Dev environment (k3d)
│   │   ├── apps/                 # ArgoCD Application manifests per service
│   │   ├── projects/             # ArgoCD Projects
│   │   └── resources/            # Environment resources
│   └── production/               # Production environment
├── apps/                         # Service Kustomize configs
│   └── <service>/
│       ├── base/                 # Base manifests
│       │   ├── kustomization.yaml  # Uses components + patches
│       │   ├── configmap.yaml
│       │   ├── migration-job.yaml
│       │   ├── networkpolicy.yaml
│       │   ├── pdb.yaml
│       │   ├── serviceaccount.yaml
│       │   └── servicemonitor.yaml
│       └── overlays/
│           ├── dev/              # Dev-specific patches
│           │   ├── kustomization.yaml
│           │   ├── configmap.yaml
│           │   └── deployment-patch.yaml
│           └── production/       # Prod-specific patches
│               ├── kustomization.yaml
│               ├── deployment-patch.yaml
│               └── hpa.yaml
├── components/                   # Reusable Kustomize components
│   ├── common-deployment/        # Standard Deployment template
│   ├── common-service/           # Standard Service template
│   ├── infrastructure-egress/    # Egress NetworkPolicy rules
│   └── imagepullsecret/          # Registry credentials
├── infrastructure/               # Infra components (Vault, DB, Redis, Dapr)
├── clusters/                     # Cluster configs (dev k3d, production)
└── scripts/                      # Utility scripts
```

### Key GitOps Patterns

1. **Kustomize Components**: All services use `components/common-deployment` and `components/common-service` as base templates, then patch with service-specific values
2. **Namespace Convention**: `{service}-dev` for dev, `{service}-prod` for production
3. **Image Registry**: `registry-api.tanhdev.com/<service>:<tag>`
4. **Config**: ConfigMaps in `base/configmap.yaml`, overlaid per environment
5. **Secrets**: External Secrets Operator → Vault (no secrets in git)
6. **Monitoring**: ServiceMonitor for Prometheus scraping per service
7. **App of Apps**: ArgoCD root app in `bootstrap/` deploys all service apps

### argocd/ Structure (Legacy — Helm-based)

```
argocd/
├── applications/
│   ├── main/                     # Main service Helm charts
│   │   ├── <service>/
│   │   │   ├── Chart.yaml
│   │   │   ├── values-base.yaml
│   │   │   ├── dev/values.yaml
│   │   │   └── templates/        # K8s manifests
│   └── notification/             # Separate namespace
├── argocd-projects/              # ArgoCD project definitions
├── infrastructure/               # Dapr components, alerts
├── resource-quotas/              # Resource quota definitions
└── scripts/                      # Deployment & security scripts
```

### Infrastructure Components (Managed in gitops/)

| Component | Type | Notes |
|-----------|------|-------|
| PostgreSQL | CloudNativePG | HA 3-node cluster |
| Redis | Redis Operator | 6-node HA (3 master + 3 slave) |
| Vault | HashiCorp Vault | HA 3-node Raft, auto-unseal |
| Dapr | Sidecar injection | PubSub (Redis Streams), State Store |
| Cert-Manager | TLS | Let's Encrypt auto-renewal |
| MinIO | Object Storage | File uploads (common-operations) |
| Consul | Service Discovery | gRPC service registration |
| Elasticsearch | Search | Search service indexing |

---

## Quick Decision Guide

### "Where does this business logic live?"
→ `<service>/internal/biz/` — Business logic layer with domain entities and use cases

### "How do two services communicate?"
→ **Synchronous**: gRPC clients in `internal/client/` (registered via Consul)
→ **Asynchronous**: Dapr PubSub events — publisher in `internal/events/`, consumer in `internal/data/eventbus/`

### "How do I deploy a change?"
→ Push code → GitLab CI builds image → Update image tag in `gitops/apps/<service>/overlays/<env>/deployment-patch.yaml` → ArgoCD syncs

### "Where is the K8s config for service X?"
→ **New way**: `gitops/apps/<service>/` (Kustomize)
→ **Old way**: `argocd/applications/main/<service>/` (Helm)

### "How do I add a new service?"
1. Create service code following standard structure
2. Add GitOps config: `gitops/apps/<new-service>/base/` + `overlays/`
3. Add ArgoCD Application: `gitops/environments/dev/apps/<new-service>.yaml`
4. Add CI pipeline: `<new-service>/.gitlab-ci.yml`

### "What shared utilities are available?"
→ Check `common/` library FIRST before writing custom code. See the `use-common-lib` skill.

### "Where are database schema changes?"
→ `<service>/migrations/*.sql` (Goose format, numbered sequentially)

---

## All Services Cloned ✅

All **23/23** services from SERVICE_INDEX.md are present in the local workspace.
