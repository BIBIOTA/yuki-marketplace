---
date: 2026-05-28
topic: spec-driven-dev plugin
status: design-approved
language: zh-TW
---

# Spec-Driven Development Plugin 設計文件

## Goals

建立一個 Claude Code plugin `spec-driven-dev`，提供一條完整的 spec-driven development 流水線：從一句話想法經過 brainstorming、可選的 UML / Figma 設計、OpenSpec 規範、實作（SDD 或 TDD），最後到完成前的全面驗收。

設計參考 superpowers plugin，但有三個關鍵差異：

1. **OpenSpec 為共同資料層**：所有產出都聚集在 `openspec/changes/{change-id}/`，與 OpenSpec CLI 完全相容。
2. **可選步驟（writing-uml / writing-figma）是流程的一級公民**：透過 brainstorming 探詢 + writing-plans 確認，明確分支進入。
3. **驗收涵蓋 UML 契約與 Figma 視覺**：verification-before-completion 不只驗 code，也驗 diagram 與 design 是否被實作落實。

## 流程

```
brainstorming
  └─→ writing-plans
        ├─→ writing-uml          (optional, 若 tasks.md 標記)
        ├─→ writing-figma        (optional, 若 tasks.md 標記)
        └─→ writing-spec
              ├─→ subagent-driven-development
              └─→ test-driven-development
                    └─→ verification-before-completion
                          └─→ openspec archive (user-triggered)
```

每個 skill 結尾以 HARD-GATE 控制下一步，user 未批准前不得進入。

## Plugin 結構

```
plugins/spec-driven-dev/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── brainstorming/SKILL.md
    ├── writing-plans/SKILL.md
    ├── writing-uml/
    │   ├── SKILL.md
    │   └── diagram-types.md
    ├── writing-figma/SKILL.md
    ├── writing-spec/
    │   ├── SKILL.md
    │   └── openspec-format.md
    ├── subagent-driven-development/
    │   ├── SKILL.md
    │   ├── implementer-prompt.md
    │   ├── spec-reviewer-prompt.md
    │   └── code-quality-reviewer-prompt.md
    ├── test-driven-development/SKILL.md
    └── verification-before-completion/SKILL.md
```

## OpenSpec Change 目錄結構

每個變更建立一個 change-id（kebab-case 動詞+名詞，例如 `add-user-auth`）：

```
openspec/changes/{change-id}/
├── proposal.md          # writing-spec 產出（Why / What Changes / Impact / Related Artifacts）
├── tasks.md             # writing-plans 產出（OpenSpec 格式 checklist + Optional artifacts 標記）
├── design.md            # brainstorming 產出（架構、元件、資料流、錯誤處理、測試）
├── specs/               # writing-spec 產出（capability deltas，ADDED / MODIFIED / REMOVED）
│   └── {capability}/spec.md
├── diagrams/            # writing-uml 產出（optional）
│   └── *.puml
├── designs/             # writing-figma 產出（optional）
│   ├── figma.md
│   └── screenshots/
└── verification-report.md   # verification-before-completion 產出
```

## 跨 skill 共通規則

1. **語言對應**：所有對 user 的回覆必須使用 user 的輸入語言（中文輸入 → 中文回覆）。Skill 內部模板字串保留英文以維持與 OpenSpec、PlantUML 相容。
2. **HARD-GATE**：每個 skill 結尾顯式指明下一個 skill；非流程內 skill 不應跨步呼叫。
3. **共用工作目錄**：產物統一在 `openspec/changes/{change-id}/`，change-id 由 brainstorming 階段決定。
4. **與 `superpowers:*` 同名 skill 共存**：因 plugin 命名空間隔離（`spec-driven-dev:brainstorming` vs `superpowers:brainstorming`），不衝突；本 plugin 內部不 invoke 其他 plugin 的同名 skill。
5. **Self-review 四項檢查**：寫出任何 artifact 後，立即做 placeholder / 內部一致性 / scope / ambiguity 四項自查，發現問題直接修正。
6. **User review gate**：每個產出檔寫完後，明確要求 user 審查並等待回應。

---

## Skill 1：brainstorming

**定位**：流程入口。從想法 → 設計文件 → 交棒 writing-plans。

**輸入**：user 描述的功能 / 變更想法。
**輸出**：`openspec/changes/{change-id}/design.md`

**Checklist**：

1. Detect language（沿用整個流程）
2. Explore project context（`ls`、`git log -10`、README、CLAUDE.md、是否為前端專案）
3. Scope check：請求若包含多個獨立子系統先協助分解，再針對第一個子系統 brainstorm
4. Decide change-id：kebab-case 動詞+名詞
5. Clarifying questions：一次一題，多選優先；釐清 purpose / constraints / success criteria
6. Propose 2-3 approaches 含 trade-offs 與推薦選項
7. Present design in sections，每段確認
8. 探詢 optional 步驟需求：
   - 「這個變更有複雜的元件互動、狀態機或資料流嗎？」→ 提示後續可走 writing-uml
   - 「這是前端 UI 變更，需要視覺設計稿嗎？」→ 提示後續可走 writing-figma
9. Write design doc 至 `openspec/changes/{change-id}/design.md`
10. Spec self-review（四項）
11. User review gate
12. Transition：批准後 invoke `writing-plans`

**HARD-GATE**：design.md 未獲 user 批准前，不得 invoke implementation skill、不得撰寫 production code。

---

## Skill 2：writing-plans

**定位**：把 design.md 翻譯成可執行 task list，並決定本次走哪些 optional skill。

**輸入**：`openspec/changes/{change-id}/design.md`
**輸出**：`openspec/changes/{change-id}/tasks.md`

**Checklist**：

1. Detect language（沿用）
2. Read design.md
3. 驗證 change-id 與目錄存在
4. Decompose into tasks（imperative form 標題、依賴關係、acceptance criteria 用 WHEN/THEN 句式、估計獨立性）
5. Confirm optional skills 需求（多選）：
   - `[ ] PlantUML 圖（writing-uml）— 適合：複雜流程、狀態機、跨元件互動、ER schema`
   - `[ ] Figma 設計稿（writing-figma）— 適合：前端 UI、互動原型、版本方案比較`
6. Write tasks.md（含 Optional artifacts section 標記下一步要走哪些 skill）
7. Self-review（四項）
8. User review gate
9. Transition logic：
   - 若選 writing-uml → invoke `writing-uml`
   - elif 選 writing-figma → invoke `writing-figma`
   - else → invoke `writing-spec`

**tasks.md 範本**：

```markdown
# Tasks: {change-id}

## 1. {Group name}
- [ ] 1.1 {Task description}
  - Acceptance: WHEN {context} THEN {expected outcome}
  - Depends on: -
- [ ] 1.2 ...

## Optional artifacts
- [x] PlantUML diagrams (writing-uml) — required types: sequence, state
- [ ] Figma designs (writing-figma)
```

**HARD-GATE**：tasks.md 未獲批准前不進入後續 skill。

---

## Skill 3：writing-uml

**定位**：以 PlantUML 建立 UML 圖，多選圖型，逐圖產出 `.puml`。

**輸入**：design.md、tasks.md
**輸出**：`openspec/changes/{change-id}/diagrams/{seq-no}-{type}-{topic}.puml`

**支援圖型（8 種，多選）**：

| 圖型 | 用途說明（呈現給 user） |
|---|---|
| Sequence Diagram | 物件 / 服務之間隨時間發生的訊息交換。API 流程、跨服務呼叫、認證握手。 |
| Class Diagram | 系統型別結構與關聯。Domain model、繼承、依賴關係。 |
| Use Case Diagram | 系統提供給外部角色的能力。釐清使用者意圖與系統邊界。 |
| Activity Diagram | 業務流程與決策分支。流程圖、可表達並行。 |
| State Diagram | 物件生命週期與狀態轉換。訂單狀態、認證 session、工作流。 |
| Component Diagram | 高階架構元件劃分與介面。系統 zoom-out 視圖。 |
| ER Diagram | 資料庫實體與關聯。Schema 設計、外鍵規劃。 |
| Deployment Diagram | 實體 / 雲端部署拓樸。跨環境、容器、雲服務配置。 |

**Checklist**：

1. Detect language（沿用）
2. Read design.md + tasks.md
3. Present diagram type menu（多選 + 用途說明）
4. For each selected diagram type：
   1. 詢問該圖要涵蓋的主體
   2. 草擬 PlantUML 程式碼
   3. 預覽：自動偵測本機 `plantuml`，無則 fallback 到 plantuml.com URL
   4. 修正直到 user 滿意
   5. 寫入 `diagrams/{seq-no}-{type}-{topic}.puml`
5. 更新 design.md 與 tasks.md：插入 `## Diagrams` section 列出每個 .puml 相對路徑與一行說明
6. Self-review：每個 .puml 透過 `plantuml -checkonly` pass、引用完整
7. Transition：若 tasks.md 標記 writing-figma → invoke `writing-figma`，否則 → invoke `writing-spec`

**輔助檔案**：`skills/writing-uml/diagram-types.md` — 8 種圖型的 PlantUML 語法要點與範例。

**HARD-GATE**：全部 diagram 未獲批准前不進入下一個 skill。

---

## Skill 4：writing-figma

**定位**：薄包裝 + 委托 figma:* skill；本身不重複 figma API 規則，但強制三項設計細節思考。

**輸入**：design.md、tasks.md
**輸出**：`openspec/changes/{change-id}/designs/figma.md`、`designs/screenshots/`

**前置檢查**：

1. 是否為前端專案（看 package.json / next.config / vite.config 等）；否 → 提示 user 重新確認
2. 是否安裝 figma plugin（檢查 `figma:figma-use` skill 可用）；否 → 提示安裝

**核心三項強制詢問**：

1. **版本方案（Versions）**：1 個還是多個方案（A/B）？多版本適合 UX 探索、stakeholder 比較。
2. **情境狀態（States）**：除 happy path，是否需要 Empty / Loading / Error / Disabled / Auth-state 等？
3. **共用元件（Shared Components）**：哪些應抽成 design system 共用元件？既有元件直接引用而非重造。

**Checklist**：

1. Detect language（沿用）
2. Read design.md + tasks.md
3. 前置檢查
4. 三項強制詢問
5. 決定委托哪個 figma skill：
   - 新建螢幕 / 頁面 / Modal → `figma:figma-generate-design`
   - 新建 design system / 元件庫 → `figma:figma-generate-library`
   - 編輯既有檔案 / 程式化操作 → `figma:figma-use`
   - Code Connect 映射 → `figma:figma-code-connect`
6. 生成設計稿
7. 下載截圖至 `designs/screenshots/`
8. 撰寫 `designs/figma.md`（範本見下）
9. 更新 design.md：插入 `## Designs` section 引用 figma.md
10. Transition：invoke `writing-spec`

**`designs/figma.md` 範本**：

```markdown
# Figma Designs: {change-id}

## Figma File
- File: https://www.figma.com/design/{fileKey}/...
- File key: {fileKey}

## Versions
- [v1] Frame node: {nodeId} — 描述
- [v2] Frame node: {nodeId} — 描述

## States
| State | Frame node | Screenshot |
|---|---|---|
| Happy path | {nodeId} | screenshots/01-happy.png |
| Empty | {nodeId} | screenshots/02-empty.png |
| Error | {nodeId} | screenshots/03-error.png |

## Shared Components Used
- `Button/Primary` (existing) — 引用
- `Card/Compact` (new) — 本次新建，已加入 design system

## Acceptance Criteria
- 實作螢幕需符合 v1 frame {nodeId} 的視覺
- Empty / Error state 需與對應 frame 一致
```

**HARD-GATE**：designs/figma.md 未獲批准前不 invoke writing-spec。

---

## Skill 5：writing-spec

**定位**：把所有產出整合成 OpenSpec 規範的 proposal.md 與 specs/{capability}/spec.md，並用 OpenSpec CLI 驗證。

**輸入**：`openspec/changes/{change-id}/` 下所有現有檔案
**輸出**：
- `openspec/changes/{change-id}/proposal.md`
- `openspec/changes/{change-id}/specs/{capability}/spec.md`（一個或多個）

**前置檢查**：

1. OpenSpec CLI 是否安裝（`which openspec`）；否 → 引導安裝
2. 專案是否已 `openspec init`；否 → 引導執行

**Checklist**：

1. Detect language（沿用）
2. Read all change artifacts（design.md / tasks.md / diagrams / designs）
3. 識別 capabilities：依 design.md 拆解為 OpenSpec capability 單位
4. 撰寫 `proposal.md`
5. 撰寫 `specs/{capability}/spec.md`（ADDED/MODIFIED/REMOVED Requirements + `#### Scenario:` WHEN/THEN）
6. 建立 artifact 關聯（強制）：
   - proposal.md 的 `## Related Artifacts` 列出全部 diagrams 與 designs
   - 每個 capability spec.md 的相關 requirement 下加註 `> See: ../../diagrams/...` 或 `> See: ../../designs/figma.md#...`
7. 執行 `openspec validate {change-id} --strict` 必須 pass
8. Self-review（四項）+ 確認所有 diagram / design 都至少被一個 requirement 引用
9. User review gate
10. Transition：詢問 user「接下來走 SDD 還是 TDD？」→ invoke 對應 skill

**proposal.md 範本**：

```markdown
## Why
{動機與當前痛點}

## What Changes
- **{capability}**: {變更摘要}

## Impact
- Affected specs: `specs/{capability}/`
- Affected code: {目錄或檔案範圍}
- Breaking changes: {Yes/No + 詳述}

## Related Artifacts
### Design
- [design.md](./design.md)
- [tasks.md](./tasks.md)

### Diagrams
- [Sequence: Login Flow](./diagrams/01-sequence-login-flow.puml)

### Figma Designs
- [Figma reference](./designs/figma.md)
```

**`specs/{capability}/spec.md` 範本**：

```markdown
## ADDED Requirements

### Requirement: User shall be able to log in with email + password
The system SHALL authenticate users via email and password credentials.

#### Scenario: Successful login
- **WHEN** a user submits valid email and password
- **THEN** the system returns a session token
- **AND** redirects to the dashboard

> See: ../../diagrams/01-sequence-login-flow.puml
> See: ../../designs/figma.md#happy-path
```

**輔助檔案**：`skills/writing-spec/openspec-format.md` — OpenSpec 格式規則、`#### Scenario:` 句法、ADDED/MODIFIED/REMOVED 用法、validate --strict 常見錯誤排查。

**HARD-GATE**：

1. 所有存在的 diagram / design 都必須在 spec 中至少被一個 requirement 透過 `> See:` 引用。
2. `openspec validate --strict` 必須 pass。
3. User 批准前不得 invoke SDD / TDD。

---

## Skill 6：subagent-driven-development

**定位**：對齊 superpowers/SDD；讀 `openspec/changes/{change-id}/`，分派 subagent 實作，驗收 task 對應的 spec / diagrams / designs。

**輸入**：`openspec/changes/{change-id}/`

**Checklist**：

1. Detect language（沿用）
2. Read change artifacts（tasks.md、specs/、瀏覽 diagrams / designs）
3. 規劃 subagent 分派：tasks.md 取出獨立 tasks，每組指派一個 implementer subagent
4. 建立 subagent context bundle：task 描述 + acceptance criteria + 對應 spec requirement + 引用的 diagram .puml 路徑 + 引用的 design figma.md section
5. 三輪 review 流程：
   - **Implementer**（`implementer-prompt.md`）：寫 code
   - **Spec reviewer**（`spec-reviewer-prompt.md`）：對照 spec.md + diagrams + designs 確認實作符合
   - **Code quality reviewer**（`code-quality-reviewer-prompt.md`）：審 code quality
6. 合併並更新 tasks.md（勾選完成 task）
7. Transition：全部 task 完成後 invoke `verification-before-completion`

**Subagent prompt 差異 vs superpowers**：

- `implementer-prompt.md` 新增：
  - 「若 task 對應 diagram (`> See: ../../diagrams/*.puml`)，先讀懂圖再實作；圖中的訊息順序 / 狀態轉換是實作的契約。」
  - 「若 task 對應 figma 設計 (`> See: ../../designs/figma.md#...`)，先讀 designs/figma.md 對應 section 與 screenshot，視覺需 pixel-aware 對齊。」
- `spec-reviewer-prompt.md` 新增：
  - 「審查時除了對照 `specs/{capability}/spec.md` 的 requirement，也需驗證對應 diagram 與 design artifact 中的契約是否被遵守。」

**HARD-GATE**：每個 task 必須通過 spec-reviewer + code-quality-reviewer 雙審才能 mark complete。

---

## Skill 7：test-driven-development

**定位**：對齊 superpowers/TDD；acceptance criteria 來源是 `specs/{capability}/spec.md` 的 `#### Scenario:`。

**輸入**：`openspec/changes/{change-id}/`

**Checklist**：

1. Detect language（沿用）
2. Read change artifacts
3. For each task in tasks.md：
   1. 找到對應的 spec requirement 與 scenarios
   2. **Red**：把 scenarios 轉成 failing tests（test 名稱對應 scenario 名）
   3. **Green**：寫最小實作讓 test pass
   4. **Refactor**：重構，tests 仍 pass
   5. 驗證 diagram / design 對應：
      - 引用 diagram → 增加 integration test 驗證流程順序 / 狀態轉換
      - 引用 figma design → 標記需要 visual / e2e 驗證（交由 verification skill）
4. 更新 tasks.md
5. Transition：全部 task 完成後 invoke `verification-before-completion`

**TDD 紀律規則**：

- 不允許先寫 implementation 再補 test
- 不允許跳過 Red 階段
- Test 名稱必須對應 `#### Scenario:` 名稱（讓 spec ↔ test 可追溯）

**HARD-GATE**：每個 task 必須有對應 failing test 證據（commit / log）才能 mark complete。

---

## Skill 8：verification-before-completion

**定位**：對齊 superpowers/verification；多兩道驗收（UML 契約、Figma 視覺）。原則：**evidence before assertions**。

**輸入**：`openspec/changes/{change-id}/` + 實作 code
**輸出**：`openspec/changes/{change-id}/verification-report.md`

**Checklist**（依序執行，任一階段 fail 整體 fail）：

### 階段 1：Code-level verification

1. Lint / type check 全 pass
2. Unit + integration tests pass（截下實際輸出）
3. 新增 tests 對應 spec scenarios（grep `#### Scenario:` 名稱 vs test 名稱）
4. Manual smoke test（前端專案）：dev server + golden path + edge cases

### 階段 2：Spec verification

5. `openspec validate {change-id} --strict` pass
6. tasks.md 全部勾選；未勾選需明確 deferred reason

### 階段 3：Diagram verification（若 `diagrams/` 存在）

7. 逐圖比對：
   - **Sequence**：圖中訊息順序 vs 實作函式呼叫順序
   - **State**：圖中狀態與轉換 vs 實作 state machine
   - **Class**：圖中型別 vs 實作 interface / class / type alias
   - **ER**：圖中實體與關聯 vs 資料庫 schema migration
   - **Activity / Use case / Component / Deployment**：人工檢視，提示 user 確認
8. 標記每張圖 pass / fail / manual-review

### 階段 4：Design verification（若 `designs/figma.md` 存在）

9. 逐 state 比對：啟動 dev server / storybook，截下實作畫面，與 figma.md 引用的 screenshot 並排，列出差異
10. 共用元件比對：figma.md 標記為 existing 的元件，實作必須直接 import，不得重造
11. 標記每個 state pass / fail

### 階段 5：彙整

12. 撰寫 `verification-report.md`（範本見下）
13. 全 pass → 提示 user 可 `openspec archive {change-id}`
14. 有 fail → 列出失敗項，回對應 skill：
    - code fail → 回 SDD / TDD
    - spec fail → 回 writing-spec
    - diagram fail → 回 writing-uml
    - design fail → 回 writing-figma

**`verification-report.md` 範本**：

```markdown
# Verification Report: {change-id}

Date: {date}
Verifier: {model}

## Summary
- Code: {status}
- Spec: {status}
- Diagrams: {status}
- Designs: {status}

## Code Evidence
{actual test output}

## Diagram Verification
| File | Type | Status | Notes |
|---|---|---|---|

## Design Verification
| State | Figma node | Status | Diff |
|---|---|---|---|

## Next Actions
- ...
```

**HARD-GATE**：

1. 任一階段 fail → 整體 fail，回對應 skill 修補。
2. verification-report.md 未寫 → 不得宣告完成。
3. 全 pass 才提示 `openspec archive`。

---

## 後續步驟

本設計通過後，invoke `writing-plans` 建立實作計畫。實作計畫應拆分為：

1. Plugin scaffold（`.claude-plugin/plugin.json` + 目錄）
2. 各 skill SKILL.md 與輔助檔案（依本文件 § 各 section）
3. Smoke test：以一個 toy change（例如 `add-hello-endpoint`）走完整條流水線驗證
4. 在 marketplace `.claude-plugin/marketplace.json`（若存在）註冊新 plugin
