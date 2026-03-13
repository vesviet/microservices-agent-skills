---
description: Emergency workflow for hotfixing production issues
---

## Hotfix Production Workflow

This workflow is for **emergency production fixes only**. Use this when there's a critical bug in production that needs immediate attention.

### When to Use
- Production is down or severely degraded
- Critical security vulnerability discovered
- Data corruption or loss risk
- Customer-impacting bug

### Prerequisites
- Issue clearly identified and reproducible
- Root cause understood
- Fix approach validated
- Stakeholders notified

### Workflow Steps

#### Phase 1: Assessment (5-10 minutes)

**1.1 Confirm Severity**

Is this truly a P0 production emergency?
- [ ] Service is down or unavailable
- [ ] Data corruption or loss occurring
- [ ] Security breach or vulnerability
- [ ] Major customer impact (>50% users affected)

If NO to all above → Use normal workflow, not hotfix

**1.2 Identify Affected Service**

```bash
# Check which service is affected
$DEV_SSH "kubectl get pods -A | grep -v Running"

# Check logs for errors
$DEV_SSH "kubectl logs -n <service>-prod -l app=<service> --tail=100"
```

**1.3 Determine Root Cause**

```bash
# Check recent deployments
cd /home/user/microservices/gitops
git log --oneline -10 apps/<service>/

# Check recent code changes
cd /home/user/microservices/<service>
git log --oneline -10
```

#### Phase 2: Immediate Mitigation (5-15 minutes)

**Option A: Rollback to Previous Version**

If the issue was introduced in the latest deployment:

```bash
# Find previous working version
cd /home/user/microservices/gitops
git log --oneline apps/<service>/base/kustomization.yaml

# Rollback to previous commit
git revert HEAD
git push origin main

# Or manually update to previous tag
vim apps/<service>/base/kustomization.yaml
# Change newTag to previous working version

git add apps/<service>/base/kustomization.yaml
git commit -m "hotfix(<service>): rollback to previous version due to <issue>"
git push origin main
```

**Option B: Scale Down (if causing cascading failures)**

```bash
# Scale down to 0 replicas temporarily
$DEV_SSH "kubectl scale deployment <service> -n <service>-prod --replicas=0"

# This gives time to fix without affecting other services
```

**Option C: Apply Quick Config Fix**

If it's a configuration issue:

```bash
cd /home/user/microservices/gitops
vim apps/<service>/overlays/production/configmap.yaml
# Fix the config

git add apps/<service>/overlays/production/
git commit -m "hotfix(<service>): fix production config for <issue>"
git push origin main
```

#### Phase 3: Develop Fix (15-30 minutes)

**3.1 Create Hotfix Branch**

```bash
cd /home/user/microservices/<service>

# Create hotfix branch from production tag
git checkout -b hotfix/<issue-description> v1.x.y  # Use current prod version

# Or from main if prod is on main
git checkout -b hotfix/<issue-description> main
```

**3.2 Implement Minimal Fix**

**CRITICAL RULES:**
- Fix ONLY the specific issue
- NO refactoring
- NO new features
- NO unrelated changes
- Minimal code changes

```bash
# Make the fix
vim internal/<layer>/<file>.go

# Example: Fix null pointer
# BAD: Refactor entire function
# GOOD: Add null check only
```

**3.3 Test the Fix Locally**

```bash
# Run unit tests
go test ./internal/<affected-package>/... -v

# Build
go build ./...

# Run locally if possible
go run ./cmd/<service>/...

# Test the specific scenario
curl -X POST http://localhost:8080/api/v1/<endpoint> \
  -H "Content-Type: application/json" \
  -d '<test-data>'
```

**3.4 Verify Fix Doesn't Break Anything**

```bash
# Run all tests
go test ./... -v

# Lint
golangci-lint run

# Check for regressions
go test ./... -race
```

#### Phase 4: Deploy Fix (10-20 minutes)

**4.1 Commit Hotfix**

```bash
cd /home/user/microservices/<service>

# Remove bin
rm -rf bin/

# Commit with clear message
git add -A
git commit -m "hotfix(<service>): fix <specific-issue>

Issue: <description>
Root cause: <explanation>
Fix: <what-was-changed>

Tested: <how-it-was-tested>"
```

**4.2 Create Hotfix Tag**

```bash
# Increment patch version
# If current prod is v1.2.3, hotfix is v1.2.4

git tag -a v1.2.4 -m "v1.2.4: Hotfix for <issue>

Fixed:
- <specific-issue>

Root cause: <explanation>"

# Push
git push origin hotfix/<issue-description>
git push origin v1.2.4
```

**4.3 Deploy to Staging First (if time allows)**

```bash
# Wait for CI to build
cd /home/user/microservices/gitops && git pull origin main

# Verify staging
$DEV_SSH "kubectl get pods -n <service>-staging"
$DEV_SSH "kubectl logs -n <service>-staging -l app=<service> --tail=50"

# Test in staging
curl http://<service>-staging.tanhdev.com/api/v1/<endpoint>
```

**4.4 Deploy to Production**

```bash
cd /home/user/microservices/gitops

# Update production kustomization
vim apps/<service>/overlays/production/kustomization.yaml
# Or if using base:
vim apps/<service>/base/kustomization.yaml

# Change newTag to v1.2.4

git add apps/<service>/
git commit -m "hotfix(<service>): deploy v1.2.4 to production

Fixes: <issue>
Tag: v1.2.4"

git push origin main
```

#### Phase 5: Monitor (30-60 minutes)

**5.1 Watch Deployment**

```bash
# Watch pods rolling out
$DEV_SSH "kubectl rollout status deployment/<service> -n <service>-prod"

# Watch pod status
$DEV_SSH "kubectl get pods -n <service>-prod -w"
```

**5.2 Check Logs**

```bash
# Check for errors
$DEV_SSH "kubectl logs -n <service>-prod -l app=<service> --tail=100 -f"

# Check all pods
$DEV_SSH "kubectl logs -n <service>-prod -l app=<service> --all-containers=true --tail=50"
```

**5.3 Verify Fix**

```bash
# Test the fixed endpoint
curl http://<service>-prod.tanhdev.com/api/v1/<endpoint>

# Check metrics
# - Error rate should decrease
# - Response time should normalize
# - No new errors introduced
```

**5.4 Monitor for 30-60 minutes**

Watch for:
- Error rate returning to normal
- No new errors
- No performance degradation
- Customer reports resolved

#### Phase 6: Post-Hotfix (After stabilization)

**6.1 Merge Hotfix to Main**

```bash
cd /home/user/microservices/<service>

# Checkout main
git checkout main
git pull origin main

# Merge hotfix
git merge hotfix/<issue-description>

# Push
git push origin main
```

**6.2 Update Documentation**

```bash
# Update CHANGELOG.md
vim CHANGELOG.md
```

```markdown
## [1.2.4] - YYYY-MM-DD

### Fixed
- **[HOTFIX]** Fixed <specific-issue> causing <impact>
  - Root cause: <explanation>
  - Impact: <who-was-affected>
  - Resolution: <what-was-done>
```

```bash
git add CHANGELOG.md
git commit -m "docs(<service>): update changelog for hotfix v1.2.4"
git push origin main
```

**6.3 Create Incident Report**

Document in `docs/10-appendix/incidents/`:

```markdown
# Incident Report: <Service> - <Issue>

**Date**: YYYY-MM-DD
**Severity**: P0
**Duration**: X hours
**Affected Users**: X%

## Summary
Brief description of what happened.

## Timeline
- HH:MM - Issue detected
- HH:MM - Root cause identified
- HH:MM - Mitigation applied
- HH:MM - Fix deployed
- HH:MM - Incident resolved

## Root Cause
Detailed explanation of what caused the issue.

## Impact
- Number of affected users
- Duration of impact
- Business impact

## Resolution
What was done to fix the issue.

## Prevention
What will be done to prevent this in the future:
- [ ] Add monitoring/alerting
- [ ] Add tests
- [ ] Update documentation
- [ ] Code review process improvement
```

**6.4 Schedule Post-Mortem**

- Review what went wrong
- Identify improvements
- Update processes
- Add preventive measures

**6.5 Add Preventive Measures**

```bash
# Add test to prevent regression
vim internal/<layer>/<file>_test.go

# Add monitoring/alerting
# Update Prometheus rules or Grafana dashboards

# Update documentation
vim docs/03-services/<group>/<service>-service.md
```

### Hotfix Checklist

#### Pre-Hotfix
- [ ] Confirmed P0 severity
- [ ] Identified affected service
- [ ] Determined root cause
- [ ] Stakeholders notified

#### Immediate Mitigation
- [ ] Rollback applied (if applicable)
- [ ] Or scale down (if applicable)
- [ ] Or config fix (if applicable)
- [ ] Impact contained

#### Fix Development
- [ ] Created hotfix branch
- [ ] Implemented minimal fix
- [ ] Tested locally
- [ ] All tests pass
- [ ] No regressions

#### Deployment
- [ ] Committed with clear message
- [ ] Created hotfix tag
- [ ] Tested in staging (if time allows)
- [ ] Deployed to production
- [ ] Deployment successful

#### Monitoring
- [ ] Watched rollout
- [ ] Checked logs
- [ ] Verified fix works
- [ ] Monitored for 30-60 minutes
- [ ] No new issues

#### Post-Hotfix
- [ ] Merged to main
- [ ] Updated CHANGELOG.md
- [ ] Created incident report
- [ ] Scheduled post-mortem
- [ ] Added preventive measures

### Common Hotfix Scenarios

#### Scenario 1: Null Pointer Exception

```go
// BAD: Causes crash
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user := s.repo.FindByID(ctx, id)
    return user.ToProto(), nil  // Crashes if user is nil
}

// GOOD: Hotfix
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user := s.repo.FindByID(ctx, id)
    if user == nil {
        return nil, errors.NotFound("USER_NOT_FOUND", "user not found")
    }
    return user.ToProto(), nil
}
```

#### Scenario 2: Database Connection Pool Exhausted

```yaml
# BAD: Too few connections
data:
  database:
    max_open_conns: 10
    max_idle_conns: 5

# GOOD: Hotfix config
data:
  database:
    max_open_conns: 100
    max_idle_conns: 50
```

#### Scenario 3: Memory Leak

```go
// BAD: Goroutine leak
func (s *Service) ProcessOrders(ctx context.Context) {
    for {
        orders := s.repo.GetPendingOrders(ctx)
        for _, order := range orders {
            go s.processOrder(order)  // Never cleaned up
        }
    }
}

// GOOD: Hotfix with context
func (s *Service) ProcessOrders(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            orders := s.repo.GetPendingOrders(ctx)
            for _, order := range orders {
                go func(o *Order) {
                    s.processOrder(ctx, o)
                }(order)
            }
        }
    }
}
```

### Emergency Contacts

- **Tech Lead**: [Contact info]
- **DevOps**: [Contact info]
- **On-Call Engineer**: [Contact info]

### Related Workflows
- [Troubleshooting](troubleshooting.md)
- [Service Review & Release](service-review-release.md)
- [Build & Deploy](build-deploy.md)

### Related Skills
- troubleshoot-service
- debug-k8s
- commit-code
