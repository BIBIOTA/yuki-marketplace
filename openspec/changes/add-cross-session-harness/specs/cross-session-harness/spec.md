## ADDED Requirements

### Requirement: Resume skill shall detect in-flight changes and route to the correct implementation skill
The system SHALL provide a `spec-driven-dev:resume` skill that scans `openspec/changes/*/` for in-flight changes (directories where `design.md` exists but `verification-report.md` does not), reads the most recent `progress.md` entry, and invokes the implementation skill named by that entry's `Stage` field.

#### Scenario: No in-flight change found
- **WHEN** `openspec/changes/` is empty or every change directory contains `verification-report.md`
- **THEN** the resume skill reports "無 in-flight change"
- **AND** suggests `/spec-driven-dev:brainstorming` as the next action
- **AND** does not invoke any other skill

#### Scenario: Exactly one in-flight change with progress.md present
- **WHEN** exactly one directory under `openspec/changes/` has `design.md` but no `verification-report.md` and `progress.md` exists with at least one `## Session N` entry
- **THEN** the resume skill reads the last Session entry's `Stage` field
- **AND** when `Stage: SDD` invokes `spec-driven-dev:subagent-driven-development`
- **AND** when `Stage: TDD` invokes `spec-driven-dev:test-driven-development`
- **AND** when `Stage: verification` invokes `spec-driven-dev:verification-before-completion`
- **AND** prints the last entry's `Next action` value before invoking

#### Scenario: Exactly one in-flight change with no progress.md (file-presence inference)
- **WHEN** exactly one in-flight directory exists but `progress.md` is missing
- **THEN** the resume skill infers stage from artifact presence
- **AND** when only `design.md` is present invokes `spec-driven-dev:writing-plans`
- **AND** when `tasks.md` is present but `proposal.md` is not invokes `spec-driven-dev:writing-spec` (or `writing-uml`/`writing-figma` if tasks.md `Optional artifacts` section marks them)
- **AND** when `proposal.md` is present prompts the user "SDD or TDD?" and routes accordingly

#### Scenario: Multiple in-flight changes
- **WHEN** more than one in-flight directory exists under `openspec/changes/`
- **THEN** the resume skill lists each change-id with its last `Next action` line (or "(no progress.md)" if absent)
- **AND** asks the user to pick one
- **AND** after selection routes per the single-in-flight scenarios above

#### Scenario: State inconsistency aborts resume
- **WHEN** progress.md last entry says `Transition: in_progress → passing` for task X but tasks.md task X still has `status: in_progress`, OR more than one task has `status: in_progress`
- **THEN** the resume skill reports the specific conflict
- **AND** does NOT auto-fix
- **AND** does NOT invoke any downstream skill

### Requirement: Per-change progress.md shall be written on every status transition
The system SHALL append one Session entry to `openspec/changes/{change-id}/progress.md` whenever `spec-driven-dev:subagent-driven-development` or `spec-driven-dev:test-driven-development` flips a task's status. The file is append-only; entries are never edited or deleted.

#### Scenario: SDD records not_started → in_progress on task dispatch
- **WHEN** SDD dispatches an implementer subagent for task N.M (current status `not_started`)
- **THEN** SDD flips the task's `status` sub-bullet in tasks.md to `in_progress`
- **AND** appends a new `## Session K` block to `progress.md` containing `Stage: SDD`, `Task: N.M {title}`, `Transition: not_started → in_progress`, and a non-empty `Next action` line
- **AND** Session number K is `max(existing Session numbers) + 1` (or 1 if none)

#### Scenario: SDD records in_progress → passing on dual review approval
- **WHEN** both spec-reviewer and code-quality-reviewer return ✅ for task N.M
- **THEN** SDD flips the task's status to `passing` and ticks the markdown checkbox to `- [x]`
- **AND** appends a Session entry with `Transition: in_progress → passing`, the implementer's commit hash(es) and reviewer outcomes under `Evidence`, and a non-empty `Next action` line

#### Scenario: SDD records in_progress → blocked on implementer BLOCKED signal
- **WHEN** the implementer subagent returns `BLOCKED` or `NEEDS_CONTEXT` for task N.M
- **THEN** SDD flips the task's status to `blocked` (the checkbox stays `- [ ]`)
- **AND** appends a Session entry with `Transition: in_progress → blocked`, a `Blockers:` line describing the cause, and a `Next action` line stating what unblocks the task

#### Scenario: TDD records transitions across the Red-Green-Refactor cycle
- **WHEN** TDD enters the per-task loop for task N.M
- **THEN** the same three transition cases (→ in_progress on Red start; → passing after the Green commit and any Refactor commit; → blocked on pause) each append a Session entry to `progress.md` with `Stage: TDD` and matching evidence (test output excerpt for transitions involving Red/Green; commit hashes for Green and Refactor)

### Requirement: tasks.md shall enforce a 4-state machine and single-in-progress invariant
The system SHALL extend the `tasks.md` template so every task carries a `status` sub-bullet drawn from `{not_started, in_progress, passing, blocked}`, and any session invoking SDD or TDD SHALL assert that at most one task in the active change has `status: in_progress`.

#### Scenario: writing-plans emits status: not_started for every new task
- **WHEN** `spec-driven-dev:writing-plans` writes a new `tasks.md`
- **THEN** every task entry in the file includes `- status: not_started` as a sub-bullet
- **AND** the SKILL.md documents the allowed transitions (`not_started → in_progress`, `in_progress → passing`, `in_progress → blocked`, `blocked → in_progress`) and the forbidden ones (any → `not_started`; `passing` → any)

#### Scenario: SDD aborts when tasks.md has multiple in-progress tasks
- **WHEN** `spec-driven-dev:subagent-driven-development` reads tasks.md at entry and finds two or more tasks with `status: in_progress`
- **THEN** SDD aborts immediately and lists the conflicting task ids
- **AND** does not flip any status or dispatch any implementer
- **AND** instructs the user to manually resolve the invariant violation before retrying

#### Scenario: TDD aborts when tasks.md has multiple in-progress tasks
- **WHEN** `spec-driven-dev:test-driven-development` reads tasks.md at entry and finds two or more tasks with `status: in_progress`
- **THEN** TDD aborts immediately with the same conflict listing and user guidance as SDD

#### Scenario: Status transition outside the state machine is rejected
- **WHEN** SDD or TDD is asked (by the resume skill or by an existing progress.md state) to flip a task directly from `passing` to any other state, or to flip any state back to `not_started`
- **THEN** the operation is rejected and the offending transition is reported

### Requirement: Entry-point skills shall run an in-flight precheck before starting new work
The `spec-driven-dev:brainstorming`, `spec-driven-dev:writing-plans`, and `spec-driven-dev:writing-spec` skills SHALL scan `openspec/changes/*/` at the top of their Checklists and offer to resume any in-flight change before continuing.

#### Scenario: brainstorming detects an in-flight change and offers resume
- **WHEN** the user invokes `spec-driven-dev:brainstorming` and `openspec/changes/` contains at least one in-flight directory
- **THEN** brainstorming pauses before its existing step 2 (Explore project context)
- **AND** prompts the user verbatim: "偵測到 in-flight change `{change-id}`，要 resume 還是開新？"
- **AND** on "resume" invokes `spec-driven-dev:resume`
- **AND** on "新" prints a warning that the in-flight change's progress is preserved but this session switches to a new change, then proceeds with the normal brainstorming flow

#### Scenario: writing-plans detects an in-flight change and offers resume
- **WHEN** the user invokes `spec-driven-dev:writing-plans` and `openspec/changes/` contains at least one in-flight directory other than the one matching its own argument
- **THEN** writing-plans applies the same prompt and routing as the brainstorming scenario above

#### Scenario: writing-spec detects an in-flight change and offers resume
- **WHEN** the user invokes `spec-driven-dev:writing-spec` and an in-flight directory exists for a change-id that does not match the spec being written
- **THEN** writing-spec applies the same prompt and routing as the brainstorming scenario above

### Requirement: Verification stage 2 shall gate on a non-empty progress log
The `spec-driven-dev:verification-before-completion` skill SHALL fail Stage 2 if `openspec/changes/{change-id}/progress.md` is missing, or if the file's last `## Session N` block lacks a non-empty `- Next action:` line.

#### Scenario: progress.md missing fails Stage 2
- **WHEN** verification runs Stage 2 for a change whose `openspec/changes/{change-id}/progress.md` does not exist
- **THEN** Stage 2 is marked FAIL with reason "progress.md missing"
- **AND** the verification-report.md `## Summary` adds a `Progress log: FAIL` line
- **AND** verification asks the user which implementation skill to re-invoke (SDD or TDD) and routes accordingly, matching the existing Stage 1 failure routing pattern

#### Scenario: progress.md last entry lacks Next action fails Stage 2
- **WHEN** progress.md exists but its last `## Session N` block has no `- Next action:` line or that line is empty
- **THEN** Stage 2 is marked FAIL with reason "progress.md last entry has empty Next action"
- **AND** the verification-report.md `## Summary` adds a `Progress log: FAIL` line

#### Scenario: progress.md complete passes Stage 2 progress-log check
- **WHEN** progress.md exists and its last `## Session N` block contains a non-empty `- Next action:` line
- **THEN** Stage 2 records `Progress log: PASS` and proceeds to the next Stage 2 check (`openspec validate --strict`)

### Requirement: Resume skill shall be registered in both plugin manifests and documented in README
The `spec-driven-dev` plugin manifests SHALL list `./skills/resume` so the skill is discoverable through both Claude Code and Codex, and the repo-level `README.md` SHALL list it in the spec-driven-dev skill table.

#### Scenario: Claude plugin manifest lists resume
- **WHEN** a reader opens `plugins/spec-driven-dev/.claude-plugin/plugin.json`
- **THEN** the `skills` array contains `./skills/resume`
- **AND** the JSON parses without error

#### Scenario: Codex plugin manifest lists resume at the matching version
- **WHEN** a reader opens `plugins/spec-driven-dev/.codex-plugin/plugin.json`
- **THEN** the `skills` array contains `./skills/resume`
- **AND** the `version` field equals the `version` field in `.claude-plugin/plugin.json`
- **AND** the JSON parses without error

#### Scenario: README skill table includes resume as the entry-point row
- **WHEN** a reader opens `README.md` at the `## Plugin: spec-driven-dev` section
- **THEN** the `### Skills` table contains a row whose first column is `resume` and whose second column describes its session-entry role
- **AND** the `resume` row is the first data row in the table (before `brainstorming`)
- **AND** the sentence introducing `Artifacts 統一存放在 openspec/changes/{change-id}/` is followed by a sentence that names `progress.md` as the cross-session resume anchor
