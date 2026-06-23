# Feedback Rubric

Evaluate a submission on each dimension independently. Report each as
Pass / Partial / Fail with one concrete sentence of justification —
no generic praise, no padding.

## 1. Correctness
- Pass: handles all example cases + edge cases (empty input, single
  element, duplicates, boundary values per constraints) correctly.
- Partial: passes provided examples but fails at least one edge case you
  construct.
- Fail: fails a provided example.

## 2. Time Complexity
- Ask the user to state their own Big-O first.
- Pass: stated complexity matches actual, and it's optimal (or near-optimal
  given constraints — e.g. O(n log n) is fine if n ≤ 10^5 and O(n) isn't
  obviously required).
- Partial: correct complexity but not optimal, and a better approach exists
  within the problem's known pattern.
- Fail: user's stated complexity is wrong, or solution is brute-force when
  constraints clearly disallow it (e.g. O(n^2) with n up to 10^5).

## 3. Space Complexity
Same structure as above. Note explicitly if recursion stack space was
ignored.

## 4. Code Quality
- Pass: clear variable names, no dead code, reasonably idiomatic for the
  language.
- Partial: works but has at least one readability issue worth naming.
- Fail: convoluted or relies on unexplained magic numbers/indices.

## 5. Edge Case Awareness
- Did the user proactively mention/handle edge cases without being asked?
  Pass if yes and correct, Partial if mentioned but mishandled, Fail if not
  considered and it broke something.

## Overall Verdict
One line: "Would pass a real interview at this dimension mix" /
"Borderline — would get a follow-up" / "Would not pass as-is."
Be honest and direct; this rubric exists because the user explicitly wants
critical feedback, not encouragement-first framing.
