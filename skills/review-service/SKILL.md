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

## Review Flow Overview

```
Step 0: Sync Latest Code (git pull)
        ↓
Step 1: Index & Review Codebase
        ├── Architecture & layers
        ├── API contracts
        ├── Business logic
        ├── Data layer
        └── List P0/P1/P2 issues
        ↓
Step 2: Cross-Service Impact Analysis
        ├── Proto backward compatibility
        ├── Event schema compatibility
        └── Go module dependencies
        ↓
Step 3: Create Review Checklist
        └── Track findings in docs/10-appendix/workflow/
        ↓
Step 4: Action Plan & Bug Fixes
        ├── Create action plan for P0/P1
        └── Implement fixes immediately
        ↓
Step 5: Test Coverage Check
        ├── Run coverage
        └── Update TEST_COVERAGE_CHECKLIST.md
        ↓
Step 6: Dependencies (Go Modules)
        ├── Check/tag common if changed
        ├── Remove replace directives
        └── Update to latest versions
        ↓
Step 7: Lint & Build
        ├── Generate proto (make api)
        ├── Regenerate Wire
        ├── Run golangci-lint
        └── Build & test
        ↓
Step 8: Deployment Readiness
        ├── Verify port allocation
        ├── Check config/GitOps alignment
        └── Verify health probes & resources
        ↓
Step 9: Documentation
        ├── Update service doc
        ├── Update README.md
        └── Update CHANGELOG.md
        ↓
Step 10: Commit & Release
        ├── Commit with conventional format
        ├── Tag version (if releasing)
        └── Update GitOps (if config changed)
```

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
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName> && git pull origin main
cd /Users/tuananh/Desktop/myproject/microservice/common && git pull origin main
cd /Users/tuananh/Desktop/myproject/microservice/gitops && git pull origin main
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
grep -r 'gitlab.com/ta-microservices/<serviceName>' --include='go.mod' /Users/tuananh/Desktop/myproject/microservice/*/go.mod
```

- Proto field numbers preserved (use `reserved` for deleted fields)
- New fields are optional (adding required fields = MAJOR break)
- RPC signatures stable (no rename/remove without versioning `v1` → `v2`)
- All client services still compile after changes

#### 2.2 Event Schema Compatibility

```bash
# Who consumes this service's events?
grep -r 'Topic.*<serviceName>' /Users/tuananh/Desktop/myproject/microservice/*/internal/ --include='*.go' -l
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

### Step 4: Action Plan & Bug Fix Implementation

> [!IMPORTANT]
> **If bugs are found during review, create an action plan and implement fixes immediately.** Do NOT just log issues and move on — fix P0 and P1 bugs in-place during the review process.

#### 4.1 Create Action Plan

For each P0/P1 issue found in Step 1–3, create a concrete action plan:

```markdown
## 🔧 Action Plan for <serviceName>

### P0 Fixes (implement now)
| # | Issue | File:Line | Root Cause | Fix Description | Status |
|---|-------|-----------|------------|-----------------|--------|
| 1 | ... | ... | ... | ... | ⬜ TODO / ✅ Done |

### P1 Fixes (implement now if time allows)
| # | Issue | File:Line | Root Cause | Fix Description | Status |
|---|-------|-----------|------------|-----------------|--------|
| 1 | ... | ... | ... | ... | ⬜ TODO / ✅ Done |

### P2 Notes (document only)
| # | Issue | File:Line | Description |
|---|-------|-----------|-------------|
| 1 | ... | ... | ... |
```

#### 4.2 Implement Bug Fixes

1. **Fix P0 bugs first** — these are blocking and must be resolved before release.
2. **Fix P1 bugs** — implement if time allows; otherwise, document in the review checklist.
3. **For each fix**:
   - Identify root cause
   - Implement the fix in the correct layer (biz/data/service)
   - Run `go build ./...` and `go test ./...` after each fix to verify
   - Mark the action plan item as ✅ Done
4. **If a fix requires changes in `common`**: follow Step 4 (Dependencies) to commit + tag common first.

> [!WARNING]
> **Do NOT skip bug fixes.** The purpose of this review is to catch and fix issues before release. If a P0 bug is found, the service CANNOT be released until it is fixed.

### Step 5: Test Coverage Check

> [!NOTE]
> **After completing the review, check the service's test coverage and update the central checklist.**

#### 5.1 Run Coverage

```bash
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>

# Full coverage by package
go test ./internal/... -count=1 -cover 2>&1 | grep -E '^ok|^FAIL'

# Service layer detailed coverage
go test ./internal/service/... -count=1 -coverprofile=/tmp/<serviceName>_service_cover.out
go tool cover -func=/tmp/<serviceName>_service_cover.out | tail -30
```

#### 5.2 Update Test Coverage Checklist

Update `docs/10-appendix/checklists/test/TEST_COVERAGE_CHECKLIST.md` with:
- Current coverage numbers for each package (biz, service, data)
- Status changes (e.g., from ⚠️ to ✅ if coverage crossed 60%)
- Work done description (what tests were added/fixed)
- Test file counts
- Update the dashboard section (total test files, services above 60%)
- Update the `Last Updated` timestamp

#### 5.3 Coverage Targets

| Layer | Target | Priority |
|-------|--------|----------|
| Biz | ≥60% | High — core business logic |
| Service | ≥60% | Medium — gRPC handler tests |
| Data | ≥60% | Lower — repository tests |

### Step 6: Dependencies (Go Modules)

> [!CAUTION]
> **NO `replace` directives for `gitlab.com/ta-microservices` are allowed.** This works locally but breaks CI/CD.

#### 6.1 Check if `common` changed

```bash
# If common has uncommitted changes, it MUST be committed + tagged FIRST
cd /Users/tuananh/Desktop/myproject/microservice/common && git status
```

**If `common` changed → commit, tag, and push `common` BEFORE touching the service:**

```bash
cd /Users/tuananh/Desktop/myproject/microservice/common
golangci-lint run && go build ./... && go test ./...
rm -rf bin/ # ALWAYS check and remove bin directory before committing
git add -A && git commit -m "<type>(common): <description>"
git tag --sort=-creatordate | head -5   # check current latest tag
git tag -a v1.x.y -m "v1.x.y: <summary>"
git push origin main && git push origin v1.x.y
```

> [!IMPORTANT]
> **Common must be tagged before any service commit.** Services import `common` via `go get @<tag>`. If the service is committed before common is tagged, `go.mod` references a non-existent version.

#### 6.2 Convert replace to import (if needed)

```bash
# Check for forbidden replace directives
grep 'replace gitlab.com/ta-microservices' <serviceName>/go.mod

# If found: remove replace lines, then get latest versions:
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>
go get gitlab.com/ta-microservices/common@latest
go get gitlab.com/ta-microservices/<other-dep>@latest
go mod tidy
```

#### 6.3 Update dependencies

```bash
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>
# Always get the latest version for common
go get gitlab.com/ta-microservices/common@latest    # or @v1.x.y if just tagged

# ALWAYS get the latest tag for ANY OTHER internal dependencies imported in go.mod
# Example: if importing catalog, run: go get gitlab.com/ta-microservices/catalog@latest
go mod tidy
```

> [!IMPORTANT]
> **Rule on Internal Dependencies**: When importing other services or packages from `gitlab.com/ta-microservices` via `go.mod`, ALWAYS ensure you are pulling their latest tagged version using `go get gitlab.com/ta-microservices/<dependency>@latest`. Do NOT use outdated versions.

### Step 7: Lint & Build

```bash
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>

# 1. Generate proto (if .proto files changed)
make api

# 2. Regenerate Wire (if DI providers changed) — BOTH binaries
cd cmd/<serviceName> && wire
cd ../worker && wire      # if worker binary exists

# 3. Lint (target: zero warnings)
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>
golangci-lint run

# 4. Build
go build ./...

# 5. Run tests
go test ./...
```

> [!NOTE]
> **Never manually edit `wire_gen.go` or `*.pb.go`** — these files are auto-generated. Always use `wire` and `make api` to regenerate.

### Step 8: Deployment Readiness (GitOps Alignment)

Before release, verify config alignment between code and GitOps.

> [!IMPORTANT]
> **Port allocation MUST follow [PORT_ALLOCATION_STANDARD.md](../../../gitops/docs/PORT_ALLOCATION_STANDARD.md).** Look up the correct HTTP/gRPC ports for `<serviceName>` in the Port Allocation Table and verify all references match.

```bash
# 0. Look up correct ports from standard
grep '<serviceName>' /Users/tuananh/Desktop/myproject/microservice/gitops/docs/PORT_ALLOCATION_STANDARD.md

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
- [ ] **HPA sync-wave set correctly**: MUST be at least **1 level higher** than the Deployment wave.
- [ ] NetworkPolicy allows required egress/ingress
- [ ] Migration strategy safe for zero-downtime deploy

### Step 9: Docs

#### 9.1 Service documentation
Update or create service docs under **`docs/03-services/<group>/<serviceName>-service.md`**.
> [!NOTE]
> **Service documentation is an introduction to the service, its architecture, and its capabilities.** It is NOT a checklist or a place to track TODOs/review findings.

- `core-services`: order, catalog, customer, payment, auth, user
- `operational-services`: notification, analytics, search, review, warehouse, fulfillment, shipping, pricing, promotion, loyalty-rewards, location
- `platform-services`: gateway, common-operations

#### 9.2 README.md
Update **`<serviceName>/README.md`** using the template at `docs/templates/readme-template.md`.

#### 9.3 CHANGELOG.md
Update **`<serviceName>/CHANGELOG.md`** (create if not exists) using conventional changelog format.

> [!IMPORTANT]
> **Do NOT commit `docs/` repo changes separately.** The `docs/` directory is a separate git repository (`master` branch). Doc file edits (service doc, review checklist) are written to disk but are **not committed** as part of the service review workflow — the user manages `docs/` repo commits independently.
>
> **Only** `<serviceName>/CHANGELOG.md` and `<serviceName>/README.md` (inside the service repo) are committed, as part of Step 8.

#### 9.4 Documentation checklist
- [ ] Current and accurate information
- [ ] Working commands (tested)
- [ ] Correct ports and endpoints
- [ ] Valid configuration examples

### Step 10: Commit & Release

> [!IMPORTANT]
> **CI/CD builds Docker images and updates GitOps tags automatically.** Never build Docker images locally. Never manually update `newTag` in gitops kustomization.

#### 10.1 Commit order (when multiple components changed)
1. `common/` → commit + tag (`v1.x.y`) + push
2. `<serviceName>/` → `go get common@v1.x.y` + commit + push
3. CI/CD builds image + updates gitops tag auto

#### 10.2 Commit

```bash
cd /Users/tuananh/Desktop/myproject/microservice/<serviceName>
rm -rf bin/ # ALWAYS check and remove bin directory before committing
git add -A
git commit -m "<type>(<serviceName>): <description>"
```

#### 10.3 Push & Release

```bash
# Push to remote
git push origin main

# IF RELEASE:
git tag -a v1.0.7 -m "v1.0.7: description"
git push origin v1.0.7
```

#### 10.4 GitOps (only for config changes)

```bash
# Only if you changed files in gitops/ (e.g. gateway.yaml, configmap.yaml)
cd /Users/tuananh/Desktop/myproject/microservice/gitops
# ⚠️ ALWAYS pull before commit — gitops is shared across all services
git pull --rebase origin main
git add apps/<serviceName>/
git commit -m "fix(<serviceName>): <description>"
git push origin main
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

### 🔧 Action Plan
| # | Severity | Issue | File:Line | Fix | Status |
|---|----------|-------|-----------|-----|--------|
| 1 | P0 | ... | ... | ... | ✅ Done / ⬜ TODO |

### 📈 Test Coverage
| Layer | Coverage | Target | Status |
|-------|----------|--------|--------|
| Biz | X% | 60% | ✅ / ⚠️ |
| Service | X% | 60% | ✅ / ⚠️ |
| Data | X% | 60% | ✅ / ⚠️ |

Coverage checklist updated: ✅ / ❌

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

---

## Quick Reference Checklist

Use this checklist to ensure all steps are completed:

### Pre-Review
- [ ] Pulled latest code (service, common, gitops)
- [ ] Identified service name and structure

### Code Review
- [ ] Indexed codebase (cmd/, internal/, api/, migrations/)
- [ ] Reviewed against coding standards
- [ ] Listed P0/P1/P2 issues with file:line references
- [ ] Checked cross-service impact (proto, events, imports)
- [ ] Verified config/GitOps alignment

### Action & Testing
- [ ] Created action plan for P0/P1 issues
- [ ] Implemented bug fixes
- [ ] Ran test coverage check
- [ ] Updated TEST_COVERAGE_CHECKLIST.md

### Dependencies
- [ ] Checked/tagged common if changed
- [ ] Removed replace directives
- [ ] Updated to latest versions (@latest)

### Build & Quality
- [ ] Generated proto (make api)
- [ ] Regenerated Wire (both binaries if dual-binary)
- [ ] Ran golangci-lint (0 warnings)
- [ ] Built successfully (go build ./...)
- [ ] Ran tests (go test ./...)

### Deployment
- [ ] Verified port allocation matches standard
- [ ] Checked health probes configured
- [ ] Verified resource limits set
- [ ] Confirmed HPA sync-wave correct
- [ ] Validated migration safety

### Documentation
- [ ] Updated service doc (docs/03-services/<group>/)
- [ ] Updated README.md
- [ ] Updated CHANGELOG.md
- [ ] Removed bin/ directory

### Release
- [ ] Committed with conventional format
- [ ] Tagged version (if releasing)
- [ ] Pushed to remote
- [ ] Updated GitOps (if config changed)

---

## Related Skills

- **review-code**: For quick code review of specific changes
- **navigate-service**: For understanding service structure
- **troubleshoot-service**: For debugging build/runtime issues
- **add-api-endpoint**: For adding new endpoints after review
