# Yuki Marketplace

個人 Claude Code plugin marketplace（BIBIOTA/my-claude-code）。

## 快速安裝

```bash
# 在 Claude Code 中執行
/plugin marketplace add BIBIOTA/my-claude-code
/plugin install yuki-toolkit@yuki-marketplace
/plugin install spec-driven-dev@yuki-marketplace
```

安裝後需手動設定 MCP servers，詳見 [MCP 配置指南](plugins/yuki-toolkit/mcp-config.md)。

## Plugin: yuki-toolkit

個人助理工具包：專業跑步教練 agent + Google Workspace 整合 + MCP server 配置模板。

### 🏃 跑步教練 Agent

專業繁體中文跑步教練代理，提供：

- Strava 跑步數據分析（配速、心率、步頻）
- Garmin 進階數據整合
- Google Calendar 訓練計畫管理
- Notion 訓練記錄與課表同步
- 個人化心率區間設定與監控
- 80/20 訓練強度分配指導

### Skills

| Skill | 說明 |
|-------|------|
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

### Skills

| Skill | 說明 |
|-------|------|
| `brainstorming` | 開始任何新功能前探索需求與設計方案 |
| `writing-plans` | 將 design.md 分解為帶 acceptance criteria 的 tasks.md |
| `writing-uml` | 用 PlantUML 產生架構圖 |
| `writing-figma` | 將設計同步到 Figma |
| `writing-spec` | 產生 OpenSpec 格式規格文件 |
| `subagent-driven-development` | 用平行 subagent 執行實作任務 |
| `test-driven-development` | Red-Green-Refactor TDD 循環 |
| `verification-before-completion` | 實作完成後的五階段驗證 |

## 前置需求

- [Claude Code](https://claude.com/claude-code) CLI
- 各 MCP server 對應的帳號和 API 認證（詳見配置指南）

## 授權

MIT
