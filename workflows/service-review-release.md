---
description: Complete workflow for reviewing and releasing a microservice to production
---

## Service Review & Release Workflow

This workflow guides you through the complete process of reviewing a service for production readiness and releasing it.

### When to Use
- Before major feature merge
- Before production deployment
- Periodic service health checks
- After significant refactoring

### Prerequisites
- Service name identified
- Access to service repository
- Access to gitops repository
- Understanding of service purpose

### Workflow Steps

#### Phase 1: Preparation

**1.1 Sync Latest Code**

```bash
# Pull latest for service, common, and gitops
cd /home/user/microservices/<service> && git pull origin main
cd /home/user/microservices/common && git pull origin main
cd /home/user/microservices/gitops && git pull origin main
```

**1.2 Review Standards**

Read these documents before starting:
- [Coding Standards](../../docs/07-development/standards/coding-standards.md)
- [Team Lead Code Review Guide](../../docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)
- [Development Review Checklist](../../docs/07-development/standards/development-review-checklist.md)

#### Phase 2: Code Review

Use skill: `review-service`

**2.1 Index Codebase**

Use skill: `navigate-service`

```bash
cd /home/user/microservices/<service>
tree -L 3 -I 'vendor|node_modules'
```

**2.2 Review Architecture**

Check:
- [ ] Clean Architecture layers (service → biz → data)
- [ ] No layer violations (biz doesn't call DB directly)
- [ ] Repository pattern used
- [ ] Dependency injection via Wire

**2.3 Review API Contracts**

```bash
# Check proto definitions
cat api/<service>/v1/<service>.proto

# Check for breaking changes
git diff HEAD~10 api/<service>/v1/<service>.proto
```

**2.4 Review Business Logic**

```bash
# Review biz layer
ls -la internal/biz/
# Check for proper error handling, context propagation
```

**2.5 Review Data Layer**

```bash
# Check migrations
ls -la migrations/
# Verify transactions, no N+1 queries
```

**2.6 List Issues**

Create issue list with severity:
- **P0 (Blocking)**: Security, data inconsistency, breaking changes
- **P1 (High)**: Performance, missing observability
- **P2 (Normal)**: Documentation, code style

#### Phase 3: Cross-Service Impact Analysis

**3.1 Check Proto Dependencies**

```bash
# Who depends on this service?
grep -r 'gitlab.com/ta-microservices/<service>' --include='go.mod' /home/user/microservices/*/go.mod
```

**3.2 Check Event Dependencies**

```bash
# Who consumes this service's events?
grep -r 'Topic.*<service>' /home/user/microservices/*/internal/ --include='*.go' -l
```

**3.3 Verify Backward Compatibility**

- [ ] Proto field numbers preserved
- [ ] New fields are optional
- [ ] No RPC signature changes
- [ ] Event schemas additive-only

#### Phase 4: Bug Fixes & Improvements

**4.1 Create Action Plan**

Document P0/P1 issues in:
`docs/10-appendix/workflow/<service>-review-checklist.md`

**4.2 Implement Fixes**

For each P0 issue:
1. Identify root cause
2. Implement fix in correct layer
3. Test the fix
4. Mark as done

**4.3 Run Tests**

```bash
cd /home/user/microservices/<service>
go test ./internal/... -v
```

#### Phase 5: Test Coverage

**5.1 Check Coverage**

```bash
# Full coverage
go test ./internal/... -count=1 -cover

# Detailed coverage for service layer
go test ./internal/service/... -count=1 -coverprofile=/tmp/<service>_cover.out
go tool cover -func=/tmp/<service>_cover.out | tail -30
```

**5.2 Update Coverage Checklist**

Edit: `docs/10-appendix/checklists/test/TEST_COVERAGE_CHECKLIST.md`

Update:
- Current coverage numbers
- Status (⚠️ → ✅ if crossed 60%)
- Work done description
- Last updated timestamp

#### Phase 6: Dependencies

**6.1 Check Common Changes**

```bash
cd /home/user/microservices/common && git status
```

If common changed:
```bash
cd /home/user/microservices/common
golangci-lint run && go build ./... && go test ./...
rm -rf bin/
git add -A && git commit -m "feat(common): <description>"
git tag -a v1.x.y -m "v1.x.y: <summary>"
git push origin main && git push origin v1.x.y
```

**6.2 Update Service Dependencies**

```bash
cd /home/user/microservices/<service>

# Remove any replace directives
grep 'replace gitlab.com/ta-microservices' go.mod
# If found, remove them

# Update to latest
go get gitlab.com/ta-microservices/common@latest
go get gitlab.com/ta-microservices/<other-dep>@latest
go mod tidy
```

#### Phase 7: Build & Quality

**7.1 Generate Proto (if changed)**

```bash
cd /home/user/microservices/<service>
make api
```

**7.2 Regenerate Wire (if DI changed)**

```bash
cd cmd/<service> && wire
cd ../worker && wire  # if exists
```

**7.3 Lint**

```bash
cd /home/user/microservices/<service>
golangci-lint run
```

Target: 0 warnings

**7.4 Build**

```bash
go build ./...
```

**7.5 Run Tests**

```bash
go test ./...
```

#### Phase 8: Deployment Readiness

**8.1 Check Port Allocation**

```bash
# Look up correct ports
grep '<service>' /home/user/microservices/gitops/docs/PORT_ALLOCATION_STANDARD.md
```

**8.2 Verify Config Alignment**

```bash
# Check env vars in code
grep -rn 'os.Getenv\|viper.Get' <service>/internal/ --include='*.go'

# Compare with gitops
cat gitops/apps/<service>/base/configmap.yaml

# Verify ports match
grep 'addr:' <service>/configs/config.yaml
grep 'containerPort:' gitops/apps/<service>/base/deployment.yaml
grep 'targetPort:' gitops/apps/<service>/base/service.yaml
```

**8.3 Check Resource Limits**

```bash
grep -A5 'resources:' gitops/apps/<service>/base/deployment.yaml
```

**8.4 Verify Health Probes**

```bash
grep -A5 'livenessProbe:\|readinessProbe:' gitops/apps/<service>/base/deployment.yaml
```

**8.5 Check HPA**

```bash
ls gitops/apps/<service>/base/hpa.yaml 2>/dev/null || echo "⚠️ No HPA configured"
```

#### Phase 9: Documentation

**9.1 Update Service Documentation**

Edit: `docs/03-services/<group>/<service>-service.md`

Groups:
- `core-services`: order, catalog, customer, payment, auth, user
- `operational-services`: notification, analytics, search, review, warehouse, fulfillment, shipping, pricing, promotion, loyalty-rewards, location
- `platform-services`: gateway, common-operations

**9.2 Update README.md**

Edit: `<service>/README.md`

Use template: `docs/templates/readme-template.md`

**9.3 Update CHANGELOG.md**

Edit: `<service>/CHANGELOG.md`

```markdown
## [Unreleased]
### Added
- Feature X
### Fixed
- Bug Y
### Changed
- Improvement Z
```

#### Phase 10: Commit & Release

**10.1 Remove Bin Directory**

```bash
cd /home/user/microservices/<service>
rm -rf bin/
```

**10.2 Commit Changes**

```bash
git add -A
git commit -m "<type>(<service>): <description>

- Detailed change 1
- Detailed change 2
- Detailed change 3"
```

**10.3 Push to Remote**

```bash
git push origin main
```

**10.4 Create Release Tag (if releasing)**

```bash
# Update CHANGELOG.md first (move [Unreleased] to version)
git add CHANGELOG.md
git commit -m "docs(<service>): update changelog for v1.x.y"

# Create annotated tag
git tag -a v1.x.y -m "v1.x.y: <summary>

Added:
- Feature A
- Feature B

Fixed:
- Bug X
- Bug Y"

# Push tag
git push origin v1.x.y
```

**10.5 Update GitOps (if config changed)**

```bash
cd /home/user/microservices/gitops
git pull --rebase origin main
git add apps/<service>/
git commit -m "fix(<service>): <description>"
git push origin main
```

#### Phase 11: Verification

**11.1 Wait for CI/CD**

```bash
# Check if CI finished
cd /home/user/microservices/gitops && git pull origin main
cat apps/<service>/base/kustomization.yaml | grep newTag
```

**11.2 Monitor Deployment**

```bash
# Watch pods
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl get pods -n <service>-dev -w"

# Check logs
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <service>-dev -l app=<service> --tail=100 -f"
```

**11.3 Verify Health**

```bash
# Check health endpoint
curl http://<service>-dev.tanhdev.com/health/live
curl http://<service>-dev.tanhdev.com/health/ready
```

**11.4 Smoke Test**

Test critical endpoints to ensure service is working.

### Review Output Template

```markdown
## 🔍 Service Review: <service>

**Date**: YYYY-MM-DD
**Reviewer**: [Name]
**Status**: ✅ Ready / ⚠️ Needs Work / ❌ Not Ready

### 📊 Issue Summary
| Severity | Count | Status |
|----------|-------|--------|
| P0 | X | Fixed / Remaining |
| P1 | X | Fixed / Remaining |
| P2 | X | Fixed / Remaining |

### 🔴 P0 Issues (Blocking)
1. [ARCH] file:line — Description

### 🟡 P1 Issues (High)
1. [PERF] file:line — Description

### 🔵 P2 Issues (Normal)
1. [DOC] file:line — Description

### ✅ Completed Actions
1. Fixed: description

### 📈 Test Coverage
| Layer | Coverage | Target | Status |
|-------|----------|--------|--------|
| Biz | X% | 60% | ✅/⚠️ |
| Service | X% | 60% | ✅/⚠️ |
| Data | X% | 60% | ✅/⚠️ |

### 🌐 Cross-Service Impact
- Services importing proto: [list]
- Services consuming events: [list]
- Backward compatibility: ✅ Preserved

### 🚀 Deployment Readiness
- Config aligned: ✅
- Health probes: ✅
- Resource limits: ✅
- Migration safety: ✅

### Build Status
- golangci-lint: ✅ 0 warnings
- go build: ✅ Pass
- wire: ✅ Generated
- bin/ removed: ✅

### Documentation
- Service doc: ✅
- README.md: ✅
- CHANGELOG.md: ✅
```

### Checklist

- [ ] Synced latest code (service, common, gitops)
- [ ] Indexed codebase structure
- [ ] Reviewed against standards
- [ ] Listed P0/P1/P2 issues
- [ ] Checked cross-service impact
- [ ] Created action plan
- [ ] Implemented bug fixes
- [ ] Ran test coverage
- [ ] Updated coverage checklist
- [ ] Tagged common (if changed)
- [ ] Removed replace directives
- [ ] Updated dependencies
- [ ] Generated proto
- [ ] Regenerated Wire
- [ ] Ran golangci-lint (0 warnings)
- [ ] Built successfully
- [ ] Ran tests
- [ ] Verified port allocation
- [ ] Checked config alignment
- [ ] Verified health probes
- [ ] Checked resource limits
- [ ] Updated service doc
- [ ] Updated README.md
- [ ] Updated CHANGELOG.md
- [ ] Removed bin/ directory
- [ ] Committed changes
- [ ] Tagged version (if releasing)
- [ ] Pushed to remote
- [ ] Updated GitOps (if needed)
- [ ] Verified deployment
- [ ] Smoke tested

### Related Workflows
- [Build & Deploy](build-deploy.md)
- [Add New Feature](add-new-feature.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills
- review-service
- navigate-service
- review-code
- commit-code
