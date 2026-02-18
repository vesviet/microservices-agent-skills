# 🛠️ Microservices Agent Skills

> A collection of **19 AI agent skills** and **10 workflows** for developing, reviewing, and operating a production-grade e-commerce microservices platform.

## 🏗️ Project Context

These skills are designed for a **Go microservices platform** built with:

- **Framework**: [Kratos](https://go-kratos.dev/) (gRPC/HTTP)
- **Architecture**: Clean Architecture + Domain-Driven Design (DDD)
- **Event Bus**: Dapr PubSub (Redis Streams)
- **Service Discovery**: Consul
- **Database**: PostgreSQL + GORM
- **Cache**: Redis
- **Search**: Elasticsearch
- **DI**: Google Wire
- **Deployment**: Kubernetes (k3s) + ArgoCD + Kustomize
- **Migrations**: Goose (SQL)

## 📋 Skills Overview

### 🔨 Development Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**add-api-endpoint**](skills/add-api-endpoint/SKILL.md) | Add new REST/gRPC endpoints | Adding CRUD operations, new business APIs |
| [**add-event-handler**](skills/add-event-handler/SKILL.md) | Add event publishers & consumers | Inter-service communication via Dapr PubSub |
| [**add-service-client**](skills/add-service-client/SKILL.md) | Add gRPC client for service-to-service calls | Service A needs to call Service B |
| [**create-migration**](skills/create-migration/SKILL.md) | Create database migrations (Goose) | Schema changes, new tables, indexes |
| [**scaffold-new-service**](skills/scaffold-new-service/SKILL.md) | Scaffold a new microservice from scratch | Creating an entirely new service |

### 🔍 Understanding & Navigation

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**navigate-service**](skills/navigate-service/SKILL.md) | Navigate and understand service structure | First time exploring a service |
| [**service-structure**](skills/service-structure/SKILL.md) | Dual-binary architecture (main + worker) | Understanding main vs worker processes |
| [**service-map**](skills/service-map/SKILL.md) | Quick-reference map of all microservices | Finding ports, dependencies, gRPC clients, event flows |
| [**trace-event-flow**](skills/trace-event-flow/SKILL.md) | Trace event-driven communication flows | Debugging event chains across services |
| [**use-common-lib**](skills/use-common-lib/SKILL.md) | Reference guide for shared `common` library | Before writing custom code — check if it exists |

### ✅ Quality & Review

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**review-code**](skills/review-code/SKILL.md) | **Tech Lead level** code review (P0/P1/P2) | Code reviews, PR reviews |
| [**review-service**](skills/review-service/SKILL.md) | Full service review & release pipeline | End-to-end service audit, tagging, and release |
| [**write-tests**](skills/write-tests/SKILL.md) | Testing patterns (testify, table-driven, mocks) | Writing unit & integration tests |
| [**commit-code**](skills/commit-code/SKILL.md) | Pre-commit validation, dependency management, git | Validating and committing changes |

### 🚀 Operations & Deployment

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**setup-gitops**](skills/setup-gitops/SKILL.md) | Set up GitOps config (Kustomize overlays) | New service deployment, config updates |
| [**debug-k8s**](skills/debug-k8s/SKILL.md) | Debug Kubernetes deployment issues | Pods crashing, ImagePullBackOff, sync failures |
| [**troubleshoot-service**](skills/troubleshoot-service/SKILL.md) | Troubleshoot service runtime issues | Build errors, connection failures, crashes |
| [**database-maintenance**](skills/database-maintenance/SKILL.md) | Database backup, restore, PITR, maintenance | PostgreSQL backup/restore, point-in-time recovery |
| [**manage-secrets**](skills/manage-secrets/SKILL.md) | Secret and environment variable management | Managing sensitive config across services |

## ⚡ Workflows

Workflows are slash-command-invoked procedures in `workflows/`. See [workflows README](workflows/README.md) for turbo mode settings.

| Slash Command | Purpose | Optimization |
|---------------|---------|-------------|
| `/add-api-quick` | Adding new API endpoints | Speed via patterns |
| `/architecture-planning` | Complex multi-service changes | Deep reasoning |
| `/debug-issue` | Troubleshooting and debugging | Problem-solving |
| `/deep-review` | Thorough code review | Quality |
| `/git-operations` | Git across all microservices | Batch operations |
| `/plan-event-driven` | Event-driven architecture | Async patterns |
| `/quick-docs` | Documentation updates | Clarity |
| `/quick-refactor` | Fast, focused refactoring | Speed |
| `/write-test-coverage` | Writing comprehensive tests | Coverage |
| `/wsl-terminal` | WSL terminal usage | Reference |

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Service Structure                         │
│                                                                   │
│  cmd/<service>/main.go  ─── Main Binary (API/gRPC, Consul)       │
│  cmd/worker/main.go     ─── Worker Binary (Events, Cron, Outbox) │
│                                                                   │
│  internal/                                                        │
│  ├── biz/       ← Business logic (domain rules, use cases)       │
│  ├── data/      ← Repositories (GORM, Redis, Elasticsearch)      │
│  ├── service/   ← API handlers (thin: parse → biz → respond)     │
│  ├── client/    ← Outbound gRPC clients                          │
│  ├── events/    ← Event publishing                                │
│  ├── worker/    ← Event consumers, cron jobs, outbox              │
│  └── constants/ ← Service-specific constants                      │
│                                                                   │
│  api/<service>/v1/  ← Proto definitions                           │
│  migrations/        ← SQL migrations (Goose)                      │
└─────────────────────────────────────────────────────────────────┘
```

## 📐 Review Severity Levels

The `review-code` and `review-service` skills use **P0/P1/P2** severity:

| Severity | Category | Examples | Action |
|----------|----------|----------|--------|
| 🔴 **P0** | Security, Data, Correctness | SQL injection, missing transactions, breaking backward compat | **Must fix** |
| 🟡 **P1** | Performance, Reliability | N+1 queries, missing circuit breakers, config drift | **Should fix** |
| 🔵 **P2** | Quality, Maintenance | Documentation, code style, low test coverage | **Nice to have** |

## 🚀 Usage

### For AI Agents (Cursor, Copilot, etc.)

Place in your workspace as `.agent/`:
```
.agent/
├── skills/
│   ├── add-api-endpoint/SKILL.md
│   ├── add-event-handler/SKILL.md
│   ├── ...
│   └── write-tests/SKILL.md
├── workflows/
│   ├── add-api-quick.md
│   ├── ...
│   └── wsl-terminal.md
└── rules/
    └── testcase.md
```

The AI agent will automatically discover and use relevant skills when you ask it to perform related tasks.

### For Developers

Use these as **reference guides** when:
- Adding new features (endpoints, events, clients)
- Reviewing code (follow the checklist)
- Debugging issues (K8s, service problems)
- Understanding the codebase structure

## 📚 Related Documentation

- **Coding Standards**: `docs/07-development/standards/coding-standards.md`
- **Team Lead Review Guide**: `docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md`
- **Development Review Checklist**: `docs/07-development/standards/development-review-checklist.md`
- **Service Review & Release**: `docs/07-development/standards/service-review-release-prompt.md`
- **Common Package Usage**: `docs/07-development/standards/common-package-usage.md`

## 📊 Stats

- **19 skills** covering the full development lifecycle
- **10 workflows** for common developer tasks
- **108 review checklist items** in the tech lead review skill
- **16 review categories** including cross-service impact analysis

---

**Maintained by**: Development Team  
**Last Updated**: 2026-02-18
