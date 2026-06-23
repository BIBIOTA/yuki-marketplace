---
name: leetcode-practice
description: |
  Use when the user runs /leetcode <url>, /hint, /leetcode --next, /leetcode --profile, or /leetcode --review. Guides real LeetCode problem sessions with progressive hints and persistent progress tracking.
---

# LeetCode Practice Skill (Custom — Real Problems via URL)

## Purpose

Help the user practice **real, existing LeetCode problems** (provided by URL),
with progressive hint-based help when stuck, and persistent progress tracking
across sessions.

This skill is triggered by these commands:

- `/leetcode <url>` — start a practice session on a specific LeetCode problem
- `/leetcode --next` — pick a problem targeting the user's weakest tracked area
- `/hint` — request the next level of hint during an active session
- `/leetcode --profile` — show progress dashboard / edit settings
- `/leetcode --review` — re-attempt a previously-struggled problem

---

## ⚠️ Copyright constraint (read first, every session)

LeetCode problem text (title, description, examples, constraints wording) is
copyrighted content. When you fetch a problem page:

- **Never paste or reproduce the original problem text verbatim**, even
  partially, even formatted as a quote.
- **Paraphrase fully**: rewrite the scenario, the input/output examples, and
  the constraints in your own words. Preserve all *information* (data ranges,
  edge cases, exact numbers in examples) but not the *wording*.
- It's fine to keep things like LeetCode problem number, title, difficulty,
  and topic tags as-is (these are facts, not protected expression) — but
  state them plainly, don't quote the page.
- If you can't access the page content (auth wall, JS-rendered content not
  visible via fetch), say so honestly and ask the user to paste the
  description text manually instead of guessing or inventing one.

---

## Phase 1 — Fetch & Paraphrase the Problem

1. The user gives a LeetCode URL (e.g. `/leetcode https://leetcode.com/problems/two-sum/`).
2. Use `web_fetch` on the URL.
   - LeetCode's problem pages are often client-rendered. If `web_fetch`
     returns mostly navigation/boilerplate with no real problem statement,
     try `web_search` for `"<problem name>" leetcode problem statement` to
     find a mirror or cross-reference (e.g. GeeksforGeeks, a GitHub repo
     solution writeup) to corroborate constraints — still paraphrase, still
     attribute nothing verbatim.
   - If you still can't recover the actual statement, tell the user plainly:
     "我抓不到題目完整內容,可以請你把題目敘述貼給我嗎?" — do not fabricate
     a problem that merely sounds plausible for that title.
3. Once you have the real content, present to the user in your own words:
   - Problem number, title, difficulty, topic tags
   - Paraphrased scenario + paraphrased examples (keep exact numbers/arrays)
   - Paraphrased constraints
   - Do NOT reveal the pattern/approach yet.
4. Create/overwrite `solutions/<problem-slug>.py` (or the user's preferred
   language — ask once, then remember via profile) with:
   - A function stub matching the real LeetCode signature for that problem
   - A `# Examples:` comment block with the paraphrased test cases
5. Tell the user to start coding. Do not solve it for them.

## Phase 2 — Working Session

- The user codes in the solution file.
- "run" → execute their code against the example test cases (and a couple of
  edge cases you construct, e.g. empty input, single element, max constraint
  if cheap to test) using `bash_tool`. Report pass/fail per case plainly.
- "submit" → run full evaluation (see `references/feedback-rubric.md`):
  correctness, time/space complexity stated by user vs actual, code quality,
  edge case coverage. Give pass/fail per dimension, not just vibes.
- Ask 1–2 dynamic follow-up questions about their approach (why this
  pattern, what's the complexity, what would break it) — see
  `references/followup-guidance.md`.

## Phase 3 — Stuck? Progressive Hints (`/hint`)

**Never jump straight to the answer.** Each `/hint` call advances exactly one
rung on this ladder, no more:

1. **Rung 1 — Reframe.** Restate what the problem is really asking, point at
   which input property matters (e.g. "注意陣列是已排序的,這個特性能省掉什麼?").
   No pattern name yet.
2. **Rung 2 — Pattern category.** Name the general technique category (e.g.
   "這類題目通常適合用雙指針" / "想想滑動窗口") without explaining how to
   apply it to this specific problem.
3. **Rung 3 — Structural hint.** Describe the shape of the solution in plain
   language (what state to track, what the loop invariant is, what to do on
   each step) — still no code.
4. **Rung 4 — Pseudocode.** Give pseudocode or heavily-commented skeleton,
   still requiring the user to translate to real code and fill in the core
   logic line(s).
5. **Rung 5 — Worked micro-example.** Trace through the algorithm by hand on
   the example input, step by step, so the user can see *why* it works. Only
   reach this rung if the user is still stuck after rung 4 and asks again —
   confirm first: "要我直接示範解法邏輯嗎?這樣會比較接近答案本身了。"

Track the current rung per problem in `.leetcode/performance/session-state.md`
so `/hint` resumes correctly even in a new conversation. Never reset to rung 1
on a new turn within the same problem unless the user explicitly restarts.

If the user says "just give me the answer," skip ahead but say plainly that
you're skipping the ladder, then give a full solution with explanation
afterward.

## Phase 4 — Wrap-up: Notes + Progress Tracking

After a problem is submitted (pass or give-up), **always** update tracking —
see `references/progress-tracking.md` for exact file formats:

1. Append a row to `.leetcode/performance/log.md` (date, problem, pattern,
   result, hints used, time spent if known).
2. Update `.leetcode/performance/weak-areas.md`: increment struggle count for
   the pattern if hints reached rung ≥3 or the user didn't pass; decrement /
   mark mastered if solved cleanly with ≤1 hint.
3. Write or append to `.leetcode/notes/<pattern>.md`: a concrete cheat-sheet
   entry using THIS problem's actual numbers as the example (not abstract
   theory) — see note style guidance in `references/progress-tracking.md`.

## `/leetcode --next`

Read `.leetcode/performance/weak-areas.md`, pick the pattern with the
highest struggle count / lowest recent success rate. Ask the user for a
LeetCode URL in that pattern category (you can suggest 2-3 well-known
problem names+slugs for that pattern so they can find the link quickly), then
proceed as Phase 1.

## `/leetcode --profile`

Show: total problems attempted, pass rate, breakdown by pattern (attempts /
solved / avg hint rung), and current weak areas sorted worst-first. Offer to
let the user edit language preference or reset stats.

## `/leetcode --review`

List problems in `log.md` marked "struggled" or "gave up." Let the user pick
one to re-attempt from scratch (fresh hint ladder, no peeking at old notes
until they finish or ask).
