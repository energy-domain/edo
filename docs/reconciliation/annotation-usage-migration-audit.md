# Annotation Usage Migration Audit

## Scope

This Phase-4 artifact translates the approved reconciliation matrix into predicate-usage actions for `core/energy-domain-ontology.ttl` at baseline commit `2042ffbc62c1b764d675a020478d76fa6b2def90`.

No TTL is modified in this phase.

## Usage classes

### A — same IRI, keep all body uses unchanged

The following current EDO AnnotationProperties survive under the same IRI. Their declarations/taxonomy change to the current normative EDO definition, but body predicate uses remain unchanged:

| Predicate | Uses |
|---|---:|
| `edo:hasAttribute` | 203 |
| `edo:hasAttributeScope` | 886 |
| `edo:hasDiscipline` | 254 |
| `edo:hasLifecycleCreationPhase` | 868 |
| `edo:hasSpec` | 36 |
| `edo:hasTypedValue` | 799 |
| `edo:hasUnit` | 468 |
| `edo:hasValueCardinality` | 798 |

Other overlapping current annotations have zero body uses and therefore require declaration replacement only.

### B — approved legacy compatibility predicates, keep all body uses unchanged

These predicates remain in the EDO namespace beneath the new independent root `edo:LegacyAnnotation`:

| Predicate | Uses | Migration action |
|---|---:|---|
| `edo:entityStatus` | 727 | preserve predicate and values unchanged |
| `edo:hasExternalRef` | 1003 | preserve predicate and values unchanged |
| `edo:hasEnd` | 7 | preserve predicate and values unchanged |

The following preserved legacy annotations have zero body predicate uses and therefore require declaration/hierarchy preservation only:

- `edo:DomainAnnotation`
- `edo:DomainRelationship`
- `edo:SingleValue_VERIFICAR`
- `edo:hasContext`
- `edo:hasCurve`
- `edo:hasLoad`

### C — typo correction

`edo:hasAtrribute` has exactly one body predicate use. Approved action:

- change that predicate to `edo:hasAttribute`;
- preserve the object (`edo:Identification`) unchanged;
- remove the typo AnnotationProperty declaration;
- validation target: zero occurrences of `edo:hasAtrribute` after implementation.

### D — IFC predicate namespace migration

| Legacy predicate | Uses | New predicate | Value action |
|---|---:|---|---|
| `edo:ifc_objectType` | 270 | `edo-ifc:ifc_objectType` | retain literal value unchanged |
| `edo:ifc_predefinedType` | 268 | `edo-ifc:ifc_predefinedType` | retain literal value unchanged |
| `edo:ifc_equivalentClass` | 274 | `edo-ifc:ifc_equivalentClass` | convert legacy IFC-class string to controlled `edo-ifc:IFCEntity` resource |

The first two migrations are mechanical predicate substitutions. The third is a predicate + value-model migration and must be validated against the controlled IFC entity vocabulary before the TTL patch is generated.

## Declaration-only actions

All current EDO AnnotationProperties whose IRI overlaps the develop ontology but whose current declaration differs must receive the complete pinned `edo.ttl` declaration. This operation must not rewrite their existing body uses merely because their parent changed.

Examples include:

- `hasAttribute`: `DomainAuxiliarAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasAttributeScope`: `DomainEngineeringAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasTypedValue`: `DomainAuxiliarAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasUnit`: `DomainEngineeringAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasLifecycleCreationPhase`: `DomainEngineeringAnnotation` → `DomainLifecycleAnnotation`;
- `hasDiscipline`: `DomainEngineeringAnnotation` → `DomainClassificationAnnotation`;
- `hasSpec`: legacy `hasContext` → current `TechnicalDefinitionRelation`.

## Legacy hierarchy action

Approved temporary compatibility hierarchy:

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

`LegacyAnnotation` must not be a subproperty of either `DomainMetamodelAnnotation` or `DomainRelation`, and neither current root may be placed beneath it.

## Phase-4 conclusion

Usage migration is now deterministic except for one technical lookup task: resolving the 274 legacy `ifc_equivalentClass` literal values to controlled `edo-ifc:IFCEntity` resources. No semantic decision remains open.

The next non-destructive step is to build that IFC-equivalent-class value mapping and then produce the explicit TTL patch plan required by the implementation gate.
