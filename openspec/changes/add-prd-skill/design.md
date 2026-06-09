# PRD Skill Design

**Date:** 2026-06-09
**Plugin:** spec-driven-dev
**Status:** Approved

---

## Summary

Add an optional PRD (Product Requirements Document) skill to the `spec-driven-dev` plugin. The skill sits between `brainstorming` and the downstream implementation skills (`writing-plans`, `writing-figma`, `writing-uml`), and writes a structured `prd.md` into the existing `openspec/changes/{change-id}/` directory.

---

## Flow Architecture

```
brainstorming
    │
    ├─ [user wants PRD] ──→ spec-driven-dev:prd
    │                            │
    │                            ↓
    │                       prd.md → openspec/changes/{change-id}/
    │                            │
    │                            ↓
    │                       prompt: writing-plans / writing-figma / writing-uml
    │
    └─ [skip PRD] ────────→ writing-plans（現有行為不變）
```

`brainstorming` terminal state 前插入選擇提示，讓使用者決定是否建立 PRD 再接下游。PRD 是 optional；跳過時流程不變。

---

## PRD Skill

### Trigger

- `/prd` 使用者直接呼叫
- 或 `brainstorming` 銜接呼叫

### Language Detection

- 偵測使用者訊息語言，預設繁體中文
- 使用者可在任何時間切換：`lang:en`、`lang:zh-TW`，或直接用目標語言對話

### Steps

1. **確認 change-id** — 從 `openspec/changes/` 偵測 in-flight change；若無則請使用者指定
2. **澄清問題（3–5 題）** — lettered options（A/B/C/D），可用 `1A 2C 3B` 快速回答；聚焦 Problem / Core Functionality / Scope / Success Criteria
3. **產生 PRD** — 依下方結構輸出，寫入 `openspec/changes/{change-id}/prd.md`
4. **使用者審核** — 詢問是否需要修改，待確認後繼續
5. **Terminal state** — 提示接下來選項：`writing-plans` / `writing-figma` / `writing-uml`

### PRD Document Structure (`prd.md`)

```
# PRD: {Feature Name}

## 1. Introduction
### Background
### Problem Statement
### Target Users

## 2. Goals
（可量化產品目標，bullet list）

## 3. Non-Goals
（明確排除範圍）

## 4. User Stories
（US-001 格式，含 Acceptance Criteria checklist）

## 5. Functional Requirements
（FR-001 格式，明確、可驗收、無歧義）

## 6. Non-Functional Requirements  [optional]
（效能、安全、權限、穩定性、監控、資料一致性）

## 7. Technical Considerations  [optional]
（約束、依賴、整合點；不寫過度細節）

## 8. Metrics
（成功指標與追蹤方式）

## 9. Open Questions
（待確認事項）
```

NFR 和 Technical Considerations 標記為 optional；小功能可省略。

---

## File Changes

| File | Change |
|------|--------|
| `plugins/spec-driven-dev/skills/prd/SKILL.md` | **New** — skill definition |
| `plugins/spec-driven-dev/skills/brainstorming/SKILL.md` | Insert PRD optional prompt before terminal state |
| `plugins/spec-driven-dev/.claude-plugin/plugin.json` | Add `./skills/prd` to `skills` array |
| `plugins/spec-driven-dev/.codex-plugin/plugin.json` | Sync prd skill entry |
| `README.md` | Add `prd` row to spec-driven-dev Skills table |

Files not touched: `writing-plans`, `writing-figma`, `writing-uml`, `yuki-toolkit`.

---

## Out of Scope

- No hard gate on writing-figma / writing-uml / writing-plans requiring prd.md to exist
- No changes to yuki-toolkit plugin
- No changes to openspec artifact format beyond adding prd.md
