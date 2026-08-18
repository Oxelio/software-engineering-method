# Software Engineering Method — Readiness Review

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Pre-implementation readiness

## 1. Purpose

A Readiness Review determines whether the authorized and designed work can
enter implementation without requiring the implementer to invent unresolved
functional, structural, execution, or validation decisions.

Readiness Review checks decisions; it does not silently make missing upstream
decisions.

## 2. Position

When Task Planning is triggered, it occurs before formal Readiness Review:

```text
Technical/authorized design
-> Task Planning when triggered
-> Readiness Review
-> Ready
-> Implementation
```

When Task Planning is not triggered, Readiness Review verifies that the Work
itself is a sufficiently bounded execution unit and that no artificial Task
decomposition is required.

This does not require exhaustive micromanagement. When Tasks exist, they should
constrain what must be preserved while leaving the Developer authority over
local details.

Quick work may use an implicit lightweight readiness check rather than a durable
review record.

## 3. Context precondition

- `RESOLVED` Context Manifest -> review may proceed.
- `PARTIALLY RESOLVED` -> proceed only when missing context is explicitly non-blocking.
- `BLOCKED` or `CONFLICTED` -> `NOT READY`.

## 4. Review dimensions

### Authority Readiness

Verify applicable owners are identifiable, required human gates are crossed,
relevant decisions have the required authority, and no competing normative
owner remains unresolved.

### Functional Readiness

When functional behavior is affected, verify approved scope, significant rules
and invariants, expected failures/edge cases, and testable acceptance criteria.

For Defect Correction, verify expected behavior is established and the proposed
work restores rather than redefines it.

### Design / Architecture Readiness

When design is applicable, verify material responsibilities, boundaries, flows,
state/persistence, transactions/consistency, concurrency/idempotency,
integration, failure semantics, security/privacy, migration/compatibility,
performance/operations, and architecture alternatives as relevant.

Project-specific architecture criteria are loaded through the Project Method
Profile.

### Execution Readiness

Verify dependencies/prerequisites and, when Tasks exist, their boundaries,
sequencing, component ownership, and absence of unresolved decisions outside
implementation authority. When no Tasks are required, verify that the Work
itself is sufficiently bounded for authorized implementation.

A useful test is: **could a competent Developer execute the Work and any Tasks by
inspecting the repository and making only authorized local implementation
decisions?**

### Validation Readiness

Verify acceptance criteria and material design risks map to an appropriate
validation strategy and that required environments/tooling/evidence boundaries
are identifiable.

### Conditional Readiness

Change Characteristics activate additional checks for security, privacy, data
migration, breaking compatibility, performance, operations, compliance, or
other project-defined concerns.

## 5. Findings

Each finding is one of:

- `BLOCKER` — implementation cannot responsibly proceed;
- `RISK` — implementation may proceed, but the risk must be carried to an explicit later activity;
- `NOTE` — non-blocking handoff information.

Every blocker MUST identify the owner/activity authorized to resolve it.
Every accepted non-blocking risk MUST identify where it will be resolved or
validated.

An unresolved decision is not a risk merely because calling it a risk would
make the work easier to mark Ready.

## 6. Results

### READY

No blocker remains. Transition to Work State `Ready` is permitted.

### READY WITH RISKS

No blocker remains, but explicit non-blocking risks must be propagated into
Implementation, Review, Validation, operations, or a separately scoped work
item. `READY WITH RISKS` still permits Work State `Ready`.

### NOT READY

At least one blocker remains. The work returns to the owner/activity able to
resolve it.

## 7. Authority

Readiness is not inherently a human-only gate because it does not create new
product truth. An AI orchestrator may assess and return `READY` when project
policy permits. Projects MAY require a human readiness authority for selected
work, such as Complex or regulated changes.

Readiness NEVER overrides a missing prior human authority gate.

## 8. Suggested record

```text
READINESS REVIEW

Identity
- Project / Work / Work Type / Depth / target scope

Context
- Context Manifest status

Prerequisite Gates
- ...

Authority Readiness
- status / findings

Functional Readiness
- applicable: yes/no
- status / findings

Design / Architecture Readiness
- applicable: yes/no
- status / findings

Execution Readiness
- status / findings

Validation Readiness
- status / findings

Conditional Reviews
- security / migration / compatibility / ...

Blockers
- issue / owner / role / return activity

Non-blocking Risks
- issue / carry-forward destination

Result
- READY | READY WITH RISKS | NOT READY
```
