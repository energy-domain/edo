# EDO Ultimate Decision Criterion

This document records the **ultimate architectural and ontological decision criterion of the EDO**.  
Its purpose is to make explicit **how decisions are taken** when new needs, ambiguities, or modelling conflicts arise.

The EDO is conceived as an **epistemological infrastructure** for the energy domain:  
a semantic foundation aimed at representing the real world in a stable, evolvable, and standard-independent way.  
It is **not an IFC plugin**, nor an ontology defined by the limitations of any specific technical schema.

---

## 1. Questions that guide every ontological decision

Whenever a new modelling need arises, the following questions must be considered, in this order:

- Does this represent a **real-world entity, relationship, or attribute**, or is it merely an artefact of a standard (e.g. IFC)?
- Would this concept **still make sense** outside the context of a specific standard?
- Am I modelling the **energy domain**, or merely enabling an **immediate technical target**?
- Does this decision contribute to **semantic clarity, conceptual consistency, and evolvability** of the EDO?
- Is the primary motivation for this decision to **facilitate export, validation, serialisation, or schema compliance**?

These questions are not a technical checklist, but a **conceptual alignment instrument**.

---

## 2. When NOT to follow IFC (or any other standard)

Standards such as IFC are **targets for mapping**, not primary sources of meaning.

When there is a conflict between:

- fidelity to the real world  
- and literal adherence to a technical standard  

the correct decision is to **prioritise the real world**.

Limitations, idiosyncrasies, or gaps in standards **do not justify distortions in the EDO semantic core**.  
Such adaptations must exist **only in mapping, interoperability, or extraction layers**, never as primary conceptual definitions.

---

## 3. About decisions that “work” but drift off axis

When a decision:

- satisfies a technical specification  
- works for a specific workflow  
- or solves an immediate problem  

but violates the criteria above, this indicates that:

- the solution may be valid **within the context of the standard**
- but it is **outside the ontological axis of the EDO**

Such decisions may exist as **technical solutions**,  
but must not be incorporated into the **conceptual core** of the ontology.

---

## 4. Implicit strategic direction

If the EDO is treated merely as a **factory for IFC extensions**,  
it is natural for it to be simplified, and for part of its conceptual rigour to appear as “overengineering”.

If, on the other hand, the EDO is the basis for **data contracts, cross-domain interoperability, and long-term semantic evolution**,  
then architectural rigour is **not a luxury** — it is a **structural prerequisite**.

This document explicitly assumes the latter direction.

---

## 5. Final note

This text does not define implementation rules, nor does it replace technical discussions.  
Its role is to keep explicit the **architectural decision criterion** that guides the EDO as an epistemological infrastructure,  
especially at points where technical and conceptual solutions come into tension.

The goal is not to prevent local mistakes,  
but to ensure that the **conceptual track remains visible** over time.
