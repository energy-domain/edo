# Energy Domain Ontology (EDO)

![EDO logo](edo-logo.png)

Welcome to the official documentation of the **Energy Domain Ontology (EDO)**.
EDO is a semantic framework for the structured representation, exchange, and validation
of information across the full lifecycle of assets in the energy sector.

**Namespace:** https://w3id.org/energy-domain/edo  
**Prefix:** `edo:`  
**Persistent URLs and stable releases:** https://w3id.org/energy-domain  

[Human-readable ontology rendering (non-normative)](./energy-domain-ontology.html)

---


## What is the EDO

The **Energy Domain Ontology (EDO)** is a formal, domain-driven ontology created to represent energy assets and their engineering information across the full asset lifecycle.

EDO is not a data format, a modelling guideline, or a software specification.  
It is a **semantic contract**: a shared, machine-readable definition of meaning, structure, and intent within the energy domain.

Its initial development focuses on complex subsea oil and gas systems, while its architectural principles are intentionally generic and extensible to other energy sectors.

---

## Why the EDO exists

Engineering information in the energy sector is traditionally:

- Fragmented across disciplines, organisations, and tools  
- Strongly document-centric  
- Weakly governed at the semantic level  
- Difficult to validate, reuse, and evolve consistently  

EDO addresses these limitations by treating **semantics as infrastructure**.

Instead of relying on informal conventions or tool-specific schemas, EDO establishes a formal semantic layer where:

- Meaning is explicit and inspectable  
- Constraints are machine-verifiable  
- Governance is embedded in the model  
- Evolution is controlled and auditable  

---

## Core principles

The EDO is guided by a small set of fundamental principles.

### Ontology as the source of truth

All normative rules, constraints, and semantic definitions are expressed **exclusively within the ontology itself**, using formal languages such as OWL and SHACL.

Textual documentation never replaces, duplicates, or overrides the ontology.

### Separation of concerns

Conceptual semantics, governance, validation, extraction, and implementation concerns are clearly separated into distinct layers, each with a well-defined role.

### Context over proliferation

Instead of uncontrolled subclassing or duplication, EDO uses explicit **contextual semantics** to express when and under which conditions concepts and relationships apply.

### Discipline-aware, not discipline-locked

EDO explicitly recognises engineering disciplines while remaining interoperable and cross-disciplinary by design.

### Tool-agnostic interoperability

EDO is designed to interoperate with existing standards and schemas without being owned by any specific tool, vendor, or platform.

---

## Architectural overview

At a high level, the EDO ecosystem is organised into:

- **Core ontology**  
  Fundamental domain concepts, relationships, and semantic primitives shared across all domains.

- **Transitional domain ontologies**  
  Discipline- or asset-specific specialisations built on top of the core, reflecting domain consensus at a given moment in time.

- **Governance ontologies**  
  Ontologies dedicated to review, maintenance, extraction, validation, and lifecycle governance.

- **Release artefacts**  
  Frozen, versioned snapshots intended for contractual, institutional, or long-term reference.

This structure allows the ontology to evolve without breaking trust, traceability, or contractual stability.

---

## Governance and evolution

EDO is designed to evolve in a controlled, transparent, and auditable manner.

Evolution is governed through:
- Explicit versioning
- Formal review and maintenance processes
- Clear separation between experimental, transitional, and released artefacts

A released version of the EDO is **immutable** and may be safely referenced in contracts, specifications, and long-term data exchanges.

---

## Relationship with IFC and other schemas

EDO does not attempt to replace existing schemas such as IFC.

Instead, it provides:
- A semantic layer above them  
- A formal interpretation of engineering intent  
- An explicit framework for governance, extraction, and validation  

Mappings, interpretations, and materialisation rules are defined formally and remain inspectable and verifiable within the ontology ecosystem.

---

## How to read the EDO

The EDO is intentionally **self-describing**.

To understand what is valid, mandatory, or constrained:
- Consult the ontology definitions (OWL)
- Consult the validation shapes (SHACL / SHACL-SPARQL)

This documentation explains *why* certain modelling decisions exist and *how to reason about them*, not *how to encode data step by step*.

---

## Documentation scope

This documentation focuses on:

- Architectural intent and modelling philosophy  
- Semantic design principles  
- Governance and lifecycle concepts  
- Interpretation of domain abstractions  

It deliberately avoids duplicating:
- Formal rules
- Mandatory structures
- Validation logic  

Those are defined exclusively in the ontology itself.

---

## Documentation structure

This documentation is organised into a small number of conceptual sections:

- [Architecture of the EDO](./architecture/architecture-of-the-edo.md)
- [Ontology Governance](./governance/ontology-governance.md)
- [Semantic Modelling Strategy](./semantics/semantic-modelling-strategy.md)
- [Transitional Domain Ontologies](./transitional/transitional-domain-ontologies.md)
- [Interoperability with IFC](./ifc/interoperability-with-ifc.md)

Each section explains *how to read and interpret* the EDO, not how to model data step by step.

---

## Scope and audience

EDO is intended for:

- Asset owners  
- Engineering contractors and suppliers  
- Software vendors  
- Data architects  
- Ontology engineers  
- Standards and interoperability initiatives  

It assumes familiarity with engineering concepts and a basic understanding of semantic technologies.

---

## Final note

The Energy Domain Ontology is not a static artefact.  
It is a **shared language**, evolving through formal governance, practical use, and collective understanding.

Its authority derives from formal semantics — not from examples, conventions, or prose.

