# Annotation Usage Migration Audit

## Scope

This Phase-4 artifact translates the approved reconciliation matrix into predicate-usage actions for `core/energy-domain-ontology.ttl` at baseline commit `2042ffbc62c1b764d675a020478d76fa6b2def90`.

The original inventory was produced before TTL implementation and counted serialized Turtle predicate occurrences. Phase-8 validation later parsed the frozen baseline as RDF and established semantic triple counts. Both measures are retained here because they answer different questions.

## Counting convention

- **Serialized occurrences**: number of places where the predicate token appears as a predicate in the Turtle body. One occurrence may introduce several RDF triples when its object is a comma-separated list.
- **RDF triples**: number of parsed triples having that IRI as predicate. This is the authoritative measure used for semantic preservation validation.

For example, legacy `hasAttribute` appeared as a predicate in 203 serialized statements but represented 878 RDF triples because many statements list multiple attributes.

## Usage classes

### A — same IRI, keep body semantics unchanged

The following current EDO AnnotationProperties survive under the same IRI. Their declarations/taxonomy change to the pinned normative EDO definition, but body data are not rewritten merely because their parent changes.

| Predicate | Serialized predicate occurrences in baseline |
|---|---:|
| `edo:hasAttribute` | 203 |
| `edo:hasAttributeScope` | 886 |
| `edo:hasDiscipline` | 254 |
| `edo:hasLifecycleCreationPhase` | 868 |
| `edo:hasSpec` | 36 |
| `edo:hasTypedValue` | 799 |
| `edo:hasUnit` | 468 |
| `edo:hasValueCardinality` | 798 |

The Phase-8 semantic validation specifically established `hasAttribute = 878` RDF triples in the frozen baseline. The final target has 879 because the single `hasAtrribute` typo triple was corrected into `hasAttribute`.

Other overlapping current annotations have zero serialized body occurrences and therefore require declaration replacement only.

### B — approved legacy compatibility predicates

These predicates remain in the EDO namespace beneath the new independent root `edo:LegacyAnnotation`:

| Predicate | Serialized occurrences | Baseline RDF triples | Final RDF triples | Migration action |
|---|---:|---:|---:|---|
| `edo:entityStatus` | 727 | 727 | 727 | preserve predicate and values unchanged |
| `edo:hasExternalRef` | 1003 | 1014 | 1014 | preserve predicate and values unchanged |
| `edo:hasEnd` | 7 | 11 | 11 | preserve predicate and values unchanged |

The following preserved legacy annotations have zero body predicate occurrences and require declaration/hierarchy preservation only:

- `edo:DomainAnnotation`
- `edo:DomainRelationship`
- `edo:SingleValue_VERIFICAR`
- `edo:hasContext`
- `edo:hasCurve`
- `edo:hasLoad`

### C — typo correction

`edo:hasAtrribute` had exactly one serialized occurrence and one RDF triple. Approved and implemented action:

- change that predicate to `edo:hasAttribute`;
- preserve the object (`edo:Identification`) unchanged;
- remove the typo AnnotationProperty declaration;
- final validation target: zero occurrences of `edo:hasAtrribute`.

Phase-8 validation confirmed the target has 879 `hasAttribute` RDF triples and zero `hasAtrribute` triples/IRI occurrences.

### D — IFC predicate namespace migration

| Legacy predicate | Baseline RDF triples | New predicate | Value action |
|---|---:|---|---|
| `edo:ifc_objectType` | 270 | `edo-ifc:ifc_objectType` | retain literal value unchanged |
| `edo:ifc_predefinedType` | 268 | `edo-ifc:ifc_predefinedType` | retain literal value unchanged |
| `edo:ifc_equivalentClass` | 274 | `edo-ifc:ifc_equivalentClass` | convert legacy IFC-class string to controlled EDO-IFC resource |

The 274 `ifc_equivalentClass` triples comprised 30 distinct literal values:

- 231 mappings / 18 distinct values already had exact controlled EDO-IFC resources;
- 42 mappings / 11 distinct IFC names required new controlled EDO-IFC resources;
- 1 mapping used the sentinel `"-"`, which is not an IFC entity and was classified as an explicit no-mapping/removal case.

The 11 controlled resources were subsequently added to the branch version of `mappings/ifc/edo-ifc.ttl`. Final Phase-8 validation confirmed 273 resource-valued `edo-ifc:ifc_equivalentClass` triples and removal of the one sentinel mapping.

## Declaration-only actions

All current EDO AnnotationProperties whose IRI overlaps the develop ontology but whose current declaration differs receive the complete pinned `edo.ttl` declaration. This operation does not rewrite existing body uses merely because the property's parent changed.

Examples:

- `hasAttribute`: `DomainAuxiliarAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasAttributeScope`: `DomainEngineeringAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasTypedValue`: `DomainAuxiliarAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasUnit`: `DomainEngineeringAnnotation` → `DomainAttributeStructureAnnotation`;
- `hasLifecycleCreationPhase`: `DomainEngineeringAnnotation` → `DomainLifecycleAnnotation`;
- `hasDiscipline`: `DomainEngineeringAnnotation` → `DomainClassificationAnnotation`;
- `hasSpec`: legacy `hasContext` → current `TechnicalDefinitionRelation`.

## Legacy hierarchy action

Approved and implemented compatibility hierarchy:

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

`LegacyAnnotation` is not a subproperty of either `DomainMetamodelAnnotation` or `DomainRelation`, and neither normative root is placed beneath it.

## Phase-4 / Phase-8 conclusion

All legacy annotation usages are accounted for. The pre-implementation serialized occurrence inventory remains useful for locating edit sites; the parsed RDF triple counts above are authoritative for semantic preservation.

Implementation and validation results are recorded in `validation-report.md`.
