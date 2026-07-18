# CMP Ontology (Draft)

## Purpose

CMP is not a programming language.

CMP is not a compiler.

CMP is not another AST.

CMP is an attempt to describe software using concepts that remain true regardless of language, framework, operating system, or implementation.

This document defines the vocabulary used by CMP.

---

# Scientific Principle

CMP does **not** assume it already knows the fundamental building blocks of software.

Instead, it treats every concept as a hypothesis until sufficient evidence supports it.

The ontology is therefore evolutionary.

Concepts may be refined, merged, or replaced as new evidence appears.

---

# Candidate Primitive Concepts

These are research hypotheses.

They are not yet considered canonical.

## Surface

A recognizable boundary within software.

Examples include:

- Function
- API endpoint
- Database table
- Message queue
- UI component
- CLI command

A Surface is something another part of the system can interact with.

---

## Effect

An observable change.

Examples:

- Database write
- File creation
- HTTP request
- Event emission
- Log message
- Screen update

Effects are observable outside pure computation.

---

## Dependency

A relationship where one Surface relies upon another.

Dependencies may be:

- Structural
- Runtime
- Semantic
- Operational

---

## Observation

Evidence extracted from a software system.

Observations never contain opinion.

They only describe measurable facts.

---

## Evidence

Proof supporting an Observation.

Evidence may include:

- Source code
- Runtime traces
- Tests
- Benchmarks
- Documentation
- Production telemetry

---

## Theory

A proposed explanation for why multiple observations appear across independent software systems.

Theories are probabilistic.

Observations are factual.

---

# Research Goal

Over time, CMP should determine:

- Which concepts are fundamental.
- Which concepts are derived.
- Which concepts should be discarded.

The ontology is expected to evolve.
