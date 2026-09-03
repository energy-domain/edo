# Annotation Reconciliation Matrix — EDO develop → current EDO

## Frozen sources

- Legacy destination baseline: `edo_develop`, commit `2042ffbc62c1b764d675a020478d76fa6b2def90`, file `core/energy-domain-ontology.ttl`.
- Normative EDO core: `main`, commit `85b7ac4fea18efd1061548a76364e821946f13a3`, file `core/edo.ttl`.
- Normative IFC mapping vocabulary: same `main` commit, file `mappings/ifc/edo-ifc.ttl`.
- This document records the approved Phase-3 reconciliation decisions. No TTL is modified by this document update.

## Approved target architecture

The reconciled ontology will contain three independent AnnotationProperty roots:

1. `edo:DomainMetamodelAnnotation` — current normative EDO metamodel annotations;
2. `edo:DomainRelation` — current normative EDO relationship annotations;
3. `edo:LegacyAnnotation` — temporary preservation area for legacy/team-specific annotations that must survive this migration but are intentionally outside the two normative current EDO roots.

`edo:LegacyAnnotation` is a transitional compatibility mechanism. Its contents are preserved so that historical/team metadata is not lost while the current EDO annotation architecture is adopted. A later work item may move some or all of these annotations to a dedicated ontology.

Where useful, old internal hierarchy is preserved beneath `LegacyAnnotation` rather than flattening every legacy property directly under the new root.

## Reconciliation rule

For the EDO namespace, the target end state is:

1. every current EDO AnnotationProperty exists with its complete normative declaration;
2. current EDO AnnotationProperties retain the normative hierarchy from `edo.ttl`;
3. explicitly approved legacy/team annotations remain under the separate `edo:LegacyAnnotation` branch;
4. the typo `edo:hasAtrribute` does not survive; its single use is corrected to `edo:hasAttribute`;
5. IFC-specific metadata uses the current `edo-ifc:` vocabulary rather than legacy `edo:ifc_*` properties.

Therefore the final AnnotationProperty set is intentionally a strict superset of the current `edo.ttl` annotation set: current normative EDO + approved legacy compatibility annotations.

## Matrix — all 33 legacy EDO AnnotationProperties

| Legacy annotation | Uses | Current EDO status | Approved declaration action | Approved usage action | Status |
|---|---:|---|---|---|---|
| `DomainAnnotation` | 0 | absent | keep under `LegacyAnnotation` as legacy structural node | none | **APPROVED** |
| `DomainAuxiliarAnnotation` | 0 | exists in EDO | replace complete declaration from `edo.ttl` | none | **APPROVED** |
| `DomainEngineeringAnnotation` | 0 | exists in EDO | replace complete declaration from `edo.ttl` | none | **APPROVED** |
| `DomainRelationship` | 0 | absent | keep as legacy node beneath `DomainAnnotation` | none | **APPROVED** |
| `SingleValue_VERIFICAR` | 0 | absent | keep under `LegacyAnnotation`; mark clearly as legacy/deprecation candidate | none | **APPROVED** |
| `appliesTo` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **APPROVED** |
| `defaultValidValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **APPROVED** |
| `entityStatus` | 727 | absent | keep under `LegacyAnnotation` as team maturity metadata | keep all existing uses unchanged | **APPROVED** |
| `hasAtrribute` | 1 | absent typo | remove typo declaration | replace its single predicate use with `edo:hasAttribute` | **APPROVED** |
| `hasAttribute` | 203 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `hasAttributeCategory` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **APPROVED** |
| `hasAttributeGroup` | 0 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | none | **APPROVED** |
| `hasAttributeScope` | 886 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `hasContext` | 0 | absent | keep under `LegacyAnnotation` / preserved legacy hierarchy | none | **APPROVED** |
| `hasCurve` | 0 | absent | keep under legacy `hasContext` | none | **APPROVED** |
| `hasDiscipline` | 254 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `hasDomain` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **APPROVED** |
| `hasEnd` | 7 | absent | keep under `LegacyAnnotation` pending later connection-model review | keep all seven existing uses unchanged | **APPROVED** |
| `hasExternalRef` | 1003 | absent | keep under `LegacyAnnotation` as team/external-reference metadata | keep all existing uses unchanged | **APPROVED** |
| `hasLifecycleCreationPhase` | 868 | exists in EDO | replace declaration; parent becomes `DomainLifecycleAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `hasLifecycleUsagePhase` | 0 | exists in EDO | replace declaration; parent becomes `DomainLifecycleAnnotation` | none | **APPROVED** |
| `hasLoad` | 0 | absent | keep under legacy `hasContext` | none | **APPROVED** |
| `hasLocationType` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **APPROVED** |
| `hasSpec` | 36 | exists in EDO | replace complete declaration; parent becomes `TechnicalDefinitionRelation` | keep all 36 predicate uses unchanged | **APPROVED** |
| `hasSubDomain` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **APPROVED** |
| `hasTypedValue` | 799 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `hasUnit` | 468 | exists in EDO | replace complete declaration from current EDO | keep existing predicate uses unchanged | **APPROVED** |
| `hasValueCardinality` | 798 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **APPROVED** |
| `ifc_equivalentClass` | 274 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | migrate to `edo-ifc:ifc_equivalentClass`; convert legacy strings to controlled `edo-ifc:IFCEntity` resources | **APPROVED, VALUE CONVERSION REQUIRED** |
| `ifc_objectType` | 270 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | rename predicate to `edo-ifc:ifc_objectType`; retain string values | **APPROVED** |
| `ifc_predefinedType` | 268 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | rename predicate to `edo-ifc:ifc_predefinedType`; retain string values | **APPROVED** |
| `specifiValidValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **APPROVED** |
| `validValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **APPROVED** |

## Approved legacy branch

The exact declaration metadata will be defined in the implementation plan, but the structural intent is:

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
- `hasContext`, `hasCurve`, and `hasLoad` preserve their useful old internal relationship.
- `SingleValue_VERIFICAR` remains explicitly legacy and should be marked as a deprecation/review candidate.
- `entityStatus` and `hasExternalRef` are intentionally retained because they carry team-created maturity/reference metadata still used throughout the ontology.
- `hasEnd` remains intact until a later dedicated review decides whether/how it should be remodelled against the current connection-point architecture.

## Source-only EDO AnnotationProperties to add

The destination currently contains only 20 IRIs that overlap the 79 current EDO AnnotationProperties. Therefore **59 current EDO AnnotationProperties are absent from the legacy destination and must be added with their complete normative declarations**.

### New structural/category annotations

- `DomainMetamodelAnnotation`
- `DomainApplicabilityAnnotation`
- `DomainAttributeStructureAnnotation`
- `DomainClassificationAnnotation`
- `DomainGovernanceAnnotation`
- `DomainLifecycleAnnotation`
- `DomainValidationAnnotation`
- `DomainRelationConstraintAnnotation`
- `DomainRelation`
- `ConnectionRelation`
- `FunctionalRelation`
- `SpatialRelation`
- `InformationRelation`
- `InterfaceRelation`
- `MaterialRelation`
- `OrganizationalRelation`
- `PartWholeRelation`
- `ProvisionRelation`
- `TechnicalDefinitionRelation`

### New leaf annotations

- `allowedValue`
- `appliesToDomainElement`
- `appliesWhen`
- `attributeCategory`
- `attributeNature`
- `attributeOntologicalNature`
- `attributePropagation`
- `belongsToGroup`
- `classInstantiationRole`
- `conceptStatus`
- `connectionRealizedBy`
- `expectedXsdType`
- `hasClassificationReference`
- `hasConnectionPoint`
- `hasTask`
- `hasSubject`
- `hasEvidence`
- `hasIssue`
- `hasResponsibleAgent`
- `hasDocument`
- `hasMaterial`
- `hasMaturityLevel`
- `hasOrderedPart`
- `hasPart`
- `hasSparePart`
- `hasOperatingCondition`
- `hasOperatingState`
- `spatiallyContains`
- `serves`
- `hasInterconnection`
- `hosts`
- `isConnectedTo`
- `isDefinedByCatalogItem`
- `lifecycleRole`
- `objectExpectedCardinality`
- `sourceType`
- `specializesAttribute`
- `subjectExpectedCardinality`
- `targetType`
- `valueOrigin`

All must be copied from the pinned normative `edo.ttl` declaration in full.

## EDO-IFC handling

The 26 current `edo-ifc:` AnnotationProperties remain defined by `mappings/ifc/edo-ifc.ttl`; they are not to be redeclared as EDO-core properties in the reconciled core. The three legacy IFC annotation uses migrate to the external `edo-ifc:` vocabulary.

This preserves the architecture in which EDO core is IFC-independent and EDO-IFC is the source of truth for IFC mapping metadata.

## Executable sets

### Set A — ADD CURRENT EDO

Add the 59 current-source EDO AnnotationProperties absent from develop, verbatim from the pinned `edo.ttl` declarations.

### Set B — REPLACE DECLARATION, KEEP USES

Replace the legacy declarations for the 20 overlapping current EDO AnnotationProperties with the complete normative declarations. Existing body uses remain unchanged.

### Set C — CREATE/PRESERVE LEGACY COMPATIBILITY BRANCH

Create `edo:LegacyAnnotation` and preserve beneath it:

- `DomainAnnotation`
- `DomainRelationship`
- `SingleValue_VERIFICAR`
- `hasContext`
- `hasCurve`
- `hasLoad`
- `entityStatus`
- `hasExternalRef`
- `hasEnd`

Existing `entityStatus`, `hasExternalRef`, and `hasEnd` predicate uses remain unchanged.

### Set D — FIX TYPO

- replace the single `edo:hasAtrribute` predicate use with `edo:hasAttribute`;
- remove the `hasAtrribute` declaration entirely.

### Set E — MIGRATE IFC METADATA

- `edo:ifc_equivalentClass` → `edo-ifc:ifc_equivalentClass` + controlled-resource conversion;
- `edo:ifc_objectType` → `edo-ifc:ifc_objectType`;
- `edo:ifc_predefinedType` → `edo-ifc:ifc_predefinedType`.

## Phase-3 acceptance criterion — achieved

All legacy AnnotationProperties now have an approved destination/action. There are no remaining semantic blockers in Phase 3.

The implementation plan and validation must enforce:

1. all 79 current EDO AnnotationProperty IRIs are present;
2. their declarations match the pinned current `edo.ttl` declarations;
3. `edo:LegacyAnnotation` is independent of `DomainMetamodelAnnotation` and `DomainRelation`;
4. only the explicitly approved legacy compatibility annotations remain outside the current normative EDO annotation set;
5. `edo:hasAtrribute` has zero declarations and zero uses;
6. legacy `edo:ifc_*` declarations/usages are eliminated in favor of current `edo-ifc:` properties;
7. all 727 `entityStatus`, 1003 `hasExternalRef`, and 7 `hasEnd` uses are preserved unchanged during this migration.
