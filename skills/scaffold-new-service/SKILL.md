---
name: scaffold-new-service
description: Create a new Go microservice following the project's Kratos + Clean Architecture conventions
---

# Scaffold New Service Skill

Use this skill when creating a new microservice from scratch. This ensures it follows all established patterns.

## When to Use
- User wants to add a new service to the platform
- User wants to create service #20+ following conventions
- Starting a new bounded context

## Prerequisites
- Go 1.25+ installed
- Familiarity with existing service structure (see `navigate-service` skill)
- Port numbers allocated (see SERVICE_INDEX.md for used ports)

## Step 1: Choose Port Numbers

Check `docs/SERVICE_INDEX.md` for the next available ports.

| Service ID | HTTP Port | gRPC Port |
|------------|-----------|-----------|
| Current last: common-operations | 8019 | 9019 |
| **Next available** | **8020** | **9020** |

## Step 2: Create Service Directory Structure

```bash
SERVICE_NAME="<service-name>"  # lowercase, hyphenated (e.g., "gift-card")
MODULE_NAME="<module-name>"    # lowercase, no hyphens (e.g., "giftcard")

mkdir -p $SERVICE_NAME/{cmd/{$MODULE_NAME,migrate,worker},internal/{biz/$MODULE_NAME,data,service,server,config,constants,events,model},api/$MODULE_NAME/v1,migrations,configs}
```

## Step 3: Initialize Go Module

```bash
cd $SERVICE_NAME
go mod init gitlab.com/ta-microservices/$SERVICE_NAME
go get github.com/go-kratos/kratos/v2@latest
go get gitlab.com/ta-microservices/common@v1.10.0
go get google.golang.org/protobuf@latest
go get github.com/google/wire@latest
go get gorm.io/gorm@latest
go get gorm.io/driver/postgres@latest
```

## Step 4: Create Core Files

### 4.1 Main Entry Point (`cmd/<module>/main.go`)

```go
package main

import (
    "flag"
    "os"

    "github.com/go-kratos/kratos/v2"
    "github.com/go-kratos/kratos/v2/config"
    "github.com/go-kratos/kratos/v2/config/file"
    "github.com/go-kratos/kratos/v2/log"
    "github.com/go-kratos/kratos/v2/transport/grpc"
    "github.com/go-kratos/kratos/v2/transport/http"
)

var flagconf string

func init() {
    flag.StringVar(&flagconf, "conf", "../../configs", "config path, eg: -conf config.yaml")
}

func main() {
    flag.Parse()
    logger := log.With(log.NewStdLogger(os.Stdout),
        "ts", log.DefaultTimestamp,
        "caller", log.DefaultCaller,
        "service.name", "<SERVICE_NAME>",
    )

    // Wire injection
    app, cleanup, err := wireApp(flagconf, logger)
    if err != nil {
        panic(err)
    }
    defer cleanup()

    if err := app.Run(); err != nil {
        panic(err)
    }
}
```

### 4.2 Wire Dependency Injection (`cmd/<module>/wire.go`)

```go
//go:build wireinject

package main

import (
    "github.com/go-kratos/kratos/v2"
    "github.com/go-kratos/kratos/v2/log"
    "github.com/google/wire"

    "gitlab.com/ta-microservices/<service>/internal/data"
    "gitlab.com/ta-microservices/<service>/internal/events"
    "gitlab.com/ta-microservices/<service>/internal/server"
    "gitlab.com/ta-microservices/<service>/internal/service"
)

func wireApp(confPath string, logger log.Logger) (*kratos.App, func(), error) {
    panic(wire.Build(
        server.ProviderSet,
        data.ProviderSet,
        events.ProviderSet,
        service.ProviderSet,
        newApp,
    ))
}
```

### 4.3 Configuration (`configs/config.yaml`)

```yaml
app:
  name: <service-name>-service
  version: 1.0.0

server:
  http:
    addr: 0.0.0.0:<HTTP_PORT>
    timeout: 10s
  grpc:
    addr: 0.0.0.0:<GRPC_PORT>
    timeout: 10s

data:
  database:
    driver: postgres
    source: postgres://<service>_user:<service>_pass@localhost:5432/<service>_db?sslmode=disable
  redis:
    addr: localhost:6379
    db: 0
  eventbus:
    default_pubsub: pubsub-redis
```

### 4.4 Data Layer (`internal/data/data.go`)

Follow the pattern from existing services. Key providers:
- `NewDB` — GORM database connection
- `NewData` — Data layer wrapper
- `NewTransactionManager` — If the service needs transactions
- Repository providers for each entity

### 4.5 Biz Layer (`internal/biz/<entity>/`)

Follow Clean Architecture:
- Define domain entity structs
- Define repository interfaces
- Implement use case logic
- No infrastructure imports (no GORM, no Redis)

## Step 5: Create Proto Definitions

```protobuf
// api/<module>/v1/<module>.proto
syntax = "proto3";

package api.<module>.v1;

option go_package = "gitlab.com/ta-microservices/<service>/api/<module>/v1;<module>v1";

import "google/api/annotations.proto";

service <Module>Service {
  rpc Health(HealthRequest) returns (HealthReply) {
    option (google.api.http) = {
      get: "/api/v1/<module>/health"
    };
  }
}

message HealthRequest {}
message HealthReply {
  string status = 1;
}
```

## Step 6: Create Database Migration

```sql
-- migrations/001_initial_schema.sql
-- +goose Up
CREATE TABLE <entities> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- columns...
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Event idempotency table (standard for event consumers)
CREATE TABLE IF NOT EXISTS event_idempotency (
    event_id VARCHAR(255) PRIMARY KEY,
    topic VARCHAR(255),
    event_type VARCHAR(255),
    consumer_service VARCHAR(100),
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_duration_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Outbox table (standard for event publishers)
CREATE TABLE IF NOT EXISTS outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- +goose Down
DROP TABLE IF EXISTS outbox_events;
DROP TABLE IF EXISTS event_idempotency;
DROP TABLE IF EXISTS <entities>;
```

## Step 7: Create Dockerfile

```dockerfile
FROM golang:1.25-alpine AS builder
RUN apk add --no-cache git make
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app ./cmd/<module>/

FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /app /app
COPY configs /configs
EXPOSE <HTTP_PORT> <GRPC_PORT>
ENTRYPOINT ["/app", "-conf", "/configs/"]
```

## Step 8: Create GitOps Configuration

Use the `setup-gitops` skill to create:
- Kustomize base + overlays (dev, staging, prod)
- Deployment, Service, ConfigMap manifests
- ArgoCD Application resource

## Step 9: Verify

```bash
# Build
go build ./...

# Run tests
go test -v ./internal/biz/...

# Generate proto
make api

# Generate Wire
wire ./cmd/<module>/

# Run locally
make run
```

## Step 10: Register in Documentation

1. Add entry to `docs/SERVICE_INDEX.md`
2. Create service doc following `docs/templates/service-doc-template.md`
3. Update `navigate-service` skill with new port

## Common Patterns to Include

### Event Publishing (outbox pattern)
Use `common/outbox` — see `use-common-lib` skill

### Event Consuming (idempotency)
Use `common/idempotency` — see `use-common-lib` skill

### Service-to-Service Calls
Use gRPC clients — see `add-service-client` skill

### Database Migrations
Use Goose format — see `create-migration` skill
