---
name: navigate-service
description: Navigate and understand any microservice's structure, architecture layers, and key components
---

# Navigate Service Skill

Use this skill when the user asks to understand, explore, or navigate a specific microservice in this project.

## When to Use
- User asks "how does the X service work?"
- User wants to understand the architecture of a service
- User needs to find where specific logic is implemented
- User is unfamiliar with a service and needs orientation
- Before making changes to a service (to understand context first)

## Project Service Registry

All services follow the same **Clean Architecture + DDD** pattern built with the **Go Kratos Framework**.

### Service Directories (relative to `/home/user/microservices/`)
| Service | Directory | HTTP Port | gRPC Port |
|---------|-----------|-----------|-----------|
| Auth | `auth/` | 8000 | 9000 |
| User | `user/` | 8001 | 9001 |
| Pricing | `pricing/` | 8002 | 9002 |
| Customer | `customer/` | 8003 | 9003 |
| Order | `order/` | 8004 | 9004 |
| Payment | `payment/` | 8005 | 9005 |
| Warehouse | `warehouse/` | 8006 | 9006 |
| Location | `location/` | 8007 | 9007 |
| Fulfillment | `fulfillment/` | 8008 | 9008 |
| Notification | `notification/` | 8009 | 9009 |
| Checkout | `checkout/` | 8010 | 9010 |
| Promotion | `promotion/` | 8011 | 9011 |
| Shipping | `shipping/` | 8012 | 9012 |
| Return | `return/` | 8013 | 9013 |
| Loyalty | `loyalty-rewards/` | 8014 | 9014 |
| Catalog | `catalog/` | 8015 | 9015 |
| Review | `review/` | 8016 | 9016 |
| Search | `search/` | 8017 | 9017 |
| Analytics | `analytics/` | 8018 | 9018 |
| Common Ops | `common-operations/` | 8019 | 9019 |
| Gateway | `gateway/` | 80 | - |
| Admin | `admin/` | 3001 | - |
| Frontend | `frontend/` | 3000 | - |

## Standard Go Service Structure

Each Go microservice follows this directory layout:

```
<service>/
├── cmd/
│   ├── <service>/         # Main entry point (main.go, wire.go, wire_gen.go)
│   ├── migrate/           # Database migration CLI
│   └── worker/            # Background worker (if applicable)
├── api/
│   └── <service>/
│       └── v1/            # Proto definitions (.proto) and generated code (.pb.go)
├── internal/
│   ├── biz/               # 🔴 DOMAIN LAYER - Business logic, use cases, domain entities
│   │   ├── <entity>.go    # Domain entity + repository interface
│   │   └── <usecase>.go   # Business use case implementation
│   ├── data/              # 🟢 DATA LAYER - Repository implementations, database queries
│   │   ├── data.go        # Database connection setup
│   │   ├── <entity>.go    # Repository implementation (implements biz interfaces)
│   │   └── model/         # Database models (GORM structs)
│   ├── service/           # 🔵 API LAYER - gRPC/HTTP service implementation
│   │   └── <service>.go   # Translates API requests to biz calls
│   ├── server/            # Server configuration (HTTP, gRPC, middleware)
│   │   ├── http.go
│   │   ├── grpc.go
│   │   └── middleware.go
│   ├── client/            # gRPC clients to other services
│   ├── model/             # Shared models/DTOs
│   └── config/            # Configuration proto
├── configs/
│   └── config.yaml        # Service configuration
├── migrations/            # SQL migration files (Goose format)
├── Dockerfile
├── Makefile
├── .gitlab-ci.yml
├── go.mod
└── go.sum
```

## Step-by-Step Navigation Process

When asked to navigate/understand a service, follow these steps:

### Step 1: Identify the Service
Determine which service the user is asking about. Map their request to the service directory.

### Step 2: Read the Entry Point
```
View: cmd/<service>/main.go
```
This shows how the service is bootstrapped, what dependencies are injected via Wire.

### Step 3: Read the API Layer (Proto Definitions)
```
View: api/<service>/v1/*.proto
```
This defines all API endpoints (gRPC & HTTP), request/response messages.

### Step 4: Read the Domain Layer (Business Logic)
```
View: internal/biz/*.go
```
This is the MOST IMPORTANT layer. Contains:
- Domain entities and value objects
- Repository interfaces (contracts)
- Business use cases and rules

### Step 5: Read the Data Layer (Repository Implementations)
```
View: internal/data/*.go
```
Contains database queries, GORM models, and repository implementations.

### Step 6: Read the Service Layer (API Implementation)
```
View: internal/service/*.go
```
Translates gRPC/HTTP requests into domain calls.

### Step 7: Check Configuration
```
View: configs/config.yaml
```
Shows database connections, service ports, external dependencies.

### Step 8: Check Migrations
```
View: migrations/*.sql
```
Shows database schema and its evolution.

## Key Patterns to Explain

### Dependency Injection (Wire)
- `cmd/<service>/wire.go` defines the dependency graph
- `cmd/<service>/wire_gen.go` is auto-generated, never edit manually

### Event-Driven Communication
- Services publish/subscribe events via **Dapr PubSub** (Redis Streams)
- Event definitions: `common/events/` or in each service's `internal/biz/`
- Look for `PublishEvent`, `SubscribeEvent`, or Dapr pub/sub references

### Service-to-Service Communication
- Via gRPC clients in `internal/client/`
- Service discovery through Consul

### Common Library
- Shared utilities: `common/` (module: `gitlab.com/ta-microservices/common`)
- Includes: middleware, validation, errors, events, config, security, utils

## Output Format

When presenting a service overview, structure your response as:

1. **Service Purpose** - What business domain it handles
2. **API Endpoints** - Key endpoints from proto files
3. **Domain Entities** - Core entities and their relationships
4. **Business Rules** - Key use cases and rules
5. **Data Model** - Database schema (from migrations)
6. **Dependencies** - Other services it calls and infrastructure needs
7. **Event Integration** - Events published/subscribed
