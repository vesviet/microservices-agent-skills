---
name: review-code
description: Review code changes following the project's coding standards, Clean Architecture principles, and best practices
---

# Code Review Skill

This is the **definitive code review skill** that consolidates ALL review criteria from:
- [Coding Standards](docs/07-development/standards/coding-standards.md) — Go style, proto, layers, errors, constants
- [Team Lead Code Review Guide](docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md) — Architecture, severity, P0/P1/P2
- [Development Review Checklist](docs/07-development/standards/development-review-checklist.md) — Pre-review, quality gates
- [Service Review & Release Prompt](docs/07-development/standards/service-review-release-prompt.md) — Full service release process

---

## Two Review Modes

| Mode | When | Trigger |
|------|------|---------|
| **Mode A: Quick Review** | Review specific code changes (files, PRs, recent edits) | "review this code", "review my changes" |
| **Mode B: Full Service Review & Release** | Review entire service for production readiness | "review service X", "review and release X", follows `service-review-release-prompt.md` |

---

# Mode A: Quick Code Review

## When to Use
- User explicitly asks for code review of specific changes
- After making significant changes to verify quality
- Before committing/pushing changes
- When reviewing pull/merge requests

## Review Process

### Step 1: Understand the Changes
1. Identify which files were changed
2. Understand the purpose of the changes
3. Determine which service(s) are affected

### Step 2: Apply Review Checklist

#### 🏗️ 1. Architecture & Clean Code (P0 if violated)

- [ ] **Layer boundaries**: `service` → `biz` → `data` (NEVER skip layers)
- [ ] **Biz MUST NOT call DB directly** (no `gorm.DB` in biz layer)
- [ ] **Service layer = thin adapter only** (parse request → call biz → return response)
- [ ] **Repository pattern**: Interfaces in `biz/`, implementations in `data/`
- [ ] **Constructor Injection (Wire DI)**: No global variables/state
- [ ] **Zero golangci-lint warnings**

#### 🔌 2. API & Contract

- [ ] **Proto naming**: RPCs use `Verb + Noun` (e.g. `CreateOrder`, `GetUser`)
- [ ] **Error mapping**: Business errors → gRPC codes (`NotFound`, `InvalidArgument`, etc.)
- [ ] **Input validation**: Comprehensive validation at Service layer
- [ ] **No breaking changes**: Proto field numbers preserved; use `reserved` for deleted fields
- [ ] **REST conventions**: `GET /api/v1/<service>/<resources>/{id}`

#### 🧠 3. Business Logic & Concurrency (P0 if violated)

- [ ] **Context propagation**: `context.Context` through ALL layers
- [ ] **NO unmanaged goroutines**: No raw `go func()`, use `errgroup` or Event Bus
- [ ] **Shared state protection**: `sync.Mutex` or `sync.Map` for mutable state
- [ ] **Idempotency**: Critical operations handle retries via Idempotency Keys
- [ ] **Error wrapping**: `fmt.Errorf("failed to create order: %w", err)`
- [ ] **Resource cleanup**: `defer` for closing DB connections, file handles, gRPC streams
- [ ] **Context timeout**: Long-running operations respect `ctx.Done()` and timeouts
- [ ] **Singleton init**: Use `sync.Once` for one-time initializations (clients, pools)

#### 💽 4. Data Layer & Persistence (P0 for missing transactions)

- [ ] **Atomic transactions**: Multi-write operations MUST use `db.Transaction()`
- [ ] **NO N+1 queries**: Use `Preload`/`Joins` for related data
- [ ] **Parameterized queries**: NEVER concatenate user input into SQL
- [ ] **Migrations**: Up/Down scripts required; NO `AutoMigrate` in production
- [ ] **DB isolation**: Implementation hidden behind interfaces
- [ ] **Pagination**: All list queries support pagination
- [ ] **Soft delete**: Use `deleted_at` where appropriate
- [ ] **Migration safety (zero-downtime)**: ↓ See §13 Migration Safety below

#### 🛡️ 5. Security (P0 for vulnerabilities)

- [ ] **Auth checks**: Every handler enforces Authentication & Authorization
- [ ] **No hardcoded secrets**: Load from ENV/Config
- [ ] **Sensitive data masked**: Passwords, tokens NOT in logs (use structured JSON)
- [ ] **Input sanitization**: No SQL injection, XSS prevention
- [ ] **Rate limiting**: Applied to public-facing endpoints

#### ⚡ 6. Performance & Resilience

- [ ] **Caching**: Cache-aside for read-heavy data
- [ ] **Connection pooling**: DB/Redis `MaxOpenConns` configured
- [ ] **Timeouts**: Configured for all external calls
- [ ] **Circuit breakers**: For inter-service calls
- [ ] **Retries**: With exponential backoff for transient failures

#### 👁️ 7. Observability

- [ ] **Structured logging**: JSON with `trace_id`, context propagated
- [ ] **Prometheus metrics**: RED metrics (Rate, Error, Duration)
- [ ] **OpenTelemetry spans**: For critical paths
- [ ] **Health probes**: `/health/live` and `/health/ready`
- [ ] **Correlation ID**: Passed through service calls

#### 🔔 8. Event-Driven Patterns

- [ ] **Idempotent handlers**: Event handlers handle duplicate delivery
- [ ] **Error handling**: Failed events don't crash the service
- [ ] **Event publishing**: Non-blocking, fire-and-forget with proper error logging
- [ ] **Outbox pattern**: Critical events use transactional outbox
- [ ] **DLQ**: Dead letter queue configured for consumers

#### 📝 9. Code Quality

- [ ] **No hardcoded values**: Use `internal/constants` or config
- [ ] **No TODO/FIXME without issue**: Track tech debt via `TODO(#issue_id)` with P0/P1/P2
- [ ] **DRY**: No duplicated code; use `common` library
- [ ] **Function length**: Under 50 lines (ideally)
- [ ] **Comments**: Explain "Why", not "What" for complex logic. Max 3 lines. DO NOT use P-0 or [ ] formats.
- [ ] **Naming**: Clear, descriptive, follows Go conventions
- [ ] **Generated files**: `wire_gen.go` and `*.pb.go` MUST NEVER be manually edited or reviewed line-by-line.
- [ ] **No bin files**: Ensure no `bin/` directories or binary files are checked in.

#### 🧪 10. Testing

- [ ] **Business logic coverage > 80%**
- [ ] **Table-driven tests** for multiple scenarios
- [ ] **Mock repositories**: Use interfaces for testing biz independently
- [ ] **Edge cases**: Error paths, empty inputs, boundary conditions

#### 📦 11. Versioning & CHANGELOG

- [ ] **CHANGELOG.md updated**: New entries under `[Unreleased]`
- [ ] **Version bump justified**: MAJOR/MINOR/PATCH matches scope
- [ ] **No breaking changes in PATCH/MINOR**
- [ ] **Proto `reserved` used**: Deleted fields use `reserved`
- [ ] **Common tagged**: If common changed, new tag created

#### 🔧 12. Common Library Usage

- [ ] **Use common middleware**: Don't reinvent auth, logging, CORS
- [ ] **Use common errors**: `common/errors.NewNotFound()`, etc.
- [ ] **Use common repository**: `common/repository.GormRepository[T]`
- [ ] **Use common events**: `common/events` for pub/sub
- [ ] **Use common constants**: `common/constants.TopicXxx` for event topics

#### 🌐 13. Cross-Service Impact (Tech Lead Focus)

**This is what separates a tech lead review from a developer review.**

##### 13.1 Proto/API Backward Compatibility (P0 if broken)
- [ ] **Proto field numbers preserved**: No reuse of deleted field numbers
- [ ] **New fields are optional**: Adding required fields to existing messages = MAJOR break
- [ ] **RPC signatures stable**: No rename/remove without versioning (`v1` → `v2`)
- [ ] **Consumers verified**: If service A changes proto, all clients (B, C...) still compile?

```bash
# Quick check: who imports this service's proto?
grep -r 'gitlab.com/ta-microservices/{serviceName}' --include='go.mod' */go.mod
```

##### 13.2 Event Schema Compatibility (P0 if broken)
- [ ] **Event struct changes are additive-only**: New fields OK, removing/renaming = breaking
- [ ] **Consumer handles old + new format**: If publisher adds fields, old consumers must not crash
- [ ] **Topic names immutable**: Never rename existing topics; create new topics instead
- [ ] **Tested with existing consumers**: Run consumer with old event payload to verify

```go
// ❌ BAD: Renamed field breaks existing consumers
type OrderEvent struct {
    OrderNumber string `json:"order_number"` // was "order_id" → consumers break
}

// ✅ GOOD: Add new field, keep old
type OrderEvent struct {
    OrderID     string `json:"order_id"`     // keep existing
    OrderNumber string `json:"order_number"` // new, optional
}
```

##### 13.3 Go Module Dependency Graph
- [ ] **No circular imports**: Service A imports B, B must NOT import A
- [ ] **Common stays base-only**: No domain interfaces/DTOs in `common`
- [ ] **Minimal import surface**: Don't import entire service module for one type; define local interface

#### 🔄 14. Migration Safety (Zero-Downtime Deploy)

##### Deploy Order Matters:
```
                    SAFE                          UNSAFE
   ┌──────────────────────────┐    ┌──────────────────────────┐
   │ 1. Deploy migration      │    │ 1. Deploy migration      │
   │    (add column nullable) │    │    (drop column)         │
   │ 2. Deploy code           │    │ 2. Deploy code           │
   │    (uses new column)     │    │    (old pods still read  │
   │ 3. Backfill data         │    │     that column → CRASH) │
   │ 4. Add NOT NULL (later)  │    │                          │
   └──────────────────────────┘    └──────────────────────────┘
```

- [ ] **Add column**: Must be `NULLABLE` or have `DEFAULT` → code deploy later
- [ ] **Remove column**: Code deploy first (stop reading) → migration later
- [ ] **Rename column**: NEVER in-place; add new → migrate data → remove old (3-step)
- [ ] **Add index**: Use `CONCURRENTLY` for large tables (no table lock)
- [ ] **Rollback tested**: Down migration reverses all changes cleanly
- [ ] **Data backfill**: Separate migration or cron, NOT in app startup

#### ⚙️ 15. Config & GitOps Alignment (P1)

- [ ] **Port allocation follows [PORT_ALLOCATION_STANDARD.md](gitops/docs/PORT_ALLOCATION_STANDARD.md)**: `config.yaml` addr ↔ `deployment.yaml` containerPort ↔ `service.yaml` targetPort ↔ `dapr.io/app-port` ↔ health probe ports
- [ ] **New env vars**: Code reads new env var → ConfigMap/Secret updated in `gitops/`?
- [ ] **Resource limits**: CPU/memory requests/limits reasonable for workload
- [ ] **Secrets**: New secrets added to both `sealed-secret.yaml` and code config
- [ ] **Feature flags**: New features behind config toggle for safe rollout?

```bash
# Quick check: config alignment
# 1. Find env vars used in code
grep -rn 'os.Getenv\|viper.Get\|envconfig' {serviceName}/internal/ --include='*.go'

# 2. Compare with gitops configmap
cat gitops/apps/{serviceName}/base/configmap.yaml
```

#### 🚀 16. Operational Readiness (P1)

- [ ] **Graceful shutdown**: Server drains in-flight requests on SIGTERM
- [ ] **Health probes correct**: Liveness (is process alive?) vs Readiness (can accept traffic?)
- [ ] **Startup probe**: For slow-starting services (DB migrations, cache warm-up)
- [ ] **Resource limits**: Set in deployment, appropriate for workload
- [ ] **HPA configured**: Auto-scaling rules for expected traffic patterns
- [ ] **PDB (PodDisruptionBudget)**: At least 1 pod available during rolling updates
- [ ] **Rollback plan**: Previous image tag known; `kubectl rollout undo` works
- [ ] **Monitoring alerts**: Key metrics have alerting rules (error rate, latency p99)

### Step 3: Output Review

```markdown
## 🔍 Code Review Summary

**Service**: <service name>
**Files Changed**: <count>
**Version Impact**: MAJOR / MINOR / PATCH / None
**CHANGELOG Updated**: Yes / No / N/A
**Overall Assessment**: ✅ Approved / ⚠️ Needs Changes / ❌ Critical Issues

### 🔴 P0 — Blocking (Must Fix)
Security, data inconsistency, SQL injection, missing transactions, unmanaged goroutines.
1. [file:line] Issue description

### 🟡 P1 — High (Should Fix)
Performance (N+1), missing observability, no timeouts/retries, missing validation.
1. [file:line] Issue description

### 🔵 P2 — Normal (Nice to Have)
Documentation, code style, low test coverage, naming.
1. [file:line] Issue description

### 🟢 Good Practices Observed
1. [Positive observation]

### 📋 Detailed Review

#### File: `path/to/file.go`
- Line XX: [Observation with severity]
- Line YY: [Suggestion with rationale]
```

---

# Mode B: Full Service Review & Release

> **This mode has been consolidated into the `review-service` skill** to avoid duplication. Use `review-service` for full service review and release processes.

## When to Use
- User says "review service X" or "review and release X"
- User references `service-review-release-prompt.md`
- Full service readiness assessment needed

**→ Follow the `review-service` skill in this pack for the complete 10-step service review process, including:**
1. Index & Review Codebase (using ALL Mode A criteria §1-§16 above)
2. Cross-Service Impact Analysis
3. Create Review Checklist
4. Action Plan & Bug Fixes
5. Test Coverage Check
6. Dependencies (Go Modules)
7. Lint & Build
8. Deployment Readiness (GitOps)
9. Documentation
10. Commit & Release

---

## Severity Reference (P0/P1/P2)

From [Team Lead Code Review Guide](docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md):

| Severity | Emoji | Category | Examples | Action |
|----------|-------|----------|----------|--------|
| **P0 (Blocking)** | 🔴 | Security, Data, Correctness | SQL injection, missing transactions, data inconsistency, no auth, unmanaged goroutines | **MUST fix** before merge/release |
| **P1 (High)** | 🟡 | Performance, Reliability | N+1 queries, missing observability, no timeouts/retries, no circuit breakers, missing validation | **Should fix** soon |
| **P2 (Normal)** | 🔵 | Quality, Maintenance | Documentation gaps, code style, low test coverage, naming inconsistencies, missing comments | **Nice to have** |

---

## Common Anti-Patterns to Watch For

### 1. God Service (P1)
```go
// ❌ BAD: Service layer doing business logic
func (s *OrderService) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderReply, error) {
    // 200 lines of business logic, DB queries, event publishing...
}

// ✅ GOOD: Delegate to use case
func (s *OrderService) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderReply, error) {
    order := &biz.Order{...} // Convert proto to domain
    result, err := s.uc.CreateOrder(ctx, order)
    return toProtoReply(result), err
}
```

### 2. Biz Calls DB Directly (P0)
```go
// ❌ BAD: Business layer importing gorm
func (uc *OrderUsecase) Get(ctx context.Context, id string) (*Order, error) {
    var order Order
    uc.db.Where("id = ?", id).First(&order)  // NEVER do this in biz
}

// ✅ GOOD: Use repository interface
func (uc *OrderUsecase) Get(ctx context.Context, id string) (*Order, error) {
    return uc.repo.FindByID(ctx, id)  // Repo interface defined in biz/
}
```

### 3. Leaking Data Models (P1)
```go
// ❌ BAD: Returning GORM model from biz layer
func (uc *OrderUsecase) Get(ctx context.Context, id string) (*data.OrderModel, error)

// ✅ GOOD: Using domain entity
func (uc *OrderUsecase) Get(ctx context.Context, id string) (*biz.Order, error)
```

### 4. Missing Error Context (P1)
```go
// ❌ BAD
return nil, err

// ✅ GOOD
return nil, fmt.Errorf("failed to create order for customer %s: %w", customerID, err)
```

### 5. Unmanaged Goroutines (P0)
```go
// ❌ BAD: Fire-and-forget goroutine
go func() {
    sendNotification(order)
}()

// ✅ GOOD: Use errgroup or event bus
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error {
    return sendNotification(ctx, order)
})
```

### 6. Raw SQL Concatenation (P0)
```go
// ❌ BAD: SQL injection vulnerability
db.Raw("SELECT * FROM users WHERE email = '" + email + "'")

// ✅ GOOD: Parameterized query
db.Where("email = ?", email).First(&user)
```

### 7. Unsafe Migration (P0)
```sql
-- ❌ BAD: Adding NOT NULL column without default (breaks existing rows)
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100) NOT NULL;

-- ✅ GOOD: Add nullable first, backfill later
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100);
-- Later migration: UPDATE orders SET tracking_number = '' WHERE tracking_number IS NULL;
-- Even later: ALTER TABLE orders ALTER COLUMN tracking_number SET NOT NULL;
```

### 8. Breaking Event Schema (P0)
```go
// ❌ BAD: Renamed field breaks all consumers
type OrderEvent struct {
    Number string `json:"number"` // was "order_id" → all consumers crash
}

// ✅ GOOD: Keep old field, add new field
type OrderEvent struct {
    OrderID string `json:"order_id"` // keep for backward compat
    Number  string `json:"number"`   // new field, consumers can adopt gradually
}
```

### 9. Config Drift (P1)
```go
// ❌ BAD: Code uses env var not in configmap
redisAddr := os.Getenv("REDIS_CLUSTER_ADDR") // not in gitops/apps/<svc>/base/configmap.yaml

// ✅ GOOD: All env vars traced to configmap/secret
// Code: os.Getenv("REDIS_ADDR")  →  configmap.yaml: REDIS_ADDR: redis:6379
```

### 10. Missing Resource Cleanup (P1)
```go
// ❌ BAD: gRPC connection never closed
conn, _ := grpc.Dial(target)
// ... use conn, never close

// ✅ GOOD: Defer cleanup
conn, err := grpc.Dial(target)
if err != nil {
    return err
}
defer conn.Close()
```

---

## Quality Gates

From [Development Review Checklist](docs/07-development/standards/development-review-checklist.md):

| Gate | Threshold |
|------|-----------|
| Code Coverage | ≥ 80% for business logic |
| Static Analysis | Zero critical issues (golangci-lint) |
| Security Scan | Zero high-severity vulnerabilities |
| Performance | No regression in key metrics |
| Documentation | All public APIs documented |

---

## Reference Documents

- [Coding Standards](docs/07-development/standards/coding-standards.md)
- [Team Lead Code Review Guide](docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)
- [Development Review Checklist](docs/07-development/standards/development-review-checklist.md)
- [Service Review & Release Prompt](docs/07-development/standards/service-review-release-prompt.md)
- [Common Package Usage](docs/07-development/standards/common-package-usage.md)
