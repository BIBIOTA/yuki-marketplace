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
   - `submit_result: passed` + `current_hint_rung == 0` + `run_failures < 3` → **Passed**
   - `submit_result: passed` + (`current_hint_rung >= 1` OR `run_failures >= 3`) → **Passed (partial)**
   - `submit_result: partial` or `submit_result: fail` → **Struggled**
   - No `submit_result` (user never ran `/submit`) → **Gave up**

   > Rationale: `run_failures >= 3` indicates the user relied heavily on test-case feedback to debug, which is equivalent in difficulty signal to using hints. The `/run` output (which test failed, what was returned) is a form of external guidance even if `/hint` was never invoked.
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
- Increment `Solved cleanly` if hint rung ≤1 AND `run_failures < 3` AND result is `Passed`
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

### 6. `.leetcode/performance/review-schedule.md`

Upsert a section for this problem (create file if missing). Compute the new interval:

| Result | `current_interval_days` | `consecutive_passes` |
|---|---|---|
| `Passed` (hint rung ≤ 1 AND run_failures < 3) | `min(current × 2, 30)` | `+ 1` |
| `Passed (partial)` | `1` | `0` |
| `Struggled` | `1` | `0` |
| `Gave up` | `1` | `0` |

New entries (problem not yet in file) start with `current_interval_days: 1`, `consecutive_passes: 0`.

Set `due_date = today + current_interval_days`.

Section format:
```
## <number>. <name>
- slug: <slug>
- pattern: <pattern>
- last_result: <result>
- current_interval_days: <N>
- last_reviewed: <today>
- due_date: <due_date>
- consecutive_passes: <N>
```

---

## Alternative Approaches

Before showing the stats summary, present **2–3 alternative solutions** for the problem. For each:

- **Name the approach** (e.g. "Two Pointers", "Monotonic Stack", "Binary Search on answer").
- Show a concise implementation (≤20 lines; pseudocode is fine if the idea is clear).
- State **Time / Space complexity** and compare to the user's solution.
- One sentence on **when to prefer this** over the user's approach (e.g. "better when input is already sorted", "trades space for a O(n) speedup").

Ordering rule: start from the approach closest to the user's solution, then progress toward the most optimal.

---

## End

Show the user a one-line stats summary: problems attempted, pass rate, current top weak area. Suggest `/next` if they want a targeted follow-up problem.
