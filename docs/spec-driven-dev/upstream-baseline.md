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
