---
description: Complex architectural decisions and multi-service changes - optimized for deep reasoning
---

# Architecture Planning Workflow

Use this workflow for **complex architectural changes** that require careful planning and affect multiple services or core patterns.

## When to Use

- Designing new microservices
- Changes affecting multiple services
- Major refactoring of core patterns
- Adding new infrastructure components
- Event flow redesign
- Database schema changes affecting multiple services
- Performance optimization requiring system-wide changes

## Approach

**Optimization**: Deep reasoning and system-wide impact analysis
- Comprehensive dependency analysis
- Consider all affected services
- Plan migrations and backward compatibility
- Document decisions and rationale

## Steps

1. **Understand the current state**
   - Use `service-map` skill to map current architecture
   - Use `trace-event-flow` for event-driven dependencies
   - Review existing architecture documentation
   - Identify all affected services and components

2. **Analyze requirements**
   - Define the business goal clearly
   - Identify non-functional requirements (performance, scalability, reliability)
   - List constraints (backward compatibility, zero-downtime deployment)
   - Consider alternative approaches

3. **Design the solution**
   - Sketch the proposed architecture
   - Define service boundaries and responsibilities
   - Plan event flows and gRPC interactions
   - Design database schema changes
   - Consider error handling and edge cases

4. **Impact analysis**
   - List all services that need changes
   - Identify breaking changes
   - Plan migration strategy
   - Consider rollback scenarios
   - Estimate effort and complexity

5. **Create implementation plan**
   - Break down into phases
   - Define dependencies between tasks
   - Identify risks and mitigation strategies
   - Plan testing strategy
   - Document in `docs/01-architecture/` if significant

6. **Review with stakeholders**
   - Present the plan clearly
   - Gather feedback on approach
   - Adjust based on business priorities
   - Get approval before execution

7. **Document decisions**
   - Create or update architecture documentation
   - Document rationale for key decisions
   - Update service map and diagrams
   - Add to knowledge base for future reference

## Skills to Use

- `service-map` - For understanding current architecture
- `trace-event-flow` - For event dependencies
- `navigate-service` - For each affected service
- `use-common-lib` - Check for reusable components

## Decision Framework

Consider these aspects:
- **Maintainability**: Will this be easy to understand and modify?
- **Scalability**: Can this handle 10x growth?
- **Reliability**: What happens when things fail?
- **Performance**: Does this meet latency/throughput requirements?
- **Security**: Are there new attack surfaces?
- **Cost**: Infrastructure and development cost

## Tips

- Think in terms of years, not months
- Prefer simple over clever
- Plan for failure scenarios
- Consider operational complexity
- Document the "why" not just the "what"
- Don't over-engineer - build what you need now, design for future extensibility
