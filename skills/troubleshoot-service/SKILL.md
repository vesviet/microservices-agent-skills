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
│   ├── Event/Dapr → Check Dapr sidecar logs
│   └── Elasticsearch → See ES section below
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

## Elasticsearch Issues (Search Service)

### Common ES Errors

#### `document_parsing_exception`
The document has a field that conflicts with the ES mapping.
- **Cause 1**: Dotted keys in Go maps (`doc["name.suggest"]`) get interpreted as nested paths by ES
- **Fix**: Remove dotted keys. ES auto-indexes multi-fields from the parent text field
- **Cause 2**: New field not in mapping with `dynamic: strict`
- **Fix**: Add field to `mapping.go` AND update live index mapping (see below)

#### `document_missing_exception`
The document doesn't exist in the target index.
- **Common cause**: Writing to wrong index (`products` vs `products_search` alias)
- All CRUD ops must use `GetIndexName("products_search")` (the alias)
- Only `CreateProductIndex` uses `GetIndexName("products")` (creates timestamped indexes)

#### `strict_dynamic_mapping_exception`
ES rejects documents with fields not defined in the mapping.
- **Fix**: Add field to `mapping.go` (`ProductIndexMapping`) AND update live mapping:
```bash
# Add new field to live ES index mapping
kubectl run es-curl --image=curlimages/curl --rm -it --restart=Never -n search-dev -- \
  curl -s -X PUT 'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_mapping' \
  -H 'Content-Type: application/json' \
  -d '{"properties":{"new_field":{"type":"boolean"}}}'
```

### ES Debugging Commands

```bash
# Check index alias mapping
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/_alias/products_search'

# Check document by ID
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_doc/<product_id>'

# Search by SKU
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_search?q=sku:<SKU>&size=1'

# Check mapping (verify field exists)
kubectl exec -n search-dev deploy/search -c search -- wget -qO- \
  'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_mapping'

# Bulk update field for all docs (use curl pod, since BusyBox wget doesn't support PUT)
kubectl run es-curl --image=curlimages/curl --rm -it --restart=Never -n search-dev -- \
  curl -s -X POST 'http://elasticsearch.argocd.svc.cluster.local:9200/products_search/_update_by_query?refresh=true' \
  -H 'Content-Type: application/json' \
  -d '{"script":{"source":"ctx._source.has_price = true","lang":"painless"},"query":{"match_all":{}}}'
```

### ES Index Architecture (Search Service)

```
products (base name)
├── products_20260213_101251 (created by sync job)
│   └── alias: products_search → points here
└── products_20260213_102147 (new sync creates new index)
    └── alias: products_search → switched here

All CRUD code → GetIndexName("products_search") → resolves to alias
Sync job → GetIndexName("products") + timestamp suffix → creates new index
```

### Product Visibility via `has_price`

Products are **only visible** in search when `has_price: true`:
- **Price update** → sets `has_price = true` (via `UpdateProduct` in price consumer)
- **Price delete** → checks if any `warehouse_stock` entries still have `base_price` > 0; if none → sets `has_price = false`
- **Search queries** → mandatory filter `{"term": {"has_price": true}}`
- **Sync job** → sets `HasPrice: true` for all indexed products (sync already skips no-price products)
