# Software Engineering Method — Review and validation

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Review / Validation

## 1. Review and validation are different

Review asks whether the implementation is acceptable against applicable quality,
architecture, and functional expectations.

Validation asks what evidence demonstrates that the resulting behavior and
technical properties work at the required boundaries.

Passing tests does not by itself prove architecture compliance. Good code does
not by itself prove functional compliance.

## 2. Core review perspectives

### Code Review

Evaluate readability, naming, complexity, duplication, error handling, test
quality, maintainability, and unnecessary abstraction.

### Architecture Review

When applicable, evaluate implementation against project-owned architecture
constraints, applicable Technical Design, durable structural decisions, and
boundary/ownership rules.

### Functional Compliance Review

When approved product behavior is applicable, compare implementation and
observable evidence against the Functional Specification and acceptance
criteria. Implementation limitations MUST NOT silently become new requirements.

## 3. Specialist review

Change Characteristics may trigger additional security, privacy, migration,
compatibility, performance, operational, compliance, or other specialist review.
Projects define their concrete specialist criteria.

## 4. Review perspective independence

Review perspectives are semantically distinct responsibilities. They do not, by
default, require distinct physical humans or AI agents. A project MAY require
physical reviewer independence when risk, compliance, or project policy warrants
it.

When the same physical human or AI changes from an implementation/design Role to
a review Role, the Role transition SHOULD be explicit and the relevant context
SHOULD be re-resolved. The result MUST be assessed under the active review Role's
criteria and authority; review acceptance MUST NOT be inferred from authorship,
implementation activity, or an earlier Role result.

## 5. Review routing

A finding must return to the authority able to resolve it:

- local implementation issue -> Implementing;
- Technical Design/architecture issue -> Preparing / Software Architect;
- functional behavior issue -> Designing / Product-Domain activity and human
  approval when behavior changes;
- governance-owner issue -> relevant governance activity.

## 6. Transition to validation

Under the normal Workflow Route, Work enters `Validating` only after applicable
review perspectives are sufficiently accepted. Validation evidence MAY be
executed earlier or overlap operationally; the Work State transition records
that review acceptance is sufficiently established, not the start of testing.

A project MAY configure controlled review/validation overlap, but it MUST preserve
the distinction between review acceptance and validation evidence and MUST still
satisfy all applicable review perspectives before `Done`.

## 7. Validation principle

Select the smallest sufficient set of evidence for the behavior, boundaries,
and risks being changed.

Possible evidence levels include:

- unit/domain tests;
- application behavior tests;
- adapter/integration tests;
- contract tests;
- acceptance/end-to-end tests;
- security checks;
- migration/compatibility verification;
- performance evidence;
- manual validation where automation is not sufficient.

The method does not mandate a specific test framework or a fixed pyramid.

## 8. Validation acceptance

Work may leave `Validating` only when required evidence is sufficient or when a
failure is explicitly routed back to the owner/activity that must change.

Validation evidence is evidence, not an owner of product or architecture truth.

## 9. Done

Work may enter `Done` only when:

- its agreed scope is implemented or otherwise concluded;
- applicable review perspectives are satisfied;
- required validation evidence is sufficient;
- current/target owners are synchronized with the truth they own;
- no unresolved Working Decision remains for completed scope.
