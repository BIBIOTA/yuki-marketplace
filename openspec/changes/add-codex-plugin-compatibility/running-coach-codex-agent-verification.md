# Running Coach Codex Agent Verification

## Scope

Task 2.2 verifies Codex handling for
`plugins/yuki-toolkit/agents/running-coach-zh-tw.md`.

This check records whether the running coach can remain agent-first without
duplicating the long instruction body into a Codex-only skill.

## Official Codex Plugin Examples Checked

Installed official Codex plugin example inspected:

- `/Users/bibiota/.codex/plugins/cache/openai-curated/figma/e2d08a2e/.codex-plugin/plugin.json`
- `/Users/bibiota/.codex/plugins/cache/openai-curated/figma/e2d08a2e/agents/`
- `/Users/bibiota/.codex/plugins/cache/openai-curated/figma/e2d08a2e/commands/`

Findings:

- The Figma Codex plugin manifest declares `skills` and `apps`; it does not
  declare an explicit `agents` field.
- The installed Figma plugin still carries plugin-level files under `agents/`.
- Figma command files reference agent names such as
  `figma-implementation-agent`, showing that plugin-carried agent files are a
  supported convention even when the plugin manifest does not list `agents`.
- Figma Markdown agent files are plain prompt files. The running coach file is
  a Claude-style agent file with YAML frontmatter including `name`,
  `description`, and `model: sonnet`.

## Local Codex Install Behavior

Commands were run with temporary `HOME` and `CODEX_HOME` values to avoid
mutating the user's real Codex configuration.

Initial setup note:

```sh
tmp_home=$(mktemp -d)
export HOME="$tmp_home"
export CODEX_HOME="$tmp_home/.codex"
mkdir -p "$CODEX_HOME"
```

Marketplace discovery:

```sh
codex plugin marketplace add /Users/bibiota/Documents/projects/my-claude-code
codex plugin list --available --json
```

Result:

- Marketplace add succeeded as `yuki-marketplace`.
- `codex plugin list --available --json` listed both `yuki-toolkit` and
  `spec-driven-dev`.
- `yuki-toolkit` resolved to
  `/Users/bibiota/Documents/projects/my-claude-code/plugins/yuki-toolkit`.

Plugin install:

```sh
codex plugin add yuki-toolkit@yuki-marketplace
codex plugin list --json
find "$CODEX_HOME" -maxdepth 8 -type f | sort
find "$CODEX_HOME" -path '*/agents/running-coach-zh-tw.md' -type f -print -exec sed -n '1,30p' {} \;
```

Result:

- `codex plugin add yuki-toolkit@yuki-marketplace` succeeded.
- Installed plugin root:
  `$CODEX_HOME/plugins/cache/yuki-marketplace/yuki-toolkit/1.1.3`.
- The installed cache includes:
  - `.codex-plugin/plugin.json`
  - `.claude-plugin/plugin.json`
  - `agents/running-coach-zh-tw.md`
  - `skills/gws-reference/SKILL.md`
  - `skills/notion-article-import/SKILL.md`
- The cached `agents/running-coach-zh-tw.md` preserved the original
  frontmatter and long instruction body.
- No `skills/running-coach-zh-tw/SKILL.md` file was created or required by the
  install flow.

## Observable Agent Exposure

The current Codex CLI commands checked were:

```sh
codex --help
codex exec --help
codex plugin --help
codex plugin list --help
codex plugin add --help
```

Finding:

- Codex exposes plugin-level listing and install state through
  `codex plugin list`.
- The checked CLI version does not expose an agent-level list command or a
  plugin-agent invocation command.
- Therefore local verification can prove that the running coach agent file is
  carried into the installed Codex plugin cache, but it cannot prove from CLI
  output alone that Codex will automatically route to this agent at runtime.

## Decision

The running coach should remain agent-first for this change.

Evidence supports keeping `plugins/yuki-toolkit/agents/running-coach-zh-tw.md`
as the preferred source of truth because:

- Official Codex plugin examples carry plugin-level `agents/` files.
- Codex local plugin install copies the `agents/` directory into the plugin
  cache.
- The install and listing flow succeeds with the running coach file present.
- No evidence was found that direct agent handling fails.

Task 2.3 is not needed for now. A thin skill wrapper should only be added if a
future runtime-level Codex check shows that the cached agent file cannot be used
or discovered in practice.

README work should document this limitation precisely: Codex installation
carries the running coach agent file, but current CLI verification only
observes plugin-level install state and cached files, not agent-level runtime
dispatch.
