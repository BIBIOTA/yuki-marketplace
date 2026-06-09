---
name: prd
description: Use after brainstorming to produce a Product Requirements Document before writing implementation plans. Triggers on invocation by brainstorming or direct /prd call. Writes prd.md to openspec/changes/{change-id}/prd.md.
user-invocable: true
---

# PRD Generator

Produce a structured Product Requirements Document from an approved design, then hand off to the next step in the spec-driven-dev pipeline.

<HARD-GATE>
Do NOT start writing implementation plans, invoking writing-plans, or touching any code until prd.md is approved by the user.

**Language:** All user-facing replies MUST use the user's input language. The user can switch language at any time by saying `lang:en`, `lang:zh-TW`, or simply writing in a different language. Default is Traditional Chinese (繁體中文).

**Document language:** The body prose of prd.md MUST be written in the same `doc_language` as the current change's design.md. If design.md has no `doc_language` frontmatter, use the user's conversation language.
</HARD-GATE>

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Detect language** — read `doc_language` from `openspec/changes/{change-id}/design.md` frontmatter; fall back to user's conversation language.
2. **Confirm change-id** — scan `openspec/changes/*/` for in-flight changes (has `design.md`, no `verification-report.md`). If exactly one found, use it. If multiple found, ask the user to choose. If none found, ask the user to specify.
3. **Ask clarifying questions** — 3–5 questions with lettered options (A/B/C/D); user may reply `1A 2C 3B`. Focus on: Problem, Core Functionality, Scope, Success Criteria. Skip questions already answered in design.md.
4. **Generate PRD** — produce the full PRD using the structure below; write to `openspec/changes/{change-id}/prd.md`.
5. **User review gate** — ask the user whether any section needs changes. Wait for confirmation before continuing.
6. **Commit** — after user approval:
   ```
   git add openspec/changes/{change-id}/prd.md
   git commit -m "docs: add PRD for {change-id}"
   ```
7. **Transition** — prompt the user to choose the next step:
   > "PRD committed. What's next?"
   > 1. `writing-plans` — create implementation task list
   > 2. `writing-figma` — produce Figma designs first
   > 3. `writing-uml` — produce PlantUML diagrams first

   Invoke the chosen `spec-driven-dev:*` skill.

## Clarifying Questions Format

Ask questions in this format (adapt language to `doc_language`):

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
- Acceptance criteria must be verifiable. "Works correctly" is bad. "Clicking Delete shows a confirmation dialog" is good.
- FR entries must be unambiguous — number them for easy reference.
- NFR and Technical Considerations are optional; omit entire sections for small features rather than leaving them empty.
- Goals must be measurable where possible ("reduce X by 50%", not "improve X").
- Non-Goals are as important as Goals — make scope boundaries explicit.

## Transition Handoff

After the user approves prd.md and the commit is done, prompt the user to choose:
- `spec-driven-dev:writing-plans` — if ready to write implementation tasks
- `spec-driven-dev:writing-figma` — if Figma designs are needed first
- `spec-driven-dev:writing-uml` — if PlantUML diagrams are needed first

Invoke only `spec-driven-dev:*` versions. Do NOT invoke `superpowers:writing-plans` or `ralph-skills:prd`.
