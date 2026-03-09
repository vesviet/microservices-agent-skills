---
name: rollback-deployment
description: Rollback a failed deployment using ArgoCD, kubectl, or GitOps revert strategies
---

# Rollback Deployment Skill

Use this skill when a deployment fails and needs to be rolled back to a previous stable version.

## When to Use
- New deployment causes CrashLoopBackOff or errors
- Service performance degrades after deployment
- Critical bug found in newly deployed version
- Migration broke the database schema
- ArgoCD sync failed and service is unhealthy

---

## ⚠️ CRITICAL RULES

1. **Rollback through GitOps** — revert the gitops commit, not kubectl directly
2. **Never delete pods manually** as primary fix — fix the root cause
3. **Check if migration is reversible** before rolling back code (data loss risk!)
4. **Communicate in team channel** before rollback in prod
5. **NEVER manually update `newTag`** — CI/CD handles image tags

---

## Decision Tree: What Type of Rollback?

```
Deployment Issue
├── Code Bug (logic error, crash)?
│   └── Strategy A: Revert Git Commit → CI rebuilds → Auto-deploy
├── Config Error (wrong env var, missing secret)?
│   └── Strategy B: Fix GitOps Config → Push → ArgoCD Sync
├── Migration Error (bad SQL)?
│   ├── Migration reversible? → Run goose down → Fix → Retry
│   └── Migration NOT reversible? → ⚠️ Manual DB fix required
└── Infrastructure Error (K8s, Dapr, Consul)?
    └── Strategy C: kubectl rollout undo (temporary) + Fix root cause
```

---

## Strategy A: Revert Code (Git Revert)

When the code itself has a bug. CI/CD will rebuild and redeploy.

### Step 1: Identify the Bad Commit

```bash
cd /Users/tuananh/Desktop/myproject/microservice/<service>
git log --oneline -10
```

### Step 2: Revert the Commit

```bash
# Revert specific commit (creates a new revert commit)
git revert <bad-commit-sha> --no-edit

# Or revert multiple commits
git revert <oldest-bad>..<newest-bad> --no-edit
```

### Step 3: Push → CI/CD Rebuilds → ArgoCD Auto-deploys

```bash
git push origin main
# CI pipeline builds new image with revert
# CI updates gitops image tag automatically
# ArgoCD syncs within 3 minutes
```

### Step 4: Verify

```bash
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl get pods -n <service>-dev"
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <service>-dev -l app.kubernetes.io/name=<service> --tail=20"
```

---

## Strategy B: Fix GitOps Config

When environment config (ConfigMap/Secret) is wrong.

### Step 1: Identify the Config Issue

```bash
# Check recent gitops changes
cd /Users/tuananh/Desktop/myproject/microservice/gitops
git log --oneline -5

# Check pod events for clues
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl describe pod -n <service>-dev -l app.kubernetes.io/name=<service> | tail -30"
```

### Step 2: Fix the Config

```bash
# Edit the problematic file
# e.g., gitops/apps/<service>/overlays/dev/configmap.yaml
# e.g., gitops/apps/<service>/overlays/dev/secrets.yaml
```

### Step 3: Verify Kustomize Builds

```bash
kubectl kustomize /Users/tuananh/Desktop/myproject/microservice/gitops/apps/<service>/overlays/dev > /dev/null 2>&1 && echo "✅ OK" || echo "❌ FAIL"
```

### Step 4: Commit, Push, Sync

```bash
cd /Users/tuananh/Desktop/myproject/microservice/gitops
git pull --rebase origin main
git add -A
git commit -m "fix(<service>): revert config change — <reason>"
git push origin main
```

### Step 5: Trigger ArgoCD Hard Refresh

```bash
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl patch application <service>-dev -n argocd \
   --type merge \
   -p '{\"metadata\":{\"annotations\":{\"argocd.argoproj.io/refresh\":\"hard\"}}}'"
```

---

## Strategy C: Emergency kubectl Rollback

When you need **immediate** rollback and can't wait for CI/CD cycle. This is a **temporary** measure — you must fix root cause through GitOps afterwards.

### Rollback Deployment to Previous Revision

```bash
# Check rollout history
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl rollout history deployment/<service>-service -n <service>-dev"

# Rollback to previous revision
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl rollout undo deployment/<service>-service -n <service>-dev"

# Verify
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl rollout status deployment/<service>-service -n <service>-dev --timeout=90s"
```

> ⚠️ **ArgoCD will detect drift** and may re-sync the bad version. Temporarily disable auto-sync if needed:
```bash
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl patch application <service>-dev -n argocd \
   --type merge \
   -p '{\"spec\":{\"syncPolicy\":null}}'"
```

> **Remember to re-enable auto-sync** after fixing through GitOps:
```bash
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl patch application <service>-dev -n argocd \
   --type merge \
   -p '{\"spec\":{\"syncPolicy\":{\"automated\":{\"prune\":true,\"selfHeal\":true}}}}'"
```

---

## Migration Rollback

### If Migration is Reversible (has `-- +goose Down`)

```bash
# Port-forward the database
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl port-forward -n infrastructure svc/postgresql 5432:5432 &"

# Check current migration status
DATABASE_URL="postgres://postgres:microservices@localhost:5432/<service>_db?sslmode=disable" \
  goose -dir migrations postgres "$DATABASE_URL" status

# Rollback last migration
DATABASE_URL="postgres://postgres:microservices@localhost:5432/<service>_db?sslmode=disable" \
  goose -dir migrations postgres "$DATABASE_URL" down
```

### If Migration is NOT Reversible

⚠️ **Manual intervention required:**
1. Connect to the database directly
2. Assess the damage (what data was changed?)
3. Write a corrective migration
4. Apply and verify

---

## Post-Rollback Checklist

- [ ] Service is running and healthy
- [ ] No errors in pod logs
- [ ] API endpoints responding correctly
- [ ] Events flowing normally (check Dapr logs)
- [ ] Root cause identified and documented
- [ ] Fix implemented in code/config (not just rolled back)
- [ ] Auto-sync re-enabled on ArgoCD (if disabled)
- [ ] Team notified of incident and resolution

---

## Related Skills

- **debug-k8s**: Diagnose pod issues before deciding to rollback
- **setup-gitops**: Fix GitOps configuration
- **commit-code**: Commit revert or fix changes
- **troubleshoot-service**: Debug the root cause
- **create-migration**: Create corrective migration
