---
name: leetcode-hint
description: |
  Use when the user runs /hint during an active LeetCode session. Delivers exactly the next rung on the progressive hint ladder — never jumps ahead. Reads and updates session-state to resume correctly across turns.
---

# LeetCode — Hint

## Trigger

`/hint` — request the next level of hint during an active session.

---

## Before giving a hint

Read `.leetcode/performance/session-state.md`:
- `current_problem` — the active problem
- `slug` — used to locate the solution file
- `current_hint_rung` — which rung was last delivered (0 = no hints given yet)

If the file is missing or shows no active session, respond: "No active problem session. Start one with `/leetcode <url>`."

Then read `./solutions/<slug>.<ext>` (use the user's preferred language extension from `.leetcode/user-profile.md`). Note what the user has written so far:
- If the file has meaningful code beyond the stub, tailor the hint to what they've attempted — point specifically at the part that's incomplete or incorrect rather than restarting from scratch.
- If the file is still just the stub (no logic added), give the hint as normal without referencing it.

---

## Hint Ladder

**Never skip a rung.** Each `/hint` advances exactly one step:

1. **Rung 1 — Reframe.** Restate what the problem is really asking; point at which input property matters. No pattern name yet.
   - Example: "Notice the array is sorted — what does that property let you skip?"
2. **Rung 2 — Pattern category.** Name the general technique without explaining how to apply it to this specific problem.
   - Example: "This type of problem is a good fit for two pointers" / "Think about a sliding window"
3. **Rung 3 — Structural hint.** Describe the shape of the solution in plain language: what state to track, what the loop invariant is, what happens on each step. Still no code.
4. **Rung 4 — Pseudocode.** Give pseudocode or a heavily-commented skeleton. The user must still translate it to real code and fill in the core logic.
5. **Rung 5 — Worked micro-example.** Trace through the algorithm by hand on the example input, step by step.
   - **Only reach this rung if the user is still stuck after rung 4 AND explicitly asks again.**
   - Confirm before delivering: "Should I walk through the full solution logic? That's pretty close to the answer itself."

After delivering the hint, increment `current_hint_rung` in `.leetcode/performance/session-state.md`.

---

## Special case: "just give me the answer"

Say plainly: "Sure, skipping the hint ladder and going straight to the solution." Then give a full solution with explanation. Set `current_hint_rung: 5` in session-state.
