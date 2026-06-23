---
name: leetcode-run
description: |
  Use when the user runs /run during an active LeetCode session. Executes their solution against the problem's examples plus a few edge cases, reporting pass/fail per case without fixing the code.
---

# LeetCode — Run

## Trigger

`/run` — execute the current solution against test cases.

---

## Steps

1. Read `.leetcode/performance/session-state.md` for the active `slug`.
2. Read `solutions/<slug>.py` (or the preferred language from `.leetcode/user-profile.md`).
3. Construct test cases:
   - The examples from the `# Examples:` block in the solution file.
   - 2–3 edge cases you construct: empty input, single element, boundary/max-constraint values — keep execution cheap (do not construct test cases that would time out).
4. Execute each case independently using `bash_tool`.
5. Report results plainly, one case per line:
   - ✅ `Case N: passed` — input → expected → got
   - ❌ `Case N: failed` — input → expected → got
6. Do not fix the code for the user. If cases fail, report only what failed and let them debug.
