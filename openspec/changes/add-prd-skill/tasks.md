# Tasks: add-prd-skill

## 1. 建立 PRD Skill

- [ ] 1.1 建立 `plugins/spec-driven-dev/skills/prd/SKILL.md`
  - Acceptance: WHEN 使用者執行 `/prd` 或由 brainstorming 呼叫 THEN skill 依序執行：確認 change-id → 澄清問題（3–5 題，lettered options）→ 產生 prd.md → 使用者審核 → 提示 writing-plans / writing-figma / writing-uml
  - AND prd.md 寫入 `openspec/changes/{change-id}/prd.md`，包含 9 個 section（Introduction/Goals/Non-Goals/User Stories/Functional Requirements/NFR[optional]/Technical Considerations[optional]/Metrics/Open Questions）
  - AND skill 偵測使用者語言，預設繁體中文，支援 `lang:en`、`lang:zh-TW` 或直接切換語言
  - Depends on: -
  - Independence: independent

## 2. 修改 brainstorming skill

- [ ] 2.1 在 `plugins/spec-driven-dev/skills/brainstorming/SKILL.md` 的 terminal state 前插入 PRD optional 提示
  - Acceptance: WHEN brainstorming 完成設計對話並準備 invoke writing-plans THEN 先提示使用者：「要先建立 PRD（`/prd`）再進入實作計畫，還是直接跳到 writing-plans？」
  - AND 使用者選擇跳過時，直接 invoke `spec-driven-dev:writing-plans`（現有行為不變）
  - AND 使用者選擇建立 PRD 時，invoke `spec-driven-dev:prd`
  - Depends on: 1.1
  - Independence: serial

## 3. 更新 Plugin Manifests

- [ ] 3.1 在 `plugins/spec-driven-dev/.claude-plugin/plugin.json` 的 `skills` 陣列加入 `./skills/prd`
  - Acceptance: WHEN plugin 載入 THEN `spec-driven-dev:prd` skill 可被 Claude Code 識別並呼叫
  - AND `prd` 插入在 `brainstorming` 之後、`writing-plans` 之前
  - Depends on: 1.1
  - Independence: parallel-safe

- [ ] 3.2 在 `plugins/spec-driven-dev/.codex-plugin/plugin.json` 的 `skills` 陣列加入 `./skills/prd`，位置與 Claude plugin 一致
  - Acceptance: WHEN Codex plugin 載入 THEN `spec-driven-dev:prd` skill 可被 Codex 識別
  - AND `.codex-plugin/plugin.json` 的 skills 順序與 `.claude-plugin/plugin.json` 一致
  - Depends on: 3.1
  - Independence: serial

## 4. 更新 README.md

- [ ] 4.1 在 README.md 的 spec-driven-dev Skills 表格中，於 `brainstorming` 列之後加入 `prd` 一列
  - Acceptance: WHEN 使用者查看 README.md THEN spec-driven-dev Skills 表格包含 `prd` 列，說明為「在 brainstorming 後、writing-plans 前，產生 Product Requirements Document 並存入 openspec/changes/{change-id}/prd.md」
  - Depends on: 1.1
  - Independence: parallel-safe

## Optional artifacts
- [ ] PlantUML diagrams (spec-driven-dev:writing-uml)
- [ ] Figma designs (spec-driven-dev:writing-figma)
