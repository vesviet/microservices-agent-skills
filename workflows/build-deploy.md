---
description: How to build and deploy a microservice
---

## Build & Deploy Workflow

This is the standard workflow for deploying code changes to development, staging, or production environments.

### When to Use
- After making code changes
- After fixing bugs
- After code review approval
- For routine deployments

### Prerequisites
- Code changes completed and tested locally
- All tests passing
- Lint checks passing
- No breaking changes (or properly versioned)

### Critical Rules

**NEVER build Docker images locally**
- Always commit & push
- CI/CD builds the image automatically
- Local builds are not pushed to registry

**NEVER manually update `newTag` in gitops**
- CI/CD pipeline automatically updates the image tag
- Manual edits will be overwritten
- Tag format: short git commit hash (e.g., `2c23782`)

**To verify CI build is done**:
```bash
cd /home/user/microservices/gitops && git pull origin main
cat apps/<service>/base/kustomization.yaml | grep newTag
# If newTag matches your commit hash, CI has finished
```

### Workflow Steps

#### Phase 1: Pre-Deployment Checks

**1.1 Verify Code Quality**

```bash
cd /home/user/microservices/<service>

# Run tests
go test ./... -v

# Run lint
golangci-lint run

# Build
go build ./...
```

All checks must pass before proceeding.

**1.2 Quick Code Review**

> ⚠️ **Mandatory gate**: Run a quick review before deploying. Use the `review-code` skill (Mode A) to check for P0/P1 issues.

```bash
# Review changed files
git diff --name-only HEAD~1

# Check for common anti-patterns:
# - Missing error wrapping
# - Biz layer calling DB directly
# - Unmanaged goroutines
# - Missing input validation at service layer
```

**1.2 Check for Breaking Changes**

If you made API changes:
```bash
# Check proto changes
git diff HEAD~1 api/<service>/v1/<service>.proto

# Verify backward compatibility
# - No removed fields
# - No renamed RPCs
# - New fields are optional
```

#### Phase 2: Commit Changes

**2.1 Remove Build Artifacts**

```bash
cd /home/user/microservices/<service>
rm -rf bin/
```

**2.2 Stage Changes**

```bash
git add -A
```

**2.3 Commit with Conventional Format**

```bash
git commit -m "<type>(<service>): <description>

[Optional detailed description]
[Optional breaking changes note]"
```

**Commit types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `docs`: Documentation only
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
# Feature
git commit -m "feat(order): add order history endpoint"

# Bug fix
git commit -m "fix(payment): handle null payment method"

# Refactoring
git commit -m "refactor(catalog): extract price calculation logic"

# With details
git commit -m "feat(order): add order cancellation

- Added CancelOrder RPC
- Implemented refund logic
- Added cancellation event"
```

#### Phase 3: Push & Deploy

**3.1 Push to Remote**

```bash
git push origin main
```

This triggers:
1. GitLab CI pipeline
2. Docker image build
3. Image push to registry
4. GitOps tag update
5. ArgoCD sync

**3.2 Monitor CI Pipeline**

```bash
# Check GitLab CI pipeline status
# Visit: https://gitlab.com/ta-microservices/<service>/-/pipelines
```

Wait for pipeline to complete (typically 2-5 minutes).

#### Phase 4: Verify Deployment

**4.1 Check GitOps Update**

```bash
# Pull latest gitops
cd /home/user/microservices/gitops && git pull origin main

# Verify tag updated
cat apps/<service>/base/kustomization.yaml | grep newTag

# Should show your commit hash
# newTag: abc1234
```

**4.2 Watch Pods Rolling Out**

```bash
# Development
$DEV_SSH "kubectl get pods -n <service>-dev -w"

# Staging
$DEV_SSH "kubectl get pods -n <service>-staging -w"

# Production
$DEV_SSH "kubectl get pods -n <service>-prod -w"
```

Wait for:
- Old pods terminating
- New pods starting
- New pods becoming Ready (2/2)

**4.3 Check Logs**

```bash
# Check for errors in new pods
$DEV_SSH "kubectl logs -n <service>-dev -l app=<service> --tail=50"

# Follow logs
$DEV_SSH "kubectl logs -n <service>-dev -l app=<service> --tail=50 -f"
```

Look for:
- ✅ Service started successfully
- ✅ Database connected
- ✅ Redis connected
- ✅ Consul registered
- ❌ No error messages
- ❌ No panic traces

**4.4 Verify Health**

```bash
# Health check
curl http://<service>-dev.tanhdev.com/health/live
curl http://<service>-dev.tanhdev.com/health/ready

# Should return: {"status":"ok"}
```

**4.5 Smoke Test**

Test critical endpoints:
```bash
# Example: Test main endpoint
curl -X POST http://<service>-dev.tanhdev.com/api/v1/<service>/<resource> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'

# Verify response is correct
```

#### Phase 5: Post-Deployment

**5.1 Monitor for Issues**

Monitor for 10-15 minutes after deployment:
- Check error rates in logs
- Check response times
- Check for any alerts

**5.2 Rollback if Needed**

If issues detected:
```bash
cd /home/user/microservices/gitops

# Revert to previous tag
git log --oneline apps/<service>/base/kustomization.yaml
git revert HEAD

# Or manually update to previous tag
vim apps/<service>/base/kustomization.yaml
# Change newTag to previous working version

git add apps/<service>/base/kustomization.yaml
git commit -m "revert(<service>): rollback to previous version"
git push origin main
```

**5.3 Update Documentation (if needed)**

If deployment includes significant changes:
```bash
# Update service documentation
vim docs/03-services/<group>/<service>-service.md

# Update CHANGELOG
vim <service>/CHANGELOG.md
```

### Deployment Targets

#### Development (dev)
- **Purpose**: Active development and testing
- **Stability**: Unstable, frequent deployments
- **Auto-deploy**: Yes, on every push to main
- **Namespace**: `<service>-dev`

#### Staging (staging)
- **Purpose**: Pre-production testing
- **Stability**: Stable, tested features
- **Auto-deploy**: Manual promotion from dev
- **Namespace**: `<service>-staging`

#### Production (prod)
- **Purpose**: Live customer traffic
- **Stability**: Very stable, thoroughly tested
- **Auto-deploy**: Manual promotion with approval
- **Namespace**: `<service>-prod`

### Troubleshooting

#### Issue: CI Pipeline Fails

**Check**:
```bash
# View pipeline logs in GitLab
# Common causes:
# - Tests failing
# - Lint errors
# - Build errors
# - Docker build errors
```

**Solution**:
```bash
# Fix the issue locally
# Run tests and lint
go test ./... -v
golangci-lint run

# Commit fix
git add -A
git commit -m "fix(<service>): fix CI pipeline issue"
git push origin main
```

#### Issue: Pods Not Starting

**Check**:
```bash
# Describe pod
$DEV_SSH "kubectl describe pod <pod-name> -n <service>-dev"

# Common causes:
# - Image pull error
# - Config error
# - Resource limits
# - Health probe failing
```

**Solution**: See [Troubleshooting Workflow](troubleshooting.md)

#### Issue: Service Not Responding

**Check**:
```bash
# Check if pods are ready
$DEV_SSH "kubectl get pods -n <service>-dev"

# Check logs
$DEV_SSH "kubectl logs -n <service>-dev -l app=<service> --tail=100"

# Check service
$DEV_SSH "kubectl get svc -n <service>-dev"
```

**Solution**: See [Troubleshooting Workflow](troubleshooting.md)

### Checklist

- [ ] Code changes completed
- [ ] Tests passing locally
- [ ] Lint passing (0 warnings)
- [ ] Build successful
- [ ] No breaking changes (or versioned)
- [ ] Removed bin/ directory
- [ ] Committed with conventional format
- [ ] Pushed to remote
- [ ] CI pipeline completed successfully
- [ ] GitOps tag updated
- [ ] Pods rolled out successfully
- [ ] Logs checked (no errors)
- [ ] Health checks passing
- [ ] Smoke test passed
- [ ] Monitored for 10-15 minutes
- [ ] No issues detected

### Time Estimate

- **Preparation**: 5 minutes
- **Commit & Push**: 2 minutes
- **CI/CD**: 2-5 minutes
- **Verification**: 5-10 minutes
- **Total**: 15-25 minutes

### Related Workflows
- [Add New Feature](add-new-feature.md) - Before deploying new features
- [Service Review & Release](service-review-release.md) - Before major releases
- [Troubleshooting](troubleshooting.md) - If deployment issues occur
- [Hotfix Production](hotfix-production.md) - For emergency fixes

### Related Skills
- commit-code
- troubleshoot-service
- debug-k8s
