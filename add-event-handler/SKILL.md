---
name: add-event-handler
description: Add a new event publisher or consumer to enable event-driven communication between microservices using Dapr PubSub
---

# Add Event Handler Skill

Use this skill when adding new event publishing or consuming capabilities to a microservice.

## When to Use
- Publishing a new event type from a service (biz layer or outbox)
- Consuming events from another service in a worker
- Adding new Dapr PubSub topic subscriptions
- Implementing saga/compensation patterns via events

---

## ⚠️ CRITICAL RULES

1. **Topics MUST be defined in `common/constants/events.go`** — single source of truth
2. **Publishers live in `internal/events/`** — used by biz layer during API calls
3. **Consumers live in `internal/data/eventbus/`** — used by worker only
4. **Consumer registration happens in `internal/worker/event/`** — worker binary only
5. **Main service publishes, Worker consumes** — NEVER consume in main service
6. **Event structs use JSON tags** — `json:"field_name"`
7. **Always add DLQ** (dead letter queue) — `deadLetterTopic: "<topic>.dlq"`

---

## Architecture Overview

```
┌─ Service A (Publisher) ──────────────────────────────────────┐
│                                                               │
│  API Request → biz layer → eventPublisher.PublishXxx()        │
│                    ↓                                          │
│  internal/events/publisher.go → common/events.PublishEvent()  │
│                    ↓                                          │
│  Dapr Sidecar → Redis Streams (PubSub)                        │
│                    ↓                                          │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌─ Service B (Consumer) ───────────────────────────────────────┐
│                                                               │
│  Worker Binary (cmd/worker/)                                  │
│       ↓                                                       │
│  internal/worker/event/event_worker.go                        │
│       → registers consumer.ConsumeXxx(ctx)                    │
│       ↓                                                       │
│  internal/data/eventbus/<source>_consumer.go                  │
│       → AddConsumerWithMetadata(topic, pubsub, handler)       │
│       → HandleXxx(ctx, message) → decode → business logic     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Part A: Adding a New Publisher

### Step 1: Define Topic in Common Constants

**File**: `common/constants/events.go`

```go
const (
    // Existing topics...
    
    // New topic
    TopicMyNewEvent = "myservice.entity.action"  // Convention: <service>.<entity>.<action>
)

// Also add event type constant
const (
    EventTypeMyNewEvent = "myservice.entity.action"
)
```

**Topic naming convention**: `<domain>.<entity>.<action>`
- `orders.order.status_changed`
- `payments.payment.confirmed`
- `fulfillments.fulfillment.status_changed`
- `shipping.shipment.created`

### Step 2: Define Event Struct

**File**: `<service>/internal/events/<entity>_events.go`

```go
package events

import "time"

// MyNewEvent represents <description>
type MyNewEvent struct {
    EventType   string                 `json:"event_type"`
    EntityID    string                 `json:"entity_id"`
    // Add domain-specific fields...
    Status      string                 `json:"status"`
    Timestamp   time.Time              `json:"timestamp"`
    Metadata    map[string]interface{} `json:"metadata,omitempty"`
}
```

### Step 3: Add Publish Method to EventPublisher Interface

**File**: `<service>/internal/events/publisher.go`

```go
// EventPublisher interface - add new method
type EventPublisher interface {
    PublishEvent(ctx context.Context, topic string, event interface{}) error
    // ... existing methods
    PublishMyNewEvent(ctx context.Context, event *MyNewEvent) error  // ← Add
    IsNoOp() bool
}

// Implement on the concrete publisher
func (p *ServiceEventPublisher) PublishMyNewEvent(ctx context.Context, event *MyNewEvent) error {
    if event == nil {
        return nil
    }
    event.EventType = constants.EventTypeMyNewEvent
    return p.PublishEvent(ctx, constants.TopicMyNewEvent, event)
}
```

### Step 4: Re-export Topic in Local Constants (Optional)

**File**: `<service>/internal/constants/constants.go`

```go
import commonConstants "gitlab.com/ta-microservices/common/constants"

const (
    TopicMyNewEvent = commonConstants.TopicMyNewEvent
)
```

### Step 5: Call from Biz Layer

**File**: `<service>/internal/biz/<entity>/usecase.go`

```go
type UseCase struct {
    eventPublisher events.EventPublisher
    // ...
}

func (uc *UseCase) DoSomething(ctx context.Context) error {
    // ... business logic ...
    
    // Publish event (fire-and-forget, don't fail the operation)
    if uc.eventPublisher != nil {
        event := &events.MyNewEvent{
            EntityID:  entity.ID,
            Status:    entity.Status,
            Timestamp: time.Now(),
        }
        if err := uc.eventPublisher.PublishMyNewEvent(ctx, event); err != nil {
            uc.log.Warnf("Failed to publish event: %v", err)
            // Don't return error - event publishing should not fail the operation
        }
    }
    
    return nil
}
```

### Step 6: Update Mock EventPublisher for Tests

**File**: `<service>/internal/biz/mocks.go`

```go
func (m *MockEventPublisher) PublishMyNewEvent(ctx context.Context, event *events.MyNewEvent) error {
    if m.Error != nil {
        return m.Error
    }
    m.Events = append(m.Events, event)
    return nil
}
```

---

## Part B: Adding a New Consumer

### Step 1: Ensure Topic Exists in Common Constants

Same as Publisher Step 1. The topic must already exist in `common/constants/events.go`.

### Step 2: Create Consumer Struct

**File**: `<service>/internal/data/eventbus/<source>_consumer.go`

```go
package eventbus

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"

    "github.com/go-kratos/kratos/v2/log"
    commonEvents "gitlab.com/ta-microservices/common/events"
    "<service>/internal/biz/<entity>"
    "<service>/internal/config"
    "<service>/internal/constants"
)

// SourceEvent represents the incoming event structure
type SourceEvent struct {
    EventType string    `json:"event_type"`
    EntityID  string    `json:"entity_id"`
    Status    string    `json:"status"`
    Timestamp time.Time `json:"timestamp"`
    // ... match the publisher's event struct
}

// SourceConsumer consumes events from <source> service
type SourceConsumer struct {
    Client                          // embeds commonEvents.ConsumerClient
    config    *config.AppConfig
    entityUc  *entity.UseCase       // biz layer use case
    log       *log.Helper
}

func NewSourceConsumer(
    client Client,
    cfg *config.AppConfig,
    entityUc *entity.UseCase,
    logger log.Logger,
) SourceConsumer {
    return SourceConsumer{
        Client:   client,
        config:   cfg,
        entityUc: entityUc,
        log:      log.NewHelper(logger),
    }
}
```

### Step 3: Add Subscribe + Handler Methods

```go
// ConsumeXxx registers the subscription for the topic
func (c SourceConsumer) ConsumeXxx(ctx context.Context) error {
    if c.config == nil {
        return fmt.Errorf("config is nil, cannot register consumer")
    }
    if c.config.Data.Eventbus.DefaultPubsub == "" {
        return fmt.Errorf("eventbus config is empty, cannot register consumer")
    }

    topic := constants.TopicMyNewEvent
    pubsub := c.config.Data.Eventbus.DefaultPubsub
    c.log.WithContext(ctx).Infof("Subscribing to topic: %s, pubsub: %s", topic, pubsub)

    return c.Client.AddConsumerWithMetadata(
        topic,
        pubsub,
        map[string]string{
            "deadLetterTopic": fmt.Sprintf("%s.dlq", topic),
        },
        c.HandleXxx,
    )
}

// HandleXxx processes the event
func (c SourceConsumer) HandleXxx(ctx context.Context, e commonEvents.Message) error {
    // 1. Decode event
    var eventData SourceEvent
    if err := json.NewDecoder(bytes.NewReader(e.Data)).Decode(&eventData); err != nil {
        c.log.WithContext(ctx).Errorf("Failed to decode event: %v, payload: %s", err, string(e.Data))
        return fmt.Errorf("failed to decode event: %w", err)
    }

    c.log.WithContext(ctx).Infof("Processing event: entity_id=%s", eventData.EntityID)

    // 2. Process business logic
    if err := c.processXxx(ctx, &eventData); err != nil {
        c.log.WithContext(ctx).Errorf("Failed to process event: %v", err)
        return fmt.Errorf("failed to process event: %w", err)  // Returning error triggers retry
    }

    c.log.WithContext(ctx).Infof("Successfully processed event: entity_id=%s", eventData.EntityID)
    return nil  // Returning nil = ACK the message
}

// processXxx contains the actual business logic
func (c SourceConsumer) processXxx(ctx context.Context, event *SourceEvent) error {
    // Call biz layer use case
    // e.g., c.entityUc.UpdateStatus(ctx, event.EntityID, event.Status)
    return nil
}
```

### Step 4: Add to Wire Provider

**File**: `<service>/internal/data/eventbus/provider.go`

```go
package eventbus

import "github.com/google/wire"

var ProviderSet = wire.NewSet(
    // ... existing consumers
    NewSourceConsumer,   // ← Add
)
```

### Step 5: Register in Event Worker

**File**: `<service>/internal/worker/event/event_worker.go`

```go
type EventConsumersWorker struct {
    *worker.BaseContinuousWorker
    eventbusClient      Client
    // ... existing consumers
    sourceConsumer      eventbus.SourceConsumer   // ← Add
}

func NewEventConsumersWorker(
    client Client,
    // ... existing
    sourceConsumer eventbus.SourceConsumer,   // ← Add parameter
    logger log.Logger,
) *EventConsumersWorker {
    return &EventConsumersWorker{
        // ... existing
        sourceConsumer: sourceConsumer,
    }
}

func (w *EventConsumersWorker) Start(ctx context.Context) error {
    // ... existing registrations
    
    // Register new consumer
    if err := w.sourceConsumer.ConsumeXxx(ctx); err != nil {
        return fmt.Errorf("failed to register source consumer: %w", err)
    }
    
    // ... start eventbus client
}
```

### Step 6: Update Worker Wire

**File**: `<service>/cmd/worker/wire.go`

Ensure the dependent provider sets include `eventbus.ProviderSet` so the new consumer is injected.

### Step 7: Regenerate Wire

```bash
cd /home/user/microservices/<service>/cmd/worker && wire
```

---

## Client Type (Important)

The eventbus Client is an alias for `common/events.ConsumerClient`:

**File**: `<service>/internal/data/eventbus/client.go`
```go
package eventbus

import commonEvents "gitlab.com/ta-microservices/common/events"

// Client is alias for ConsumerClient from common/events
type Client = commonEvents.ConsumerClient
```

This provides:
- `AddConsumer(topic, pubsub string, fn ConsumeFn) error`
- `AddConsumerWithMetadata(topic, pubsub string, metadata map[string]string, fn ConsumeFn) error`
- `Start() error`

---

## Event Schema Standard

All events should follow this schema:

```go
type StandardEvent struct {
    EventType string                 `json:"event_type"`   // Required: matches topic
    // Entity-specific ID field(s)
    EntityID  string                 `json:"entity_id"`    // Required
    // Business fields...
    Timestamp time.Time              `json:"timestamp"`    // Required
    Metadata  map[string]interface{} `json:"metadata,omitempty"` // Optional
}
```

---

## Error Handling in Consumers

```go
func (c Consumer) Handle(ctx context.Context, e commonEvents.Message) error {
    // Return error → Dapr will RETRY (exponential backoff)
    // Return nil   → Message is ACK'd (consumed successfully)
    
    // For decode errors: return error (retry may fix transient issues)
    // For business logic errors: return error (will retry)
    // For permanent errors: log and return nil (skip message, prevent infinite retry)
    
    if isPermanentError(err) {
        c.log.Errorf("Permanent error, skipping message: %v", err)
        return nil  // ACK to prevent infinite retry
    }
    return err  // Retry
}
```

---

## Outbox Pattern (Alternative to Direct Publishing)

For guaranteed delivery, use the outbox pattern instead of direct publishing:

```go
// In biz layer: write event to outbox table (same transaction as business data)
outboxEvent := &biz.OutboxEvent{
    Topic:   constants.TopicMyNewEvent,
    Payload: map[string]interface{}{
        "event_type": constants.EventTypeMyNewEvent,
        "entity_id":  entity.ID,
        "status":     entity.Status,
        "timestamp":  time.Now().Unix(),
    },
}
outboxRepo.Save(ctx, outboxEvent)

// The outbox worker (internal/worker/outbox/) will pick up and publish
```

---

## Checklist

### Publisher
- [ ] Topic defined in `common/constants/events.go`
- [ ] Event struct defined in `internal/events/<entity>_events.go`
- [ ] `PublishXxx` method added to `EventPublisher` interface
- [ ] Concrete implementation added to publisher
- [ ] Called from biz layer (fire-and-forget, don't fail the operation)
- [ ] Mock updated in `internal/biz/mocks.go`
- [ ] Tests updated
- [ ] **CHANGELOG.md updated** (new topic/publisher = MINOR version bump)

### Consumer
- [ ] Topic exists in `common/constants/events.go`
- [ ] Consumer struct in `internal/data/eventbus/<source>_consumer.go`
- [ ] `ConsumeXxx()` registers subscription with DLQ
- [ ] `HandleXxx()` decodes and processes event
- [ ] Added to `eventbus/provider.go` Wire ProviderSet
- [ ] Registered in `internal/worker/event/event_worker.go`
- [ ] Wire regenerated (`cd cmd/worker && wire`)
- [ ] Build passes (`go build ./...`)
- [ ] Error handling: retry vs skip for permanent errors
- [ ] **CHANGELOG.md updated** (new consumer = MINOR version bump)
- [ ] **If topic constant added to `common`**: tag common with new version (`v1.x.y`)
