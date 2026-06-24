---
name: leetcode-submit
description: |
  Use when the user runs /submit during an active LeetCode session. Runs full evaluation (correctness, complexity, code quality, edge case awareness) and asks 1-2 targeted follow-up questions. Does not log progress — that's /finish.
---

# LeetCode — Submit

## Trigger

`/submit` — full evaluation of the current solution.

---

## Steps

1. Read `.leetcode/performance/session-state.md` for the active `slug` and `current_hint_rung`.
2. Read `solutions/<slug>.py` (or preferred language from `.leetcode/user-profile.md`).
3. Run all example cases + edge cases (same construction rules as `/run`).

---

## Evaluation Rubric

Evaluate each dimension independently. Report each as **Pass / Partial / Fail** with one concrete sentence — no generic praise, no padding.

### 1. Correctness
- Pass: handles all example cases + edge cases correctly.
- Partial: passes provided examples but fails ≥1 edge case you construct.
- Fail: fails a provided example.

### 2. Time Complexity
- Ask the user to state their Big-O **before** you reveal your assessment.
- Pass: stated complexity matches actual and is optimal (or near-optimal given constraints — e.g. O(n log n) is fine if n ≤ 10⁵ and O(n) isn't obviously required).
- Partial: correct complexity but not optimal, and a better approach exists within the known pattern.
- Fail: user's stated complexity is wrong, or solution is brute-force when constraints clearly disallow it.

### 3. Space Complexity
- Same structure. Note explicitly if recursion stack space was ignored.

### 4. Code Quality
- Pass: clear variable names, no dead code, reasonably idiomatic for the language.
- Partial: works but has ≥1 readability issue worth naming.
- Fail: convoluted or relies on unexplained magic numbers/indices.

### 5. Edge Case Awareness
- Pass: user proactively mentioned or handled edge cases correctly without being prompted.
- Partial: mentioned but mishandled.
- Fail: not considered and it broke something.

### Overall Verdict
One line: "Would pass a real interview at this dimension mix" / "Borderline — would get a follow-up" / "Would not pass as-is." Be direct; don't soften.

---

## Follow-up Questions

After the rubric, ask 1–2 follow-ups that probe an actual weak point you noticed. Choose from:

1. **Why this pattern?** — "為什麼這裡適合用雙指針而不是雜湊表？" — tests whether they understand *why*, not just pattern-matched the title.
2. **Complexity justification** — "如果輸入是 10 萬筆，你的解法大概要跑多久？"
3. **Breaking case** — construct an input designed to break their logic if there's a subtle bug; ask them to predict output before running.
4. **Variant** — "如果題目改成陣列已排序，你的解法會怎麼變？" — tests adaptability.
5. **Trade-off** — if multiple valid approaches exist, ask which they'd choose under different constraints.

Give direct feedback on their answer — don't just move on if they're wrong, correct it.

---

## After evaluation

Ask: "你覺得這題用的是什麼 pattern？（例如：Sliding Window、Two Pointers、Hash Table）"

Give direct feedback if their answer is off. Then write to `.leetcode/performance/session-state.md`:
- Correctness Pass → `submit_result: passed`
- Correctness Partial → `submit_result: partial`
- Correctness Fail → `submit_result: fail`
- `pattern: <user's answer, corrected if needed>`

Then remind the user to run `/finish` to log the result and update their pattern notes.
