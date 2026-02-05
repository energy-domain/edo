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

## Relationships as semantic possibility, not factual assertion

In the EDO, relationships do **not** assert that two project instances are connected, related, or composed.

Instead, the ontology declares **which relationships are semantically possible** between classes of elements, under specific contextual conditions.

A relationship in the EDO defines:
- a permitted semantic interpretation  
- a recognised engineering meaning  
- a valid space of interaction  

Whether such a relationship actually exists in a given project instance is determined outside the ontology, through contextual data, validation rules, and contractual scope.

This distinction is fundamental.

EDO defines what *can* be meaningfully stated.  
Project data determines what *is* stated.

---

## Relationships as declarative semantics

Because relationships express semantic possibility rather than factual truth, many engineering relationships in EDO are not modelled as OWL object properties.

They are expressed as **declarative relationship semantics**, using annotations that describe:
- the nature of the relationship  
- the roles involved  
- the context under which it applies  

This avoids encoding engineering intent as rigid logical axioms, while still making the semantics explicit, inspectable, and governable.

Relationships are therefore understood as **semantic declarations**, not as universally true logical facts.

---

## Taxonomy as semantic contract

Within the EDO semantic strategy, class hierarchies are not treated as neutral classification mechanisms.

Declaring a class as a subclass of another class represents an explicit **semantic commitment**.

In the EDO, taxonomy is understood as **contractual**:
subclassing implies full acceptance of the semantic relationships declared at the superclass level.

This means that inheriting a class also entails inheriting the space of relationships in which that class is allowed to participate.
Relationship compatibility is therefore determined by correct ontological classification, not by downstream exceptions or validation rules.

If a class must not participate in a relationship declared for its superclass, this is not a validation concern but a modelling error in the taxonomy itself.

This principle is formalised as the **Contractual Inheritance Principle**, which defines how inheritance, relationships, and semantic responsibility interact in the EDO.

For a detailed explanation, rationale, and modelling consequences, see:

[Contractual Inheritance Principle](./contractual-inheritance-principle.md)

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

## Decision criteria and modelling judgement

The semantic modelling strategy described in this document explains **how meaning is expressed and interpreted** in the EDO.

When concrete modelling decisions involve ambiguity, trade-offs, or tension between real-world fidelity and technical constraints, those decisions are guided by an explicit architectural criterion.

That criterion is documented separately in:

[Ontology Decision Criterion](./ontology-decision-criterion.md)

This separation is intentional:
- this document explains the modelling mindset
- the decision criterion defines what prevails when interpretations or solutions diverge

---

## Architectural consequence

The semantic modelling strategy described here is not an isolated choice.

It underpins:
- the use of annotations for relationships  
- the interpretation of relationships as semantic possibilities  
- the treatment of context as a core abstraction  
- the separation between semantics, validation, and governance  

Understanding this strategy is essential to understanding the EDO as a whole.
