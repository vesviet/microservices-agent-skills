---
description: How to build and deploy a microservice
---

## Build & Deploy Workflow

// turbo-all

### Rules
- **NEVER build Docker images locally.** Always commit & push, then CI/CD builds the image.
- **NEVER manually update `newTag` in gitops.** CI/CD pipeline automatically updates the image tag in gitops after building the image. Do NOT ever edit `newTag` yourself.
- Tag format: short git commit hash (e.g., `2c23782`)
- **To verify CI build is done:** Run `cd /home/user/microservices/gitops && git pull origin main` and check if the `newTag` in the service's `kustomization.yaml` matches the latest commit hash. If it matches, CI has finished building and pushed the new image.

### Steps

1. **Make code changes** in the service repo (e.g., `/home/user/microservices/gateway`)

2. Run tests and verify build:
```bash
cd /home/user/microservices/<service> && go build ./...
```

3. Commit changes with a clear message:
```bash
cd /home/user/microservices/<service> && git add -A && git commit -m "<type>: <description>"
```

4. Push to remote (CI will build Docker image and update gitops tag automatically):
```bash
cd /home/user/microservices/<service> && git push origin main
```

5. Wait for CI to build the image and ArgoCD to sync (typically 2-5 minutes).

6. Verify deployment:
```bash
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl get pods -n <service>-dev -w"
```
