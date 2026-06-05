# Tasks: add-codex-plugin-compatibility

## 1. Codex Packaging Metadata
- [x] 1.1 Add the Codex marketplace entry
  - Acceptance: WHEN `.agents/plugins/marketplace.json` is read THEN it lists `yuki-toolkit` and `spec-driven-dev` with Codex-compatible source paths
  - Depends on: -
  - Independence: independent
- [x] 1.2 Add the `yuki-toolkit` Codex plugin manifest
  - Acceptance: WHEN `plugins/yuki-toolkit/.codex-plugin/plugin.json` is read THEN it declares `yuki-toolkit`, references the shared `./skills/` directory, includes Codex interface metadata, and does not duplicate skill or agent instruction bodies
  - Depends on: 1.1
  - Independence: parallel-safe
- [x] 1.3 Add the `spec-driven-dev` Codex plugin manifest
  - Acceptance: WHEN `plugins/spec-driven-dev/.codex-plugin/plugin.json` is read THEN it declares `spec-driven-dev`, references the shared `./skills/` directory, includes Codex interface metadata, and does not duplicate skill instruction bodies
  - Depends on: 1.1
  - Independence: parallel-safe

## 2. Shared Agent and Skill Compatibility
- [x] 2.1 Preserve Claude plugin metadata
  - Acceptance: WHEN the change is complete THEN `.claude-plugin/marketplace.json`, `plugins/yuki-toolkit/.claude-plugin/plugin.json`, and `plugins/spec-driven-dev/.claude-plugin/plugin.json` still exist and still reference the existing Claude plugin paths
  - Depends on: -
  - Independence: independent
- [x] 2.2 Verify Codex handling for the running coach agent
  - Acceptance: WHEN Codex plugin examples and local install behavior are checked THEN the result records whether `plugins/yuki-toolkit/agents/running-coach-zh-tw.md` is usable as a Codex agent without converting the long instruction body into a skill
  - Depends on: 1.2
  - Independence: serial
- [x] 2.3 Add a thin running coach skill wrapper only if required
  - Acceptance: WHEN Codex cannot use the running coach agent directly THEN a minimal `SKILL.md` wrapper is added that routes to the same running coach behavior without duplicating the long instruction body
  - Depends on: 2.2
  - Independence: serial
  - Completion note: Not required for this change; task 2.2 verified install/cache behavior and found no install-time or discovery-time failure requiring a wrapper.

## 3. Documentation
- [x] 3.1 Update README with Codex installation instructions
  - Acceptance: WHEN README is read THEN it documents both Claude Code and Codex installation commands for the two-plugin marketplace
  - Depends on: 1.1, 1.2, 1.3
  - Independence: serial
- [x] 3.2 Document the shared-maintenance rule
  - Acceptance: WHEN README is read THEN it explains that Claude and Codex manifests are separate packaging metadata while `skills/` and `agents/` remain the shared behavioral source of truth
  - Depends on: 3.1
  - Independence: serial
- [x] 3.3 Document version maintenance expectations
  - Acceptance: WHEN README or repo guidance is read THEN it explains how Codex manifest versions should stay aligned with the existing Claude plugin version bump process
  - Depends on: 3.1
  - Independence: serial

## 4. Validation
- [x] 4.1 Validate manifest JSON
  - Acceptance: WHEN all Claude and Codex marketplace and plugin manifest files are parsed as JSON THEN parsing succeeds without syntax errors
  - Depends on: 1.1, 1.2, 1.3
  - Independence: parallel-safe
- [x] 4.2 Validate shared path references
  - Acceptance: WHEN Codex plugin manifests are inspected THEN their `skills` references point to existing shared `skills/` directories and no copied instruction body appears in manifest JSON
  - Depends on: 1.2, 1.3
  - Independence: parallel-safe
- [x] 4.3 Run a Codex marketplace smoke test
  - Acceptance: WHEN the best supported local or repository marketplace command is run THEN Codex can list or attempt to install `yuki-toolkit` and `spec-driven-dev`, or the exact command limitation is recorded with evidence
  - Depends on: 1.1, 1.2, 1.3, 2.2
  - Independence: serial
- [x] 4.4 Verify README completion criteria
  - Acceptance: WHEN README is checked THEN Codex installation guidance, Claude installation guidance, shared-maintenance guidance, and version maintenance guidance are all present
  - Depends on: 3.1, 3.2, 3.3
  - Independence: parallel-safe

## Optional artifacts
- [ ] PlantUML diagrams (spec-driven-dev:writing-uml)
- [ ] Figma designs (spec-driven-dev:writing-figma)
