# EDO Develop Annotation Reconciliation — Work Plan

## Objective

Reconcile the annotation layer and all legacy annotation usages in `core/energy-domain-ontology.ttl` from the `edo_develop` lineage against the current normative architecture defined by:

- `core/edo.ttl` for EDO core annotations; and
- `mappings/ifc/edo-ifc.ttl` for IFC-specific mapping annotations.

The work must preserve useful legacy information where a valid current representation exists, while eliminating obsolete or misplaced annotation architecture.

No ontology change should be made before the inventory and reconciliation matrix are complete and reviewed.

---

## Phase 0 — Freeze references and protect the work

### Inputs

- Legacy baseline: `edo_develop` at commit `2042ffbc62c1b764d675a020478d76fa6b2def90`
- Current EDO/EDO-IFC reference: `main` at commit `85b7ac4fea18efd1061548a76364e821946f13a3`
- Working branch: `reconcile-edo-develop-annotations`

### Actions

1. Keep the working branch based on the frozen legacy baseline.
2. Record any later movement of `main` explicitly before using newer normative files.
3. Do not mix unrelated ontology changes into this branch.

### Deliverable

- Reproducible technical baseline.

---

## Phase 1 — Inventory current normative annotations

### 1A. EDO core

Extract every EDO annotation property declared in `core/edo.ttl`.

For each property record:

- IRI/local name
- complete declaration triples
- parent annotation property
- root/family in the annotation taxonomy
- labels
- identifiers
- definitions
- alt labels
- range/domain if present
- relevant notes/examples

### 1B. EDO-IFC

Extract every annotation property declared in `mappings/ifc/edo-ifc.ttl`.

For each property record the same information, plus:

- whether it is a direct or indirect descendant of `edo-ifc:IFCMappingAnnotation`
- its intended mapping role
- whether it appears to be a successor of a legacy EDO-core IFC annotation

### Deliverable

`docs/reconciliation/normative-annotation-inventory.md`

---

## Phase 2 — Inventory legacy annotations in `edo_develop`

Extract every annotation property declared in `core/energy-domain-ontology.ttl`.

For each property record:

- complete RDF definition
- taxonomy position
- number of occurrences as predicate across the ontology
- representative usage locations
- whether its local name also exists in current EDO core
- whether its local name or semantics exists in EDO-IFC

Explicitly include old roots/categories such as `DomainAnnotation`, `DomainRelationship` and all descendants.

### Deliverable

`docs/reconciliation/legacy-annotation-inventory.md`

---

## Phase 3 — Build the reconciliation matrix

Compare each legacy property against both normative ontologies.

### Required status values

- `ADD_FROM_EDO`
- `KEEP_NORMATIVE_EDO`
- `REPLACE_WITH_EDO_DEFINITION`
- `MIGRATE_TO_EDO_IFC`
- `REMOVE_OBSOLETE`
- `REVIEW_NO_1_TO_1_SUCCESSOR`
- `FIX_LEGACY_TYPO`

### Required fields

| Field | Description |
|---|---|
| Legacy property | IRI/local name in `edo_develop` |
| Legacy parent | Current legacy taxonomy location |
| Legacy usages | Count and summary |
| EDO core match | Normative EDO property, if any |
| EDO-IFC match | Mapping property, if any |
| Semantic equivalence | yes / partial / no / uncertain |
| Proposed action | One of the status values above |
| Usage migration | What happens to statements using the legacy property |
| Decision required | yes/no |
| Notes | Rationale and edge cases |

### Known cases that must appear

- `DomainRelationship`
- `DomainAnnotation`
- `hasAttribute`
- `hasAtrribute`
- `entityStatus`
- `hasExternalRef`
- `ifc_equivalentClass`
- `ifc_objectType`
- `ifc_predefinedType`
- every other IFC-oriented legacy annotation

### Deliverable

`docs/reconciliation/annotation-reconciliation-matrix.md`

No ontology edits before review of this matrix.

---

## Phase 4 — Audit every usage of properties marked for removal or migration

For every property with status:

- `MIGRATE_TO_EDO_IFC`
- `REMOVE_OBSOLETE`
- `REVIEW_NO_1_TO_1_SUCCESSOR`
- `FIX_LEGACY_TYPO`

search the whole ontology body and classify every statement using it.

### Usage classes

1. **Direct EDO-core successor**
2. **Direct EDO-IFC successor**
3. **Semantics remodelled; human decision needed**
4. **Obsolete statement**
5. **Potential data loss risk**

### Important rule

Do not infer equivalence merely from similar local names.

Example: `entityStatus` must not automatically become another status property without comparing definitions and intended usage.

### Deliverable

`docs/reconciliation/legacy-usage-audit.md`

---

## Phase 5 — Decide location of migrated IFC mapping statements

Because the reconciled EDO core is intended to be complemented by `edo-ifc.ttl`, IFC-specific statements currently embedded in the legacy ontology must be reassigned deliberately.

For every legacy IFC mapping statement decide whether it should:

1. be represented directly in `edo-ifc.ttl` on the corresponding EDO resource;
2. be represented using one of the structured mapping-rule resources already defined by EDO-IFC;
3. be removed because the legacy representation is obsolete or superseded;
4. remain pending because there is no semantically equivalent EDO-IFC representation.

### Deliverable

`docs/reconciliation/ifc-mapping-migration-plan.md`

---

## Phase 6 — Prepare an explicit patch plan

Before changing TTL, produce an operation-level plan containing:

### EDO core changes

- annotation declarations to remove
- declarations to replace
- declarations to add from `edo.ttl`
- legacy predicate usages to update/remove

### EDO-IFC changes

- mapping statements to add or update
- namespace changes (`edo:*` legacy mapping predicate -> `edo-ifc:*`)
- any new mapping resources required

### Safety checks

- no property removed while unresolved usages remain
- no information moved to EDO-IFC without a documented semantic mapping
- no duplicate old/new annotation roots

### Deliverable

`docs/reconciliation/ttl-change-plan.md`

This document is the approval gate for implementation.

---

## Phase 7 — Implement in small commits

Recommended commit sequence:

1. Replace/add normative EDO annotation taxonomy declarations.
2. Fix unambiguous legacy typos and EDO-core successor usages.
3. Migrate unambiguous IFC mapping annotations/usages to EDO-IFC.
4. Remove obsolete legacy annotation declarations and statements.
5. Apply individually approved remodelled cases.
6. Cleanup formatting/generated ontology sections only if necessary.

Each commit should be narrowly scoped and reversible.

---

## Phase 8 — Validation

### Structural validation

Verify that the reconciled EDO core has no unintended legacy annotation declarations.

Target invariant:

> Every EDO-core annotation property in the reconciled ontology is justified by the normative EDO core architecture.

### Legacy predicate validation

Verify that no predicate selected for removal still occurs anywhere in the reconciled EDO core.

### IFC separation validation

Verify that IFC-specific mapping metadata uses EDO-IFC vocabulary and is not reintroduced into EDO core.

### Import/composition validation

Load the reconciled EDO core together with `edo-ifc.ttl` and verify:

- resolvable imports
- no accidental duplicate mapping vocabulary in the EDO namespace
- expected mapping assertions remain available in the combined model

### Semantic spot checks

At minimum test resources that previously used:

- `hasAttribute` / `hasAtrribute`
- `ifc_equivalentClass`
- `ifc_objectType`
- `ifc_predefinedType`
- status/governance annotations
- relationship annotations

### Deliverable

`docs/reconciliation/validation-report.md`

---

## Phase 9 — Final review and integration decision

Before merging:

1. Compare the working branch against the frozen `edo_develop` baseline.
2. Re-check current `main` for changes made after reference commit `85b7ac4fea18efd1061548a76364e821946f13a3`.
3. If normative files changed materially, explicitly reconcile those changes before merge.
4. Review all decisions marked as human-required.
5. Open a PR with links to the reconciliation matrix and validation report.

---

## Acceptance criteria

The work is complete only when all of the following are true:

- [ ] The legacy and normative annotation inventories are complete.
- [ ] Every legacy annotation property has an explicit reconciliation status.
- [ ] Every usage of every removed/migrated property has been accounted for.
- [ ] No legacy annotation root survives accidentally.
- [ ] `hasAttribute` follows the current EDO definition/taxonomy.
- [ ] `DomainRelationship` is removed unless an explicit later decision reverses this.
- [ ] IFC-specific annotation definitions are not retained in EDO core.
- [ ] Valid IFC mappings are represented through EDO-IFC.
- [ ] No legacy IFC predicate remains in the reconciled EDO core unintentionally.
- [ ] The combined EDO + EDO-IFC model loads consistently.
- [ ] A validation report documents all checks and remaining limitations.

---

## Working rule for future discussions

Any new decision made during this work that changes taxonomy, migration semantics, or acceptance criteria must be recorded in the branch documentation before implementation. The Git branch, not chat memory, is the durable project record.
