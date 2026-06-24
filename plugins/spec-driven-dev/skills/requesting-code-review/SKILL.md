---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

<language>
**Language policy (read carefully — most output bugs come from violating this):**

- `conversation_language` = the language detected from the user's own messages (NOT from code, diffs, or git output). ALL user-facing prose (questions, prompts, transitions, error messages) MUST be rendered in this language. Do NOT hardcode or copy any user-facing phrase from this SKILL file — every example sentence here is for your understanding only, not a string to echo.
- Stay in one language per surface. Do not mix Chinese characters with untranslated English nouns unless that English token is a literal identifier (file path, code symbol, git command, OpenSpec keyword, slash-command name, placeholder like `{USER_LANGUAGE}`). When in doubt, translate.
- File paths, code blocks, git commands, OpenSpec structural keywords, and slash-command names always stay in English regardless of `conversation_language`.
- When dispatching the reviewer subagent, pass the value of `conversation_language` through the `{USER_LANGUAGE}` placeholder so the returned review is also rendered in that language. The example value shown in the *Example* section below is illustrative — substitute the actual `conversation_language` at dispatch time.
</language>

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Use Task tool with `general-purpose` type, fill template at `code-reviewer.md`

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do. If an `openspec/changes/{change-id}/` directory exists for the current work, prefer referencing its `design.md` / `tasks.md` (and `specs/` scenarios) as the source of truth.
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{USER_LANGUAGE}` - The current `conversation_language`. Fill this with the user's input language before dispatching, so the reviewer returns its review in that language. Do NOT hardcode a default value (e.g., do not pre-fill `繁體中文`); always resolve from `conversation_language`.

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

The example below shows one possible dispatch shape. The `USER_LANGUAGE` value is illustrative — at dispatch time, substitute the active `conversation_language`.

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  USER_LANGUAGE: {conversation_language}   # e.g., English, 繁體中文, 日本語 — fill from the live value

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development (`spec-driven-dev:subagent-driven-development`):**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task
- This skill is an additional, on-demand review you can trigger at any checkpoint; it does not replace `spec-driven-dev:verification-before-completion`, which runs the final staged gate before completion. Treat requesting-code-review as an early check that surfaces issues sooner.

**Executing Plans:**
- Review after each task or at natural checkpoints
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: requesting-code-review/code-reviewer.md
