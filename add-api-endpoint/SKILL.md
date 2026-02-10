---
name: add-api-endpoint
description: Add a new API endpoint to a Go microservice following the project's Kratos + Clean Architecture patterns
---

# Add API Endpoint Skill

Use this skill when the user needs to add a new API endpoint (REST/gRPC) to any Go microservice.

## When to Use
- Adding new CRUD endpoints
- Adding new business operations
- Extending existing API with new functionality

## Architecture Flow

Adding a new endpoint requires changes across multiple layers:

```
1. Proto Definition (api/<service>/v1/*.proto)
        ↓
2. Generate Code (make api)
        ↓
3. Service Layer (internal/service/*.go)     ← implements proto-generated interface
        ↓
4. Business Logic (internal/biz/*.go)         ← domain logic & use cases
        ↓
5. Data Layer (internal/data/*.go)            ← repository implementation
        ↓
6. Wire DI (cmd/<service>/wire.go)            ← dependency injection
```

## Step-by-Step Process

### Step 1: Define the API in Proto

**File**: `api/<service>/v1/<service>.proto`

```protobuf
syntax = "proto3";

package api.<service>.v1;

import "google/api/annotations.proto";

service <Service>Service {
  // Existing RPCs...

  // NEW: Add your RPC here
  rpc GetExample (GetExampleRequest) returns (GetExampleReply) {
    option (google.api.http) = {
      get: "/api/v1/<service>/examples/{id}"
    };
  }

  rpc CreateExample (CreateExampleRequest) returns (CreateExampleReply) {
    option (google.api.http) = {
      post: "/api/v1/<service>/examples"
      body: "*"
    };
  }

  rpc ListExamples (ListExamplesRequest) returns (ListExamplesReply) {
    option (google.api.http) = {
      get: "/api/v1/<service>/examples"
    };
  }

  rpc UpdateExample (UpdateExampleRequest) returns (UpdateExampleReply) {
    option (google.api.http) = {
      put: "/api/v1/<service>/examples/{id}"
      body: "*"
    };
  }

  rpc DeleteExample (DeleteExampleRequest) returns (DeleteExampleReply) {
    option (google.api.http) = {
      delete: "/api/v1/<service>/examples/{id}"
    };
  }
}

// Messages
message GetExampleRequest {
  string id = 1;
}

message GetExampleReply {
  ExampleData data = 1;
}

message CreateExampleRequest {
  string name = 1;
  string description = 2;
}

message CreateExampleReply {
  ExampleData data = 1;
}

message ListExamplesRequest {
  int32 page = 1;
  int32 page_size = 2;
}

message ListExamplesReply {
  repeated ExampleData items = 1;
  int32 total = 2;
}

message ExampleData {
  string id = 1;
  string name = 2;
  string description = 3;
  string created_at = 4;
}
```

### Step 2: Generate Proto Code

```bash
cd /home/user/microservices/<service> && make api
```

This generates:
- `api/<service>/v1/<service>.pb.go` - Message types
- `api/<service>/v1/<service>_grpc.pb.go` - gRPC server/client
- `api/<service>/v1/<service>_http.pb.go` - HTTP server

### Step 3: Define Domain Entity (Business Layer)

**File**: `internal/biz/<entity>.go`

```go
package biz

import (
	"context"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

// Domain entity
type Example struct {
	ID          string
	Name        string
	Description string
	CreatedAt   time.Time
	UpdatedAt   time.Time
}

// Repository interface (contract for data layer)
type ExampleRepo interface {
	Create(ctx context.Context, example *Example) (*Example, error)
	Get(ctx context.Context, id string) (*Example, error)
	List(ctx context.Context, page, pageSize int) ([]*Example, int, error)
	Update(ctx context.Context, example *Example) (*Example, error)
	Delete(ctx context.Context, id string) error
}

// Use case (business logic)
type ExampleUsecase struct {
	repo ExampleRepo
	log  *log.Helper
}

func NewExampleUsecase(repo ExampleRepo, logger log.Logger) *ExampleUsecase {
	return &ExampleUsecase{
		repo: repo,
		log:  log.NewHelper(logger),
	}
}

func (uc *ExampleUsecase) Create(ctx context.Context, example *Example) (*Example, error) {
	// Add business validation here
	return uc.repo.Create(ctx, example)
}

func (uc *ExampleUsecase) Get(ctx context.Context, id string) (*Example, error) {
	return uc.repo.Get(ctx, id)
}

func (uc *ExampleUsecase) List(ctx context.Context, page, pageSize int) ([]*Example, int, error) {
	if pageSize <= 0 {
		pageSize = 20
	}
	if page <= 0 {
		page = 1
	}
	return uc.repo.List(ctx, page, pageSize)
}
```

### Step 4: Implement Repository (Data Layer)

**File**: `internal/data/<entity>.go`

```go
package data

import (
	"context"

	"github.com/go-kratos/kratos/v2/log"
	"<module>/internal/biz"
)

type exampleRepo struct {
	data *Data
	log  *log.Helper
}

func NewExampleRepo(data *Data, logger log.Logger) biz.ExampleRepo {
	return &exampleRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

func (r *exampleRepo) Create(ctx context.Context, example *biz.Example) (*biz.Example, error) {
	// GORM implementation
	model := &ExampleModel{
		Name:        example.Name,
		Description: example.Description,
	}
	if err := r.data.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, err
	}
	return modelToEntity(model), nil
}
```

### Step 5: Implement Service Layer

**File**: `internal/service/<service>.go`

```go
// Implement the proto-generated interface method
func (s *<Service>Service) GetExample(ctx context.Context, req *pb.GetExampleRequest) (*pb.GetExampleReply, error) {
	example, err := s.uc.Get(ctx, req.Id)
	if err != nil {
		return nil, err
	}
	return &pb.GetExampleReply{
		Data: &pb.ExampleData{
			Id:          example.ID,
			Name:        example.Name,
			Description: example.Description,
		},
	}, nil
}
```

### Step 6: Register in Wire DI

**File**: `cmd/<service>/wire.go`

Add your new providers to the Wire provider set:
```go
// Add NewExampleRepo and NewExampleUsecase to the ProviderSet
var providerSet = wire.NewSet(
	// ... existing providers
	data.NewExampleRepo,
	biz.NewExampleUsecase,
)
```

Then regenerate wire:
```bash
cd /home/user/microservices/<service>/cmd/<service> && wire
```

### Step 7: Register Routes in Server

**File**: `internal/server/http.go`

```go
// Ensure the service is registered on the HTTP server
pb.RegisterExampleServiceHTTPServer(httpSrv, exampleService)
```

**File**: `internal/server/grpc.go`

```go
// Ensure the service is registered on the gRPC server
pb.RegisterExampleServiceServer(grpcSrv, exampleService)
```

### Step 8: Build and Verify

```bash
cd /home/user/microservices/<service> && go build ./...
```

## HTTP Method Conventions

| Operation | HTTP Method | URL Pattern | Proto |
|-----------|-------------|-------------|-------|
| Create | POST | `/api/v1/<service>/<resources>` | `body: "*"` |
| Get | GET | `/api/v1/<service>/<resources>/{id}` | |
| List | GET | `/api/v1/<service>/<resources>` | query params |
| Update | PUT | `/api/v1/<service>/<resources>/{id}` | `body: "*"` |
| Delete | DELETE | `/api/v1/<service>/<resources>/{id}` | |
| Custom | POST | `/api/v1/<service>/<resources>/{id}/<action>` | `body: "*"` |

## Error Handling Pattern

Use Kratos errors:
```go
import "github.com/go-kratos/kratos/v2/errors"

// In biz layer
if example == nil {
    return nil, errors.NotFound("EXAMPLE_NOT_FOUND", "example not found: %s", id)
}

// In service layer  
if err != nil {
    return nil, err  // Kratos handles error conversion automatically
}
```

## Common Library Usage

Always check `common/` for existing utilities before writing custom code:
- `common/errors/` - Standard error codes
- `common/middleware/` - Auth, logging, tracing middleware
- `common/validation/` - Input validation helpers
- `common/utils/` - Pagination, string helpers, etc.

## Versioning & CHANGELOG

Ref: [Coding Standards §3](docs/07-development/standards/coding-standards.md)

When adding a new API endpoint, always consider the version impact:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New RPC method (backward compatible) | **MINOR** | Add `GetOrderHistory` RPC |
| New optional proto field | **MINOR** | Add `metadata` field to response |
| Remove/rename RPC or field | **MAJOR** | Rename `GetOrder` → `FetchOrder` |
| Change field type | **MAJOR** | `int64 user_id` → `string user_id` |
| Bug fix in existing endpoint | **PATCH** | Fix validation logic |

### After Adding API

1. **Update `CHANGELOG.md`** in the service root:
```markdown
## [Unreleased]
### Added
- New gRPC method `GetExample` with REST mapping `GET /api/v1/<service>/examples/{id}`
- New gRPC method `CreateExample` with REST mapping `POST /api/v1/<service>/examples`
```

2. **Breaking changes** → Create new API version package:
```
api/<service>/v2/  ← New version for breaking changes
```
- Do NOT reuse deleted proto field numbers; use `reserved`
- Keep `v1` available for backward compatibility during migration

3. **When ready to release**:
```bash
# Move [Unreleased] to version section in CHANGELOG.md
git commit -m "docs: update changelog for v1.3.0"
git tag -a v1.3.0 -m "v1.3.0: Add Example API endpoints

Added:
- GetExample RPC with REST GET /api/v1/<service>/examples/{id}
- CreateExample RPC with REST POST /api/v1/<service>/examples"
git push origin v1.3.0
```

## Checklist

- [ ] Proto file updated with new RPC and messages
- [ ] Proto code generated (`make api`)
- [ ] Domain entity created in `internal/biz/`
- [ ] Repository interface defined in `internal/biz/`
- [ ] Repository implemented in `internal/data/`
- [ ] Service method implemented in `internal/service/`
- [ ] Wire providers added and regenerated
- [ ] Routes registered in server
- [ ] Build passes (`go build ./...`)
- [ ] Database migration created (if new table/columns needed)
- [ ] **CHANGELOG.md updated** with new entries under `[Unreleased]`
- [ ] **Version impact assessed** (MAJOR/MINOR/PATCH)
- [ ] **No breaking changes** in current version (or new API version created)
