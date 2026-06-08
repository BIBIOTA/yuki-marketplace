## Why

spec-driven-dev plugin 目前的九個 skill 在「單一連續 session」內把 brainstorming → verification 走得很完整，但缺**跨 session 入口**：當 session 被壓縮、被使用者中斷、或下次重開時，沒有任何 skill 能無歧義從 `openspec/changes/{change-id}/` 推斷「上次走到哪、下一步該做什麼」。LLM 只能 grep 整個目錄自己推測，而 tasks.md 的 checkbox 太粗、無法告訴你某個 task 是「正在做」還是「卡住」還是「未開始」。

對照 walkinglabs/learn-harness-engineering 的五子系統，spec-driven-dev 在 **State** 與 **Session Lifecycle** 兩條軸線缺最關鍵的入口。本 change 補上三件互相依賴的事：機器可讀的 task status、append-only 的 progress.md、會讀這兩者的 resume skill。

## What Changes

- **cross-session-harness**: 新增「跨 session 進度延續」能力
  - 新 skill `resume`：掃 `openspec/changes/*/` 找 in-flight change，讀 `progress.md` 末筆 entry，路由回對應的 implementation skill（SDD / TDD / verification）
  - 新 artifact `openspec/changes/{change-id}/progress.md`：SDD / TDD 在每個 task 的 status transition（`not_started → in_progress`、`in_progress → passing`、`in_progress → blocked`）後 append 一筆 Session entry，verification stage 2 把「progress.md 存在且末筆有 `Next action`」加入閘門
  - `tasks.md` 的 task entry 加 `status` sub-bullet 與 4-state machine（`not_started`、`in_progress`、`passing`、`blocked`），SDD / TDD 在入口強制「at most one `in_progress` per change」不變式
  - 上游三個 entry-point skill（`brainstorming`、`writing-plans`、`writing-spec`）入口加 in-flight precheck：偵測到既有 in-flight change 時反問「resume 還是開新？」
  - `resume` skill 在 Claude 與 Codex 兩份 plugin manifest 註冊
  - `README.md` 的 `## Plugin: spec-driven-dev` skill 表加入 `resume` 列並提及 `progress.md` 作為 cross-session anchor

## Impact

- Affected specs: `specs/cross-session-harness/`
- Affected code:
  - 新增：`plugins/spec-driven-dev/skills/resume/SKILL.md`
  - 編輯：`plugins/spec-driven-dev/skills/{brainstorming,writing-plans,writing-spec,subagent-driven-development,test-driven-development,verification-before-completion}/SKILL.md`
  - 編輯：`plugins/spec-driven-dev/.claude-plugin/plugin.json`、`plugins/spec-driven-dev/.codex-plugin/plugin.json`
  - 編輯：`README.md`（repo root）
- Breaking changes: No
  - 既有 9 個 skill 的對外行為（input / output / 對下游 skill 的 invoke 語意）不變；新增的 precheck、status flip、progress.md append 都是 additive
  - 既有的 tasks.md 沒有 `status: ...` 欄位也能繼續運作（SDD/TDD 視為 `not_started`），但 verification stage 2 從本 change 起會要求 progress.md 存在，未遷移的舊 change 走完整流程前需手動補一個初始 entry

## Related Artifacts

### Design
- [design.md](./design.md)
- [tasks.md](./tasks.md)
