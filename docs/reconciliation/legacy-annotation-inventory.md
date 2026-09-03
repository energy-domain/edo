# Legacy Annotation Inventory — `edo_develop`

## Frozen source

- File: `core/energy-domain-ontology.ttl`.
- Baseline: `edo_develop` commit `2042ffbc62c1b764d675a020478d76fa6b2def90`.
- Blob: `c8b6781393949a082d43b6b95f063430549b83cc` (~1.7 MB).
- The GitHub Contents endpoint returns empty content for this large blob; the inventory was therefore read from the Git blob itself.
- No TTL was modified.

## Summary

- EDO-namespace AnnotationProperties declared in the legacy file: **33**.
- Legacy root: `edo:DomainAnnotation`.
- Direct branches: `DomainAuxiliarAnnotation`, `DomainEngineeringAnnotation`, `DomainRelationship`.
- `DomainRelationship` has no subproperties in this legacy ontology.
- The annotation declarations alone are not the migration problem: many of these properties are used hundreds of times in the ontology body.

## Complete legacy annotation inventory

| Annotation | Legacy parent | Predicate uses in ontology body | Current normative destination | Preliminary class |
|---|---|---:|---|---|
| `DomainAnnotation` | — | 0 | none | `REMOVE_OBSOLETE_ARCHITECTURE` |
| `DomainAuxiliarAnnotation` | `DomainAnnotation` | 0 | `edo:DomainAuxiliarAnnotation` | `REPLACE_WITH_EDO_DEFINITION` |
| `DomainEngineeringAnnotation` | `DomainAnnotation` | 0 | `edo:DomainEngineeringAnnotation` | `REPLACE_WITH_EDO_DEFINITION` |
| `DomainRelationship` | `DomainAnnotation` | 0 | none | `REMOVE_OBSOLETE_ARCHITECTURE` |
| `SingleValue_VERIFICAR` | — | 0 | none | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `appliesTo` | `DomainAuxiliarAnnotation` | 0 | `edo:appliesTo` | `REPLACE_WITH_EDO_DEFINITION` |
| `defaultValidValues` | `DomainAuxiliarAnnotation` | 0 | `edo:defaultValidValues` | `REPLACE_WITH_EDO_DEFINITION` |
| `entityStatus` | `DomainAuxiliarAnnotation` | **727** | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasAtrribute` | — | **1** | probable `edo:hasAttribute` | `FIX_LEGACY_TYPO` |
| `hasAttribute` | `DomainAuxiliarAnnotation` | **203** | `edo:hasAttribute` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasAttributeCategory` | `DomainEngineeringAnnotation` | 0 | `edo:hasAttributeCategory` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasAttributeGroup` | `DomainEngineeringAnnotation` | 0 | `edo:hasAttributeGroup` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasAttributeScope` | `DomainEngineeringAnnotation` | **886** | `edo:hasAttributeScope` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasContext` | `DomainAuxiliarAnnotation` | 0 | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasCurve` | `hasContext` | 0 | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasDiscipline` | `DomainEngineeringAnnotation` | **254** | `edo:hasDiscipline` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasDomain` | `DomainEngineeringAnnotation` | 0 | `edo:hasDomain` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasEnd` | `DomainAuxiliarAnnotation` | **7** | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasExternalRef` | `DomainAuxiliarAnnotation` | **1003** | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasLifecycleCreationPhase` | `DomainEngineeringAnnotation` | **868** | `edo:hasLifecycleCreationPhase` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasLifecycleUsagePhase` | `DomainEngineeringAnnotation` | 0 | `edo:hasLifecycleUsagePhase` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasLoad` | `hasContext` | 0 | none identical | `REVIEW_NO_1_TO_1_SUCCESSOR` |
| `hasLocationType` | `DomainEngineeringAnnotation` | 0 | `edo:hasLocationType` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasSpec` | `hasContext` | **36** | `edo:hasSpec` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasSubDomain` | `DomainEngineeringAnnotation` | 0 | `edo:hasSubDomain` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasTypedValue` | `DomainAuxiliarAnnotation` | **799** | `edo:hasTypedValue` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasUnit` | `DomainEngineeringAnnotation` | **468** | `edo:hasUnit` | `REPLACE_WITH_EDO_DEFINITION` |
| `hasValueCardinality` | `DomainAuxiliarAnnotation` | **798** | `edo:hasValueCardinality` | `REPLACE_WITH_EDO_DEFINITION` |
| `ifc_equivalentClass` | `DomainEngineeringAnnotation` | **274** | `edo-ifc:ifc_equivalentClass` | `MIGRATE_TO_EDO_IFC` |
| `ifc_objectType` | `DomainEngineeringAnnotation` | **270** | `edo-ifc:ifc_objectType` | `MIGRATE_TO_EDO_IFC` |
| `ifc_predefinedType` | `DomainEngineeringAnnotation` | **268** | `edo-ifc:ifc_predefinedType` | `MIGRATE_TO_EDO_IFC` |
| `specifiValidValues` | `DomainAuxiliarAnnotation` | 0 | `edo:specifiValidValues` | `REPLACE_WITH_EDO_DEFINITION` |
| `validValues` | `DomainAuxiliarAnnotation` | 0 | `edo:validValues` | `REPLACE_WITH_EDO_DEFINITION` |

### Counting method

Counts are occurrences where the legacy AnnotationProperty is used as a predicate in the ontology body. Its own declaration and occurrences solely as the object of `rdfs:subPropertyOf` are excluded. The Git blob is represented twice internally by the connector; raw match totals were deduplicated before deriving the counts.

## High-impact observations

### Existing IRIs whose declaration/taxonomy changed

Several annotations exist both in the legacy ontology and current EDO but sit in a different taxonomy and/or have different declaration metadata. Examples:

- `hasAttribute`: legacy `DomainAuxiliarAnnotation` → normative `DomainAttributeStructureAnnotation` (**203 uses**).
- `hasAttributeScope`: legacy `DomainEngineeringAnnotation` → normative `DomainAttributeStructureAnnotation` (**886 uses**).
- `hasTypedValue`: legacy `DomainAuxiliarAnnotation` → normative `DomainAttributeStructureAnnotation` (**799 uses**).
- `hasUnit`: legacy `DomainEngineeringAnnotation` → normative `DomainAttributeStructureAnnotation` (**468 uses**).
- `hasValueCardinality`: legacy `DomainAuxiliarAnnotation` → normative `DomainAttributeStructureAnnotation` (**798 uses**).
- `hasLifecycleCreationPhase`: legacy `DomainEngineeringAnnotation` → normative `DomainLifecycleAnnotation` (**868 uses**).
- `hasDiscipline`: legacy `DomainEngineeringAnnotation` → normative `DomainClassificationAnnotation` (**254 uses**).
- `hasSpec`: legacy `hasContext` → normative `TechnicalDefinitionRelation` (**36 uses**).

These are not additive migrations: their legacy declarations must be replaced by the complete declarations from `edo.ttl`.

### IFC annotations moved out of EDO core

The legacy core still contains and uses:

- `edo:ifc_equivalentClass`: **274** uses;
- `edo:ifc_objectType`: **270** uses;
- `edo:ifc_predefinedType`: **268** uses.

The current normative properties are `edo-ifc:*` annotations. Migration cannot be a blind namespace rename. In particular, current `edo-ifc:ifc_equivalentClass` has range `edo-ifc:IFCEntity`, while the legacy property stores string values such as `"IfcPipeFitting"`. Each legacy string must therefore be resolved to the corresponding controlled EDO-IFC resource.

### Typo with live data

`edo:hasAtrribute` is separately declared and has exactly **1** predicate use: `MooringLine` points to `Identification`. This is a concrete candidate for correction to normative `edo:hasAttribute`.

### Legacy-only annotations requiring semantic decision

The following have no identical current EDO or EDO-IFC IRI:

- `entityStatus` — **727 uses**;
- `hasExternalRef` — **1003 uses**;
- `hasEnd` — **7 uses**;
- `hasContext` — 0 uses (but is parent of legacy `hasCurve`, `hasLoad`, `hasSpec`);
- `hasCurve` — 0 uses;
- `hasLoad` — 0 uses;
- `SingleValue_VERIFICAR` — 0 uses.

They must not be mapped by name similarity. `entityStatus` may look related to current governance metadata such as `conceptStatus`, and `hasEnd` may look related to the newer connection model, but those are semantic hypotheses to be decided in the reconciliation matrix, not automatic transformations.

## Phase-2 conclusion

The legacy annotation layer cannot be reconciled by unioning the current annotations into the develop file. The next artifact must be a property-by-property reconciliation matrix covering both declarations and live predicate usages, with explicit actions such as:

- `REPLACE_WITH_EDO_DEFINITION`;
- `MIGRATE_TO_EDO_IFC`;
- `REMOVE_OBSOLETE_ARCHITECTURE`;
- `FIX_LEGACY_TYPO`;
- `REVIEW_NO_1_TO_1_SUCCESSOR`.

No TTL should be modified before that matrix is reviewed.
