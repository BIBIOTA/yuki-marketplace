# Tasks: add-cross-session-harness

## 1. Foundation: task status field

- [x] 1.1 Update `plugins/spec-driven-dev/skills/writing-plans/SKILL.md` to embed task status into the tasks.md template
  - Acceptance: WHEN reading the updated writing-plans SKILL.md THEN the `## tasks.md Template` section shows a `- status: not_started` sub-bullet on each task example AND a new subsection documents the 4-state machine (`not_started → in_progress → passing | blocked`) with forbidden transitions explicitly listed AND a new bullet in the Checklist asserts "in-flight change precheck" before step 2 (Read design.md)
  - Depends on: -
  - Independence: independent
  - status: passing
  - evidence: 316980c (round 2 after code-quality fixes)

## 2. SDD / TDD progress integration

- [x] 2.1 Update `plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md` to enforce single-in-progress invariant and write progress.md on every status transition
  - Acceptance: WHEN reading the updated SDD SKILL.md THEN the Checklist has a new item between current step 2 and step 3 that runs the in-flight precheck (offer resume vs continue) AND a new item asserts at most one tasks.md entry has `status: in_progress` before dispatching AND step 5.a (implementer dispatch) is amended to (i) flip the target task status to `in_progress` and (ii) append a Session entry to `openspec/changes/{change-id}/progress.md` with `Stage: SDD`, the task id, `Transition: not_started → in_progress`, and a `Next action` line AND step 5.d (mark complete) is amended to (i) flip status to `passing` and (ii) append a Session entry with `Transition: in_progress → passing`, evidence (commit hash(es) from the implementer + reviewer outcomes), and a `Next action` line AND a new step covers the BLOCKED path: when implementer returns BLOCKED, flip status to `blocked` and append a Session entry with `Transition: in_progress → blocked`, the blocker description, and a `Next action` line
  - Depends on: 1.1
  - Independence: parallel-safe (with 2.2)
  - status: passing
  - evidence: manual inspection + `openspec validate add-cross-session-harness --strict`

- [x] 2.2 Update `plugins/spec-driven-dev/skills/test-driven-development/SKILL.md` with the same precheck, invariant, and per-transition progress.md writes as 2.1
  - Acceptance: WHEN reading the updated TDD SKILL.md THEN the Checklist has the same in-flight precheck and single-in-progress invariant assertion as 2.1 AND the per-task TDD loop is amended so step 1 (Identify spec coverage) is preceded by (i) flipping status to `in_progress` and (ii) appending a Session entry with `Stage: TDD`, the task id, `Transition: not_started → in_progress`, and a `Next action` line AND step 11 (Mark task complete) is preceded by (i) flipping status to `passing` and (ii) appending a Session entry with `Transition: in_progress → passing`, the green commit hash + (if applicable) refactor commit hash, a short test output excerpt, and a `Next action` line AND if any step (Red/Green/Refactor) cannot proceed and the task is paused, the skill flips status to `blocked` and appends a Session entry with `Transition: in_progress → blocked`, the blocker description, and a `Next action` line
  - Depends on: 1.1
  - Independence: parallel-safe (with 2.1)
  - status: passing
  - evidence: manual inspection + `openspec validate add-cross-session-harness --strict`

- [x] 2.3 Update `plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md` Stage 2 to require progress.md exists with non-empty `Next action` on the last entry
  - Acceptance: WHEN reading the updated verification SKILL.md THEN Stage 2 contains a new item (between current 5 and 6) that reads `openspec/changes/{change-id}/progress.md` AND fails Stage 2 if the file does not exist OR if the last `## Session N` block lacks a non-empty `- Next action:` line AND the verification-report.md template gains a "Progress log: PASS | FAIL" line in the Summary
  - Depends on: -
  - Independence: independent (no shared lines with 2.1/2.2)
  - status: passing
  - evidence: dbdfd9a

## 3. Resume skill

- [x] 3.1 Create `plugins/spec-driven-dev/skills/resume/SKILL.md`
  - Acceptance: WHEN reading the new resume SKILL.md THEN it has YAML frontmatter with `name: resume` and a description matching the manual-+-upstream-precheck trigger model AND a Checklist that (i) scans `openspec/changes/*/` for "design.md exists, verification-report.md missing", (ii) handles 0/1/>1 in-flight cases per the design.md routing table, (iii) on 1 in-flight reads `progress.md` last entry and routes by `Stage` field (SDD → subagent-driven-development, TDD → test-driven-development, verification → verification-before-completion) AND falls back to file-presence inference when progress.md is missing AND raises an error without auto-fixing when the single-in-progress invariant is violated AND a Process Flow `digraph` covers the same branches AND error handling section enumerates the cases in the design.md "Error handling" table
  - Depends on: 1.1, 2.1, 2.2
  - Independence: serial (foundation skill that others reference)
  - status: passing
  - evidence: new `plugins/spec-driven-dev/skills/resume/SKILL.md` + JSON/openspec validation

## 4. Upstream skill prechecks

- [x] 4.1 Update `plugins/spec-driven-dev/skills/brainstorming/SKILL.md` to add an in-flight precheck at skill entry
  - Acceptance: WHEN reading the updated brainstorming SKILL.md THEN the Checklist gains a new step 1.5 (between Detect language and Explore project context) that scans `openspec/changes/*/` for in-flight changes AND if found prompts the user verbatim "偵測到 in-flight change `{change-id}`，要 resume 還是開新？" AND on "resume" invokes `spec-driven-dev:resume` AND on "新" emits a warning that the in-flight change's progress is preserved but this session switches context
  - Depends on: 3.1
  - Independence: parallel-safe (with 4.2)
  - status: passing
  - evidence: manual inspection + `rg` acceptance keyword check

- [x] 4.2 Update `plugins/spec-driven-dev/skills/writing-spec/SKILL.md` to add the same in-flight precheck as 4.1
  - Acceptance: WHEN reading the updated writing-spec SKILL.md THEN the Checklist gains the same in-flight precheck step before step 2 (Read ALL artifacts) AND the prompt and routing match 4.1
  - Depends on: 3.1
  - Independence: parallel-safe (with 4.1)
  - status: passing
  - evidence: manual inspection + `rg` acceptance keyword check

## 5. Registration & documentation

- [x] 5.1 Update `plugins/spec-driven-dev/.claude-plugin/plugin.json` to register the resume skill
  - Acceptance: WHEN reading the updated .claude-plugin/plugin.json THEN the `skills` array contains `./skills/resume` AND the existing entries and ordering are preserved AND the file is valid JSON (no trailing comma, correct quoting)
  - Depends on: 3.1
  - Independence: parallel-safe (with 5.2, 5.3)
  - status: passing
  - evidence: `python3 -m json.tool plugins/spec-driven-dev/.claude-plugin/plugin.json`

- [x] 5.2 Update `plugins/spec-driven-dev/.codex-plugin/plugin.json` to register the resume skill at the same version as the Claude manifest
  - Acceptance: WHEN reading the updated .codex-plugin/plugin.json THEN the `skills` array contains `./skills/resume` AND the `version` field matches `.claude-plugin/plugin.json` AND the file is valid JSON
  - Depends on: 3.1, 5.1
  - Independence: serial (must match 5.1's resulting version)
  - status: passing
  - evidence: `python3 -m json.tool plugins/spec-driven-dev/.codex-plugin/plugin.json`; version matches Claude manifest (`0.1.0`)

- [x] 5.3 Update `README.md` (repo root) to document the new resume skill and progress.md artifact
  - Acceptance: WHEN reading the updated README.md THEN the `### Skills` table under `## Plugin: spec-driven-dev` has a new row `| resume | session 入口；偵測 in-flight change 並路由回對應 skill |` placed as the FIRST row of the table (entry-point semantics, before `brainstorming`) AND the line `Artifacts 統一存放在 \`openspec/changes/{change-id}/\`` is immediately followed by a sentence stating that `progress.md` is the cross-session resume anchor written by SDD/TDD/verification AND no existing rows are removed (table grows from 9 to 10 rows)
  - Depends on: 3.1
  - Independence: parallel-safe (with 5.1, 5.2)
  - status: passing
  - evidence: README skill table now contains `resume` as first row and documents `progress.md`

## Optional artifacts

- [ ] PlantUML diagrams (spec-driven-dev:writing-uml)
- [ ] Figma designs (spec-driven-dev:writing-figma)
