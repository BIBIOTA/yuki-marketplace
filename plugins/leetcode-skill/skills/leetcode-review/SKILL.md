---
name: leetcode-review
description: |
  Use when the user runs /review. Reads the spaced-repetition review schedule to find the highest-priority problem due for re-attempt, then hands off to the leetcode skill to start the session.
---

# LeetCode — Spaced Repetition Review

## Trigger

`/review` — surface the highest-priority problem due for review today.

---

## Steps

1. Read `.leetcode/performance/review-schedule.md`.
   - If the file is missing or empty: "No review history yet — complete and submit a problem first to start building your review queue!"
2. Filter problems where `due_date <= today`.
3. If no problems are due:
   - Find the problem with the nearest `due_date`.
   - Tell the user: "All caught up! Next review: **<number>. <name>** in X days."
   - Stop here.
4. Sort due problems:
   - Primary: days overdue descending (`today - due_date`), most overdue first.
   - Tiebreaker: `Gave up` results get an extra +7 day overdue weight added before sorting.
5. Take the top problem. Tell the user:
   > "Time to review: **<number>. <name>** — last result: <last_result>, due <due_date> (X days overdue / due today)."
6. Invoke the `leetcode` skill with `https://leetcode.com/problems/<slug>/` to start a fresh session (hint rung resets to 0, no old hints shown).
