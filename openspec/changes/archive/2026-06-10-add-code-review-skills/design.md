---
change_id: add-code-review-skills
doc_language: 繁體中文
---

# 設計：新增 requesting-code-review / receiving-code-review skills

## 目的

把 obra/superpowers repo 的兩個 code-review skill 移植進本 marketplace 的
`spec-driven-dev` plugin，並確保它們在面對使用者時**以使用者輸入語言為準**回覆，
包含 `requesting-code-review` 所派工的 reviewer subagent 回傳內容。

來源：
- https://github.com/obra/superpowers — `skills/requesting-code-review`
- https://github.com/obra/superpowers — `skills/receiving-code-review`

## 範圍

- **In scope**：新增兩個 skill 目錄、語言指令、reviewer template 的語言 placeholder、
  輕量 spec-driven-dev pipeline 整合、Claude plugin.json 註冊。
- **Out of scope**：修改既有 `subagent-driven-development` /
  `verification-before-completion` skill 的行為；全面繁中改寫 skill 正文；
  手動 bump plugin version。

## 架構：檔案結構與放置

```
plugins/spec-driven-dev/skills/
├── requesting-code-review/
│   ├── SKILL.md          # 忠實移植 + <language> 區塊 + 輕量 pipeline 整合
│   └── code-reviewer.md  # reviewer subagent template + {USER_LANGUAGE} placeholder
└── receiving-code-review/
    └── SKILL.md          # 忠實移植 + <language> 區塊
```

- skill 正文採「忠實移植」：保留 superpowers 原始英文內容（forbidden responses、
  red flags 等精準措辭不改寫），只新增語言指令與 pipeline 整合文字。
- frontmatter（`name` / `description`）維持英文原樣，符合既有 skill 慣例，
  且開頭/結尾都有 `---` 分隔線（CLAUDE.md 規則）。

## 元件

### 1. requesting-code-review/SKILL.md
- 移植自 superpowers，frontmatter `name: requesting-code-review`。
- 開頭加 `<language>` 區塊（見下）。
- 「How to Request」步驟補上：填 `code-reviewer.md` template 前，以當前對話語言填入
  `{USER_LANGUAGE}`；`{PLAN_OR_REQUIREMENTS}` 若存在 `openspec/changes/{change-id}/`
  則優先引用其 `design.md` / `tasks.md`。
- 「Integration with Workflows」把 `Subagent-Driven Development` 對應到
  `spec-driven-dev:subagent-driven-development`，並說明與
  `spec-driven-dev:verification-before-completion` 的關係（review 是 verification
  前的 early check，不取代它）。

### 2. requesting-code-review/code-reviewer.md
- 移植 reviewer subagent prompt template。
- 新增 `{USER_LANGUAGE}` placeholder，並在 prompt 開頭加一行：
  `Write all review output (Strengths, Issues, Assessment, etc.) in {USER_LANGUAGE}.`
- 文末 placeholder 清單同步加入 `{USER_LANGUAGE}` 說明。

### 3. receiving-code-review/SKILL.md
- 移植自 superpowers，frontmatter `name: receiving-code-review`。
- 開頭加 `<language>` 區塊。
- 正文（response pattern、forbidden responses、push back 等）忠實保留，
  不做 pipeline 綁定（保持通用）。

### 4. 註冊
- 在 `plugins/spec-driven-dev/.claude-plugin/plugin.json` 的 `skills` array
  新增 `./skills/requesting-code-review` 與 `./skills/receiving-code-review`。
- `.codex-plugin/plugin.json` 使用 `"./skills/"` 目錄掃描，自動涵蓋，無需修改。

## 語言指令設計（核心需求）

每個 SKILL.md 在 frontmatter 之後、正文之前加入：

```markdown
<language>
All user-facing replies in this skill MUST use the user's input language.
Internal strings (file paths, code blocks, git commands, OpenSpec keywords)
stay in English.
</language>
```

reviewer subagent 是獨立 context、看不到對話語言，因此透過 `code-reviewer.md`
的 `{USER_LANGUAGE}` placeholder 注入語言要求，由 requesting 端在 dispatch 前填入。
這確保 requesting 端回覆與 reviewer 回傳內容都使用使用者語言。

## 資料流

```
使用者（語言 L）
  → requesting-code-review（以 L 回覆，<language> 區塊保證）
    → 填 code-reviewer.md，USER_LANGUAGE = L
      → reviewer subagent（以 L 產出 review）
    → requesting 端整理 review（仍以 L 回覆）

使用者收到 review feedback
  → receiving-code-review（以 L 回覆，<language> 區塊保證）
```

## 錯誤處理 / 邊界

- 若無法判定使用者語言：沿用對話既有語言（與其他 yuki skill 一致），不預設英文。
- 若 `openspec/changes/{change-id}/` 不存在：`{PLAN_OR_REQUIREMENTS}` 退回原始用法
  （plan 路徑 / task 文字 / 自由描述），整合為「優先」而非「強制」。
- 已知重疊：`subagent-driven-development` 已內含 reviewer 派工；
  `requesting-code-review` 提供更通用、可在任意 checkpoint 觸發的 review 流程，
  兩者互補不衝突。

## 測試 / 驗證

無可執行測試（markdown skill），以人工檢查為主：
1. 兩個 SKILL.md frontmatter 完整、開頭結尾有 `---`。
2. `.claude-plugin/plugin.json` 新增兩條路徑且 JSON 合法（`python3 -m json.tool`）。
3. 兩個 SKILL.md 含 `<language>` 區塊；`code-reviewer.md` 含 `{USER_LANGUAGE}`
   placeholder 且 SKILL.md 有對應填寫說明。
4. `code-reviewer.md` placeholder 清單已加入 `{USER_LANGUAGE}`。

## 版本

不手動改 `version`（CI merge master 時自動 bump patch）。Codex version 與 Claude
一致（皆 0.1.0），不需動。

## Probable next steps

- UML（`spec-driven-dev:writing-uml`）：**不需要** — 無複雜元件互動／狀態機／資料流。
- Figma（`spec-driven-dev:writing-figma`）：**不需要** — 非前端 UI 變更。
