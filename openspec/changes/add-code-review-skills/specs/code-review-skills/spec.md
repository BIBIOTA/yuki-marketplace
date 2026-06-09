## ADDED Requirements

### Requirement: requesting-code-review skill 移植並以使用者語言回覆
系統 SHALL 在 `spec-driven-dev` plugin 提供 `requesting-code-review` skill，忠實移植自
superpowers，並 SHALL 確保所有面向使用者的回覆使用使用者輸入語言。

#### Scenario: Skill 檔案結構與語言指令
- **WHEN** 建立 `plugins/spec-driven-dev/skills/requesting-code-review/SKILL.md`
- **THEN** frontmatter `name` 為 `requesting-code-review` 且開頭與結尾皆有 `---` 分隔線
- **AND** 在 frontmatter 之後、正文之前含 `<language>` 區塊，要求所有 user-facing 回覆使用使用者輸入語言、內部字串（路徑、程式碼、git 指令、OpenSpec keyword）維持英文
- **AND** 正文內容忠實移植自 superpowers `requesting-code-review`

#### Scenario: 輕量 pipeline 整合
- **WHEN** 使用者在存在 `openspec/changes/{change-id}/` 的情況下請求 review
- **THEN** SKILL.md 的「How to Request」指示 `{PLAN_OR_REQUIREMENTS}` 優先引用該目錄的 `design.md` / `tasks.md`
- **AND** 「Integration with Workflows」將 `Subagent-Driven Development` 對應到 `spec-driven-dev:subagent-driven-development` 並說明與 `spec-driven-dev:verification-before-completion` 的關係（review 為 verification 前的 early check，不取代它）

### Requirement: reviewer subagent template 以使用者語言產出 review
系統 SHALL 提供 `code-reviewer.md` reviewer subagent template，並 SHALL 透過
`{USER_LANGUAGE}` placeholder 確保 subagent 回傳的 review 內容使用使用者語言。

#### Scenario: template 含語言 placeholder
- **WHEN** 建立 `plugins/spec-driven-dev/skills/requesting-code-review/code-reviewer.md`
- **THEN** 內容忠實移植自 superpowers reviewer prompt template
- **AND** prompt 開頭含一行 `Write all review output (Strengths, Issues, Assessment, etc.) in {USER_LANGUAGE}.`
- **AND** 文末 placeholder 清單新增 `{USER_LANGUAGE}` 說明

#### Scenario: requesting skill 指示填入語言
- **WHEN** `requesting-code-review/SKILL.md` 說明如何 dispatch reviewer subagent
- **THEN** 指示在填寫 template 前以當前對話語言填入 `{USER_LANGUAGE}`

### Requirement: receiving-code-review skill 移植並以使用者語言回覆
系統 SHALL 在 `spec-driven-dev` plugin 提供 `receiving-code-review` skill，忠實移植自
superpowers，並 SHALL 確保所有面向使用者的回覆使用使用者輸入語言。

#### Scenario: Skill 檔案結構與語言指令
- **WHEN** 建立 `plugins/spec-driven-dev/skills/receiving-code-review/SKILL.md`
- **THEN** frontmatter `name` 為 `receiving-code-review` 且開頭與結尾皆有 `---` 分隔線
- **AND** 在 frontmatter 之後、正文之前含 `<language>` 區塊
- **AND** 正文（response pattern、forbidden responses、push back 等）忠實移植自 superpowers 且保持通用、不綁定 pipeline

### Requirement: 兩個 skill 於 Claude plugin manifest 註冊
系統 SHALL 在 `spec-driven-dev` 的 Claude plugin manifest 註冊兩個新 skill，且 SHALL
不手動更動 plugin version。

#### Scenario: manifest 註冊與相容性
- **WHEN** 編輯 `plugins/spec-driven-dev/.claude-plugin/plugin.json`
- **THEN** `skills` array 新增 `./skills/requesting-code-review` 與 `./skills/receiving-code-review`
- **AND** JSON 通過 `python3 -m json.tool` 驗證
- **AND** `.codex-plugin/plugin.json` 維持 `"./skills/"` 目錄掃描、不修改
- **AND** `version` 欄位不手動更動（交由 CI 自動 bump）
