# 🛠️ Microservices Agent Skills

> A collection of **13 AI agent skills** for developing, reviewing, and operating a production-grade e-commerce microservices platform.

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
| [**add-api-endpoint**](add-api-endpoint/SKILL.md) | Add new REST/gRPC endpoints | Adding CRUD operations, new business APIs |
| [**add-event-handler**](add-event-handler/SKILL.md) | Add event publishers & consumers | Inter-service communication via Dapr PubSub |
| [**add-service-client**](add-service-client/SKILL.md) | Add gRPC client for service-to-service calls | Service A needs to call Service B |
| [**create-migration**](create-migration/SKILL.md) | Create database migrations (Goose) | Schema changes, new tables, indexes |

### 🔍 Understanding & Navigation

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**navigate-service**](navigate-service/SKILL.md) | Navigate and understand service structure | First time exploring a service |
| [**service-structure**](service-structure/SKILL.md) | Dual-binary architecture (main + worker) | Understanding main vs worker processes |
| [**trace-event-flow**](trace-event-flow/SKILL.md) | Trace event-driven communication flows | Debugging event chains across services |
| [**use-common-lib**](use-common-lib/SKILL.md) | Reference guide for shared `common` library | Before writing custom code — check if it exists |

### ✅ Quality & Review

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**review-code**](review-code/SKILL.md) | **Tech Lead level** code review (P0/P1/P2) | Code reviews, PR reviews, service release |
| [**write-tests**](write-tests/SKILL.md) | Testing patterns (testify, table-driven, mocks) | Writing unit & integration tests |

### 🚀 Operations & Deployment

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**setup-gitops**](setup-gitops/SKILL.md) | Set up GitOps config (Kustomize overlays) | New service deployment, config updates |
| [**debug-k8s**](debug-k8s/SKILL.md) | Debug Kubernetes deployment issues | Pods crashing, ImagePullBackOff, sync failures |
| [**troubleshoot-service**](troubleshoot-service/SKILL.md) | Troubleshoot service runtime issues | Build errors, connection failures, crashes |

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

The `review-code` skill uses **P0/P1/P2** severity:

| Severity | Category | Examples | Action |
|----------|----------|----------|--------|
| 🔴 **P0** | Security, Data, Correctness | SQL injection, missing transactions, breaking backward compat | **Must fix** |
| 🟡 **P1** | Performance, Reliability | N+1 queries, missing circuit breakers, config drift | **Should fix** |
| 🔵 **P2** | Quality, Maintenance | Documentation, code style, low test coverage | **Nice to have** |

## 🚀 Usage

### For AI Agents (Cursor, Copilot, etc.)

Place skills in your workspace:
```
.agent/skills/
├── add-api-endpoint/SKILL.md
├── add-event-handler/SKILL.md
├── add-service-client/SKILL.md
├── ...
└── write-tests/SKILL.md
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

- **13 skills** covering the full development lifecycle
- **4,400+ lines** of documented patterns and checklists
- **108 review checklist items** in the tech lead review skill
- **16 review categories** including cross-service impact analysis

---

**Maintained by**: Development Team  
**Last Updated**: 2026-02-10
