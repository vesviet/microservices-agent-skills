---
description: Documentation updates and generation - optimized for clarity
---

# Quick Documentation Workflow

Use this workflow for **creating or updating documentation** with focus on clarity and consistency.

## When to Use

- Updating service README files
- Creating business domain documentation
- Updating API documentation
- Adding architecture diagrams
- Documenting new features
- Fixing outdated documentation

## Approach

**Optimization**: Clarity and consistency
- Follow existing documentation structure
- Maintain consistent formatting and tone
- Ensure cross-references are correct
- Use clear, concise language

## Steps

1. **Understand the documentation structure**
   - Review existing docs in the same category
   - Identify the target location (`docs/01-architecture`, `docs/02-business-domains`, or `docs/03-services`)
   - Note the existing format and style

2. **Gather information**
   - Use `navigate-service` to understand implementation details
   - Use `service-map` for dependency information
   - Review code comments and existing docs

3. **Write or update documentation**
   - Follow markdown best practices
   - Use headers, lists, and code blocks appropriately
   - Add links to related documentation
   - Include examples where helpful

4. **Ensure consistency**
   - Check documentation header format matches existing files
   - Verify port numbers match standards (see `docs/01-architecture/port-allocation.md`)
   - Update table of contents or index files if needed
   - Fix broken links

5. **Cross-reference validation**
   - Ensure links to other docs are correct
   - Update `docs/03-services/README.md` if adding new service docs
   - Add references in related business domain docs

## Documentation Structure

### Service Documentation (`docs/03-services/`)
```markdown
# [Service Name]

## Overview
Brief description and purpose

## Architecture
Clean Architecture layers

## API Endpoints
Document HTTP/gRPC APIs

## Events
Published and consumed events

## Configuration
Environment variables and settings

## Dependencies
Other services and external systems
```

### Business Domain Documentation (`docs/02-business-domains/`)
```markdown
# [Domain Name]

## Overview
Business context

## Key Concepts
Domain entities and rules

## Flows
Business process flows

## Services Involved
List of microservices in this domain
```

## Skills to Use

- `navigate-service` - For understanding implementation
- `service-map` - For quick-reference information

## Tips

- Write for someone new to the project
- Use diagrams for complex flows (Mermaid)
- Keep documentation close to code - update together
- Avoid duplicating information - link instead
- Use Vietnamese if business stakeholders prefer, English for technical docs
