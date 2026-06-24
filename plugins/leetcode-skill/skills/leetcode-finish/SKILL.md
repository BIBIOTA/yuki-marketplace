---
name: leetcode-finish
description: |
  Use when the user runs /finish after completing or giving up on a LeetCode problem. Logs the result, updates weak-area tracking, writes a concrete pattern cheat-sheet entry, and clears session state.
---

# LeetCode — Finish

## Trigger

`/finish` — wrap up the current problem session after submitting or giving up.

---

## Steps

1. Read `.leetcode/performance/session-state.md` for: `current_problem`, `slug`, `current_hint_rung`, `submit_result`, `run_attempts`, `pattern`, `started`.
2. Derive result automatically — do not ask the user:
   - `submit_result: passed` + `current_hint_rung == 0` → **Passed**
   - `submit_result: passed` + `current_hint_rung >= 1` → **Passed (partial)**
   - `submit_result: partial` or `submit_result: fail` → **Struggled**
   - No `submit_result` (user never ran `/submit`) → **Gave up**
3. Calculate time spent from `started` to now. If `started` is absent, omit the time field.
4. Use `pattern` from session-state. If absent (user skipped `/submit`), leave the pattern field blank in logs.

---

## Update tracking files (do all four)

### 1. `.leetcode/performance/log.md`

Append a row at the bottom (create file with header if missing):

```
| Date       | Problem (# + name)      | Pattern         | Result           | Hint rung reached | Notes |
|------------|-------------------------|-----------------|------------------|-------------------|-------|
| <date>     | <number>. <name>        | <pattern>       | <result>         | <rung>            | <note>|
```

Result values: `Passed`, `Passed (partial)`, `Struggled`, `Gave up`.

### 2. `.leetcode/performance/weak-areas.md`

Find the section for this pattern (create if missing). Update fields:
- Increment `Attempts`
- Increment `Solved cleanly` if hint rung ≤1 AND result is `Passed`
- Recompute `Struggle rate` = (Attempts − Solved cleanly) / Attempts × 100%
- Update `Last attempted` to today's date
- Recompute `Status`:
  - 🟢 Solid — struggle rate < 20%
  - 🟡 Developing — 20–50%
  - 🔴 Needs work — > 50%

### 3. `.leetcode/notes/<pattern-name>.md`

Append a cheat-sheet entry using **this problem's actual numbers** (not abstract theory):

```markdown
### From: <number>. <name> (<date>)

Input: <actual example input from the problem>
Approach: <1–2 sentence summary of the solution strategy>
Key insight: <the single thing that unlocked the solution>

<Trace one example step-by-step if the algorithm involves non-obvious state transitions>

Mistake I made: <if any — be specific about what went wrong and why>
```

### 4. `.leetcode/performance/session-state.md`

Clear the file — write: `# no active session`

### 5. `.leetcode/user-profile.md`

Increment `total_attempted`. Increment `total_passed` if result is `Passed` or `Passed (partial)`.

---

## End

Show the user a one-line stats summary: problems attempted, pass rate, current top weak area. Suggest `/next` if they want a targeted follow-up problem.
