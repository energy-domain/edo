# TTL Change Plan — Approval Gate

## Purpose

This Phase-6 document is the operation-level plan required before any ontology TTL is edited.

It consolidates the approved reconciliation matrix, usage audit and IFC mapping migration analysis into an executable sequence.

No TTL is modified by this document.

## Frozen references

- develop baseline: `core/energy-domain-ontology.ttl` at commit `2042ffbc62c1b764d675a020478d76fa6b2def90`;
- normative EDO core: `core/edo.ttl` at `main` commit `85b7ac4fea18efd1061548a76364e821946f13a3`;
- normative EDO-IFC: `mappings/ifc/edo-ifc.ttl` at the same `main` commit;
- working branch: `reconcile-edo-develop-annotations`.

## Target architecture

The reconciled develop ontology will use:

1. the complete current EDO AnnotationProperty layer from the pinned `edo.ttl`;
2. a separate transitional `edo:LegacyAnnotation` branch for explicitly approved legacy metadata;
3. EDO-IFC predicates and controlled resources for IFC mapping assertions;
4. no legacy IFC mapping AnnotationProperty declarations in the `edo:` namespace.

The EDO and EDO-IFC vocabularies remain architecturally separate.

## Important composition rule

Do **not** add `owl:imports <https://w3id.org/energy-domain/edo/mappings/ifc>` to the develop ontology merely to use EDO-IFC terms.

Reason: the EDO-IFC ontology itself imports the canonical EDO ontology URI. Making develop import EDO-IFC could therefore cause a loader to pull the canonical EDO alongside the develop variant and unintentionally mix the two ontology versions.

Instead:

- add the `edo-ifc:` prefix to develop;
- use EDO-IFC IRIs in mapping assertions;
- load/compose develop and EDO-IFC explicitly in consuming applications when both are required.

## Commit 1 — Extend the controlled IFC vocabulary

### File

`mappings/ifc/edo-ifc.ttl`

### Add six `IFCObjectEntity` individuals

- `edo-ifc:IfcCovering`
- `edo-ifc:IfcActuator`
- `edo-ifc:IfcTask`
- `edo-ifc:IfcActor`
- `edo-ifc:IfcJunctionBox`
- `edo-ifc:IfcFastener`

Each declaration shall follow the existing controlled-resource pattern:

```turtle
edo-ifc:IfcX
    rdf:type owl:NamedIndividual ;
    rdf:type edo-ifc:IFCObjectEntity ;
    rdfs:label "IfcX"@en ;
    edo-ifc:ifcEntityName "IfcX" ;
    skos:exactMatch <https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcX> ;
    rdfs:seeAlso <https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcX.htm> ;
    dcterms:identifier "IfcX" .
```

### Add five direct `IFCEntity` individuals

- `edo-ifc:IfcMaterial`
- `edo-ifc:IfcClassificationReference`
- `edo-ifc:IfcClassification`
- `edo-ifc:IfcProject`
- `edo-ifc:IfcPerson`

These shall use the same pattern except:

```turtle
rdf:type edo-ifc:IFCEntity
```

rather than `IFCObjectEntity`.

### Scope guard

Do not redesign existing EDO-IFC controlled-resource taxonomy in this commit. In particular, the pre-existing typing of `IfcDocumentInformation` is not changed as part of this migration.

### Validation

- all 11 IRIs exist exactly once;
- all are `owl:NamedIndividual`;
- all are instances of `IFCEntity` directly or through `IFCObjectEntity`;
- `ifcEntityName`, label and identifier exactly match the IFC entity name;
- no relation-mapping rules are otherwise changed.

## Commit 2 — Replace/add the EDO annotation taxonomy in develop

### File

`core/energy-domain-ontology.ttl`

### Add all 59 current EDO AnnotationProperties absent from develop

Copy their complete declarations verbatim from pinned `core/edo.ttl`.

### Replace all 20 overlapping EDO AnnotationProperty declarations

Replace each legacy declaration with the complete normative declaration from pinned `core/edo.ttl`.

Body predicate uses are **not** rewritten merely because a property's parent or metadata changed.

Examples:

- `hasAttribute` → `DomainAttributeStructureAnnotation`;
- `hasAttributeScope` → `DomainAttributeStructureAnnotation`;
- `hasTypedValue` → `DomainAttributeStructureAnnotation`;
- `hasUnit` → `DomainAttributeStructureAnnotation`;
- `hasLifecycleCreationPhase` → `DomainLifecycleAnnotation`;
- `hasDiscipline` → `DomainClassificationAnnotation`;
- `hasSpec` → `TechnicalDefinitionRelation`.

### Expected normative set

After this operation, all **79** current EDO AnnotationProperty IRIs shall be present with declarations matching the pinned normative EDO source.

## Commit 3 — Create the approved legacy compatibility branch

### Add root

```turtle
edo:LegacyAnnotation rdf:type owl:AnnotationProperty .
```

The complete declaration should clearly state that this branch preserves legacy/team metadata during transition and is not part of either normative current EDO annotation root.

### Preserve beneath it

```text
LegacyAnnotation
├── DomainAnnotation
│   └── DomainRelationship
├── SingleValue_VERIFICAR
├── hasContext
│   ├── hasCurve
│   └── hasLoad
├── entityStatus
├── hasExternalRef
└── hasEnd
```

### Rules

- `LegacyAnnotation` is independent of `DomainMetamodelAnnotation` and `DomainRelation`;
- no current normative EDO annotation becomes a descendant of `LegacyAnnotation`;
- preserve existing semantic metadata of the legacy properties where useful;
- mark `SingleValue_VERIFICAR` explicitly as a legacy/review candidate;
- preserve all existing body uses of `entityStatus`, `hasExternalRef` and `hasEnd` unchanged.

### Expected final EDO-namespace AnnotationProperty count

- 79 normative current EDO properties;
- 10 legacy compatibility properties including the new `LegacyAnnotation` root;
- total expected EDO-namespace AnnotationProperties: **89**.

This count excludes external vocabularies such as DCTERMS, SKOS and QUDT.

## Commit 4 — Fix the legacy typo

Replace the one live predicate use:

```turtle
edo:hasAtrribute edo:Identification
```

with:

```turtle
edo:hasAttribute edo:Identification
```

Then remove the `edo:hasAtrribute` AnnotationProperty declaration.

Validation target:

- zero occurrences of `edo:hasAtrribute` anywhere in develop.

## Commit 5 — Migrate IFC mapping predicates in develop

### Namespace

Add:

```turtle
@prefix edo-ifc: <https://w3id.org/energy-domain/edo/mappings/ifc#> .
```

Do not add an EDO-IFC `owl:imports` statement to develop.

### `ifc_objectType`

For all **270** predicate uses:

```text
edo:ifc_objectType → edo-ifc:ifc_objectType
```

Literal values remain unchanged.

### `ifc_predefinedType`

For all **268** predicate uses:

```text
edo:ifc_predefinedType → edo-ifc:ifc_predefinedType
```

Literal values remain unchanged.

### `ifc_equivalentClass`

For **273** valid IFC-name mappings:

```turtle
edo:ifc_equivalentClass "IfcX"
```

becomes:

```turtle
edo-ifc:ifc_equivalentClass edo-ifc:IfcX
```

All targets are exact-name controlled resources after Commit 1.

### Sentinel removal

Remove the single placeholder assertion:

```turtle
edo:IfcInstanciableElement edo:ifc_equivalentClass "-" .
```

Do not replace it with another mapping and do not create an IFC resource named `-`.

### Remove obsolete declarations

After all body uses have migrated, remove the three legacy EDO-namespace AnnotationProperty declarations:

- `edo:ifc_equivalentClass`
- `edo:ifc_objectType`
- `edo:ifc_predefinedType`

## Commit 6 — Mechanical cleanup only if required

Perform only formatting/section cleanup needed to leave syntactically coherent Turtle.

No semantic changes are allowed in this commit.

## Post-implementation validation

### EDO annotation invariants

1. all 79 pinned normative EDO AnnotationProperty IRIs present;
2. complete normative declarations preserved;
3. `DomainMetamodelAnnotation` and `DomainRelation` remain independent roots;
4. `LegacyAnnotation` remains a third independent compatibility root;
5. exactly the approved legacy compatibility set survives.

### Legacy-use invariants

1. 727 `entityStatus` uses preserved;
2. 1003 `hasExternalRef` uses preserved;
3. 7 `hasEnd` uses preserved;
4. zero `hasAtrribute` occurrences.

### IFC invariants

1. zero legacy `edo:ifc_equivalentClass` occurrences;
2. zero legacy `edo:ifc_objectType` occurrences;
3. zero legacy `edo:ifc_predefinedType` occurrences;
4. 273 `edo-ifc:ifc_equivalentClass` mappings resulting from legacy valid-name mappings;
5. zero string literal values for `edo-ifc:ifc_equivalentClass` among migrated statements;
6. each migrated equivalent-class value resolves to a controlled EDO-IFC resource;
7. 270 migrated `edo-ifc:ifc_objectType` uses;
8. 268 migrated `edo-ifc:ifc_predefinedType` uses;
9. the `"-"` placeholder is absent as an equivalent-class mapping.

### Syntax and composition

1. parse both changed TTL files successfully;
2. load develop and EDO-IFC together explicitly;
3. verify that EDO-IFC mapping terms resolve without redeclaration in develop;
4. verify no unintended canonical-EDO import was introduced into develop;
5. spot-check representative classes for each mapping category.

## Representative spot checks

At minimum inspect:

- a class mapped to existing `edo-ifc:IfcPipeFitting`;
- a class mapped to newly added `edo-ifc:IfcMaterial`;
- a class mapped to newly added `edo-ifc:IfcActuator`;
- `IfcInstanciableElement` sentinel removal;
- `MooringLine` typo correction;
- one `hasSpec` usage after taxonomy replacement;
- one `entityStatus`, one `hasExternalRef`, and one `hasEnd` preserved legacy use.

## Rollback discipline

Each commit is intentionally narrow and reversible. If any validation fails, revert only the failing commit rather than combining corrective semantic changes with unrelated steps.

## Approval gate

**This document is the implementation approval gate defined in the reconciliation plan.**

No TTL changes should be made until this Phase-6 plan is accepted.

Once accepted, implementation can proceed in the commit sequence above, followed immediately by Phase-8 validation and a validation report.