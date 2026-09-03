# TTL Change Plan — Approval Gate and Implementation Record

## Status

**APPROVED AND IMPLEMENTED.**

This Phase-6 document was the operation-level approval gate before ontology TTL changes. The approved sequence was implemented on `reconcile-edo-develop-annotations` and subsequently passed Phase-8 RDF validation.

Detailed validation results are in `validation-report.md`.

## Frozen references

- develop baseline: `core/energy-domain-ontology.ttl` at commit `2042ffbc62c1b764d675a020478d76fa6b2def90`;
- normative EDO core: `core/edo.ttl` at `main` commit `85b7ac4fea18efd1061548a76364e821946f13a3`;
- normative EDO-IFC: `mappings/ifc/edo-ifc.ttl` at the same `main` commit;
- working branch: `reconcile-edo-develop-annotations`.

## Target architecture

The reconciled develop ontology uses:

1. the complete pinned EDO AnnotationProperty layer;
2. a separate transitional `edo:LegacyAnnotation` branch for explicitly approved legacy metadata;
3. EDO-IFC predicates and controlled resources for IFC mapping assertions;
4. no legacy IFC mapping AnnotationProperty declarations in the `edo:` namespace.

The EDO and EDO-IFC vocabularies remain architecturally separate.

## Composition rule

Do **not** add:

```turtle
owl:imports <https://w3id.org/energy-domain/edo/mappings/ifc>
```

to the develop ontology merely to use EDO-IFC terms.

Reason: EDO-IFC imports the canonical EDO ontology URI. Develop importing EDO-IFC could therefore cause a loader to pull canonical EDO alongside the develop variant and mix ontology versions.

Implemented approach:

- add/use the `edo-ifc:` prefix in develop;
- use EDO-IFC IRIs in mapping assertions;
- compose develop and EDO-IFC explicitly in consuming applications.

Phase-8 validation confirmed no EDO-IFC import was introduced into develop.

## Commit 1 — Extend controlled IFC vocabulary

### File

`mappings/ifc/edo-ifc.ttl`

Because the working branch originated from `edo_develop`, this file did not exist on the branch. Implementation therefore brought the exact pinned normative EDO-IFC file from `main` into the working branch and extended that branch copy.

### Added as `IFCObjectEntity`

- `edo-ifc:IfcCovering`
- `edo-ifc:IfcActuator`
- `edo-ifc:IfcTask`
- `edo-ifc:IfcActor`
- `edo-ifc:IfcJunctionBox`
- `edo-ifc:IfcFastener`

### Added as direct `IFCEntity`

- `edo-ifc:IfcMaterial`
- `edo-ifc:IfcClassificationReference`
- `edo-ifc:IfcClassification`
- `edo-ifc:IfcProject`
- `edo-ifc:IfcPerson`

Each resource follows the controlled-resource pattern with `owl:NamedIndividual`, controlled EDO-IFC type, label, `ifcEntityName`, buildingSMART reference and identifier.

Implemented commit: `918652f`.

## Commit 2 — Replace/add normative EDO annotation taxonomy

### File

`core/energy-domain-ontology.ttl`

Implemented operations:

- add all 59 current EDO AnnotationProperties absent from develop;
- replace all 20 overlapping legacy declarations with the complete pinned normative declarations;
- do not rewrite body data merely because an annotation parent/taxonomy changed.

Expected and validated normative set: **79 AnnotationProperties**.

Implemented commit: `15bc023`.

## Commit 3 — Create approved legacy compatibility branch

Implemented hierarchy:

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

Rules implemented:

- `LegacyAnnotation` independent of `DomainMetamodelAnnotation` and `DomainRelation`;
- no normative current EDO annotation moved beneath it;
- useful legacy semantic metadata retained;
- `SingleValue_VERIFICAR` marked as deprecated/review candidate;
- live `entityStatus`, `hasExternalRef` and `hasEnd` RDF data preserved exactly.

Final EDO-namespace AnnotationProperty count: **89 = 79 normative + 10 legacy compatibility**.

Implemented commit: `39ac0f0`.

## Commit 4 — Fix legacy typo

Implemented transformation:

```turtle
edo:hasAtrribute edo:Identification
```

→

```turtle
edo:hasAttribute edo:Identification
```

The typo declaration was removed.

Phase-8 RDF validation established:

- baseline `hasAttribute`: 878 triples;
- baseline `hasAtrribute`: 1 triple;
- target `hasAttribute`: 879 triples;
- target `hasAtrribute`: zero occurrences.

Implemented commit: `ebf51e1`.

## Commit 5 — Migrate IFC mapping predicates

### Namespace

Develop references:

```turtle
@prefix edo-ifc: <https://w3id.org/energy-domain/edo/mappings/ifc#> .
```

without importing EDO-IFC.

### `ifc_objectType`

270 RDF triples migrated:

```text
edo:ifc_objectType → edo-ifc:ifc_objectType
```

Literal values retained unchanged.

### `ifc_predefinedType`

268 RDF triples migrated:

```text
edo:ifc_predefinedType → edo-ifc:ifc_predefinedType
```

Literal values retained unchanged.

### `ifc_equivalentClass`

Baseline: 274 RDF triples.

- 273 valid IFC-name mappings became controlled-resource assertions;
- the one `"-"` placeholder was removed with no replacement.

Transformation shape:

```turtle
edo:ifc_equivalentClass "IfcX"
```

→

```turtle
edo-ifc:ifc_equivalentClass edo-ifc:IfcX
```

After migration, the three obsolete EDO-namespace IFC AnnotationProperty declarations were removed:

- `edo:ifc_equivalentClass`
- `edo:ifc_objectType`
- `edo:ifc_predefinedType`

Implemented commit: `e21e637552a41b2f5e5ce15ec76ecfc176bffee3`.

## Validation methodology correction

The pre-implementation inventories sometimes reported **serialized Turtle predicate occurrences**. For predicates whose statements contain comma-separated object lists, that number differs from the number of RDF triples.

Phase-8 acceptance therefore uses parsed graph counts against the frozen baseline.

Authoritative preservation results:

| Predicate | Serialized occurrences in earlier inventory | Baseline RDF triples | Final RDF triples |
|---|---:|---:|---:|
| `entityStatus` | 727 | 727 | 727 |
| `hasExternalRef` | 1003 | 1014 | 1014 |
| `hasEnd` | 7 | 11 | 11 |
| `hasAttribute` | 203 | 878 | 879 |
| `hasAtrribute` | 1 | 1 | 0 |

The earlier occurrence counts remain valid serialization-level inventory values; the RDF counts are authoritative for semantic preservation.

## Post-implementation invariants — validated

### EDO annotation layer

1. all 79 pinned normative EDO AnnotationProperty IRIs present;
2. complete RDF declaration triples match pinned normative EDO;
3. `DomainMetamodelAnnotation`, `DomainRelation`, and `LegacyAnnotation` remain independent roots;
4. exactly the approved 10 legacy compatibility properties survive outside the normative set.

### Legacy data

1. 727 `entityStatus` RDF triples preserved;
2. 1014 `hasExternalRef` RDF triples preserved;
3. 11 `hasEnd` RDF triples preserved;
4. zero `hasAtrribute` occurrences;
5. 879 final `hasAttribute` RDF triples = baseline 878 + one typo correction.

### IFC mapping

1. zero legacy `edo:ifc_equivalentClass` predicate/declaration;
2. zero legacy `edo:ifc_objectType` predicate/declaration;
3. zero legacy `edo:ifc_predefinedType` predicate/declaration;
4. 273 resource-valued `edo-ifc:ifc_equivalentClass` mappings;
5. zero literal equivalent-class values among migrated mappings;
6. every equivalent-class target resolves to a controlled EDO-IFC resource;
7. 270 `edo-ifc:ifc_objectType` triples;
8. 268 `edo-ifc:ifc_predefinedType` triples;
9. the `"-"` placeholder is absent as an equivalent-class mapping.

### Syntax and composition

1. both changed TTL files parse successfully as Turtle;
2. EDO-IFC mapping terms resolve through the paired ontology file;
3. no EDO-IFC AnnotationProperty is redeclared in develop;
4. no unintended EDO-IFC import is introduced into develop.

## Representative spot checks — passed

- `MooringLine`: typo corrected and IFC mapping predicates migrated;
- existing controlled target such as `IfcElementAssembly`: resolved;
- newly added `IfcMaterial`: resolved as direct `IFCEntity`;
- newly added `IfcActuator`: resolved as `IFCObjectEntity`;
- `IfcInstanciableElement`: sentinel mapping absent;
- `hasSpec`: body statements retained under normative relation declaration;
- legacy `entityStatus`, `hasExternalRef`, `hasEnd`: data preserved;
- `LegacyAnnotation`: approved hierarchy present and independent.

## Implementation gate outcome

The approval gate is satisfied. Phase 7 implementation and Phase 8 validation are complete for this scope.

Remaining work belongs to Phase 9: final branch review, normative-main drift check, integration-target decision, and PR/review when appropriate.
