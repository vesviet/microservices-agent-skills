---
name: manage-secrets
description: Best practices for managing secrets, environment variables, and sensitive configuration across microservices
---

# Manage Secrets Skill

Use this skill for managing secrets, environment variables, and sensitive configuration across the microservices platform.

## When to Use
- Adding new secrets (API keys, database credentials, JWT signing keys)
- Rotating existing secrets
- Setting up secret management for a new service
- Reviewing security posture of configurations
- Moving from hardcoded secrets to proper secret management

## Current Secret Management Architecture

### Development (Local)
- Secrets stored in `configs/config.yaml` per service
- Database passwords in docker-compose environment
- **Never commit real secrets** — use `.example` suffix files

### Kubernetes (Dev/Staging/Prod)
- Kubernetes `Secret` resources in GitOps overlays
- **⚠️ KNOWN ISSUE**: Some secrets are currently base64-encoded in Git (ARGOCD-P0-1)
- **Target**: Migrate to Sealed Secrets or External Secrets Operator

## Secret Categories

### 1. Database Credentials
```yaml
# Pattern: Per-service database user with limited permissions
# Name convention: <service>-db-credentials
kind: Secret
metadata:
  name: order-db-credentials
  namespace: order-dev
type: Opaque
data:
  DATABASE_URL: <base64-encoded>
  # Format: postgres://<user>:<pass>@<host>:5432/<db>?sslmode=require
```

**Best Practices**:
- Each service gets its own database user (principle of least privilege)
- Read-only replicas use separate credentials
- Connection strings include `sslmode=require` for production

### 2. Redis Credentials
```yaml
kind: Secret
metadata:
  name: redis-credentials
type: Opaque
data:
  REDIS_ADDR: <base64>
  REDIS_PASSWORD: <base64>
```

### 3. JWT Signing Keys
```yaml
# Used by: auth service, gateway
# Rotation: Every 90 days
kind: Secret
metadata:
  name: jwt-signing-key
data:
  JWT_SECRET: <base64>
  JWT_REFRESH_SECRET: <base64>
```

**Rotation Process**:
1. Generate new key: `openssl rand -hex 64`
2. Update secret in all environments
3. Both old and new keys should be valid during transition (dual-key support)
4. After 24h (max token lifetime), remove old key

### 4. External API Keys
```yaml
# Payment gateways, shipping carriers, GeoIP
kind: Secret
metadata:
  name: payment-api-keys
data:
  STRIPE_SECRET_KEY: <base64>
  VNPAY_HASH_SECRET: <base64>
  MOMO_SECRET_KEY: <base64>
```

### 5. Service-to-Service Auth
- Currently: No auth (trust within cluster)
- Planned: mTLS via service mesh or Dapr auth

## GitOps Secret Locations

```
gitops-k8s/
├── base/
│   └── <service>/
│       ├── deployment.yaml    # References secrets as env vars
│       └── kustomization.yaml
├── overlays/
│   ├── dev/
│   │   └── <service>/
│   │       ├── secrets.yaml   # ⚠️ Should use Sealed Secrets
│   │       └── kustomization.yaml
│   ├── staging/
│   └── prod/
```

## Checklist: Adding a New Secret

1. **Identify the secret type** (DB, API key, JWT, etc.)
2. **Create the Kubernetes Secret manifest**:
   ```bash
   kubectl create secret generic <name> \
     --from-literal=KEY=value \
     --dry-run=client -o yaml > secret.yaml
   ```
3. **Add to GitOps overlay** for each environment (dev, staging, prod)
4. **Reference in Deployment**:
   ```yaml
   env:
     - name: DATABASE_URL
       valueFrom:
         secretKeyRef:
           name: <secret-name>
           key: DATABASE_URL
   ```
5. **Update service config** to read from environment variable
6. **Test locally** with `.env` file or direct config
7. **Document** in service doc's Configuration section

## Checklist: Rotating a Secret

1. **Generate new value**: `openssl rand -hex 32` (or service-specific generation)
2. **Update in all environments** (dev → staging → prod, in order)
3. **For JWT keys**: Support dual keys during rotation window
4. **For DB passwords**:
   - Create new DB user with new password
   - Update secret
   - Verify application connects
   - Drop old user after confirmation
5. **Monitor** for connection errors after rotation
6. **Update documentation** with rotation date

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Hardcode secrets in Go source | Use environment variables via config |
| Commit real secrets in `config.yaml` | Use `config.yaml.example` with placeholders |
| Share database users across services | Create per-service database users |
| Store secrets in ConfigMaps | Use Kubernetes Secrets (or Sealed Secrets) |
| Log secret values | Log secret names only, mask values |
| Use same secrets across environments | Unique secrets per environment |

## Future: Sealed Secrets Migration

When migrating from plain Secrets to Sealed Secrets:

```bash
# 1. Install Sealed Secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# 2. Seal existing secrets
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

# 3. Replace in GitOps
# sealed-secret.yaml is safe to commit to Git

# 4. Delete plain secret.yaml from Git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret.yaml' HEAD
```
