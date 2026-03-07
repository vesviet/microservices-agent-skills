---
description: Workflow for setting up a new microservice from scratch
---

## Setup New Service Workflow

This workflow guides you through creating a new microservice in the project.

### Prerequisites
- Service name decided (e.g., `inventory`, `recommendation`)
- Service purpose clearly defined
- Port allocation determined (check PORT_ALLOCATION_STANDARD.md)
- Database requirements identified

### Workflow Steps

#### Phase 1: Planning

**1.1 Define Service Scope**

Answer these questions:
- What is the business domain?
- What are the main responsibilities?
- What APIs will it expose?
- What data will it manage?
- What events will it publish/consume?
- What other services will it call?

**1.2 Check Port Allocation**

```bash
# Check available ports
cat /home/user/microservices/gitops/docs/PORT_ALLOCATION_STANDARD.md

# Reserve ports for new service
# HTTP: 80XX
# gRPC: 90XX
```

**1.3 Determine Service Group**

- **core-services**: Core business logic (order, catalog, customer, payment, auth, user)
- **operational-services**: Supporting operations (notification, analytics, search, review, warehouse, fulfillment, shipping, pricing, promotion, loyalty-rewards, location)
- **platform-services**: Infrastructure (gateway, common-operations)

#### Phase 2: Create Service Structure

**2.1 Clone Template or Copy Existing Service**

```bash
cd /home/user/microservices

# Option 1: Copy similar service
cp -r user <new-service>
cd <new-service>

# Clean up
rm -rf .git bin/ vendor/
find . -name "*.pb.go" -delete
find . -name "wire_gen.go" -delete
```

**2.2 Update Module Name**

```bash
# Update go.mod
vim go.mod
# Change: module gitlab.com/ta-microservices/<new-service>

# Update all imports
find . -type f -name "*.go" -exec sed -i 's/gitlab.com\/ta-microservices\/user/gitlab.com\/ta-microservices\/<new-service>/g' {} +
```

**2.3 Create Directory Structure**

```bash
mkdir -p api/<new-service>/v1
mkdir -p cmd/<new-service>
mkdir -p cmd/worker
mkdir -p internal/biz
mkdir -p internal/data
mkdir -p internal/service
mkdir -p internal/client
mkdir -p internal/events
mkdir -p internal/worker
mkdir -p internal/constants
mkdir -p internal/server
mkdir -p internal/middleware
mkdir -p configs
mkdir -p migrations
mkdir -p dapr
mkdir -p k8s
mkdir -p docs
```

#### Phase 3: Define API Contract

**3.1 Create Proto File**

```bash
vim api/<new-service>/v1/<new-service>.proto
```

```protobuf
syntax = "proto3";

package api.<new-service>.v1;

option go_package = "gitlab.com/ta-microservices/<new-service>/api/<new-service>/v1;v1";

import "google/api/annotations.proto";
import "google/protobuf/empty.proto";

service <NewService>Service {
  rpc Create<Entity> (Create<Entity>Request) returns (Create<Entity>Reply) {
    option (google.api.http) = {
      post: "/api/v1/<new-service>/<entities>"
      body: "*"
    };
  }

  rpc Get<Entity> (Get<Entity>Request) returns (Get<Entity>Reply) {
    option (google.api.http) = {
      get: "/api/v1/<new-service>/<entities>/{id}"
    };
  }

  rpc List<Entities> (List<Entities>Request) returns (List<Entities>Reply) {
    option (google.api.http) = {
      get: "/api/v1/<new-service>/<entities>"
    };
  }
}

message Create<Entity>Request {
  string name = 1;
  string description = 2;
}

message Create<Entity>Reply {
  <Entity>Data data = 1;
}

message Get<Entity>Request {
  string id = 1;
}

message Get<Entity>Reply {
  <Entity>Data data = 1;
}

message List<Entities>Request {
  int32 page = 1;
  int32 page_size = 2;
}

message List<Entities>Reply {
  repeated <Entity>Data items = 1;
  int32 total = 2;
}

message <Entity>Data {
  string id = 1;
  string name = 2;
  string description = 3;
  string created_at = 4;
  string updated_at = 5;
}
```

**3.2 Create Makefile**

```bash
vim Makefile
```

```makefile
.PHONY: api build run test migrate-up migrate-down

api:
	protoc --proto_path=. \
		--proto_path=./third_party \
		--go_out=paths=source_relative:. \
		--go-grpc_out=paths=source_relative:. \
		--go-http_out=paths=source_relative:. \
		api/<new-service>/v1/*.proto

build:
	go build -o bin/<new-service> ./cmd/<new-service>
	go build -o bin/worker ./cmd/worker

run:
	go run ./cmd/<new-service>

test:
	go test ./... -v

migrate-up:
	goose -dir migrations postgres "$(DATABASE_URL)" up

migrate-down:
	goose -dir migrations postgres "$(DATABASE_URL)" down
```

**3.3 Generate Proto Code**

```bash
# Copy third_party
cp -r /home/user/microservices/user/third_party .

# Generate
make api
```

#### Phase 4: Implement Core Layers

**4.1 Create Domain Entity (Biz Layer)**

```bash
vim internal/biz/<entity>.go
```

Use skill: `service-structure` for reference

**4.2 Create Repository (Data Layer)**

```bash
vim internal/data/<entity>.go
```

**4.3 Create Service Handler (Service Layer)**

```bash
vim internal/service/<new-service>.go
```

**4.4 Setup Dependency Injection (Wire)**

```bash
vim cmd/<new-service>/wire.go
```

```go
//go:build wireinject
// +build wireinject

package main

import (
	"github.com/go-kratos/kratos/v2"
	"github.com/google/wire"
	"gitlab.com/ta-microservices/<new-service>/internal/biz"
	"gitlab.com/ta-microservices/<new-service>/internal/data"
	"gitlab.com/ta-microservices/<new-service>/internal/server"
	"gitlab.com/ta-microservices/<new-service>/internal/service"
)

func wireApp(*conf.Server, *conf.Data, log.Logger) (*kratos.App, func(), error) {
	panic(wire.Build(
		server.ProviderSet,
		data.ProviderSet,
		biz.ProviderSet,
		service.ProviderSet,
		newApp,
	))
}
```

**4.5 Generate Wire**

```bash
cd cmd/<new-service> && wire
cd ../worker && wire  # if worker exists
```

#### Phase 5: Database Setup

**5.1 Create Initial Migration**

```bash
cd /home/user/microservices/<new-service>
make migration name=create_initial_tables
```

**5.2 Write Migration SQL**

```bash
vim migrations/<timestamp>_create_initial_tables.sql
```

```sql
-- +goose Up
CREATE TABLE IF NOT EXISTS <entities> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_<entities>_deleted_at ON <entities>(deleted_at);

-- +goose Down
DROP TABLE IF EXISTS <entities>;
```

**5.3 Create Database**

```bash
psql -h localhost -U ecommerce_user -d postgres -c "CREATE DATABASE <new-service>_db;"
```

**5.4 Run Migration**

```bash
DATABASE_URL="postgres://ecommerce_user:ecommerce_pass@localhost:5432/<new-service>_db?sslmode=disable" \
  make migrate-up
```

#### Phase 6: Configuration

**6.1 Create Config File**

```bash
vim configs/config.yaml
```

```yaml
server:
  http:
    addr: 0.0.0.0:80XX  # Use allocated port
    timeout: 30s
  grpc:
    addr: 0.0.0.0:90XX  # Use allocated port
    timeout: 30s

data:
  database:
    driver: postgres
    source: postgres://ecommerce_user:ecommerce_pass@localhost:5432/<new-service>_db?sslmode=disable
  redis:
    addr: localhost:6379
    read_timeout: 0.2s
    write_timeout: 0.2s

consul:
  address: localhost:8500
  scheme: http

log:
  level: info
  format: json
```

**6.2 Create .env File**

```bash
vim .env
```

```bash
DATABASE_URL=postgres://ecommerce_user:ecommerce_pass@localhost:5432/<new-service>_db?sslmode=disable
REDIS_ADDR=localhost:6379
CONSUL_ADDR=localhost:8500
```

#### Phase 7: GitOps Setup

Use skill: `setup-gitops`

**7.1 Create GitOps Structure**

```bash
cd /home/user/microservices/gitops
mkdir -p apps/<new-service>/base
mkdir -p apps/<new-service>/overlays/dev
mkdir -p apps/<new-service>/overlays/staging
mkdir -p apps/<new-service>/overlays/production
```

**7.2 Create Base Manifests**

```bash
# deployment.yaml
vim apps/<new-service>/base/deployment.yaml

# service.yaml
vim apps/<new-service>/base/service.yaml

# configmap.yaml
vim apps/<new-service>/base/configmap.yaml

# hpa.yaml
vim apps/<new-service>/base/hpa.yaml

# kustomization.yaml
vim apps/<new-service>/base/kustomization.yaml
```

**7.3 Update Port Allocation Document**

```bash
vim docs/PORT_ALLOCATION_STANDARD.md
```

Add entry for new service with allocated ports.

#### Phase 8: Documentation

**8.1 Create Service Documentation**

```bash
vim /home/user/microservices/docs/03-services/<group>/<new-service>-service.md
```

Use template from existing service docs.

**8.2 Create README.md**

```bash
vim README.md
```

Use template: `docs/templates/readme-template.md`

**8.3 Create CHANGELOG.md**

```bash
vim CHANGELOG.md
```

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial service setup
- Basic CRUD operations for <entity>
- Database migrations
- API documentation
```

#### Phase 9: Testing

**9.1 Write Unit Tests**

Use skill: `write-tests`

```bash
# Test biz layer
vim internal/biz/<entity>_test.go

# Test service layer
vim internal/service/<new-service>_test.go

# Test data layer
vim internal/data/<entity>_test.go
```

**9.2 Run Tests**

```bash
go test ./... -v
```

#### Phase 10: Build & Verify

**10.1 Lint**

```bash
golangci-lint run
```

**10.2 Build**

```bash
go build ./...
```

**10.3 Run Locally**

```bash
# Start infrastructure
docker-compose up -d postgres redis consul

# Run service
go run ./cmd/<new-service>/...
```

**10.4 Test Endpoints**

```bash
# Health check
curl http://localhost:80XX/health/live

# Create entity
curl -X POST http://localhost:80XX/api/v1/<new-service>/<entities> \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test entity"}'

# Get entity
curl http://localhost:80XX/api/v1/<new-service>/<entities>/<id>

# List entities
curl http://localhost:80XX/api/v1/<new-service>/<entities>
```

#### Phase 11: Initial Commit

**11.1 Initialize Git**

```bash
cd /home/user/microservices/<new-service>
git init
git remote add origin git@gitlab.com:ta-microservices/<new-service>.git
```

**11.2 Create .gitignore**

```bash
vim .gitignore
```

```
bin/
vendor/
*.log
.env
.DS_Store
coverage.out
```

**11.3 Commit**

```bash
rm -rf bin/
git add -A
git commit -m "feat(<new-service>): initial service setup

- Created service structure
- Implemented basic CRUD operations
- Added database migrations
- Configured GitOps manifests
- Added documentation"

git push -u origin main
```

#### Phase 12: Deploy

**12.1 Create CI/CD Pipeline**

```bash
vim .gitlab-ci.yml
```

Copy from existing service and update service name.

**12.2 Push and Deploy**

```bash
git push origin main
```

**12.3 Verify Deployment**

```bash
# Wait for CI/CD
cd /home/user/microservices/gitops && git pull origin main
cat apps/<new-service>/base/kustomization.yaml | grep newTag

# Check pods
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl get pods -n <new-service>-dev"

# Check logs
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <new-service>-dev -l app=<new-service> --tail=50"
```

### Checklist

- [ ] Service name and purpose defined
- [ ] Ports allocated (HTTP: 80XX, gRPC: 90XX)
- [ ] Service group determined
- [ ] Directory structure created
- [ ] Proto file created and generated
- [ ] Makefile created
- [ ] Domain entity implemented (biz layer)
- [ ] Repository implemented (data layer)
- [ ] Service handler implemented (service layer)
- [ ] Wire DI configured and generated
- [ ] Database created
- [ ] Initial migration created and run
- [ ] Config file created
- [ ] .env file created
- [ ] GitOps manifests created
- [ ] Port allocation document updated
- [ ] Service documentation created
- [ ] README.md created
- [ ] CHANGELOG.md created
- [ ] Unit tests written
- [ ] Lint passed (0 warnings)
- [ ] Build successful
- [ ] Local testing passed
- [ ] .gitignore created
- [ ] Git initialized and remote added
- [ ] Initial commit made
- [ ] CI/CD pipeline configured
- [ ] Deployed to dev environment
- [ ] Deployment verified

### Related Workflows
- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)
- [Build & Deploy](build-deploy.md)

### Related Skills
- service-structure
- add-api-endpoint
- create-migration
- setup-gitops
- write-tests
- commit-code
