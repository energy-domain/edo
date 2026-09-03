# Annotation Reconciliation Matrix — EDO develop → current EDO

## Frozen sources

- Legacy destination baseline: `edo_develop`, commit `2042ffbc62c1b764d675a020478d76fa6b2def90`, file `core/energy-domain-ontology.ttl`.
- Normative EDO core: `main`, commit `85b7ac4fea18efd1061548a76364e821946f13a3`, file `core/edo.ttl`.
- Normative IFC mapping vocabulary: same `main` commit, file `mappings/ifc/edo-ifc.ttl`.
- This document is analysis only. No TTL is modified by Phase 3.

## Reconciliation rule

For the EDO namespace, the target end state is strict reconciliation with the current `edo.ttl` AnnotationProperty vocabulary:

1. every current EDO AnnotationProperty must exist with its complete normative declaration;
2. every legacy EDO AnnotationProperty absent from current `edo.ttl` must disappear from the EDO namespace;
3. legacy predicate usages must either remain under a still-normative IRI, be explicitly migrated, or be removed by an approved semantic decision;
4. IFC-specific metadata must use the current `edo-ifc:` vocabulary rather than legacy `edo:ifc_*` properties.

## Matrix — all 33 legacy EDO AnnotationProperties

| Legacy annotation | Uses | Normative status | Declaration action | Usage action | Phase-3 status |
|---|---:|---|---|---|---|
| `DomainAnnotation` | 0 | absent | remove legacy declaration | none | **READY** |
| `DomainAuxiliarAnnotation` | 0 | exists in EDO | replace complete declaration from `edo.ttl` | none | **READY** |
| `DomainEngineeringAnnotation` | 0 | exists in EDO | replace complete declaration from `edo.ttl` | none | **READY** |
| `DomainRelationship` | 0 | absent | remove legacy declaration | none | **READY** |
| `SingleValue_VERIFICAR` | 0 | absent | remove legacy declaration | none | **READY** |
| `appliesTo` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **READY** |
| `defaultValidValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **READY** |
| `entityStatus` | 727 | absent | remove legacy declaration only after usages are resolved | **decision required** | **BLOCKED** |
| `hasAtrribute` | 1 | absent typo | remove typo declaration | replace predicate with `edo:hasAttribute` | **READY** |
| `hasAttribute` | 203 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **READY** |
| `hasAttributeCategory` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **READY** |
| `hasAttributeGroup` | 0 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | none | **READY** |
| `hasAttributeScope` | 886 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **READY** |
| `hasContext` | 0 | absent | remove legacy declaration | none; its only role is legacy parentage | **READY** |
| `hasCurve` | 0 | absent | remove legacy declaration | none | **READY** |
| `hasDiscipline` | 254 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | keep existing predicate uses unchanged | **READY** |
| `hasDomain` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **READY** |
| `hasEnd` | 7 | absent | remove legacy declaration only after usages are resolved | **decision required** | **BLOCKED** |
| `hasExternalRef` | 1003 | absent | remove legacy declaration only after usages are resolved | **decision required** | **BLOCKED** |
| `hasLifecycleCreationPhase` | 868 | exists in EDO | replace declaration; parent becomes `DomainLifecycleAnnotation` | keep existing predicate uses unchanged | **READY** |
| `hasLifecycleUsagePhase` | 0 | exists in EDO | replace declaration; parent becomes `DomainLifecycleAnnotation` | none | **READY** |
| `hasLoad` | 0 | absent | remove legacy declaration | none | **READY** |
| `hasLocationType` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **READY** |
| `hasSpec` | 36 | exists in EDO | replace complete declaration; parent becomes `TechnicalDefinitionRelation` | keep all 36 predicate uses unchanged | **READY** |
| `hasSubDomain` | 0 | exists in EDO | replace declaration; parent becomes `DomainClassificationAnnotation` | none | **READY** |
| `hasTypedValue` | 799 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **READY** |
| `hasUnit` | 468 | exists in EDO | replace complete declaration from current EDO | keep existing predicate uses unchanged | **READY** |
| `hasValueCardinality` | 798 | exists in EDO | replace declaration; parent becomes `DomainAttributeStructureAnnotation` | keep existing predicate uses unchanged | **READY** |
| `ifc_equivalentClass` | 274 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | migrate to `edo-ifc:ifc_equivalentClass`; convert legacy strings to controlled `edo-ifc:IFCEntity` resources | **READY WITH VALUE CONVERSION** |
| `ifc_objectType` | 270 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | rename predicate to `edo-ifc:ifc_objectType`; string value remains valid | **READY** |
| `ifc_predefinedType` | 268 | absent from EDO core; successor in EDO-IFC | remove legacy `edo:` declaration | rename predicate to `edo-ifc:ifc_predefinedType`; string value remains valid | **READY** |
| `specifiValidValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **READY** |
| `validValues` | 0 | exists in EDO | replace declaration; parent becomes `DomainApplicabilityAnnotation` | none | **READY** |

### Result

- **30 of the 33 legacy AnnotationProperties have a deterministic Phase-3 action.**
- Only **3** remain semantically blocked: `entityStatus`, `hasExternalRef`, and `hasEnd`.

## Analysis of the three blocked legacy annotations

### 1. `entityStatus` — do not map automatically to `conceptStatus`

Legacy definition:

> identifies entity status with values such as `NEW`, `REVIEW`, `APPROVED`.

Current `edo:conceptStatus` definition:

> editorial/governance status such as active, to-be-deprecated, deprecated, or replaced.

These are not the same controlled dimension. The legacy file has 727 uses of `entityStatus`; observed live values include `"NEW"`. Replacing the predicate by `conceptStatus` would preserve syntax but change semantics and would also leave uncontrolled legacy values under a property whose intended vocabulary is different.

**Recommendation:** do **not** map `entityStatus → conceptStatus` mechanically. Decide separately whether the old information should:

- be discarded as obsolete migration metadata;
- be translated through an explicit mapping to a current governance vocabulary;
- or be preserved outside the normative EDO AnnotationProperty namespace until a governance rule is defined.

### 2. `hasExternalRef` — `hasClassificationReference` is narrower

Legacy definition:

> reference or equivalent name of an entity in an external data dictionary or standard.

The 1003 live values are predominantly identifier-like strings, e.g. `MDA:AbandonmentCap`, `MDA:spec.api5l_delivery_condition`, etc.

Current `edo:hasClassificationReference` is specifically defined as association to an **external classification reference**, such as an identifier from a classification system.

Therefore `hasClassificationReference` is semantically narrower than legacy `hasExternalRef`. The MDA references may be dictionary alignments rather than classification-system membership.

**Recommendation:** do **not** bulk-map `hasExternalRef → hasClassificationReference` without an explicit decision that MDA references are intended to be treated as classification references. A generic external-reference mechanism is not currently present among EDO AnnotationProperties.

### 3. `hasEnd` — strong conceptual relation to `hasConnectionPoint`, but not a mechanical rename

Legacy definition:

> relates an entity to one of its functional connection ends.

The seven live uses point to legacy resources such as `FlangeAdapter_End_In` and `FlangeAdapter_End_Out`. Those resources are represented in the develop ontology as `owl:NamedIndividual` and describe input/output functional ends.

Current EDO defines:

- `edo:ConnectionPoint` as a `Feature` class representing a point used to establish a physical or logical connection;
- `edo:hasConnectionPoint` as the InterfaceRelation annotation associating a domain entity with a point, port or feature enabling connection.

The concepts are clearly related, but the representation changed: the old objects are named individuals representing directional ends, whereas the new model is based on `ConnectionPoint` classes/features and current project-instantiable connection-point specializations.

**Recommendation:** treat `hasEnd` migration as a small model migration, not a predicate rename. For each of the seven usages, determine whether its old end resource should become/refer to a current ConnectionPoint class and only then use `hasConnectionPoint` (or another approved current relation).

## Source-only EDO AnnotationProperties to add

The destination currently contains only 20 IRIs that overlap the 79 current EDO AnnotationProperties. Therefore **59 current EDO AnnotationProperties are absent from the legacy destination and must be added with their complete normative declarations**.

They are exactly the current-source properties not listed as surviving overlaps above, including the current structural roots/categories and relationship vocabulary:

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

All must be copied from the pinned normative `edo.ttl` declaration in full. This list plus the 20 overlapping current IRIs accounts for all 79 current EDO AnnotationProperties.

## EDO-IFC handling

The 26 current `edo-ifc:` AnnotationProperties remain defined by `mappings/ifc/edo-ifc.ttl`; they are **not to be redeclared as EDO-core properties** in the reconciled core. The legacy core usages of the three old IFC annotations should reference the external `edo-ifc:` vocabulary after migration.

This preserves the current architecture in which EDO core is IFC-independent and EDO-IFC is the source of truth for IFC mapping metadata.

## Proposed executable sets after decisions

### Set A — ADD

Add the 59 current-source EDO AnnotationProperties absent from develop, verbatim from the pinned `edo.ttl` declarations.

### Set B — REPLACE DECLARATION, KEEP USES

Replace the legacy declarations for the 20 overlapping current EDO AnnotationProperties with the complete normative declarations. Existing body uses remain unchanged.

### Set C — REMOVE LEGACY WITHOUT DATA MIGRATION

Remove:

- `DomainAnnotation`
- `DomainRelationship`
- `SingleValue_VERIFICAR`
- `hasContext`
- `hasCurve`
- `hasLoad`

These have no live predicate uses.

### Set D — FIX TYPO

- `hasAtrribute` → `hasAttribute` for its single live use, then remove the typo declaration.

### Set E — MIGRATE IFC METADATA

- `edo:ifc_equivalentClass` → `edo-ifc:ifc_equivalentClass` + controlled-resource conversion;
- `edo:ifc_objectType` → `edo-ifc:ifc_objectType`;
- `edo:ifc_predefinedType` → `edo-ifc:ifc_predefinedType`.

### Set F — BLOCKED PENDING SEMANTIC DECISION

- `entityStatus` — 727 uses;
- `hasExternalRef` — 1003 uses;
- `hasEnd` — 7 uses.

No TTL reconciliation should be considered complete while any of these three legacy predicates remain unresolved.

## Phase-3 acceptance criterion

After the three semantic decisions are approved, the implementation plan can be generated mechanically with four validations:

1. set equality of EDO AnnotationProperty IRIs against current `edo.ttl`;
2. declaration equality for every current EDO AnnotationProperty;
3. zero use of removed legacy EDO AnnotationProperties as predicates;
4. zero use of legacy `edo:ifc_*` predicates, with equivalent metadata represented through current `edo-ifc:` properties.
