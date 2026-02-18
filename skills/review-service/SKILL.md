---
name: review-service
description: Full service review & release — index codebase, cross-reference GitOps, fix P0/P1/P2 issues, commit and tag both repos
---

# Review Service Skill

Operational step-by-step process for reviewing and releasing any microservice. Codifies the exact workflow validated across analytics, gateway, and location service reviews.

> **Trigger**: User says "review service X", "review and release X", or references `service-review-release-prompt.md`

---

## Prerequisites

Before starting, you MUST read these three standards (they define severity levels and review criteria):

1. **[Coding Standards](docs/07-development/standards/coding-standards.md)** — Go style, layers, errors
2. **[Team Lead Code Review Guide](docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)** — P0/P1/P2 severity
3. **[Development Review Checklist](docs/07-development/standards/development-review-checklist.md)** — Quality gates

Also read the PORT_ALLOCATION_STANDARD — it is the single source of truth for ports:
- **[PORT_ALLOCATION_STANDARD](gitops/docs/PORT_ALLOCATION_STANDARD.md)**

---

## Phase 1: Index & Review (PLANNING mode)

### Step 1.1: Parallel initial indexing

Run ALL of these in parallel to maximize speed:

```
// All parallel:
list_dir:     {serviceName}/
list_dir:     gitops/apps/{serviceName}/base/
find_by_name: *.go in {serviceName}/ (get full file inventory)
view_file:    docs/07-development/standards/service-review-release-prompt.md (if not cached)
```

### Step 1.2: Read critical config files (parallel batch)

```
// All parallel:
view_file: {serviceName}/configs/config.yaml
view_file: {serviceName}/go.mod
view_file: {serviceName}/internal/config/config.go
view_file: {serviceName}/cmd/{serviceName}/main.go
```

**Key checks on go.mod:**
- [ ] No `replace gitlab.com/ta-microservices` directives (breaks CI/CD)
- [ ] `common` version — note exact version for later comparison
- [ ] Other service dependencies (shipping, user, warehouse, etc.)

### Step 1.3: Read ALL GitOps base manifests (parallel batch)

```
// All parallel:
view_file: gitops/apps/{serviceName}/base/deployment.yaml
view_file: gitops/apps/{serviceName}/base/service.yaml
view_file: gitops/apps/{serviceName}/base/configmap.yaml
view_file: gitops/apps/{serviceName}/base/networkpolicy.yaml
view_file: gitops/apps/{serviceName}/base/servicemonitor.yaml
```

Also check if these exist (may or may not):
- `hpa.yaml` — HorizontalPodAutoscaler
- `pdb.yaml` — PodDisruptionBudget
- `ingress.yaml` — Ingress (usually only gateway)
- `migration-job.yaml` — Migration Job
- `serviceaccount.yaml` — ServiceAccount
- Worker deployment: `{serviceName}-worker.yaml` or separate worker deployment

### Step 1.4: Port cross-reference table (CRITICAL)

Build this table from PORT_ALLOCATION_STANDARD and compare ALL config sources. This single check has found P0 issues in EVERY service reviewed so far.

| Source | HTTP Port | gRPC Port | Status |
|---|---|---|---|
| **PORT_ALLOCATION_STANDARD** | `80XX` | `90XX` | Authoritative |
| deployment.yaml `containerPort` | ? | ? | Must match standard |
| service.yaml `targetPort` | ? | ? | Must match standard |
| base ConfigMap `config.yaml` (embedded) | ? | ? | Must match standard |
| overlay ConfigMap env vars | ? | ? | Must match standard |
| local `configs/config.yaml` | ? | ? | Should match standard |
| NetworkPolicy ingress ports | ? | ? | Must match standard |
| Dapr `app-port` annotation | ? | ? | Must match standard |
| Health probe ports | ? | ? | Must match standard |
| README.md port references | ? | ? | Should match standard |

> **Known pattern from past reviews**: Port values are frequently copied from other services during scaffolding and never updated. Check for checkout ports (8010), auth ports (8000), search ports (8017), loyalty ports (8014) appearing where they shouldn't.

### Step 1.5: Deployment checklist

Check deployment.yaml for ALL of:

- [ ] **Security context** — `runAsNonRoot: true`, `runAsUser: 65532`
- [ ] **Dapr annotations** — `dapr.io/enabled`, `dapr.io/app-id`, `dapr.io/app-port`, `dapr.io/app-protocol`
- [ ] **Health probes** — liveness + readiness with correct port and path
- [ ] **envFrom** — `configMapRef: overlays-config` (env var overrides from overlay)
- [ ] **Resource limits** — requests + limits for CPU and memory
- [ ] **Volume mounts** — config.yaml mounted correctly

### Step 1.6: ServiceMonitor check

- [ ] Port name in ServiceMonitor MUST match port name in service.yaml
  - Common bug: ServiceMonitor says `http-svc`, service.yaml says `http` → Prometheus can't scrape

### Step 1.7: Overlay check

```
// Parallel:
list_dir:  gitops/apps/{serviceName}/overlays/
view_file: gitops/apps/{serviceName}/overlays/dev/kustomization.yaml
view_file: gitops/apps/{serviceName}/overlays/dev/configmap.yaml  (if exists)
view_file: gitops/apps/{serviceName}/overlays/dev/secrets.yaml    (if exists)
```

**Check for:**
- [ ] Overlay `configmap.yaml` env vars have correct port values
- [ ] No plaintext secrets in ConfigMap (JWT_SECRET, DB passwords → should be in Secret)
- [ ] Secrets reference is mounted in deployment (`secretRef` or volume)

### Step 1.8: Cross-service impact

```bash
# Who depends on this service's proto?
grep -r 'ta-microservices/{serviceName}' --include='go.mod' /home/user/microservices/*/go.mod

# Who consumes this service's events?
grep -r 'Topic.*{serviceName}' /home/user/microservices/common/constants/events.go
```

- [ ] Proto field numbers preserved (no reuse)
- [ ] Event schemas additive-only
- [ ] No circular module imports

### Step 1.9: Code architecture spot check

Use `view_file_outline` on key files (not full read — just verify structure):

```
view_file_outline: internal/biz/{entity}/{entity}_usecase.go
view_file_outline: internal/data/postgres/{entity}.go
view_file_outline: internal/service/{entity}.go
```

**Quick checks:**
- [ ] Service layer is thin (parse → call biz → return)
- [ ] Biz layer doesn't import gorm/DB directly
- [ ] Repository interface defined in biz, implemented in data
- [ ] Error wrapping with context (`fmt.Errorf("...: %w", err)`)

### Step 1.10: Check for stale files

```
find_by_name: *.disabled in {serviceName}/
find_by_name: *REVIEW* or *CHECKLIST* or *FINAL* at root of {serviceName}/
```

---

## Phase 2: Compile Issue List & Plan (PLANNING mode)

### Severity definitions

| Severity | Emoji | Definition | Examples |
|---|---|---|---|
| **P0** | 🔴 | Blocks deployment or causes runtime failure | Port mismatch (pod won't start), missing probes, security vuln, broken config |
| **P1** | 🟡 | Impacts reliability or observability | Missing Dapr, ServiceMonitor mismatch, no HPA, wrong README |
| **P2** | 🔵 | Documentation, style, cleanup | Stale files, missing CHANGELOG, naming |

### Write implementation_plan.md

Must include:
1. Summary of findings
2. Port cross-reference table (from Step 1.4)
3. All P0/P1/P2 issues with file:line references
4. Proposed changes grouped by component
5. Verification plan

### Request user approval via notify_user

---

## Phase 3: Fix All Issues (EXECUTION mode)

> **Code comment rule**: Do NOT add issue-tracking comments (e.g. `# P0: Fixed port`, `// REVIEW-FIX:`, `# was 8015, changed to 8016`) directly in code or YAML files. The code should be clean — issue context belongs ONLY in commit messages and CHANGELOG entries.

### Fix order (most critical first)

1. **Port fixes** — service.yaml, configmap.yaml, local config.yaml
2. **Deployment fixes** — envFrom, Dapr, probes, security context
3. **ServiceMonitor** — port name alignment
4. **Documentation** — README ports, CHANGELOG creation
5. **Stale file cleanup** — delete review docs, disabled files

### Fix patterns (use multi_replace_file_content for efficiency)

```
# Port fix in service.yaml — change targetPort
multi_replace_file_content: service.yaml
  targetPort: WRONG → CORRECT (both HTTP and gRPC)

# Port fix in base ConfigMap config.yaml
multi_replace_file_content: configmap.yaml
  addr: 0.0.0.0:WRONG → 0.0.0.0:CORRECT

# Deployment — add envFrom + Dapr + probes
multi_replace_file_content: deployment.yaml
  1. Add annotations block under template.metadata
  2. Add envFrom before env block
  3. Add probes after env block
```

---

## Phase 4: Verify (VERIFICATION mode)

### Build & test

```bash
# Build (expected: pre-existing Windows syscall.Statfs error from common lib is OK)
go build ./...

# Test specific packages
go test -v ./internal/biz/... ./internal/service/...
```

> **Note**: `go build` may fail on Windows due to `syscall.Statfs` in `common` health checkers. This is a pre-existing cross-platform issue, not caused by our changes. Document it but don't block on it.

### Check latest tag

```bash
git tag --sort=-creatordate | head -5
```

---

## Phase 5: Commit & Release (EXECUTION mode)

> **Execute all `run_command` steps below. Each service is its own git repo — there is NO git repo at `d:\microservices` root.**

### Commit order matters

```
┌──────────────────────────────────────────────────┐
│              COMMIT ORDER                         │
│                                                   │
│  1. common/ → if changed, commit + tag FIRST      │
│  2. {serviceName}/ → commit + tag + push           │
│  3. gitops/ → commit + push (pull --rebase first!) │
└──────────────────────────────────────────────────┘
```

### Step 5.1: Get current tag and compute next version

```bash
# // turbo
cd d:\microservices\{serviceName}
git tag --sort=-creatordate | Select-Object -First 5
```

Determine next version: increment PATCH for review fixes (e.g. v1.0.14 → v1.0.15).

### Step 5.2: Stage ALL changes and commit

> ⚠️ **IMPORTANT**: Commit ALL uncommitted changes in the service repo, not just the files you modified during review. Prior uncommitted work (Dockerfiles, go.mod updates, new tests, refactors, etc.) should be included in this commit.

```bash
cd d:\microservices\{serviceName}
git add -A
git status
```

Review `git status` to confirm all files are staged, then commit:

```bash
cd d:\microservices\{serviceName}
git commit -m "fix({serviceName}): service review — P0/P1/P2 fixes

- P0: <list P0 fixes, one per line>
- P1: <list P1 fixes>
- P2: <list P2 fixes>
- Includes prior uncommitted changes"
```

**Verify clean status after commit:**

```bash
# // turbo
cd d:\microservices\{serviceName}
git status --short
```

If output is not empty, `git add -A` and `git commit --amend --no-edit` to include remaining files.

### Step 5.3: Tag the service

Follow the tag format from **commit-code** skill:

```bash
cd d:\microservices\{serviceName}
git tag -a v{NEXT_VERSION} -m "v{NEXT_VERSION}: service review fixes

Fixed:
- <list P0 fixes>
- <list P1 fixes>
- <list P2 fixes>

Changed:
- <list changes, e.g. README updated, CHANGELOG entry added>"
```

### Step 5.4: Push service + tag

```bash
cd d:\microservices\{serviceName}
git push origin main
git push origin v{NEXT_VERSION}
```

### Step 5.5: Stage and commit GitOps changes

> ⚠️ **ALWAYS pull --rebase before commit** — gitops is shared across all services.
> ⚠️ **NEVER manually update `newTag`** in `overlays/*/kustomization.yaml` — CI/CD handles image tags.

```bash
cd d:\microservices\gitops
git pull --rebase origin main
git add apps/{serviceName}/
git status
```

Review status, then commit:

```bash
cd d:\microservices\gitops
git commit -m "fix({serviceName}): service review — GitOps fixes

- <list GitOps-specific fixes with severity>"
```

### Step 5.6: Push GitOps

```bash
cd d:\microservices\gitops
git push origin main
```

### Step 5.7: Record commit hashes for walkthrough

```bash
# // turbo
cd d:\microservices\{serviceName}
git log -1 --oneline

# // turbo
cd d:\microservices\gitops
git log -1 --oneline
```

Save both commit hashes to include in the walkthrough.md artifact.

---

## Phase 6: Write Walkthrough (VERIFICATION mode)

Create `walkthrough.md` artifact with:
- Issue summary table (P0/P1/P2 counts)
- Changes made (with `render_diffs` for key files)
- Verification results (build, tests)
- Commit details (hashes, tags, both repos)

---

## Common Issues Found in Past Reviews

These are the most frequent issues — check for them first:

| Issue | Frequency | Services Affected |
|---|---|---|
| Port mismatch across configs | **Every service** | analytics, gateway, location |
| ServiceMonitor port name ≠ service.yaml port name | Very common | gateway, location |
| Missing Dapr annotations | Common | location |
| Missing health probes | Common | location |
| Missing `envFrom` for overlay ConfigMap | Common | location |
| Plaintext secrets in ConfigMap | Common | gateway (JWT_SECRET) |
| Stale review docs at root | Occasional | gateway |
| README with wrong ports | Common | location (had 8017 instead of 8007) |
| `go.mod` outdated `common` version | Occasional | varies |

---

## Reference Port Allocation

| Service | HTTP | gRPC |
|---|---|---|
| Auth | 8000 | 9000 |
| User | 8001 | 9001 |
| Pricing | 8002 | 9002 |
| Customer | 8003 | 9003 |
| Order | 8004 | 9004 |
| Payment | 8005 | 9005 |
| Warehouse | 8006 | 9006 |
| Location | 8007 | 9007 |
| Fulfillment | 8008 | 9008 |
| Notification | 8009 | 9009 |
| Checkout | 8010 | 9010 |
| Promotion | 8011 | 9011 |
| Shipping | 8012 | 9012 |
| Return | 8013 | 9013 |
| Loyalty | 8014 | 9014 |
| Catalog | 8015 | 9015 |
| Review | 8016 | 9016 |
| Search | 8017 | 9017 |
| Common Ops | 8018 | 9018 |
| Analytics | 8019 | 9019 |
| Gateway | 80 | 81 |
