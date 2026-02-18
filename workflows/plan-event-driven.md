---
description: Event-driven architecture changes - optimized for async patterns
---

# Plan Event Driven Workflow

Use this workflow for **adding or modifying event-driven communication** between microservices using Dapr PubSub.

## When to Use

- Adding event publishers
- Adding event consumers
- Designing event flows between services
- Debugging event delivery issues
- Refactoring synchronous calls to async events
- Implementing saga patterns

## Approach

**Optimization**: Async patterns and event flow design
- Clear event naming and schemas
- Consider ordering guarantees
- Plan for idempotency
- Handle failures gracefully

## Steps

1. **Understand the event flow**
   - What triggers the event?
   - What data needs to be in the event?
   - Which services need to consume it?
   - Use `trace-event-flow` skill for existing flows

2. **Design the event schema**
   - Define event name (clear, descriptive)
   - Define event payload structure
   - Consider versioning strategy
   - Include correlation ID for tracing

3. **Publisher side**
   - Use `add-event-handler` skill for publisher
   - Decide: Direct publish vs Outbox pattern
   - Implement in business logic layer
   - Handle publishing failures

   **Outbox Pattern** (recommended for reliability):
   - Write event to `outbox` table in same transaction
   - Worker processes outbox and publishes to Dapr
   - Guarantees at-least-once delivery

4. **Consumer side**
   - Use `add-event-handler` skill for consumer
   - Implement consumer in worker binary (not main service)
   - Make consumer idempotent (can process same event multiple times)
   - Handle errors and retries

5. **Configure Dapr subscription**
   - Define subscription in `configs/dapr/subscriptions.yaml`
   - Set topic name
   - Configure route or handler
   - Consider dead letter queue for failures

6. **Handle ordering and consistency**
   - Events are typically unordered
   - If order matters, design accordingly (partition keys, sequence numbers)
   - Use saga pattern for distributed transactions
   - Plan for eventual consistency

7. **Error handling**
   - Consumer errors trigger retries
   - Set max retries and backoff
   - Use dead letter topic for failed events
   - Log errors with correlation IDs

8. **Testing**
   - Unit test event handlers
   - Integration test event publishing
   - Test consumer idempotency
   - Test failure scenarios

9. **Monitoring**
   - Log event publishing and consumption
   - Monitor event delivery latency
   - Track dead letter queue
   - Use correlation IDs for tracing

## Event Patterns

### Simple Notification
- Lightweight events (IDs only)
- Consumers fetch details if needed
- Low coupling

### Event Carried State Transfer
- Events contain full data
- Consumers don't need to call back
- Higher coupling but more performant

### Saga Pattern
- Coordinate multi-service transactions
- Each service publishes success/failure events
- Compensating transactions for rollbacks

## Service Structure

**Publisher** (main service):
```
internal/biz/usecase.go
  └── Publish event directly OR write to outbox table
```

**Consumer** (worker binary):
```
cmd/worker/main.go
  └── Initialize event consumers
internal/consumer/
  └── event_handler.go  # Consumer implementation
configs/dapr/
  └── subscriptions.yaml  # Dapr subscription config
```

**Outbox Processing** (worker binary):
```
internal/outbox/
  └── processor.go  # Reads outbox table and publishes
```

## Skills to Use

- `add-event-handler` - Primary skill for publishers and consumers
- `trace-event-flow` - To understand existing event flows
- `service-structure` - Understand worker vs main service
- `service-map` - Identify which services publish/consume

## Tips

- Events are for notification, not commands
- Make consumers idempotent - events may be delivered multiple times
- Include correlation IDs for tracing across services
- Use outbox pattern for reliability in critical flows
- Consider event versioning from the start
- Don't use events for real-time synchronous workflows
- Monitor dead letter queues - they indicate problems
- Test failure scenarios thoroughly
