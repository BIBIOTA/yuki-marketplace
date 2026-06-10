---
name: create-pr
description: |
  ALWAYS use this skill before running `gh pr create` or whenever the user asks to create a pull request. Enforces three mandatory PR conventions: English-only title, description in the user's language, and the user set as assignee.
---

# Create PR

Every pull request MUST follow these three conventions before calling `gh pr create`.

## Convention 1 — Title: English only

The PR title must be written entirely in English.

- Summarise the change in one short phrase (≤ 70 characters)
- Use imperative mood: "Add feature", "Fix bug", "Refactor module"
- No Chinese, Japanese, or other non-Latin characters in the title

If the user supplies a title in another language, translate it to English before using it.

## Convention 2 — Description: user's language

Write the PR body in the **same language the user is currently speaking**.

- If the user's message is in Traditional Chinese → write the body in Traditional Chinese
- If the user's message is in English → write the body in English
- Never write the body in a different language than the user's active language

Use this structure for the body:

```
## 摘要 / Summary
<1–3 bullet points explaining what changed and why>

## 測試計畫 / Test plan
<bulleted checklist of steps to verify the change>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Use the heading language that matches the user's language (e.g. `## 摘要` for Chinese, `## Summary` for English).

## Convention 3 — Assignee: always the user

Always add `--assignee @me` to the `gh pr create` command so the PR is assigned to the authenticated GitHub user.

## Command template

```bash
gh pr create \
  --title "<English title>" \
  --assignee @me \
  --body "$(cat <<'EOF'
<body in user's language>
EOF
)"
```

## Checklist before executing

- [ ] Title is 100% English
- [ ] Body language matches the user's current language
- [ ] `--assignee @me` is present in the command
