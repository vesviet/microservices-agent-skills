# Workflows Configuration

## Turbo Mode Control Panel

`// turbo-all` = Auto-run ALL `run_command` steps without user approval.
`// turbo` = Auto-run only the NEXT step (place above specific step).
No annotation = Every command requires manual approval.

> **How it works**: The annotation must be inside each workflow `.md` file.
> This README serves as the central reference. To toggle a workflow,
> edit the corresponding file and add/remove the annotation.

### Current Turbo Settings

| # | Workflow | File | Turbo Mode | Notes |
|---|----------|------|------------|-------|
| 1 | `/add-api-quick` | `add-api-quick.md` | ❌ off | |
| 2 | `/architecture-planning` | `architecture-planning.md` | ❌ off | |
| 3 | `/debug-issue` | `debug-issue.md` | ❌ off | |
| 4 | `/deep-review` | `deep-review.md` | ❌ off | |
| 5 | `/git-operations` | `git-operations.md` | ❌ off | |
| 6 | `/plan-event-driven` | `plan-event-driven.md` | ❌ off | |
| 7 | `/quick-docs` | `quick-docs.md` | ❌ off | |
| 8 | `/quick-refactor` | `quick-refactor.md` | ❌ off | |
| 9 | `/write-test-coverage` | `write-test-coverage.md` | ✅ `turbo-all` | Flow dài: build → test → fix → re-test |
| 10 | `/wsl-terminal` | `wsl-terminal.md` | ❌ off | |

### How to Change

**Enable turbo for a workflow** — Add `// turbo-all` right after the `---` frontmatter:
```markdown
---
description: ...
---

// turbo-all

# Workflow Title
```

**Enable turbo for specific steps only** — Add `// turbo` above individual steps:
```markdown
// turbo
7. **Run tests**
   - go test ./...
```

**Disable turbo** — Remove `// turbo-all` or `// turbo` from the file.

## Workflow Descriptions

| Slash Command | Purpose | Optimization |
|---------------|---------|-------------|
| `/add-api-quick` | Adding new API endpoints | Speed via patterns |
| `/architecture-planning` | Complex multi-service changes | Deep reasoning |
| `/debug-issue` | Troubleshooting and debugging | Problem-solving |
| `/deep-review` | Thorough code review | Quality |
| `/git-operations` | Git across all microservices | Batch operations |
| `/plan-event-driven` | Event-driven architecture | Async patterns |
| `/quick-docs` | Documentation updates | Clarity |
| `/quick-refactor` | Fast, focused refactoring | Speed |
| `/write-test-coverage` | Writing comprehensive tests | Coverage |
| `/wsl-terminal` | WSL terminal usage | Reference |
