---
name: leetcode
description: |
  Use when the user runs /leetcode <url>, /leetcode --profile, or /leetcode --review. Fetches and paraphrases the problem, creates a solution stub, and initialises session state. Sub-skills handle the rest of the session.
---

# LeetCode — Start / Profile / Review

## Triggers

- `/leetcode <url>` — start a practice session on a specific problem
- `/leetcode --profile` — show progress dashboard / edit settings
- `/leetcode --review` — re-attempt a previously-struggled problem

---

## ⚠️ Copyright constraint (read every session)

LeetCode problem text is copyrighted. When you fetch a problem page:

- **Never reproduce the original problem text verbatim**, even partially.
- **Paraphrase fully**: rewrite the scenario, examples, and constraints in your own words. Preserve all information (data ranges, exact numbers) but not the wording.
- Problem number, title, difficulty, and topic tags are facts — state them plainly.
- If you can't access the page content (JS-rendered, auth wall), say honestly: "我抓不到題目完整內容，可以請你把題目敘述貼給我嗎？" — do not fabricate.

---

## `/leetcode <url>` — Start Session

1. Use `web_fetch` on the URL.
   - If it returns mostly boilerplate (JS-rendered), try `web_search` for `"<problem name>" leetcode problem statement` to find a mirror for constraints — still paraphrase, never quote verbatim.
   - If still no content, ask the user to paste the description.
2. Present to the user in your own words:
   - Problem number, title, difficulty, topic tags
   - Paraphrased scenario + examples (keep exact numbers/arrays)
   - Paraphrased constraints
   - Do NOT reveal the pattern or approach yet.
3. Check `.leetcode/user-profile.md` for preferred language (default: Python). Ask once if not set, then save it.
4. Create/overwrite `solutions/<problem-slug>.py` (or preferred language) with:
   - Function stub matching the real LeetCode signature for that problem
   - A `# Examples:` comment block with the paraphrased test cases
5. Write `.leetcode/performance/session-state.md`:
   ```
   current_problem: <number>. <name>
   slug: <slug>
   pattern: (leave blank — fill in at /finish)
   current_hint_rung: 0
   started: <ISO datetime>
   ```
6. Tell the user to start coding. Do not solve it for them.
7. Remind them of available commands: `/run` · `/hint` · `/submit` · `/finish` · `/next`.

---

## `/leetcode --profile`

Read `.leetcode/performance/log.md` and `.leetcode/performance/weak-areas.md`. Show:

- Total problems attempted and overall pass rate
- Breakdown by pattern: attempts / solved cleanly / avg hint rung reached
- Weak areas sorted worst-first (highest struggle rate first)
- Current language preference from `.leetcode/user-profile.md`

Offer to let the user edit language preference or reset stats.

---

## `/leetcode --review`

Read `.leetcode/performance/log.md`. List all problems marked `Struggled` or `Gave up`. Let the user pick one, then:

1. Fetch the problem via `/leetcode <url>` flow (fresh session, hint rung reset to 0).
2. Do NOT show old notes or previous hints until the user finishes or explicitly asks.
