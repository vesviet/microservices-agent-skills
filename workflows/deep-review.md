---
description: Thorough code review and analysis - optimized for quality
---

# Deep Review Workflow

Use this workflow for **comprehensive code review** that ensures quality, maintainability, and adherence to architecture patterns.

## When to Use

- Reviewing pull requests
- Auditing existing code quality
- Pre-merge validation
- Security and performance reviews
- Architecture compliance checks

## Approach

**Optimization**: Thoroughness and quality over speed
- Deep analysis of code patterns
- Cross-reference with architecture guidelines
- Check for potential issues and edge cases
- Consider system-wide impact

## Steps

1. **Understand the context**
   - Read the change description or PR description
   - Identify which service(s) are affected
   - Use `service-map` skill to understand dependencies

2. **Architecture compliance**
   - Verify Clean Architecture layers (delivery → biz → data)
   - Check Kratos framework patterns are followed
   - Ensure proper separation of concerns
   - Use `navigate-service` skill for structure verification

3. **Code quality review**
   - Use `review-code` skill for comprehensive checks
   - Verify error handling patterns
   - Check for proper logging
   - Review test coverage

4. **Cross-service impact**
   - If changes affect gRPC interfaces → check all clients
   - If changes affect events → use `trace-event-flow` skill
   - Review database migrations for breaking changes

5. **Security and performance**
   - Check for SQL injection, XSS, and security issues
   - Review database query efficiency
   - Check for N+1 query problems
   - Verify proper authorization checks

6. **Documentation**
   - Ensure code comments for complex logic
   - Check if service docs need updates
   - Verify API documentation is current

7. **Provide feedback**
   - Summarize findings by severity (critical, important, minor)
   - Suggest specific improvements with code examples
   - Highlight positive patterns worth keeping

## Skills to Use

- `review-code` - Primary skill for code review
- `service-map` - For dependency analysis
- `navigate-service` - For structure verification
- `trace-event-flow` - For event-driven changes
- `use-common-lib` - Check for code duplication

## Tips

- Take your time - thoroughness is the goal
- Don't just point out problems, suggest solutions
- Consider maintainability and future extensibility
- Balance perfectionism with pragmatism
