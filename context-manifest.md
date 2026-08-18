# Software Engineering Method — Context Manifest

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Context engineering

## 1. Purpose

A Context Manifest is an activity-scoped working artifact describing which
sources are needed, why they are needed, what authority they have, which
sources are conditionally relevant, and which context is intentionally excluded.

It is a context resolver, not a project summary or a new source of truth.

## 2. Inputs

Context resolution uses:

- Project Method Profile;
- current Work and Work Type;
- Workflow Depth;
- current Work State and Activity;
- active Role;
- Change Characteristics;
- artifact ownership dependencies;
- implementation evidence discovered during the work.

## 3. Context classes

### Authoritative Context

Sources that own normative truth required by the current activity. Record the
scope of authority, not merely the path.

### Required Working Context

Non-authoritative working artifacts necessary to continue the current activity,
such as an active Exploration or Technical Design draft.

### Relevant Evidence

Code, tests, current interfaces, benchmarks, or other evidence of what is
currently implemented or observed.

### Conditional Context

Context loaded only when a Work Type, Change Characteristic, discovered
dependency, or project policy makes it relevant.

### Excluded by Default

Context intentionally omitted from the initial working set because it is
unrelated, obsolete, rejected, overly broad, or likely to bias the current role.
Exclusion is revisable when a new dependency appears.

### Missing / Conflicting Context

Required sources that are missing, ambiguous, stale, or mutually inconsistent.
Classify findings as blocking, non-blocking, or warnings.

## 4. Status

A Context Manifest has one of these statuses:

- `RESOLVED` — required context is available and coherent;
- `PARTIALLY RESOLVED` — missing context is explicitly non-blocking;
- `BLOCKED` — a required source is missing;
- `CONFLICTED` — authority cannot be resolved because relevant sources conflict.

A blocked/conflicted context may still support investigation, but normative
activity output MUST NOT pretend the blocker does not exist.

## 5. Principles

1. Context is scoped to the current activity.
2. Relevance and authority are separate dimensions.
3. Durable owners outrank working artifacts for the subject they own.
4. Implementation is evidence unless it owns the fact being asked about.
5. Context is resolved progressively rather than accumulated blindly.
6. Role transitions SHOULD trigger context re-resolution.
7. Conditional context is activated by work characteristics and discovered
   dependencies.
8. Missing/conflicting required context MUST be surfaced, not guessed away.
9. Downstream context SHOULD prefer an authoritative promoted owner over a
   resolved Working Decision entry.
10. A Context Manifest never becomes a competing source of project truth.

## 6. Suggested shape

```text
CONTEXT MANIFEST

Identity
- Project
- Work
- Work Type
- Workflow Depth
- Work State
- Activity
- Role

Context Status
- RESOLVED | PARTIALLY RESOLVED | BLOCKED | CONFLICTED

Authoritative Context
- source
  authority
  relevance

Required Working Context
- source
  purpose

Relevant Evidence
- source
  evidence provided

Conditional Context
- source/capability
  trigger
  loaded: yes/no

Excluded by Default
- source/category
  reason

Missing / Conflicting Context
- requirement
  issue
  severity
  required resolution
```

## 7. Stop condition

Context resolution is sufficient when all information necessary for the
current role's authorized decisions is available, applicable conflicts are
surfaced, and remaining unknowns cannot invalidate those decisions.

Prefer the narrowest context that still preserves the decision boundary and its
relevant dependencies; do not optimize context so aggressively that important
surrounding constraints disappear.
