# Software Engineering Method — Lifecycle

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Lifecycle

## 1. Available Work States

The method defines ten available Work States:

> **Idea -> Exploring -> Designing -> Awaiting Approval -> Preparing -> Ready -> Implementing -> Reviewing -> Validating -> Done**

This is **not** a mandatory linear pipeline. A Workflow Route selects only the
states and transitions required by the Work Type, Workflow Depth, artifact
triggers, Change Characteristics, and project policies.

`Approved` is not a Work State. It is an authority result/status of the artifact
or decision that was approved.

## 2. State meanings

### Idea

A possible need, problem, change, or question exists without a commitment to
implement it.

### Exploring

Important uncertainty is being investigated. Exploration, research, spikes, and
POCs may occur here.

### Designing

Candidate product behavior, architecture, or governance is being made explicit
before required authority gates are crossed.

### Awaiting Approval

The work is blocked on an external authority decision. AI may assess and
recommend but may not execute a human-only gate.

### Preparing

Accepted scope is being made executable. Typical activities include Technical
Design, ADR work, Task Planning when triggered, migration/compatibility planning,
validation planning, and Readiness Review.

### Ready

Implementation can proceed without requiring the implementer to decide
unresolved matters outside implementation authority.

### Implementing

The agreed scope is being implemented.

### Reviewing

Applicable code, architecture, functional, and specialist review perspectives
are being evaluated for acceptance.

### Validating

Final required evidence is being executed/evaluated to demonstrate that the
result works at the required boundaries. Tests may and should run earlier; this
state represents validation acceptance, not the first time tests are executed.

### Done

The agreed scope is concluded; applicable reviews and validation are satisfied;
durable owners are synchronized with the truth they own; and no unresolved
Working Decision remains for the completed scope.

## 3. Activities are not states

Examples:

| Activity                                | Typical Work State               |
| --------------------------------------- | -------------------------------- |
| Classification                          | Idea                             |
| Exploration / Research                  | Exploring                        |
| Functional Specification                | Designing                        |
| Architecture / Governance Design        | Designing                        |
| Human approval                          | Awaiting Approval (gate)         |
| Technical Design                        | Preparing                        |
| ADR analysis/finalization               | Designing or Preparing           |
| Task Planning                           | Preparing                        |
| Context Resolution                      | Any non-terminal state as needed |
| Readiness Review                        | Preparing                        |
| Implementation                          | Implementing                     |
| Code / Architecture / Functional Review | Reviewing                        |
| Validation                              | Validating                       |

## 4. Gates

### Authority Gate

Creates authority for a proposed decision, for example Human Functional
Approval. Authority gates may be project-configured but AI MUST NOT execute a
gate reserved for humans.

### Readiness Gate

Readiness Review returns `READY`, `READY WITH RISKS`, or `NOT READY`. Only the
first two permit transition to `Ready`.

### Quality Gate

All applicable review perspectives must be sufficiently accepted before work
can complete validation/closure.

### Evidence Gate

Required validation evidence must be sufficient for the work and its risks.

## 5. Transition rule

A state transition is permitted only when:

1. the selected Workflow Route permits it;
2. required activities are sufficiently complete;
3. applicable gates are satisfied;
4. blocking context or decision conflicts are absent;
5. artifact ownership remains valid.

If a later activity reveals an upstream problem, return to the owner/activity
authorized to resolve it. Returning is normal lifecycle behavior, not a process
failure.

## 6. Representative routes

### Quick defect

```text
Idea
-> Preparing (lightweight scope/readiness check)
-> Ready
-> Implementing
-> Reviewing
-> Validating
-> Done
```

No new Functional Specification is created when expected behavior is already
established.

### Standard product behavior change

```text
Idea
-> Exploring                 (when uncertainty warrants it)
-> Designing                 (Functional Specification)
-> Awaiting Approval         (Human Functional Approval)
-> Preparing                 (Technical Design if triggered, Tasks if triggered, Readiness)
-> Ready
-> Implementing
-> Reviewing
-> Validating
-> Done
```

### Complex architecture change without functional change

```text
Idea
-> Exploring
-> Designing                 (architecture alternatives / decision)
-> Awaiting Approval         (when project policy requires structural approval)
-> Preparing                 (ADR if triggered, implementation design, Tasks if triggered, Readiness)
-> Ready
-> Implementing
-> Reviewing                 (Architecture Review required)
-> Validating
-> Done
```

No artificial Functional Specification is required when product behavior is
unchanged.

### Research / Discovery

```text
Idea
-> Exploring                 (research / spike / POC)
-> Done                      (conclusions integrated where appropriate)
```

If research authorizes a materially different implementation effort, create or
continue the appropriate Product Behavior, Technical, or Architecture work
scope rather than treating POC code as automatically approved production code.
