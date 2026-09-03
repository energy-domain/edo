# Annotation Reconciliation Matrix — EDO develop → current EDO

## Frozen sources

- Legacy destination baseline: `edo_develop`, commit `2042ffbc62c1b764d675a020478d76fa6b2def90`, `core/energy-domain-ontology.ttl`.
- Normative EDO core: `main`, commit `85b7ac4fea18efd1061548a76364e821946f13a3`, `core/edo.ttl`.
- Normative IFC mapping vocabulary: same `main` commit, `mappings/ifc/edo-ifc.ttl`.
- Working branch: `reconcile-edo-develop-annotations`.

## Counting clarification

The original Phase-2 matrix column `Uses` counted serialized Turtle predicate occurrences, not parsed RDF triples. This matters where a single predicate occurrence has a comma-separated object list.

Phase-8 semantic validation established the authoritative baseline RDF counts for the preserved/high-impact predicates:

| Predicate | Serialized occurrences | Baseline RDF triples | Final RDF triples |
|---|---:|---:|---:|
| `entityStatus` | 727 | 727 | 727 |
| `hasExternalRef` | 1003 | 1014 | 1014 |
| `hasEnd` | 7 | 11 | 11 |
| `hasAttribute` | 203 | 878 | 879 |
| `hasAtrribute` | 1 | 1 | 0 |
| `ifc_equivalentClass` | 274 | 274 | 0 in `edo:` / 273 in `edo-ifc:` |
| `ifc_objectType` | 270 | 270 | 0 in `edo:` / 270 in `edo-ifc:` |
| `ifc_predefinedType` | 268 | 268 | 0 in `edo:` / 268 in `edo-ifc:` |

The increase of `hasAttribute` from 878 to 879 is exactly the correction of the single `hasAtrribute` triple. The reduction of equivalent-class mappings from 274 to 273 is exactly the removal of the `"-"` sentinel.

## Approved target architecture

The reconciled ontology contains three independent AnnotationProperty roots:

1. `edo:DomainMetamodelAnnotation` — current normative EDO metamodel annotations;
2. `edo:DomainRelation` — current normative EDO relationship annotations;
3. `edo:LegacyAnnotation` — temporary preservation area for explicitly approved legacy/team-specific annotations.

The final EDO-namespace AnnotationProperty set is intentionally a strict superset of the current normative EDO set: **79 normative properties + 10 approved legacy compatibility properties = 89**.

## Matrix — all 33 legacy EDO AnnotationProperties

`Uses` below preserves the original serialized-occurrence inventory. Semantic preservation is validated by RDF graph comparison where relevant.

| Legacy annotation | Uses | Approved declaration action | Approved usage action | Final status |
|---|---:|---|---|---|
| `DomainAnnotation` | 0 | keep under `LegacyAnnotation` | none | **IMPLEMENTED** |
| `DomainAuxiliarAnnotation` | 0 | replace complete declaration from current EDO | none | **IMPLEMENTED** |
| `DomainEngineeringAnnotation` | 0 | replace complete declaration from current EDO | none | **IMPLEMENTED** |
| `DomainRelationship` | 0 | keep beneath legacy `DomainAnnotation` | none | **IMPLEMENTED** |
| `SingleValue_VERIFICAR` | 0 | keep under `LegacyAnnotation`, mark review/deprecation candidate | none | **IMPLEMENTED** |
| `appliesTo` | 0 | replace; parent → `DomainApplicabilityAnnotation` | none | **IMPLEMENTED** |
| `defaultValidValues` | 0 | replace; parent → `DomainApplicabilityAnnotation` | none | **IMPLEMENTED** |
| `entityStatus` | 727 | keep under `LegacyAnnotation` | preserve all data | **IMPLEMENTED / 727 RDF triples preserved** |
| `hasAtrribute` | 1 | remove typo declaration | migrate one triple to `hasAttribute` | **IMPLEMENTED / zero remaining** |
| `hasAttribute` | 203 | replace; parent → `DomainAttributeStructureAnnotation` | preserve body data + receive typo triple | **IMPLEMENTED / 879 final RDF triples** |
| `hasAttributeCategory` | 0 | replace; parent → `DomainClassificationAnnotation` | none | **IMPLEMENTED** |
| `hasAttributeGroup` | 0 | replace; parent → `DomainAttributeStructureAnnotation` | none | **IMPLEMENTED** |
| `hasAttributeScope` | 886 | replace; parent → `DomainAttributeStructureAnnotation` | preserve body data | **IMPLEMENTED** |
| `hasContext` | 0 | keep under `LegacyAnnotation` | none | **IMPLEMENTED** |
| `hasCurve` | 0 | keep under legacy `hasContext` | none | **IMPLEMENTED** |
| `hasDiscipline` | 254 | replace; parent → `DomainClassificationAnnotation` | preserve body data | **IMPLEMENTED** |
| `hasDomain` | 0 | replace; parent → `DomainClassificationAnnotation` | none | **IMPLEMENTED** |
| `hasEnd` | 7 | keep under `LegacyAnnotation` | preserve all data | **IMPLEMENTED / 11 RDF triples preserved** |
| `hasExternalRef` | 1003 | keep under `LegacyAnnotation` | preserve all data | **IMPLEMENTED / 1014 RDF triples preserved** |
| `hasLifecycleCreationPhase` | 868 | replace; parent → `DomainLifecycleAnnotation` | preserve body data | **IMPLEMENTED** |
| `hasLifecycleUsagePhase` | 0 | replace; parent → `DomainLifecycleAnnotation` | none | **IMPLEMENTED** |
| `hasLoad` | 0 | keep under legacy `hasContext` | none | **IMPLEMENTED** |
| `hasLocationType` | 0 | replace; parent → `DomainClassificationAnnotation` | none | **IMPLEMENTED** |
| `hasSpec` | 36 | replace; parent → `TechnicalDefinitionRelation` | preserve body data | **IMPLEMENTED** |
| `hasSubDomain` | 0 | replace; parent → `DomainClassificationAnnotation` | none | **IMPLEMENTED** |
| `hasTypedValue` | 799 | replace; parent → `DomainAttributeStructureAnnotation` | preserve body data | **IMPLEMENTED** |
| `hasUnit` | 468 | replace complete declaration from current EDO | preserve body data | **IMPLEMENTED** |
| `hasValueCardinality` | 798 | replace; parent → `DomainAttributeStructureAnnotation` | preserve body data | **IMPLEMENTED** |
| `ifc_equivalentClass` | 274 | remove legacy EDO declaration | migrate valid values to controlled `edo-ifc:` resources; remove `"-"` | **IMPLEMENTED / 273 final mappings** |
| `ifc_objectType` | 270 | remove legacy EDO declaration | predicate → `edo-ifc:ifc_objectType`, literals unchanged | **IMPLEMENTED** |
| `ifc_predefinedType` | 268 | remove legacy EDO declaration | predicate → `edo-ifc:ifc_predefinedType`, literals unchanged | **IMPLEMENTED** |
| `specifiValidValues` | 0 | replace; parent → `DomainApplicabilityAnnotation` | none | **IMPLEMENTED** |
| `validValues` | 0 | replace; parent → `DomainApplicabilityAnnotation` | none | **IMPLEMENTED** |

## Approved legacy branch

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

Notes:

- `DomainAnnotation` and `DomainRelationship` are preserved for historical traceability, not as normative current EDO roots.
- `hasContext`, `hasCurve`, and `hasLoad` preserve their useful old internal hierarchy.
- `SingleValue_VERIFICAR` is explicitly legacy and marked deprecated/review candidate.
- `entityStatus` and `hasExternalRef` remain because they carry team-created maturity/reference metadata.
- `hasEnd` remains until a later dedicated connection-model review.

## Current EDO properties added/replaced

The baseline develop ontology overlapped 20 of the 79 current normative EDO AnnotationProperty IRIs. Implementation therefore:

- added the 59 normative EDO AnnotationProperties absent from develop;
- replaced the complete declarations of the 20 overlapping IRIs with the pinned current EDO declarations;
- preserved their body data except where an explicit migration decision required otherwise.

Phase-8 validation compared the complete RDF declaration triples of all 79 properties against pinned `core/edo.ttl` and passed.

## EDO-IFC handling

The current `edo-ifc:` AnnotationProperties remain defined in `mappings/ifc/edo-ifc.ttl`; they are not redeclared in the EDO namespace.

The branch now also contains the 11 controlled IFC resources required to migrate all valid legacy equivalent-class values. The 273 valid mappings use controlled resources; the single `"-"` placeholder was removed.

The develop ontology references the `edo-ifc:` namespace but does not import EDO-IFC, preserving the approved external-composition architecture.

## Acceptance criteria — achieved for implementation scope

Phase-8 validation confirms:

1. all 79 current EDO AnnotationProperty IRIs are present;
2. their complete RDF declarations match the pinned normative `edo.ttl` declarations;
3. `edo:LegacyAnnotation` is independent of `DomainMetamodelAnnotation` and `DomainRelation`;
4. only the 10 explicitly approved legacy compatibility properties remain outside the normative set;
5. `edo:hasAtrribute` has zero declarations and zero graph occurrences;
6. legacy `edo:ifc_*` declarations/usages are eliminated in favor of current `edo-ifc:` properties;
7. `entityStatus` is preserved at 727 RDF triples;
8. `hasExternalRef` is preserved at 1014 RDF triples;
9. `hasEnd` is preserved at 11 RDF triples;
10. `hasAttribute` ends at 879 RDF triples, exactly baseline 878 + one corrected typo triple;
11. all 273 valid equivalent-class mappings point to controlled EDO-IFC resources;
12. the `"-"` sentinel has no replacement mapping.

Detailed results are recorded in `validation-report.md`.
