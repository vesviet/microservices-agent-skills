# 🛠️ Microservices Agent Skills

> A collection of **15 AI agent skills** and **7 workflows** for developing, reviewing, and operating a production-grade e-commerce microservices platform.

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
| [**add-api-endpoint**](skills/add-api-endpoint/SKILL.md) | Add new REST/gRPC endpoints following Kratos + Clean Architecture patterns | Adding CRUD operations, new business APIs |
| [**add-event-handler**](skills/add-event-handler/SKILL.md) | Add event publishers & consumers via Dapr PubSub | Inter-service communication, event-driven workflows |
| [**add-service-client**](skills/add-service-client/SKILL.md) | Add gRPC client for service-to-service calls via service discovery | Service A needs to call Service B |
| [**create-migration**](skills/create-migration/SKILL.md) | Create database migrations using Goose format | Schema changes, new tables, indexes |

### 🔍 Understanding & Navigation

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**navigate-service**](skills/navigate-service/SKILL.md) | Navigate and understand service structure, architecture layers, and key components | First time exploring a service |
| [**service-structure**](skills/service-structure/SKILL.md) | Understand the dual-binary architecture (main + worker) | Understanding main vs worker processes |
| [**trace-event-flow**](skills/trace-event-flow/SKILL.md) | Trace event-driven communication flows between microservices | Debugging event chains across services |
| [**use-common-lib**](skills/use-common-lib/SKILL.md) | Reference guide for the shared `common` library | Before writing custom code — check if it already exists |

### ✅ Quality & Review

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**review-code**](skills/review-code/SKILL.md) | Code review following coding standards and Clean Architecture principles | Code reviews, PR reviews |
| [**review-service**](skills/review-service/SKILL.md) | Full service review & release pipeline | End-to-end service audit, tagging, and release |
| [**write-tests**](skills/write-tests/SKILL.md) | Testing patterns (testify, table-driven, mockgen-generated mocks) | Writing unit & integration tests |
| [**commit-code**](skills/commit-code/SKILL.md) | Pre-commit validation, dependency management, git workflow | Validating and committing changes |

### 🚀 Operations & Deployment

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**setup-gitops**](skills/setup-gitops/SKILL.md) | Set up or update GitOps config (Kustomize overlays, ConfigMaps, Secrets, Deployments) | New service deployment, config updates |
| [**debug-k8s**](skills/debug-k8s/SKILL.md) | Debug Kubernetes deployment issues (pods, services, configs, images, ArgoCD) | Pods crashing, ImagePullBackOff, sync failures |
| [**troubleshoot-service**](skills/troubleshoot-service/SKILL.md) | Troubleshoot service runtime issues (build errors, crashes, connection failures) | Build errors, connection failures, crashes |

## ⚡ Workflows

Workflows are step-by-step procedures stored in `workflows/`. See [workflows README](workflows/README.md) for details.

| Slash Command | Purpose |
|---------------|---------|
| `/add-new-feature` | Complete workflow for adding a new feature to a microservice |
| `/build-deploy` | How to build and deploy a microservice |
| `/hotfix-production` | Emergency workflow for hotfixing production issues |
| `/refactoring` | Safely refactoring code while maintaining functionality |
| `/service-review-release` | Complete workflow for reviewing and releasing a microservice to production |
| `/setup-new-service` | Setting up a new microservice from scratch |
| `/troubleshooting` | Troubleshooting common service issues |

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

### For AI Agents (Cursor, Gemini CLI, etc.)

Place in your workspace as `.agent/`:
```
.agent/
├── skills/
│   ├── add-api-endpoint/SKILL.md
│   ├── add-event-handler/SKILL.md
│   ├── ...
│   └── write-tests/SKILL.md
├── workflows/
│   ├── add-new-feature.md
│   ├── ...
│   └── troubleshooting.md
└── rules/
    └── microservices.md
```

The AI agent will automatically discover and use relevant skills when you ask it to perform related tasks.

### For Developers

Use these as **reference guides** when:
- Adding new features (endpoints, events, clients)
- Reviewing code (follow the checklist)
- Debugging issues (K8s, service problems)
- Understanding the codebase structure

## 📊 Stats

- **15 skills** covering the full development lifecycle
- **7 workflows** for common developer tasks
- **1 rule** defining project context and standards

---

**Maintained by**: Development Team
**Last Updated**: 2026-03-07
