---
name: writing-plans
description: Use when openspec/changes/{change-id}/design.md exists and tasks must be decomposed into an OpenSpec-format tasks.md checklist - reads the approved design, breaks work into bite-sized tasks with WHEN/THEN acceptance criteria, confirms whether the change needs writing-uml and/or writing-figma, then chains to the next skill in the pipeline.
---

# Writing Implementation Plans

Decompose an approved design into a concrete, reviewable task checklist, then hand off to the next skill in the spec-driven-dev pipeline.

<HARD-GATE>
Do NOT invoke `spec-driven-dev:writing-uml`, `spec-driven-dev:writing-figma`, or `spec-driven-dev:writing-spec` until the user has approved tasks.md.

**Language:** All user-facing replies in this skill MUST use the user's input language; internal template strings (file paths, code blocks, OpenSpec keywords) stay in English. Reuse the language detected in design.md or the first user message.

**Document language:** Write tasks.md body prose in the `doc_language` value from design.md frontmatter. If no frontmatter is present, default to the detected conversation language.
</HARD-GATE>

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Detect language** — reuse the conversation language from design.md frontmatter (or fall back to the user's first message language). Also read `doc_language` from design.md frontmatter; this controls what language to write tasks.md body prose in. Lock both for the conversation.
2. **In-flight change precheck** — scan `openspec/changes/*/` for directories that have `design.md` but no `verification-report.md` (= in-flight).
   - If no in-flight change is found (other than the one matching this skill's argument), proceed directly to step 3 — no warning, no prompt.
   - If any in-flight change OTHER than the one matching this skill's argument is found, pause before step 3 and prompt the user verbatim: "偵測到 in-flight change `{change-id}`，要 resume 還是開新？".
     - On "resume" invoke `spec-driven-dev:resume`.
     - On "新" emit a warning that the in-flight change's progress is preserved but this session switches context, then proceed to step 3.
3. **Read `openspec/changes/{change-id}/design.md`** completely.
4. **Validate change-id and directory exist.** If not, escalate: "design.md not found — return to spec-driven-dev:brainstorming."
5. **Decompose into bite-sized tasks.** Each task entry must include:
   - Imperative title (e.g., "Add /login POST endpoint")
   - Acceptance criteria using `WHEN ... THEN ...` (and optionally `AND`) format
   - Dependencies: list any prerequisite task numbers
   - Independence estimate (note as `independent`, `serial`, or `parallel-safe` — used by downstream SDD/TDD selection)
6. **Confirm optional artifacts** with this exact multi-select prompt (verbatim, but adapt language):
   > Does this change require any of the following artifacts before implementation? (multi-select)
   > - [ ] PlantUML diagrams (spec-driven-dev:writing-uml) — fits: complex flows, state machines, cross-component interactions, ER schemas
   > - [ ] Figma designs (spec-driven-dev:writing-figma) — fits: frontend UI, interactive prototypes, A/B version comparison
7. **Write tasks.md** to `openspec/changes/{change-id}/tasks.md` using the template below. Include a `## Optional artifacts` section marking the user's selection.
8. **Spec self-review** — four checks: placeholder / consistency / scope / ambiguity. Fix inline.
9. **User review gate** — say verbatim:
   > "tasks.md written to `{path}`. Please review and tell me whether to proceed or make changes."

   Then `git add` and `git commit` the file:
   ```
   git add openspec/changes/{change-id}/tasks.md
   git commit -m "docs: add tasks for {change-id}"
   ```
10. **Transition logic:**
    ```
    if writing-uml selected → invoke spec-driven-dev:writing-uml
    elif writing-figma selected → invoke spec-driven-dev:writing-figma
    else → invoke spec-driven-dev:writing-spec
    ```

## Process Flow

```dot
digraph writing_plans {
    rankdir=TB;

    "Detect language" [shape=box];
    "In-flight change precheck" [shape=diamond];
    "Invoke spec-driven-dev:resume" [shape=doublecircle];
    "Read design.md" [shape=box];
    "Validate change-id directory exists" [shape=box];
    "Decompose into tasks" [shape=box];
    "Confirm optional artifacts (UML/Figma)" [shape=box];
    "Write tasks.md" [shape=box];
    "Self-review" [shape=box];
    "User review gate" [shape=diamond];
    "Invoke spec-driven-dev:writing-uml" [shape=doublecircle];
    "Invoke spec-driven-dev:writing-figma" [shape=doublecircle];
    "Invoke spec-driven-dev:writing-spec" [shape=doublecircle];

    "Detect language" -> "In-flight change precheck";
    "In-flight change precheck" -> "Invoke spec-driven-dev:resume" [label="in-flight found + resume"];
    "In-flight change precheck" -> "Read design.md" [label="in-flight found + 新 (warn + proceed)"];
    "In-flight change precheck" -> "Read design.md" [label="no in-flight (proceed)"];
    "Read design.md" -> "Validate change-id directory exists";
    "Validate change-id directory exists" -> "Decompose into tasks";
    "Decompose into tasks" -> "Confirm optional artifacts (UML/Figma)";
    "Confirm optional artifacts (UML/Figma)" -> "Write tasks.md";
    "Write tasks.md" -> "Self-review";
    "Self-review" -> "User review gate";
    "User review gate" -> "Write tasks.md" [label="changes requested"];
    "User review gate" -> "Invoke spec-driven-dev:writing-uml" [label="UML selected"];
    "User review gate" -> "Invoke spec-driven-dev:writing-figma" [label="Figma selected (no UML)"];
    "User review gate" -> "Invoke spec-driven-dev:writing-spec" [label="no artifacts selected"];
}
```

## tasks.md Template

Use this template when writing `openspec/changes/{change-id}/tasks.md`:

````markdown
# Tasks: {change-id}

## 1. {Group name}
- [ ] 1.1 {Task description}
  - Acceptance: WHEN {context} THEN {expected outcome}
  - Depends on: -
  - Independence: independent | serial | parallel-safe
  - status: not_started
- [ ] 1.2 {Task description}
  - Acceptance: WHEN {context} THEN {expected outcome}
  - Depends on: 1.1
  - Independence: serial
  - status: not_started

## Optional artifacts
- [x] PlantUML diagrams (spec-driven-dev:writing-uml) — required types: sequence, state
- [ ] Figma designs (spec-driven-dev:writing-figma)
````

### Task status state machine

Every task entry MUST carry a `- status: {state}` sub-bullet. New tasks are written with `status: not_started`; downstream skills (SDD, TDD, verification, resume) update the status on every transition.

Allowed states:

- `not_started` — task has not been picked up yet (initial state for every new task)
- `in_progress` — actively being implemented in the current session
- `passing` — implementation complete, tests / reviews green, terminal
- `blocked` — implementer paused (BLOCKED / NEEDS_CONTEXT or TDD step cannot proceed); resumable later

Allowed transitions:

- `not_started → in_progress`
- `in_progress → passing`
- `in_progress → blocked`
- `blocked → in_progress`

Forbidden transitions (any of these is a spec violation — skills MUST raise an error rather than silently rewrite):

- `not_started → passing` (work cannot skip implementation)
- `not_started → blocked` (cannot block work that has not started)
- `passing → not_started`, `passing → in_progress`, `passing → blocked` (`passing` is terminal; reopen via a new change, never by mutating status)
- `blocked → not_started` (resume via `blocked → in_progress`, never by erasing progress)
- `blocked → passing` (must re-enter `in_progress` so the unblock is recorded)
- any state → itself (no-op self-transitions are not recorded)

Single-in-progress invariant: across all tasks in a change, at most ONE task may have `status: in_progress` at any time. SDD and TDD assert this before dispatching new work; `resume` raises an error without auto-fixing when the invariant is violated.

## Spec Self-Review

After writing tasks.md, apply these four checks. Fix any issues inline — no re-review needed after fixing.

1. **Placeholder scan:** Any "TBD", "TODO", incomplete acceptance criteria, or missing dependency references? Fix.
2. **Consistency check:** Do task groupings match the architecture sections in design.md? Do acceptance criteria contradict each other? Fix.
3. **Scope check:** Are tasks scoped to the current change-id? Remove anything belonging to a different change. Fix.
4. **Ambiguity check:** Could any WHEN/THEN criterion be interpreted two different ways? Pick one interpretation, make it explicit. Fix.

## Transition Handoff

After the user approves tasks.md, transition to exactly one of:

- `spec-driven-dev:writing-uml` — if PlantUML diagrams were selected
- `spec-driven-dev:writing-figma` — if Figma designs were selected (and UML was not)
- `spec-driven-dev:writing-spec` — if no optional artifacts were selected

`spec-driven-dev:writing-uml` also covers the case when **both** UML and Figma were selected — UML runs first, and the writing-uml skill chains to writing-figma when its own transition logic detects that Figma was also selected.

Invoke only the `spec-driven-dev:*` versions via Skill tool. Do NOT invoke `superpowers:writing-uml`, `superpowers:writing-figma`, or `superpowers:writing-spec` — they are different skills with different downstream chains.
