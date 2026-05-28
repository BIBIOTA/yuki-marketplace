# OpenSpec Format Reference

## OpenSpec Project Layout

An OpenSpec repository keeps all specification artifacts under the `openspec/` directory at the repo root. `openspec/project.md` holds project-level metadata: name, owner, and the active change list. `openspec/specs/` contains the canonical, versioned capability specs that represent the current state of the system — each capability lives under its own subdirectory (e.g., `openspec/specs/auth/spec.md`). `openspec/changes/` is the working area: each in-progress change gets its own subdirectory named by a change ID (e.g., `openspec/changes/2026-05-28-add-login/`). Completed changes are moved to `openspec/archive/changes/` after merge.

## Change Anatomy

Every change lives under `openspec/changes/{change-id}/` and contains the following standard files:

- `proposal.md` — motivation, summary of what changes, impact assessment, and links to all related artifacts.
- `tasks.md` — implementation task checklist with acceptance criteria, dependencies, and independence estimates.
- `design.md` — architecture or technical design decisions for the change.
- `specs/` — subdirectory containing one `spec.md` per affected capability, written in Requirement delta syntax.
- `diagrams/` — (optional) PlantUML sources (`.puml`) for sequence, state, ER, and other diagram types.
- `designs/` — (optional) Figma reference document (`figma.md`) and screenshot assets.

## Requirement Naming Rules

Requirement names appear in `### Requirement: <name>` headings. The name must be:

- **Unique within a capability spec.** Duplicate names inside the same `spec.md` are a validation error.
- **Stable across patches.** If you revise a requirement without changing its core identity, keep the same name and put it under `## MODIFIED Requirements`. Renaming a requirement that is being kept is a breaking traceability change.
- **Written from the user or system perspective** (e.g., "User shall be able to reset their password", "System SHALL throttle login attempts"). Avoid implementation-detail names like "Call /api/v1/auth/reset".

The body line immediately after the `### Requirement:` heading is the normative statement and MUST use the word `SHALL` (not "should", "must", or "will").

## Requirement Delta Syntax

OpenSpec uses three delta keywords to indicate how requirements change. Use `## ADDED Requirements` for net-new requirements, `## MODIFIED Requirements` for changes to existing requirements, and `## REMOVED Requirements` for requirements being retired. A single `spec.md` file may contain any combination of the three sections, but each section heading must appear at most once per file.

### ADDED Requirements

```markdown
## ADDED Requirements

### Requirement: User shall be able to reset their password
The system SHALL allow registered users to request a password-reset email.

#### Scenario: Reset email sent
- **WHEN** a user submits a registered email address
- **THEN** the system sends a password-reset link to that address
- **AND** the link expires after 30 minutes
```

### MODIFIED Requirements

```markdown
## MODIFIED Requirements

### Requirement: Session token lifetime increased to 7 days
The system SHALL issue session tokens valid for 7 days (previously 24 hours).

#### Scenario: Token still valid on day 6
- **WHEN** a user presents a token issued 6 days ago
- **THEN** the system accepts the token and returns 200
```

### REMOVED Requirements

```markdown
## REMOVED Requirements

### Requirement: Legacy basic-auth endpoint removed
The `/api/v1/auth/basic` endpoint SHALL no longer be available.

#### Scenario: Basic-auth request rejected
- **WHEN** a client sends a Basic Authorization header to any endpoint
- **THEN** the system returns 410 Gone with a migration notice
```

## Scenario Syntax

Each Requirement must have at least one Scenario block. A Scenario captures one observable system behavior using a structured WHEN / THEN / AND format.

```markdown
#### Scenario: <descriptive name>
- **WHEN** <precondition or trigger>
- **THEN** <expected outcome>
- **AND** <additional outcome or constraint>   ← optional; repeat as needed
```

The `#### Scenario:` heading uses four `#` marks. The name after the colon should be a short, plain-language description of the case being tested (e.g., "Successful login", "Token expired", "Duplicate email rejected").

Example:

```markdown
#### Scenario: Duplicate email rejected
- **WHEN** a user attempts to register with an email already in the system
- **THEN** the system returns 409 Conflict
- **AND** the response body includes `"error": "email_already_registered"`
- **AND** no new account is created
```

## > See: Reference Convention

The `> See: <relative-path>` blockquote links a Scenario to an artifact — a PlantUML diagram or a Figma design document — that visually specifies the behavior. The path is relative to the `spec.md` file that contains the reference.

Every diagram in `openspec/changes/{change-id}/diagrams/` and every design in `openspec/changes/{change-id}/designs/figma.md` MUST appear in at least one `> See:` reference across the change's specs. This ensures traceability from written requirements back to visual artifacts.

Example (a Scenario that references both a diagram and a Figma design):

```markdown
#### Scenario: Successful OAuth callback
- **WHEN** the OAuth provider redirects with a valid `code` parameter
- **THEN** the system exchanges the code for tokens and creates a session
- **AND** the user is redirected to the dashboard

> See: ../../diagrams/01-sequence-oauth-flow.puml
> See: ../../designs/figma.md#oauth-happy-path
```

The `> See:` lines appear immediately after the last `- **AND**` / `- **THEN**` line in the Scenario block, with no blank line between them and the scenario body.

## openspec validate --strict — Common Errors and Fixes

Run `openspec validate {change-id} --strict` from the repo root. The tool exits non-zero and prints error messages for any structural violation. Below are the four most common errors.

| # | Error message snippet | Fix |
|---|---|---|
| 1 | `proposal.md: missing '## Why' section` | Add a `## Why` section to `proposal.md` with at least one sentence of motivation. |
| 2 | `specs/{capability}/spec.md: Requirement '{name}' has no Scenario` | Add at least one `#### Scenario:` block with WHEN/THEN lines under the offending Requirement. |
| 3 | `specs/{capability}/spec.md: duplicate Requirement name '{name}'` | Rename one of the two Requirements — names must be unique within a single spec file. |
| 4 | `proposal.md: capability '{name}' not found under specs/` | Either create `openspec/changes/{change-id}/specs/{name}/spec.md` or correct the capability name in `## What Changes`. |

Re-run `openspec validate {change-id} --strict` after each fix; it is safe to run multiple times.

Two additional errors worth noting:

- **`> See:` path not found** — the referenced file does not exist relative to the spec. Double-check the relative path: from `specs/{capability}/spec.md` to a diagram the path is `../../diagrams/{file}.puml`. Correct the path or create the missing artifact.
- **`proposal.md: 'What Changes' lists no capabilities`** — the `## What Changes` section is empty or has no bolded capability names. Add at least one `- **{capability}**: ...` bullet.

## openspec archive — Post-merge Workflow

After a change branch is merged to master, run:

```bash
openspec archive {change-id}
```

This command moves `openspec/changes/{change-id}/` into `openspec/archive/changes/{change-id}/` and stamps the directory with the merge date in `openspec/archive/changes/{change-id}/.archived-at`. The archived directory becomes immutable history: the specs that were written for this change are preserved exactly as they were at merge time, allowing future maintainers to trace why a requirement was added, modified, or removed. Do not edit files under `openspec/archive/` after archiving.

Typical post-merge workflow:

```bash
# 1. Merge the feature branch
git checkout master && git merge feat/{change-id}

# 2. Archive the change
openspec archive {change-id}

# 3. Commit the archive operation
git add openspec/archive/changes/{change-id}/ openspec/changes/
git commit -m "chore: archive OpenSpec change {change-id}"
```

The `openspec/changes/{change-id}/` directory is removed from the working tree after a successful archive. If you need to inspect the historical spec, read from `openspec/archive/changes/{change-id}/`.
