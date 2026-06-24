---
name: prd
description: Use after brainstorming to produce a Product Requirements Document before writing implementation plans. Triggers on invocation by brainstorming or direct /prd call. Writes prd.md to openspec/changes/{change-id}/prd.md.
user-invocable: true
---

# PRD Generator

Produce a structured Product Requirements Document from an approved design, then hand off to the next step in the spec-driven-dev pipeline.

<HARD-GATE>
Do NOT start writing implementation plans, invoking writing-plans, or touching any code until prd.md is approved by the user.

**Language policy (read carefully — most output bugs come from violating this):**

- `conversation_language` = the language the user wrote their first message in (or the language of design.md's frontmatter if this skill was invoked mid-pipeline). ALL user-facing prose (questions, prompts, transitions, error messages) MUST be rendered in this language. The user can switch by saying `lang:en`, `lang:zh-TW`, etc., or simply by writing in a different language — update `conversation_language` accordingly.
- `doc_language` = the language used inside prd.md body prose. Read it from `openspec/changes/{change-id}/design.md` frontmatter. If design.md has no `doc_language`, default to `conversation_language`. Do NOT default to a fixed language; never override the value from design.md.
- Stay in one language per surface. Do not mix Chinese characters with untranslated English nouns ("requirement", "actor", "PRD" written inline in a Chinese sentence) unless that English token is a literal identifier (file path, code symbol, OpenSpec keyword, slash-command name like `/prd`, or a section anchor like `FR-001`). When in doubt, translate.
- Every example sentence below is for your understanding only — do NOT echo any of them verbatim. Re-render every user-facing string in the active language.
</HARD-GATE>

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Detect language** — read `doc_language` from `openspec/changes/{change-id}/design.md` frontmatter; if absent, fall back to `conversation_language`.
2. **Confirm change-id** — scan `openspec/changes/*/` for in-flight changes (has `design.md`, no `verification-report.md`). If exactly one found, use it. If multiple found, ask the user — in `conversation_language` — to choose. If none found, ask the user to specify.
2.5. **Requirements Lens** — distil a requirements-perspective summary from design.md before generating the PRD. This is an internal working artefact: do NOT write it to prd.md. It only shapes how you draft the PRD sections below.

   Produce an internal summary covering these three reframings:

   - **Identify real actors.** Keep only human roles (e.g., marketing user, system administrator). Drop any "as a system" framing or system-component subjects.
     - Example transformation: "Kafka consumer receives domain.events" → actor list shows only "marketing user"; the Kafka consumer is removed.

   - **Convert technical descriptions into capability statements.** Rewrite implementation language as observable system capability language.
     - Example transformation: "consume domain.events via Kafka" → "the system responds to user behaviour events in real time".

   - **Map to business outcomes.** State the business value each functional area delivers, not the technical implementation.
     - Example transformation: "implement a Redis cache layer to reduce DB queries" → "users experience smooth, immediate feedback with no perceived wait".

   The examples above are in English to illustrate the principle. When you produce the actual internal summary, write it in `doc_language` (since it feeds directly into PRD section drafting).
3. **Ask clarifying questions** — 3–5 questions with lettered options (A/B/C/D); user may reply `1A 2C 3B`. Focus on: Problem, Core Functionality, Scope, Success Criteria. Skip questions already answered in design.md. Render the questions in `conversation_language`.
4. **Generate PRD** — produce the full PRD using the structure below; write to `openspec/changes/{change-id}/prd.md`.
5. **User review gate** — ask the user, in `conversation_language`, whether any section needs changes. Wait for confirmation before continuing.
6. **Commit** — after user approval:
   ```
   git add openspec/changes/{change-id}/prd.md
   git commit -m "docs: add PRD for {change-id}"
   ```
7. **Transition** — prompt the user, in `conversation_language`, to choose the next step from these three options (keep the skill identifiers verbatim because they are command names):
   - `spec-driven-dev:writing-plans` — create the implementation task list
   - `spec-driven-dev:writing-figma` — produce Figma designs first
   - `spec-driven-dev:writing-uml` — produce PlantUML diagrams first

   Invoke the chosen `spec-driven-dev:*` skill.

## Clarifying Questions Format

Ask questions in this shape, rendered in `conversation_language`. The English wording below is illustrative — re-render it in the active language; do not paste it as-is.

```
1. What is the primary problem this feature solves?
   A. [Option A]
   B. [Option B]
   C. [Option C]
   D. Other: [please specify]

2. Who are the primary target users?
   A. End users (non-technical)
   B. Internal team / admin users
   C. Developers / API consumers
   D. All of the above

3. What is the intended scope?
   A. Minimal viable version
   B. Full-featured implementation
   C. Backend / API only
   D. Frontend / UI only
```

Users may answer `1A 2B 3C` for speed.

## PRD Document Structure

```markdown
---
change_id: {change-id}
doc_language: {doc_language}
---

# PRD: {Feature Name}

## 1. Introduction

### Background
{Context and motivation for this feature}

### Problem Statement
{The specific problem being solved}

### Target Users
{Who will use this feature and in what context}

## 2. Goals
- {Measurable objective 1}
- {Measurable objective 2}

## 3. Non-Goals
- {Explicitly excluded capability 1}
- {Explicitly excluded capability 2}

## 4. User Stories

### US-001: {Title}
**Description:** As a {user}, I want {feature} so that {benefit}.

**Acceptance Criteria:**
- [ ] {Specific, verifiable criterion}
- [ ] {Another criterion}

### US-002: {Title}
...

## 5. Functional Requirements
- FR-001: {Specific system behavior — use "must" or "shall"}
- FR-002: ...

## 6. Non-Functional Requirements *(optional — omit if not applicable)*
- NFR-001: {Performance / security / availability / data consistency requirement}

## 7. Technical Considerations *(optional — omit if not applicable)*
- {Known constraints, dependencies, or integration points — no implementation detail}

## 8. Metrics
- {How success will be measured and tracked}

## 9. Open Questions
- {Unresolved questions that need follow-up}
```

**Writing rules:**

Write all prd.md prose in `doc_language`. The Bad/Good examples below are illustrative — apply the same principle in `doc_language`, not by copying the example wording.

- Acceptance criteria must be verifiable. "Works correctly" is bad. "Clicking Delete shows a confirmation dialog" is good.
- FR entries must be unambiguous — number them for easy reference.
- NFR and Technical Considerations are optional; omit entire sections for small features rather than leaving them empty.
- Goals must be measurable where possible ("reduce X by 50%", not "improve X").
- Non-Goals are as important as Goals — make scope boundaries explicit.
- **Rule 1 — Acceptance Criteria: user-observable only.** Every AC must describe behaviour or outcomes observable by a user or business stakeholder. Prohibited: class names, API field names, topic names, state-machine enum values, third-party component names (e.g., ShedLock, Kafka, circuit breaker).
  - Bad: `Create a campaign with type=DISCOUNT via REST API, carrying ruleConfig and targetSpec`
  - Good: `A marketing user can create a campaign that includes discount rules and specify the target audience and reach plan`
- **Rule 2 — Functional Requirements: capability, not implementation.** FR entries describe what the system must be able to do, not how it does it. No architecture terms, component names, or data-schema references.
  - Bad: `FR-008: reach.orchestrator must be the sole consumer of the reach.requested topic`
  - Good: `FR-008: The system must ensure that reach requests for the same campaign are not executed more than once`
- **Rule 3 — Technical Considerations (Section 7): scope constraints only.** Section 7 may only contain constraints that limit the requirements scope (e.g., "this iteration delivers only the backend API; no admin UI"). Do not reproduce architecture decisions from design.md. If no such constraints exist, omit the section entirely.

## Transition Handoff

After the user approves prd.md and the commit is done, prompt the user to choose:
- `spec-driven-dev:writing-plans` — if ready to write implementation tasks
- `spec-driven-dev:writing-figma` — if Figma designs are needed first
- `spec-driven-dev:writing-uml` — if PlantUML diagrams are needed first

Invoke only `spec-driven-dev:*` versions. Do NOT invoke `superpowers:writing-plans` or `ralph-skills:prd`.
