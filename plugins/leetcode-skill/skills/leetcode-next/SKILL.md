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
   - If the file is missing or empty: "No history yet — start with `/leetcode <url>` to practice your first problem!"
2. Sort patterns by struggle rate, highest first. Break ties by most recently attempted.
3. Pick the top pattern. Tell the user:
   > "Based on your history, **<Pattern>** needs the most work (struggle rate: X%, last practiced: <date>)."
4. Suggest 2–3 well-known LeetCode problems in that category. For each, give:
   - Problem number + name
   - Difficulty (Easy / Medium / Hard)
   - Slug (so they can construct the URL: `leetcode.com/problems/<slug>/`)
   - One-line description of why it's a good representative for this pattern
5. Once the user provides a URL (or picks a suggestion), invoke the `leetcode` skill to start the session with `/leetcode <url>`.
