---
trigger: always_on
glob:
description: Enforce test-writing standards across all microservices
---

## Test Writing Rules

When writing or modifying test files (`*_test.go`), ALWAYS follow these rules:

### Framework & Assertions
- Use `testify/assert` and `testify/require` — NEVER raw `if err != nil { t.Fatal() }` checks
- Use `require` for fatal preconditions, `assert` for non-fatal checks

### Test Structure
- Use **table-driven tests** (`tests := []struct{}`) for multiple scenarios
- Test naming convention: `TestFunctionName_Scenario` (e.g., `TestCreateOrder_EmptyItems`)
- Arrange → Act → Assert pattern in every test

### Mocks
- **testify mocks** (`mock.Mock`) in `*_test.go` for simple cases
- **gomock generated mocks** in `internal/biz/<package>/mocks/` for complex interfaces (preferred for repo mocks)
- Mock MUST implement the **full interface** — compile will catch missing methods
- Always call `mock.AssertExpectations(t)` (testify) or `defer ctrl.Finish()` (gomock)

### Coverage Requirements
- Test happy paths first, then error cases and edge cases
- Cover: validation errors, not-found, DB errors, permission errors
- Test boundary conditions (nil, empty, zero values)

### Execution (MANDATORY)
- After writing tests, ALWAYS run: `go test -v ./internal/biz/<package>/...`
- If tests fail, fix and re-run until all pass
- Run coverage check: `go test -cover ./internal/biz/<package>/...`

### Auto-Run Commands (MANDATORY)
- ALL `go test` commands MUST use `SafeToAutoRun: true` — do NOT ask for user confirmation
- This includes: `go test -v`, `go test -cover`, `go test -race`, `go test -run`
- `go test` is a read-only operation, it is ALWAYS safe to auto-run
