# Interoperability with IFC

## Purpose of this section

This section explains the **philosophy adopted by the Energy Domain Ontology (EDO) for interoperability with IFC and similar schemas**.

It clarifies the conceptual relationship between EDO and IFC, and how semantic interpretation, governance, and validation are positioned relative to schema-based data models.

This document does not define mapping rules or implementation details.
It explains how interoperability should be **understood and reasoned about**.

---

## EDO and IFC: different roles, complementary purposes

EDO does not attempt to replace IFC.

The two serve fundamentally different purposes:

- **IFC** is a schema designed for structured data exchange and persistence.
- **EDO** is an ontology designed to express semantic meaning, intent, and governance.

EDO operates *above* schemas such as IFC, providing a semantic layer that interprets, constrains, and contextualises schema-based data without being bound to a specific data model.

---

## Schema semantics versus domain semantics

IFC encodes meaning primarily through:
- entity structures
- attributes
- predefined relationships
- formal constraints embedded in the schema

This form of semantics is necessary for interoperability, but it is inherently limited to what can be stabilised at schema level.

EDO addresses a different layer of meaning:
- engineering intent
- contextual applicability
- contractual interpretation
- lifecycle-dependent semantics

These aspects cannot be fully expressed within a fixed exchange schema without compromising flexibility or long-term stability.

---

## Ontology as a semantic interpretation layer

In the EDO ecosystem, IFC is interpreted through the ontology.

This means that:
- IFC entities are not treated as semantic primitives
- meaning is derived through ontological interpretation
- multiple semantic readings of the same IFC structure may coexist, depending on context

EDO defines *how IFC data should be understood*, not merely *how it is structured*.

---

## Declarative mapping philosophy

Interoperability between EDO and IFC is based on a **declarative mapping philosophy**.

Rather than embedding semantics directly into schema constraints or hard-coded transformations, EDO expresses:
- semantic correspondence
- interpretation rules
- applicability conditions

These declarations remain explicit, inspectable, and governable.

This approach avoids:
- brittle one-to-one mappings
- premature semantic freezing
- implicit assumptions hidden in transformation code

---

## Separation between semantics and materialisation

EDO deliberately separates:
- **semantic interpretation** (what data means)
- **materialisation** (how data is represented in a schema)

This separation ensures that:
- semantic evolution does not require schema redesign
- the same semantic model can support multiple schema versions
- schema constraints do not dictate domain meaning

Materialisation is treated as a controlled act, governed by explicit rules and context.

---

## Validation and interoperability

Validation in the context of IFC interoperability is not universal.

What is valid depends on:
- lifecycle phase
- contractual scope
- domain responsibility
- intended use of the data

EDO enables context-aware validation by:
- interpreting IFC data semantically
- applying appropriate validation layers
- separating schema validity from semantic acceptability

This reflects real-world engineering practice, where data may be schema-valid but semantically incomplete or inappropriate for a given purpose.

---

## Avoiding semantic lock-in

A central goal of the EDO–IFC interoperability strategy is to avoid semantic lock-in.

EDO:
- is not bound to a specific IFC version
- does not encode domain meaning exclusively through IFC constructs
- remains open to interoperability with other schemas and formats

IFC is treated as one important interoperability surface, not as the semantic foundation of the domain.

---

## Architectural consequence

The interoperability philosophy described here supports:

- long-term semantic stability
- controlled evolution of both ontology and schemas
- coexistence of multiple representations
- clear separation of concerns

Understanding this philosophy is essential to interpreting how EDO relates to IFC without conflating schema structure with domain meaning.
