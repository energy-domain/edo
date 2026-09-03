# Normative Annotation Inventory — EDO core + EDO-IFC

## Frozen sources

- EDO core: `core/edo.ttl`, `main` at commit `85b7ac4fea18efd1061548a76364e821946f13a3`, blob `7767202e00807da81e87ae5ecb9d83432051ce00`.
- EDO-IFC: `mappings/ifc/edo-ifc.ttl`, same commit, blob `750c3a1e7c8bd46123b4f4878430818fa99eb6f2`.
- No TTL was modified during this inventory.

## Summary

- EDO namespace AnnotationProperties: **79**.
- EDO-IFC namespace AnnotationProperties: **26**.
- EDO core has two independent roots: `edo:DomainMetamodelAnnotation` and `edo:DomainRelation`.
- EDO-IFC has its own root: `edo-ifc:IFCMappingAnnotation` and imports EDO core.

## EDO core — complete structural inventory

### DomainRelation tree

- `DomainRelation`
  - `ConnectionRelation`
    - `connectionRealizedBy`
    - `isConnectedTo`
  - `FunctionalRelation`
    - `serves`
    - `hasInterconnection`
    - `hosts`
  - `SpatialRelation`
    - `spatiallyContains`
  - `InformationRelation`
    - `hasClassificationReference`
    - `hasEvidence`
    - `hasIssue`
    - `hasDocument`
  - `InterfaceRelation`
    - `hasConnectionPoint`
  - `MaterialRelation`
    - `hasMaterial`
  - `OrganizationalRelation`
    - `belongsToGroup`
    - `hasResponsibleAgent`
  - `PartWholeRelation`
    - `hasTask`
    - `hasPart`
      - `hasOrderedPart`
  - `ProvisionRelation`
    - `hasSparePart`
  - `TechnicalDefinitionRelation`
    - `hasOperatingCondition`
    - `hasOperatingState`
    - `hasSpec`
    - `isDefinedByCatalogItem`
  - `hasSubject`

### DomainMetamodelAnnotation tree

- `DomainMetamodelAnnotation`
  - `DomainApplicabilityAnnotation`
    - `allowedValue`
    - `appliesTo`
    - `appliesToDomainElement`
    - `appliesWhen`
    - `attributePropagation`
    - `defaultValidValues`
    - `sourceType`
    - `specifiValidValues`
    - `targetType`
    - `validValues`
  - `DomainAttributeStructureAnnotation`
    - `expectedXsdType`
    - `hasAttribute`
    - `hasAttributeGroup`
    - `hasAttributeScope`
    - `hasTypedValue`
    - `hasUnit`
    - `hasValueCardinality`
    - `specializesAttribute`
    - `valueOrigin`
  - `DomainAuxiliarAnnotation`
  - `DomainClassificationAnnotation`
    - `attributeCategory`
    - `attributeNature`
    - `attributeOntologicalNature`
    - `hasAttributeCategory`
    - `hasDiscipline`
    - `hasDomain`
    - `hasLocationType`
    - `hasSubDomain`
  - `DomainEngineeringAnnotation`
  - `DomainGovernanceAnnotation`
    - `conceptStatus`
    - `hasMaturityLevel`
  - `DomainLifecycleAnnotation`
    - `hasLifecycleCreationPhase`
    - `hasLifecycleUsagePhase`
    - `lifecycleRole`
  - `DomainValidationAnnotation`
    - `DomainRelationConstraintAnnotation`
      - `objectExpectedCardinality`
      - `subjectExpectedCardinality`
  - `classInstantiationRole`

This accounts for all **79** AnnotationProperties in the EDO namespace in the pinned `edo.ttl`.

## EDO-IFC — complete structural inventory

Root: `edo-ifc:IFCMappingAnnotation`.

All current EDO-IFC AnnotationProperties are direct subproperties of that root:

1. `IFCMappingAnnotation` (root)
2. `ifc_equivalentClass`
3. `ifc_invertedDirection`
4. `ifc_subjectRole`
5. `ifc_objectRole`
6. `ifc_objectType`
7. `ifc_predefinedType`
8. `ifc_relationshipName`
9. `ifc_attachToProject`
10. `ifc_materializationMode`
11. `ifc_attributeProjectionRule`
12. `sourceEDOClass`
13. `targetEDOClass`
14. `attributeProjectionDirection`
15. `projectInheritedAttributes`
16. `ifc_psetNameTemplate`
17. `projectNestedStructures`
18. `ifc_mappingRule`
19. `sourceIfcEquivalentClass`
20. `targetIfcEquivalentClass`
21. `sourceNotIfcEquivalentClass`
22. `targetNotIfcEquivalentClass`
23. `realizingElementRequirement`
24. `realizingElementRole`
25. `ifcEntityName`
26. `ifcAttributeName`

## Metadata/declaration rule for reconciliation

The pinned TTL declarations are normative **in full**, not only by local name or taxonomy. Reconciliation must preserve the complete source declarations, including as applicable:

- `rdf:type owl:AnnotationProperty`;
- `rdfs:subPropertyOf`;
- `dcterms:identifier`;
- `rdfs:label`;
- `skos:definition` and `skos:altLabel`;
- `rdfs:domain` / `rdfs:range`;
- other declaration metadata present in the source.

Therefore an annotation already present in `edo_develop` is not considered reconciled merely because its IRI exists: its old declaration must be replaced if it differs from the normative declaration.

## Key findings for the next phase

1. `edo:DomainRelationship` does not exist in either current normative annotation set.
2. `edo:hasAttribute` is normative under `edo:DomainAttributeStructureAnnotation`, not under the legacy `DomainAuxiliarAnnotation`.
3. `edo:hasSpec` is normative under `edo:TechnicalDefinitionRelation`, not under the old `hasContext` branch.
4. Lifecycle annotations now belong to `DomainLifecycleAnnotation`; discipline/domain/location classification annotations belong to `DomainClassificationAnnotation`.
5. `edo:ifc_equivalentClass`, `edo:ifc_objectType` and `edo:ifc_predefinedType` are no longer EDO-core annotations. Their current counterparts are `edo-ifc:*` annotations.
6. `edo-ifc:ifc_equivalentClass` has range `edo-ifc:IFCEntity`: legacy string values such as `"IfcPipeFitting"` cannot be migrated by namespace substitution alone; they must be resolved to controlled EDO-IFC resources.
