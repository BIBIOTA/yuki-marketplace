---
change-id: add-cross-session-harness
language: zh-TW
date: 2026-06-08
author: BIBIOTA
status: draft
---

# Design: add-cross-session-harness

## Why

walkinglabs/learn-harness-engineering 的 12 場 lectures 把「為什麼有能力的模型還是會在真實工程任務上失敗」歸納成 5 個子系統：Instructions / State / Verification / Scope / Session Lifecycle。

對照目前 spec-driven-dev plugin：

- **Instructions（漸進式揭露）** — 9 個 SKILL.md，已對齊 L4。
- **Verification（victory detector）** — `verification-before-completion` 五階段 + SDD 雙審，已對齊 L9/L10。
- **Scope（單一在途功能）** — 有意識（brainstorming 的 scope check、tasks.md 的 `independence`）但沒有強制的機器可讀標記。
- **State（跨 session 持久狀態）** — 只有 per-change state，缺 cross-session state；若 session 在 SDD 第 3/7 個任務被壓縮或重啟，LLM 必須 grep 整個 `openspec/changes/{change-id}/` 自己推斷狀態。
- **Session Lifecycle（init / cleanup）** — 完全沒有 init phase。每個 skill 都假設「從上一個 skill 接過來」的乾淨脈絡。

本 change 補齊 State + Session Lifecycle 兩條軸線中最關鍵的入口問題：**讓任何被重啟的 session 能無歧義恢復進度**。

## Scope

In scope：
1. 新 skill：`resume` — 偵測 in-flight change 並路由到對應的 implementation skill
2. 新檔案規範：`progress.md`（per-change append-only log）
3. tasks.md template 加 `status` 欄並建立 single-in-progress 不變式

Out of scope（未來再評估）：
- cleanup-scanner（L12）
- trivial change 快車道
- verification-pending 結算稽核
- observability runtime logger（L11）
- 全域 `.openspec/active-change` 指標檔（採用 Approach A，不引入）

## Approach selected

**A. Minimal additive** — 加 1 個新 skill + 動 4 個現有 skill。理由：

- ④⑤⑥⑦ 已先排除 → 不做 Approach C（範圍會超出同意）。
- 多 in-flight change 是罕見場景（spec-driven-dev 鼓勵 single-change-in-flight）→ 不需要 Approach B 的全域指標檔；resume 在「找到 >1 個」時直接列表給使用者擇一即可。

## Architecture

新增「per-change session state」這一層，覆蓋在既有 per-change spec state 之上。

```
openspec/changes/{change-id}/
├── design.md                ← brainstorming
├── tasks.md                 ← writing-plans（新加 status 欄）
├── proposal.md              ← writing-spec
├── specs/                   ← writing-spec
├── diagrams/                ← writing-uml (optional)
├── designs/                 ← writing-figma (optional)
├── progress.md              ← NEW; SDD/TDD/verification append-only
├── debugging-report.md      ← system-debugging (optional)
└── verification-report.md   ← verification
```

Resume skill 的核心演算法：

1. 掃 `openspec/changes/*/` 找「有 `design.md` 但無 `verification-report.md`」的 directory（= in-flight）
2. 0 個 → 報告 no in-flight change，建議 `/spec-driven-dev:brainstorming`
3. 1 個 → 讀 `progress.md` 最後一筆 → 輸出 next action 並 invoke 對應 skill
4. >1 個 → 列表，等使用者擇一後再進入步驟 3

上游 skill（brainstorming / writing-plans / writing-spec / SDD / TDD）入口加 ~5 行 precheck：發現有 in-flight change → 反問「要 resume 還是開新 change？」。

## Components

| 動作 | 路徑 | 變更摘要 |
|---|---|---|
| 新增 | `plugins/spec-driven-dev/skills/resume/SKILL.md` | 全新 skill；checklist + process flow + 演算法 |
| 改 | `plugins/spec-driven-dev/skills/writing-plans/SKILL.md` | tasks.md template 加 `status` sub-bullet 與 4 狀態說明 |
| 改 | `plugins/spec-driven-dev/skills/subagent-driven-development/SKILL.md` | (a) 入口 precheck；(b) 每 task 開始時把 status 改 `in_progress`；(c) 每 task 完成後 append progress.md entry + 改 status `passing`；(d) 入口檢查 single-in-progress 不變式 |
| 改 | `plugins/spec-driven-dev/skills/test-driven-development/SKILL.md` | 同上四點 |
| 改 | `plugins/spec-driven-dev/skills/brainstorming/SKILL.md` | 入口 precheck（其餘流程不動） |
| 改 | `plugins/spec-driven-dev/skills/writing-spec/SKILL.md` | 入口 precheck |
| 改 | `plugins/spec-driven-dev/skills/verification-before-completion/SKILL.md` | Stage 2 加：progress.md 存在 + 最後一筆有 `Next action` |
| 改 | `plugins/spec-driven-dev/.claude-plugin/plugin.json` | `skills` array 加 `./skills/resume` |
| 改 | `plugins/spec-driven-dev/.codex-plugin/plugin.json` | 同步 |
| 改 | `README.md`（repo root） | `## Plugin: spec-driven-dev` 段的 `### Skills` 表加入 `resume` 一列；若 `Artifacts 統一存放在 openspec/changes/{change-id}/` 該段需要提及 `progress.md` 也補上 |

## Data flow

### progress.md schema

Append-only Markdown。第一筆由首個進入該 change 的實作 skill（SDD/TDD）建立；之後每完成一個 task 就 append 一筆 Session entry。`brainstorming`/`writing-plans`/`writing-spec` 階段**不寫**（這些階段以 commit 為證據已足夠，且狀態變更頻率低）。

````markdown
# Progress: {change-id}

## Session {N} — {YYYY-MM-DD HH:mm}
- Stage: SDD | TDD | verification
- Task: {task-id} {title}  (or "n/a" for non-task work)
- Transition: not_started → in_progress  |  in_progress → passing  |  in_progress → blocked
- Evidence:
  - Commits: {hash} {subject}
  - Tests: {short output excerpt or path to log}
- Next action: {one sentence}
- Blockers: {if any}
````

設計約束：

- **Append-only** — 永不修改舊 entry。歷史是稽核資料。
- **Session N 由寫入時掃既有 Session entries 取 max+1** — 不需外部計數器。
- **Next action 必填** — 缺值 → verification stage 2 FAIL。給 resume 提供無歧義的恢復點。
- **Evidence 不能空** — 若該 entry 描述 `in_progress → passing`，必須帶至少一個 commit hash。

### Task status 狀態機

tasks.md 每個 task 加一個 `status` sub-bullet，4 個狀態：

```
not_started → in_progress     (SDD/TDD 開始該 task)
in_progress → passing         (SDD 雙審通過 / TDD green+refactor 完成)
in_progress → blocked         (BLOCKED 訊號 / 等使用者輸入)
blocked     → in_progress     (resume 後恢復)
```

不允許的轉換：
- 任何狀態 → `not_started`（單調往前）
- `passing` → 任何狀態（已通過視為終態）
- 同時多個 task 為 `in_progress`（違反不變式）

tasks.md template 變更（writing-plans skill 內）：

````markdown
## 1. {Group name}
- [ ] 1.1 {Task description}
  - status: not_started
  - acceptance: WHEN {context} THEN {expected outcome}
  - depends on: -
  - independence: independent | serial | parallel-safe
````

寫入規則：
- `writing-plans` 建立時所有 task 預設 `not_started`
- SDD/TDD 開始 task 前改 `in_progress`、完成後改 `passing`、卡住時改 `blocked`
- `- [x]` checkbox 與 `status: passing` 視為等價，兩者必須同時設置

### Resume routing 表

| 偵測到的狀態 | 動作 |
|---|---|
| 無 in-flight change | 告知使用者，建議 `/spec-driven-dev:brainstorming` |
| 1 個 in-flight、無 `progress.md`、有 `design.md`、無 `tasks.md` | invoke `writing-plans` |
| 1 個 in-flight、無 `progress.md`、有 `tasks.md`、無 `proposal.md` | 按 tasks.md 的 optional artifacts 決定 invoke `writing-uml` / `writing-figma` / `writing-spec` |
| 1 個 in-flight、無 `progress.md`、有 `proposal.md` | 詢問使用者 SDD or TDD |
| 1 個 in-flight、有 `progress.md` | 讀最後一筆 `Stage` 與 `Transition`：<br>• `Stage: SDD` 且 transition 未到 `passing` → invoke SDD<br>• `Stage: TDD` 同上 → invoke TDD<br>• `Stage: verification` → invoke `verification-before-completion`<br>• 所有 task 都 `passing` 但無 verification-report → invoke verification |
| >1 個 in-flight | 列出讓使用者擇一，再走上述邏輯 |

## Error handling

| 情境 | 處理 |
|---|---|
| `progress.md` 缺但 tasks.md 已有 `in_progress` | 從 `git log --grep={change-id}` 推斷 evidence，重建第一筆 entry，標註 `(reconstructed)` |
| 多個 `in_progress` task | 報錯：「違反 single-in-progress 不變式：[task 1.2, task 2.1]，請手動修正後重試」，不自動修 |
| `design.md` 存在但目前 git branch ≠ change-id 對應分支 | 警告 branch mismatch，請使用者確認再繼續 |
| `openspec validate --strict` 失敗 | resume 停手，輸出 validate errors 與修復建議 |
| precheck 在上游 skill（如 brainstorming）偵測到 in-flight change | 反問「要 resume 該 change 還是開新 change？」開新會警告「舊 change 進度仍會保留，但本 session 將切換到新 change」 |
| Session N entry 寫入時發現上一筆 transition 為 `in_progress` 但這次寫入也是 `→ in_progress`（無中間 passing/blocked） | 警告：可能上一個 session 中斷未記錄結束狀態；append 一筆「Session {N-1} 補記：transition unknown, assumed interrupted」 |

## Testing

### Skill-layer 手動驗收場景

寫入 `tasks.md` 作為 acceptance criteria，每個 scenario 對應 spec 的 `#### Scenario:` 區塊：

1. **無 in-flight change → resume 建議 brainstorming**
   - 空的 `openspec/changes/`，跑 resume → 應提示「無 in-flight，建議 `/spec-driven-dev:brainstorming`」
2. **1 個 in-flight、SDD 中途 → resume 接回 SDD**
   - 給定 mock change：design.md / tasks.md（3 task：1.1 passing、1.2 in_progress、1.3 not_started）/ progress.md 末筆為 `Stage: SDD, Task: 1.2, Transition: not_started → in_progress`
   - 跑 resume → 應 invoke `subagent-driven-development` 並把 context bundle 鎖在 task 1.2
3. **多 in-flight → resume 列表讓使用者選**
   - 兩個 mock change 同時 in-flight，跑 resume → 應列表，使用者選 A 後接回 A
4. **brainstorming precheck 攔截**
   - 已有 in-flight change 的 repo 啟動 brainstorming → 應反問「resume 或開新」
5. **SDD 寫 progress.md**
   - SDD 完成一個 task → 應 append 一筆 progress entry，含 commit hash 與 next action
6. **single-in-progress 不變式檢查**
   - 手動把 tasks.md 改成兩個 in_progress，跑 SDD → 應在入口 abort 並指出衝突 task
7. **verification stage 2 缺 progress.md → FAIL**
   - 移掉 progress.md，跑 verification → Stage 2 應 FAIL 並指明缺漏

### Dogfood 驗收

本 change 自身走完整 spec-driven-dev pipeline：
- brainstorming → writing-plans → writing-uml（為 task status 狀態機畫 state diagram）→ writing-spec → SDD（建議，因為三個 component 高度獨立）→ verification

implementation 完成、verification 全綠後，才從 master 砍掉 `openspec/`（依使用者要求「用完即丟」）。在那之前 `openspec/changes/add-cross-session-harness/` 保留為工作目錄但不 commit。

## Probable next steps

走完本 design 後的下一步 skill 鏈：

- **`spec-driven-dev:writing-uml`** — 強烈建議。本 change 涉及一個狀態機（task status 4 狀態 + 不允許的轉換）與一個 routing 決策表（resume 演算法）。PlantUML state diagram 比 markdown 表格更能精確表達不變式。
- **`spec-driven-dev:writing-figma`** — 不需要。本 change 無 UI 介面。

writing-plans 階段請使用者在 optional artifacts 多選題勾選 PlantUML、不勾選 Figma。
