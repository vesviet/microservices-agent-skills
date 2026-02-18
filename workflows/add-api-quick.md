---
description: Adding new API endpoints efficiently - optimized for speed using patterns
---

# Add API Quick Workflow

Use this workflow for **quickly adding new HTTP or gRPC API endpoints** following established Kratos + Clean Architecture patterns.

## When to Use

- Adding new HTTP endpoints
- Adding new gRPC service methods
- Extending existing API functionality
- Creating CRUD operations
- Exposing business logic via APIs

## Approach

**Optimization**: Speed by following established patterns
- Leverage existing code patterns
- Use boilerplate generation where possible
- Follow Clean Architecture layers strictly
- Minimal deviation from conventions

## Steps

1. **Use the add-api-endpoint skill**
   - Primary skill: `add-api-endpoint`
   - Follows Kratos + Clean Architecture patterns
   - Covers HTTP and gRPC endpoints
   - Includes all required layers

2. **Define the API contract**
   - For HTTP: Define path, method, request/response structures
   - For gRPC: Define service and method in `.proto` file
   - Consider versioning (e.g., `/v1/...`)
   - Follow REST conventions if applicable

3. **Implement in layers (bottom-up)**

   **Data Layer** (`internal/data/`)
   - Create repository interface if needed
   - Implement data access logic
   - Handle database operations
   
   **Business Layer** (`internal/biz/`)
   - Define use case interface
   - Implement business logic
   - Handle business rules and validation
   
   **Delivery Layer** (`internal/delivery/http/` or `internal/delivery/grpc/`)
   - Create handler/controller
   - Define routes/service methods
   - Handle request/response mapping
   - Input validation

4. **Wire dependencies**
   - Update `internal/server/wire.go` (wire providers)
   - Update `cmd/server/wire_gen.go` if needed (or run wire)
   - Ensure dependency injection is correct

5. **Add validation**
   - Validate input in delivery layer
   - Return appropriate error codes
   - Use common validation utilities

6. **Add error handling**
   - Return proper HTTP status codes or gRPC status
   - Use structured error responses
   - Log errors appropriately

7. **Test the endpoint**
   - Build the service
   - Run locally
   - Test with curl (HTTP) or grpcurl (gRPC)
   - Verify response format and status codes

8. **Write tests**
   - Unit tests for business logic
   - Integration tests for the endpoint
   - Use `write-tests` skill patterns

9. **Update documentation**
   - Add to service README
   - Document request/response schemas
   - Add usage examples if complex

## Quick Reference

### HTTP Endpoint Structure
```
internal/delivery/http/
  └── handler.go         # HTTP handlers
internal/biz/
  └── usecase.go         # Business logic
  └── usecase_test.go    # Unit tests
internal/data/
  └── repository.go      # Data access
```

### gRPC Service Structure
```
api/
  └── service/v1/
      └── service.proto  # Proto definitions
internal/delivery/grpc/
  └── service.go         # gRPC service impl
internal/biz/
  └── usecase.go         # Business logic
internal/data/
  └── repository.go      # Data access
```

## Skills to Use

- `add-api-endpoint` - Primary skill with detailed patterns
- `navigate-service` - To understand existing structure
- `write-tests` - For test creation
- `use-common-lib` - Check for reusable validators, converters

## Tips

- Copy-paste from similar existing endpoints
- Follow the exact layer separation pattern
- Don't put business logic in handlers
- Use middleware for cross-cutting concerns (auth, logging)
- Version your APIs from day one
- Keep request/response DTOs separate from domain models
- Return consistent error formats
