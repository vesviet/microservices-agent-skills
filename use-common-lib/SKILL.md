---
name: use-common-lib
description: Reference guide for the shared common library - know what's available before writing custom code to avoid duplication
---

# Use Common Library Skill

**ALWAYS check this before writing utility code.** The `common` module (`gitlab.com/ta-microservices/common`) provides shared packages used across all microservices. Using them ensures consistency and avoids code duplication.

## When to Use
- Before implementing any utility, helper, or shared functionality
- When adding error handling, validation, middleware, or data access patterns
- When setting up event publishing/consuming, gRPC clients, or observability
- When you see repeated patterns across services

---

## ⚠️ CRITICAL: Check Common First

Before writing **any** of the following, check if `common` already provides it:
- Error types and constructors
- Validation logic
- Repository patterns (CRUD, pagination, filtering)
- Middleware (auth, CORS, rate limiting, logging, recovery)
- Event publishing/consuming
- Config loading
- gRPC client helpers
- Observability (metrics, tracing, health checks)
- Security (passwords, PII, file sanitization)
- Worker patterns

---

## Quick Reference: "I need to..." → Use This

| I need to... | Use this from `common` |
|---|---|
| Create/return errors | `common/errors` — `NewNotFound()`, `NewBadRequest()`, `NewConflict()` |
| Handle CRUD operations | `common/repository.GormRepository[T]` — generic GORM repo |
| Add pagination | `common/repository.Filter` + `common/utils/pagination` |
| Validate input | `common/validation.Validator` — struct validation with rules |
| Validate JWT tokens | `common/validation.ValidateJWT()` |
| Auth middleware | `common/middleware.AuthKratos()` or `Auth()` (Gin) |
| CORS middleware | `common/middleware.CORS()` |
| Rate limiting | `common/middleware.RateLimit()` |
| Request logging | `common/middleware.Logging()` |
| Panic recovery | `common/middleware.Recovery()` |
| Publish events | `common/events.NewDaprEventPublisher()` |
| Consume events | `common/events.NewConsumerClientWithLogger()` |
| Event helper | `common/events.NewEventHelper()` — CRUD event publishing |
| Load config | `common/config.Init(path, prefix)` |
| Hash passwords | `common/security.HashPassword()`, `CheckPassword()` |
| Sanitize filenames | `common/security.SanitizeFilename()` |
| PII masking | `common/security/pii.MaskEmail()`, `MaskPhone()` |
| Health checks | `common/observability/health` |
| Metrics | `common/observability/metrics` |
| Tracing | `common/observability/tracing` |
| Worker patterns | `common/worker.BaseContinuousWorker`, `ContinuousWorkerRegistry` |
| gRPC client base | `common/client/grpc_client.go` — connection pooling, retries |
| Circuit breaker | `common/client/circuitbreaker` |
| Base model fields | `common/models.BaseModel` — ID, CreatedAt, UpdatedAt, DeletedAt |
| API responses | `common/models.NewAPIError()`, `NewAPIResponse()` |
| Idempotency | `common/idempotency` |
| Context helpers | `common/middleware.GetUserID()`, `GetUserRole()`, `GetUserEmail()` |
| Correlation ID | `common/utils/ctx.ExtractCorrelationID()` |
| Topic constants | `common/constants.TopicXxx` — all event topic names |

---

## Package Details

### `common/errors` — Error Handling

**Import**: `gitlab.com/ta-microservices/common/errors`

Provides domain-rich error types with HTTP status code mapping:

```go
import cerrors "gitlab.com/ta-microservices/common/errors"

// Constructors
cerrors.NewNotFound("order", orderID)           // 404
cerrors.NewBadRequest("invalid field", "email")  // 400
cerrors.NewConflict("order", orderID)            // 409
cerrors.NewUnauthorized("invalid token")         // 401
cerrors.NewForbidden("insufficient permissions") // 403
cerrors.NewInternal("database error")            // 500

// Classification
cerrors.IsNotFound(err)     // Check error type
cerrors.IsBadRequest(err)
cerrors.IsConflict(err)

// HTTP response helpers
cerrors.ToHTTPResponse(err) // Returns structured error response
```

**Key files**: `constructors.go`, `classifier.go`, `response.go`, `types.go`

### `common/repository` — Base Repository (GORM)

**Import**: `gitlab.com/ta-microservices/common/repository`

Generic GORM repository with CRUD, pagination, filtering, transactions:

```go
import repo "gitlab.com/ta-microservices/common/repository"

// Create repository for any GORM model
type OrderRepository struct {
    *repo.GormRepository[model.Order]
}

func NewOrderRepository(db *gorm.DB, logger log.Logger) *OrderRepository {
    r := repo.NewGormRepository[model.Order](db, logger)
    r.SetSearchFields([]string{"order_number", "customer_name"})
    return &OrderRepository{GormRepository: r}
}

// Built-in methods (no need to implement):
r.FindByID(ctx, id)
r.Create(ctx, entity)
r.Update(ctx, entity, params)
r.Save(ctx, entity)
r.DeleteByID(ctx, id)
r.List(ctx, filter)      // With pagination and filtering
r.Count(ctx, filter)
r.Exists(ctx, id)
r.CreateBatch(ctx, entities)
r.WithTx(tx)              // Transaction support
r.GetDB(ctx)              // Raw DB access

// Filtering & Pagination
filter := &repo.Filter{
    Page:     1,
    PageSize: 20,
    Sort:     "created_at",
    Order:    "desc",
    Search:   "keyword",
    Conditions: []repo.Condition{
        {Field: "status", Operator: "=", Value: "active"},
        {Field: "amount", Operator: ">=", Value: 100},
    },
    Preloads: []string{"Items", "Customer"},
}
orders, pagination, err := r.List(ctx, filter)
```

### `common/validation` — Input Validation

**Import**: `gitlab.com/ta-microservices/common/validation`

Struct-based validation with custom rules:

```go
import "gitlab.com/ta-microservices/common/validation"

// Validate struct
type CreateOrderRequest struct {
    CustomerID string `validate:"required,uuid"`
    Email      string `validate:"required,email"`
    Amount     float64 `validate:"required,gt=0"`
}

err := validation.ValidateStruct(req)

// Business rule validation
validation.ValidateBusinessRules(...)

// JWT validation
claims, err := validation.ValidateJWT(token, secret)
```

### `common/middleware` — HTTP/gRPC Middleware

**Import**: `gitlab.com/ta-microservices/common/middleware`

```go
import mw "gitlab.com/ta-microservices/common/middleware"

// Kratos middleware (for gRPC/HTTP servers)
authMiddleware := mw.AuthKratos(&mw.AuthConfig{
    JWTSecret: cfg.Auth.JWTSecret,
    SkipPaths: []string{"/health", "/api/v1/public"},
})

// Gin middleware (for HTTP only)
router.Use(mw.Auth(&mw.AuthConfig{...}))
router.Use(mw.RequireRole("admin", "manager"))
router.Use(mw.OptionalAuth(&mw.AuthConfig{...}))
router.Use(mw.CORS())
router.Use(mw.RateLimit(config))
router.Use(mw.Logging(logger))
router.Use(mw.Recovery(logger))

// Context helpers
userID, ok := mw.GetUserID(c)
role, ok := mw.GetUserRole(c)
email, ok := mw.GetUserEmail(c)
```

### `common/events` — Event Publishing/Consuming

**Import**: `gitlab.com/ta-microservices/common/events`

```go
import "gitlab.com/ta-microservices/common/events"

// Publisher (gRPC-based, connects to Dapr sidecar)
publisher, err := events.NewDaprEventPublisher(config, logger)
publisher.PublishEvent(ctx, "topic.name", eventData)

// No-op publisher for testing or disabled events
publisher := events.NewNoOpEventPublisher(logger)

// Event Helper (CRUD convenience methods)
helper := events.NewEventHelper(publisher, "order-service", logger)
helper.PublishCreated(ctx, "order", orderID, data)
helper.PublishUpdated(ctx, "order", orderID, changes)
helper.PublishDeleted(ctx, "order", orderID)
helper.PublishCustom(ctx, "my.custom.event", data)

// Consumer
consumer, err := events.NewConsumerClientWithLogger(logger)
consumer.AddConsumerWithMetadata(topic, pubsub, metadata, handler)
consumer.Start()  // Blocks

// Handler function type
type ConsumeFn func(ctx context.Context, e Message) error
type Message struct { Data []byte }
```

### `common/config` — Configuration Loading

**Import**: `gitlab.com/ta-microservices/common/config`

Viper-based config with env var override:

```go
import "gitlab.com/ta-microservices/common/config"

// Load config (Viper reads YAML + env vars with prefix)
cfg, err := config.Init("configs/config.yaml", "ORDER")
// Environment variables: ORDER_SERVER_HTTP_PORT, ORDER_DATA_DATABASE_DSN, etc.
```

### `common/models` — Base Models

**Import**: `gitlab.com/ta-microservices/common/models`

```go
import "gitlab.com/ta-microservices/common/models"

// Base model with standard fields
type Order struct {
    models.BaseModel                    // ID, CreatedAt, UpdatedAt, DeletedAt
    OrderNumber string `gorm:"uniqueIndex"`
}

// API response helpers
models.NewAPIError(code, message, detail)
models.NewAPIResponse(data, message)
```

### `common/worker` — Background Worker Patterns

**Import**: `gitlab.com/ta-microservices/common/worker`

```go
import "gitlab.com/ta-microservices/common/worker"

// ContinuousWorker interface
type ContinuousWorker interface {
    Name() string
    Start(ctx context.Context) error
    Stop(ctx context.Context) error
    HealthCheck(ctx context.Context) error
    GetBaseWorker() *BaseContinuousWorker
}

// Base implementation (embed in your worker)
base := worker.NewBaseContinuousWorker(worker.WorkerConfig{
    Name: "my-worker",
}, logger)

// Registry for managing multiple workers
registry := worker.NewContinuousWorkerRegistry(logger)
registry.Register("my-worker", base)
registry.StartAll(ctx, workersMap)
registry.StopAll()
```

### `common/security` — Security Utilities

**Import**: `gitlab.com/ta-microservices/common/security`

```go
import "gitlab.com/ta-microservices/common/security"

// Password hashing (bcrypt)
hash, err := security.HashPassword("plaintext")
ok := security.CheckPassword("plaintext", hash)

// File sanitization
safeName := security.SanitizeFilename(userInput)

// PII masking
import "gitlab.com/ta-microservices/common/security/pii"
masked := pii.MaskEmail("user@example.com")  // u***@example.com
masked := pii.MaskPhone("+84123456789")       // +84***456789
```

### `common/constants` — Shared Constants

**Import**: `gitlab.com/ta-microservices/common/constants`

```go
import "gitlab.com/ta-microservices/common/constants"

// Event topics (single source of truth)
constants.TopicOrderStatusChanged     // "orders.order.status_changed"
constants.TopicPaymentConfirmed       // "payments.payment.confirmed"
constants.TopicFulfillmentStatusChanged // "fulfillments.fulfillment.status_changed"
// ... see common/constants/events.go for full list

// Dapr
constants.DaprDefaultPubSub  // "pubsub"
```

---

## Anti-Patterns (DON'T Do This)

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Write custom pagination logic | Use `common/repository.Filter` + `GormRepository.List()` |
| Create error types per service | Use `common/errors.NewNotFound()`, etc. |
| Write JWT validation from scratch | Use `common/validation.ValidateJWT()` or `common/middleware.AuthKratos()` |
| Implement event publishing manually | Use `common/events.NewDaprEventPublisher()` |
| Define topic strings inline | Use `common/constants.TopicXxx` |
| Write CORS middleware | Use `common/middleware.CORS()` |
| Hash passwords manually | Use `common/security.HashPassword()` |
| Write base model fields per service | Embed `common/models.BaseModel` |

---

## Checklist

- [ ] Searched `common/` for existing functionality before writing custom code
- [ ] Used `common/errors` for error types (not custom error structs)
- [ ] Used `common/repository.GormRepository` for data access (not raw GORM in every method)
- [ ] Used `common/constants` for event topics (not inline strings)
- [ ] Used `common/events` for pub/sub (not raw Dapr SDK calls)
- [ ] Used `common/middleware` for auth/CORS/rate limiting (not custom implementations)
- [ ] Used `common/validation` for input validation (not ad-hoc checks)
