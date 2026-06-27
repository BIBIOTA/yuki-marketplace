# Progress Tracking — File Formats

All files live under `.leetcode/` at the project root. Create them if missing.

## `.leetcode/performance/log.md`

Append-only table, newest row at bottom:

```
| Date       | Problem (# + name)      | Pattern         | Result      | Hint rung reached | Run attempts | Notes |
|------------|--------------------------|-----------------|-------------|-------------------|--------------|-------|
| 2026-06-23 | 1. Two Sum               | Hash Table      | Passed      | 0                 | 2            |       |
| 2026-06-23 | 3. Longest Substring...  | Sliding Window  | Struggled   | 4                 | 7            | Off-by-one on window shrink |
```

Result values: `Passed`, `Passed (partial)`, `Struggled`, `Gave up`.

## `.leetcode/performance/weak-areas.md`

One section per pattern, auto-maintained:

```
## Sliding Window
- Attempts: 4
- Solved cleanly (hint rung ≤1): 1
- Struggle rate: 75%
- Last attempted: 2026-06-23
- Status: 🔴 Needs work

## Hash Table
- Attempts: 3
- Solved cleanly: 3
- Struggle rate: 0%
- Status: 🟢 Solid
```

Status thresholds: 🟢 Solid (struggle rate <20%), 🟡 Developing (20-50%),
🔴 Needs work (>50%). Recompute after every logged attempt.

## `.leetcode/notes/<pattern-name>.md`

Cheat sheet per pattern, appended to (don't overwrite). Each entry must use
**concrete numbers from a real solved problem**, not abstract theory:

```
### From: 3. Longest Substring Without Repeating Characters (2026-06-23)

Input: "abcabcbb"
Window: track last-seen index of each char in a dict.
When `s[right]` already in window and its last index >= left,
jump `left` to `last_seen[s[right]] + 1`.

Trace:
left=0, right=3 (s[3]='a'), 'a' last seen at 0 >= left=0 → left=1
...

Mistake I made: forgot the `>= left` check, jumped left even when the
duplicate was outside the current window — caused window to shrink
incorrectly on input "abba".
```

## `.leetcode/performance/session-state.md`

Tracks in-progress problem so `/hint` resumes correctly across turns/sessions:

```
current_problem: 3. Longest Substring Without Repeating Characters
slug: longest-substring-without-repeating-characters
current_hint_rung: 2
run_attempts: 4
run_failures: 3
submit_result: passed
pattern: Sliding Window
started: 2026-06-23T10:15
```

- `run_attempts` — total `/run` executions this session (default 0).
- `run_failures` — number of runs where at least one case failed (default 0).
- `submit_result` — Correctness verdict from `/submit`: `passed`, `partial`, or `fail`. Absent if `/submit` was never called.
- `pattern` — pattern name confirmed at `/submit` (user's answer, corrected if needed). Absent if `/submit` was never called.

Clear this file (or overwrite) when a problem is submitted or abandoned.

## `.leetcode/performance/review-schedule.md`

One section per attempted problem, upserted by `leetcode-finish` after every submit:

```
## 1. Two Sum
- slug: two-sum
- pattern: Hash Table
- last_result: Passed
- current_interval_days: 14
- last_reviewed: 2026-06-28
- due_date: 2026-07-12
- consecutive_passes: 3

## 3. Longest Substring Without Repeating Characters
- slug: longest-substring-without-repeating-characters
- pattern: Sliding Window
- last_result: Struggled
- current_interval_days: 1
- last_reviewed: 2026-06-28
- due_date: 2026-06-29
- consecutive_passes: 0
```

Read by `leetcode-review` skill (`/review`) to surface the highest-priority problem due for re-attempt.

## `.leetcode/user-profile.md`

```
preferred_language: python
total_attempted: 7
total_passed: 5
```
