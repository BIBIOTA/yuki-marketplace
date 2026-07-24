---
name: leetcode-run
description: |
  Use when the user runs /run during an active LeetCode session. Executes their solution against the problem's examples plus a few edge cases, reporting pass/fail per case without fixing the code.
---

# LeetCode — Run

## Language

Respond entirely in **Traditional Chinese (繁體中文)** — all test result reports and status messages.

## Trigger

`/run` — execute the current solution against test cases.

---

## Steps

1. Read `.leetcode/performance/session-state.md` for the active `slug`, `run_attempts`, and `run_failures`.
2. Read `./solutions/<slug>.py` (or the preferred language from `.leetcode/user-profile.md`).
3. Construct test cases:
   - The examples from the `# Examples:` block in the solution file.
   - 2–3 edge cases you construct: empty input, single element, boundary/max-constraint values — keep execution cheap (do not construct test cases that would time out).
4. Execute each case independently using `bash_tool`.
5. Report results plainly, one case per line:
   - **Example cases** (from `# Examples:`): show full `input → expected → got` — expected is already visible in the problem statement.
   - **Edge cases** (constructed by you): show only `input → got` on failure, **never reveal expected** — the user must reason what the correct output should be.
   - ✅ `Case N [example|edge]: passed` — input → got
   - ❌ `Case N [example|edge]: failed` — input → got (edge cases omit expected)
6. Do not fix the code for the user. If cases fail, report only what failed and let them debug.
7. Update `.leetcode/performance/session-state.md`:
   - Increment `run_attempts` by 1.
   - If any case failed, increment `run_failures` by 1.
8. If `run_failures` reaches 3 or more, append after the results:
   > Failed N times in a row — want to try `/hint` for a nudge?
