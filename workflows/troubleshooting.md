---
description: Workflow for troubleshooting common service issues
---

## Troubleshooting Workflow

This workflow helps you diagnose and fix common issues with microservices.

### Quick Diagnostic Tree

```
Service Issue?
├── Build Error?
│   ├── Proto generation → See Proto Issues
│   ├── Go compile error → See Compile Issues
│   └── Wire generation → See Wire Issues
├── Startup Crash?
│   ├── Database connection → See Database Issues
│   ├── Redis connection → See Redis Issues
│   ├── Consul connection → See Consul Issues
│   └── Port already in use → See Port Issues
├── Runtime Error?
│   ├── Migration failed → See Migration Issues
│   ├── Data layer error → See Data Issues
│   ├── Event/Dapr error → See Event Issues
│   └── Elasticsearch error → See ES Issues
└── Kubernetes Issue?
    └── Use debug-k8s skill
```

### Common Issues & Solutions

#### Proto Generation Issues

**Symptom**: `make api` fails

**Diagnosis**:
```bash
# Check if proto tools are installed
which protoc-gen-go
which protoc-gen-go-grpc
which protoc-gen-go-http
```

**Solution**:
```bash
# Install proto tools
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest

# Copy third_party if missing
cp -r /home/user/microservices/user/third_party /home/user/microservices/<service>/

# Regenerate
cd /home/user/microservices/<service> && make api
```

#### Go Compile Issues

**Symptom**: `go build ./...` fails

**Diagnosis**:
```bash
# Check for import errors
go build ./... 2>&1 | grep "cannot find package"

# Check go.mod
cat go.mod | grep replace
```

**Solution**:
```bash
# Clean and rebuild
go clean -cache
go mod tidy
go build ./...

# If replace directives exist, remove them
# Then get latest versions
go get gitlab.com/ta-microservices/common@latest
go mod tidy
```

#### Wire Generation Issues

**Symptom**: `wire` command fails

**Diagnosis**:
```bash
cd cmd/<service>
wire 2>&1 | grep -E "no provider|unused provider|cycle"
```

**Common causes**:
- Missing provider in provider set
- Circular dependency
- Interface not satisfied
- Unused provider

**Solution**:
```bash
# Check wire.go
cat cmd/<service>/wire.go

# Ensure all dependencies have providers
# Example fix: Add missing provider
# var providerSet = wire.NewSet(
#     data.NewData,
#     data.NewExampleRepo,  ← Add this if missing
#     biz.NewExampleUsecase,
# )

# Regenerate
cd cmd/<service> && wire
```

#### Database Connection Issues

**Symptom**: Service crashes with "connection refused" or "database does not exist"

**Diagnosis**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check database exists
psql -h localhost -U ecommerce_user -d postgres -c "\l" | grep <service>_db

# Check config
cat configs/config.yaml | grep -A5 database
```

**Solution**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Create database if missing
psql -h localhost -U ecommerce_user -d postgres -c "CREATE DATABASE <service>_db;"

# Test connection
psql -h localhost -U ecommerce_user -d <service>_db -c "SELECT 1"

# Run migrations
DATABASE_URL="postgres://ecommerce_user:ecommerce_pass@localhost:5432/<service>_db?sslmode=disable" \
  make migrate-up
```

#### Redis Connection Issues

**Symptom**: Service crashes with "connection refused" to Redis

**Diagnosis**:
```bash
# Check if Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
```

**Solution**:
```bash
# Start Redis
docker-compose up -d redis

# Test connection
redis-cli ping
# Should return: PONG
```

#### Consul Connection Issues

**Symptom**: Service can't register with Consul

**Diagnosis**:
```bash
# Check if Consul is running
docker ps | grep consul

# Check Consul status
curl -s http://localhost:8500/v1/status/leader
```

**Solution**:
```bash
# Start Consul
docker-compose up -d consul

# Verify Consul is healthy
curl http://localhost:8500/v1/status/leader
```

#### Port Already in Use

**Symptom**: Service fails to start with "address already in use"

**Diagnosis**:
```bash
# Find process using the port
lsof -i :8080  # Replace with your port
```

**Solution**:
```bash
# Kill the process
kill -9 <PID>

# Or use a different port in config.yaml
vim configs/config.yaml
# Change server.http.addr or server.grpc.addr
```

#### Migration Issues

**Symptom**: Migration fails with SQL syntax error

**Diagnosis**:
```bash
# Check migration file
cat migrations/<timestamp>_<name>.sql

# Check migration status
DATABASE_URL="postgres://ecommerce_user:ecommerce_pass@localhost:5432/<service>_db?sslmode=disable" \
  goose -dir migrations status
```

**Common causes**:
- Missing `-- +goose Up` annotation
- SQL syntax error
- Constraint violation
- Missing dependency (table/column)

**Solution**:
```bash
# Fix migration file
vim migrations/<timestamp>_<name>.sql

# Ensure proper annotations:
# -- +goose Up
# CREATE TABLE ...
#
# -- +goose Down
# DROP TABLE ...

# Rollback if needed
DATABASE_URL="..." make migrate-down

# Re-run migration
DATABASE_URL="..." make migrate-up
```

#### Data Layer Issues

**Symptom**: Runtime error in data layer (GORM errors)

**Diagnosis**:
```bash
# Check GORM model matches DB schema
# Compare model struct with migration

# Check for N+1 queries
grep -r "\.Find\|\.First" internal/data/ --include='*.go'
```

**Common causes**:
- Model doesn't match schema
- N+1 query problem
- Missing transaction
- Wrong query

**Solution**:
```bash
# Use Preload for related data
# BAD:
# for _, order := range orders {
#     db.First(&order.Customer, order.CustomerID)
# }

# GOOD:
# db.Preload("Customer").Find(&orders)

# Use transactions for multi-write
# db.Transaction(func(tx *gorm.DB) error {
#     // Multiple writes here
#     return nil
# })
```

#### Event/Dapr Issues

**Symptom**: Events not being published or consumed

**Diagnosis**:
```bash
# Check Dapr sidecar logs
kubectl logs -n <service>-dev <pod-name> -c daprd

# Check subscription file
cat dapr/subscription.yaml

# Check event publishing code
grep -r "PublishEvent" internal/ --include='*.go'
```

**Solution**:
```bash
# Verify Dapr annotations in deployment
grep -A3 "dapr.io" gitops/apps/<service>/base/deployment.yaml

# Should have:
# dapr.io/enabled: "true"
# dapr.io/app-id: "<service>"
# dapr.io/app-port: "8080"
# dapr.io/app-protocol: "grpc"

# Check topic name matches
# Publisher: common.PublishEvent(ctx, constants.TopicOrderCreated, event)
# Subscriber: dapr/subscription.yaml topic: order-created
```

#### Elasticsearch Issues (Search Service)

**Symptom**: `document_parsing_exception` or `document_missing_exception`

**Diagnosis**:
```bash
# Check index exists
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/_cat/indices?v'

# Check document
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_doc/<id>'
```

**Common causes**:
- Dotted keys in document (e.g., `name.suggest`)
- Field not in mapping
- Wrong index name
- Strict dynamic mapping

**Solution**:
```bash
# Remove dotted keys from document
# ES auto-indexes multi-fields

# Add field to mapping
kubectl run es-curl --image=curlimages/curl --rm -it --restart=Never -n search-dev -- \
  curl -s -X PUT 'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_mapping' \
  -H 'Content-Type: application/json' \
  -d '{"properties":{"new_field":{"type":"boolean"}}}'

# Use correct index (alias)
# Always use GetIndexName("products_search") for CRUD
```

### Systematic Troubleshooting Process

#### Step 1: Identify the Issue

**Collect information**:
- What is the error message?
- When does it occur? (build, startup, runtime)
- What changed recently?
- Can you reproduce it?

#### Step 2: Check Logs

**Local development**:
```bash
# Service logs
cd /home/user/microservices/<service>
go run ./cmd/<service>/... 2>&1 | tee service.log
```

**Kubernetes**:
```bash
# Pod logs
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <service>-dev -l app=<service> --tail=100"

# Dapr sidecar logs
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <service>-dev <pod-name> -c daprd --tail=100"
```

#### Step 3: Check Configuration

```bash
# Service config
cat configs/config.yaml

# GitOps config
cat gitops/apps/<service>/base/configmap.yaml
cat gitops/apps/<service>/base/deployment.yaml

# Environment variables
env | grep -i <service>
```

#### Step 4: Check Dependencies

```bash
# Database
psql -h localhost -U ecommerce_user -d <service>_db -c "SELECT 1"

# Redis
redis-cli ping

# Consul
curl http://localhost:8500/v1/status/leader

# Other services
curl http://<other-service>:8080/health/live
```

#### Step 5: Verify Code

```bash
# Lint
golangci-lint run

# Build
go build ./...

# Test
go test ./...

# Check for common issues
grep -r "TODO\|FIXME\|XXX" internal/ --include='*.go'
```

#### Step 6: Check Recent Changes

```bash
# Recent commits
git log --oneline -10

# Diff with last working version
git diff <last-working-commit> HEAD

# Check if common changed
cd /home/user/microservices/common && git log --oneline -5
```

#### Step 7: Isolate the Problem

**Test components individually**:
```bash
# Test database connection only
go test ./internal/data/... -v

# Test business logic only
go test ./internal/biz/... -v

# Test service layer only
go test ./internal/service/... -v
```

#### Step 8: Fix and Verify

```bash
# Make fix
vim internal/<layer>/<file>.go

# Test fix
go test ./internal/<layer>/... -v

# Build
go build ./...

# Run locally
go run ./cmd/<service>/...
```

### Quick Health Check Script

```bash
#!/bin/bash
echo "=== PostgreSQL ==="
psql -h localhost -U ecommerce_user -d postgres -c "SELECT 1" 2>&1 | tail -1

echo "=== Redis ==="
redis-cli ping

echo "=== Consul ==="
curl -s http://localhost:8500/v1/status/leader

echo "=== Service Build ==="
cd /home/user/microservices/<service> && go build ./... && echo "✅ Build OK" || echo "❌ Build Failed"

echo "=== Service Tests ==="
cd /home/user/microservices/<service> && go test ./... && echo "✅ Tests OK" || echo "❌ Tests Failed"
```

### When to Escalate

Escalate to senior developer or tech lead if:
- Issue persists after trying all solutions
- Issue affects multiple services
- Issue is in production
- Issue requires infrastructure changes
- Issue requires breaking changes

### Related Workflows
- [Build & Deploy](build-deploy.md)
- [Service Review & Release](service-review-release.md)

### Related Skills
- troubleshoot-service
- debug-k8s
- navigate-service
