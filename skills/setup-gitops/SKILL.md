---
name: setup-gitops
description: Set up or update GitOps configuration (Kustomize overlays, ConfigMaps, Secrets, Deployments) for a microservice
---

# Setup GitOps Skill

Use this skill when the user needs to configure or update GitOps deployment files for a microservice.

## When to Use
- Setting up GitOps for a new service
- Updating ConfigMaps, Secrets, or Deployments
- Changing image tags for deployment
- Adding new environment variables
- Configuring migration jobs
- Troubleshooting deployment configuration mismatches

## GitOps Directory Structure

All GitOps configuration lives in `/home/user/microservices/gitops/`.

```
gitops/apps/<service>/
├── base/                           # Base manifests (shared across environments)
│   ├── kustomization.yaml          # Base kustomization
│   ├── deployment.yaml             # Deployment manifest
│   ├── service.yaml                # Kubernetes Service
│   ├── configmap.yaml              # Base ConfigMap (if any)
│   ├── migration-job.yaml          # Database migration Job
│   ├── namespace.yaml              # Namespace definition
│   ├── dapr-components.yaml        # Dapr components (if service uses Dapr)
│   └── dapr-subscription.yaml      # Dapr subscriptions (if applicable)
├── overlays/
│   └── dev/                        # Dev environment overlay
│       ├── kustomization.yaml      # Overlay kustomization (image tag override)
│       ├── configmap.yaml          # Environment-specific config
│       ├── secrets.yaml            # Environment-specific secrets (SealedSecrets)
│       └── migration-configmap.yaml # Migration-specific config
```

## Key Files Explained

### `overlays/dev/kustomization.yaml` - Image Tag Management
This is the **most frequently edited file**. It controls which Docker image version is deployed.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: <service>-dev

resources:
  - ../../base

patches:
  - path: configmap.yaml
  - path: secrets.yaml

images:
  - name: <service>-service
    newName: registry-api.tanhdev.com/<service>-service
    newTag: "abc1234"  # ← Auto-updated by CI/CD pipeline (DO NOT edit manually)
```

> ⚠️ **NEVER manually update `newTag`** — CI/CD pipeline automatically updates this after building the Docker image. Manual edits will be overwritten or cause conflicts.

### `base/deployment.yaml` - Deployment Manifest

Standard deployment template:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <service>-service
  labels:
    app: <service>-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <service>-service
  template:
    metadata:
      labels:
        app: <service>-service
      annotations:
        dapr.io/enabled: "true"          # Enable Dapr sidecar
        dapr.io/app-id: "<service>"      # Dapr app ID
        dapr.io/app-port: "80XX"         # App HTTP port
    spec:
      imagePullSecrets:
        - name: registry-secret
      containers:
        - name: <service>
          image: <service>-service        # Overridden by kustomization
          ports:
            - name: http
              containerPort: 80XX
            - name: grpc
              containerPort: 90XX
          envFrom:
            - configMapRef:
                name: <service>-config
            - secretRef:
                name: <service>-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: 80XX
            initialDelaySeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 80XX
            initialDelaySeconds: 10
```

### `overlays/dev/configmap.yaml` - Environment Config

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <service>-config
data:
  # Database
  DATABASE_HOST: "postgresql.postgresql-dev.svc.cluster.local"
  DATABASE_PORT: "5432"
  DATABASE_USER: "ecommerce_user"
  DATABASE_NAME: "<service>_db"
  DATABASE_SSLMODE: "disable"
  
  # Redis
  REDIS_ADDR: "redis-ha.redis-ha-dev.svc.cluster.local:6379"
  
  # Consul
  CONSUL_ADDR: "consul.consul-dev.svc.cluster.local:8500"
  
  # Service
  HTTP_PORT: "80XX"
  GRPC_PORT: "90XX"
  
  # Dapr
  DAPR_HTTP_PORT: "3500"
  DAPR_GRPC_PORT: "50001"
```

### `base/migration-job.yaml` - Database Migration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: <service>-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      imagePullSecrets:
        - name: registry-secret
      containers:
        - name: migrate
          image: <service>-service
          command: ["/app/migrate"]
          args: ["-command", "up"]
          envFrom:
            - configMapRef:
                name: <service>-config
            - secretRef:
                name: <service>-secrets
      restartPolicy: Never
  backoffLimit: 3
```

## Common Operations

### Deploy a New Version
1. Push code to GitLab (CI builds Docker image automatically)
2. CI/CD pipeline auto-updates `newTag` in `gitops/apps/<service>/overlays/dev/kustomization.yaml`
3. ArgoCD auto-syncs within 3 minutes

> ⚠️ **NEVER manually update `newTag`** — CI/CD handles image tag updates automatically after building. Only commit gitops changes for ConfigMaps, Secrets, Deployments, or other infrastructure config.

### Add New Environment Variable
1. Edit `gitops/apps/<service>/overlays/dev/configmap.yaml`
2. Add the new key-value pair
3. Commit and push gitops changes

### Add New Secret
1. Create a SealedSecret or add to existing `secrets.yaml`
2. Ensure the deployment references it via `envFrom` or `env`

### Setup New Service
1. Copy structure from an existing service in `gitops/apps/`
2. Update all references (namespace, service name, ports, image)
3. Add ArgoCD Application manifest
4. Update port numbers per SERVICE_INDEX.md

### Fix Migration Job
1. Check `gitops/apps/<service>/base/migration-job.yaml`
2. Ensure correct image and command
3. Verify `DATABASE_URL` or individual DB env vars are set
4. Delete stuck job: `kubectl delete job <service>-migration -n <service>-dev`
5. Force ArgoCD sync to recreate

## Port Reference

Always use the standardized ports from `docs/SERVICE_INDEX.md`:
- HTTP: `80XX` (where XX is the service number)
- gRPC: `90XX` (same numbering)

## Namespace Convention

- Dev environment: `<service>-dev` (e.g., `auth-dev`, `order-dev`)
- Staging: `<service>-staging`
- Production: `<service>-prod`

## ArgoCD Application Setup

To register a service with ArgoCD, an Application manifest is needed (usually in `gitops/bootstrap/` or managed separately).

## Checklist for New Service GitOps

- [ ] Namespace created (`namespace.yaml`)
- [ ] Deployment manifest (`deployment.yaml`)
- [ ] Service manifest (`service.yaml`)
- [ ] ConfigMap with correct ports and DB config
- [ ] Secrets with DB password and other sensitive data
- [ ] Image pull secret (`registry-secret`) in namespace
- [ ] Migration job (if service has database)
- [ ] Dapr components (if service uses events)
- [ ] Kustomization files (base + overlay)
- [ ] ArgoCD Application registered
- [ ] Image tag set to valid commit SHA
