---
name: system-debugging
description: Use when investigating bugs, failed verification, flaky behavior, UI regressions, data inconsistencies, or any unexpected behavior in a spec-driven-dev change - requires root-cause investigation before fixes, discovers concrete observation methods such as browser inspection, logs, API calls, database queries, and reproducible steps, then records evidence in openspec/changes/{change-id}/debugging-report.md.
---

# System Debugging

Find the root cause before changing implementation. This skill turns a vague bug report into observed facts, reliable reproduction steps, and a falsifiable hypothesis.

<HARD-GATE>
Do NOT propose or implement a fix until you have:

1. Identified at least one observation method for every relevant layer.
2. Attempted to reproduce the issue with concrete steps.
3. Captured evidence showing where the behavior diverges from expected behavior.
4. Written or updated `openspec/changes/{change-id}/debugging-report.md`.

If the issue cannot be reproduced, do not guess. Gather more observations, document what was tried, and state what evidence is missing.

**Language:** All user-facing replies in this skill MUST use the user's input language; internal file paths, commands, and OpenSpec keywords stay in English. Reuse the language detected in `design.md`, `tasks.md`, or the user's first message.
</HARD-GATE>

## Checklist

Complete each item in order:

1. **Detect language** - reuse the language from existing change artifacts or the user's first message.
2. **Identify change context** - locate `openspec/changes/{change-id}/`; if no change-id exists, create the debugging report under `openspec/changes/debug-{short-slug}/debugging-report.md` and clearly mark it as a debugging-only artifact.
3. **Read expected behavior** - read relevant `design.md`, `tasks.md`, `specs/*/spec.md`, verification reports, failing test output, and the user's bug report.
4. **Map system layers** - list the layers that could participate in the bug: UI/browser, frontend state, network/API, backend service, database, cache, queue/worker, file storage, external provider, CI/runtime environment.
5. **Discover observation methods** - for every relevant layer, find the concrete command, tool, URL, query, log location, or browser action that can reveal state.
6. **Reproduce** - run the smallest reliable reproduction. If it is browser-visible, use browser/devtools evidence. If it is data-related, inspect the actual data store. If it is integration-related, observe both sides of the boundary.
7. **Trace data flow** - follow the bad value or missing event backward from the symptom until the first incorrect state, missing transition, or failed boundary is found.
8. **Compare with a working reference** - find a similar passing test, route, screen, query, previous commit, or documented expected flow and list the meaningful differences.
9. **State one hypothesis** - write: "I think the root cause is X because evidence Y." Test one variable at a time.
10. **Write `debugging-report.md`** - include the template below with commands, observations, screenshots/URLs if applicable, database queries if applicable, and current hypothesis.
11. **Transition** - after root cause is established, return to the appropriate implementation skill:
    - Spec or acceptance criteria wrong -> `spec-driven-dev:writing-spec`
    - Implementation bug with approved spec -> `spec-driven-dev:test-driven-development` or `spec-driven-dev:subagent-driven-development`
    - Verification method wrong or incomplete -> `spec-driven-dev:verification-before-completion`

## Observation Method Discovery

Use this as a prompt to find concrete observation surfaces. Do not stop at "check the UI" or "check the DB"; identify the actual way to observe it in this repo.

### Browser / UI

- Find how to run the app (`package.json`, README, docker compose, Makefile).
- Start or attach to the real dev server.
- Use browser automation or DevTools to inspect:
  - rendered DOM text and visible state
  - console errors and warnings
  - network requests, status codes, request payloads, and response bodies
  - localStorage/sessionStorage/cookies when relevant
  - screenshots for layout, empty states, loading states, and error states
- Record the exact URL, viewport, user steps, and observed result.

### API / Backend

- Find route definitions, OpenAPI docs, controllers/handlers, service logs, and test fixtures.
- Exercise the API directly with `curl`, HTTP client tests, or framework test tools.
- Capture request, response, status code, correlation/request IDs if available, and backend logs for the same request.
- Compare browser network evidence against direct API evidence to locate frontend-vs-backend boundaries.

### Database / Persistence

- Detect the datastore from config files, env examples, ORM settings, migrations, compose files, or connection helpers.
- Prefer read-only inspection first:
  - SQL: list relevant tables, describe schema, query the specific record IDs involved.
  - ORM shell: load the same model/entity used by the application.
  - Document store: query by the same key used by the request.
- Capture the exact query and result shape. Redact secrets and tokens.
- If containers are used, identify the actual running container and database name before querying.
- Do not mutate data unless the reproduction explicitly requires a controlled fixture; document any setup and cleanup.

### Background Work / Async Boundaries

- Inspect job queues, workers, scheduled tasks, message brokers, cache entries, webhooks, and retry/dead-letter logs.
- Verify both enqueue and consume sides. Record job IDs, payload shape, timestamps, and worker logs.

### Environment / Build / CI

- Compare local, container, preview, and CI environments when behavior differs.
- Capture dependency versions, env var presence (not secret values), build output, feature flags, and runtime config.
- For flaky failures, collect timing, retries, seed values, and resource constraints.

## Reproduction Rules

- Use the smallest path that still triggers the bug.
- Write reproduction steps as commands or numbered UI actions that another agent can run.
- If the bug is intermittent, run repeated attempts and record pass/fail counts.
- If reproduction depends on data, record fixture creation and the identifying record IDs.
- If reproduction depends on user permissions, roles, locale, timezone, viewport, or feature flags, include them explicitly.

## Report Template

Write this file to `openspec/changes/{change-id}/debugging-report.md`:

````markdown
# Debugging Report: {change-id}

Date: {YYYY-MM-DD}
Debugger: {model name or session id}

## Symptom
- Reported behavior:
- Expected behavior:
- Impact:

## Reproduction
- Status: reproduced | not reproduced | intermittent
- Steps:
- Environment:
- Test data / record IDs:

## Observation Plan
| Layer | Observation method | Evidence captured |
|---|---|---|
| Browser/UI |  |  |
| API/backend |  |  |
| Database/persistence |  |  |
| Background/async |  |  |
| Environment/build |  |  |

## Evidence
```text
{commands, logs, query results, network observations, screenshot paths}
```

## Data Flow Trace
- Symptom observed at:
- First incorrect state found at:
- Boundary where expected became actual:

## Working Reference
- Reference:
- Meaningful differences:

## Hypothesis
I think the root cause is {X} because {Y evidence}.

## Next Action
- Route to:
- Minimal fix/test direction:
```
````

## Stop Conditions

Stop and ask for user input only when:

- Required credentials or production-only access are unavailable.
- Observing the real system would mutate production data or expose sensitive data.
- The same hypothesis fails three times and the architecture or requirements need reconsideration.

Otherwise, continue gathering evidence until root cause is established.
