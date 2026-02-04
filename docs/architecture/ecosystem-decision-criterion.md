# EDO Ecosystem – Architectural Decision Criterion

This document records the **architectural decision criterion of the EDO ecosystem**.  
Its purpose is to make explicit **how the ecosystem is conceived, structured, and allowed to evolve** over time.

The EDO ecosystem is not a single artefact, tool, or ontology.  
It is a **coherent system of artefacts, processes, and responsibilities** designed to support semantic modelling, governance, interoperability, and long-term evolution.

---

## 1. What the EDO ecosystem is

The EDO ecosystem exists to support the EDO as an **epistemological infrastructure**, not merely as a technical deliverable.

It encompasses, among others:

- the core ontology (EDO)
- transitional and domain-specific extensions
- governance artefacts
- extraction and mapping mechanisms
- validation and quality control structures
- documentation and decision records

Each artefact has a **clear role within the system**, and no single artefact defines the ecosystem on its own.

---

## 2. Separation of concerns as a first-class principle

The ecosystem is intentionally structured around **clear separation of concerns**, including but not limited to:

- domain semantics vs. technical standards
- core ontology vs. mappings and extractions
- stable concepts vs. transitional or contractual artefacts
- decision criteria vs. implementations

Blurring these boundaries may simplify short-term implementation,  
but it weakens the ecosystem’s ability to evolve coherently over time.

---

## 3. Tooling does not define meaning

Tools, schemas, formats, and platforms (e.g. IFC, SHACL, CDEs, pipelines) are **means**, not drivers.

The ecosystem is not shaped around the limitations or affordances of tools.  
Instead, tools are selected, adapted, or replaced to serve **pre-existing semantic and architectural intent**.

A decision that exists solely to accommodate a tool or platform  
does not belong to the conceptual backbone of the ecosystem.

---

## 4. Evolution over optimisation

The EDO ecosystem prioritises **long-term semantic evolution** over short-term optimisation.

This implies that:

- some solutions may appear heavier or more complex initially
- redundancy may exist temporarily to preserve clarity
- transitions may coexist with stable structures

These are intentional characteristics of a system designed to evolve,  
not symptoms of overengineering.

---

## 5. About deviations and local solutions

Local, tool-oriented, or contract-driven solutions are **expected to emerge** within the ecosystem.

Such solutions are not errors by default.  
They become problematic only when they:

- redefine core concepts
- collapse separation of concerns
- or impose local constraints as global meaning

The role of the ecosystem is not to prevent such solutions,  
but to **contain them in the appropriate layer**.

---

## 6. Implicit strategic direction

If the ecosystem is treated merely as a **delivery pipeline for specific standards or contracts**,  
it will naturally converge towards efficiency and simplification.

If it is treated as a **foundation for cross-domain data contracts, semantic governance, and long-term interoperability**,  
then architectural discipline and conceptual clarity are **structural necessities**.

This document assumes and supports the latter direction.

---

## 7. Final note

This text does not prescribe processes or organisational structure.  
It exists to make explicit the **architectural intent of the EDO ecosystem**.

Its purpose is to ensure that, even as artefacts, tools, and people change,  
the **ecosystem remains coherent**, and its underlying intent remains visible.
