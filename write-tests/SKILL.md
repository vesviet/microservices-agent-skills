---
name: write-tests
description: Write unit and integration tests following the project's testing patterns - testify, table-driven tests, manual mocks in biz/mocks.go
---

# Write Tests Skill

Use this skill when writing or updating tests for microservice code.

## When to Use
- Adding new business logic that needs unit tests
- Adding new API endpoints
- Writing integration tests
- Updating existing tests after refactoring
- Creating mocks for dependencies

---

## ⚠️ CRITICAL RULES

1. **Use `testify`** — `assert` and `require` packages, NOT raw `if` checks
2. **Table-driven tests** — Use `tests := []struct{}` pattern for multiple cases
3. **Manual mocks in `internal/biz/mocks.go`** — NOT generated mocks (mockgen/mockery)
4. **Test biz layer primarily** — This is where business logic lives
5. **Test in same package** — Test files in the same package as the code being tested
6. **Use `_test.go` suffix** — Standard Go convention

---

## Test File Locations

```
<service>/
├── internal/
│   ├── biz/
│   │   ├── mocks.go                      # 🔴 All mocks defined here
│   │   ├── order/
│   │   │   ├── usecase.go
│   │   │   ├── create.go
│   │   │   ├── order_test.go             # 🟢 Unit tests for order use case
│   │   │   ├── create_test.go            # 🟢 Unit tests for create logic
│   │   │   └── mocks_test.go             # 🟢 Test-specific mocks (testify)
│   │   └── cancellation/
│   │       ├── cancellation.go
│   │       └── cancellation_test.go      # 🟢 Unit tests
│   ├── data/
│   │   └── eventbus/
│   │       └── fulfillment_consumer_test.go  # Consumer handler tests
│   └── security/
│       └── input_sanitizer_test.go
├── test/
│   └── integration/
│       └── checkout_flow_test.go         # 🔵 Integration tests
```

---

## Unit Test Pattern

### Basic Test Structure

```go
package order

import (
    "context"
    "testing"
    "time"

    "github.com/google/uuid"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    
    "gitlab.com/ta-microservices/order/internal/model"
)

func TestCreateOrder_Success(t *testing.T) {
    // Arrange
    ctx := context.Background()
    mockRepo := new(MockOrderRepository)   // testify mock
    
    req := &CreateOrderRequest{
        CustomerID: uuid.New().String(),
        Items: []*CreateOrderItemRequest{
            {ProductID: "prod-1", Quantity: 2},
        },
    }
    
    // Setup mock expectations
    mockRepo.On("FindByCartSessionID", ctx, mock.Anything).
        Return(nil, nil).Once()
    mockRepo.On("Create", ctx, mock.Anything).
        Return(nil).Once()
    
    // Act
    result, err := createOrder(ctx, mockRepo, req)
    
    // Assert
    require.NoError(t, err)       // require = fail immediately if error
    assert.NotNil(t, result)      // assert = continue on failure
    assert.Equal(t, "pending", result.Status)
    assert.Equal(t, req.CustomerID, result.CustomerID)
    
    mockRepo.AssertExpectations(t)
}
```

### Table-Driven Tests

```go
func TestCreateOrder_ValidationErrors(t *testing.T) {
    tests := []struct {
        name    string
        req     *CreateOrderRequest
        wantErr bool
        errMsg  string
    }{
        {
            name: "empty customer ID",
            req: &CreateOrderRequest{
                CustomerID: "",
                Items:      []*CreateOrderItemRequest{{ProductID: "p1", Quantity: 1}},
            },
            wantErr: true,
            errMsg:  "customer_id",
        },
        {
            name: "empty items",
            req: &CreateOrderRequest{
                CustomerID: uuid.New().String(),
                Items:      []*CreateOrderItemRequest{},
            },
            wantErr: true,
            errMsg:  "items",
        },
        {
            name: "zero quantity",
            req: &CreateOrderRequest{
                CustomerID: uuid.New().String(),
                Items:      []*CreateOrderItemRequest{{ProductID: "p1", Quantity: 0}},
            },
            wantErr: true,
            errMsg:  "quantity",
        },
        {
            name: "valid request",
            req: &CreateOrderRequest{
                CustomerID: uuid.New().String(),
                Items:      []*CreateOrderItemRequest{{ProductID: "p1", Quantity: 1}},
            },
            wantErr: false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validateCreateOrderRequest(tt.req)

            if tt.wantErr {
                assert.Error(t, err)
                assert.Contains(t, err.Error(), tt.errMsg)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### Testing Database Errors

```go
func TestGetOrder_DatabaseError(t *testing.T) {
    mockRepo := new(MockOrderRepository)
    ctx := context.Background()

    dbErr := errors.New("database connection failed")
    mockRepo.On("FindByID", ctx, "order-123").
        Return(nil, dbErr).Once()

    result, err := mockRepo.FindByID(ctx, "order-123")

    assert.Error(t, err)
    assert.Nil(t, result)
    assert.Contains(t, err.Error(), "database")
    mockRepo.AssertExpectations(t)
}
```

---

## Mock Patterns

### Manual Mocks in `biz/mocks.go` (Project Standard)

The project uses **manual mocks** defined in `internal/biz/mocks.go`. These implement the biz layer interfaces directly:

```go
// In internal/biz/mocks.go
package biz

// MockOrderRepo implements OrderRepo
type MockOrderRepo struct {
    Orders map[string]*Order
    Error  error
    // Function callbacks for flexible testing
    FindByIDFunc func(ctx context.Context, id string) (*model.Order, error)
}

func NewMockOrderRepo() *MockOrderRepo {
    return &MockOrderRepo{
        Orders: make(map[string]*Order),
    }
}

func (m *MockOrderRepo) FindByID(ctx context.Context, id string) (*model.Order, error) {
    if m.FindByIDFunc != nil {
        return m.FindByIDFunc(ctx, id)
    }
    if m.Error != nil {
        return nil, m.Error
    }
    // ... default implementation
}
```

Key patterns:
- **`Error` field**: Set to simulate errors for all methods
- **`XxxFunc` callback**: Override specific methods for specific tests
- **In-memory storage**: `map[string]*Entity` for stateful mocks

### Testify Mocks in `*_test.go` (For Simpler Cases)

For simpler mock needs within test files, use testify mock:

```go
// In internal/biz/order/mocks_test.go
package order

import (
    "context"
    "github.com/stretchr/testify/mock"
    "gitlab.com/ta-microservices/order/internal/model"
)

type MockOrderRepository struct {
    mock.Mock
}

func (m *MockOrderRepository) FindByID(ctx context.Context, id string) (*model.Order, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*model.Order), args.Error(1)
}

func (m *MockOrderRepository) FindByCartSessionID(ctx context.Context, sessionID string) (*model.Order, error) {
    args := m.Called(ctx, sessionID)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*model.Order), args.Error(1)
}
```

### MockEventPublisher

```go
// In internal/biz/mocks.go
type MockEventPublisher struct {
    Events []interface{}
    Error  error
}

func NewMockEventPublisher() *MockEventPublisher {
    return &MockEventPublisher{Events: make([]interface{}, 0)}
}

func (m *MockEventPublisher) PublishOrderStatusChanged(ctx context.Context, event *events.OrderStatusChangedEvent) error {
    if m.Error != nil { return m.Error }
    m.Events = append(m.Events, event)
    return nil
}

func (m *MockEventPublisher) PublishEvent(ctx context.Context, topic string, event interface{}) error {
    if m.Error != nil { return m.Error }
    m.Events = append(m.Events, event)
    return nil
}

func (m *MockEventPublisher) IsNoOp() bool { return false }
```

---

## What to Test

### Biz Layer (Primary Focus)

| Test Type | What | Example |
|-----------|------|---------|
| **Happy path** | Successful operation | `TestCreateOrder_Success` |
| **Validation** | Input validation rules | `TestCreateOrder_ValidationErrors` |
| **Idempotency** | Duplicate request handling | `TestCreateOrder_Idempotency` |
| **Error handling** | DB errors, service errors | `TestCreateOrder_DatabaseError` |
| **State transitions** | Status change rules | `TestUpdateStatus_InvalidTransition` |
| **Edge cases** | Zero quantity, nil pointers | `TestCalculateTotal_EmptyItems` |
| **Business rules** | Domain-specific logic | `TestCancellation_AlreadyShipped` |

### Consumer Handlers

```go
func TestHandlePaymentConfirmed(t *testing.T) {
    // Test event deserialization and business logic
    eventData := PaymentConfirmedEvent{
        PaymentID: "pay-123",
        OrderID:   "order-456",
        Amount:    99.99,
        Status:    "confirmed",
    }
    
    eventBytes, _ := json.Marshal(eventData)
    msg := commonEvents.Message{Data: eventBytes}
    
    // ... test handler processes correctly
}

func TestHandlePaymentConfirmed_InvalidPayload(t *testing.T) {
    msg := commonEvents.Message{Data: []byte("invalid json")}
    
    err := consumer.HandlePaymentConfirmed(ctx, msg)
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "decode")
}
```

---

## Running Tests

```bash
# Run all tests in a service
cd /home/user/microservices/<service>
go test ./...

# Run specific package tests
go test ./internal/biz/order/...

# Run specific test
go test ./internal/biz/order/ -run TestCreateOrder_Success

# With verbose output
go test -v ./internal/biz/order/...

# With coverage
go test -cover ./internal/biz/...
go test -coverprofile=coverage.out ./internal/biz/...
go tool cover -html=coverage.out
```

---

## Checklist

- [ ] Tests use `testify/assert` and `testify/require`
- [ ] Table-driven tests for validation and multiple scenarios
- [ ] Mocks defined in `internal/biz/mocks.go` (manual) or `_test.go` (testify)
- [ ] Mock implements the full interface
- [ ] Happy path tested
- [ ] Error cases tested (DB errors, validation, not found)
- [ ] Edge cases tested (nil, empty, zero values)
- [ ] `mockRepo.AssertExpectations(t)` called for testify mocks
- [ ] Tests run: `go test ./...`
- [ ] No test leaks (goroutines, file handles)
