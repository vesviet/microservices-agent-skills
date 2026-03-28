# 🛠️ Microservices Agent Skills

> A Codex-compatible pack of **22 AI skills** and **7 workflows** for developing, reviewing, and operating a production-grade e-commerce microservices platform.

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
| [**add-cron-job**](skills/add-cron-job/SKILL.md) | Add scheduled jobs to a worker binary using the project's cron patterns | Periodic syncs, cleanup jobs, reconciliation tasks |
| [**add-event-handler**](skills/add-event-handler/SKILL.md) | Add event publishers & consumers via Dapr PubSub | Inter-service communication, event-driven workflows |
| [**add-service-client**](skills/add-service-client/SKILL.md) | Add gRPC client for service-to-service calls via service discovery | Service A needs to call Service B |
| [**create-migration**](skills/create-migration/SKILL.md) | Create database migrations using Goose format | Schema changes, new tables, indexes |
| [**upgrade-common-lib**](skills/upgrade-common-lib/SKILL.md) | Upgrade the shared `common` library version across services safely | After tagging a new `common` release |

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
| [**meeting-review**](skills/meeting-review/SKILL.md) | Simulate a structured multi-perspective technical review | Architecture decisions, tech debt, feature design reviews |
| [**create-agent-task**](skills/create-agent-task/SKILL.md) | Turn high-level hardening requests into actionable AGENT task files | Assigning scoped implementation tasks |
| [**process-agent-task**](skills/process-agent-task/SKILL.md) | Process AGENT task files end to end with validation and documentation | Implementing tracked hardening work |

### 🚀 Operations & Deployment

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [**setup-gitops**](skills/setup-gitops/SKILL.md) | Set up or update GitOps config (Kustomize overlays, ConfigMaps, Secrets, Deployments) | New service deployment, config updates |
| [**debug-k8s**](skills/debug-k8s/SKILL.md) | Debug Kubernetes deployment issues (pods, services, configs, images, ArgoCD) | Pods crashing, ImagePullBackOff, sync failures |
| [**troubleshoot-service**](skills/troubleshoot-service/SKILL.md) | Troubleshoot service runtime issues (build errors, crashes, connection failures) | Build errors, connection failures, crashes |
| [**rollback-deployment**](skills/rollback-deployment/SKILL.md) | Roll back a failed deployment using GitOps-safe recovery steps | Broken releases, bad config rollouts |
| [**performance-profiling**](skills/performance-profiling/SKILL.md) | Profile and optimize Go services with pprof and benchmarks | Hot paths, latency, throughput issues |

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

### For Codex

Each skill folder in `skills/` is now structured for Codex with:
- `SKILL.md`
- `agents/openai.yaml`

To install them into Codex as symlinks:

```bash
cd microservices-agent-skills
mkdir -p ~/.codex/skills
for d in skills/*; do
  ln -sfn "$PWD/$d" "$HOME/.codex/skills/$(basename "$d")"
done
```

These skills are intended for use while this microservices repository is open, because they reference project paths like `docs/`, service directories, and workflow files.

### For `.agent/`-style Tooling

The original source material remains in the project-level `.agent/` directory:
```
.agent/
├── skills/
├── workflows/
└── rules/
```

Use that layout directly for tools that auto-discover `.agent/` prompts.

### For Developers

Use these as **reference guides** when:
- Adding new features (endpoints, events, clients)
- Reviewing code (follow the checklist)
- Debugging issues (K8s, service problems)
- Understanding the codebase structure

## 📊 Stats

- **22 skills** covering the full development lifecycle
- **7 workflows** for common developer tasks
- **1 rule** defining project context and standards

---

**Maintained by**: Development Team
**Last Updated**: 2026-03-19
