# Software Engineering Method — Working Decision Log

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Working memory

## 1. Purpose

A Working Decision Log is temporary workflow memory for decisions that are open
or provisional and matter to continuation of the current Work.

It does not own durable product, architecture, governance, or implementation
truth.

## 2. When to record a decision

Record a working decision when one or more apply:

- the decision affects more than the immediate local action;
- a later role/handoff needs to know it;
- several reasonable alternatives exist and a temporary choice is required;
- the choice may need promotion into an authoritative owner;
- the decision is intentionally deferred to a known trigger/evidence;
- losing the rationale before the next activity would cause meaningful rediscovery;
- the decision may affect route, depth, context, or readiness.

Do not record routine local implementation choices that are already delegated
to the current role.

## 3. Status and disposition

Use simple statuses:

- `Open` — a material decision is needed;
- `Provisional` — a bounded temporary choice exists;
- `Resolved` — the working entry no longer carries unresolved authority.

Resolved entries identify a disposition:

- `Integrated` — incorporated into the appropriate existing owner;
- `Promoted` — moved through a durable decision mechanism such as an ADR;
- `Superseded` — replaced by another decision;
- `Dropped` — no longer relevant to the work scope.

## 4. Authority rules

1. A Working Decision MUST have explicit scope.
2. A provisional decision MUST be visibly provisional.
3. A Working Decision MUST NOT override an authoritative owner.
4. Decisions outside the active role's authority MUST be escalated rather than silently made in the log.
5. A functional working decision becomes durable only through the Functional Specification and applicable human approval.
6. A local technical working decision may be integrated into Technical Design.
7. A durable structural decision is evaluated against ADR policy and current architecture ownership.
8. Governance decisions belong to governance owners, not automatically to ADRs.

## 5. Ready and Done constraints

Work MUST NOT enter `Ready` while an unresolved Working Decision exceeds the authority delegated to implementation.

Work MUST NOT enter `Done` with unresolved Working Decisions for the completed scope. Every entry must be integrated, promoted, superseded, dropped, or moved to an explicitly separate work scope.

## 6. Downstream context

Once a decision has an authoritative owner, downstream Context Manifests SHOULD load the owner rather than the resolved Working Decision entry. The log is not a second copy of the final decision.

## 7. Retention

The log may live in a conversation, issue, temporary workspace, or repository file when long-running/Complex work needs external memory.

It is not durable history by default. After decisions are integrated, the log may be discarded. Git preserves repository history; important durable rationale belongs in its proper owner.

## 8. Suggested entry

```text
WD-<id>

Decision
- <what must be / was decided>

Status
- Open | Provisional | Resolved

Scope
- <where the decision applies>

Rationale
- <only the rationale needed to preserve workflow memory>

Constraints / Evidence
- <references, not duplicated source material>

Target Owner
- <if the decision becomes durable>

Resolution Trigger
- <what makes it final or requires reconsideration>

Disposition
- <when resolved>
```
