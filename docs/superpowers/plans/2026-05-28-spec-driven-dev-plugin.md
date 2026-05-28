# spec-driven-dev Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a Claude Code plugin `spec-driven-dev` with 8 skills implementing the chain brainstorming → writing-plans → (writing-uml?) → (writing-figma?) → writing-spec → SDD|TDD → verification-before-completion, per the approved spec.

**Architecture:** Plugin lives in `plugins/spec-driven-dev/`. `plugin.json` registers 8 skills. Each skill is a `SKILL.md` with YAML frontmatter. SDD bundles 3 subagent prompt files. Two skills (writing-uml, writing-spec) have supporting reference markdown. All skills produce/consume `openspec/changes/{change-id}/` as common data layer.

**Tech Stack:** Markdown (skill files), JSON (manifests), YAML (frontmatter), bash + Python (frontmatter validation), Node.js (OpenSpec CLI for smoke test).

**Spec (locked, approved):** [`docs/superpowers/specs/2026-05-28-spec-driven-dev-plugin-design.md`](../specs/2026-05-28-spec-driven-dev-plugin-design.md)

**Branch:** `feat/spec-driven-dev` (per project git convention: `feat:` prefix, PR target `master`)

---

## File Structure

Files to create:

```
plugins/spec-driven-dev/
├── .claude-plugin/plugin.json
└── skills/
    ├── brainstorming/SKILL.md
    ├── writing-plans/SKILL.md
    ├── writing-uml/SKILL.md
    ├── writing-uml/diagram-types.md
    ├── writing-figma/SKILL.md
    ├── writing-spec/SKILL.md
    ├── writing-spec/openspec-format.md
    ├── subagent-driven-development/SKILL.md
    ├── subagent-driven-development/implementer-prompt.md
    ├── subagent-driven-development/spec-reviewer-prompt.md
    ├── subagent-driven-development/code-quality-reviewer-prompt.md
    ├── test-driven-development/SKILL.md
    └── verification-before-completion/SKILL.md
```

Files to modify:

- `.claude-plugin/marketplace.json` — register the new plugin

Validation script (created once in Task 1, reused throughout):

- `scripts/validate-skill-frontmatter.py`

---

## Task 0: Branch + Validation Script

**Files:**
- Create: `scripts/validate-skill-frontmatter.py`

- [ ] **Step 1: Create feature branch**

```bash
git checkout -b feat/spec-driven-dev
```

Expected: `Switched to a new branch 'feat/spec-driven-dev'`

- [ ] **Step 2: Create the validation script**

```python
# scripts/validate-skill-frontmatter.py
import sys
import yaml
from pathlib import Path

REQUIRED = {"name", "description"}

def validate(path: Path) -> list[str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return [f"{path}: missing opening '---' frontmatter delimiter"]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [f"{path}: missing closing '---' frontmatter delimiter"]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [f"{path}: invalid YAML: {e}"]
    if not isinstance(fm, dict):
        return [f"{path}: frontmatter is not a mapping"]
    missing = REQUIRED - fm.keys()
    if missing:
        return [f"{path}: missing required keys: {sorted(missing)}"]
    expected_name = path.parent.name
    if fm["name"] != expected_name:
        return [f"{path}: frontmatter name '{fm['name']}' != directory name '{expected_name}'"]
    return []

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-skill-frontmatter.py <SKILL.md> [<SKILL.md>...]")
        return 2
    errors = []
    for arg in sys.argv[1:]:
        errors.extend(validate(Path(arg)))
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"OK: {len(sys.argv) - 1} skill file(s) validated")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Verify script runs (no input → usage error)**

Run: `python scripts/validate-skill-frontmatter.py`
Expected: exit code 2, prints usage line.

- [ ] **Step 4: Verify script catches an existing valid skill**

Run: `python scripts/validate-skill-frontmatter.py plugins/yuki-toolkit/skills/gws-reference/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 5: Commit**

```bash
git add scripts/validate-skill-frontmatter.py
git commit -m "chore: add skill frontmatter validation script"
```

---

## Task 1: Plugin Scaffold

**Files:**
- Create: `plugins/spec-driven-dev/.claude-plugin/plugin.json`
- Create: `plugins/spec-driven-dev/skills/` (empty subfolders)

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p plugins/spec-driven-dev/.claude-plugin
mkdir -p plugins/spec-driven-dev/skills/{brainstorming,writing-plans,writing-uml,writing-figma,writing-spec,subagent-driven-development,test-driven-development,verification-before-completion}
```

Verify: `find plugins/spec-driven-dev -type d | sort`
Expected: 10 directories listed (plugin root, `.claude-plugin`, `skills`, plus 8 skill folders).

- [ ] **Step 2: Write `plugin.json`**

```json
{
  "name": "spec-driven-dev",
  "description": "Spec-driven development pipeline: brainstorming → plans → (UML/Figma) → OpenSpec → SDD/TDD → verification. Each step gated by user review; artifacts converge in openspec/changes/{change-id}/.",
  "version": "0.1.0",
  "author": {
    "name": "BIBIOTA"
  },
  "keywords": [
    "spec-driven",
    "openspec",
    "tdd",
    "sdd",
    "plantuml",
    "figma",
    "brainstorming",
    "planning"
  ],
  "skills": [
    "./skills/brainstorming/SKILL.md",
    "./skills/writing-plans/SKILL.md",
    "./skills/writing-uml/SKILL.md",
    "./skills/writing-figma/SKILL.md",
    "./skills/writing-spec/SKILL.md",
    "./skills/subagent-driven-development/SKILL.md",
    "./skills/test-driven-development/SKILL.md",
    "./skills/verification-before-completion/SKILL.md"
  ]
}
```

- [ ] **Step 3: Validate JSON parses**

Run: `python -c "import json; json.load(open('plugins/spec-driven-dev/.claude-plugin/plugin.json'))"`
Expected: no output, exit 0.

- [ ] **Step 4: Commit**

```bash
git add plugins/spec-driven-dev/
git commit -m "feat: scaffold spec-driven-dev plugin"
```

> **Reminder:** Do NOT manually bump `version` after this point — CI handles it on merge to master.

---

## Task 2: brainstorming SKILL.md

**Spec reference:** § Skill 1 (brainstorming) of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter (exact):

```yaml
---
name: brainstorming
description: Use when starting any new feature, change, or idea before writing code or invoking any implementation skill - detects user language, explores project context, asks one clarifying question at a time, proposes 2-3 approaches, presents design in sections with user approval, and writes design.md to openspec/changes/{change-id}/. Terminal state is invoking writing-plans.
---
```

Body (per spec § Skill 1; key required sections):

- **HARD-GATE banner** (top of body): "Do NOT invoke any implementation skill, write code, or scaffold files until design.md is approved by the user."
- **Process Flow** (dot graph): from "Detect language" through "Invoke writing-plans skill", branches for visual companion and decompose-large-projects.
- **Checklist** (12 items): Detect language → Explore project context → Scope check → Decide change-id → Clarifying questions → Propose approaches → Present design in sections → Explore optional skills → Write design.md → Self-review → User review gate → Transition to writing-plans.
- **change-id rules**: kebab-case, verb+noun (`add-`, `refactor-`, `fix-`, `remove-`); skill must propose one and confirm with user.
- **Optional skills探詢 phrasing** (verbatim from spec § 1 step 8): two questions about UML and Figma needs; record outcomes in design.md as `## Probable next steps`.
- **Self-review four checks**: placeholder / consistency / scope / ambiguity.
- **User review gate text** (translatable but English template): "Spec written and committed to {path}. Please review and let me know if you want changes before we move to writing-plans."
- **Transition**: explicitly states `Invoke the writing-plans skill in this same plugin (spec-driven-dev:writing-plans).` Do NOT invoke superpowers:writing-plans.

Cross-plugin rule (verbatim near the top): "All user-facing replies in this skill MUST use the user's input language; internal template strings (file paths, code blocks, OpenSpec keywords) stay in English."

- [ ] **Step 2: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/brainstorming/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 3: Cross-reference sanity check**

Run: `grep -E "writing-plans|writing-uml|writing-figma" plugins/spec-driven-dev/skills/brainstorming/SKILL.md`
Expected: at least one match for each (transition to writing-plans,探詢 mention of writing-uml/writing-figma).

- [ ] **Step 4: Commit**

```bash
git add plugins/spec-driven-dev/skills/brainstorming/SKILL.md
git commit -m "feat: add brainstorming skill"
```

---

## Task 3: writing-plans SKILL.md

**Spec reference:** § Skill 2 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: writing-plans
description: Use when openspec/changes/{change-id}/design.md exists and tasks must be decomposed into an OpenSpec-format tasks.md checklist - reads the approved design, breaks work into bite-sized tasks with WHEN/THEN acceptance criteria, confirms whether the change needs writing-uml and/or writing-figma, then chains to the next skill in the pipeline.
---
```

Body (per spec § Skill 2):

- HARD-GATE: "User must approve tasks.md before invoking writing-uml, writing-figma, or writing-spec."
- Language detection sentence: "Reuse the language detected in design.md frontmatter or the first user message."
- Checklist (9 items per spec).
- `tasks.md` template (verbatim from spec § Skill 2).
- **Optional artifacts confirmation block** (multi-select; phrase exactly as in spec):
  > "Does this change require any of the following artifacts before implementation? (multi-select)
  > - [ ] PlantUML diagrams (writing-uml) — fits: complex flows, state machines, cross-component interactions, ER schemas
  > - [ ] Figma designs (writing-figma) — fits: frontend UI, interactive prototypes, A/B version comparison"
- **Transition logic** (verbatim):
  ```
  if writing-uml selected → invoke spec-driven-dev:writing-uml
  elif writing-figma selected → invoke spec-driven-dev:writing-figma
  else → invoke spec-driven-dev:writing-spec
  ```
- Self-review four checks + user review gate.

- [ ] **Step 2: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/writing-plans/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 3: Verify transition logic mentions all three downstream skills**

Run: `grep -E "writing-uml|writing-figma|writing-spec" plugins/spec-driven-dev/skills/writing-plans/SKILL.md | wc -l`
Expected: at least 3.

- [ ] **Step 4: Commit**

```bash
git add plugins/spec-driven-dev/skills/writing-plans/SKILL.md
git commit -m "feat: add writing-plans skill"
```

---

## Task 4: writing-uml SKILL.md + diagram-types.md

**Spec reference:** § Skill 3 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/writing-uml/SKILL.md`
- Create: `plugins/spec-driven-dev/skills/writing-uml/diagram-types.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: writing-uml
description: Use when tasks.md marks PlantUML diagrams as required - presents a multi-select menu of 8 diagram types (sequence, class, use case, activity, state, component, ER, deployment) with usage notes, drafts each .puml under openspec/changes/{change-id}/diagrams/ with user iteration, previews via local plantuml CLI or plantuml.com URL, and updates design.md and tasks.md with reference links.
---
```

Body (per spec § Skill 3):

- HARD-GATE: "All diagrams must be user-approved before invoking the next skill."
- Checklist (7 items per spec).
- File naming rule: `{seq-no}-{type}-{topic}.puml`, e.g. `01-sequence-login-flow.puml`.
- **Preview detection** (verbatim logic):
  ```
  if `which plantuml` returns a path:
      render PNG locally with `plantuml -tpng diagrams/{file}.puml`
  else:
      generate plantuml.com encoded URL via official encoding helper
      prompt user to open the URL
  ```
- Multi-select diagram menu (verbatim from spec table; 8 rows).
- **Reference to `diagram-types.md`**: "For PlantUML syntax cheat sheets and example fragments per diagram type, see `./diagram-types.md`."
- **Transition** (verbatim):
  ```
  if tasks.md marks writing-figma → invoke spec-driven-dev:writing-figma
  else → invoke spec-driven-dev:writing-spec
  ```

- [ ] **Step 2: Write `diagram-types.md`**

One section per diagram type. Each section contains:
- Purpose (1-2 sentences, same wording as the user-facing menu)
- Minimal `@startuml ... @enduml` example (5-15 lines)
- 2-3 "fits" example use cases
- Common pitfalls (1 short bullet, e.g. "Sequence diagrams: keep participants ordered top-to-bottom on the page in the order they first appear, or arrow lines cross")

Order: sequence → class → use case → activity → state → component → ER → deployment.

- [ ] **Step 3: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/writing-uml/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 4: Confirm all 8 diagram types present in diagram-types.md**

Run: `grep -cE "^## (Sequence|Class|Use Case|Activity|State|Component|ER|Deployment)" plugins/spec-driven-dev/skills/writing-uml/diagram-types.md`
Expected: `8`

- [ ] **Step 5: Commit**

```bash
git add plugins/spec-driven-dev/skills/writing-uml/
git commit -m "feat: add writing-uml skill with 8 plantuml diagram types"
```

---

## Task 5: writing-figma SKILL.md

**Spec reference:** § Skill 4 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/writing-figma/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: writing-figma
description: Use when tasks.md marks Figma designs as required - thin orchestrator over the official figma:* skills (figma-generate-design, figma-generate-library, figma-use, figma-code-connect). Enforces three mandatory design considerations (version variants, state coverage, shared component reuse), downloads screenshots, and writes openspec/changes/{change-id}/designs/figma.md with acceptance criteria for downstream verification.
---
```

Body (per spec § Skill 4):

- HARD-GATE: "User must approve designs/figma.md before invoking writing-spec."
- **Frontend project precheck**: list of files to look for (`package.json`, `next.config.{js,ts,mjs}`, `vite.config.{js,ts}`, `app/`, `pages/`, `src/components/`). If none present, prompt user to confirm Figma is still needed.
- **Figma plugin precheck**: detect `figma:figma-use` skill availability; abort with install instructions if absent.
- **Three mandatory questions** (verbatim from spec):
  1. Versions: "1 variant or multiple A/B/C variants?"
  2. States (multi-select): Empty / Loading / Error / Disabled / Auth-state / Other
  3. Shared Components: list which UI elements should be design-system primitives (new vs reused).
- **Delegation matrix** (verbatim):
  - new screen/page/modal → `figma:figma-generate-design`
  - design system / component library → `figma:figma-generate-library`
  - edit existing file / programmatic ops → `figma:figma-use`
  - Code Connect mapping → `figma:figma-code-connect`
- `designs/figma.md` template (verbatim from spec § Skill 4).
- Screenshots saved to `openspec/changes/{change-id}/designs/screenshots/{NN}-{state}.png`.
- **Transition** (single path): "→ invoke spec-driven-dev:writing-spec".

- [ ] **Step 2: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/writing-figma/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 3: Confirm delegation matrix includes all four figma skills**

Run: `grep -E "figma:figma-(generate-design|generate-library|use|code-connect)" plugins/spec-driven-dev/skills/writing-figma/SKILL.md | wc -l`
Expected: at least 4.

- [ ] **Step 4: Commit**

```bash
git add plugins/spec-driven-dev/skills/writing-figma/SKILL.md
git commit -m "feat: add writing-figma orchestrator skill"
```

---

## Task 6: writing-spec SKILL.md + openspec-format.md

**Spec reference:** § Skill 5 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/writing-spec/SKILL.md`
- Create: `plugins/spec-driven-dev/skills/writing-spec/openspec-format.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: writing-spec
description: Use when design.md, tasks.md, and any UML/Figma artifacts exist in openspec/changes/{change-id}/ - produces OpenSpec-compliant proposal.md and one or more specs/{capability}/spec.md using ADDED/MODIFIED/REMOVED Requirements with WHEN/THEN Scenarios; mandates that every diagram and design artifact be referenced via '> See: ...' from at least one requirement; validates with `openspec validate --strict`.
---
```

Body (per spec § Skill 5):

- HARD-GATE (three rules verbatim from spec): every artifact must be referenced; `openspec validate --strict` must pass; user must approve.
- **OpenSpec CLI precheck**: `which openspec` and `test -d openspec/`; instructions to install (`npm i -g @fission-ai/openspec`) and run `openspec init` if missing.
- Checklist (10 items per spec).
- proposal.md template (verbatim).
- spec.md ADDED Requirement template with `> See:` references (verbatim).
- **Capability identification heuristics**: derive from design.md's top-level sections; one capability per cohesive domain; fall back to single capability named after change-id with `-cap` suffix if unclear.
- **Reference enforcement check** (pseudocode):
  ```
  artifacts = list(diagrams/*.puml) + (designs/figma.md exists ? ["designs/figma.md"] : [])
  references = grep "> See:" across specs/*/spec.md
  for artifact in artifacts:
      assert any(artifact in ref for ref in references), f"unreferenced artifact: {artifact}"
  ```
- **Transition**: ask user "SDD or TDD?" → invoke `spec-driven-dev:subagent-driven-development` or `spec-driven-dev:test-driven-development`.

- [ ] **Step 2: Write `openspec-format.md`**

Sections:
1. OpenSpec project layout (`openspec/project.md`, `openspec/specs/`, `openspec/changes/`).
2. Change anatomy (proposal.md, tasks.md, design.md, specs/, optional folders).
3. Requirement delta syntax: `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements` with examples.
4. Scenario syntax: `#### Scenario: <name>` followed by `- **WHEN** ... - **THEN** ... - **AND** ...`.
5. `> See:` reference convention.
6. `openspec validate --strict` common errors and fixes (missing Why, missing Scenarios, duplicate requirement names, broken capability paths).
7. `openspec archive {change-id}` workflow after merge.

- [ ] **Step 3: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/writing-spec/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 4: Confirm openspec-format.md covers all required sections**

Run: `grep -cE "^## " plugins/spec-driven-dev/skills/writing-spec/openspec-format.md`
Expected: `7`

- [ ] **Step 5: Commit**

```bash
git add plugins/spec-driven-dev/skills/writing-spec/
git commit -m "feat: add writing-spec skill with openspec format reference"
```

---

## Task 7: subagent-driven-development SKILL.md + prompts

**Spec reference:** § Skill 6 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md`
- Create: `plugins/spec-driven-dev/skills/subagent-driven-development/implementer-prompt.md`
- Create: `plugins/spec-driven-dev/skills/subagent-driven-development/spec-reviewer-prompt.md`
- Create: `plugins/spec-driven-dev/skills/subagent-driven-development/code-quality-reviewer-prompt.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: subagent-driven-development
description: Use when spec is approved and implementation should run with multi-subagent dispatch - reads openspec/changes/{change-id}/ (tasks.md, specs/, diagrams/, designs/) and assigns one implementer subagent per independent task, followed by spec-reviewer and code-quality-reviewer subagents that verify the work against the OpenSpec scenarios plus referenced UML diagrams and Figma designs.
---
```

Body (per spec § Skill 6):

- HARD-GATE: "Every task must pass both spec-reviewer AND code-quality-reviewer before being marked complete in tasks.md."
- Checklist (7 items per spec).
- **Subagent context bundle template** (verbatim):
  ```
  - task description (from tasks.md item N.M)
  - acceptance criteria (WHEN/THEN from spec.md)
  - referenced spec requirement excerpt
  - referenced diagrams (full .puml content embedded)
  - referenced design section (from designs/figma.md plus screenshot paths)
  ```
- Three prompt files referenced via relative path: `./implementer-prompt.md`, `./spec-reviewer-prompt.md`, `./code-quality-reviewer-prompt.md`.
- **Transition**: "→ invoke spec-driven-dev:verification-before-completion".

- [ ] **Step 2: Write `implementer-prompt.md`**

Sections:
- Role: "You are an implementer subagent. Your job: complete one task from tasks.md."
- Inputs: enumerate what is passed (task, spec excerpt, diagrams, designs).
- **Diagram contract rule** (verbatim from spec § Skill 6):
  > "If your task references a diagram via `> See: ../../diagrams/*.puml`, read the diagram first. Its message order or state transitions are the contract — your implementation must match."
- **Design contract rule** (verbatim):
  > "If your task references a Figma design via `> See: ../../designs/figma.md#...`, read that section and its screenshots before coding. Visual layout must be pixel-aware aligned to the referenced frame."
- Output: code diff, test diff, and a 3-bullet rationale.

- [ ] **Step 3: Write `spec-reviewer-prompt.md`**

Sections:
- Role: "You are a spec-reviewer subagent. Verify that the implementation matches the OpenSpec scenario AND any referenced diagram/design contracts."
- Checks:
  1. Every `#### Scenario:` in the cited requirement has a matching test case.
  2. Each referenced diagram's contract (message order, state transitions, schema) is reflected in the code.
  3. Each referenced design state (happy/empty/error/etc.) is implemented.
- Output: pass / fail per check + actionable feedback per failure.

- [ ] **Step 4: Write `code-quality-reviewer-prompt.md`**

Sections:
- Role: "You are a code-quality-reviewer subagent. Independent of spec compliance, assess the code on quality."
- Checks: DRY, YAGNI, naming, error handling at trust boundaries (per CLAUDE.md / system prompt rules), no unnecessary comments, no backwards-compat hacks, tests are focused (one assertion concept per test).
- Output: pass / fail + non-blocking suggestions vs blocking issues.

- [ ] **Step 5: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 6: Confirm all 3 prompt files exist and are non-empty**

Run: `for f in implementer-prompt.md spec-reviewer-prompt.md code-quality-reviewer-prompt.md; do test -s plugins/spec-driven-dev/skills/subagent-driven-development/$f && echo "OK $f" || echo "MISSING $f"; done`
Expected: 3 lines `OK ...`.

- [ ] **Step 7: Commit**

```bash
git add plugins/spec-driven-dev/skills/subagent-driven-development/
git commit -m "feat: add subagent-driven-development skill with three reviewer prompts"
```

---

## Task 8: test-driven-development SKILL.md

**Spec reference:** § Skill 7 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/test-driven-development/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: test-driven-development
description: Use when spec is approved and implementation should follow Red-Green-Refactor cycles - reads openspec/changes/{change-id}/ and for each task converts the cited '#### Scenario:' entries into failing tests with names matching scenario names (for traceability), then drives minimal implementation, then refactors. Marks visual/e2e checks for Figma-referenced tasks as deferred to verification-before-completion.
---
```

Body (per spec § Skill 7):

- HARD-GATE: "Each task must show a failing-test commit before any implementation commit; tasks.md item cannot be checked off without a green test commit."
- Checklist (5 items per spec).
- **Discipline rules** (verbatim):
  - No implementation before test
  - No skipping the Red phase
  - Test name MUST match `#### Scenario:` name (use the exact text in test function/case names, e.g. `test("Successful login", ...)`)
- **Diagram → integration test rule** (verbatim from spec):
  > "If a scenario references a diagram, add an integration test that asserts the runtime flow matches the diagram's message order or state transitions."
- **Design → deferred verification rule**:
  > "If a scenario references a Figma design, do NOT attempt visual assertions here. Mark the scenario as `verification-pending: design` in tasks.md and let verification-before-completion handle visual diffs."
- **Transition**: "→ invoke spec-driven-dev:verification-before-completion".

- [ ] **Step 2: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/test-driven-development/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 3: Commit**

```bash
git add plugins/spec-driven-dev/skills/test-driven-development/SKILL.md
git commit -m "feat: add test-driven-development skill"
```

---

## Task 9: verification-before-completion SKILL.md

**Spec reference:** § Skill 8 of the design doc.

**Files:**
- Create: `plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter:

```yaml
---
name: verification-before-completion
description: Use when implementation is complete and you need to verify before claiming done - runs five staged checks (code lint+tests+smoke, openspec validate --strict, diagram contract conformance, Figma design state conformance, deferred verification-pending items) and produces openspec/changes/{change-id}/verification-report.md. Any failure routes back to the originating skill; only full pass permits suggesting `openspec archive`.
---
```

Body (per spec § Skill 8):

- HARD-GATE (three rules verbatim): any stage fail → integral fail; verification-report.md must exist; archive only on full pass.
- Principle (verbatim): "evidence before assertions — no success claim without captured output."
- **Stage 1 — Code-level** (4 items per spec):
  - lint/type check pass
  - unit+integration tests pass with captured output appended to report
  - cross-check: every `#### Scenario:` name has a matching test name (grep both, set difference == ∅)
  - manual smoke test for frontend projects (dev server + golden path + edge cases)
- **Stage 2 — Spec** (2 items per spec):
  - `openspec validate {change-id} --strict` pass
  - tasks.md all checked OR have explicit deferred reason
- **Stage 3 — Diagram** (per diagram type, conditional on `diagrams/` non-empty):
  - sequence: extract message order, grep matching call sequence in code
  - state: extract states/transitions, compare to state-machine enum/switch in code
  - class: compare entities/methods to actual type definitions
  - ER: compare entities/relations to migration DDL or ORM models
  - activity / use case / component / deployment: mark `manual-review`, prompt user for go/no-go
- **Stage 4 — Design** (per state in `designs/figma.md`, conditional on file exists):
  - launch dev server / storybook
  - capture implementation screenshot per state
  - place side-by-side with Figma reference; list diffs
  - shared components check: confirm `existing` components are imported, not duplicated
- **Stage 5 — Aggregation**:
  - write `verification-report.md` (template per spec)
  - full pass → suggest `openspec archive {change-id}`
  - any fail → route back: code fail → SDD/TDD; spec fail → writing-spec; diagram fail → writing-uml; design fail → writing-figma

- [ ] **Step 2: Validate frontmatter**

Run: `python scripts/validate-skill-frontmatter.py plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md`
Expected: `OK: 1 skill file(s) validated`

- [ ] **Step 3: Confirm all 5 stages documented**

Run: `grep -cE "^### Stage [1-5]" plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md`
Expected: `5`

- [ ] **Step 4: Commit**

```bash
git add plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md
git commit -m "feat: add verification-before-completion skill"
```

---

## Task 10: Marketplace Registration + Full Frontmatter Validation

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Add `spec-driven-dev` to `plugins` array**

Edit `.claude-plugin/marketplace.json`. The new `plugins` array:

```json
"plugins": [
    {
      "name": "yuki-toolkit",
      "source": "./plugins/yuki-toolkit",
      "description": "整合 Google Calendar、Strava、Notion、Garmin 的個人助理工具包"
    },
    {
      "name": "spec-driven-dev",
      "source": "./plugins/spec-driven-dev",
      "description": "Spec-driven development pipeline: brainstorming → plans → (UML/Figma) → OpenSpec → SDD/TDD → verification"
    }
  ]
```

- [ ] **Step 2: Validate marketplace JSON**

Run: `python -c "import json; m=json.load(open('.claude-plugin/marketplace.json')); names=[p['name'] for p in m['plugins']]; assert names==['yuki-toolkit','spec-driven-dev'], names; print('OK', names)"`
Expected: `OK ['yuki-toolkit', 'spec-driven-dev']`

- [ ] **Step 3: Run frontmatter validation across ALL new SKILL.md files**

Run:
```bash
python scripts/validate-skill-frontmatter.py \
  plugins/spec-driven-dev/skills/brainstorming/SKILL.md \
  plugins/spec-driven-dev/skills/writing-plans/SKILL.md \
  plugins/spec-driven-dev/skills/writing-uml/SKILL.md \
  plugins/spec-driven-dev/skills/writing-figma/SKILL.md \
  plugins/spec-driven-dev/skills/writing-spec/SKILL.md \
  plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md \
  plugins/spec-driven-dev/skills/test-driven-development/SKILL.md \
  plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md
```
Expected: `OK: 8 skill file(s) validated`

- [ ] **Step 4: Cross-skill transition link check**

Run:
```bash
grep -l "spec-driven-dev:writing-plans" plugins/spec-driven-dev/skills/brainstorming/SKILL.md && \
grep -l "spec-driven-dev:writing-spec" plugins/spec-driven-dev/skills/writing-uml/SKILL.md plugins/spec-driven-dev/skills/writing-figma/SKILL.md && \
grep -l "spec-driven-dev:subagent-driven-development\|spec-driven-dev:test-driven-development" plugins/spec-driven-dev/skills/writing-spec/SKILL.md && \
grep -l "spec-driven-dev:verification-before-completion" plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md plugins/spec-driven-dev/skills/test-driven-development/SKILL.md
```
Expected: all greps return their input filenames (no empty output, no errors).

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: register spec-driven-dev plugin in marketplace"
```

---

## Task 11: Smoke Test with Toy Change

**Goal:** Walk a tiny change end-to-end to confirm the chain works. This is the integration test for the whole plugin.

**Setup**: Pick a toy change-id `add-hello-endpoint` (purely demo — no real implementation merged).

- [ ] **Step 1: Install plugin locally**

Per Claude Code marketplace conventions:

```bash
# In a fresh Claude Code session
/plugin marketplace add /Users/bibiota/Documents/projects/my-claude-code
/plugin install spec-driven-dev@yuki-marketplace
```

Confirm: skills appear in `/help` skill list under `spec-driven-dev:*`.

- [ ] **Step 2: Verify brainstorming is invokable**

In a new Claude Code session, prompt: "Use spec-driven-dev:brainstorming to design a trivial /hello GET endpoint that returns 'world'."

Expected: brainstorming announces itself, detects language, asks clarifying questions, and after approval writes `openspec/changes/add-hello-endpoint/design.md`.

- [ ] **Step 3: Verify writing-plans chains correctly**

After approving the design, confirm Claude invokes `spec-driven-dev:writing-plans` (not `superpowers:writing-plans`).

Expected: `openspec/changes/add-hello-endpoint/tasks.md` is produced.

- [ ] **Step 4: Verify optional skill bypass works**

When asked about UML/Figma, answer "no" to both.

Expected: writing-plans transitions directly to `spec-driven-dev:writing-spec`, skipping writing-uml and writing-figma.

- [ ] **Step 5: Verify writing-spec produces OpenSpec output**

Expected:
- `openspec/changes/add-hello-endpoint/proposal.md` exists with Why / What Changes / Impact / Related Artifacts sections.
- `openspec/changes/add-hello-endpoint/specs/{capability}/spec.md` exists with at least one ADDED Requirement and `#### Scenario:`.
- `openspec validate add-hello-endpoint --strict` passes (skip if openspec CLI not installed; instead lint manually).

- [ ] **Step 6: Verify SDD vs TDD choice prompt**

Expected: writing-spec ends by asking "SDD or TDD?". Pick TDD for this smoke test.

- [ ] **Step 7: Verify TDD writes a failing test**

Expected: a failing test for `GET /hello returns 'world'` exists and was committed in Red state.

- [ ] **Step 8: Verify verification-before-completion produces report**

After TDD finishes (Green + Refactor), the chain auto-invokes verification.

Expected: `openspec/changes/add-hello-endpoint/verification-report.md` exists with Code / Spec sections (Diagram and Design sections marked `n/a`).

- [ ] **Step 9: Tear down smoke artifacts**

```bash
rm -rf openspec/changes/add-hello-endpoint
git checkout -- openspec  # if anything else accidentally changed
```

> **Note:** Smoke-test artifacts are NOT committed. The toy change is throwaway.

- [ ] **Step 10: Commit smoke-test journal**

Append a brief summary to `docs/superpowers/plans/2026-05-28-spec-driven-dev-plugin.md` (this file) under a new `## Smoke Test Result` section: pass/fail per step, any issues, total time.

```bash
git add docs/superpowers/plans/2026-05-28-spec-driven-dev-plugin.md
git commit -m "docs: record spec-driven-dev plugin smoke test result"
```

---

## Task 12: Push and Open PR

- [ ] **Step 1: Push branch**

```bash
git push -u origin feat/spec-driven-dev
```

- [ ] **Step 2: Open PR**

```bash
gh pr create --title "feat: add spec-driven-dev plugin" --body "$(cat <<'EOF'
## Summary
- Adds new plugin `spec-driven-dev` with 8 chained skills: brainstorming → writing-plans → (writing-uml?) → (writing-figma?) → writing-spec → SDD|TDD → verification-before-completion.
- All skills produce/consume `openspec/changes/{change-id}/` as common data layer; full OpenSpec CLI integration.
- Registered in `marketplace.json` alongside `yuki-toolkit`.

## Test plan
- [ ] Smoke test passes (see `docs/superpowers/plans/2026-05-28-spec-driven-dev-plugin.md` § Smoke Test Result).
- [ ] All 8 SKILL.md files pass `scripts/validate-skill-frontmatter.py`.
- [ ] `marketplace.json` parses and lists both plugins.
- [ ] Cross-skill transitions verified via grep checks (Task 10 step 4).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Confirm CI version-bump workflow does not need manual intervention**

CI bumps patch version on merge to master (`.github/workflows/auto-version-bump.yml`). No manual `version` edit needed in `plugin.json`.

---

## Self-Review

**Spec coverage check** (each spec section → task):

| Spec § | Covered by Task |
|---|---|
| Goals + 流程 + Plugin 結構 | Task 1 |
| 跨 skill 共通規則 | embedded in every SKILL.md task |
| Skill 1 brainstorming | Task 2 |
| Skill 2 writing-plans | Task 3 |
| Skill 3 writing-uml | Task 4 |
| Skill 4 writing-figma | Task 5 |
| Skill 5 writing-spec | Task 6 |
| Skill 6 SDD | Task 7 |
| Skill 7 TDD | Task 8 |
| Skill 8 verification | Task 9 |
| Marketplace registration + smoke (後續步驟) | Tasks 10 + 11 |

All spec sections covered.

**Placeholder scan**: no `TBD`, `TODO`, "implement later", or "similar to Task N" in the plan. Every step has either exact code, an exact command, or a spec § reference for content that is fully specified in the spec.

**Type consistency**: skill names used across transition strings are consistent (`spec-driven-dev:writing-plans`, etc.). `change-id`, `capability`, file path conventions (`openspec/changes/{change-id}/...`) are used identically across tasks.

**One known dependency on locked input**: The plan defers `SKILL.md` body content to specific spec sections rather than inlining ~1500 lines of markdown. This is acceptable because:
1. The spec is locked and committed at `docs/superpowers/specs/2026-05-28-spec-driven-dev-plugin-design.md`.
2. Each task names the exact `§ Skill N` to read.
3. The structural skeleton (frontmatter, HARD-GATE, Checklist, templates) is inlined verbatim in the plan.
