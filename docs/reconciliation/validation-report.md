# Annotation Reconciliation — Validation Report

## Scope

This report closes Phase 8 of the annotation reconciliation work for the EDO develop ontology.

Validated working branch:

- `reconcile-edo-develop-annotations`

Frozen technical references:

- develop baseline: `2042ffbc62c1b764d675a020478d76fa6b2def90`;
- normative EDO reference: `85b7ac4fea18efd1061548a76364e821946f13a3`, `core/edo.ttl`;
- normative EDO-IFC reference: the same commit, `mappings/ifc/edo-ifc.ttl`.

Validated implementation sequence:

1. `918652f` — extend controlled IFC vocabulary for develop mappings;
2. `15bc023` — reconcile develop annotation taxonomy with current EDO;
3. `39ac0f0` — add explicit legacy annotation compatibility branch;
4. `ebf51e1` — fix legacy `hasAtrribute` typo;
5. `e21e637552a41b2f5e5ce15ec76ecfc176bffee3` — migrate develop IFC annotations to EDO-IFC vocabulary.

The integrated validation was executed by GitHub Actions run `33805790802`. The run completed successfully and pushed the five implementation commits only after all validation checks passed.

The temporary workflow and helper scripts used to perform the deterministic transformation were removed after successful validation and are not part of the intended final ontology deliverable.

## Important counting clarification

The earlier Phase-2/Phase-4 inventory counted **textual predicate occurrences/statements** in the serialized Turtle. This was useful for locating migration work, but it is not always identical to the number of RDF triples because one Turtle predicate occurrence may contain an object list separated by commas.

The final validation therefore uses the parsed **RDF graph** as the semantic source for preservation counts.

Examples from the frozen baseline:

| Predicate | Earlier textual predicate occurrences | RDF triples in frozen baseline | Final RDF triples |
|---|---:|---:|---:|
| `edo:entityStatus` | 727 | 727 | 727 |
| `edo:hasExternalRef` | 1003 | 1014 | 1014 |
| `edo:hasEnd` | 7 | 11 | 11 |
| `edo:hasAttribute` | 203 | 878 | 879 |
| `edo:hasAtrribute` | 1 | 1 | 0 |

`hasAttribute` increases from 878 to 879 RDF triples exactly because the single typo use `hasAtrribute` was corrected to `hasAttribute`.

Therefore the old textual counts were not lost or fabricated; they measured a different serialization-level quantity. For semantic preservation and acceptance, the RDF triple counts in this report are authoritative.

## Structural validation

### Normative EDO annotations

Result: **PASS**.

- 79 EDO-namespace AnnotationProperties exist in the pinned normative `core/edo.ttl`.
- All 79 are present in the reconciled develop ontology.
- For each of the 79 properties, the complete set of RDF triples describing the AnnotationProperty declaration in the reconciled target matches the pinned normative declaration.

### Legacy compatibility branch

Result: **PASS**.

The reconciled target contains exactly 10 additional EDO-namespace AnnotationProperties outside the normative 79:

- `LegacyAnnotation`;
- `DomainAnnotation`;
- `DomainRelationship`;
- `SingleValue_VERIFICAR`;
- `hasContext`;
- `hasCurve`;
- `hasLoad`;
- `entityStatus`;
- `hasExternalRef`;
- `hasEnd`.

Total EDO-namespace AnnotationProperties in the reconciled target: **89**.

Validated topology:

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

`LegacyAnnotation` has no `rdfs:subPropertyOf` parent and remains independent of both `DomainMetamodelAnnotation` and `DomainRelation`.

`SingleValue_VERIFICAR` is retained as an explicit legacy/review candidate and marked deprecated.

## Legacy data preservation

Result: **PASS**.

Parsed RDF graph comparison against the frozen baseline confirms:

- `entityStatus`: 727 → 727 triples;
- `hasExternalRef`: 1014 → 1014 triples;
- `hasEnd`: 11 → 11 triples.

No semantic remapping was performed for these predicates.

## Typo correction

Result: **PASS**.

Baseline:

- `edo:hasAttribute`: 878 RDF triples;
- `edo:hasAtrribute`: 1 RDF triple.

Target:

- `edo:hasAttribute`: 879 RDF triples;
- `edo:hasAtrribute`: zero occurrences anywhere in the parsed graph.

The corrected statement is the `MooringLine` → `Identification` attribute relation.

## IFC mapping migration

Result: **PASS**.

Baseline RDF counts:

- `edo:ifc_equivalentClass`: 274;
- `edo:ifc_objectType`: 270;
- `edo:ifc_predefinedType`: 268;
- equivalent-class sentinel `"-"`: 1.

Target RDF counts in `core/energy-domain-ontology.ttl`:

- `edo-ifc:ifc_equivalentClass`: 273;
- `edo-ifc:ifc_objectType`: 270;
- `edo-ifc:ifc_predefinedType`: 268;
- legacy `edo:ifc_equivalentClass`: 0;
- legacy `edo:ifc_objectType`: 0;
- legacy `edo:ifc_predefinedType`: 0.

The 273 valid equivalent-class mappings now use controlled resources rather than string literals. The one `"-"` placeholder was removed without replacement.

Validation confirmed that every object of a migrated `edo-ifc:ifc_equivalentClass` statement resolves to a controlled resource in the branch version of EDO-IFC.

## EDO-IFC controlled vocabulary completion

Result: **PASS**.

The branch now contains the pinned normative `mappings/ifc/edo-ifc.ttl` plus the 11 controlled resources required by the develop mappings.

Added as `IFCObjectEntity` individuals:

- `IfcCovering`;
- `IfcActuator`;
- `IfcTask`;
- `IfcActor`;
- `IfcJunctionBox`;
- `IfcFastener`.

Added as direct `IFCEntity` individuals:

- `IfcMaterial`;
- `IfcClassificationReference`;
- `IfcClassification`;
- `IfcProject`;
- `IfcPerson`.

Each added resource was validated as an `owl:NamedIndividual`, with the approved controlled-resource type, `ifcEntityName`, and identifier.

## Syntax and composition validation

Result: **PASS**.

- `core/energy-domain-ontology.ttl` parses successfully as Turtle.
- `mappings/ifc/edo-ifc.ttl` parses successfully as Turtle.
- The develop ontology uses the `edo-ifc:` namespace for mapping assertions.
- The develop ontology does **not** import the EDO-IFC ontology.
- No unintended `owl:imports <https://w3id.org/energy-domain/edo/mappings/ifc>` was introduced.

This preserves the approved composition rule: consumers may explicitly load the reconciled develop ontology together with the corresponding EDO-IFC mapping ontology without causing develop itself to pull the canonical EDO ontology transitively.

## Representative spot checks

All required spot checks passed:

1. **Existing controlled IFC resource:** `MooringLine` maps through `edo-ifc:ifc_equivalentClass edo-ifc:IfcElementAssembly`, and its `ifc_objectType` / `ifc_predefinedType` predicates are in the EDO-IFC namespace.
2. **New direct IFCEntity:** legacy `IfcMaterial` mappings now resolve to `edo-ifc:IfcMaterial`.
3. **New IFCObjectEntity:** actuator mappings such as `DoubleActingHydraulicActuator`, `ElectricMotorActuator`, `ManualActuator`, `ROVActuator`, `SingleActingHydraulicActuator`, and `SteppingHydraulicActuator` now resolve to `edo-ifc:IfcActuator`.
4. **Sentinel removal:** `IfcInstanciableElement` no longer has an equivalent-class mapping with value `"-"`.
5. **Typo correction:** `MooringLine` now uses `edo:hasAttribute edo:Identification`.
6. **Normative relation use retained:** existing `edo:hasSpec` statements remain in the ontology body while the property declaration follows the normative `TechnicalDefinitionRelation` taxonomy.
7. **Legacy metadata retained:** representative classes continue to carry `entityStatus`, `hasExternalRef`, and `hasEnd` where present in the baseline.
8. **Legacy root:** `LegacyAnnotation` is explicitly present and independent, with only the approved compatibility hierarchy below it.

## Implementation outcome

Phase 7 implementation and Phase 8 validation are complete for the approved reconciliation scope.

The technical result is a coherent pair on the working branch:

```text
core/energy-domain-ontology.ttl
+
mappings/ifc/edo-ifc.ttl
```

with:

- the complete pinned normative EDO AnnotationProperty layer;
- the explicitly approved, isolated legacy compatibility branch;
- corrected typo data;
- migrated EDO-IFC predicates;
- controlled IFC equivalent-class resources;
- no fake resource for the `"-"` sentinel;
- no EDO-IFC import introduced into develop.

## Remaining work

The reconciliation implementation itself has no known validation blocker.

The remaining Phase-9 work is governance/integration work:

1. final branch review against the frozen develop baseline;
2. check whether normative `main` changed materially after the pinned reference commit;
3. decide how the paired reconciled files should be integrated;
4. open/review a PR when the integration target is chosen.
