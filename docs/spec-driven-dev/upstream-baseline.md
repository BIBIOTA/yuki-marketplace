# spec-driven-dev upstream baseline

This document records the upstream version baseline that `spec-driven-dev` was originally grounded on, so later reviews can compare upstream changes against the historical starting point instead of only against the current local plugin state.

## Baseline method

- `spec-driven-dev` initial scaffold commit:
  - Repository: `BIBIOTA/yuki-marketplace`
  - Commit: `b2ab7a31ae5d99fbd0b7450c6b446fef2609e411`
  - Commit time: `2026-05-28 15:00:03 +0800`
  - Subject: `feat: scaffold spec-driven-dev plugin`
- Upstream baseline definition:
  - For each upstream source, use the most recent commit at or before the `spec-driven-dev` scaffold commit time.

## Recorded upstream baselines

### obra/superpowers

- Baseline commit: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- Commit time: `2026-05-04 15:05:01 -0700`
- Subject: `Release v5.1.0 (#1468)`
- Repository: `https://github.com/obra/superpowers`

### Fission-AI/openspec

- Baseline commit: `11b269061897b011075a984c6c95d970a5533a66`
- Commit time: `2026-05-28 06:54:51 +0000`
- Subject: `test: split slow workspace open CI case (#1134)`
- Repository: `https://github.com/Fission-AI/openspec`

## Intended use

- Weekly upstream review jobs should read the machine-readable baseline file at `plugins/spec-driven-dev/upstream-baseline.json`.
- Review logic should compare:
  - `superpowers`: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7..current`
  - `openspec`: `11b269061897b011075a984c6c95d970a5533a66..current`
- The goal is to identify key upstream differences across that version gap that are relevant to `spec-driven-dev`, then judge whether they should be absorbed into the plugin.
- Before flagging a difference, cross-check it against the **Absorbed upstream changes** log below — already-absorbed items should not be re-raised.

## Absorbed upstream changes

Log of upstream changes that have been reviewed and deliberately absorbed into `spec-driven-dev`, so later reviews do not re-flag them.

### 2026-07-09 — superpowers v6.0.0

- **Single reviewer / dual verdict** — merged the separate `spec-reviewer-prompt.md` and `code-quality-reviewer-prompt.md` in `subagent-driven-development` into one `task-reviewer-prompt.md` that returns a spec-compliance verdict and a code-quality verdict in a single read-only pass. The SDD review loop is now two-stage (implementer → task-reviewer).
- **Plan task contract** — `writing-plans` now captures cross-task **Global Constraints** and a per-task **Interfaces** field, and adds **task right-sizing** guidance. Both new fields flow through the `subagent-driven-development` context bundle to implementers and the task-reviewer.

### Reviewed but NOT absorbed (not applicable to this plugin's architecture)

- **superpowers v6.0.3 `.git/sdd` → `.superpowers/sdd`** — `spec-driven-dev` never wrote scratch/ledger state under `.git/`; progress lives in `openspec/changes/{change-id}/progress.md`. No change needed.
- **superpowers v6.1.1 Codex `hooks: {}`** — this marketplace's `.codex-plugin/plugin.json` is metadata-only with no SessionStart hook, so the auto-discovery conflict does not apply.
- **OpenSpec OPSX quick-path narrative (`/opsx:new` → `/opsx:propose` etc.)** — `spec-driven-dev` runs its own skill pipeline and only invokes `openspec validate` / `openspec archive`; it is not built on the `opsx` slash-command workflow.
- **OpenSpec Stores beta** — direction noted; kept under observation rather than absorbed while the CLI/JSON shape is still beta.
