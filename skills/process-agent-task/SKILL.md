---
name: process-agent-task
description: A strict workflow to process, implement, validate, and document hardening tasks located in docs/10-appendix/checklists/workflow/agent-tasks.
---

# Process Agent Task Skill

Use this skill when the user asks you to implement or process a specific agent task from `docs/10-appendix/checklists/workflow/agent-tasks/`. These tasks are usually high-priority (P0/P1/P2) "Hardening" tasks or tech debt resolutions.

## 🚨 MANDATORY WORKFLOW

When processing an agent task, you MUST follow these **7 steps EXACTLY in order**.

### Step 1: Read and Understand the Task File
1. Read the target task file directly (e.g., `docs/10-appendix/checklists/workflow/agent-tasks/AGENT-14-CHECKOUT-HARDENING.md`).
2. Identify ALL the **pending tasks** (unchecked `[ ]` boxes) in the P0/P1/P2 sections.
3. Review the **Overview** to understand the context.
4. Review the **Acceptance Criteria** at the bottom of the file.
5. **CRITICAL PROCEDURE**: You MUST process EVERY pending task sequentially. Do not ask for the user's confirmation between tasks. Loop through Steps 2 to 6 for EACH task until all tasks in the file are 100% completed.

### Step 2: Code Analysis
1. Before editing any code, inspect the exact files and lines mentioned in the task.
2. Understand the Clean Architecture layers (biz, data, service) involved.
3. If the solution is provided in the task file, map it to the current codebase. If not, plan the correct architectural fix based on the problem description.

### Step 3: Implement the Fix
1. Make changes to the code using the normal Codex editing workflow, preferring focused patches over broad rewrites.
2. Ensure you modify the code exactly per the Kratos + Clean Architecture rules (no DB calls in the biz layer, return proper gRPC status errors, do not discard errors with `_ =`, etc.).

### Step 4: Mandatory Validation (Pre-Commit)
1. You **MUST** run the validation commands specified in the "🔧 Pre-Commit Checklist" section of the task file in the shell.
2. Typically, this involves:
   - `wire gen ./cmd/server/ ./cmd/worker/` (CRITICAL: Always run this if dependencies change!)
   - `go build ./...`
   - `go test -race ./...` (Run the specific unit tests you added or modified)
   - `golangci-lint run ./...`
3. If any step fails, you MUST fix the issue and run the validation again until it passes.

### Step 5: Update the Task File (.md)
1. You MUST update the task markdown file to mark it completed. 
2. Change `[ ] Task N:` to `[x] Task N: ... ✅ IMPLEMENTED`.
3. Following the existing task format, add the implementation details directly below the task:
   - **Files**: List the exact files and lines modified.
   - **Risk / Problem**: (Keep original description or summarize it).
   - **Solution Applied**: Explain exactly what you did, and include the core code snippet you implemented (using standard Markdown Go blocks).
   - **Validation**: Show the validation commands you ran.

### Step 6: Verify Acceptance Criteria
1. Cross-check your work with the `Acceptance Criteria` table at the end of the markdown file.
2. Update the `Acceptance Criteria` table by changing the Status column for the implemented task from blank or pending to `✅`.

### Step 7: Commit and Push Code
1. Use the `commit-code` skill in this pack to perform the final validation and commit flow.
2. Format the commit message EXACTLY as specified in the "📝 Commit Format" section of the task file.
3. Push only if the user explicitly asked for it and the environment allows remote operations.

---

## 🛑 STRICT RULES

- **Never skip validation**: Do not assume your code works. Always run `go build` and `go test` and verify the real command output.
- **Zero error discarding**: Do not use `_ = err` unless explicitly justified. Use proper error returning, retry, or DLQ.
- **Detailed Markdown Updates**: The user relies on the `AGENT-*.md` files as auditing reports. If you just check the `[x]` box without documenting the changes comprehensively, you have FAILED.
- **Process ALL pending tasks**: When processing an agent task file, you MUST automatically process and implement ALL pending (`[ ]`) tasks found in the file sequentially during the same session. DO NOT stop and ask the user for confirmation after each task. Continue looping through Steps 2-6 for each pending task until the entire task file is completely resolved. Only when all tasks are implemented and validated should you proceed to Step 7 (Git Commit).
- **Rollback on regression**: If a fix breaks other tests or causes build failures that cannot be resolved within 3 attempts, carefully undo only your in-progress edits, preserve unrelated user changes, and mark the task as `[ ] Task N: ... ⏸️ DEFERRED — regression in <details>`. Document the regression and move to the next task.
