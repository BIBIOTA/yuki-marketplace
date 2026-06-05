## ADDED Requirements

### Requirement: Repository shall expose a Codex marketplace entry
The repository SHALL provide Codex marketplace metadata that lists both existing plugins without replacing the Claude marketplace metadata.

#### Scenario: Codex marketplace lists both plugins
- **WHEN** `.agents/plugins/marketplace.json` is read
- **THEN** it lists `yuki-toolkit` and `spec-driven-dev`
- **AND** each listed plugin points to its existing plugin directory

#### Scenario: Claude marketplace remains present
- **WHEN** the Codex marketplace metadata is added
- **THEN** `.claude-plugin/marketplace.json` still exists
- **AND** it still lists the existing Claude plugin sources

### Requirement: Each plugin shall provide Codex plugin metadata
Each existing plugin SHALL include a `.codex-plugin/plugin.json` manifest that exposes the plugin to Codex while keeping instruction content in shared files.

#### Scenario: yuki-toolkit has Codex metadata
- **WHEN** `plugins/yuki-toolkit/.codex-plugin/plugin.json` is read
- **THEN** it declares the `yuki-toolkit` plugin
- **AND** it references the shared `./skills/` directory
- **AND** it includes Codex interface metadata
- **AND** it does not contain copied skill or agent instruction bodies

#### Scenario: spec-driven-dev has Codex metadata
- **WHEN** `plugins/spec-driven-dev/.codex-plugin/plugin.json` is read
- **THEN** it declares the `spec-driven-dev` plugin
- **AND** it references the shared `./skills/` directory
- **AND** it includes Codex interface metadata
- **AND** it does not contain copied skill instruction bodies

#### Scenario: Claude plugin manifests remain compatible
- **WHEN** Codex plugin manifests are added
- **THEN** `plugins/yuki-toolkit/.claude-plugin/plugin.json` still exists
- **AND** `plugins/spec-driven-dev/.claude-plugin/plugin.json` still exists
- **AND** both Claude manifests still reference their existing shared skill and agent paths

### Requirement: Shared instruction files shall remain the source of truth
The system SHALL keep skill and agent instruction bodies in one maintained set of content files.

#### Scenario: Existing skills remain shared
- **WHEN** skill behavior is maintained
- **THEN** `plugins/spec-driven-dev/skills/*/SKILL.md` remains the source for `spec-driven-dev`
- **AND** `plugins/yuki-toolkit/skills/*/SKILL.md` remains the source for `yuki-toolkit`
- **AND** Codex manifests reference shared paths instead of duplicated instruction content

#### Scenario: Running coach remains agent-first
- **WHEN** `running-coach-zh-tw` is exposed for Codex
- **THEN** `plugins/yuki-toolkit/agents/running-coach-zh-tw.md` remains the preferred source of truth
- **AND** the long running coach instruction body is not duplicated into a separate Codex-only skill

#### Scenario: Thin wrapper is added only when required
- **WHEN** Codex cannot directly consume `plugins/yuki-toolkit/agents/running-coach-zh-tw.md`
- **THEN** a minimal `SKILL.md` wrapper may be added
- **AND** the wrapper routes to the same running coach behavior
- **AND** it does not duplicate the long running coach instruction body

### Requirement: README shall document Codex installation and maintenance
The README SHALL document both installation paths and the shared-maintenance model before the change is considered complete.

#### Scenario: README includes Codex installation
- **WHEN** `README.md` is read
- **THEN** it documents Codex marketplace setup
- **AND** it documents installing `yuki-toolkit` and `spec-driven-dev` through Codex
- **AND** it still documents the Claude Code install path

#### Scenario: README explains one-content-source maintenance
- **WHEN** `README.md` is read
- **THEN** it explains that Claude and Codex manifests are separate packaging metadata
- **AND** it explains that `skills/` and `agents/` are the shared behavioral source of truth

#### Scenario: README or repo guidance explains version alignment
- **WHEN** README or repository guidance is read
- **THEN** it explains how Codex manifest versions should stay aligned with the existing Claude plugin version bump process

### Requirement: Compatibility shall be verified with concrete checks
The implementation SHALL verify the compatibility layer with syntax, structure, documentation, and Codex smoke checks.

#### Scenario: Manifest JSON parses successfully
- **WHEN** all Claude and Codex marketplace and plugin manifest files are parsed as JSON
- **THEN** parsing succeeds without syntax errors

#### Scenario: Codex manifests reference existing shared paths
- **WHEN** Codex plugin manifests are inspected
- **THEN** their `skills` references point to existing shared `skills/` directories
- **AND** no manifest contains copied instruction bodies

#### Scenario: Codex marketplace smoke behavior is recorded
- **WHEN** the best supported local or repository Codex marketplace command is run
- **THEN** Codex can list or attempt to install `yuki-toolkit` and `spec-driven-dev`
- **OR** the exact command limitation is recorded with evidence

#### Scenario: Running coach Codex behavior is recorded
- **WHEN** Codex agent behavior can be verified locally
- **THEN** the result records whether `running-coach-zh-tw` appears or is otherwise usable as an agent
- **AND** if agent behavior cannot be verified, the limitation is recorded before adding any fallback wrapper
