---
name: troubleshoot-service
description: Troubleshoot common service issues - build errors, runtime crashes, connection failures, and configuration problems
---

# Troubleshoot Service Skill

## When to Use
- Service fails to build, crashes on startup, or has connection failures
- Proto/Wire generation errors, config mismatches

## Diagnostic Decision Tree

```
Service Issue
├── Build Error?
│   ├── Proto → Check protoc tools, third_party dir
│   ├── Go compile → Check imports, go mod tidy
│   └── Wire → Check provider set, interfaces
├── Startup Crash?
│   ├── DB connection → Check credentials, DB exists, PostgreSQL running
│   ├── Redis → Check Redis running (docker-compose up -d redis)
│   ├── Consul → Check Consul running (docker-compose up -d consul)
│   └── Port in use → lsof -i :PORT, kill process
├── Runtime Error?
│   ├── Migration → Check SQL syntax, -- +goose Up annotations
│   ├── Data layer → Check GORM model matches DB schema
│   └── Event/Dapr → Check Dapr sidecar logs
└── K8s Issue? → Use debug-k8s skill
```

## Common Fixes

### Proto Generation (`make api`)
```bash
# Install tools
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest

# Copy third_party if missing
cp -r /home/user/microservices/user/third_party /home/user/microservices/<service>/
```

### Wire Generation
```bash
cd /home/user/microservices/<service>/cmd/<service> && wire
# Common issues: missing provider, circular deps, interface not satisfied
```

### Database Connection
```bash
# Check config
cat /home/user/microservices/<service>/configs/config.yaml | grep -A5 database

# Create DB if missing
psql -h localhost -U ecommerce_user -d postgres -c "CREATE DATABASE <service>_db;"
```

### Run Migrations
```bash
DATABASE_URL="postgres://ecommerce_user:ecommerce_pass@localhost:5432/<service>_db?sslmode=disable" \
  make migrate-up
```

### Start Infrastructure
```bash
docker-compose up -d postgres redis consul
```

### Build & Run Service
```bash
cd /home/user/microservices/<service>
go mod tidy
go build ./...
go run ./cmd/<service>/...  # or: kratos run
```

## Config.yaml Standard Structure
```yaml
server:
  http:
    addr: 0.0.0.0:80XX
  grpc:
    addr: 0.0.0.0:90XX
data:
  database:
    driver: postgres
    source: postgres://user:pass@localhost:5432/<service>_db?sslmode=disable
  redis:
    addr: localhost:6379
consul:
  address: localhost:8500
```

## Quick Health Check
```bash
echo "=== PostgreSQL ===" && psql -h localhost -U ecommerce_user -d postgres -c "SELECT 1" 2>&1 | tail -1
echo "=== Redis ===" && redis-cli ping
echo "=== Consul ===" && curl -s http://localhost:8500/v1/status/leader
```
