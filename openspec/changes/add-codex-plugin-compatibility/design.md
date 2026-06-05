# Add Codex Plugin Compatibility

## Goal

Make this repository installable as both a Claude Code plugin marketplace and a Codex plugin marketplace while keeping the actual tool instructions in one shared set of files.

The change must preserve the current Claude plugin path and add Codex compatibility in parallel. Daily maintenance should remain focused on the existing `skills/` and `agents/` content files, not duplicated Claude-only and Codex-only instruction copies.

## Scope

This change covers both existing plugins:

- `plugins/yuki-toolkit`
- `plugins/spec-driven-dev`

It does not introduce a manifest generator. Claude and Codex will each have small, separate packaging metadata files, while the underlying skills and agents remain shared content.

## Architecture

The repository will support two marketplace entry paths:

- Claude Code continues to use `.claude-plugin/marketplace.json` and each plugin's `.claude-plugin/plugin.json`.
- Codex will use a new `.agents/plugins/marketplace.json` and each plugin's `.codex-plugin/plugin.json`.

The existing Claude metadata must stay intact. Codex metadata is added as a compatibility layer beside it.

`spec-driven-dev` is primarily exposed through its existing `skills/` directory. Its `SKILL.md` files are already in a shape Codex can consume.

`yuki-toolkit` exposes its existing skills plus the running coach agent. `plugins/yuki-toolkit/agents/running-coach-zh-tw.md` remains the source of truth for the running coach behavior. The implementation should prefer Codex agent compatibility over converting this into a full skill. If Codex cannot directly use the current agent format, the fallback is a thin skill wrapper that points to the same running coach behavior instead of duplicating the long instruction body.

## Components

### Codex Marketplace Metadata

Add `.agents/plugins/marketplace.json` as the Codex marketplace entry. It lists:

- `yuki-toolkit`
- `spec-driven-dev`

The marketplace metadata should mirror the existing Claude marketplace at the product level, but use Codex-compatible structure.

### Codex Plugin Manifests

Add:

- `plugins/yuki-toolkit/.codex-plugin/plugin.json`
- `plugins/spec-driven-dev/.codex-plugin/plugin.json`

Each manifest should include plugin name, version, description, author, keywords, skills path, and interface metadata where appropriate.

The manifests should reference shared directories such as `./skills/` rather than listing or duplicating instruction bodies.

### Shared Content Files

The existing content files remain the source of truth:

- `plugins/spec-driven-dev/skills/*/SKILL.md`
- `plugins/yuki-toolkit/skills/*/SKILL.md`
- `plugins/yuki-toolkit/agents/running-coach-zh-tw.md`

Claude and Codex packaging should point at these files or directories. Changes to skill or agent behavior should be made once in these shared files.

### Running Coach Agent Compatibility

Codex compatibility should preserve the agent form first. The implementation should inspect Codex plugin examples and local install behavior to decide whether the existing Claude agent frontmatter is accepted.

If required, make minimal metadata changes to the existing agent file so it remains valid for both Claude and Codex. If shared agent metadata cannot satisfy both systems, add a small Codex-specific wrapper file only for routing, not a duplicated instruction body.

### Documentation

Update README and/or repo guidance with:

- Codex install commands.
- The two-package, one-content-source maintenance rule.
- The rule that Claude and Codex manifests are small packaging files, while skills and agents are the shared behavioral source.

README updates are required before development is considered complete. The final implementation must document both Claude and Codex installation paths so users can install either marketplace without inspecting manifest files manually.

## Data Flow

Claude installation continues as:

```text
Claude Code
-> /plugin marketplace add BIBIOTA/my-claude-code
-> .claude-plugin/marketplace.json
-> plugins/*/.claude-plugin/plugin.json
-> shared skills and agents
```

Codex installation becomes:

```text
Codex
-> codex plugin marketplace add <source>
-> .agents/plugins/marketplace.json
-> plugins/*/.codex-plugin/plugin.json
-> shared skills and agents
```

Maintenance flow:

```text
Edit skill or agent content
-> same file affects Claude and Codex
-> update both manifests only when a plugin capability is added, removed, or renamed
```

## Error Handling

If Codex marketplace or manifest format is invalid, validation should fail before claiming installability. Use local Codex plugin examples and real `codex plugin` commands where possible.

If Codex cannot consume the existing running coach agent metadata, adjust only the smallest incompatible metadata surface. Do not fork the long running coach instruction content into a second maintained document.

If Codex agent compatibility cannot be proven, add a thin `SKILL.md` wrapper as fallback and document why it exists.

Claude install behavior must remain unchanged. The implementation should avoid replacing or deleting `.claude-plugin` files.

Version values should initially align between Claude and Codex manifests. Because the repo currently relies on CI to bump Claude plugin versions, the implementation should document the expected version maintenance rule for the Codex manifests.

## Testing

Validation should include:

- JSON syntax checks for all new and existing marketplace and plugin manifests.
- A structural check that both Codex plugin manifests reference the intended shared `skills/` directories.
- A check that Claude marketplace and plugin manifests still exist and still point to the existing plugin paths.
- A README check confirming Codex installation and shared-maintenance guidance are documented.
- A Codex install/list smoke test using the local marketplace path or the best supported equivalent command.
- If Codex agent behavior can be verified locally, confirm `running-coach-zh-tw` appears or is otherwise usable as an agent. If it cannot be verified, record the limitation and use the fallback wrapper only if necessary.

## Probable Next Steps

This change does not require UML diagrams because it is packaging metadata plus compatibility validation, not a complex runtime flow or state machine.

This change does not require Figma designs because there is no frontend UI change.

After this design is approved, the next step is `writing-plans` to produce an implementation checklist with acceptance criteria.
