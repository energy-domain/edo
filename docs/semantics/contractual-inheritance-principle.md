# Contractual Inheritance Principle

## Principle Name
**Contractual Inheritance Principle**

---

## Statement

In the Energy Domain Ontology (EDO), **class hierarchies are not merely classificatory; they are contractual**.

Declaring a class as a subclass of another class implies **full acceptance of all semantic contracts associated with the superclass**, including its declared domain relationships.

In other words:

> **To inherit a class is to inherit its relationships.**

---

## Formal Interpretation

Given the declaration:

```ttl
ClassA rel ClassB .
```

and a taxonomic hierarchy:

```ttl
ClassC rdfs:subClassOf ClassB .
ClassD rdfs:subClassOf ClassB .
```

the following interpretation applies:

- `ClassC` and `ClassD` are **valid targets** for the relationship `rel` originating from `ClassA`
- this validity is derived **by inheritance**, not by explicit repetition of relationships
- no additional triples are required to materialise this compatibility

---

## Modelling Consequence

This principle imposes a strict and intentional discipline on ontology design:

- If a class **must not** participate in a relationship inherited from its superclass,
  then it **must not** be modelled as a subclass of that superclass.

Therefore:

> **Relationship incompatibility is a modelling error in the taxonomy, not a special case to be handled downstream.**

This shifts the responsibility from validation and exception handling to **correct ontological classification**.

---

## Benefits

Adopting the Contractual Inheritance Principle yields several structural advantages:

- prevents silent semantic drift in class hierarchies
- avoids duplication of relationship declarations
- enables automatic expansion of allowed relationships via taxonomy
- improves quality of extracted schemas (e.g. IFC, JSON, bsDD)
- provides immediate feedback during ontology evolution

---

## Operational Implications

This principle is especially effective in design-time tooling scenarios:

- schema generation
- model authoring interfaces (e.g. CAD / DCC tools)
- guided relationship selection
- prevention of invalid modelling choices before project data exists

By enforcing relationship compatibility at the taxonomic level, the EDO ensures that downstream tools remain simple, deterministic, and robust.

---

## Summary

> **In the EDO, taxonomy carries semantic responsibility.**  
> Subclassing is not a neutral act — it is an explicit acceptance of inherited relational contracts.

This principle is foundational to maintaining a clean, scalable, and semantically rigorous ontology.
