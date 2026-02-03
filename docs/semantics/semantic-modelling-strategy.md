# Semantic Modelling Strategy

## Purpose of this section

This section describes the **semantic modelling strategy adopted by the Energy Domain Ontology (EDO)**.

It explains *why* EDO expresses meaning primarily through declarative annotations and contextual semantics, rather than through prescriptive OWL object properties and logical restrictions.

This document does not define modelling rules.
It explains how the EDO should be **read and interpreted**.

---

## The nature of the energy domain

The energy domain — particularly in sectors such as oil and gas, subsea systems, and nuclear energy — exhibits characteristics that strongly influence how semantics must be represented.

Engineering knowledge in this domain is:

- contextual and phase-dependent  
- negotiated through technical and contractual agreement  
- subject to revision, exception, and tolerance  
- distributed across multiple actors and responsibilities  

Meaning is rarely universal or timeless.  
The same concept may be valid, required, optional, or even irrelevant depending on lifecycle phase, contractual scope, or engineering responsibility.

As a result, the domain is not naturally inferential in the logical sense.
It is **situated and declarative**.

---

## Limitations of prescriptive OWL semantics in this domain

Classical OWL modelling, based on object properties and logical restrictions, assumes that:

- axioms are universally true  
- meanings are stable and context-independent  
- inference is monotonic  
- contradictions represent modelling errors  

In the energy domain, these assumptions frequently do not hold.

Engineering models may legitimately:
- coexist with partial inconsistency  
- express provisional or negotiated decisions  
- change meaning across phases  
- accept deviations under contractual agreement  

Encoding such semantics directly as OWL restrictions would lead to:
- fragile ontologies  
- premature formalisation  
- excessive refactoring as domain understanding evolves  

---

## Declarative semantic modelling

To address this, EDO adopts a **declarative semantic modelling strategy**.

In this strategy:
- meaning is **declared explicitly**, not inferred implicitly  
- semantics are described rather than enforced at the logical level  
- interpretation is deferred to contextual and validation layers  

Annotations are used as first-class semantic carriers, allowing the ontology to express:
- intent  
- scope  
- applicability  
- responsibility  
- domain interpretation  

This approach reflects how engineering knowledge is actually produced, reviewed, and accepted.

---

## Relationships as declarative semantics

In EDO, many engineering relationships are not modelled as OWL object properties.

Instead, they are expressed as **declarative relationship semantics**, using annotations that describe:
- the nature of the relationship  
- the roles involved  
- the context under which it applies  

This avoids encoding engineering intent as rigid logical axioms, while still making the semantics explicit, inspectable, and governable.

Relationships are therefore understood as **semantic statements**, not as universally true logical facts.

---

## Context as a first-class concept

Context is central to the EDO semantic strategy.

Rather than encoding meaning through subclass hierarchies or hard constraints, EDO expresses:
- *when* a semantic statement applies  
- *under which conditions* it is valid  

Contextual semantics allow:
- multiple interpretations to coexist  
- gradual refinement of meaning  
- clear separation between core meaning and conditional applicability  

This enables semantic precision without sacrificing flexibility.

---

## Validation outside OWL inference

EDO does not abandon rigour.
It **relocates rigour**.

Formal validation is performed through:
- explicit validation layers
- context-aware constraints
- contract- or phase-specific rules

This allows validation to be:
- precise without being universal  
- strict without being brittle  
- adaptable without redefining core semantics  

OWL defines the semantic space.
Validation determines acceptable usage within a given context.

---

## Governance and evolvability

The declarative semantic strategy directly supports governance and long-term evolution.

Because semantics are expressed declaratively:
- changes are explicit and traceable  
- governance rules can be inspected and versioned  
- domain evolution does not invalidate core meaning  

This is essential for an ontology intended to function as **semantic infrastructure** over long time horizons.

---

## How to read the EDO under this strategy

When reading the EDO, it is important to understand that:

- annotations express declared meaning  
- context defines applicability  
- validation defines acceptability  
- inference is not the primary objective  

Meaning emerges from the combination of these layers, not from logical deduction alone.

---

## Architectural consequence

The semantic modelling strategy described here is not an isolated choice.
It underpins:

- the use of annotations for relationships  
- the treatment of context as a core abstraction  
- the separation between core, transitional, and governance ontologies  
- the distinction between semantics and validation  

Understanding this strategy is essential to understanding the EDO as a whole.
