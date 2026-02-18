---
description: Writing comprehensive tests - optimized for coverage and reliability
---

// turbo-all

# Write Test Coverage Workflow

Use this workflow for **creating thorough unit and integration tests** following project testing patterns.

## When to Use

- Adding tests for new features
- Improving test coverage
- Writing integration tests
- Creating mock objects
- Refactoring with test safety
- TDD (Test-Driven Development)

## Approach

**Optimization**: Coverage and reliability
- Follow table-driven test patterns
- Use testify for assertions
- Create mocks (testify `mock.Mock` in `_test.go` or gomock generated mocks)
- Test both happy paths and edge cases

## Steps

1. **Read the write-tests skill first**
   - Run: `view_file d:\microservices\.agent\skills\write-tests\SKILL.md`
   - Understand patterns before writing any code

2. **Understand what to test**
   - Identify the component (delivery, biz, or data layer)
   - Determine test type needed (unit vs integration)
   - Review existing tests for patterns in the target service
   - Use `navigate-service` skill to understand code structure

3. **Check existing mocks**
   - Look for generated mocks in `internal/biz/<package>/mocks/`
   - Look for manual mocks in `internal/biz/mocks.go`
   - Reuse existing mocks when available

4. **Create mocks if needed**
   - For repo interfaces with many methods → use **gomock generated mocks** in `mocks/` subfolder
   - For simple interfaces → use **testify `mock.Mock`** in `_test.go` file
   - Mock MUST implement the full interface (compiler will catch missing methods)

5. **Write unit tests**
   - Test business logic in isolation
   - Mock external dependencies
   - Cover happy paths first
   - Add edge cases and error scenarios
   - Test input validation
   - Follow table-driven pattern:
   ```go
   func TestFunctionName(t *testing.T) {
       tests := []struct {
           name    string
           input   InputType
           want    OutputType
           wantErr bool
       }{
           {name: "success case", ...},
           {name: "error case", ...},
       }
       for _, tt := range tests {
           t.Run(tt.name, func(t *testing.T) {
               // Arrange → Act → Assert
           })
       }
   }
   ```

6. **Write integration tests if needed**
   - Test interactions between layers
   - Use real databases (with cleanup)
   - Test gRPC endpoints end-to-end
   - Test event publishing/consuming

7. **Run tests and verify**
   - Run tests:
   ```
   go test -v ./internal/biz/<package>/...
   ```
   - If tests fail → fix issues and re-run until all pass
   - Check coverage:
   ```
   go test -cover ./internal/biz/<package>/...
   ```
   - Run race detector:
   ```
   go test -race ./internal/biz/<package>/...
   ```

8. **Fix-and-rerun loop**
   - If any test fails, read the error output carefully
   - Fix the root cause (mock signature mismatch, wrong expectations, type errors)
   - Re-run the failing test:
   ```
   go test -v ./internal/biz/<package>/ -run TestFailingName
   ```
   - Repeat until all tests pass

9. **Review test quality**
   - Tests should be readable and maintainable
   - Test names clearly describe what's being tested
   - Avoid brittle tests that break on refactoring
   - Keep tests independent (no shared state)

## Test Organization

### Unit Tests
- Location: `internal/biz/<package>/*_test.go`
- Focus: Individual functions in isolation
- Mocks: testify or gomock for dependencies

### Integration Tests
- Location: Same as unit tests, but test multiple components
- Focus: Component interactions
- Database: Use test databases with proper cleanup

### Mock Objects
- gomock generated: `internal/biz/<package>/mocks/`
- testify manual: `*_test.go` in same package
- Keep mocks simple and focused

## Skills to Use

- `write-tests` - Primary skill with detailed patterns
- `navigate-service` - To understand code structure
- `use-common-lib` - Check for existing test utilities

## Tips

- Write tests as you write code, not after
- Test behavior, not implementation details
- Good test names serve as documentation
- If a test is hard to write, the code might need refactoring
- Aim for high coverage, but 100% is not always practical
- Mock at boundaries (external services, databases)
- Keep tests fast - slow tests won't be run
