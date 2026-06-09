## ADDED Requirements

### Requirement: PRD skill shall extract a requirements-perspective summary before generating the PRD
The system SHALL perform a Requirements Lens step between reading design.md and generating prd.md, producing an internal summary that identifies real Actors, converts technical descriptions to capability statements, and maps each feature area to a business outcome.

#### Scenario: Requirements Lens produces Actor list without "as a system" entries
- **WHEN** the PRD skill reads a design.md that contains technical component descriptions and "as a system" language
- **THEN** the Requirements Lens step produces an Actor list containing only human roles
- **AND** no "as a system" or system-component subjects appear in the Actor list

#### Scenario: Requirements Lens converts technical language to capability statements
- **WHEN** the design.md contains technical terms such as component names, topic names, or third-party library names
- **THEN** the Requirements Lens summary rephrases each item as an observable system capability
- **AND** the summary does not contain the original technical terms

#### Scenario: Requirements Lens is internal and not written to prd.md
- **WHEN** the PRD skill completes the Requirements Lens step
- **THEN** the resulting summary is used only as generation input
- **AND** the summary content does not appear as a section in the final prd.md

### Requirement: PRD skill Acceptance Criteria shall describe user-observable behavior only
The system SHALL enforce that every Acceptance Criterion in prd.md describes behavior or outcomes observable by a user or business stakeholder, containing no class names, API field names, topic names, state machine enum values, or third-party component names.

#### Scenario: AC written from user perspective
- **WHEN** the PRD skill generates an Acceptance Criterion
- **THEN** the criterion describes what a user or stakeholder can see, do, or verify
- **AND** the criterion contains no technical identifiers such as class names, DTO field names, Kafka topic names, or library names

#### Scenario: AC bad example rejected
- **WHEN** a generated AC contains text such as "透過 REST API 建立 type=DISCOUNT 的活動，帶 ruleConfig"
- **THEN** the skill rewrites it to user-observable form such as "行銷人員可建立含折扣規則的活動，並指定目標受眾與觸達計畫"

### Requirement: PRD skill Functional Requirements shall describe capabilities, not implementations
The system SHALL enforce that every Functional Requirement in prd.md describes what the system must be able to do, containing no architecture terms, component names, or data schema references.

#### Scenario: FR written as capability statement
- **WHEN** the PRD skill generates a Functional Requirement
- **THEN** the requirement describes a system capability in plain language
- **AND** the requirement contains no component names, topic references, or schema field names

#### Scenario: FR bad example rejected
- **WHEN** a generated FR contains text such as "reach.orchestrator 必須是 reach.requested topic 的唯一消費者"
- **THEN** the skill rewrites it as "系統必須確保同一活動的觸達請求不重複執行"

### Requirement: PRD skill Technical Considerations section shall contain only scope constraints
The system SHALL restrict Section 7 (Technical Considerations) to constraints that limit requirements scope. Architecture decisions already documented in design.md SHALL NOT be reproduced in prd.md. If no scope constraints exist, the section SHALL be omitted entirely.

#### Scenario: Section 7 omitted when no scope constraints exist
- **WHEN** the PRD skill generates a prd.md for a change with no scope-limiting constraints
- **THEN** Section 7 (Technical Considerations) is absent from the output

#### Scenario: Section 7 contains only scope-limiting constraints
- **WHEN** the PRD skill generates a prd.md for a change that has scope constraints (e.g., "本期僅提供後端 API，不含管理 UI")
- **THEN** Section 7 lists only those constraints
- **AND** Section 7 does not reproduce architecture or component design from design.md
