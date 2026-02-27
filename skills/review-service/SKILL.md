---
name: review-service
description: Single process for reviewing and releasing any microservice based on service-review-release-prompt.md
---

# Service Review & Release Skill

Use this skill to review an entire service for production readiness and prepare it for release.

## When to Use
- When the user asks to "review service X" or "review and release X"
- When running the full service release process
- Before a major feature merge or production deployment of a microservice

---

## Standards (read first)

Before any code change, apply these standards:
1. **[Coding Standards](docs/07-development/standards/coding-standards.md)** — Go style, proto, layers, context, errors, constants.
2. **[Team Lead Code Review Guide](docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)** — Architecture, API, biz logic, data, security, performance, observability.
3. **[Development Review Checklist](docs/07-development/standards/development-review-checklist.md)** — Pre-review, issue levels, Go/security/testing/DevOps criteria.

---

## Process for `<serviceName>`

Use this process for the service identified by **`<serviceName>`** (e.g. warehouse → `warehouse`, pricing → `pricing`).
Paths and commands below use `<serviceName>`; replace it with the real service name.

> [!IMPORTANT]
> Many services use a **dual-binary architecture**: `cmd/<serviceName>/` (main API server) + `cmd/worker/` (event consumers, cron, outbox). Always review **both** entry points.

### Step 0: Sync Latest Code

> [!CAUTION]
> **Always pull latest before reviewing.** Missing recent commits leads to reviewing stale code and duplicating already-fixed work.

```bash
# Pull latest for the service AND related repos
cd /home/user/microservices/<serviceName> && git pull origin main
cd /home/user/microservices/common && git pull origin main
cd /home/user/microservices/gitops && git pull origin main
```

### Step 1: Index & Review Codebase

1. **Index and understand the `<serviceName>` service**:
   - Directory `<serviceName>/` layout: `cmd/` (main + worker entry points), `internal/biz/`, `internal/data/`, `internal/service/`, `internal/client/`, `internal/events/`, `internal/worker/`, `internal/constants/`
   - Proto under `api/<serviceName>/v1/`
   - Migrations: `migrations/`
   - Config: `configs/`, `go.mod`
2. **Review code** against the three standards above (architecture, layers, context, errors, validation, security, no N+1, transactions, observability).
3. **List P0 / P1 / P2 issues** (use severity from TEAM_LEAD_CODE_REVIEW_GUIDE).

| Severity | Definition | Examples |
|----------|-----------|----------|
| **P0 (Blocking)** | Security, data inconsistency, breaking backward compat | No auth, raw SQL concat, biz calls DB directly, proto field removed without `reserved`, breaking event schema |
| **P1 (High)** | Performance, missing observability, config mismatch | N+1 queries, no circuit breaker, env var not in configmap |
| **P2 (Normal)** | Documentation, code style, naming | Missing comments, TODO without ticket |

### Step 2: Cross-Service Impact Analysis

> [!WARNING]
> **This step is mandatory.** Skipping it risks deploying breaking changes that crash other services at runtime.

#### 2.1 Proto/API Backward Compatibility

```bash
# Who depends on this service's proto?
grep -r 'gitlab.com/ta-microservices/<serviceName>' --include='go.mod' /home/user/microservices/*/go.mod
```

- Proto field numbers preserved (use `reserved` for deleted fields)
- New fields are optional (adding required fields = MAJOR break)
- RPC signatures stable (no rename/remove without versioning `v1` → `v2`)
- All client services still compile after changes

#### 2.2 Event Schema Compatibility

```bash
# Who consumes this service's events?
grep -r 'Topic.*<serviceName>' /home/user/microservices/*/internal/ --include='*.go' -l
```

- Event struct changes are additive-only (removing/renaming fields = breaking)
- Consumers handle old + new format gracefully
- Topic names immutable (never rename existing topics)

#### 2.3 Go Module Dependency Graph
- No circular imports between services
- Minimal import surface (don't import entire service module for one type)

### Step 3: Checklist & TODO for `<serviceName>`

- Track review findings and TODOs in a dedicated review checklist (e.g., `docs/10-appendix/workflow/<serviceName>-review-checklist.md`). **Do NOT put checklists, TODOs, or review findings in the service documentation.**
- Align items with TEAM_LEAD_CODE_REVIEW_GUIDE and development-review-checklist (P0/P1/P2).
- Mark completed items; add items for remaining work. **Skip adding or requiring test-case tasks** (per user request).

### Step 4: Dependencies (Go Modules)

> [!CAUTION]
> **NO `replace` directives for `gitlab.com/ta-microservices` are allowed.** This works locally but breaks CI/CD.

#### 4.1 Check if `common` changed

```bash
# If common has uncommitted changes, it MUST be committed + tagged FIRST
cd /home/user/microservices/common && git status
```

**If `common` changed → commit, tag, and push `common` BEFORE touching the service:**

```bash
cd /home/user/microservices/common
golangci-lint run && go build ./... && go test ./...
rm -rf bin/ # ALWAYS check and remove bin directory before committing
git add -A && git commit -m "<type>(common): <description>"
git tag --sort=-creatordate | head -5   # check current latest tag
git tag -a v1.x.y -m "v1.x.y: <summary>"
git push origin main && git push origin v1.x.y
```

> [!IMPORTANT]
> **Common must be tagged before any service commit.** Services import `common` via `go get @<tag>`. If the service is committed before common is tagged, `go.mod` references a non-existent version.

#### 4.2 Convert replace to import (if needed)

```bash
# Check for forbidden replace directives
grep 'replace gitlab.com/ta-microservices' <serviceName>/go.mod

# If found: remove replace lines, then get latest versions:
cd /home/user/microservices/<serviceName>
go get gitlab.com/ta-microservices/common@latest
go get gitlab.com/ta-microservices/<other-dep>@latest
go mod tidy
```

#### 4.3 Update dependencies

```bash
cd /home/user/microservices/<serviceName>
# Always get the latest version for common
go get gitlab.com/ta-microservices/common@latest    # or @v1.x.y if just tagged

# ALWAYS get the latest tag for ANY OTHER internal dependencies imported in go.mod
# Example: if importing catalog, run: go get gitlab.com/ta-microservices/catalog@latest
go mod tidy
```

> [!IMPORTANT]
> **Rule on Internal Dependencies**: When importing other services or packages from `gitlab.com/ta-microservices` via `go.mod`, ALWAYS ensure you are pulling their latest tagged version using `go get gitlab.com/ta-microservices/<dependency>@latest`. Do NOT use outdated versions.

### Step 5: Lint & Build

```bash
cd /home/user/microservices/<serviceName>

# 1. Generate proto (if .proto files changed)
make api

# 2. Regenerate Wire (if DI providers changed) — BOTH binaries
cd cmd/<serviceName> && wire
cd ../worker && wire      # if worker binary exists

# 3. Lint (target: zero warnings)
cd /home/user/microservices/<serviceName>
golangci-lint run

# 4. Build
go build ./...

# 5. Run tests
go test ./...
```

> [!NOTE]
> **Never manually edit `wire_gen.go` or `*.pb.go`** — these files are auto-generated. Always use `wire` and `make api` to regenerate.

### Step 6: Deployment Readiness (GitOps Alignment)

Before release, verify config alignment between code and GitOps.

> [!IMPORTANT]
> **Port allocation MUST follow [PORT_ALLOCATION_STANDARD.md](../../../gitops/docs/PORT_ALLOCATION_STANDARD.md).** Look up the correct HTTP/gRPC ports for `<serviceName>` in the Port Allocation Table and verify all references match.

```bash
# 0. Look up correct ports from standard
grep '<serviceName>' /home/user/microservices/gitops/docs/PORT_ALLOCATION_STANDARD.md

# 1. Check env vars used in code
grep -rn 'os.Getenv\|viper.Get\|envconfig' <serviceName>/internal/ --include='*.go'

# 2. Compare with gitops configmap
cat gitops/apps/<serviceName>/base/configmap.yaml

# 3. Verify ports match (MUST align with PORT_ALLOCATION_STANDARD.md)
grep 'addr:' <serviceName>/configs/config.yaml
grep 'containerPort:' gitops/apps/<serviceName>/base/deployment.yaml
grep 'targetPort:' gitops/apps/<serviceName>/base/service.yaml
grep 'dapr.io/app-port:' gitops/apps/<serviceName>/base/deployment.yaml
grep -A2 'livenessProbe:\|readinessProbe:' gitops/apps/<serviceName>/base/deployment.yaml | grep port

# 4. Check resource limits are set
grep -A5 'resources:' gitops/apps/<serviceName>/base/deployment.yaml

# 5. Check HPA exists
ls gitops/apps/<serviceName>/base/hpa.yaml 2>/dev/null || echo "⚠️ No HPA configured"
```

Checklist:
- [ ] **Ports match PORT_ALLOCATION_STANDARD.md**: `config.yaml` addr ↔ `deployment.yaml` containerPort ↔ `service.yaml` targetPort ↔ `dapr.io/app-port` ↔ health probe ports
- [ ] New env vars in code → ConfigMap/Secret updated in `gitops/`
- [ ] Resource limits set (not unbounded)
- [ ] Health probes configured (liveness + readiness) on correct port
- [ ] Dapr annotations correct (`app-id`, `app-port`, `app-protocol`)
- [ ] NetworkPolicy allows required egress/ingress
- [ ] Migration strategy safe for zero-downtime deploy

### Step 7: Docs

#### 7.1 Service documentation
Update or create service docs under **`docs/03-services/<group>/<serviceName>-service.md`**.
> [!NOTE]
> **Service documentation is an introduction to the service, its architecture, and its capabilities.** It is NOT a checklist or a place to track TODOs/review findings.

- `core-services`: order, catalog, customer, payment, auth, user
- `operational-services`: notification, analytics, search, review, warehouse, fulfillment, shipping, pricing, promotion, loyalty-rewards, location
- `platform-services`: gateway, common-operations

#### 7.2 README.md
Update **`<serviceName>/README.md`** using the template at `docs/templates/readme-template.md`.

#### 7.3 CHANGELOG.md
Update **`<serviceName>/CHANGELOG.md`** (create if not exists) using conventional changelog format.

> [!IMPORTANT]
> **Do NOT commit `docs/` repo changes separately.** The `docs/` directory is a separate git repository (`master` branch). Doc file edits (service doc, review checklist) are written to disk but are **not committed** as part of the service review workflow — the user manages `docs/` repo commits independently.
>
> **Only** `<serviceName>/CHANGELOG.md` and `<serviceName>/README.md` (inside the service repo) are committed, as part of Step 8.

#### 7.4 Documentation checklist
- [ ] Current and accurate information
- [ ] Working commands (tested)
- [ ] Correct ports and endpoints
- [ ] Valid configuration examples

### Step 8: Commit & Release

> [!IMPORTANT]
> **CI/CD builds Docker images and updates GitOps tags automatically.** Never build Docker images locally. Never manually update `newTag` in gitops kustomization.

#### 8.1 Commit order (when multiple components changed)
1. `common/` → commit + tag (`v1.x.y`) + push
2. `<serviceName>/` → `go get common@v1.x.y` + commit + push
3. CI/CD builds image + updates gitops tag auto

#### 8.2 Commit

```bash
cd /home/user/microservices/<serviceName>
rm -rf bin/ # ALWAYS check and remove bin directory before committing
git add -A
git commit -m "<type>(<serviceName>): <description>"
```

#### 8.3 Push & Release

```bash
# Push to remote
git push origin main

# IF RELEASE:
git tag -a v1.0.7 -m "v1.0.7: description"
git push origin v1.0.7
```

---

## Review Output Format

Use this format to report review findings:

```markdown
## 🔍 Service Review: <serviceName>

**Date**: YYYY-MM-DD
**Status**: ✅ Ready / ⚠️ Needs Work / ❌ Not Ready

### 📊 Issue Summary

| Severity | Count | Status |
|----------|-------|--------|
| P0 (Blocking) | X | Fixed / Remaining |
| P1 (High) | X | Fixed / Remaining |
| P2 (Normal) | X | Fixed / Remaining |

### 🔴 P0 Issues (Blocking)
1. **[CATEGORY]** file:line — Description

### 🟡 P1 Issues (High)
1. **[CATEGORY]** file:line — Description

### 🔵 P2 Issues (Normal)
1. **[CATEGORY]** file:line — Description

### ✅ Completed Actions
1. Fixed: description

### 🌐 Cross-Service Impact
- Services that import this proto: [list]
- Services that consume events: [list]
- Backward compatibility: ✅ Preserved / ❌ Breaking

### 🚀 Deployment Readiness
- Config/GitOps aligned: ✅ / ❌
- Health probes: ✅ / ❌
- Resource limits: ✅ / ❌
- Migration safety: ✅ / ❌

### Build Status
- `golangci-lint`: ✅ 0 warnings / ❌ X warnings
- `go build ./...`: ✅ / ❌
- `wire`: ✅ Generated / ❌ Needs regen
- Generated Files (`wire_gen.go`, `*.pb.go`): ✅ Not modified manually / ❌ Modified manually
- `bin/` Files: ✅ Removed / ❌ Present

### Documentation
- Service doc: ✅ / ❌
- README.md: ✅ / ❌
- CHANGELOG.md: ✅ / ❌
```
