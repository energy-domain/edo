# IFC Equivalent Class Mapping Audit

## Status

**AUDIT COMPLETE — BLOCKER RESOLVED AND MIGRATION IMPLEMENTED.**

## Frozen sources

- Legacy source: `core/energy-domain-ontology.ttl` at `edo_develop` baseline commit `2042ffbc62c1b764d675a020478d76fa6b2def90`.
- Normative IFC mapping vocabulary: `mappings/ifc/edo-ifc.ttl` at `main` commit `85b7ac4fea18efd1061548a76364e821946f13a3`.

## Audit result

The legacy ontology contains exactly **274 RDF triples** using `edo:ifc_equivalentClass`, comprising **30 distinct literal values**.

- **18 distinct values / 231 mappings** already had an exact controlled resource in the pinned EDO-IFC vocabulary.
- **11 distinct IFC names / 42 mappings** lacked a controlled resource in the pinned EDO-IFC vocabulary.
- **1 distinct value / 1 mapping** was the sentinel `"-"`, not an IFC entity name.

The counts below sum to exactly 274.

## Complete mapping table and final resolution

| Legacy literal | Uses | Final controlled target | Final resolution |
|---|---:|---|---|
| `IfcPipeFitting` | 124 | `edo-ifc:IfcPipeFitting` | migrated |
| `IfcPipeSegment` | 27 | `edo-ifc:IfcPipeSegment` | migrated |
| `IfcElementAssembly` | 15 | `edo-ifc:IfcElementAssembly` | migrated |
| `IfcDiscreteAccessory` | 12 | `edo-ifc:IfcDiscreteAccessory` | migrated |
| `IfcMechanicalFastener` | 12 | `edo-ifc:IfcMechanicalFastener` | migrated |
| `IfcMaterial` | 11 | `edo-ifc:IfcMaterial` | controlled resource added; migrated |
| `IfcCovering` | 10 | `edo-ifc:IfcCovering` | controlled resource added; migrated |
| `IfcBuildingElementProxy` | 6 | `edo-ifc:IfcBuildingElementProxy` | migrated |
| `IfcActuator` | 6 | `edo-ifc:IfcActuator` | controlled resource added; migrated |
| `IfcValve` | 6 | `edo-ifc:IfcValve` | migrated |
| `IfcDistributionPort` | 5 | `edo-ifc:IfcDistributionPort` | migrated |
| `IfcCableFitting` | 3 | `edo-ifc:IfcCableFitting` | migrated |
| `IfcCableSegment` | 3 | `edo-ifc:IfcCableSegment` | migrated |
| `IfcMember` | 3 | `edo-ifc:IfcMember` | migrated |
| `IfcPipeSegmentType` | 3 | `edo-ifc:IfcPipeSegmentType` | migrated |
| `IfcPile` | 3 | `edo-ifc:IfcPile` | migrated |
| `IfcGroup` | 3 | `edo-ifc:IfcGroup` | migrated |
| `IfcTask` | 3 | `edo-ifc:IfcTask` | controlled resource added; migrated |
| `IfcClassificationReference` | 3 | `edo-ifc:IfcClassificationReference` | controlled resource added; migrated |
| `IfcClassification` | 3 | `edo-ifc:IfcClassification` | controlled resource added; migrated |
| `IfcDocumentInformation` | 2 | `edo-ifc:IfcDocumentInformation` | migrated |
| `IfcProject` | 2 | `edo-ifc:IfcProject` | controlled resource added; migrated |
| `IfcBuilding` | 2 | `edo-ifc:IfcBuilding` | migrated |
| `IfcPerson` | 1 | `edo-ifc:IfcPerson` | controlled resource added; migrated |
| `IfcActor` | 1 | `edo-ifc:IfcActor` | controlled resource added; migrated |
| `IfcJunctionBox` | 1 | `edo-ifc:IfcJunctionBox` | controlled resource added; migrated |
| `IfcFastener` | 1 | `edo-ifc:IfcFastener` | controlled resource added; migrated |
| `IfcSite` | 1 | `edo-ifc:IfcSite` | migrated |
| `UmbilicalSegment` | 1 | `edo-ifc:UmbilicalSegment` | migrated |
| `-` | 1 | — | placeholder removed; no resource created |

## Controlled vocabulary completion

The branch version of EDO-IFC was extended with the 11 missing resources.

### Added as `IFCObjectEntity`

- `IfcCovering`
- `IfcActuator`
- `IfcTask`
- `IfcActor`
- `IfcJunctionBox`
- `IfcFastener`

### Added directly as `IFCEntity`

- `IfcMaterial`
- `IfcClassificationReference`
- `IfcClassification`
- `IfcProject`
- `IfcPerson`

The distinction intentionally avoids classifying non-`IfcObject` IFC concepts as `IFCObjectEntity` merely to satisfy the mapping vocabulary.

## Implemented transformation

Legacy shape:

```turtle
edo:SomeClass edo:ifc_equivalentClass "IfcX" .
```

Target shape:

```turtle
edo:SomeClass edo-ifc:ifc_equivalentClass edo-ifc:IfcX .
```

The transformation is exact-name based. No fuzzy or heuristic mapping was used.

## Sentinel handling

The baseline contains exactly one placeholder:

```turtle
edo:IfcInstanciableElement edo:ifc_equivalentClass "-" .
```

`"-"` is not an IFC entity and cannot satisfy the controlled-resource model. The assertion was removed and no fake IFC resource was created.

## Final validation

Phase-8 RDF validation confirmed:

1. zero legacy `edo:ifc_equivalentClass` predicate usages/declaration in the reconciled develop ontology;
2. exactly **273** final `edo-ifc:ifc_equivalentClass` mappings;
3. zero string literals as values of those migrated mappings;
4. every mapped value resolves to a controlled resource in the branch EDO-IFC ontology;
5. no controlled resource exists for the `"-"` sentinel;
6. all 274 baseline mappings are accounted for: 273 migrated + 1 explicitly removed placeholder.

The former EDO-IFC vocabulary-completeness blocker is therefore closed.

See `validation-report.md` for the integrated implementation validation.
