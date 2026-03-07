---
description: Workflow for safely refactoring code while maintaining functionality
---

## Refactoring Workflow

This workflow guides you through refactoring code safely without breaking functionality.

### When to Use
- Code smells detected (duplication, long functions, god classes)
- Technical debt needs to be addressed
- Performance optimization needed
- Architecture improvements required
- After code review feedback

### Prerequisites
- Existing tests in place (or write them first)
- Clear refactoring goal
- Understanding of current implementation
- Time allocated (refactoring takes longer than expected)

### Refactoring Principles

**The Golden Rule**: Refactoring should NOT change behavior

**Red-Green-Refactor Cycle**:
1. **Red**: Write failing test (if needed)
2. **Green**: Make it pass (quick & dirty)
3. **Refactor**: Clean up while keeping tests green

### Workflow Steps

#### Phase 1: Preparation

**1.1 Ensure Tests Exist**

```bash
cd /home/user/microservices/<service>

# Check test coverage
go test ./internal/... -cover

# If coverage < 60%, write tests FIRST
# Use skill: write-tests
```

**1.2 Run All Tests (Baseline)**

```bash
# All tests must pass before refactoring
go test ./... -v

# Record baseline
go test ./... -v > /tmp/baseline_tests.txt
```

**1.3 Identify Refactoring Target**

Common targets:
- Long functions (>50 lines)
- Duplicated code
- God classes/services
- Complex conditionals
- Magic numbers
- Poor naming

**1.4 Define Success Criteria**

What will be better after refactoring?
- [ ] Code is more readable
- [ ] Duplication removed
- [ ] Functions are smaller
- [ ] Complexity reduced
- [ ] Performance improved
- [ ] Tests still pass

#### Phase 2: Small Steps Refactoring

**CRITICAL**: Make small, incremental changes. Test after each change.

**2.1 Extract Method**

```go
// BEFORE: Long function
func (s *OrderService) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderReply, error) {
    // 100 lines of code
    // Validation
    // Price calculation
    // Inventory check
    // Payment processing
    // Order creation
    // Event publishing
}

// AFTER: Extracted methods
func (s *OrderService) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderReply, error) {
    if err := s.validateRequest(req); err != nil {
        return nil, err
    }
    
    price := s.calculateTotalPrice(req.Items)
    
    if err := s.checkInventory(ctx, req.Items); err != nil {
        return nil, err
    }
    
    if err := s.processPayment(ctx, req.PaymentInfo, price); err != nil {
        return nil, err
    }
    
    order, err := s.createOrder(ctx, req, price)
    if err != nil {
        return nil, err
    }
    
    s.publishOrderCreatedEvent(ctx, order)
    
    return toProtoReply(order), nil
}
```

**Test after extraction**:
```bash
go test ./internal/service/... -v
```

**2.2 Extract Variable**

```go
// BEFORE: Magic numbers
if order.Total > 1000000 && order.Items > 50 {
    // Apply bulk discount
}

// AFTER: Named constants
const (
    BulkOrderMinAmount = 1000000
    BulkOrderMinItems  = 50
)

if order.Total > BulkOrderMinAmount && order.Items > BulkOrderMinItems {
    // Apply bulk discount
}
```

**2.3 Remove Duplication**

```go
// BEFORE: Duplicated code
func (s *Service) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.CreateUserReply, error) {
    if req.Email == "" {
        return nil, errors.InvalidArgument("INVALID_EMAIL", "email is required")
    }
    if !isValidEmail(req.Email) {
        return nil, errors.InvalidArgument("INVALID_EMAIL", "email format is invalid")
    }
    // ... create user
}

func (s *Service) UpdateUser(ctx context.Context, req *pb.UpdateUserRequest) (*pb.UpdateUserReply, error) {
    if req.Email == "" {
        return nil, errors.InvalidArgument("INVALID_EMAIL", "email is required")
    }
    if !isValidEmail(req.Email) {
        return nil, errors.InvalidArgument("INVALID_EMAIL", "email format is invalid")
    }
    // ... update user
}

// AFTER: Extract common validation
func (s *Service) validateEmail(email string) error {
    if email == "" {
        return errors.InvalidArgument("INVALID_EMAIL", "email is required")
    }
    if !isValidEmail(email) {
        return errors.InvalidArgument("INVALID_EMAIL", "email format is invalid")
    }
    return nil
}

func (s *Service) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.CreateUserReply, error) {
    if err := s.validateEmail(req.Email); err != nil {
        return nil, err
    }
    // ... create user
}

func (s *Service) UpdateUser(ctx context.Context, req *pb.UpdateUserRequest) (*pb.UpdateUserReply, error) {
    if err := s.validateEmail(req.Email); err != nil {
        return nil, err
    }
    // ... update user
}
```

**2.4 Simplify Conditionals**

```go
// BEFORE: Complex nested conditionals
func (s *Service) CanApplyDiscount(order *Order) bool {
    if order != nil {
        if order.Total > 100 {
            if order.Customer != nil {
                if order.Customer.IsPremium {
                    return true
                }
            }
        }
    }
    return false
}

// AFTER: Early returns
func (s *Service) CanApplyDiscount(order *Order) bool {
    if order == nil {
        return false
    }
    if order.Total <= 100 {
        return false
    }
    if order.Customer == nil {
        return false
    }
    return order.Customer.IsPremium
}
```

**2.5 Replace Magic Numbers with Constants**

```go
// BEFORE: Magic numbers
func (s *Service) CalculateShipping(weight float64) float64 {
    if weight < 1 {
        return 5.0
    } else if weight < 5 {
        return 10.0
    } else {
        return 15.0
    }
}

// AFTER: Named constants
const (
    ShippingLightWeight   = 1.0
    ShippingMediumWeight  = 5.0
    ShippingLightCost     = 5.0
    ShippingMediumCost    = 10.0
    ShippingHeavyCost     = 15.0
)

func (s *Service) CalculateShipping(weight float64) float64 {
    if weight < ShippingLightWeight {
        return ShippingLightCost
    } else if weight < ShippingMediumWeight {
        return ShippingMediumCost
    } else {
        return ShippingHeavyCost
    }
}
```

#### Phase 3: Test After Each Change

**CRITICAL**: Test after EVERY refactoring step

```bash
# Run tests
go test ./internal/<package>/... -v

# If tests fail, revert and try smaller step
git checkout -- internal/<package>/<file>.go
```

#### Phase 4: Larger Refactorings

**4.1 Move to Common Library**

If code is used by multiple services:

```bash
# Move to common
cp internal/utils/helper.go /home/user/microservices/common/utils/

# Update common
cd /home/user/microservices/common
go test ./utils/... -v
git add utils/
git commit -m "feat(common): add helper utility"
git tag -a v1.x.y -m "v1.x.y: add helper utility"
git push origin main && git push origin v1.x.y

# Update service to use common
cd /home/user/microservices/<service>
go get gitlab.com/ta-microservices/common@v1.x.y
# Update imports
# Remove old file
rm internal/utils/helper.go
```

**4.2 Extract to Separate Package**

```bash
# Create new package
mkdir -p internal/calculator

# Move related functions
mv internal/service/price_calculation.go internal/calculator/

# Update package name and imports
vim internal/calculator/price_calculation.go

# Update imports in service
vim internal/service/<service>.go
```

**4.3 Introduce Interface**

```go
// BEFORE: Concrete dependency
type OrderService struct {
    emailSender *EmailSender
}

// AFTER: Interface dependency
type EmailSender interface {
    SendEmail(ctx context.Context, to, subject, body string) error
}

type OrderService struct {
    emailSender EmailSender
}

// Now can mock in tests
type MockEmailSender struct{}

func (m *MockEmailSender) SendEmail(ctx context.Context, to, subject, body string) error {
    return nil
}
```

**4.4 Replace Conditional with Polymorphism**

```go
// BEFORE: Type switch
func (s *Service) CalculatePrice(item Item) float64 {
    switch item.Type {
    case "book":
        return item.BasePrice * 0.9  // 10% discount
    case "electronics":
        return item.BasePrice * 0.95  // 5% discount
    case "clothing":
        return item.BasePrice * 0.8  // 20% discount
    default:
        return item.BasePrice
    }
}

// AFTER: Strategy pattern
type PricingStrategy interface {
    CalculatePrice(basePrice float64) float64
}

type BookPricing struct{}
func (b *BookPricing) CalculatePrice(basePrice float64) float64 {
    return basePrice * 0.9
}

type ElectronicsPricing struct{}
func (e *ElectronicsPricing) CalculatePrice(basePrice float64) float64 {
    return basePrice * 0.95
}

type ClothingPricing struct{}
func (c *ClothingPricing) CalculatePrice(basePrice float64) float64 {
    return basePrice * 0.8
}

func (s *Service) CalculatePrice(item Item, strategy PricingStrategy) float64 {
    return strategy.CalculatePrice(item.BasePrice)
}
```

#### Phase 5: Performance Refactoring

**5.1 Fix N+1 Queries**

```go
// BEFORE: N+1 query
func (r *OrderRepo) GetOrdersWithCustomers(ctx context.Context) ([]*Order, error) {
    var orders []*Order
    r.db.Find(&orders)
    
    for i := range orders {
        r.db.First(&orders[i].Customer, orders[i].CustomerID)  // N queries
    }
    return orders, nil
}

// AFTER: Preload
func (r *OrderRepo) GetOrdersWithCustomers(ctx context.Context) ([]*Order, error) {
    var orders []*Order
    err := r.db.Preload("Customer").Find(&orders).Error  // 2 queries total
    return orders, err
}
```

**5.2 Add Caching**

```go
// BEFORE: Always query DB
func (r *ProductRepo) GetByID(ctx context.Context, id string) (*Product, error) {
    var product Product
    err := r.db.First(&product, "id = ?", id).Error
    return &product, err
}

// AFTER: Cache-aside pattern
func (r *ProductRepo) GetByID(ctx context.Context, id string) (*Product, error) {
    // Try cache first
    cacheKey := fmt.Sprintf("product:%s", id)
    if cached, err := r.cache.Get(ctx, cacheKey); err == nil {
        var product Product
        json.Unmarshal([]byte(cached), &product)
        return &product, nil
    }
    
    // Cache miss, query DB
    var product Product
    err := r.db.First(&product, "id = ?", id).Error
    if err != nil {
        return nil, err
    }
    
    // Store in cache
    data, _ := json.Marshal(product)
    r.cache.Set(ctx, cacheKey, data, 5*time.Minute)
    
    return &product, nil
}
```

**5.3 Use Batch Operations**

```go
// BEFORE: Loop with individual inserts
func (r *OrderRepo) CreateOrders(ctx context.Context, orders []*Order) error {
    for _, order := range orders {
        if err := r.db.Create(order).Error; err != nil {
            return err
        }
    }
    return nil
}

// AFTER: Batch insert
func (r *OrderRepo) CreateOrders(ctx context.Context, orders []*Order) error {
    return r.db.CreateInBatches(orders, 100).Error
}
```

#### Phase 6: Verify & Document

**6.1 Run Full Test Suite**

```bash
# All tests
go test ./... -v

# With race detector
go test ./... -race

# With coverage
go test ./... -cover
```

**6.2 Benchmark (if performance refactoring)**

```bash
# Run benchmarks
go test ./internal/<package>/... -bench=. -benchmem

# Compare with baseline
# Before: BenchmarkCalculatePrice-8   1000000   1234 ns/op
# After:  BenchmarkCalculatePrice-8   2000000    567 ns/op
```

**6.3 Lint**

```bash
golangci-lint run
```

**6.4 Build**

```bash
go build ./...
```

**6.5 Update Documentation**

```bash
# Update CHANGELOG.md
vim CHANGELOG.md
```

```markdown
## [Unreleased]
### Changed
- Refactored <component> to improve <aspect>
  - Extracted <method> for better readability
  - Removed code duplication in <area>
  - Improved performance by <optimization>
```

#### Phase 7: Commit

```bash
cd /home/user/microservices/<service>

rm -rf bin/

git add -A
git commit -m "refactor(<service>): improve <component>

- Extracted methods for better readability
- Removed code duplication
- Simplified complex conditionals
- Added constants for magic numbers

No functional changes. All tests pass."

git push origin main
```

### Refactoring Patterns

#### Pattern 1: Extract Method
**When**: Function is too long (>50 lines)
**How**: Extract logical blocks into separate methods

#### Pattern 2: Extract Variable
**When**: Complex expression or magic number
**How**: Assign to well-named variable/constant

#### Pattern 3: Inline Method
**When**: Method body is as clear as its name
**How**: Replace method call with method body

#### Pattern 4: Move Method
**When**: Method uses more features of another class
**How**: Move to the class it uses most

#### Pattern 5: Replace Conditional with Polymorphism
**When**: Type-based conditionals
**How**: Use interfaces and implementations

#### Pattern 6: Introduce Parameter Object
**When**: Functions have long parameter lists
**How**: Group parameters into object

```go
// BEFORE
func CreateOrder(customerID, productID, quantity, shippingAddr, billingAddr string, price float64) error

// AFTER
type OrderRequest struct {
    CustomerID   string
    ProductID    string
    Quantity     int
    ShippingAddr string
    BillingAddr  string
    Price        float64
}

func CreateOrder(req OrderRequest) error
```

### Common Refactoring Mistakes

**Mistake 1: Refactoring without tests**
- Always have tests before refactoring
- Tests are your safety net

**Mistake 2: Too many changes at once**
- Make small, incremental changes
- Test after each change

**Mistake 3: Changing behavior**
- Refactoring should NOT change behavior
- If behavior changes, it's not refactoring

**Mistake 4: Premature optimization**
- Don't optimize without profiling
- Measure before and after

**Mistake 5: Over-engineering**
- Keep it simple
- Don't add complexity for future needs

### Checklist

- [ ] Tests exist and pass (baseline)
- [ ] Refactoring goal defined
- [ ] Success criteria clear
- [ ] Made small, incremental changes
- [ ] Tested after each change
- [ ] All tests still pass
- [ ] No behavior changes
- [ ] Lint passes
- [ ] Build successful
- [ ] Performance verified (if applicable)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Committed with clear message

### Related Workflows
- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)

### Related Skills
- review-code
- write-tests
- use-common-lib
