---
name: add-service-client
description: Add a gRPC client to enable communication between two microservices via service discovery
---

# Add Service Client Skill

Use this skill when a service needs to call another service's API (service-to-service communication).

## ⚠️ CRITICAL RULE: Internal calls MUST use gRPC

**ALL service-to-service communication MUST use gRPC.** Never use HTTP for internal calls.

```
┌─────────────┐   gRPC (port 90XX)  ┌─────────────┐
│  Service A  │ ──────────────────→  │  Service B  │
│ (consumer)  │   direct address     │ (provider)  │
└─────────────┘                      └─────────────┘
```

- **Protocol**: gRPC only (strongly typed, high performance)
- **Address**: K8s DNS `<service>-service.<service>-dev.svc.cluster.local:<grpc-port>`
- **Security**: Insecure inside cluster (TLS configurable for production)
- **Resilience**: Circuit breaker + keepalive + gzip compression

## When to Use
- Service A needs data from Service B
- Cross-service business logic (e.g., Order needs Product details from Catalog)
- Adding new inter-service dependency

## Real Pattern from Codebase

This project uses a consistent pattern across all services. See existing examples:
- `order/internal/client/catalog_grpc_client.go`
- `order/internal/client/user_grpc_client.go`
- `order/internal/client/payment_grpc_client.go`

**Always check existing clients first before creating new ones:**
```bash
find /home/user/microservices/*/internal/client -name "*_grpc_client.go" 2>/dev/null
```

---

## Step-by-Step Process

### Step 1: Import the Target Service's Proto Package

Each service generates its proto client in `api/<service>/v1/`. Import it via Go module:

```go
import targetV1 "gitlab.com/ta-microservices/<target-service>/api/<target-service>/v1"
```

Update `go.mod`:
```bash
cd /home/user/microservices/<source-service>

# Add dependency
go get gitlab.com/ta-microservices/<target-service>@latest

# Or use replace for local development
# In go.mod:
# replace gitlab.com/ta-microservices/<target-service> => ../<target-service>
```

### Step 2: Define the Client Interface

**File**: `<source-service>/internal/client/types.go` (or existing types file)

Define what methods the consumer needs. **Only expose what you actually need, not the entire target API.**

```go
// TargetClient defines the interface for calling <target-service>
type TargetClient interface {
	GetSomething(ctx context.Context, id string) (*Something, error)
	Close() error
}

// Something is the client-side DTO (NOT the proto message directly)
type Something struct {
	ID   string
	Name string
	// ... only fields you need
}
```

### Step 3: Create the gRPC Client Implementation

**File**: `<source-service>/internal/client/<target>_grpc_client.go`

Follow the **exact pattern** used in the codebase:

```go
package client

import (
	"context"
	"fmt"
	"time"

	"github.com/go-kratos/kratos/v2/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/encoding/gzip"
	"google.golang.org/grpc/keepalive"

	"gitlab.com/ta-microservices/common/client/circuitbreaker"
	targetV1 "gitlab.com/ta-microservices/<target>/api/<target>/v1"
)

// grpcTargetClient implements TargetClient using gRPC
type grpcTargetClient struct {
	conn           *grpc.ClientConn
	client         targetV1.<Target>ServiceClient
	logger         *log.Helper
	circuitBreaker *circuitbreaker.CircuitBreaker
}

// NewGRPCTargetClient creates a new gRPC target client
// targetServiceAddr: gRPC address (e.g., "target-service.target-dev.svc.cluster.local:90XX")
// useTLS: Enable TLS (default: false for internal network)
// tlsCertPath: Path to custom TLS certificate (optional)
func NewGRPCTargetClient(targetServiceAddr string, useTLS bool, tlsCertPath string, logger log.Logger) (TargetClient, error) {
	if targetServiceAddr == "" {
		return nil, fmt.Errorf("target service address is required")
	}

	// Get appropriate credentials based on config
	credsOption, err := GetGRPCCredentials(useTLS, tlsCertPath)
	if err != nil {
		return nil, fmt.Errorf("failed to get gRPC credentials: %w", err)
	}

	conn, err := grpc.NewClient(
		targetServiceAddr,
		credsOption,
		grpc.WithKeepaliveParams(keepalive.ClientParameters{
			Time:                10 * time.Second,
			Timeout:             3 * time.Second,
			PermitWithoutStream: true,
		}),
		grpc.WithDefaultCallOptions(grpc.UseCompressor(gzip.Name)),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to target service: %w", err)
	}

	client := targetV1.New<Target>ServiceClient(conn)

	// Create circuit breaker
	config := circuitbreaker.DefaultConfig()
	config.ReadyToTrip = func(counts circuitbreaker.Counts) bool {
		return counts.ConsecutiveFailures >= 5
	}
	cb := circuitbreaker.NewCircuitBreaker("target-service-grpc", config, logger)

	return &grpcTargetClient{
		conn:           conn,
		client:         client,
		logger:         log.NewHelper(logger),
		circuitBreaker: cb,
	}, nil
}

// Close closes the gRPC connection
func (c *grpcTargetClient) Close() error {
	if c.conn != nil {
		return c.conn.Close()
	}
	return nil
}

// GetSomething calls target service with circuit breaker and timeout
func (c *grpcTargetClient) GetSomething(ctx context.Context, id string) (*Something, error) {
	// Add timeout (5 seconds for quick operations)
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	var resp *targetV1.GetSomethingReply
	var err error

	// Wrap gRPC call with circuit breaker
	err = c.circuitBreaker.Call(func() error {
		resp, err = c.client.GetSomething(ctx, &targetV1.GetSomethingRequest{
			Id: id,
		})
		if err != nil {
			return mapGRPCError(err, "GetSomething")
		}
		if resp == nil {
			return fmt.Errorf("something not found: %s", id)
		}
		return nil
	})

	if err != nil {
		c.logger.WithContext(ctx).Errorf("Failed to get something via gRPC: %v", err)
		return nil, err
	}

	// Convert proto response to client DTO
	return &Something{
		ID:   resp.Id,
		Name: resp.Name,
	}, nil
}
```

### Step 4: Add GetGRPCCredentials Helper (if not exists)

If the source service doesn't have this helper yet, create it:

**File**: `<source-service>/internal/client/grpc_credentials.go`

```go
package client

import (
	"crypto/tls"
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
)

// GetGRPCCredentials returns appropriate gRPC transport credentials
func GetGRPCCredentials(useTLS bool, tlsCertPath string) (grpc.DialOption, error) {
	if !useTLS {
		return grpc.WithTransportCredentials(insecure.NewCredentials()), nil
	}
	if tlsCertPath != "" {
		creds, err := credentials.NewClientTLSFromFile(tlsCertPath, "")
		if err != nil {
			return nil, fmt.Errorf("failed to load TLS certificate: %w", err)
		}
		return grpc.WithTransportCredentials(creds), nil
	}
	return grpc.WithTransportCredentials(credentials.NewTLS(&tls.Config{
		MinVersion: tls.VersionTLS12,
	})), nil
}
```

### Step 5: Add mapGRPCError Helper (if not exists)

**File**: `<source-service>/internal/client/grpc_helpers.go`

```go
package client

import (
	"fmt"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func mapGRPCError(err error, method string) error {
	st, ok := status.FromError(err)
	if !ok {
		return fmt.Errorf("service error in %s: %w", method, err)
	}
	switch st.Code() {
	case codes.DeadlineExceeded:
		return fmt.Errorf("service timeout in %s: %w", method, err)
	case codes.Unavailable:
		return fmt.Errorf("service unavailable in %s: %w", method, err)
	case codes.NotFound:
		return fmt.Errorf("resource not found in %s: %w", method, err)
	case codes.InvalidArgument:
		return fmt.Errorf("invalid request in %s: %w", method, err)
	case codes.PermissionDenied:
		return fmt.Errorf("permission denied in %s: %w", method, err)
	default:
		return fmt.Errorf("service error [%s] in %s: %w", st.Code(), method, err)
	}
}
```

### Step 6: Wire Dependency Injection

**File**: `<source-service>/cmd/<service>/wire.go`

```go
var providerSet = wire.NewSet(
	// ... existing providers
	client.NewGRPCTargetClient,  // Add gRPC client provider
)
```

Regenerate wire:
```bash
cd /home/user/microservices/<source-service>/cmd/<service> && wire
```

### Step 7: Configure Service Address

Add the target service gRPC address to the source service's config:

**Service config** (`<source-service>/configs/config.yaml`):
```yaml
services:
  target:
    grpc_addr: "localhost:90XX"   # Local dev
```

**K8s ConfigMap** (`gitops/apps/<source-service>/overlays/dev/configmap.yaml`):
```yaml
data:
  TARGET_GRPC_ADDR: "target-service.target-dev.svc.cluster.local:90XX"
```

---

## gRPC Service Addresses (K8s DNS)

| Service | gRPC Port | K8s DNS Address |
|---------|-----------|-----------------|
| Auth | 9000 | `auth-service.auth-dev.svc.cluster.local:9000` |
| User | 9001 | `user-service.user-dev.svc.cluster.local:9001` |
| Pricing | 9002 | `pricing-service.pricing-dev.svc.cluster.local:9002` |
| Customer | 9003 | `customer-service.customer-dev.svc.cluster.local:9003` |
| Order | 9004 | `order-service.order-dev.svc.cluster.local:9004` |
| Payment | 9005 | `payment-service.payment-dev.svc.cluster.local:9005` |
| Warehouse | 9006 | `warehouse-service.warehouse-dev.svc.cluster.local:9006` |
| Location | 9007 | `location-service.location-dev.svc.cluster.local:9007` |
| Fulfillment | 9008 | `fulfillment-service.fulfillment-dev.svc.cluster.local:9008` |
| Notification | 9009 | `notification-service.notification-dev.svc.cluster.local:9009` |
| Checkout | 9010 | `checkout-service.checkout-dev.svc.cluster.local:9010` |
| Promotion | 9011 | `promotion-service.promotion-dev.svc.cluster.local:9011` |
| Shipping | 9012 | `shipping-service.shipping-dev.svc.cluster.local:9012` |
| Return | 9013 | `return-service.return-dev.svc.cluster.local:9013` |
| Loyalty | 9014 | `loyalty-rewards-service.loyalty-rewards-dev.svc.cluster.local:9014` |
| Catalog | 9015 | `catalog-service.catalog-dev.svc.cluster.local:9015` |
| Review | 9016 | `review-service.review-dev.svc.cluster.local:9016` |
| Search | 9017 | `search-service.search-dev.svc.cluster.local:9017` |
| Analytics | 9018 | `analytics-service.analytics-dev.svc.cluster.local:9018` |

---

## Key Components Summary

| File | Purpose |
|------|---------|
| `client/types.go` | Client interfaces + DTOs |
| `client/<target>_grpc_client.go` | gRPC client implementation |
| `client/grpc_credentials.go` | TLS/insecure credential helper |
| `client/grpc_helpers.go` | `mapGRPCError` helper |
| `cmd/<service>/wire.go` | Wire DI registration |
| `configs/config.yaml` | Service address config |

## Checklist

- [ ] Target service proto package imported (`go get`)
- [ ] Client interface defined in `client/types.go`
- [ ] gRPC client implemented with `grpc.NewClient` + circuit breaker + keepalive
- [ ] `GetGRPCCredentials` helper exists
- [ ] `mapGRPCError` helper exists
- [ ] Response converted to client DTO (NOT exposing proto types to biz layer)
- [ ] Wire DI configured and regenerated
- [ ] Service address configured (config.yaml + K8s configmap)
- [ ] Build passes (`go build ./...`)
- [ ] **CHANGELOG.md updated** (new service client = MINOR version bump)
