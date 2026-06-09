## Why
PRD skill 從 design.md 與 brainstorming 討論素材直接生成內容，導致輸出保留了大量技術詞彙（class 名稱、API field、Kafka topic、狀態機 enum）。PRD 應是需求端文件，技術細節應留在 design.md；目前的輸出讓 stakeholder 難以閱讀，也讓 AC 無法作為驗收基準。

## What Changes
- **prd-skill**: 在生成 PRD 前插入「Requirements Lens」提煉步驟，強制切換至需求視角；並新增三條 writing rules 禁止技術細節滲入 AC、FR 與 Technical Considerations。

## Impact
- Affected specs: `specs/prd-skill/`
- Affected code: `plugins/spec-driven-dev/skills/prd/SKILL.md`
- Breaking changes: No（現有 prd.md 結構不變，只影響生成內容品質）

## Related Artifacts
### Design
- [design.md](./design.md)
- [tasks.md](./tasks.md)
