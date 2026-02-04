# Architecture of the Energy Domain Ontology

## Purpose of this section

This section describes the **architectural organisation of the Energy Domain Ontology (EDO)**.

It explains how the ontology is structured, how its parts relate to each other, and how evolution and stability are achieved over time.

This document does not define modelling rules or constraints.  
Those are defined formally within the ontology itself.

---

## EDO as an ontology ecosystem

EDO is not a single monolithic ontology.

It is an **ontology ecosystem**, composed of multiple ontologies with distinct and complementary roles, designed to support:

- semantic consistency
- controlled evolution
- contractual stability
- domain extensibility

Each ontology within the ecosystem exists for a specific architectural reason.

---

## Core ontology

The **core ontology** defines the fundamental semantic building blocks shared across all energy domains and disciplines.

It contains:
- domain-independent abstractions
- foundational relationships
- semantic primitives used throughout the ecosystem

The core ontology is intentionally conservative and evolves slowly.  
Its role is to provide long-term semantic stability.

---

## Transitional domain ontologies

**Transitional domain ontologies** specialise the core ontology for a specific domain, asset class, or engineering context.

They:
- extend the core without modifying it
- capture domain consensus at a given moment in time
- may evolve more rapidly than the core

Transitional ontologies are the primary place where domain-specific semantics are introduced before being stabilised or promoted.

---

## Governance ontologies

Governance in EDO is itself expressed through ontologies.

Governance ontologies define and formalise:
- review processes
- maintenance rules
- extraction and validation logic
- lifecycle-related semantics

By modelling governance explicitly, EDO ensures that evolution is transparent, inspectable, and machine-readable.

---

## Releases and immutability

At specific points in time, selected ontologies are grouped into a **release**.

A release is:
- versioned
- immutable
- intended for long-term reference

Released artefacts may be safely referenced in contracts, specifications, and institutional agreements.

Once released, an artefact is never modified; evolution occurs through new versions.

---

## Separation of responsibilities

The architectural structure of EDO enforces a clear separation between:

- conceptual semantics  
- domain specialisation  
- governance and validation  
- released contractual artefacts  

This separation is intentional and fundamental to the reliability of the ontology.

---

## Architectural intent

The architecture of EDO is designed to ensure that:

- meaning is explicit and stable  
- evolution does not break trust  
- domains can evolve independently  
- formal semantics remain the ultimate source of truth  

This architectural discipline is what allows EDO to function as semantic infrastructure rather than as documentation or convention.

---

## Architectural decision criteria for the EDO ecosystem

This document describes the architectural organisation of the EDO and the intent behind its structure.

When architectural decisions involve trade-offs between stability and evolution,  
between domain specificity and reuse,  
or between conceptual clarity and practical delivery constraints,  
those decisions are guided by an explicit ecosystem-level criterion.

That criterion is documented separately in:

[EDO Ecosystem – Architectural Decision Criterion](./ecosystem-decision-criterion.md)

This separation is intentional:
- this document explains how the ecosystem is structured
- the decision criterion defines how architectural tensions are resolved over time
