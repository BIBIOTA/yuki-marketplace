---
name: writing-figma
description: Use when tasks.md marks Figma designs as required - thin orchestrator over the official figma:* skills (figma-generate-design, figma-generate-library, figma-use, figma-code-connect). Enforces three mandatory design considerations (version variants, state coverage, shared component reuse), downloads screenshots, and writes openspec/changes/{change-id}/designs/figma.md with acceptance criteria for downstream verification.
---

# Writing Figma Designs

Orchestrate the official figma:* skills to produce committed design assets, then hand off to writing-spec.

<HARD-GATE>
User must approve `openspec/changes/{change-id}/designs/figma.md` before invoking `spec-driven-dev:writing-spec`.

**Language:** All user-facing replies in this skill MUST use the user's input language; internal template strings (file paths, code blocks, Figma node IDs) stay in English. Reuse the language detected in design.md frontmatter or the first user message.
</HARD-GATE>

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Detect language** — reuse from design.md frontmatter or the user's first message. Lock for the conversation.
2. **Read** `openspec/changes/{change-id}/design.md` and `openspec/changes/{change-id}/tasks.md` completely.
3. **Frontend project precheck** — check for any of these files in the project root. If NONE are present, prompt the user to confirm Figma is still needed before continuing:
   - `package.json`
   - `next.config.{js,ts,mjs}`
   - `vite.config.{js,ts}`
   - `app/`
   - `pages/`
   - `src/components/`
4. **Figma plugin precheck** — check whether the `figma:figma-use` skill is available (it appears in the system-reminder skills list). If it is NOT available, abort with:
   > "Install the official figma plugin: `/plugin marketplace add anthropics/claude-plugins` then `/plugin install figma`."
5. **Three mandatory questions** — ask each question in turn. Record the answers. None may be skipped.
   a. **Versions**: "Do you need 1 variant or multiple A/B/C variants? Multi-variant designs fit UX exploration and stakeholder comparison; single-variant is appropriate when the UX is already settled."
   b. **States** (multi-select — present all options; user may choose any combination):
      - Empty state
      - Loading state
      - Error state
      - Disabled / read-only state
      - Authenticated vs unauthenticated
      - Other (specify)
   c. **Shared components**: "Which UI elements should be design-system primitives? For each, indicate `existing` (reuse from the library) or `new` (create and add to the library this change)."
6. **Decide delegation** — based on the task type and user answers, invoke exactly one figma:* skill:
   - New screen / page / modal → invoke `figma:figma-generate-design`
   - New design system / component library → invoke `figma:figma-generate-library`
   - Edit existing Figma file / programmatic operations → invoke `figma:figma-use`
   - Code Connect component mapping → invoke `figma:figma-code-connect`
7. **Generate designs** — delegate to the chosen figma:* skill. Iterate with the user (revise → preview → approve) until designs are approved.
8. **Download screenshots** via `figma:figma__get_screenshot` MCP tool. Save each file to:
   `openspec/changes/{change-id}/designs/screenshots/{NN}-{state}.png`
   (e.g., `01-happy.png`, `02-empty.png`, `03-error.png`)
9. **Write `openspec/changes/{change-id}/designs/figma.md`** using the template in the [figma.md Template](#figmamd-template) section below.
10. **Update `design.md`**: append a `## Designs` section linking to `./designs/figma.md`. Example:
    ```
    ## Designs
    - [Figma Designs](./designs/figma.md) — frames and acceptance criteria for {change-id}
    ```
11. **Self-review** — run the four checks in the [Spec Self-Review](#spec-self-review) section. Fix inline.
12. **Commit**:
    ```bash
    git add openspec/changes/{change-id}/designs/ openspec/changes/{change-id}/design.md
    git commit -m "docs: add Figma designs for {change-id}"
    ```
13. **Transition**: invoke `spec-driven-dev:writing-spec`.

## Process Flow

```dot
digraph writing_figma {
    rankdir=TB;

    "Detect language" [shape=box];
    "Read design.md + tasks.md" [shape=box];
    "Frontend project precheck" [shape=box];
    "Figma plugin precheck" [shape=box];
    "Three mandatory questions\n(versions / states / shared components)" [shape=box];
    "Decide delegation\n(generate-design / generate-library / use / code-connect)" [shape=box];
    "Generate designs via figma:* skill" [shape=box];
    "User approves designs?" [shape=diamond];
    "Download screenshots" [shape=box];
    "Write designs/figma.md" [shape=box];
    "Update design.md (## Designs)" [shape=box];
    "Self-review" [shape=box];
    "Commit" [shape=box];
    "Invoke spec-driven-dev:writing-spec" [shape=doublecircle];

    "Detect language" -> "Read design.md + tasks.md";
    "Read design.md + tasks.md" -> "Frontend project precheck";
    "Frontend project precheck" -> "Figma plugin precheck";
    "Figma plugin precheck" -> "Three mandatory questions\n(versions / states / shared components)";
    "Three mandatory questions\n(versions / states / shared components)" -> "Decide delegation\n(generate-design / generate-library / use / code-connect)";
    "Decide delegation\n(generate-design / generate-library / use / code-connect)" -> "Generate designs via figma:* skill";
    "Generate designs via figma:* skill" -> "User approves designs?";
    "User approves designs?" -> "Generate designs via figma:* skill" [label="no, revise"];
    "User approves designs?" -> "Download screenshots" [label="yes"];
    "Download screenshots" -> "Write designs/figma.md";
    "Write designs/figma.md" -> "Update design.md (## Designs)";
    "Update design.md (## Designs)" -> "Self-review";
    "Self-review" -> "Commit";
    "Commit" -> "Invoke spec-driven-dev:writing-spec";
}
```

## figma.md Template

Use this template verbatim when writing `openspec/changes/{change-id}/designs/figma.md`:

````markdown
# Figma Designs: {change-id}

## Figma File
- File: https://www.figma.com/design/{fileKey}/...
- File key: {fileKey}

## Versions
- [v1] Frame node: {nodeId} — description
- [v2] Frame node: {nodeId} — description

## States
| State | Frame node | Screenshot |
|---|---|---|
| Happy path | {nodeId} | screenshots/01-happy.png |
| Empty | {nodeId} | screenshots/02-empty.png |
| Error | {nodeId} | screenshots/03-error.png |

## Shared Components Used
- `Button/Primary` (existing) — reused from design system
- `Card/Compact` (new) — added to design system this change

## Acceptance Criteria
- Implementation screens must match v1 frame {nodeId}.
- Empty / Error states must match their respective frames.
````

## Spec Self-Review

After writing `figma.md`, apply these four checks. Fix any issues inline — no re-review needed after fixing.

1. **Placeholder scan:** Any `{nodeId}`, `{fileKey}`, or `{change-id}` placeholders left unfilled? Fix.
2. **Consistency check:** Do the States table rows match the states selected in step 5b? Do screenshot filenames match files actually downloaded? Fix.
3. **Scope check:** Are all frames scoped to the current change-id? Remove anything belonging to a different change. Fix.
4. **Ambiguity check:** Could any acceptance criterion be interpreted two ways? Pick one interpretation, make it explicit. Fix.

## Transition Handoff

After the user approves `figma.md` and the commit succeeds, transition to:

- `spec-driven-dev:writing-spec` — always; this is the final artifact step before spec writing.

Invoke only the `spec-driven-dev:*` version via Skill tool. Do NOT invoke `superpowers:writing-figma` or `superpowers:writing-spec` — they are different skills with different downstream chains.
