# Yuki Marketplace

個人 Claude Code / Codex plugin marketplace（BIBIOTA/yuki-marketplace）。

## 快速安裝

### Claude Code

```bash
# 在 Claude Code 中執行
/plugin marketplace add BIBIOTA/yuki-marketplace
/plugin install yuki-toolkit@yuki-marketplace
/plugin install spec-driven-dev@yuki-marketplace
```

### Codex

以下安裝來源擇一執行。

```bash
# 本機開發版本
codex plugin marketplace add /Users/bibiota/Documents/projects/yuki-marketplace
codex plugin add yuki-toolkit@yuki-marketplace
codex plugin add spec-driven-dev@yuki-marketplace
```

```bash
# GitHub repo 版本
codex plugin marketplace add BIBIOTA/yuki-marketplace
codex plugin add yuki-toolkit@yuki-marketplace
codex plugin add spec-driven-dev@yuki-marketplace
```

安裝後需手動設定 MCP servers，詳見 [MCP 配置指南](plugins/yuki-toolkit/mcp-config.md)。

## Plugin: yuki-toolkit

個人助理工具包：專業跑步教練 agent + Google Workspace 整合 + MCP server 配置模板。

### 🏃 跑步教練 Agent / Skill

專業繁體中文跑步教練代理，提供：

- Strava 跑步數據分析（配速、心率、步頻）
- Garmin 進階數據整合
- Google Calendar 訓練計畫管理
- Notion 訓練記錄與課表同步
- 個人化心率區間設定與監控
- 80/20 訓練強度分配指導

跑步教練指令只維護一份：`plugins/yuki-toolkit/skills/running-coach-zh-tw/SKILL.md`。Codex 透過 `skills/` 目錄將它載入為 skill；Claude Code 則透過 `.claude-plugin/plugin.json` 的 `agents` 設定指向同一份檔案，作為 agent 使用。

### Skills

| Skill | 說明 |
|-------|------|
| `running-coach-zh-tw` | 繁體中文專業跑步教練，分析 Strava/Garmin/Calendar/Notion 訓練資料 |
| `gws-reference` | Google Workspace CLI（`gws`）指令速查表 |
| `notion-article-import` | 將 Notion 文章匯入 bibiota-blog（VitePress Markdown 格式） |

### 📡 MCP Server 配置模板

提供以下 MCP server 的 `claude mcp add` 指令模板：

| Server | 用途 | 套件/工具 |
|------------------|--------------------------|---------------------------------------|
| Google Workspace | 日曆、郵件、雲端硬碟等 | `@anthropic-ai/gws` (`gws` CLI) |
| Strava | 運動數據 | `strava-mcp` (手動設定) |
| Notion | 筆記管理 | `@notionhq/notion-mcp-server` |
| Garmin | 穿戴裝置數據 | `garmin_mcp` (Python/UV) |
| Chrome DevTools | 瀏覽器自動化 | `chrome-devtools-mcp` |

## Plugin: spec-driven-dev

Spec-driven development pipeline：從構想到實作的完整流程，每個步驟都有使用者審核把關。

Artifacts 統一存放在 `openspec/changes/{change-id}/`。
`progress.md` 是跨 session resume anchor，由 SDD/TDD/verification 在狀態轉換時寫入。

### Skills

| Skill | 說明 |
|-------|------|
| `resume` | session 入口；偵測 in-flight change 並路由回對應 skill |
| `brainstorming` | 開始任何新功能前探索需求與設計方案 |
| `writing-plans` | 將 design.md 分解為帶 acceptance criteria 的 tasks.md |
| `writing-uml` | 用 PlantUML 產生架構圖 |
| `writing-figma` | 將設計同步到 Figma |
| `writing-spec` | 產生 OpenSpec 格式規格文件 |
| `updating-spec` | 實作或驗證後需求範圍變更時，更新 OpenSpec artifacts 並路由回實作或驗證 |
| `system-debugging` | 針對 bug 先建立觀測方法、重現步驟與根因證據 |
| `subagent-driven-development` | 用平行 subagent 執行實作任務 |
| `test-driven-development` | Red-Green-Refactor TDD 循環 |
| `verification-before-completion` | 實作完成後的五階段驗證 |

## 前置需求

- [Claude Code](https://claude.com/claude-code) CLI
- Codex CLI
- 各 MCP server 對應的帳號和 API 認證（詳見配置指南）

## 維護規則

- Claude 與 Codex 使用各自的包裝 metadata：`.claude-plugin/*`、`plugins/*/.claude-plugin/plugin.json`、`.agents/plugins/marketplace.json`、`plugins/*/.codex-plugin/plugin.json`。
- 實際行為文件只維護一份：`plugins/*/skills/` 是 Claude/Codex 共用的 source of truth；Claude agent 可以透過 manifest 指向同一份 `SKILL.md`，不要為 Codex 或 Claude 複製第二份長篇 skill/agent 內容。
- 新增、移除或改名 plugin 能力時，才同步更新 Claude/Codex manifest；日常修改 skill/agent 內容不需要改 manifest。
- 不要手動修改 Claude `plugin.json` 的 `version`；CI merge 到 `master` 時會自動 bump patch version。Codex manifest version 應與對應 Claude plugin version 保持一致；若版本 bump 流程改變，或 bump 後 Codex manifest 沒有同步，需補上對應更新。

## 授權

MIT
