## Why

`spec-driven-dev` pipeline 目前缺少獨立、可在任意 checkpoint 觸發的 code review 流程。
obra/superpowers 的 `requesting-code-review` / `receiving-code-review` 兩個 skill 提供
成熟的「派工 reviewer subagent」與「技術性接收 review feedback」實務，值得納入。
移植時需確保兩個 skill 面對使用者時以**使用者輸入語言**回覆，包含 reviewer subagent
回傳的 review 內容。

## What Changes

- **code-review-skills**: 新增 `requesting-code-review` skill（含 `code-reviewer.md`
  reviewer subagent template）與 `receiving-code-review` skill 到 `spec-driven-dev`
  plugin；兩者忠實移植 superpowers 內容並加上語言指令；reviewer template 新增
  `{USER_LANGUAGE}` placeholder；`requesting-code-review` 加上輕量 pipeline 整合
  （優先引用 `openspec/changes/{change-id}/` 的 design/tasks 當 review 依據）；
  於 Claude plugin manifest 註冊兩個 skill。

## Impact

- Affected specs: `specs/code-review-skills/`
- Affected code: `plugins/spec-driven-dev/skills/requesting-code-review/`、
  `plugins/spec-driven-dev/skills/receiving-code-review/`、
  `plugins/spec-driven-dev/.claude-plugin/plugin.json`
- Breaking changes: No（純新增 skill，不改動既有 skill 行為）

## Related Artifacts

### Design
- [design.md](./design.md)
- [tasks.md](./tasks.md)
