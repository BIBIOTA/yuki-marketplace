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
- `current_hint_rung` — which rung was last delivered (0 = no hints given yet)

If the file is missing or shows no active session, respond: "目前沒有進行中的題目，請先用 `/leetcode <url>` 開始一題。"

---

## Hint Ladder

**Never skip a rung.** Each `/hint` advances exactly one step:

1. **Rung 1 — Reframe.** Restate what the problem is really asking; point at which input property matters. No pattern name yet.
   - Example: "注意陣列是已排序的，這個特性能省掉什麼？"
2. **Rung 2 — Pattern category.** Name the general technique without explaining how to apply it to this specific problem.
   - Example: "這類題目通常適合用雙指針" / "想想滑動窗口"
3. **Rung 3 — Structural hint.** Describe the shape of the solution in plain language: what state to track, what the loop invariant is, what happens on each step. Still no code.
4. **Rung 4 — Pseudocode.** Give pseudocode or a heavily-commented skeleton. The user must still translate it to real code and fill in the core logic.
5. **Rung 5 — Worked micro-example.** Trace through the algorithm by hand on the example input, step by step.
   - **Only reach this rung if the user is still stuck after rung 4 AND explicitly asks again.**
   - Confirm before delivering: "要我直接示範解法邏輯嗎？這樣會比較接近答案本身了。"

After delivering the hint, increment `current_hint_rung` in `.leetcode/performance/session-state.md`.

---

## Special case: "just give me the answer"

Say plainly: "好，我跳過提示階梯直接給解法。" Then give a full solution with explanation. Set `current_hint_rung: 5` in session-state.
