---
change_id: prd-skill-requirement-oriented
doc_language: 繁體中文
---

# PRD Skill — Requirement-Oriented Output Design

**Date:** 2026-06-09
**Plugin:** spec-driven-dev
**Status:** Approved

---

## Summary

The current PRD skill generates technically-oriented content because it reads from design.md and brainstorming discussions that contain implementation details. This change adds a "Requirements Lens" distillation step before PRD generation, and strengthens writing rules to keep all sections at the requirements layer.

---

## Problem

Brainstorming discussions often include technical vocabulary (class names, API fields, Kafka topics, state machine enums). When the PRD skill generates content directly from that material, the output mirrors that vocabulary — producing Acceptance Criteria that reference `ruleConfig schema`, FR entries that name `reach.orchestrator`, and User Stories with "as a system" actors. Technical details belong in design.md, not the PRD.

---

## Design

### Step 2.5 — Requirements Lens (new intermediate step)

Inserted between "read design.md" and "generate PRD". This is an internal working artifact — not written to prd.md.

The skill extracts a requirements-perspective summary by doing three things:

1. **Identify real Actors** — only human roles (e.g., 行銷人員, 系統管理員). Remove any "as a system" subjects.
2. **Convert technical descriptions to capability statements** — translate implementation language to observable capability language:
   - "消費 domain.events via Kafka" → "系統能即時回應使用者行為事件"
   - "ruleConfig schema 驗證" → "系統防止設定錯誤的活動上線"
   - "ShedLock 保證同 cycle 僅執行一次" → "系統確保排程觸達不重複執行"
3. **Map each feature area to a business outcome** — what value does it deliver, not what it does technically.

This summary becomes the sole input lens for generating the PRD sections.

### Updated Writing Rules

Three explicit prohibitions added to the PRD skill:

**Rule 1 — Acceptance Criteria: user-observable only**
AC must describe behavior or outcomes observable by a user or business stakeholder without knowledge of system internals. Prohibited: class names, API field names, topic names, state machine enum values, third-party component names (ShedLock, Kafka, circuit breaker, etc.).

- Bad: `透過 REST API 建立 type=DISCOUNT 的活動，帶 ruleConfig、targetSpec`
- Good: `行銷人員可建立含折扣規則的活動，並指定目標受眾與觸達計畫`

**Rule 2 — Functional Requirements: capability, not implementation**
FR entries describe what the system must be *able to do*, not how it does it. No architecture terms, no component names, no data schema references.

- Bad: `FR-008: reach.orchestrator 必須是 reach.requested topic 的唯一消費者`
- Good: `FR-008: 系統必須確保同一活動的觸達請求不重複執行`

**Rule 3 — Technical Considerations: constraints only**
Section 7 may only contain constraints that *limit requirements scope* (e.g., "本期僅提供後端 API，不含管理 UI"). Do not reproduce architecture decisions from design.md. If no such constraints exist, omit the section entirely.

---

## File Changes

| File | Change |
|------|--------|
| `plugins/spec-driven-dev/skills/prd/SKILL.md` | Add Step 2.5 (Requirements Lens) to checklist; add three writing rules to the Writing Rules section |

No other files changed.

---

## Out of Scope

- No changes to PRD document structure (sections remain the same)
- No changes to brainstorming skill
- No changes to writing-plans or other downstream skills
