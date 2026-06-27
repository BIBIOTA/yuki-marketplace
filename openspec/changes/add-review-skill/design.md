---
change_id: add-review-skill
doc_language: English
---

# Design: Add `/review` Skill (Spaced Repetition)

## Overview

Add a `/review` slash command that uses spaced repetition to surface the highest-priority problem for the user to re-attempt. The review schedule is maintained automatically by `leetcode-finish` after every submit.

## Architecture

Three change points:

1. **New data file** — `.leetcode/performance/review-schedule.md`: per-problem review state, owned and updated by `leetcode-finish`
2. **New skill** — `leetcode-review`: handles `/review` trigger, reads the schedule, selects the top-priority problem, hands off to the `leetcode` skill
3. **Modified skill** — `leetcode-finish`: after writing `log.md` and `weak-areas.md`, upserts `review-schedule.md`

## Components

### `review-schedule.md` Format

One section per attempted problem, upserted on every submit:

```
## 1. Two Sum
- slug: two-sum
- pattern: Hash Table
- last_result: Passed
- current_interval_days: 14
- last_reviewed: 2026-06-28
- due_date: 2026-07-12
- consecutive_passes: 3
```

### Interval Algorithm

Difficulty-escalating intervals based on submit result:

| Result | Interval update | consecutive_passes |
|---|---|---|
| `Passed` (hint rung ≤ 1) | `interval × 2`, cap at 30 days | `+ 1` |
| `Passed (partial)` | reset to 1 day | `= 0` |
| `Struggled` | reset to 1 day | `= 0` |
| `Gave up` | reset to 1 day | `= 0` |

New problems start with `current_interval_days: 1`.

### `leetcode-review` Skill Flow

1. Read `.leetcode/performance/review-schedule.md`
   - Missing or empty → `"Submit a problem first to build your review queue."`
2. Filter problems where `due_date <= today`
3. No due items → `"Next due: <problem> in X days."` (show closest)
4. Sort due items: most overdue first; `Gave up` problems get extra priority weight
5. Take the top problem, announce it, then invoke `leetcode` skill with its URL

### `leetcode-finish` New Logic

After existing `log.md` and `weak-areas.md` updates, upsert `review-schedule.md`:
- If problem section exists: update `last_result`, `last_reviewed`, `due_date`, `current_interval_days`, `consecutive_passes`
- If problem section is new: create entry with `current_interval_days: 1`, `consecutive_passes: 0`

## Data Flow

```
User: /review
  └─ leetcode-review skill
       ├─ read .leetcode/performance/review-schedule.md
       ├─ [no file] → guidance message
       ├─ [no due items] → show next upcoming problem
       └─ [due items found] → announce top problem → /leetcode <url>

User: /submit (inside a session)
  └─ leetcode-submit → leetcode-finish
       ├─ write log.md (existing)
       ├─ write weak-areas.md (existing)
       └─ upsert review-schedule.md
            ├─ problem exists → update interval + due_date
            └─ problem new → create entry, interval = 1 day
```

## Error Handling

| Scenario | Behavior |
|---|---|
| `review-schedule.md` missing | Show guidance message, no error |
| No problems due today | Show next upcoming problem and days remaining |
| Same problem submitted multiple times in one day | `leetcode-finish` upserts in-place, no duplicate sections |
| Problem URL inaccessible | Handled by `leetcode` skill, `leetcode-review` does not need to handle |

## Testing

- `leetcode-finish` correctly writes `review-schedule.md` for all result types (interval math, 30-day cap, consecutive_passes increment/reset)
- `leetcode-review` correctly filters and sorts due problems (`Gave up` weighted first, most overdue first)
- No-due-items path shows correct "next in X days" message
- First-use path (no `review-schedule.md`) shows guidance message

Test approach: manually author `review-schedule.md` fixtures and trigger `/review`; run full `/submit` sessions and inspect `review-schedule.md` output.

## Probable Next Steps

- UML: not needed (flow is linear, no complex state machine)
- Figma: not needed (CLI skill, no UI)
