# Progress Tracking — File Formats

All files live under `.leetcode/` at the project root. Create them if missing.

## `.leetcode/performance/log.md`

Append-only table, newest row at bottom:

```
| Date       | Problem (# + name)      | Pattern         | Result      | Hint rung reached | Notes |
|------------|--------------------------|------------------|--------------|--------------------|-------|
| 2026-06-23 | 1. Two Sum               | Hash Table       | Passed       | 0                  |       |
| 2026-06-23 | 3. Longest Substring...  | Sliding Window   | Struggled    | 4                  | Off-by-one on window shrink |
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
started: 2026-06-23T10:15
```

Clear this file (or overwrite) when a problem is submitted or abandoned.

## `.leetcode/user-profile.md`

```
preferred_language: python
total_attempted: 7
total_passed: 5
```
