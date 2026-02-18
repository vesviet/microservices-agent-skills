---
description: Fast, focused refactoring tasks - optimized for speed
---

# Quick Refactor Workflow

Use this workflow for **small-scale, focused refactoring** that doesn't require extensive planning or documentation updates.

## When to Use

- Renaming variables, functions, or classes
- Extracting helper functions
- Simple code cleanup or formatting
- Moving code within the same file
- Removing dead code
- Single-file refactoring

## Approach

**Optimization**: Speed and minimal scope
- Focus on the specific change requested
- Skip extensive documentation updates (unless docs are directly affected)
- Auto-run safe commands
- Avoid scope creep

## Steps

1. **Understand the scope**
   - Identify the exact code to refactor
   - Verify it's truly a small-scale change
   - If it affects multiple services → use `/architecture-planning` instead

2. **Make the change**
   - Edit the target file(s)
   - Maintain existing code style and patterns
   - Keep changes minimal and focused

3. **Quick verification**
   - Run build to check for compilation errors
   - Run affected tests if available
   - Check for obvious breaking changes

4. **Done**
   - Commit if everything passes
   - No need for extensive documentation

## Skills to Use

- `navigate-service` - If navigating unfamiliar code
- `commit-code` - For validation and commit

## Tips

- Stay focused on the specific request
- Don't try to "improve everything" at once
- If you discover larger issues, note them but don't fix in this workflow
- This workflow prioritizes speed over thoroughness
