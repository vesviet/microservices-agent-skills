---
name: debug-k8s
description: Debug Kubernetes deployment issues - pods, services, configs, images, and ArgoCD sync problems
---

# Debug Kubernetes Skill

Use this skill when the user reports Kubernetes deployment issues, pod failures, or service connectivity problems.

## When to Use
- Pods are in `CrashLoopBackOff`, `ImagePullBackOff`, `ErrImagePull`, `Error`, or `Pending` state
- Services are not accessible or returning errors
- ArgoCD sync failures
- Database connection issues from pods
- Service initialization hangs or fails
- Config/secret mismatches

## Environment Details

- **Cluster**: k3d/k3s (kubectl configured locally to connect to remote cluster)
- **GitOps**: ArgoCD watches `gitops/` repo for changes → auto-deploy
- **Registry**: `registry-api.tanhdev.com` (private Docker registry)
- **Access**: kubectl and argocd CLI run directly on local machine (no SSH needed)
- **Namespaces**: Each service has its own namespace: `<service>-dev` (e.g., `auth-dev`, `order-dev`)
- **GitOps Repo**: `/home/user/microservices/gitops/`

## ⚠️ CRITICAL RULE: GitOps-Only Changes

**NEVER apply changes directly with `kubectl apply` or `kubectl edit`.**
ALL changes MUST go through GitOps:

1. **Edit** the gitops files in `/home/user/microservices/gitops/apps/<service>/`
2. **Commit** changes to the gitops repo
3. **Push** to remote
4. **Force sync** ArgoCD to apply immediately

```bash
# Standard GitOps commit + force sync flow
cd /home/user/microservices/gitops && git add -A && git commit -m "fix: <service> <description>" && git push origin main

# Then force ArgoCD sync (do NOT wait 3 min for auto-sync)
argocd app sync <service>-dev --force
```

---

## Debugging Workflow (Step-by-Step)

### Step 1: Identify the Symptom

```bash
# Check pod status
kubectl get pods -n <service>-dev

# Get detailed pod events
kubectl describe pod -n <service>-dev -l app=<service>-service

# Check pod logs
kubectl logs -n <service>-dev -l app=<service>-service --tail=100

# Check previous crash logs (if CrashLoopBackOff)
kubectl logs -n <service>-dev -l app=<service>-service --previous --tail=50
```

### Step 2: Diagnose the Root Cause

Based on the symptom, jump to the matching issue section below.

### Step 3: Fix via GitOps

Edit the relevant gitops files (see issue-specific sections below).

### Step 4: Commit, Push & Force Sync

```bash
# Commit the fix
cd /home/user/microservices/gitops && git add -A && git commit -m "fix: <service> <description>"

# Push to remote
cd /home/user/microservices/gitops && git push origin main

# Force ArgoCD sync immediately
argocd app sync <service>-dev --force
```

### Step 5: Verify the Fix

```bash
# Watch pod status until Running
kubectl get pods -n <service>-dev -w

# Check logs for healthy startup
kubectl logs -n <service>-dev -l app=<service>-service --tail=30
```

---

## Common Issues & GitOps Fixes

### Issue 1: ImagePullBackOff / ErrImagePull

**Diagnosis:**
```bash
kubectl describe pod -n <service>-dev -l app=<service>-service | grep -A5 'Events\|image\|Error'
```

**Root Causes & GitOps Fixes:**

**1a. Wrong image tag (CI/CD didn't update):**

> ⚠️ **Do NOT manually edit `newTag`** — CI/CD auto-updates it. If the tag is wrong, the CI pipeline likely failed.

Check if CI pipeline ran successfully:
```bash
cd /home/user/microservices/<service> && git log --oneline -5
# Verify the latest commit has a successful CI pipeline in GitLab
```

If CI failed, fix the build error in the service code, push again, and CI will update the tag automatically.

**1b. Missing registry secret:**
Check if `imagePullSecrets` is in deployment. Edit `gitops/apps/<service>/base/deployment.yaml`:
```yaml
spec:
  template:
    spec:
      imagePullSecrets:
        - name: registry-secret    # ← Must be present
```

**1c. Image not built yet:**
```bash
# Check if image exists by checking GitLab CI
cd /home/user/microservices/<service> && git log --oneline -5
# Verify the commit SHA has a corresponding CI pipeline that built the Docker image
```

**After fixing → commit, push, force sync (Step 4).**

---

### Issue 2: CrashLoopBackOff

**Diagnosis:**
```bash
# Pod logs (most important)
kubectl logs -n <service>-dev -l app=<service>-service --tail=100

# Previous crash logs
kubectl logs -n <service>-dev -l app=<service>-service --previous --tail=50
```

**Root Causes & GitOps Fixes:**

**2a. Database connection failed:**
Edit `gitops/apps/<service>/overlays/dev/configmap.yaml`:
```yaml
data:
  DATABASE_HOST: "postgresql.postgresql-dev.svc.cluster.local"
  DATABASE_PORT: "5432"
  DATABASE_USER: "ecommerce_user"
  DATABASE_NAME: "<service>_db"
  DATABASE_SSLMODE: "disable"
```

**2b. Redis connection failed:**
Edit `gitops/apps/<service>/overlays/dev/configmap.yaml`:
```yaml
data:
  REDIS_ADDR: "redis-ha.redis-ha-dev.svc.cluster.local:6379"
```

**2c. Consul connection failed:**
Edit `gitops/apps/<service>/overlays/dev/configmap.yaml`:
```yaml
data:
  CONSUL_ADDR: "consul.consul-dev.svc.cluster.local:8500"
```

**2d. Wrong port configuration:**
Check `docs/SERVICE_INDEX.md` for correct ports, then edit `gitops/apps/<service>/overlays/dev/configmap.yaml`:
```yaml
data:
  HTTP_PORT: "80XX"    # ← Must match SERVICE_INDEX.md
  GRPC_PORT: "90XX"    # ← Must match SERVICE_INDEX.md
```
And ensure `gitops/apps/<service>/base/deployment.yaml` container ports match.

**2e. Missing environment variable:**
Compare `<service>/configs/config.yaml` with `gitops/apps/<service>/overlays/dev/configmap.yaml` to find missing vars.

**After fixing → commit, push, force sync (Step 4).**

---

### Issue 3: Service Not Accessible

**Diagnosis:**
```bash
kubectl get svc -n <service>-dev
kubectl get endpoints -n <service>-dev
```

**GitOps Fix:**
Check `gitops/apps/<service>/base/service.yaml` ports match the deployment container ports.

---

### Issue 4: ArgoCD Sync Issues

**Diagnosis:**
```bash
# Check app status
argocd app get <service>-dev

# Check sync status
kubectl get application -n argocd <service>-dev -o jsonpath='{.status.sync.status}'
```

**Fixes:**

```bash
# Force sync (most common fix)
argocd app sync <service>-dev --force

# If stuck, hard refresh then sync
argocd app get <service>-dev --hard-refresh
argocd app sync <service>-dev --force --prune

# If old resources block sync, replace
argocd app sync <service>-dev --force --replace
```

---

### Issue 5: Migration Job Failures

**Diagnosis:**
```bash
kubectl get jobs -n <service>-dev
kubectl logs job/<service>-migration -n <service>-dev
```

**GitOps Fixes:**

**5a. Stuck old job (most common):**
Delete the stuck job, then ArgoCD recreates it on next sync:
```bash
kubectl delete job <service>-migration -n <service>-dev
argocd app sync <service>-dev --force
```

**5b. Wrong migration image:**
Edit `gitops/apps/<service>/base/migration-job.yaml` to use correct image. Also ensure kustomization image override covers the migration job container image name.

**5c. Missing Goose annotations in SQL:**
Fix the migration file in `<service>/migrations/`, commit+push the service code, wait for CI, update gitops tag, commit+push gitops, force sync.

---

## GitOps File Reference

| What | File Location |
|------|---------------|
| **Image tag** (most edited) | `gitops/apps/<service>/overlays/dev/kustomization.yaml` |
| **ConfigMap** (env vars) | `gitops/apps/<service>/overlays/dev/configmap.yaml` |
| **Deployment** (containers, ports, probes) | `gitops/apps/<service>/base/deployment.yaml` |
| **Service** (K8s service, ports) | `gitops/apps/<service>/base/service.yaml` |
| **Migration job** | `gitops/apps/<service>/base/migration-job.yaml` |
| **Secrets** | `gitops/apps/<service>/overlays/dev/secrets.yaml` |
| **Dapr components** | `gitops/apps/<service>/base/dapr-*.yaml` |
| **Network policy** | `gitops/apps/<service>/base/networkpolicy.yaml` |
| **Base kustomization** | `gitops/apps/<service>/base/kustomization.yaml` |

---

## Quick Diagnosis Commands

```bash
# Get all pods across all service namespaces
kubectl get pods --all-namespaces | grep -E '(NAME|-dev)'

# Get pods for a specific service
kubectl get pods -n <service>-dev

# Watch pod status changes
kubectl get pods -n <service>-dev -w

# Get recent events for a namespace
kubectl get events -n <service>-dev --sort-by=.metadata.creationTimestamp | tail -20

# Get all ArgoCD applications and their sync status
argocd app list

# Check what image is currently deployed
kubectl get deployment -n <service>-dev -o jsonpath='{.items[0].spec.template.spec.containers[0].image}'
```

## GitOps Fix + Force Sync (Copy-Paste Template)

```bash
# 1. Edit the gitops files (configmap, deployment, kustomization, etc.)
# 2. Then run:
cd /home/user/microservices/gitops && git add -A && git commit -m "fix: <service> <description>" && git push origin main

# 3. Force sync ArgoCD
argocd app sync <service>-dev --force

# 4. Verify
kubectl get pods -n <service>-dev -w
```
