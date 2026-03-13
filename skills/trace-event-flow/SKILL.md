---
name: trace-event-flow
description: Trace event-driven communication flows between microservices using Dapr PubSub
---

# Trace Event Flow Skill

Use this skill to understand, debug, or implement event-driven communication between services.

## When to Use
- Debugging why an event is not being received
- Understanding the flow of a business process across services
- Adding new event publishing or subscribing
- Tracing data flow across service boundaries
- Investigating eventual consistency issues

## Event Architecture Overview

```
┌─────────────┐     Dapr PubSub      ┌─────────────┐
│  Publisher   │ ──── (Redis) ────→   │  Subscriber  │
│  Service     │                      │  Service     │
└─────────────┘                      └─────────────┘
```

- **Message Broker**: Dapr PubSub backed by **Redis Streams**
- **Event Library**: `common/events/` contains shared event definitions
- **Pattern**: Publish/Subscribe with topic-based routing
- **Serialization**: JSON

## Key Event Flows in the Platform

### 1. Order Creation Flow
```
Checkout → order.created → Order Service
Order Service → order.confirmed → Warehouse (reserve stock)
Order Service → order.confirmed → Payment (process payment)
Order Service → order.confirmed → Notification (send confirmation)
Order Service → order.confirmed → Analytics (track order)
```

### 2. Payment Flow
```
Payment Service → payment.completed → Order Service (update status)
Payment Service → payment.failed → Order Service (cancel/retry)
Payment Service → payment.refunded → Order Service (handle refund)
```

### 3. Fulfillment Flow
```
Order Service → order.paid → Fulfillment (start picking)
Fulfillment → fulfillment.completed → Shipping (create shipment)
Shipping → shipping.shipped → Order Service (update status)
Shipping → shipping.delivered → Order Service (mark delivered)
```

### 4. Catalog/Search Sync
```
Catalog → product.created → Search (index product)
Catalog → product.updated → Search (reindex product)
Catalog → product.deleted → Search (remove from index)
Catalog → product.updated → Pricing (recalculate prices)
```

### 5. Customer Events
```
Auth → user.registered → Customer (create profile)
Customer → customer.updated → Notification (welcome email)
Customer → customer.segment_changed → Pricing (pricing rules)
```

### 6. Inventory Events
```
Warehouse → stock.low → Notification (alert admins)
Warehouse → stock.reserved → Order Service (confirm availability)
Warehouse → stock.released → Order Service (release hold)
```

### 7. Pricing → Search Sync
```
Pricing → pricing.price.updated → Search Worker (update ES price)
Pricing → pricing.price.deleted → Search Worker (remove ES price)
  ↳ If product not in ES → fetch from Catalog gRPC → index → apply price
  ↳ On price update → set has_price=true (product visible in search)
  ↳ On price delete → check remaining prices → if none → has_price=false (hidden)
```

### 8. Checkout Flow
```
Checkout → checkout.completed → Order Service (create order from cart)
Checkout uses gRPC to: Pricing (calculate), Promotion (apply), Shipping (rates)
```

### 9. Return/Refund Flow
```
Order Service → order.return_requested → Return (initiate return)
Return → return.approved → Warehouse (restock items)
Return → return.approved → Payment (issue refund)
Return → return.completed → Order Service (update order status)
Return → return.completed → Notification (notify customer)
```

### 10. Loyalty/Rewards Flow
```
Order → order.completed → Loyalty (award points)
Payment → payment.refunded → Loyalty (deduct points)
Customer → customer.registered → Loyalty (create rewards account)
Loyalty → rewards.tier_changed → Notification (notify tier upgrade)
```

> **GOTCHA**: Pricing uses the **outbox pattern** (`worker/outbox.go`). Events are
> written to an outbox table in the same DB transaction, then a worker polls and
> publishes via Dapr. This guarantees at-least-once delivery.

## How to Trace an Event

### Step 1: Identify the Event Topic
Search for the event name in the common events library:
```bash
grep -r "<event_name>" common/events/
```

### Step 2: Find the Publisher
Search for where the event is published:
```bash
# Search for Publish calls
grep -rn "Publish" <service>/internal/ --include="*.go" | grep -i "<topic>"

# Search for event topic constant
grep -rn "<TOPIC_NAME>" <service>/internal/ --include="*.go"
```

### Step 3: Find the Subscriber
Search for where the event is consumed:
```bash
# Search for Subscribe/Handler
grep -rn "Subscribe\|HandleEvent\|OnEvent" <service>/internal/ --include="*.go" | grep -i "<topic>"

# Check Dapr subscription config
find <service> -name "*.yaml" -exec grep -l "<topic>" {} \;
```

### Step 4: Check Event Structure
Look at the event payload definition:
```bash
# In common events library
cat common/events/<domain>_events.go

# Or in the service itself
grep -rn "type.*Event struct" <service>/internal/ --include="*.go"
```

### Step 5: Check Dapr Configuration
```bash
# Dapr PubSub component (local)
cat dapr/components/pubsub.yaml

# Dapr subscription config (K8s)
find gitops/apps/<service> -name "*dapr*" -o -name "*subscription*"
```

## How to Add a New Event

### Step 1: Define Event in Common Library

**File**: `common/events/<domain>_events.go`

```go
package events

const (
	TopicExampleCreated = "example.created"
	TopicExampleUpdated = "example.updated"
)

type ExampleCreatedEvent struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Timestamp time.Time `json:"timestamp"`
}
```

### Step 2: Publish Event from Source Service

In the business logic (`internal/biz/`):
```go
func (uc *ExampleUsecase) Create(ctx context.Context, example *Example) (*Example, error) {
	result, err := uc.repo.Create(ctx, example)
	if err != nil {
		return nil, err
	}

	// Publish event
	event := &events.ExampleCreatedEvent{
		ID:        result.ID,
		Name:      result.Name,
		Timestamp: time.Now(),
	}
	if err := uc.eventPublisher.Publish(ctx, events.TopicExampleCreated, event); err != nil {
		uc.log.Warnf("failed to publish event: %v", err)
		// Don't fail the operation for event publishing failure
	}

	return result, nil
}
```

### Step 3: Subscribe in Consumer Service

Create an event handler:
```go
func (h *ExampleEventHandler) HandleExampleCreated(ctx context.Context, event *events.ExampleCreatedEvent) error {
	h.log.Infof("received example.created event: %s", event.ID)
	// Process the event
	return nil
}
```

Register the subscription in the server setup or worker.

### Step 4: Configure Dapr Subscription

For K8s deployment, ensure Dapr subscription is configured:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Subscription
metadata:
  name: example-created-sub
spec:
  topic: example.created
  route: /api/v1/events/example-created
  pubsubname: pubsub
```

## Debugging Event Issues

### Event Not Being Published
```bash
# Check for errors in publisher service logs
$DEV_SSH "kubectl logs -n <service>-dev -l app=<service>-service --tail=200 | grep -i 'publish\|event\|dapr'"

# Check Dapr sidecar logs
$DEV_SSH "kubectl logs -n <service>-dev -l app=<service>-service -c daprd --tail=100"
```

### Event Not Being Received
```bash
# Check subscriber service logs
$DEV_SSH "kubectl logs -n <subscriber-service>-dev -l app=<subscriber-service>-service --tail=200 | grep -i 'subscribe\|event\|handler'"

# Check Dapr subscription config
$DEV_SSH "kubectl get subscription -n <service>-dev"

# Check Redis streams directly
$DEV_SSH "kubectl exec -n redis redis-0 -- redis-cli XLEN <topic>"
```

### Event Processing Failed
```bash
# Look for DLQ (Dead Letter Queue) entries
grep -rn "DLQ\|dead.letter\|retry" <service>/internal/ --include="*.go"
```

## Event Best Practices

1. **Idempotent handlers** - Events may be delivered more than once
2. **Include correlation ID** - For distributed tracing
3. **Don't fail operations on publish failure** - Log and continue (eventual consistency)
4. **Use outbox pattern** for critical events - Ensures event is published even if service crashes
5. **Version your events** - Include version field for backward compatibility
6. **Keep events small** - Include IDs, not full objects. Let consumers fetch details if needed.

## Known Gotchas

### 1. Dapr PubSub Component Namespace
The `pubsub-redis` Dapr component MUST exist in **every namespace** that has Dapr-enabled pods.
If a service can't subscribe to topics, check:
```bash
kubectl get component pubsub-redis -n <service>-dev
```
If missing, create the component in that namespace (copy from `common-operations-dev`).

### 2. Elasticsearch Issues (Search Service Events)
For ES-related event processing failures (`document_parsing_exception`, `document_missing_exception`, index naming, Go map dotted keys), see the **`troubleshoot-service`** skill — it contains the complete ES debugging reference with commands and solutions.

---

## Checklist

### Event Tracing
- [ ] Event topic identified
- [ ] Publisher found
- [ ] Subscriber found
- [ ] Event structure understood

### Debugging
- [ ] Publisher logs checked
- [ ] Subscriber logs checked
- [ ] Dapr configuration verified
- [ ] Event flow tested

### Implementation
- [ ] Event defined in common
- [ ] Publisher implemented
- [ ] Subscriber implemented
- [ ] Dapr subscription configured

---

## Quick Reference Checklist

Use this for rapid event flow tracing:

### Trace Flow
- [ ] Identify event topic
- [ ] Find publisher
- [ ] Find subscriber
- [ ] Check event structure

### Debug Issues
- [ ] Check logs
- [ ] Verify Dapr config
- [ ] Test event flow

---

## Related Skills

- **add-event-handler**: Add new event publishers/consumers
- **troubleshoot-service**: Debug event processing issues
- **debug-k8s**: Debug Dapr deployment issues
- **use-common-lib**: Use common event utilities
- **review-code**: Review event handler implementation
