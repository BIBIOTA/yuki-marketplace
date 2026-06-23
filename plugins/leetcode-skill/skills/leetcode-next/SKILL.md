---
name: leetcode-next
description: |
  Use when the user runs /next or /leetcode --next. Reads weak-area data to identify the highest-priority pattern, suggests 2-3 suitable LeetCode problems, then hands off to the leetcode skill once the user picks one.
---

# LeetCode — Next Problem

## Triggers

- `/next`
- `/leetcode --next`

---

## Steps

1. Read `.leetcode/performance/weak-areas.md`.
   - If the file is missing or empty: "還沒有追蹤記錄，先用 `/leetcode <url>` 練一題吧！"
2. Sort patterns by struggle rate, highest first. Break ties by most recently attempted.
3. Pick the top pattern. Tell the user:
   > "根據你的記錄，你在 **<Pattern>** 最需要加強（struggle rate: X%，最近練習：<date>）。"
4. Suggest 2–3 well-known LeetCode problems in that category. For each, give:
   - Problem number + name
   - Slug (so they can construct the URL: `leetcode.com/problems/<slug>/`)
   - One-line description of why it's a good representative for this pattern
5. Once the user provides a URL (or picks a suggestion), invoke the `leetcode` skill to start the session with `/leetcode <url>`.
