---
description: Git operations across all microservices - each service is its own Git repo, no git at root
---

# Git Operations for Microservices

## Key Architecture
- **No git at root**: `d:\microservices` is NOT a git repo
- **Each service = separate git repo**: `admin`, `auth`, `catalog`, etc.
- **Docs = separate git repo**: `docs/` is its own repo
- **GitOps configs**: `argocd/`, `gitops/` are also separate repos

## Available Script: `git-all.sh`
Located at `d:\microservices\git-all.sh` — runs git commands across ALL repos at once.

### Running the script
```bash
# Via WSL (recommended)
wsl bash git-all.sh <command> [args]

# Or from WSL shell
cd /mnt/d/microservices && bash git-all.sh <command> [args]
```

### Commands
| Command | Usage | Description |
|---------|-------|-------------|
| `status` | `bash git-all.sh status` | Show status of all repos |
| `pull` | `bash git-all.sh pull` | Pull all repos |
| `add` | `bash git-all.sh add` | Stage all changes |
| `commit` | `bash git-all.sh commit "message"` | Commit all repos |
| `push` | `bash git-all.sh push` | Push all repos |
| `sync` | `bash git-all.sh sync "message"` | Add + commit + push in one command |
| `stash` | `bash git-all.sh stash ["message"]` | Stash changes across all repos |
| `tag` | `bash git-all.sh tag "v1.0.0" "msg"` | Create & push tag on all repos |
| `clone` | `bash git-all.sh clone` | Clone all repos from GitLab |
| `clone-or-pull` | `bash git-all.sh clone-or-pull` | Clone new or pull existing (excludes docs) |

## Single Service Git Operations

When working on a single service, run git directly in that service directory:

```bash
# PowerShell — specify the service directory
git -C d:\microservices\<service> status
git -C d:\microservices\<service> add -A
git -C d:\microservices\<service> commit -m "message"
git -C d:\microservices\<service> push

# WSL
wsl git -C /mnt/d/microservices/<service> status
```

### Common single-service workflows

#### Check what changed in one service
```bash
git -C d:\microservices\catalog status
git -C d:\microservices\catalog diff
```

#### Commit & push one service
```bash
git -C d:\microservices\catalog add -A
git -C d:\microservices\catalog commit -m "feat(catalog): add product variants"
git -C d:\microservices\catalog push
```

## Repository List (ROOT_SERVICES)
All repos in `d:\microservices`:

| Category | Repos |
|----------|-------|
| **Services** | admin, auth, catalog, customer, checkout, fulfillment, gateway, location, loyalty-rewards, notification, order, payment, pricing, promotion, return, review, search, shipping, user, warehouse |
| **Shared** | common, common-operations |
| **Frontend** | frontend |
| **Infra/GitOps** | argocd, gitops, gitlab-ci-templates |
| **Docs** | docs |
| **Analytics** | analytics |

## GitLab Remote
- URL: `gitlab.com/ta-microservices/<service-name>`
- Each service maps to a GitLab project under the `ta-microservices` group

## Tips
- Always check `status` before bulk operations to avoid committing unintended changes
- Use `sync` for quick "save all" — it does `add + commit + push` across all repos
- The `clone-or-pull` command skips docs repo — useful for code-only updates
- Commit messages should follow conventional format: `feat(service): description`
