# EDO Develop Annotation Reconciliation — Context and Decisions

## Purpose

This document records the technical context, agreed principles and important decisions for reconciling the legacy annotation layer currently present in `core/energy-domain-ontology.ttl` on the `edo_develop` branch with the current EDO core and EDO-IFC mapping ontology on `main`.

The purpose of this document is to make the work reproducible and independent of chat history or individual memory.

## Technical references fixed at the start of the work

### Target branch used as legacy baseline

- Repository: `energy-domain/edo`
- Branch: `edo_develop`
- Baseline commit: `2042ffbc62c1b764d675a020478d76fa6b2def90`
- Legacy ontology under reconciliation: `core/energy-domain-ontology.ttl`

### Normative EDO core source

- Repository: `energy-domain/edo`
- Branch: `main`
- Reference commit at the start of the work: `85b7ac4fea18efd1061548a76364e821946f13a3`
- File: `core/edo.ttl`

### Normative IFC mapping source

- Repository: `energy-domain/edo`
- Branch: `main`
- Reference commit at the start of the work: `85b7ac4fea18efd1061548a76364e821946f13a3`
- File: `mappings/ifc/edo-ifc.ttl`

## Working branch

- Branch: `reconcile-edo-develop-annotations`
- Created from `edo_develop` baseline commit `2042ffbc62c1b764d675a020478d76fa6b2def90`

No ontology content shall be changed until the inventory and reconciliation plan are complete and reviewed.

---

## Architectural model to preserve

The target architecture is not a merge of the old and new annotation taxonomies.

The target architecture is composed of two complementary ontologies:

1. **EDO core (`edo.ttl`)**
   - source of truth for EDO domain concepts and EDO core annotation properties;
   - independent of IFC;
   - normative source for the EDO annotation taxonomy.

2. **EDO-IFC (`edo-ifc.ttl`)**
   - imports EDO core;
   - source of truth for EDO → IFC mapping metadata;
   - contains IFC-specific mapping annotations under its own namespace and root `edo-ifc:IFCMappingAnnotation`;
   - complements EDO rather than being folded back into the EDO core.

The future reconciled `edo_develop` is intended to be used together with the EDO-IFC mapping ontology.

---

## Core reconciliation principle

The reconciliation MUST NOT be implemented as:

> legacy annotations + annotations copied from `edo.ttl`

Instead, EDO core annotation properties in the target ontology must be reconciled against the current `edo.ttl` as the normative source.

For every legacy annotation property, the operation must be determined by comparison with the normative sources.

### Reconciliation classes

| Situation | Required action |
|---|---|
| Property exists only in `edo.ttl` | ADD to the reconciled EDO core |
| Property exists in both and is equivalent | KEEP / reproduce normative definition |
| Property exists in both but differs in taxonomy or definition | REPLACE legacy definition with `edo.ttl` definition |
| Property exists only in legacy EDO and has no valid role in either normative ontology | REMOVE |
| Property exists only in legacy EDO because its semantics moved to EDO-IFC | REMOVE from EDO core and migrate/reconcile its uses to `edo-ifc:*` |
| Legacy property is a typo or obsolete alias | REMOVE and migrate usages only when the successor is semantically unambiguous |

The comparison must consider the complete RDF definition, including at least:

- `rdf:type`
- `rdfs:subPropertyOf`
- range/domain declarations when present
- identifiers
- labels
- definitions
- alternative labels
- other metadata attached to the property

---

## Important cases already identified

### `edo:DomainRelationship`

The legacy `edo_develop` ontology contains `edo:DomainRelationship` as part of its old annotation taxonomy.

It was historically used as a relationship root but the current `edo.ttl` uses `edo:DomainRelation` instead.

Decision:

- `edo:DomainRelationship` is legacy.
- It must not be retained as a parallel root.
- It must not be linked using `owl:equivalentProperty` or preserved as a deprecated structural parent unless a later explicit decision says otherwise.
- The expected outcome is removal from the reconciled EDO core after all usages have been audited.

### `edo:hasAttribute`

`edo:hasAttribute` already exists in the legacy ontology, but its current legacy location and/or definition are not normative.

Decision:

- Existing presence does not mean “do not copy”.
- Its legacy definition must be replaced by the complete normative definition from `edo.ttl`.
- The same rule applies to every coincident IRI whose definition differs.

### IFC annotations historically stored in EDO core

The legacy ontology contains IFC-oriented annotation properties such as:

- `ifc_equivalentClass`
- `ifc_objectType`
- `ifc_predefinedType`
- and potentially other IFC mapping annotations

These concepts are now intentionally separated into `mappings/ifc/edo-ifc.ttl` under the `edo-ifc:` namespace.

Examples in the current EDO-IFC ontology include:

- `edo-ifc:IFCMappingAnnotation`
- `edo-ifc:ifc_equivalentClass`
- `edo-ifc:ifc_objectType`
- `edo-ifc:ifc_predefinedType`
- `edo-ifc:ifc_invertedDirection`
- `edo-ifc:ifc_subjectRole`
- `edo-ifc:ifc_objectRole`
- mapping-rule annotations and projection/materialisation annotations

Decision:

- IFC-specific annotations must not remain in the reconciled EDO core merely because they existed in the legacy file.
- Their definitions and usages must be compared against EDO-IFC.
- Where a legacy EDO annotation has a clear EDO-IFC successor, usages should be migrated to the EDO-IFC property in the mapping ontology, not reintroduced into EDO core.
- No automatic migration shall be performed where semantics are not demonstrably equivalent.

### Legacy annotation usages inside the ontology body

Removing only the declaration of a legacy annotation is insufficient if the property continues to be used as a predicate elsewhere.

Known examples that require usage-level audit include:

- `hasAtrribute` (legacy typo)
- `entityStatus`
- `hasExternalRef`
- IFC-specific predicates
- other annotations not present in the normative EDO core

Decision:

Every property marked for removal must be searched across the entire legacy ontology and classified by usage.

---

## Usage migration categories

Every usage of a legacy annotation selected for removal must fall into one of the following categories.

### A. Unambiguous normative successor in EDO core

Example pattern:

`legacy predicate -> current edo:* predicate`

Migration may be mechanical only after semantic equivalence is confirmed.

### B. Unambiguous successor in EDO-IFC

Example pattern:

`legacy IFC predicate in edo namespace -> edo-ifc:* predicate`

The mapping must be moved out of the EDO core architecture and represented in the complementary EDO-IFC ontology.

### C. Remodelled semantics without a 1:1 successor

No mechanical replacement.

The usage must be reviewed and a deliberate modelling decision recorded.

### D. Obsolete information

The legacy statement is no longer part of the target architecture and should be removed after review.

---

## Final-state principles

The intended final state is:

- EDO core contains only the current normative EDO annotation layer.
- EDO core contains no residual IFC-specific mapping annotation architecture.
- EDO-IFC contains IFC-specific mapping metadata.
- No legacy annotation remains declared or used accidentally.
- Existing useful information is preserved through deliberate migration where a valid target representation exists.

The final reconciliation must be based on semantic equivalence, not only local-name similarity.
