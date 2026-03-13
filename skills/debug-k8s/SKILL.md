---
name: debug-k8s
description: Debug Kubernetes deployment issues - pods, services, configs, images, and ArgoCD sync problems
---

# Debug Kubernetes Skill

Use this skill when the user reports Kubernetes deployment issues, pod failures, or service connectivity problems.

## When to Use
- Pods are in `CrashLoopBackOff`, `ImagePullBackOff`, `ErrImagePull`, `CreateContainerConfigError`, `Pending` state
- ArgoCD sync / manifest generation failures
- Dapr sidecar not ready
- Missing secrets, broken configmaps, port mismatches
- Services not accessible

## Environment Details

- **Cluster**: k3d/k3s (remote dev server)
- **SSH Access**: `$DEV_SSH`
- **Namespaces**: `<service>-dev` (e.g., `auth-dev`, `order-dev`)
- **GitOps Repo (local)**: `gitops/`
- **GitOps structure**: `apps/<service>/base/` + `apps/<service>/overlays/dev/`

---

## ⚠️ GOLDEN RULE: GitOps + CI/CD Only

1. **ALL fixes go through GitOps or standard commits. Period.**
2. **NEVER use Docker locally** — no `docker build`, `docker-compose`, or `make docker-build`. All image building happens in GitLab CI.

```
Edit code → commit → push → wait for CI pipeline to build image
Update gitops (if needed) → commit → push → ArgoCD hard-refresh → verify
```

```
Edit gitops file → commit → push → ArgoCD hard-refresh → verify
```

---

## The Only Workflow You Need

### Step 1: Diagnose

```bash
# Pod status
$DEV_SSH "kubectl get pods -n <service>-dev"

# Events (best first signal)
$DEV_SSH "kubectl get events -n <service>-dev --sort-by=.metadata.creationTimestamp | tail -20"

# Logs
$DEV_SSH "kubectl logs -n <service>-dev -l app.kubernetes.io/name=<service> --tail=80 2>&1"

# Previous crash logs
$DEV_SSH "kubectl logs -n <service>-dev -l app.kubernetes.io/name=<service> --previous --tail=50 2>&1"

# Describe pod (for CreateContainerConfigError, probe failures)
$DEV_SSH "kubectl describe pod -n <service>-dev -l app.kubernetes.io/name=<service> 2>&1 | tail -40"
```

### Step 2: Fix in GitOps

Edit the relevant file(s) in `gitops/apps/<service>/`.

**GitOps File Map:**

| What to fix | File |
|---|---|
| Image tag | 🚫 **NEVER modify manually** (Handled by CI/CD) |
| Env vars / config | `overlays/dev/configmap.yaml` |
| Secrets (DB password, keys) | `overlays/dev/secrets.yaml` |
| Ports, probes, Dapr annotations | `base/deployment.yaml` or `base/worker-deployment.yaml` |
| Migration job | `base/migration-job.yaml` |
| Kustomize resource list | `overlays/dev/kustomization.yaml` → `resources:` |

**Infrastructure endpoints (dev cluster):**
```
PostgreSQL : postgresql.infrastructure.svc.cluster.local:5432
Redis      : redis.infrastructure.svc.cluster.local:6379
Consul     : consul.infrastructure.svc.cluster.local:8500
```

**Secrets pattern** — if `secretRef: name: <service>-secrets` is in deployment but missing:
```yaml
# overlays/dev/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: <service>-secrets
  labels:
    app.kubernetes.io/name: <service>
    app.kubernetes.io/environment: dev
type: Opaque
stringData:
  # Use actual secrets from SealedSecrets or Vault in production
  <SERVICE>_DATA_DATABASE_SOURCE: "postgres://postgres:<DB_PASSWORD>@postgresql.infrastructure.svc.cluster.local:5432/<service>_db?sslmode=disable"
  DATABASE_URL: "postgres://postgres:<DB_PASSWORD>@postgresql.infrastructure.svc.cluster.local:5432/<service>_db?sslmode=disable"
```
Then add `- secrets.yaml` to `overlays/dev/kustomization.yaml` resources.

### Step 3: Verify kustomize builds clean

```bash
kubectl kustomize gitops/apps/<service>/overlays/dev > /dev/null 2>&1 && echo "✅ OK" || echo "❌ FAIL"
```

### Step 4: Commit + Push

```bash
cd gitops \
  && git add -A \
  && git commit -m "fix: <service> <description>" \
  && git pull --rebase origin main \
  && git push origin main
```

### Step 5: Trigger ArgoCD Sync

> `argocd` CLI is NOT available in SSH PATH. Use `kubectl patch` to trigger hard-refresh + sync.

```bash
# Hard refresh (forces ArgoCD to pull latest git)
$DEV_SSH \
  "kubectl patch application <service>-dev -n argocd \
   --type merge \
   -p '{\"metadata\":{\"annotations\":{\"argocd.argoproj.io/refresh\":\"hard\"}}}'"

# Check ArgoCD picked up the new revision
$DEV_SSH \
  "kubectl get application -n argocd <service>-dev \
   -o jsonpath='{.status.sync.revision} {.status.sync.status} {.status.health.status}' && echo ''"

# If still OutOfSync, force sync via patch
$DEV_SSH \
  "kubectl patch application <service>-dev -n argocd \
   --type merge \
   -p '{\"operation\":{\"initiatedBy\":{\"username\":\"admin\"},\"sync\":{\"revision\":\"HEAD\",\"prune\":true}}}'"
```

### Step 6: Verify

```bash
# Watch pods until Running
$DEV_SSH "kubectl get pods -n <service>-dev"

# Rollout status
$DEV_SSH "kubectl rollout status deployment/<service> -n <service>-dev --timeout=90s"

# Confirm secret was created
$DEV_SSH "kubectl get secret <name> -n <service>-dev"
```

---

## Common Issues — Quick Reference

### CreateContainerConfigError — Missing Secret
Secret referenced in `secretRef` does not exist in the namespace.
1. Create `overlays/dev/secrets.yaml` with the correct secret name
2. Add `- secrets.yaml` to `overlays/dev/kustomization.yaml` resources list
3. Commit → push → sync

### CrashLoopBackOff — Bad Config / DB unreachable
Check logs → compare `<service>/configs/config.yaml` with `overlays/dev/configmap.yaml`.
Fix the mismatch → commit → push → sync.

### ImagePullBackOff — Wrong tag
⚠️ **NEVER manually update `newTag` in `kustomization.yaml`** — CI/CD pipeline automatically updates image tags after building.
If an image is missing, trigger a CI build in GitLab to build and update the image tags automatically.

### kustomize build error — Duplicate YAML key / bad manifest
```bash
kubectl kustomize gitops/apps/<service>/overlays/dev 2>&1
```
Fix the YAML error in the reported file → commit → push → sync.

### Dapr sidecar NotReady — app-port mismatch
`dapr.io/app-port` in deployment annotation must match the port the app's HTTP server actually listens on.
Fix in `base/deployment.yaml` or `base/worker-deployment.yaml` → commit → push → sync.

### Stuck Migration Job
```bash
$DEV_SSH "kubectl delete job <service>-migration -n <service>-dev"
# Then sync to recreate
```

---

## Bulk Audit — All Services

```bash
# Check kustomize build for ALL services at once
for svc in $(ls gitops/apps/); do
  if [ -d "gitops/apps/$svc/overlays/dev" ]; then
    kubectl kustomize gitops/apps/$svc/overlays/dev > /dev/null 2>&1 \
      && echo "✅ $svc" || echo "❌ $svc"
  fi
done

# All pods across dev namespaces
$DEV_SSH "kubectl get pods --all-namespaces | grep '\-dev'"

# Find pods not Running
$DEV_SSH "kubectl get pods --all-namespaces | grep -v 'Running\|Completed\|NAME'"
```

---

## Checklist

### Diagnosis
- [ ] Pod status checked
- [ ] Events reviewed
- [ ] Logs examined
- [ ] Previous crash logs checked

### Fix
- [ ] Root cause identified
- [ ] GitOps file edited
- [ ] Kustomize build verified
- [ ] Changes committed and pushed

### Verification
- [ ] ArgoCD hard refresh triggered
- [ ] Pods running
- [ ] Service accessible
- [ ] No errors in logs

---

## Quick Reference Checklist

Use this for rapid K8s debugging:

### Diagnose
- [ ] Check pod status
- [ ] Review events
- [ ] Check logs

### Fix
- [ ] Edit GitOps files
- [ ] Verify kustomize
- [ ] Commit + push

### Deploy
- [ ] Trigger ArgoCD sync
- [ ] Verify pods running

---

## Related Skills

- **setup-gitops**: Update GitOps configuration
- **troubleshoot-service**: Debug service-level issues
- **commit-code**: Commit GitOps changes
- **trace-event-flow**: Debug event communication issues
- **review-service**: Full service review including deployment
- **performance-profiling**: Profile service performance in K8s

---

## Persistent Volume Debugging (PVC/PV)

If a pod is stuck in `Pending` due to storage:

```bash
# Check PVC status
$DEV_SSH "kubectl get pvc -n <service>-dev"

# Describe PVC for events
$DEV_SSH "kubectl describe pvc <claim-name> -n <service>-dev"

# Check available PVs
$DEV_SSH "kubectl get pv | grep -E 'Available|Released'"

# Check StorageClass
$DEV_SSH "kubectl get storageclass"
```

Common fixes:
- **No matching PV**: Check StorageClass exists and has provisioner
- **PV in Released state**: Delete PV and let provisioner create new one
- **Capacity mismatch**: Ensure PVC request ≤ PV capacity
