# EDO to CFIHOS / IOGP alignment report
## Purpose
This report presents the current EDO alignment assertions from the CFIHOS / IOGP information-handover perspective. The TTL files remain the source of truth; this document is a human-readable derivative for review, discussion and presentation.
## Summary
- Total mapping assertions: 23
- `closeMatch`: 4
- `relatedMatch`: 19

## Main target concepts
- `edo-cfihos:LifecycleInformation` — CFIHOS lifecycle information: 6 mappings
- `edo-cfihos:Property` — CFIHOS Property: 6 mappings
- `edo-cfihos:EquipmentClass` — CFIHOS equipment class: 2 mappings
- `edo-cfihos:TagClass` — CFIHOS tag class: 2 mappings
- `edo-cfihos:Requirement` — CFIHOS requirement: 2 mappings
- `edo-cfihos:Document` — CFIHOS document: 2 mappings
- `edo-cfihos:ClassProperty` — CFIHOS class property: 2 mappings
- `edo-cfihos:UnitOfMeasure` — CFIHOS unit of measure: 1 mappings

## Alignment assertions

### `edo-cfihos:ClassProperty` — CFIHOS class property

#### `edo:hasAttribute` — Has Attribute
- Mapping: `closeMatch` → `edo-cfihos:ClassProperty`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: hasAttribute expresses that an EDO domain element has an applicable domain attribute. This is close to the CFIHOS class-property applicability pattern, while remaining an EDO annotation relation rather than a materialised class-property entity.

#### `edo:hasAttributeScope` — has attribute scope
- Mapping: `relatedMatch` → `edo-cfihos:ClassProperty`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: hasAttributeScope distinguishes type-level and instance-level attribute use in EDO. This is relevant to the CFIHOS distinction between class-level property applicability and delivered instance information.

### `edo-cfihos:Document` — CFIHOS document

#### `edo:Specification` — Specification
- Mapping: `relatedMatch` → `edo-cfihos:Document`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: Specification may act both as a document-like artefact and as a source of requirements for property values or information delivery constraints.

#### `edo:TechnicalArtifact` — Technical Artifact
- Mapping: `relatedMatch` → `edo-cfihos:Document`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: TechnicalArtifact covers informational artefacts used by EDO. In a CFIHOS handover perspective, many such artefacts correspond to documents or document references.

### `edo-cfihos:EquipmentClass` — CFIHOS equipment class

#### `edo:Asset` — Asset
- Mapping: `relatedMatch` → `edo-cfihos:EquipmentClass`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: Asset is related to CFIHOS tag and equipment classification, but exact mapping depends on whether the EDO class is used as a functional asset, physical asset, system or equipment concept.

#### `edo:DomainElement` — Domain Element
- Mapping: `relatedMatch` → `edo-cfihos:EquipmentClass`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: DomainElement is broader than CFIHOS tag or equipment classes. It represents EDO concepts that make up projects or assets and can participate in information deliveries, including physical, functional and informational elements.

### `edo-cfihos:LifecycleInformation` — CFIHOS lifecycle information

#### `edo:AsBuiltRole` — As-built role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: AsBuiltRole marks as-built information relevant to handover and operation.

#### `edo:CertifiedRole` — Certified role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: CertifiedRole marks certified values that can support traceability and acceptance in handover information.

#### `edo:DesignRole` — Design role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: DesignRole marks design-stage information relevant to handover and lifecycle data management.

#### `edo:OperatingRole` — Operating role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: OperatingRole marks operating information relevant to lifecycle operation and maintenance contexts.

#### `edo:TestRole` — Test role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: TestRole marks test information that may support verification, acceptance and handover traceability.

#### `edo:lifecycleRole` — Lifecycle role
- Mapping: `relatedMatch` → `edo-cfihos:LifecycleInformation`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: lifecycleRole classifies the role of a value in the asset lifecycle, such as requirement, design, certified, installed, as-built, operating or test information. This supports CFIHOS-style handover interpretation without making the EDO core dependent on CFIHOS.

### `edo-cfihos:Property` — CFIHOS Property

#### `edo:DomainAttribute` — Domain Attribute
- Mapping: `closeMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: DomainAttribute is the EDO operational concept closest to a CFIHOS property: it represents a named information requirement or property that can be used in data dictionaries and data contracts.

#### `edo:FunctionalAttribute` — Functional Attribute
- Mapping: `relatedMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: FunctionalAttribute represents functional characteristics or capabilities that may appear as handover properties.

#### `edo:IdentificationAttribute` — Identification Attribute
- Mapping: `relatedMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: IdentificationAttribute represents identifiers and naming-related properties used in information handover.

#### `edo:PhysicalPropertyAttribute` — Physical Property Attribute
- Mapping: `relatedMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: PhysicalPropertyAttribute represents physical properties used as delivered or required property information.

#### `edo:hasTypedValue` — Has Typed Value
- Mapping: `relatedMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: hasTypedValue records the expected value datatype category of an EDO attribute. It is related to, but not equivalent to, CFIHOS property value typing.

#### `edo:hasValueCardinality` — Has Value Cardinality
- Mapping: `relatedMatch` → `edo-cfihos:Property`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: hasValueCardinality records whether an EDO attribute is expected to have a single value or multiple values. It supports data-contract validation rather than representing a CFIHOS concept directly.

### `edo-cfihos:Requirement` — CFIHOS requirement

#### `edo:RequirementRole` — Requirement role
- Mapping: `closeMatch` → `edo-cfihos:Requirement`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: RequirementRole marks EDO attributes whose values express required, contractual or specification-driven information.

#### `edo:Specification` — Specification
- Mapping: `relatedMatch` → `edo-cfihos:Requirement`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: Specification may act both as a document-like artefact and as a source of requirements for property values or information delivery constraints.

### `edo-cfihos:TagClass` — CFIHOS tag class

#### `edo:Asset` — Asset
- Mapping: `relatedMatch` → `edo-cfihos:TagClass`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: Asset is related to CFIHOS tag and equipment classification, but exact mapping depends on whether the EDO class is used as a functional asset, physical asset, system or equipment concept.

#### `edo:DomainElement` — Domain Element
- Mapping: `relatedMatch` → `edo-cfihos:TagClass`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:MediumConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: DomainElement is broader than CFIHOS tag or equipment classes. It represents EDO concepts that make up projects or assets and can participate in information deliveries, including physical, functional and informational elements.

### `edo-cfihos:UnitOfMeasure` — CFIHOS unit of measure

#### `edo:hasUnit` — Has Unit
- Mapping: `closeMatch` → `edo-cfihos:UnitOfMeasure`
- Alignment status: `edo-align:ProposedAlignment`
- Confidence: `edo-align:HighConfidence`
- Review status: `edo-align:UnderReview`
- Source standard: `CFIHOS / IOGP`
- Rationale: hasUnit records the expected unit for an EDO domain attribute. This is close to the CFIHOS treatment of unit of measure associated with property values.
