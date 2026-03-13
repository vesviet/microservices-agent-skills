---
name: write-tests
description: Write unit and integration tests following the project's testing patterns - testify, table-driven tests, mockgen-generated mocks
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
3. **Generated mocks via `mockgen`** — Use `go.uber.org/mock/mockgen` to generate mocks in `internal/biz/mocks/` subpackage. Run `go generate ./internal/biz/...` after interface changes
4. **Test biz layer primarily** — This is where business logic lives
5. **Test in same package** — Test files in the same package as the code being tested
6. **Use `_test.go` suffix** — Standard Go convention
7. **Commit & push after done** — After all tests pass and checklists are updated, use the `commit-code` skill to commit and push changes

---

## Test File Locations

```
<service>/
├── internal/
│   ├── biz/
│   │   ├── mocks/                        # 🔴 Generated mocks (mockgen)
│   │   │   ├── mock_order_repo.go        #   go:generate mockgen output
│   │   │   └── mock_event_publisher.go
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

### Choosing the Right Mock Framework

> ⚠️ Use ONE framework per test file. NEVER mix mockgen and testify/mock in the same file.

| Criteria | `mockgen` (gomock) | `testify/mock` |
|---|---|---|
| Interface has **4+ methods** | ✅ Use this | ❌ Too verbose |
| Interface has **1-3 methods** | ⚠️ Overkill | ✅ Use this |
| **Cross-package** mocks (shared by multiple tests) | ✅ Use this → `internal/biz/mocks/` | ❌ Not recommended |
| **Single-file** test helper | ❌ Too heavy | ✅ Use this → `*_test.go` |
| Need **strict call order** verification | ✅ `InOrder()` | ⚠️ Limited |
| Need **argument matching** flexibility | ✅ `gomock.Any()` | ✅ `mock.Anything` |

### Generated Mocks via mockgen (Project Standard)

The project uses `go.uber.org/mock/mockgen` to generate mocks from interfaces.

**Step 1: Add `//go:generate` directives to interface files**

```go
// In internal/biz/interfaces.go
package biz

//go:generate mockgen -destination=mocks/mock_order_repo.go -package=mocks . OrderRepo
//go:generate mockgen -destination=mocks/mock_event_publisher.go -package=mocks . EventPublisher

type OrderRepo interface {
    FindByID(ctx context.Context, id string) (*model.Order, error)
    Create(ctx context.Context, order *model.Order) error
}
```

**Step 2: Generate mocks**

```bash
cd <service>
go generate ./internal/biz/...
```

**Step 3: Use in tests**

```go
package order_test

import (
    "testing"
    "go.uber.org/mock/gomock"
    "gitlab.com/ta-microservices/<service>/internal/biz/mocks"
)

func TestCreateOrder_Success(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockOrderRepo(ctrl)
    mockRepo.EXPECT().FindByCartSessionID(gomock.Any(), gomock.Any()).
        Return(nil, nil).Times(1)
    mockRepo.EXPECT().Create(gomock.Any(), gomock.Any()).
        Return(nil).Times(1)

    // Act
    result, err := createOrder(ctx, mockRepo, req)

    // Assert
    require.NoError(t, err)
    assert.NotNil(t, result)
}
```

### Testify Mocks in `*_test.go` (For Simpler Cases)

For simpler mock needs within test files, testify mock is still acceptable:

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
cd <service>
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

### Test Implementation
- [ ] Tests use `testify/assert` and `testify/require`
- [ ] Table-driven tests for validation and multiple scenarios
- [ ] Generated mocks via `mockgen` in `internal/biz/mocks/` (or testify mocks in `_test.go`)
- [ ] Mock implements the full interface
- [ ] Happy path tested
- [ ] Error cases tested (DB errors, validation, not found)
- [ ] Edge cases tested (nil, empty, zero values)
- [ ] `mockRepo.AssertExpectations(t)` called for testify mocks

### Test Execution
- [ ] Tests run successfully: `go test ./...`
- [ ] No test leaks (goroutines, file handles)
- [ ] Coverage checked: `go test -cover ./internal/biz/...`
- [ ] Coverage meets targets (≥60% for biz layer)

### Documentation
- [ ] Test files follow naming convention (`*_test.go`)
- [ ] Test functions have descriptive names
- [ ] Complex test logic has comments
- [ ] **⚠️ MANDATORY: Update `docs/10-appendix/checklists/test/TEST_COVERAGE_CHECKLIST.md`** after tests are done

### Commit & Push
- [ ] Use `commit-code` skill to commit and push all test changes
- [ ] Commit message uses `test(<service>): <description>` format
- [ ] Pushed to remote

---

## ⚠️ MANDATORY: Update Coverage Checklist After Tests Done

**After completing test coverage work for ANY service, you MUST update the test coverage checklist:**

**File**: `docs/10-appendix/checklists/test/TEST_COVERAGE_CHECKLIST.md`

**What to update:**
1. **"Last Updated" timestamp** in the header
2. **"Recent Changes" table** — add a row for the service you worked on
3. **Dashboard table** — update the service's Current %, Gap, Est. Effort, and Work Done columns
4. **Per-Service section** — update each package's coverage %, mark completed items with ✅, add ⚡ for improved items
5. **Sprint section** — mark service as `⚡ partially done` if applicable
6. **Test Files inventory** — add new/modified test files

**How to get coverage numbers:**
```bash
cd <service>
go test -cover ./internal/biz/... 2>&1 | grep -E "^ok|coverage"
```

This checklist is the **single source of truth** for test coverage status across all services. Other agents rely on it to know what work has been done and what remains.

---

## Quick Reference Checklist

Use this checklist for quick test writing workflow:

### Setup
- [ ] Identified code to test (biz layer priority)
- [ ] Checked existing test patterns in service
- [ ] Reviewed interfaces that need mocking

### Write Tests
- [ ] Created `*_test.go` file in same package
- [ ] Imported testify (`assert`, `require`)
- [ ] Used table-driven pattern for multiple cases
- [ ] Generated mocks via `mockgen` (if needed)
- [ ] Tested happy path
- [ ] Tested error cases
- [ ] Tested edge cases

### Verify
- [ ] Tests pass: `go test ./...`
- [ ] Coverage checked: `go test -cover ./internal/biz/...`
- [ ] No test leaks
- [ ] Mock expectations asserted

### Document
- [ ] Updated TEST_COVERAGE_CHECKLIST.md
- [ ] Added coverage numbers
- [ ] Marked completed items

### Commit & Push
- [ ] Use `commit-code` skill to commit and push all test changes
- [ ] Commit message uses `test(<service>): <description>` format
- [ ] Pushed to remote

---

## ⚠️ MANDATORY: Commit & Push After Done

**After completing all test work, you MUST commit and push using the `commit-code` skill.**

```bash
cd <service>
rm -rf bin/
git add -A
git commit -m "test(<service>): <description of test changes>"
git push origin main
```

> For full commit workflow (lint, build, dependency checks), refer to the **commit-code** skill.

---

## Related Skills

- **commit-code**: Commit and push changes after tests are done
- **review-service**: Full service review includes test coverage check
- **add-api-endpoint**: New endpoints require corresponding tests
- **troubleshoot-service**: Debug test failures and coverage issues
- **review-code**: Code review includes test quality assessment
