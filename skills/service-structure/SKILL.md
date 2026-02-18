---
name: service-structure
description: Understand the dual-binary architecture - main service handles API/data, worker handles event consumers, cron jobs, and outbox processing
---

# Service Structure Skill

Use this skill to understand or implement the standard service architecture in this project.

## When to Use
- Creating a new microservice
- Adding a worker to an existing service
- Understanding where to put API vs background logic
- Adding cron jobs, event consumers, or outbox processors

---

## ⚠️ CRITICAL: Dual-Binary Architecture

Every service has **2 separate binaries** from the **same codebase**:

```
┌──────────────────────────────────────────────────────────────┐
│                   Same Docker Image / Same Codebase           │
│                                                               │
│  ┌─────────────────────────┐    ┌──────────────────────────┐ │
│  │   Main Service           │    │   Worker                  │ │
│  │   /app/bin/<service>     │    │   /app/bin/worker         │ │
│  │                          │    │                           │ │
│  │  • HTTP Server (80XX)    │    │  • Event Consumers ←──┐  │ │
│  │  • gRPC Server (90XX)    │    │  • Cron Jobs           │  │ │
│  │  • API Handlers          │    │  • Outbox Processor     │  │ │
│  │  • Data Layer            │    │                         │  │ │
│  │  • Domain Logic          │    │  Dapr port: 5005 (gRPC) │  │ │
│  │                          │    │                         │  │ │
│  │  📤 PUBLISH events ─────────→ Dapr PubSub (Redis) ─────┘  │ │
│  │  (during API calls)      │    │  📤 PUBLISH events too    │ │
│  │                          │    │  (via outbox processor)   │ │
│  └─────────────────────────┘    └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

📤 Publish: Both main + worker can publish events
📥 Consume: ONLY worker consumes events (Dapr PubSub subscribers)
```

| Aspect | Main Service (`cmd/<service>/`) | Worker (`cmd/worker/`) |
|--------|------|--------|
| **Purpose** | Serve API requests (REST + gRPC) | Background processing |
| **Entry point** | `cmd/<service>/main.go` | `cmd/worker/main.go` |
| **Wire DI** | `cmd/<service>/wire.go` | `cmd/worker/wire.go` |
| **K8s Deployment** | `deployment.yaml` | `worker-deployment.yaml` |
| **Ports** | HTTP `80XX` + gRPC `90XX` | Dapr gRPC `5005` |
| **Dapr app-id** | `<service>` | `<service>-worker` |
| **Framework** | Kratos (`kratos.New(...)`) | `common/worker` package |
| **Publish events** | ✅ Yes (via `biz/` layer during API calls) | ✅ Yes (via outbox processor) |
| **Consume events** | ❌ No | ✅ Yes (Dapr PubSub consumers) |
| **Cron jobs** | ❌ No | ✅ Yes |
| **Scales** | By API load | By event/job throughput |
| **Consul** | Registered for service discovery | Not registered |

---

## Directory Structure

```
<service>/
├── cmd/
│   ├── <service>/             # 🔵 MAIN SERVICE BINARY
│   │   ├── main.go            #    Kratos app startup
│   │   ├── wire.go            #    DI: server + service + data
│   │   └── wire_gen.go        #    Auto-generated
│   ├── worker/                # 🟠 WORKER BINARY
│   │   ├── main.go            #    Worker startup (signal handling, modes)
│   │   ├── wire.go            #    DI: data + biz + worker jobs
│   │   └── wire_gen.go        #    Auto-generated
│   └── migrate/               # 🟢 MIGRATION BINARY
│       └── main.go            #    Goose migrations
│
├── internal/
│   ├── biz/                   # 🔴 Domain logic (shared by main + worker)
│   ├── data/                  # 🟢 Data layer (shared by main + worker)
│   ├── service/               # 🔵 API handlers (main only)
│   ├── server/                # 🔵 HTTP/gRPC server configs (main only)
│   ├── client/                # gRPC clients to other services (shared)
│   ├── worker/                # 🟠 Worker-specific logic (worker only)
│   │   ├── cron/              #    Cron/scheduled jobs
│   │   ├── event/             #    Event consumers (Dapr PubSub)
│   │   └── outbox/            #    Transactional outbox processor
│   ├── events/                # Event publishing (shared)
│   ├── model/                 # GORM models (shared)
│   ├── repository/            # Repository interfaces (shared)
│   └── config/                # Config loading (shared)
│
├── configs/
│   └── config.yaml            # Shared config for both binaries
├── Dockerfile                 # Builds BOTH binaries
└── migrations/                # SQL migrations
```

**Key insight**: `biz/`, `data/`, `model/`, `client/` are **shared** between main and worker. Only `service/`, `server/` are main-only. Only `worker/` is worker-only.

---

## Main Service Binary (`cmd/<service>/main.go`)

The main service is a standard Kratos app serving HTTP + gRPC:

```go
package main

import (
	"github.com/go-kratos/kratos/v2"
	"github.com/go-kratos/kratos/v2/transport/grpc"
	"github.com/go-kratos/kratos/v2/transport/http"
	"github.com/go-kratos/kratos/v2/registry"
)

var Name string = "<service>"

func newApp(logger log.Logger, gs *grpc.Server, hs *http.Server, rr registry.Registrar) *kratos.App {
	return kratos.New(
		kratos.ID(id),
		kratos.Name(Name),
		kratos.Server(gs, hs),        // HTTP + gRPC servers
		kratos.Registrar(rr),          // Consul registration
	)
}

func main() {
	// Load config → Wire DI → app.Run()
	cfg, err := config.Init(configPath, "<SERVICE_PREFIX>")
	app, cleanup, err := wireApp(cfg, logger)
	defer cleanup()
	app.App.Run()
}
```

**Wire DI** (`cmd/<service>/wire.go`):
```go
func wireApp(*config.AppConfig, log.Logger) (*App, func(), error) {
	panic(wire.Build(
		server.ProviderSet,     // HTTP + gRPC servers
		data.ProviderSet,       // DB, Redis, repositories
		service.ProviderSet,    // API service handlers
		// biz use cases...
		newApp,
	))
}
```

---

## Worker Binary (`cmd/worker/main.go`)

The worker uses `common/worker` package, NOT Kratos:

```go
package main

import (
	"gitlab.com/ta-microservices/common/worker"
	"gitlab.com/ta-microservices/<service>/internal/config"
)

var (
	Name       string = "<service>-worker"
	workerMode string  // "cron" | "event" | "all"
)

func init() {
	flag.StringVar(&workerMode, "mode", "all", "Worker mode: cron|event|all")
}

func main() {
	// Load config (same config as main service)
	cfg, err := config.Init(configPath, "<SERVICE_PREFIX>")

	// Wire DI for workers
	workers, cleanup, err := wireWorkers(cfg, logger)
	defer cleanup()

	// Registry manages lifecycle
	registry := worker.NewContinuousWorkerRegistry(logger)

	// Filter workers by mode
	for _, w := range workers {
		if shouldRunWorker(w, workerMode) {
			registry.Register(w.Name(), w.GetBaseWorker())
		}
	}

	// Start all, wait for signal, stop all
	ctx, cancel := context.WithCancel(context.Background())
	registry.StartAll(ctx, workerMap)

	<-sigCh  // Wait for SIGINT/SIGTERM
	registry.StopAll()
	cancel()
}

// shouldRunWorker filters by mode
func shouldRunWorker(w worker.ContinuousWorker, mode string) bool {
	if mode == "all" { return true }
	isEvent := strings.Contains(w.Name(), "event") || strings.Contains(w.Name(), "consumer")
	if mode == "event" { return isEvent }
	if mode == "cron" { return !isEvent }
	return false
}
```

**Wire DI** (`cmd/worker/wire.go`):
```go
func wireWorkers(c *config.AppConfig, logger log.Logger) ([]commonWorker.ContinuousWorker, func(), error) {
	panic(wire.Build(
		data.ProviderSet,       // Same data layer as main
		// biz use cases needed by workers...
		cron.ProviderSet,       // Cron job providers
		event.ProviderSet,      // Event consumer providers
		outbox.ProviderSet,     // Outbox processor providers
		newWorkers,             // Collect into []ContinuousWorker
	))
}

func newWorkers(
	reservationCleanup *cron.ReservationCleanupJob,
	codAutoConfirm *cron.CODAutoConfirmJob,
	eventConsumers *event.EventConsumersWorker,
	outboxWorker *outbox.OutboxWorker,
) []commonWorker.ContinuousWorker {
	return []commonWorker.ContinuousWorker{
		reservationCleanup,
		codAutoConfirm,
		eventConsumers,
		outboxWorker,
	}
}
```

---

## Worker Types

### 1. Cron Jobs (`internal/worker/cron/`)

Periodic tasks using `time.Ticker`:

```go
package cron

import (
	"gitlab.com/ta-microservices/common/worker"
)

type ReservationCleanupJob struct {
	*worker.BaseContinuousWorker
	orderRepo  repoOrder.OrderRepo    // Uses same repos as main service
}

func NewReservationCleanupJob(
	orderRepo repoOrder.OrderRepo,
	logger log.Logger,
) *ReservationCleanupJob {
	return &ReservationCleanupJob{
		BaseContinuousWorker: worker.NewBaseContinuousWorker(worker.WorkerConfig{
			Name: "reservation-cleanup-job",
		}, logger),
		orderRepo: orderRepo,
	}
}

func (j *ReservationCleanupJob) Start(ctx context.Context) error {
	j.Log().Info("Starting reservation cleanup (interval: 15m)")
	j.cleanup(ctx)  // Run immediately on start

	ticker := time.NewTicker(15 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			j.cleanup(ctx)
		case <-ctx.Done():
			return nil
		case <-j.StopChan():
			return nil
		}
	}
}

func (j *ReservationCleanupJob) Stop(ctx context.Context) error {
	return j.BaseContinuousWorker.Stop(ctx)
}

func (j *ReservationCleanupJob) HealthCheck(ctx context.Context) error {
	return nil
}

func (j *ReservationCleanupJob) cleanup(ctx context.Context) {
	// Actual business logic using repos
}
```

**Wire provider** (`internal/worker/cron/wire.go`):
```go
package cron

import "github.com/google/wire"

var ProviderSet = wire.NewSet(
	NewReservationCleanupJob,
	NewCODAutoConfirmJob,
	// ... more cron jobs
)
```

### 2. Event Consumers (`internal/worker/event/`)

Dapr PubSub event listeners:

```go
package event

type EventConsumersWorker struct {
	*worker.BaseContinuousWorker
	eventbusClient      eventbus.Client
	paymentConsumer     eventbus.PaymentConsumer
	fulfillmentConsumer eventbus.FulfillmentConsumer
}

func (w *EventConsumersWorker) Start(ctx context.Context) error {
	// Register all topic subscriptions
	w.paymentConsumer.ConsumePaymentConfirmed(ctx)
	w.paymentConsumer.ConsumePaymentFailed(ctx)
	w.fulfillmentConsumer.ConsumeFulfillmentStatusChanged(ctx)

	// Start eventbus gRPC server on port 5005 (Dapr sidecar connects here)
	w.eventbusClient.Start()  // Blocks until stopped
	return nil
}
```

### 3. Outbox Processor (`internal/worker/outbox/`)

Transactional outbox pattern - polls DB for unsent events and publishes:

```go
package outbox

type OutboxWorker struct {
	*worker.BaseContinuousWorker
	outboxRepo OutboxRepo
	publisher  events.EventPublisher
}

func (w *OutboxWorker) Start(ctx context.Context) error {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			w.processOutbox(ctx)
		case <-ctx.Done():
			return nil
		case <-w.StopChan():
			return nil
		}
	}
}
```

---

## ContinuousWorker Interface

All workers implement `common/worker.ContinuousWorker`:

```go
type ContinuousWorker interface {
	Name() string
	Start(ctx context.Context) error       // Blocks until stopped
	Stop(ctx context.Context) error        // Graceful shutdown
	HealthCheck(ctx context.Context) error
	GetBaseWorker() *BaseContinuousWorker
}
```

Embed `*worker.BaseContinuousWorker` for default implementations.

---

## Dockerfile: Single Image, Multiple Binaries

```dockerfile
# Build ALL binaries in the same image
RUN go build -o ./bin/<service> ./cmd/<service>    # Main API binary
RUN go build -o ./bin/migrate ./cmd/migrate         # Migration binary
RUN go build -o ./bin/worker ./cmd/worker            # Worker binary

# Final image contains all binaries
COPY --from=builder /src/bin /app/bin
# /app/bin/<service>  → main service
# /app/bin/worker     → worker
# /app/bin/migrate    → migrations
```

---

## K8s Deployments: Separate Pods, Same Image

**Main deployment** (`gitops/apps/<service>/base/deployment.yaml`):
```yaml
metadata:
  name: <service>-service
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "<service>"
    dapr.io/app-port: "80XX"           # HTTP port
    dapr.io/app-protocol: "http"
spec:
  containers:
  - name: <service>-service
    image: registry-api.tanhdev.com/<service>:placeholder
    command: ["/app/bin/<service>", "-conf", "/app/configs"]
    ports:
    - containerPort: 80XX   # HTTP
    - containerPort: 90XX   # gRPC
```

**Worker deployment** (`gitops/apps/<service>/base/worker-deployment.yaml`):
```yaml
metadata:
  name: <service>-worker
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "<service>-worker"
    dapr.io/app-port: "5005"           # Dapr gRPC port
    dapr.io/app-protocol: "grpc"
spec:
  containers:
  - name: <service>-worker
    image: registry-api.tanhdev.com/<service>:placeholder  # ← Same image!
    command: ["/bin/sh", "-c"]
    args:
      - |
        ulimit -n 65536 || true
        exec /app/bin/worker -conf /app/configs/config.yaml
    ports:
    - containerPort: 5005   # Dapr gRPC
```

**Key**: Both use the **same Docker image** (same `newTag` in kustomization), just different `command`.

---

## Services with Workers

| Service | Has Worker | Worker Types |
|---------|-----------|--------------|
| Order | ✅ | Cron (cleanup, COD confirm, capture retry), Event (payment, fulfillment), Outbox |
| Payment | ✅ | Cron (settlement, webhook retry), Event (order events) |
| Catalog | ✅ | Event (price sync, inventory sync) |
| Warehouse | ✅ | Cron (stock reconciliation), Event (order events) |
| Fulfillment | ✅ | Event (order events, shipping events) |
| Shipping | ✅ | Event (fulfillment events) |
| Notification | ✅ | Event (multi-service notification triggers) |
| Customer | ✅ | Event (order/auth events) |
| Search | ✅ | Sync (Elasticsearch indexing), DLQ worker |
| Pricing | ✅ | Event (catalog events) |
| Common-ops | ✅ | Event (cross-service operations) |
| Auth | ✅ | Cron (token cleanup) |

---

## Adding a New Worker

### Step 1: Create Worker Implementation

**File**: `<service>/internal/worker/cron/my_job.go` (or `event/`, `outbox/`)

```go
package cron

type MyJob struct {
	*worker.BaseContinuousWorker
	myRepo biz.MyRepo
}

func NewMyJob(myRepo biz.MyRepo, logger log.Logger) *MyJob {
	return &MyJob{
		BaseContinuousWorker: worker.NewBaseContinuousWorker(worker.WorkerConfig{
			Name: "my-job",
		}, logger),
		myRepo: myRepo,
	}
}

func (j *MyJob) Start(ctx context.Context) error { /* ... */ }
func (j *MyJob) Stop(ctx context.Context) error { return j.BaseContinuousWorker.Stop(ctx) }
func (j *MyJob) HealthCheck(ctx context.Context) error { return nil }
```

### Step 2: Add to Wire Provider

**File**: `<service>/internal/worker/cron/wire.go`
```go
var ProviderSet = wire.NewSet(
	// ... existing
	NewMyJob,   // ← Add
)
```

### Step 3: Add to `newWorkers()` Collector

**File**: `<service>/cmd/worker/wire.go`
```go
func newWorkers(
	// ... existing
	myJob *cron.MyJob,   // ← Add parameter
) []commonWorker.ContinuousWorker {
	workers = append(workers, myJob)  // ← Add
	return workers
}
```

### Step 4: Regenerate Wire

```bash
cd /home/user/microservices/<service>/cmd/worker && wire
```

### Step 5: Build & Test

```bash
cd /home/user/microservices/<service> && go build ./...
```

## Checklist

- [ ] Worker implements `common/worker.ContinuousWorker` interface
- [ ] Embeds `*worker.BaseContinuousWorker`
- [ ] `Start()` blocks with proper `select` on `ctx.Done()` and `j.StopChan()`
- [ ] `Stop()` delegates to `BaseContinuousWorker.Stop()`
- [ ] `HealthCheck()` implemented
- [ ] Added to Wire ProviderSet (`internal/worker/<type>/wire.go`)
- [ ] Added to `newWorkers()` in `cmd/worker/wire.go`
- [ ] Wire regenerated (`wire` command)
- [ ] Build passes (`go build ./...`)
- [ ] Worker name follows convention: descriptive, lowercase with hyphens
