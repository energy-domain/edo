# EDO Annotation Reconciliation — Replay Runbook

## Purpose

This runbook exists so that the annotation reconciliation performed in September 2026 can be repeated later against the **then-current** state of the EDO repository, after the MDA / Flexible 2.1 reconciliation work has finished.

The objective is **not** to replay old commits mechanically.

The objective is to reproduce the same method:

- inspect the current repository state;
- freeze the new technical references;
- compare the then-current develop ontology against the then-current normative EDO and EDO-IFC;
- rebuild the inventories and reconciliation matrix from scratch;
- obtain explicit approval before editing TTL;
- implement in small reversible commits;
- validate by parsed RDF graph, not only by serialized-text counts;
- produce a final validation and integration review.

This document is intentionally written as a procedure that remains useful even if classes, annotations, mappings, branch names or counts have changed substantially.

---

## Strategic context

The reconciliation is a prerequisite for a larger consolidation effort in which semantic information currently spread across multiple artifacts should move into EDO / EDO-IFC so that downstream products can be generated from the ontology itself.

The intended later work includes, among other things:

1. modelling the relationships between `DomainElement` classes in EDO;
2. migrating relationship information currently represented only in diagrams into EDO;
3. moving information that is semantically part of the domain model but currently lives incorrectly in SHACL into EDO;
4. modelling IFC Property Set / Property mappings currently hardcoded in extractors inside EDO-IFC;
5. modifying extractors so their source of truth is EDO + EDO-IFC rather than parallel hardcoded artefacts;
6. accelerating generation of discipline-specific subproducts for domains such as flexible pipes, umbilicals, ANM/WCT and others.

The reconciliation must only be resumed when the team can safely change the ontology without disturbing the active MDA / Flexible 2.1 alignment work.

---

## Fundamental rule: start from the future repository, not from today's reconciled TTL

When this work is resumed, do **not** assume that the September 2026 reconciled branch is still technically correct.

The future run must treat the repository state at that time as source of truth.

The September 2026 branch and its documentation are evidence of method and prior decisions, not a substitute for a fresh comparison.

In particular:

- do not cherry-pick the old reconciliation commits blindly;
- do not copy the old `energy-domain-ontology.ttl` over the future file;
- do not reuse old usage counts as acceptance criteria;
- do not assume the same set of AnnotationProperties still exists;
- do not assume the same IFC controlled-resource gaps still exist;
- do not assume the old `LegacyAnnotation` compatibility set remains necessary or sufficient;
- do not assume the future MDA reconciliation has not changed semantics relevant to annotations or mappings.

Everything structural must be re-derived from the future repository.

---

## Sources of truth for the future run

At the start of the replay, identify and freeze three technical sources.

### A. Future destination ontology

The ontology that will receive the reconciliation, expected to be the evolved develop / MDA-aligned ontology, for example:

```text
core/energy-domain-ontology.ttl
```

Record:

- branch;
- exact commit SHA;
- blob SHA when useful;
- file path.

This is the future equivalent of the September 2026 `edo_develop` baseline.

### B. Future normative EDO core

Identify the then-current authoritative EDO core, expected to include the normative annotation taxonomy and relationships, for example:

```text
core/edo.ttl
```

Record its exact commit SHA.

### C. Future normative EDO-IFC

Identify the then-current mapping ontology, expected at:

```text
mappings/ifc/edo-ifc.ttl
```

Record its exact commit SHA.

EDO-IFC is a separate source of truth for IFC-specific mapping semantics. Do not move IFC mapping annotations back into EDO core merely for convenience.

---

## Architecture to preserve unless a new explicit decision changes it

The architectural intent established in the September 2026 work was:

- EDO core contains domain/metamodel semantics;
- EDO-IFC contains IFC-specific mapping semantics;
- EDO core should remain IFC-independent;
- consuming applications may compose the appropriate EDO and EDO-IFC versions explicitly;
- avoid creating an import structure that causes a develop ontology to pull a different canonical EDO version transitively.

If the future ontology architecture has evolved, reassess this explicitly rather than silently carrying this rule forward.

---

# Replay procedure

## Phase 0 — Freeze the future technical state

Before any ontology edit:

1. inspect the current repository and relevant branches;
2. identify the future destination ontology;
3. identify the current normative EDO core;
4. identify the current EDO-IFC;
5. record exact commit SHAs;
6. create a dedicated reconciliation branch from the destination baseline;
7. document all frozen references.

Recommended branch naming pattern:

```text
reconcile-edo-develop-annotations-YYYYMM
```

or another name that makes the replay distinguishable from the September 2026 branch.

### Gate 0

No TTL edit before the technical baseline and normative references are frozen.

---

## Phase 1 — Rebuild the normative annotation inventories

### 1A. EDO core

Extract the complete set of current EDO-namespace `owl:AnnotationProperty` resources from the future normative `core/edo.ttl`.

For each property capture its complete RDF declaration, including when present:

- `rdf:type`;
- `rdfs:subPropertyOf`;
- `rdfs:domain`;
- `rdfs:range`;
- labels;
- definitions;
- identifiers;
- alternative labels;
- governance / metadata statements;
- any other declaration triples.

Do **not** reduce comparison to property names or hierarchy only.

Produce a complete tree / inventory and record the count.

### 1B. EDO-IFC

Extract the complete current set of EDO-IFC annotation properties and controlled resources relevant to mappings.

At minimum inventory:

- mapping AnnotationProperties;
- controlled IFC entity resources;
- IFC role resources;
- materialisation modes;
- mapping rules;
- any other controlled vocabulary that can be the value of migrated annotations.

### Output

Create/update a future equivalent of:

```text
docs/reconciliation/normative-annotation-inventory.md
```

### Important

The September 2026 result was 79 normative EDO AnnotationProperties and 26 EDO-IFC AnnotationProperties. These numbers are historical facts only. The future run must calculate its own counts.

---

## Phase 2 — Rebuild the destination/legacy inventory

Extract every EDO-namespace `owl:AnnotationProperty` declared in the future destination ontology.

For every property record:

- parent hierarchy;
- complete declaration metadata;
- whether it exists in current normative EDO;
- whether an IFC-specific successor exists in current EDO-IFC;
- actual usages in the ontology body;
- candidate preliminary action.

### Count both serialization occurrences and RDF triples

This is a lesson learned from the September 2026 execution.

For each live predicate, distinguish:

1. **serialized Turtle predicate occurrences** — useful for locating edits;
2. **parsed RDF triples using that predicate** — authoritative for semantic preservation.

A single Turtle predicate occurrence may contain several comma-separated objects, so the two values can differ.

Future validation must use the RDF graph counts as the preservation criterion.

### Output

Create/update a future equivalent of:

```text
docs/reconciliation/legacy-annotation-inventory.md
```

---

## Phase 3 — Build a fresh reconciliation matrix

Do not assume the old 33-property matrix still applies.

For every destination AnnotationProperty classify both:

- declaration action;
- usage action.

Use action categories such as:

### `ADD_CURRENT_EDO`

Property exists in current normative EDO but not in destination.

Action: add complete normative declaration.

### `REPLACE_WITH_EDO_DEFINITION`

Same IRI exists in destination and normative EDO, but declaration/taxonomy differs.

Action: replace the destination declaration with the complete current normative declaration. Existing usages remain unchanged unless a separate semantic reason requires migration.

### `KEEP_IDENTICAL`

Declaration is already semantically identical.

### `MIGRATE_TO_EDO_IFC`

Legacy EDO-core annotation represents IFC mapping semantics that now belong in EDO-IFC.

Action: migrate predicate and, where required, value shape.

### `PRESERVE_LEGACY_COMPATIBILITY`

Property is not part of current normative EDO but carries information that must not be discarded and has no approved current equivalent.

Action: preserve explicitly in a separate compatibility area if still appropriate.

### `FIX_LEGACY_TYPO`

Unambiguous typo/alias with a known canonical successor.

### `REMOVE_OBSOLETE`

Property and its information are genuinely obsolete.

### `REVIEW_NO_1_TO_1_SUCCESSOR`

No safe mechanical migration exists. Human semantic decision required.

### Critical rule

Never map properties only because their names look similar.

Examples from the September 2026 work that must not become automatic rules:

- `entityStatus` must not automatically become `conceptStatus`;
- `hasExternalRef` must not automatically become `hasClassificationReference`;
- `hasEnd` must not automatically become `hasConnectionPoint`.

In a future run those relationships may have evolved, but any mapping still requires explicit semantic evidence.

### Output

Create/update:

```text
docs/reconciliation/annotation-reconciliation-matrix.md
```

### Gate 3

All destination AnnotationProperties must have an approved action before implementation planning.

---

## Phase 4 — Audit every live usage

For every property being removed, renamed or migrated, audit all usages.

Classify each usage into one of four semantic cases:

### A. Clear successor in EDO core

Mechanical migration allowed after validation.

### B. Clear successor in EDO-IFC

Mechanical predicate migration allowed; check whether the value representation also changed.

### C. No 1:1 successor / remodelled semantics

Requires explicit decision.

### D. Obsolete data

Remove only after explicit approval.

For same-IRI properties whose declaration changes but whose semantics remain the same, preserve body uses unchanged.

### Output

Create/update:

```text
docs/reconciliation/annotation-usage-migration-audit.md
```

---

## Phase 5 — Audit IFC controlled-resource migration

This phase is required whenever legacy equivalent-class mappings use literals or other value forms while current EDO-IFC expects controlled resources.

For every distinct legacy IFC value:

1. identify exact frequency in the RDF graph;
2. test for exact existing controlled EDO-IFC resource;
3. classify as:
   - exact existing target;
   - missing controlled resource;
   - special sentinel / invalid IFC entity;
   - semantically ambiguous;
4. do not invent resources silently;
5. define controlled resources first when required;
6. explicitly classify placeholders such as `"-"` as no-mapping rather than manufacturing a fake IFC class.

### Output

Create/update:

```text
docs/reconciliation/ifc-equivalent-class-mapping.md
```

and, if necessary:

```text
docs/reconciliation/ifc-mapping-migration-plan.md
```

---

## Phase 6 — Produce the executable TTL change plan

Before editing any TTL, write the exact operation-level plan.

The plan must state:

- files to change;
- properties/resources to add;
- declarations to replace;
- compatibility branch to create/preserve;
- typos to fix;
- predicate migrations;
- value conversions;
- controlled resources to add;
- placeholders to remove;
- exact post-change invariants;
- validation procedure;
- intended commit sequence.

Prefer small reversible commits grouped by semantic operation.

Example structure:

1. extend EDO-IFC controlled vocabulary if necessary;
2. reconcile/add normative EDO annotation taxonomy;
3. create/preserve approved compatibility annotations;
4. fix deterministic typos/aliases;
5. migrate IFC mapping assertions;
6. mechanical cleanup only if required.

### Output

Create/update:

```text
docs/reconciliation/ttl-change-plan.md
```

### Gate 6 — mandatory approval gate

**Do not edit either TTL until this plan is explicitly approved.**

This was a core discipline of the September 2026 process and should be preserved.

---

## Phase 7 — Implement in small commits

After approval:

- execute one semantic operation per commit where practical;
- avoid bundling unrelated ontology changes;
- preserve rollback capability;
- do not mix reconciliation with new domain modelling that belongs to subsequent work packages;
- do not opportunistically redesign ontology structures outside the approved scope.

If the target file is very large, deterministic scripts or temporary CI may be used to avoid unsafe manual full-file rewrites, provided that:

- transformation rules are fail-fast;
- they operate only on approved scopes;
- semantic validation occurs before push;
- temporary execution machinery is removed afterward unless intentionally retained as a permanent repository tool.

---

## Phase 8 — Validate the result semantically

### Parse both TTLs

Parse the changed files as RDF/Turtle.

### Normative declaration equivalence

For every current normative EDO AnnotationProperty, compare the set of RDF declaration triples in the target with the normative source.

Do not rely only on textual similarity.

### Compatibility branch invariants

Verify:

- only explicitly approved compatibility properties survive outside the normative set;
- compatibility roots remain independent where intended;
- no normative property is accidentally reparented under a legacy root.

### Data preservation

For each predicate whose usages must be preserved, compare parsed RDF triples against the frozen destination baseline.

This is authoritative.

### Typo/alias validation

Verify obsolete typo IRIs have zero declarations and zero usages.

### IFC validation

Verify:

- zero legacy IFC annotation usages remain when migration is intended to be complete;
- equivalent-class mappings use the expected controlled-resource value shape;
- no literal remains where a controlled resource is required;
- every controlled target actually exists in EDO-IFC;
- no fake resource exists for placeholders/sentinels;
- object type / predefined type values remain unchanged where the approved migration said only the predicate namespace changes.

### Composition validation

Verify ontology imports and explicit composition behavior match the approved architecture.

### Spot checks

Always perform representative human-readable checks for:

- at least one same-IRI annotation whose taxonomy changed;
- one compatibility annotation;
- one typo/alias correction if applicable;
- one mapping to an already-existing IFC controlled resource;
- one mapping to a newly-added IFC controlled resource, if any;
- one sentinel/no-mapping case, if any.

### Output

Create/update:

```text
docs/reconciliation/validation-report.md
```

---

## Phase 9 — Final drift and integration review

Immediately before integration:

1. check the current normative branch head again;
2. compare it with the commit frozen in Phase 0;
3. if normative EDO or EDO-IFC changed materially, reconcile that drift before integration;
4. compare the working branch against the frozen destination baseline;
5. verify temporary tooling is removed;
6. document the final technical state;
7. only then decide PR / merge target.

### Output

Create/update:

```text
docs/reconciliation/final-review.md
```

---

# What from September 2026 may be reused

The following are reusable as **methodological precedents**:

- the phase structure;
- the rule to freeze exact commits;
- the three-source comparison EDO / EDO-IFC / destination ontology;
- the distinction between declaration migration and usage migration;
- the mandatory usage audit before removing a property;
- the separate compatibility branch concept;
- the rule not to map by name similarity alone;
- the controlled-resource migration pattern for IFC values;
- the Phase-6 approval gate;
- small reversible commits;
- graph-based validation;
- final normative drift check;
- temporary-tool cleanup.

The existing documents under `docs/reconciliation/` can be read as worked examples.

---

# What must NOT be reused without recalculation

Do not treat any of the following September 2026 values as future truth:

- 79 normative EDO AnnotationProperties;
- 26 EDO-IFC AnnotationProperties;
- 33 legacy AnnotationProperties;
- 59 additions;
- 20 overlapping declarations;
- 10 compatibility annotations;
- the exact `LegacyAnnotation` subtree;
- 274 `ifc_equivalentClass` mappings;
- 270 `ifc_objectType` mappings;
- 268 `ifc_predefinedType` mappings;
- the list of 11 missing IFC resources;
- any old textual occurrence count;
- any old RDF triple count;
- old commit SHAs as the future source of truth.

Those values describe only the September 2026 execution.

---

# Definition of done for a replay

A future reconciliation is complete only when all of the following are true:

1. future destination, EDO and EDO-IFC references are frozen by exact commit;
2. current normative and destination annotation inventories are complete;
3. every destination AnnotationProperty has an approved declaration and usage action;
4. every removed/migrated live usage is accounted for;
5. controlled IFC-value gaps are resolved explicitly;
6. the executable TTL plan has been approved;
7. implementation is complete in reviewable commits;
8. changed Turtle files parse successfully;
9. normative declarations match current normative sources semantically;
10. preservation checks pass on parsed RDF graphs;
11. obsolete aliases/legacy IFC predicates expected to disappear are absent;
12. all equivalent-class targets resolve to valid controlled resources;
13. the final normative drift check is clean or reconciled;
14. a final validation report and integration review exist.

---

# Recommended replay prompt

When the MDA / Flexible 2.1 reconciliation is finished and the ontology is again available for structural evolution, start a new ChatGPT conversation and send a prompt equivalent to the following:

```text
@GitHub

Vamos repetir a reconciliação das AnnotationProperties da EDO usando o procedimento documentado em:

docs/reconciliation/reconciliation-replay-runbook.md

Repositório:
https://github.com/energy-domain/edo

A situação de setembro de 2026 serve apenas como precedente metodológico. Não reutilize os antigos TTLs, commits, contagens ou matrizes como fonte de verdade.

Antes de qualquer alteração:

1. consulte o estado atual do repositório;
2. identifique a ontologia destino atual depois da conciliação com o MDA;
3. identifique a EDO core normativa atual;
4. identifique a EDO-IFC normativa atual;
5. fixe e informe explicitamente os commits que serão usados;
6. crie uma nova branch de reconciliação a partir do estado atual da ontologia destino;
7. refaça do zero os inventários e a matriz de reconciliação seguindo o runbook;
8. use os documentos de setembro de 2026 apenas como exemplos de método e decisões históricas;
9. não altere nenhum TTL antes de eu aprovar o novo Phase-6 TTL Change Plan;
10. para contagens de preservação, use o grafo RDF parseado como critério autoritativo e mantenha separadas as contagens de ocorrências textuais.

O objetivo é obter, sobre o estado atual da EDO, o mesmo nível de reconciliação, rastreabilidade, aprovação e validação que obtivemos no processo de setembro de 2026.
```

This prompt is intentionally source-driven. It forces a new run to re-discover the ontology state instead of assuming that the September 2026 result can simply be replayed.

---

## Historical reference: September 2026 replay precedent

For traceability only, the first completed execution used:

- destination baseline: `2042ffbc62c1b764d675a020478d76fa6b2def90`;
- normative EDO / EDO-IFC: `85b7ac4fea18efd1061548a76364e821946f13a3`;
- working branch: `reconcile-edo-develop-annotations`.

Its permanent artifacts under `docs/reconciliation/` include the context, inventories, matrix, usage audit, IFC mapping audit, change plan, validation report and final review.

These references exist to make the reasoning auditable, **not** to pin the next replay to an obsolete ontology state.
