# IFC Mapping Migration Plan

## Scope

This Phase-5 document resolves how the legacy IFC mapping annotations in `core/energy-domain-ontology.ttl` will move to the complementary EDO-IFC ontology.

Frozen references:

- develop baseline: `2042ffbc62c1b764d675a020478d76fa6b2def90`;
- normative EDO / EDO-IFC reference: `85b7ac4fea18efd1061548a76364e821946f13a3`.

No TTL is modified by this document.

## Existing approved predicate migrations

| Legacy predicate | Target predicate | Uses | Value action |
|---|---|---:|---|
| `edo:ifc_objectType` | `edo-ifc:ifc_objectType` | 270 | retain literal unchanged |
| `edo:ifc_predefinedType` | `edo-ifc:ifc_predefinedType` | 268 | retain literal unchanged |
| `edo:ifc_equivalentClass` | `edo-ifc:ifc_equivalentClass` | 274 | convert IFC name literal to controlled EDO-IFC resource |

## `ifc_equivalentClass` closed inventory

The 274 legacy values are fully accounted for:

- 231 uses already resolve to an existing exact controlled EDO-IFC resource;
- 42 uses require 11 new controlled resources;
- 1 use is the sentinel `"-"` and shall be removed rather than converted.

The detailed count table is maintained in `ifc-equivalent-class-mapping.md`.

## Required controlled-vocabulary extension

### New resources typed as `edo-ifc:IFCObjectEntity`

These IFC entities inherit through the IFC object branch and can use the existing controlled category without introducing a new class:

| Resource | Legacy uses |
|---|---:|
| `edo-ifc:IfcCovering` | 10 |
| `edo-ifc:IfcActuator` | 6 |
| `edo-ifc:IfcTask` | 3 |
| `edo-ifc:IfcActor` | 1 |
| `edo-ifc:IfcJunctionBox` | 1 |
| `edo-ifc:IfcFastener` | 1 |

Each shall be declared as an `owl:NamedIndividual` and an `edo-ifc:IFCObjectEntity`, with:

- `rdfs:label` equal to the IFC entity name;
- `edo-ifc:ifcEntityName` equal to the IFC entity name;
- `dcterms:identifier` equal to the IFC entity name;
- `rdfs:seeAlso` pointing to the official IFC 4.3 lexical documentation;
- preferably `skos:exactMatch` to the buildingSMART identifier URI where available, following the strongest existing EDO-IFC pattern.

### New resources typed directly as `edo-ifc:IFCEntity`

These are valid IFC entities but are not members of the IFC `IfcObject` inheritance branch. They shall therefore not be misclassified merely for convenience:

| Resource | IFC structural nature | Legacy uses |
|---|---|---:|
| `edo-ifc:IfcMaterial` | material-definition entity | 11 |
| `edo-ifc:IfcClassificationReference` | external-reference entity | 3 |
| `edo-ifc:IfcClassification` | external-information entity | 3 |
| `edo-ifc:IfcProject` | context entity | 2 |
| `edo-ifc:IfcPerson` | person/resource-level entity | 1 |

Each shall be declared as an `owl:NamedIndividual` and directly as `edo-ifc:IFCEntity`, with the same controlled-reference metadata listed above.

This is intentionally a minimal extension. No new intermediate EDO-IFC category is required for this migration.

## Existing EDO-IFC taxonomy observation

`edo-ifc:IFCObjectEntity` is currently used for at least one resource that is not an IFC `IfcObject` in the EXPRESS inheritance sense (`IfcDocumentInformation`). That pre-existing modeling issue is outside the scope of this reconciliation.

For the 11 new resources, this plan uses IFC inheritance accurately rather than propagating that inconsistency. A future dedicated EDO-IFC taxonomy review may refine existing controlled-resource categories independently.

## Deterministic value conversion

After the 11 resources above exist, every valid legacy IFC-name literal has an exact target by local name.

Example:

```turtle
# legacy develop
edo:SomeClass edo:ifc_equivalentClass "IfcMaterial" .

# target develop using complementary EDO-IFC
edo:SomeClass edo-ifc:ifc_equivalentClass edo-ifc:IfcMaterial .
```

No fuzzy matching or semantic inference is required.

## Sentinel handling

The single legacy statement using:

```turtle
edo:ifc_equivalentClass "-"
```

represents absence of an IFC mapping. It shall be removed during migration. No controlled resource shall be created for `"-"`.

## Namespace/import requirement in the reconciled develop ontology

Because the target ontology will contain EDO-IFC annotation assertions, the file must make the `edo-ifc:` namespace available.

The implementation plan shall also explicitly decide whether the reconciled develop ontology itself imports EDO-IFC or whether EDO-IFC remains an externally composed companion ontology. The architecture agreed in this work is that EDO-IFC complements EDO and is the source of truth for IFC mapping semantics; it must not be copied back into the EDO namespace.

For this reconciliation, the preferred composition is:

- declare the `edo-ifc:` prefix in develop;
- use EDO-IFC predicates/resources in develop mapping assertions;
- keep the EDO-IFC ontology definitions exclusively in `mappings/ifc/edo-ifc.ttl`;
- do not duplicate EDO-IFC AnnotationProperty or controlled-resource declarations in develop.

## Phase-5 conclusion

All IFC mapping migrations are now specified without semantic ambiguity.

The remaining work is operational rather than conceptual:

1. extend EDO-IFC with the 11 missing controlled resources;
2. migrate the 274 `ifc_equivalentClass` uses (273 converted, 1 sentinel removed);
3. migrate the 270 `ifc_objectType` predicates;
4. migrate the 268 `ifc_predefinedType` predicates;
5. remove the three legacy `edo:ifc_*` declarations;
6. validate composition of reconciled develop + EDO-IFC.

These operations are detailed in the Phase-6 TTL change plan.