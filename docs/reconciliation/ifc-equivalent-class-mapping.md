# IFC Equivalent Class Mapping Audit

## Frozen sources

- Legacy source: `core/energy-domain-ontology.ttl` at `edo_develop` baseline commit `2042ffbc62c1b764d675a020478d76fa6b2def90` (blob `c8b6781393949a082d43b6b95f063430549b83cc`).
- Normative IFC mapping vocabulary: `mappings/ifc/edo-ifc.ttl` at `main` commit `85b7ac4fea18efd1061548a76364e821946f13a3`.
- This is a non-destructive audit. No TTL is modified here.

## Result

The legacy ontology contains exactly **274** uses of `edo:ifc_equivalentClass`, comprising **30 distinct literal values**.

- **18 distinct values / 231 uses** already have an exact controlled resource in the current EDO-IFC vocabulary.
- **11 distinct IFC names / 42 uses** do not currently have a corresponding controlled resource in EDO-IFC.
- **1 distinct value / 1 use** is the sentinel `"-"`, not an IFC entity name.

The occurrence counts below sum to exactly 274, providing a closed inventory of the legacy data.

## Complete mapping table

| Legacy literal | Uses | Current EDO-IFC target | Match | Migration status |
|---|---:|---|---|---|
| `IfcPipeFitting` | 124 | `edo-ifc:IfcPipeFitting` | exact | READY |
| `IfcPipeSegment` | 27 | `edo-ifc:IfcPipeSegment` | exact | READY |
| `IfcElementAssembly` | 15 | `edo-ifc:IfcElementAssembly` | exact | READY |
| `IfcDiscreteAccessory` | 12 | `edo-ifc:IfcDiscreteAccessory` | exact | READY |
| `IfcMechanicalFastener` | 12 | `edo-ifc:IfcMechanicalFastener` | exact | READY |
| `IfcMaterial` | 11 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcCovering` | 10 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcBuildingElementProxy` | 6 | `edo-ifc:IfcBuildingElementProxy` | exact | READY |
| `IfcActuator` | 6 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcValve` | 6 | `edo-ifc:IfcValve` | exact | READY |
| `IfcDistributionPort` | 5 | `edo-ifc:IfcDistributionPort` | exact | READY |
| `IfcCableFitting` | 3 | `edo-ifc:IfcCableFitting` | exact | READY |
| `IfcCableSegment` | 3 | `edo-ifc:IfcCableSegment` | exact | READY |
| `IfcMember` | 3 | `edo-ifc:IfcMember` | exact | READY |
| `IfcPipeSegmentType` | 3 | `edo-ifc:IfcPipeSegmentType` | exact | READY |
| `IfcPile` | 3 | `edo-ifc:IfcPile` | exact | READY |
| `IfcGroup` | 3 | `edo-ifc:IfcGroup` | exact | READY |
| `IfcTask` | 3 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcClassificationReference` | 3 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcClassification` | 3 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcDocumentInformation` | 2 | `edo-ifc:IfcDocumentInformation` | exact | READY |
| `IfcProject` | 2 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcBuilding` | 2 | `edo-ifc:IfcBuilding` | exact | READY |
| `IfcPerson` | 1 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcActor` | 1 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcJunctionBox` | 1 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcFastener` | 1 | — | missing controlled resource | BLOCKED ON EDO-IFC VOCABULARY |
| `IfcSite` | 1 | `edo-ifc:IfcSite` | exact | READY |
| `UmbilicalSegment` | 1 | `edo-ifc:UmbilicalSegment` | exact | READY |
| `-` | 1 | — | sentinel, not an IFC entity | SPECIAL CASE |

## Exact mappings already supported

For the 231 uses whose values already exist in the current controlled vocabulary, migration is deterministic:

```turtle
# legacy
edo:ifc_equivalentClass "IfcPipeFitting" .

# target
edo-ifc:ifc_equivalentClass edo-ifc:IfcPipeFitting .
```

The same literal-to-resource rule applies to all 18 `READY` rows above. The local name is an exact match; no fuzzy or heuristic mapping is required.

## Controlled resources missing from current EDO-IFC

The following legacy IFC names occur in 42 annotations but are not currently represented by controlled resources in `edo-ifc.ttl`:

| IFC name | Uses |
|---|---:|
| `IfcMaterial` | 11 |
| `IfcCovering` | 10 |
| `IfcActuator` | 6 |
| `IfcTask` | 3 |
| `IfcClassificationReference` | 3 |
| `IfcClassification` | 3 |
| `IfcProject` | 2 |
| `IfcPerson` | 1 |
| `IfcActor` | 1 |
| `IfcJunctionBox` | 1 |
| `IfcFastener` | 1 |

These values must **not** be converted to invented EDO-IFC IRIs during the develop migration. The EDO-IFC controlled vocabulary must first be extended or an explicit alternative mapping must be approved. Only then can these 42 legacy literals be migrated to controlled resources.

This is a vocabulary-completeness issue in EDO-IFC, not ambiguity in the legacy data: each legacy value is syntactically unambiguous.

## Sentinel value

There is exactly one legacy use:

```turtle
edo:IfcInstanciableElement edo:ifc_equivalentClass "-" .
```

`"-"` is not an IFC entity and therefore cannot satisfy the current `rdfs:range edo-ifc:IFCEntity` model. It must not become an `edo-ifc:IFCEntity` resource. The patch plan must treat this as an explicit removal/no-mapping case rather than manufacture an IFC class.

## Consequence for the migration plan

The old statement shape:

```turtle
edo:SomeClass edo:ifc_equivalentClass "IfcX" .
```

has three target cases:

1. **Controlled resource already exists — 231 uses:** `edo:SomeClass edo-ifc:ifc_equivalentClass edo-ifc:IfcX .`
2. **Controlled resource missing — 42 uses:** defer the value migration until the EDO-IFC vocabulary contains an approved resource for that IFC entity.
3. **Sentinel `"-"` — 1 use:** remove the legacy placeholder mapping; do not create a fake controlled resource.

## Validation targets

After EDO-IFC vocabulary completion and TTL implementation:

1. zero uses of legacy `edo:ifc_equivalentClass`;
2. zero string literals as values of `edo-ifc:ifc_equivalentClass`;
3. every value of `edo-ifc:ifc_equivalentClass` resolves to a controlled EDO-IFC IFC entity resource;
4. no controlled resource is created for the sentinel `"-"`;
5. all 274 legacy uses are accounted for as either migrated or explicitly removed (`"-"`).

## Phase conclusion

The literal inventory itself is complete and fully deterministic. The remaining blocker is now precisely defined: **11 controlled IFC resources needed by 42 legacy mappings are absent from the current EDO-IFC vocabulary**. This should be resolved in EDO-IFC before generating the final executable TTL patch for the develop ontology.
