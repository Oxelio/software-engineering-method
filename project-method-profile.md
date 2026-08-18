# Software Engineering Method — Project Method Profile

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Project integration

## 1. Purpose

A Project Method Profile binds method-defined semantic requirements to the
canonical project sources and project-specific policy extensions that satisfy
them.

It is a typed index/composition mechanism, not a second project summary and not
a duplicate source of architecture or product truth.

## 2. Typical bindings

An adopting project SHOULD make the following semantic owners discoverable when
applicable:

```text
project.vision
project.scope

governance.documentation
governance.delivery

architecture.principles
architecture.current
architecture.dependencies
architecture.decisions

development.conventions
validation.policy

agents.operations
agents.project_context
```

The method defines the semantic slot; the project decides the file, directory,
service, or other canonical owner that fulfills it.

## 3. Reference rather than duplicate

Prefer:

```text
architecture.principles -> docs/.../architecture-principles.md
```

over:

```text
architecture.principles:
  - DDD
  - Clean Architecture
  - ...
```

when another canonical document already owns those facts.

A profile may directly own a small configuration value only when no other
project owner exists and the profile is intentionally chosen as that owner.

## 4. Agent use

The profile allows an orchestrator to resolve the Context Manifest without
hard-coding repository paths into the generic method.

Example:

```text
Activity = Technical Design
Method requires = approved functional owner + architecture constraints + current architecture + relevant ADRs
Profile resolves = concrete project sources
Context Manifest selects = only the relevant sources/sections/evidence
```

## 5. Errors

If a required binding is missing, stale, or resolves to competing normative
owners, the orchestrator MUST surface the problem rather than invent the missing
project rule.

## 6. Method relationship

Projects may configure method extension points, add stricter project-specific
requirements, or explicitly document deviations. Project-specific architecture
must not be promoted into the generic method simply because one project uses it.
