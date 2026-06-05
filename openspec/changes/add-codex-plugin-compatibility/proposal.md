## Why

This repository currently works as a Claude Code plugin marketplace, but it is not installable as a Codex plugin marketplace because Codex expects different marketplace and plugin metadata.

The existing skill and agent instruction files are largely reusable. The change adds Codex packaging without forking the long instruction content, so the repository can support both Claude Code and Codex while keeping one behavioral source of truth.

## What Changes

- **codex-plugin-compatibility**: Add Codex marketplace metadata and Codex plugin manifests for `yuki-toolkit` and `spec-driven-dev`.
- **codex-plugin-compatibility**: Preserve existing Claude plugin metadata and shared `skills/` / `agents/` content.
- **codex-plugin-compatibility**: Prefer Codex agent compatibility for `running-coach-zh-tw`, with a thin skill wrapper only if direct agent use cannot be verified.
- **codex-plugin-compatibility**: Update README with Codex installation and shared-maintenance guidance.
- **codex-plugin-compatibility**: Validate JSON, shared path references, Claude metadata preservation, README coverage, and Codex marketplace smoke behavior.

## Impact

- Affected specs: `specs/codex-plugin-compatibility/`
- Affected code: `.agents/plugins/marketplace.json`, `plugins/*/.codex-plugin/plugin.json`, `README.md`, and possibly a minimal `plugins/yuki-toolkit/skills/running-coach-zh-tw/SKILL.md` fallback if Codex cannot directly consume the existing agent.
- Breaking changes: No. Existing `.claude-plugin` metadata and shared instruction files must remain compatible with the current Claude Code install path.

## Related Artifacts

### Design

- [design.md](./design.md)
- [tasks.md](./tasks.md)

### Diagrams

- None

### Figma Designs

- None
