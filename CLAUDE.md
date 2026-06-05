# Yuki Marketplace

個人 Claude Code / Codex plugin marketplace（BIBIOTA/my-claude-code）。

## 目錄結構

```
plugins/yuki-toolkit/
├── .claude-plugin/plugin.json   # plugin 註冊（agents, skills, metadata）
├── .codex-plugin/plugin.json    # Codex plugin 註冊（shared content metadata）
├── agents/                       # Agent 定義（.md frontmatter 格式）
├── skills/                       # Skill 定義（.md frontmatter 格式）
└── mcp-config.md                 # MCP server 設定指南
```

## 開發規則

- **不要手動修改 Claude `plugin.json` 的 `version`** — CI merge 到 master 時自動 bump patch version（`.github/workflows/auto-version-bump.yml`）。Codex `.codex-plugin/plugin.json` version 要與對應 Claude plugin version 保持一致；若 bump 流程改變或 bump 後 Codex version 未同步，需補上同步更新。
- **Claude/Codex manifest 是包裝 metadata** — `skills/` 與 `agents/` 才是共用行為 source of truth，不要複製第二份長篇 skill/agent 內容。
- **Google Workspace 操作統一用 `gws` CLI** — 不使用個別 MCP server。指令參考見 `plugins/yuki-toolkit/skills/gws-reference/SKILL.md`
- **Agent/Skill 檔案使用 YAML frontmatter** — 開頭和結尾都要有 `---` 分隔線

## Git 慣例

- Branch: `feat/<feature-name>`
- PR target: `master`
- Commit prefix: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
