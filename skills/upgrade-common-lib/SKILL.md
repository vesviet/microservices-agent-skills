---
name: upgrade-common-lib
description: Bulk upgrade common library version across all microservices after a new common tag
---

# Upgrade Common Library Skill

Use this skill when `common` has been tagged with a new version and all services need to be updated.

## When to Use
- After committing + tagging a new `common` version
- When services have stale `common` imports (version drift)
- When a new utility in `common` needs to be available across services

---

## ⚠️ CRITICAL RULES

1. **Common MUST be tagged first** — never start upgrading services before common is pushed + tagged
2. **Build each service** after upgrade — don't batch-commit without verifying builds
3. **No `replace` directives** — if any service has `replace gitlab.com/ta-microservices/...`, remove it
4. **Update ALL ta-microservices deps** — not just common, also any cross-service imports

---

## Step-by-Step Process

### Step 1: Verify Common is Tagged

```bash
cd common && git log --oneline -3
git tag --sort=-creatordate | head -5
# Confirm the target tag exists and is pushed
```

### Step 2: Bulk Upgrade All Services

Run this for each service that imports common:

```bash
# List all services that import common
grep -rl 'gitlab.com/ta-microservices/common' */go.mod | sed 's|/go.mod||'
```

For each service:
```bash
cd <service>

# 1. Remove any replace directives
grep 'replace gitlab.com/ta-microservices' go.mod && \
  sed -i '/replace gitlab.com\/ta-microservices/d' go.mod

# 2. Update common to latest tag
go get gitlab.com/ta-microservices/common@latest

# 3. Update any other ta-microservices dependencies
grep 'gitlab.com/ta-microservices/' go.mod | grep -v common | awk '{print $1}' | \
  xargs -I{} go get {}@latest 2>/dev/null || true

# 4. Tidy
go mod tidy

# 5. Build
go build ./...
```

### Step 3: Verify All Builds Pass

```bash
# Quick check: build all services
for svc in auth user customer catalog order payment warehouse fulfillment shipping location pricing promotion loyalty-rewards review search analytics notification checkout return common-operations gateway; do
  echo "=== Building $svc ==="
  (cd $svc && go build ./... 2>&1) && echo "✅ $svc" || echo "❌ $svc FAILED"
done
```

### Step 4: Commit Services That Pass

For each passing service:
```bash
cd <service>
rm -rf bin/
git add go.mod go.sum vendor/
git commit -m "chore(<service>): upgrade common to <version>"
git push origin main
```

---

## Handling Build Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `undefined: common.NewFunc` | New function not in the imported version | Verify the correct tag is being fetched |
| `ambiguous import` | Circular dependency | Check `go.mod` for cross-service imports |
| `proto mismatch` | Proto regeneration needed | Run `make api` then rebuild |
| `wire injection error` | DI graph changed | Run `wire` in `cmd/<service>/` and `cmd/worker/` |

---

## Checklist

- [ ] Common tagged and pushed (`git tag -a v1.x.y && git push origin v1.x.y`)
- [ ] All services updated (`go get common@latest`)
- [ ] Replace directives removed
- [ ] All services build (`go build ./...`)
- [ ] Passing services committed and pushed
- [ ] Failing services documented with root cause

---

## Related Skills

- **commit-code**: Commit service changes after upgrade
- **use-common-lib**: Reference common library packages
- **troubleshoot-service**: Debug build failures after upgrade
