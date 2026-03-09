---
name: add-cron-job
description: Add a new cron/scheduled job to a microservice worker following the project's common worker patterns
---

# Add Cron Job Skill

Use this skill when adding a new periodic/scheduled background job to any microservice's worker binary.

## When to Use
- Adding scheduled cleanup tasks (expired reservations, stale records)
- Adding periodic reconciliation jobs (stock drift, balance checks)
- Adding monitoring/alerting cron tasks (low stock, capacity)
- Adding report generation jobs (daily summaries, weekly reports)

---

## ⚠️ CRITICAL RULES

1. **Cron jobs run in the Worker binary** (`cmd/worker/`), NEVER in the main service
2. **Embed `*worker.BaseContinuousWorker`** from `common/worker` package
3. **Use `time.Ticker` or `robfig/cron`** for scheduling, NOT raw goroutines
4. **Always respect `ctx.Done()` and `StopChan()`** for graceful shutdown
5. **Use bounded queries** (LIMIT) to prevent OOM on large datasets
6. **Log start/end/duration** of each job run for observability
7. **Never fail silently** — log errors but don't crash the worker

---

## Architecture

```
cmd/worker/main.go
    ↓ Wire DI
cmd/worker/wire.go → newWorkers() collects all ContinuousWorker
    ↓
internal/worker/cron/<job_name>.go    ← YOUR NEW JOB
    ↓ uses
internal/biz/<entity>/usecase.go      ← Business logic (shared with main)
    ↓ uses
internal/data/<entity>.go             ← Repository (shared with main)
```

---

## Step-by-Step Process

### Step 1: Create the Job Implementation

**File**: `<service>/internal/worker/cron/<job_name>.go`

```go
package cron

import (
	"context"
	"time"

	"github.com/go-kratos/kratos/v2/log"
	commonWorker "gitlab.com/ta-microservices/common/worker"

	"gitlab.com/ta-microservices/<service>/internal/biz/<entity>"
)

// MyCleanupJob periodically cleans up stale records.
type MyCleanupJob struct {
	*commonWorker.BaseContinuousWorker
	entityUsecase *entity.UseCase
	log           *log.Helper
}

func NewMyCleanupJob(
	entityUsecase *entity.UseCase,
	logger log.Logger,
) *MyCleanupJob {
	return &MyCleanupJob{
		BaseContinuousWorker: commonWorker.NewBaseContinuousWorker(commonWorker.WorkerConfig{
			Name: "my-cleanup-job",
		}, logger),
		entityUsecase: entityUsecase,
		log:           log.NewHelper(logger),
	}
}

func (j *MyCleanupJob) Start(ctx context.Context) error {
	j.log.WithContext(ctx).Info("Starting my-cleanup-job (interval: 15m)")

	// Run immediately on startup
	j.execute(ctx)

	ticker := time.NewTicker(15 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			j.execute(ctx)
		case <-ctx.Done():
			j.log.Info("my-cleanup-job stopped (context cancelled)")
			return nil
		case <-j.StopChan():
			j.log.Info("my-cleanup-job stopped (stop signal)")
			return nil
		}
	}
}

func (j *MyCleanupJob) Stop(ctx context.Context) error {
	return j.BaseContinuousWorker.Stop(ctx)
}

func (j *MyCleanupJob) HealthCheck(_ context.Context) error {
	return nil
}

func (j *MyCleanupJob) execute(ctx context.Context) {
	startTime := time.Now()
	j.log.WithContext(ctx).Info("Running cleanup pass...")

	// Use bounded query to prevent OOM
	count, err := j.entityUsecase.CleanupStaleRecords(ctx, 500)
	if err != nil {
		j.log.WithContext(ctx).Errorf("Cleanup failed: %v", err)
		return
	}

	duration := time.Since(startTime)
	j.log.WithContext(ctx).Infof("Cleanup completed in %v: %d records processed", duration, count)
}
```

### Alternative: Using `robfig/cron` for Complex Schedules

```go
import "github.com/robfig/cron/v3"

func (j *MyJob) Start(ctx context.Context) error {
	c := cron.New(cron.WithSeconds())

	// Run every day at 2:00 AM
	_, err := c.AddFunc("0 0 2 * * *", func() {
		j.execute(ctx)
	})
	if err != nil {
		return fmt.Errorf("failed to schedule job: %w", err)
	}

	c.Start()
	<-ctx.Done()
	c.Stop()
	return nil
}
```

### Step 2: Add to Wire Provider

**File**: `<service>/internal/worker/cron/provider.go`

```go
package cron

import "github.com/google/wire"

var ProviderSet = wire.NewSet(
	// ... existing jobs
	NewMyCleanupJob,   // ← Add
)
```

### Step 3: Add to `newWorkers()` Collector

**File**: `<service>/cmd/worker/wire.go`

```go
func newWorkers(
	// ... existing workers
	myCleanupJob *cron.MyCleanupJob,   // ← Add parameter
) []commonWorker.ContinuousWorker {
	return []commonWorker.ContinuousWorker{
		// ... existing
		myCleanupJob,   // ← Add
	}
}
```

### Step 4: Regenerate Wire

```bash
cd <service>/cmd/worker && wire
```

### Step 5: Build & Verify

```bash
cd <service> && go build ./...
```

---

## Scheduling Reference

| Use Case | Interval | Pattern |
|----------|----------|---------|
| Cleanup stale sessions | Every 15 min | `time.Ticker(15 * time.Minute)` |
| Stock reconciliation | Every 1 hour | `time.Ticker(1 * time.Hour)` |
| Daily report generation | Daily 2 AM | `cron: "0 0 2 * * *"` |
| Capacity monitoring | Every 5 min | `time.Ticker(5 * time.Minute)` |
| Weekly summary | Sunday midnight | `cron: "0 0 0 * * 0"` |

---

## Checklist

- [ ] Job implements `common/worker.ContinuousWorker` interface
- [ ] Embeds `*worker.BaseContinuousWorker`
- [ ] `Start()` blocks with proper `select` on `ctx.Done()` and `StopChan()`
- [ ] `Stop()` delegates to `BaseContinuousWorker.Stop()`
- [ ] `HealthCheck()` implemented
- [ ] Uses bounded queries (LIMIT) to prevent OOM
- [ ] Logs start/end/duration of each run
- [ ] Error handling: logs but doesn't crash
- [ ] Added to Wire ProviderSet (`internal/worker/cron/provider.go`)
- [ ] Added to `newWorkers()` in `cmd/worker/wire.go`
- [ ] Wire regenerated (`wire` command)
- [ ] Build passes (`go build ./...`)
- [ ] **CHANGELOG.md updated**

---

## Related Skills

- **service-structure**: Understand dual-binary architecture
- **add-event-handler**: Add event consumers (different from cron)
- **commit-code**: Commit worker changes
- **write-tests**: Test cron job logic
- **use-common-lib**: Use common worker utilities
