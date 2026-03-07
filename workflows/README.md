# Agent Workflows

This directory contains comprehensive workflows for common development tasks in the microservices project.

## Available Workflows

### 1. [Build & Deploy](build-deploy.md)
**When to use**: Deploy code changes to development/staging/production

**Key steps**:
- Make code changes
- Run tests and build
- Commit with conventional format
- Push (CI/CD builds and deploys automatically)
- Verify deployment

**Time**: 10-15 minutes

---

### 2. [Add New Feature](add-new-feature.md)
**When to use**: Implement a new feature from design to deployment

**Key steps**:
- Design phase (requirements, API contract)
- Implementation (proto, business logic, data layer)
- Testing (unit tests, coverage check)
- Quality check (lint, build, wire)
- Documentation (CHANGELOG, README, service doc)
- Review and commit
- Deploy and verify

**Time**: 2-8 hours (depending on complexity)

---

### 3. [Service Review & Release](service-review-release.md)
**When to use**: Review entire service for production readiness

**Key steps**:
- Sync latest code
- Index and review codebase
- Cross-service impact analysis
- Bug fixes and improvements
- Test coverage check
- Dependencies update
- Build and quality checks
- Deployment readiness verification
- Documentation updates
- Commit, tag, and release

**Time**: 4-8 hours

---

### 4. [Troubleshooting](troubleshooting.md)
**When to use**: Diagnose and fix service issues

**Key steps**:
- Identify issue type (build, startup, runtime, K8s)
- Check logs and configuration
- Verify dependencies
- Isolate the problem
- Fix and verify
- Document solution

**Time**: 30 minutes - 4 hours

**Common issues covered**:
- Proto generation failures
- Go compile errors
- Wire generation issues
- Database connection problems
- Redis/Consul connection issues
- Port conflicts
- Migration failures
- Event/Dapr issues
- Elasticsearch errors

---

### 5. [Setup New Service](setup-new-service.md)
**When to use**: Create a new microservice from scratch

**Key steps**:
- Planning (scope, ports, service group)
- Create service structure
- Define API contract (proto)
- Implement core layers (biz, data, service)
- Database setup (migrations)
- Configuration (config.yaml, .env)
- GitOps setup (K8s manifests)
- Documentation (service doc, README, CHANGELOG)
- Testing (unit tests)
- Initial commit and deploy

**Time**: 1-2 days

---

### 6. [Hotfix Production](hotfix-production.md)
**When to use**: Emergency production fixes only (P0 issues)

**Key steps**:
- Assessment (confirm severity, identify service)
- Immediate mitigation (rollback, scale down, or config fix)
- Develop minimal fix
- Deploy to staging then production
- Monitor for 30-60 minutes
- Post-hotfix (merge to main, documentation, incident report)

**Time**: 1-3 hours

**Use only for**:
- Production down or severely degraded
- Critical security vulnerability
- Data corruption risk
- Major customer impact

---

### 7. [Refactoring](refactoring.md)
**When to use**: Improve code quality without changing behavior

**Key steps**:
- Ensure tests exist (write them first if needed)
- Make small, incremental changes
- Test after each change
- Verify no behavior changes
- Update documentation
- Commit

**Time**: 2-8 hours

**Common refactorings**:
- Extract method
- Remove duplication
- Simplify conditionals
- Replace magic numbers with constants
- Fix N+1 queries
- Add caching
- Introduce interfaces

---

## Workflow Selection Guide

```
What do you need to do?
├── Deploy code changes?
│   └── Use: Build & Deploy
├── Add new functionality?
│   └── Use: Add New Feature
├── Review service before release?
│   └── Use: Service Review & Release
├── Fix a bug or issue?
│   ├── Production emergency? (P0)
│   │   └── Use: Hotfix Production
│   └── Development issue?
│       └── Use: Troubleshooting
├── Create new service?
│   └── Use: Setup New Service
└── Improve code quality?
    └── Use: Refactoring
```

## Workflow Relationships

```
Setup New Service
    ↓
Add New Feature (multiple times)
    ↓
Refactoring (as needed)
    ↓
Service Review & Release
    ↓
Build & Deploy
    ↓
Troubleshooting (if issues)
    ↓
Hotfix Production (if P0 emergency)
```

## Quick Reference

### Most Common Workflows

1. **Daily development**: Add New Feature → Build & Deploy
2. **Before release**: Service Review & Release
3. **When stuck**: Troubleshooting
4. **Production issue**: Hotfix Production

### Time Estimates

| Workflow | Typical Time | Complexity |
|----------|-------------|------------|
| Build & Deploy | 10-15 min | Low |
| Add New Feature | 2-8 hours | Medium |
| Service Review & Release | 4-8 hours | High |
| Troubleshooting | 30 min - 4 hours | Variable |
| Setup New Service | 1-2 days | High |
| Hotfix Production | 1-3 hours | High |
| Refactoring | 2-8 hours | Medium |

### Skill Requirements

| Workflow | Required Skills |
|----------|----------------|
| Build & Deploy | commit-code |
| Add New Feature | add-api-endpoint, create-migration, add-service-client, add-event-handler, write-tests, review-code, commit-code |
| Service Review & Release | review-service, navigate-service, review-code, commit-code |
| Troubleshooting | troubleshoot-service, debug-k8s, navigate-service |
| Setup New Service | service-structure, add-api-endpoint, create-migration, setup-gitops, write-tests, commit-code |
| Hotfix Production | troubleshoot-service, debug-k8s, commit-code |
| Refactoring | review-code, write-tests, use-common-lib |

## Standards & References

All workflows follow these standards:
- [Coding Standards](../../docs/07-development/standards/coding-standards.md)
- [Team Lead Code Review Guide](../../docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)
- [Development Review Checklist](../../docs/07-development/standards/development-review-checklist.md)
- [Port Allocation Standard](../../gitops/docs/PORT_ALLOCATION_STANDARD.md)

## Best Practices

### General
- Always pull latest code before starting
- Test after every change
- Commit frequently with clear messages
- Document as you go
- Ask for help when stuck

### Code Quality
- Follow Clean Architecture (service → biz → data)
- Write tests before or with code
- Keep functions small (<50 lines)
- Use meaningful names
- No magic numbers
- Handle errors properly

### Deployment
- Never build Docker images locally
- Never manually update GitOps tags
- Always verify deployment
- Monitor after deployment
- Have rollback plan

### Emergency
- Assess severity first
- Communicate with team
- Document everything
- Follow hotfix workflow for P0
- Conduct post-mortem

## Getting Help

### When to Use Which Workflow
- **Not sure which workflow?** → Check the Workflow Selection Guide above
- **Workflow not working?** → Check Troubleshooting workflow
- **Need to customize?** → Workflows are guidelines, adapt as needed

### Escalation
Escalate to senior developer or tech lead if:
- Issue persists after following workflow
- Issue affects multiple services
- Issue is in production
- Unsure about approach
- Need architectural decision

## Contributing

To add or update workflows:
1. Follow existing workflow format
2. Include clear "When to use" section
3. Provide step-by-step instructions
4. Add time estimates
5. Include checklists
6. Link to related workflows and skills
7. Update this README.md

## Workflow Template

```markdown
---
description: Brief description of the workflow
---

## <Workflow Name> Workflow

Brief introduction.

### When to Use
- Scenario 1
- Scenario 2

### Prerequisites
- Prerequisite 1
- Prerequisite 2

### Workflow Steps

#### Phase 1: <Phase Name>

**1.1 Step Name**

Description and commands.

#### Phase 2: <Phase Name>

...

### Checklist

- [ ] Item 1
- [ ] Item 2

### Related Workflows
- [Workflow 1](workflow1.md)
- [Workflow 2](workflow2.md)

### Related Skills
- skill-1
- skill-2
```

---

*Last updated: 2026-03-05*
*Total workflows: 7*
