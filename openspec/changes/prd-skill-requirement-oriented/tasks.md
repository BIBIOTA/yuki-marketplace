# Tasks: prd-skill-requirement-oriented

## 1. 插入 Requirements Lens 步驟

- [x] 1.1 在 SKILL.md checklist 的步驟 3（Ask clarifying questions）之前插入 Step 2.5
  - Acceptance: WHEN 使用者呼叫 PRD skill THEN checklist 中出現「Requirements Lens」步驟，位於「Confirm change-id」與「Ask clarifying questions」之間
  - Depends on: -
  - Independence: independent

- [x] 1.2 在 Step 2.5 說明內容中，寫明三件事：識別真實 Actor、將技術描述轉為能力陳述、對應業務成果
  - Acceptance: WHEN 閱讀 Step 2.5 說明 THEN 可清楚看到三個子項目，各附帶一個具體轉換範例
  - AND 說明文字中標注「此摘要為內部工作產物，不寫入 prd.md」
  - Depends on: 1.1
  - Independence: serial

## 2. 新增 Writing Rules

- [x] 2.1 在 SKILL.md 的「Writing rules」區塊新增 Rule 1：AC 只能描述使用者可觀測行為
  - Acceptance: WHEN 閱讀 Writing rules THEN 可看到明確禁止清單（class 名稱、API field 名稱、topic 名稱、狀態機 enum 值、第三方元件名）
  - AND 附有一個「Bad」與一個「Good」範例
  - Depends on: -
  - Independence: independent

- [x] 2.2 新增 Rule 2：FR 描述能力，不描述實作
  - Acceptance: WHEN 閱讀 Writing rules THEN 可看到 FR 的「Bad」（含元件名）與「Good」（純能力陳述）範例
  - Depends on: 2.1
  - Independence: serial

- [x] 2.3 新增 Rule 3：Technical Considerations 只記錄影響需求範圍的約束
  - Acceptance: WHEN 閱讀 Writing rules THEN 可看到 Rule 3 說明：Section 7 只能記錄限制需求範圍的約束；若無此類約束則省略整個 section
  - Depends on: 2.2
  - Independence: serial

## Optional artifacts
- [ ] PlantUML diagrams (spec-driven-dev:writing-uml)
- [ ] Figma designs (spec-driven-dev:writing-figma)
