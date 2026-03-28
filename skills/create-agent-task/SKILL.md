---
name: create-agent-task
description: Create and assign tasks to an AGENT-XX.md file in docs/10-appendix/checklists/workflow/agent-tasks — auto-finds the slot by number, cleans old content, breaks down the work into granular checklist tasks
---

# Create Agent Task Skill

Use this skill when the user asks you to "create a task for agent", "assign task to AGENT-XX", "tạo task cho agent", or similar. The skill finds the correct `AGENT-XX.md` file, cleans any old/template content, and populates it with well-structured, granular hardening tasks.

## When to Use

- User says: "tạo task cho agent 14", "assign tasks to AGENT-20", "add task to agent 18"
- User provides a high-level task description or a meeting review report, expecting you to break it into actionable sub-tasks
- User wants to fill an empty agent slot with new work

---

## 🚨 MANDATORY WORKFLOW

### Step 1: Identify the Agent Slot (Create or Update)

1. Parse the agent number from the user's request (e.g., "agent 14" → `AGENT-14`).
2. Look for the file in `docs/10-appendix/checklists/workflow/agent-tasks/`:
   - First try: `AGENT-XX.md` (empty slot)
   - Then try: `AGENT-XX-*.md` (existing file with suffix)
3. Read the current content of the file directly before editing it.
4. **CRITICAL UPDATE RULE**: If the user requests to **update** or **reassign** an existing agent task (even if it has old pending tasks), you MUST:
   - **CLEAN OLD TEXT**: Completely overwrite the file's old content with the new task requirements. Do not append to old, unrelated tasks.
   - **RENAME FILE**: If the new task has a different topic, rename the file using a normal shell move/rename command (e.g., `mv AGENT-XX-OLD-TOPIC.md AGENT-XX-NEW-TOPIC.md`).
5. If creating a new task in an empty slot, proceed to overwrite the empty template.

### Step 2: Understand the Work

1. Read the user's task description carefully.
2. If the user references a **meeting review report**, **checklist**, or **review document**, read those source files to extract actionable issues.
3. If the user provides a high-level description (e.g., "harden the payment service"), you MUST:
   - Navigate the target service's codebase using fast repo search and file reads (for example `rg --files`, `rg -n`, and direct file inspection)
   - Identify concrete issues (security gaps, missing error handling, N+1 queries, etc.)
   - Break them into specific, implementable tasks

### Step 3: Break Down into Granular Tasks

Each task MUST be:
- **Atomic**: One clear change per task (one function, one file, one concern)
- **Specific**: Exact file path, line numbers, and code snippets (BEFORE → AFTER)
- **Prioritized**: Classified as P0 (blocking/critical), P1 (high priority), or P2 (nice to have)
- **Validatable**: Include verification commands or test expectations

Task structure template:
```markdown
### [ ] Task N: [Clear Title]

**File**: `service/internal/path/to/file.go`
**Lines**: X-Y
**Risk**: [What can go wrong if not fixed]
**Problem**: [What's wrong now — with code snippet]
**Fix**:
```go
// BEFORE:
<existing code>

// AFTER:
<fixed code>
```

**Validation**:
```bash
cd <service> && go test ./path/... -run TestName -v
```
```

### Step 4: Clean and Write the Agent File

1. **ALWAYS overwrite the entire file** — do NOT append to old template/content. Replace the file contents in one clean pass.
2. Follow this exact file structure:

```markdown
# AGENT-XX: [Descriptive Title]

> **Created**: YYYY-MM-DD
> **Priority**: P0/P1/P2 (summary)
> **Sprint**: Tech Debt Sprint / Feature Sprint
> **Services**: `service-name`
> **Estimated Effort**: X-Y days
> **Source**: [Link to meeting review or issue tracker if applicable]

---

## 📋 Overview

[2-3 sentences describing the scope and context of this task batch]

### [Optional: Architecture/Flow Context Diagram]

---

## ✅ Checklist — P0 Issues (MUST FIX)

### [ ] Task 1: [Title]
...

---

## ✅ Checklist — P1 Issues (Fix In Sprint)

### [ ] Task 2: [Title]
...

---

## ✅ Checklist — P2 Issues (Backlog)

### [ ] Task N: [Title]
...

---

## 🔧 Pre-Commit Checklist

```bash
cd <service> && wire gen ./cmd/server/ ./cmd/worker/
cd <service> && go build ./...
cd <service> && go test -race ./...
cd <service> && golangci-lint run ./...
```

---

## 📝 Commit Format

```
fix(<service>): <description>

- fix: <task 1 summary>
- fix: <task 2 summary>
...

Closes: AGENT-XX
```

---

## 📊 Acceptance Criteria

| Criteria | Verification | Status |
|---|---|---|
| [Task 1 criteria] | [How to verify] | |
| [Task 2 criteria] | [How to verify] | |
```

### Step 5: Rename File (if needed)

If the file was an empty slot (`AGENT-XX.md`), rename it to include the topic:
```
AGENT-XX.md → AGENT-XX-<TOPIC>.md
```

Use a normal shell `mv` command to rename:
```bash
mv docs/.../agent-tasks/AGENT-XX.md docs/.../agent-tasks/AGENT-XX-<TOPIC>.md
```

---

## 🛑 STRICT RULES

- **Clean before write**: ALWAYS overwrite the file completely. Never leave old template placeholders mixed with new content.
- **No vague tasks**: Every task MUST have exact file path, line numbers (or function name), and a concrete code fix or clear instructions. "Fix the error handling" is NOT acceptable — "Handle `orderRepo.Update` error at `payment_consumer.go:242` instead of discarding with `_ =`" IS acceptable.
- **Minimum 3 tasks**: If the user gives a single high-level request, break it into at least 3 granular sub-tasks. If fewer than 3 issues exist, document why.
- **Priority ordering**: P0 tasks first, then P1, then P2. Within each priority, order by risk/impact.
- **Include validation**: Every task must have a `Validation` section with runnable commands (`go build`, `go test`, `grep`).
- **Source attribution**: If tasks come from a meeting review or external document, include a `Source` link in the header.

---

## Example Triggers

| User says | Action |
|---|---|
| "tạo task cho agent 18 về hardening payment service" | Navigate payment service → find issues → write to AGENT-18.md |
| "assign meeting review results to agent 20" | Read meeting review → extract issues → write to AGENT-20.md |
| "add task AGENT-14: fix N+1 queries in catalog" | Investigate catalog N+1 → break into sub-tasks → write to AGENT-14.md |
| "tạo task agent 21 từ review checkout" | Read checkout review → extract pending issues → write to AGENT-21.md |
