# Software Engineering Method

> **Content status:** Canonical
>
> **Document type:** Engineering Method
>
> **Domain:** Delivery / AI-assisted engineering

## Purpose

This repository defines a generic software-engineering method for governing how
work is understood, classified, specified, approved, designed, prepared,
implemented, reviewed, validated, and contextualized for humans and AI agents.

The method deliberately does **not** prescribe a product architecture, a
programming language, a framework, or Domain-Driven Design. Those choices belong
to each adopting project.

An adopting project binds the method to its own canonical project sources
through a project-owned Project Method Profile conforming to this method's
[Project Method Profile](project-method-profile.md) contract.

## Core documents

1. [Core model](core-model.md) — vocabulary, invariants, truth model, and method/project boundary.
2. [Work classification](work-classification.md) — Work Types, Change Characteristics, Quick/Standard/Complex, and artifact triggers.
3. [Lifecycle](lifecycle.md) — Work States, Activities, Gates, transitions, and route examples.
4. [Artifact ownership](artifact-ownership.md) — durable owners, working artifacts, evidence, and synchronization rules.
5. [AI role contracts](roles.md) — permissions, limits, escalations, and role transitions.
6. [Context Manifest](context-manifest.md) — progressive context resolution and authority-aware context selection.
7. [Readiness Review](readiness-review.md) — the gate that determines whether work may enter `Ready`.
8. [Working Decision Log](working-decision-log.md) — temporary workflow memory and decision-promotion rules.
9. [Review and validation](review-validation.md) — independent review perspectives and evidence-based validation.
10. [Project Method Profile](project-method-profile.md) — how an adopting project binds the method to canonical sources.

## Method boundary

The method owns **work governance**. An adopting project owns its product intent,
scope, architecture, technologies, conventions, concrete decisions,
implementation, and evidence.

When the method requires a project-specific choice, the method owns the
requirement that the choice be explicit; the project owns the chosen value.
For example, the method requires an identifiable owner for architecture
constraints; each adopting project defines those constraints in its own
canonical sources.

## Adoption

Projects adopt this method by referencing this repository/version and maintaining
a project-owned Project Method Profile that binds method semantic slots to
project canonical owners and explicit project extensions or deviations.

Adoption MUST NOT create a second normative copy of the method inside the
adopting project. Project-owned documents may summarize method expectations for
local context, but the canonical method remains owned here.

## Authority

Git history in this repository is the canonical history of the method. Each
adopting project's repository or configured operational owners remain canonical
for that project's own product, architecture, governance extensions,
implementation, and evidence.

AI conversations, handoffs, Context Manifests, Working Decision Logs, and
generated proposals are working context only until accepted knowledge is
integrated into its authoritative owner.
