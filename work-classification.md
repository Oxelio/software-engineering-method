# Software Engineering Method — Work classification

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Work classification

## 1. Work Types

Identify the primary intent before selecting workflow depth.

### Product Behavior Change

Intentional introduction, removal, or modification of externally observable or
business-relevant behavior.

Typical examples: a new capability, business rule, use case, authorization
behavior, or product policy.

### Defect Correction

Restoration of behavior that is already established by an authoritative owner
or explicit contract.

A defect workflow MUST NOT be used to introduce unapproved product behavior. If
expected behavior cannot be established, reclassify the affected question as a
Product Behavior Change or Exploration.

### Technical Change

A change to implementation, tooling, infrastructure, operations, or internal
technical structure that intentionally preserves approved product behavior and
does not establish a new durable structural architecture rule.

Typical examples: dependency updates, refactoring, build/CI changes, compatible
framework upgrades, and internal performance improvements.

### Architecture Change

Intentional establishment, replacement, or material alteration of a durable
structural property of the system.

Architecture Change does not imply a Functional Specification when no product
behavior is being changed.

### Research / Discovery

Work whose primary purpose is to reduce uncertainty, compare alternatives,
collect evidence, or determine whether another change should be undertaken.
A spike or POC does not become production architecture merely because it exists.

### Governance Change

A change to project/method governance, ownership rules, approval rules,
delivery policy, engineering conventions, or other normative process.

Changing a normative Markdown rule is Governance or Architecture work as
appropriate; it is not Documentation-only merely because only documentation is
edited.

### Documentation-only Change

A representation-only change that does not alter the truth or policy being
documented: typo correction, formatting, link repair, or meaning-preserving
clarification.

## 2. Change Characteristics

Characteristics modify risk, context, review, and validation. They do not
replace the primary Work Type.

Common characteristics include:

- security-sensitive;
- privacy-sensitive;
- data migration;
- breaking/public compatibility;
- performance-sensitive;
- cross-component or cross-system;
- concurrency-sensitive;
- difficult to reverse / destructive;
- operationally critical;
- compliance-sensitive.

A migration, security concern, database change, or refactoring is therefore not
necessarily a separate Work Type.

## 3. Workflow Depth

### Quick

Use when the work is well understood, local, low risk, highly reversible, and
requires no unresolved product, structural architecture, or governance decision.

Typical cases:

- a clear defect against established behavior;
- a documentation-only correction;
- a mechanical refactoring;
- a safe dependency update with no material compatibility consequence;
- adding missing tests for established behavior.

### Standard

Use for meaningful work that requires explicit reasoning and controlled
implementation but remains primarily within established product, architecture,
and governance boundaries.

Typical cases:

- a bounded product behavior change;
- a new local use case;
- a non-trivial technical upgrade;
- a local technical design decision using established architecture.

### Complex

Use when one or more strong escalation signals exist:

- a durable structural decision;
- high uncertainty or several important alternatives;
- security/privacy/safety/compliance criticality;
- significant data-integrity risk;
- breaking public compatibility or coordinated rollout;
- destructive or difficult-to-recover migration;
- broad cross-system/cross-capability impact;
- difficult reversibility.

A small code diff may be Complex; a large mechanical diff may be Quick.

## 4. Classification is revisable

Workflow Depth MUST be re-evaluated when new functional, architectural, risk,
migration, compatibility, or uncertainty information appears.

Upward reclassification may happen immediately. Downward reclassification that
removes a required artifact or gate MUST be explicit and justified.

Workflow Depth never overrides a human authority gate.

## 5. Artifact and gate triggers

Artifacts are triggered by needs, not mechanically by depth.

### Exploration

Required when important uncertainty exists about the problem, behavior,
solution, or material trade-offs.

### Functional Specification

Required when new or intentionally changed product behavior must become
approved project truth.

### Human Functional Approval

Required before proposed functional behavior becomes `Approved`.

### Technical Design

Required when implementation depends on non-trivial technical decisions that
should be understood before coding.

### ADR

Required when a durable structural architecture decision has meaningful
alternatives and its rationale would otherwise be costly to reconstruct.

### Tasks

Required when implementation needs delegation, sequencing, or independently
verifiable execution units. A lightweight work item may be enough for Quick work.

### Readiness Review

Required for meaningful designed/planned implementation before entering `Ready`.
Quick work may use an implicit lightweight readiness check instead of a durable
review artifact.

### Architecture Review

Required when architecture constraints or structural design are affected.

### Functional Compliance Review

Required when implementation must satisfy approved functional behavior.

### Validation

Every implemented change requires sufficient validation evidence. The form and
scope are proportional to the work and its characteristics.
