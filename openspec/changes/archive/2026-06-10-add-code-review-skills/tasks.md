# Tasks: add-code-review-skills

## 1. requesting-code-review skill
- [x] 1.1 移植 `requesting-code-review/SKILL.md`（忠實移植 + `<language>` 區塊 + 輕量 pipeline 整合）
  - Acceptance: WHEN 建立 `plugins/spec-driven-dev/skills/requesting-code-review/SKILL.md` THEN 內容忠實移植自 superpowers，frontmatter `name: requesting-code-review` 且開頭結尾有 `---` AND 在 frontmatter 之後正文之前含 `<language>` 區塊 AND 「Integration with Workflows」對應到 `spec-driven-dev:subagent-driven-development` 並說明與 `spec-driven-dev:verification-before-completion` 的關係 AND 「How to Request」說明填 template 前以對話語言填入 `{USER_LANGUAGE}`、且 `{PLAN_OR_REQUIREMENTS}` 在 `openspec/changes/{change-id}/` 存在時優先引用其 design.md / tasks.md
  - Depends on: -
  - Independence: independent
  - status: passing
- [x] 1.2 移植 `requesting-code-review/code-reviewer.md`（reviewer template + `{USER_LANGUAGE}` placeholder）
  - Acceptance: WHEN 建立 `plugins/spec-driven-dev/skills/requesting-code-review/code-reviewer.md` THEN 內容忠實移植自 superpowers AND prompt 開頭含一行 `Write all review output (Strengths, Issues, Assessment, etc.) in {USER_LANGUAGE}.` AND 文末 placeholder 清單新增 `{USER_LANGUAGE}` 說明
  - Depends on: 1.1
  - Independence: serial
  - status: passing

## 2. receiving-code-review skill
- [x] 2.1 移植 `receiving-code-review/SKILL.md`（忠實移植 + `<language>` 區塊）
  - Acceptance: WHEN 建立 `plugins/spec-driven-dev/skills/receiving-code-review/SKILL.md` THEN 內容忠實移植自 superpowers，frontmatter `name: receiving-code-review` 且開頭結尾有 `---` AND 在 frontmatter 之後正文之前含 `<language>` 區塊 AND 正文（response pattern、forbidden responses、push back 等）保持通用、不綁定 pipeline
  - Depends on: -
  - Independence: independent
  - status: passing

## 3. 註冊
- [x] 3.1 在 Claude plugin manifest 註冊兩個 skill
  - Acceptance: WHEN 編輯 `plugins/spec-driven-dev/.claude-plugin/plugin.json` THEN `skills` array 新增 `./skills/requesting-code-review` 與 `./skills/receiving-code-review` AND JSON 合法 AND `.codex-plugin/plugin.json` 保持 `"./skills/"` 目錄掃描、不修改 AND 不手動更動 `version`
  - Depends on: 1.1, 2.1
  - Independence: serial
  - status: passing

## 4. 驗證
- [x] 4.1 人工驗證 skill 與註冊正確
  - Acceptance: WHEN 完成 1.x–3.x THEN 兩個 SKILL.md frontmatter 完整且開頭結尾有 `---` AND `.claude-plugin/plugin.json` 通過 `python3 -m json.tool` AND 兩個 SKILL.md 含 `<language>` 區塊 AND `code-reviewer.md` 含 `{USER_LANGUAGE}` placeholder 與 SKILL.md 對應填寫說明 AND `code-reviewer.md` placeholder 清單已含 `{USER_LANGUAGE}`
  - Depends on: 1.1, 1.2, 2.1, 3.1
  - Independence: serial
  - status: passing

## Optional artifacts
- [ ] PlantUML diagrams (spec-driven-dev:writing-uml)
- [ ] Figma designs (spec-driven-dev:writing-figma)
