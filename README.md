# Energy Domain Ontology (EDO)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

The **Energy Domain Ontology (EDO)** provides a semantic foundation for representing engineering concepts, entities, properties, and relationships across the energy sector.

EDO supports consistent interpretation and exchange of engineering information across disciplines, systems, and organizations, with a particular focus on subsea oil and gas engineering.

The ontology combines Semantic Web technologies with **openBIM principles** and **Industry Foundation Classes (IFC)** to support structured, machine-readable engineering knowledge and interoperable data contracts.

EDO separates the continuous evolution of domain knowledge from the stable semantic references required for engineering information exchange, validation, and publication.

## Objectives

EDO is intended to support:

- **Semantic consistency:** Establish shared definitions for engineering concepts, properties, and relationships.
- **Interoperability:** Facilitate information exchange across engineering disciplines, applications, and organizations.
- **Engineering data contracts:** Provide semantic references for specifying and validating structured engineering information.
- **Knowledge representation:** Represent domain concepts and their relationships independently of individual software applications.
- **Traceability:** Maintain explicit relationships between semantic definitions, ontology versions, and derived artifacts.
- **Controlled evolution:** Support the review and consolidation of domain knowledge while preserving identifiable versions for downstream use.

## Architectural Principles

### Evolving Core Ontology

The EDO core maintains the evolving semantic model of the energy domain.

Its primary ontology is maintained in:

`core/energy-domain-ontology.ttl`

Changes to the core are managed through the project's review and maintenance processes.

The evolving core should not be confused with a frozen ontology release intended for use as a stable contractual or technical reference.

### Domain-Specific Semantic Models

EDO supports the representation of engineering knowledge associated with specific disciplines and technical domains.

Domain-specific concepts may include equipment, systems, components, properties, classifications, and engineering relationships.

The integration of such knowledge into the EDO core is subject to semantic review and the applicable governance process.

### Versioned Releases

The repository includes a `release/` directory for organizing version-specific ontology artifacts.

Releases provide identifiable semantic references that can support engineering data contracts, documentation, validation, and other downstream uses.

The release process addresses version identification, ontology metadata, artifact preservation, and traceability.

A directory in the repository does not, by itself, establish that a release has completed all formal publication and approval activities.

### Transitional Ontologies

The `transitional/` directory contains semantic artifacts developed for exceptional delivery circumstances in which the necessary domain consensus has not yet been established.

Transitional ontologies are context-specific and must remain distinguishable from the consensual EDO core.

They are not normative references and must not be treated as formally consolidated domain semantics.

The repository includes **EDO-SRP**, a transitional ontology associated with the Subsea Rigid Pipes domain.

See [Transitional Ontologies](transitional/README.md) for the applicable architectural restrictions and lifecycle principles.

## Repository Structure

The following structure identifies the principal directories and selected files in the repository.

```text
edo/
├── core/
│   ├── energy-domain-ontology.ttl
│   ├── energy-domain-ontology-shacl.ttl
│   └── energy-domain-ontology.properties
│
├── edo-sandbox/
│   └── edo-sandbox.ttl
│
├── governance/
│   ├── extraction/
│   ├── maintenance/
│   └── review/
│
├── release/
│   ├── 0.1/
│   │   ├── core/
│   │   └── subsea-flexible-pipes/
│   └── 0.2/
│       ├── core/
│       └── electric-hydraulic-umbilicals/
│
├── transitional/
│   ├── README.md
│   └── edo-srp/
│       └── README.md
│
├── docs/
│   ├── index.md
│   ├── energy-domain-ontology.html
│   └── changelog/
│
├── README.md
└── LICENSE.md
```

*This is a structural overview, not an exhaustive file inventory. The contents and organization of the repository may evolve.*

### Directory Responsibilities

| Directory | Purpose |
|---|---|
| `core/` | Main ontology and associated semantic resources |
| `edo-sandbox/` | Sandbox resources for ontology experimentation |
| `governance/` | Ontology extraction, maintenance, and review resources |
| `release/` | Version-specific ontology directories |
| `transitional/` | Exceptional, non-consensual semantic artifacts |
| `docs/` | Documentation, ontology representations, and supporting materials |

## Semantic Technologies and Interoperability

EDO uses Semantic Web technologies to represent engineering knowledge in a form that can be interpreted and processed by software.

Its technical context includes:

- **RDF:** Graph-based representation of semantic information.
- **OWL:** Formal representation of ontology concepts and relationships.
- **Turtle (TTL):** Human-readable serialization of RDF information.
- **SHACL:** Representation of constraints used to assess RDF data against defined shapes.
- **IFC:** Open information models for the exchange of built-asset and engineering information.
- **openBIM:** Principles and practices supporting interoperable, vendor-neutral information exchange.
- **bSDD:** buildingSMART Data Dictionary, used in the broader publication methodology for engineering concepts and properties.
- **IDS:** Information Delivery Specification, used to express machine-checkable information requirements within its supported scope.

These technologies serve different purposes and are not interchangeable. EDO provides the semantic foundation, while downstream artifacts and tools address specific exchange, documentation, and validation requirements.

## Engineering Data Contracts

An important application of EDO is the definition and publication of **Open BIM IFC data contracts**.

A data contract establishes the information expected in an engineering exchange, including applicable entities, properties, relationships, and associated requirements.

The publication methodology describes a process in which an identified EDO release serves as the semantic source for related artifacts.

Depending on the contract scope and applicable procedures, these artifacts may include:

1. A buildingSMART Data Dictionary publication.
2. Engineering spreadsheets documenting classes, properties, and relationships.
3. Relationship diagrams.
4. IFC example models.
5. IDS and extended validation specifications.
6. Versioned publication packages and persistent references.
7. Supporting technical documentation.

The existence of a publication procedure does not imply that every artifact has already been generated or published for every ontology version.

## Governance and Versioning

EDO distinguishes between evolving ontology content and identifiable, version-specific semantic references.

Governance is intended to maintain semantic consistency, control changes, and preserve the traceability of information used by downstream consumers.

The release methodology addresses:

- Ontology version identification and metadata.
- Release and transitional classifications.
- Source repository references.
- Version-specific artifact organization.
- Persistent identifiers.
- Publication manifests.
- Traceability between EDO and derived resources.
- Review and publication checks.

The project distinguishes Git references, repository artifacts, and persistent ontology URIs. These identifiers serve complementary purposes and should not be considered interchangeable.

The EDO base URI is:

`https://w3id.org/energy-domain/edo`

Version-specific identifiers and publication metadata must follow the applicable, approved release procedures.

## Getting Started

### Access the Repository

The source repository is available at:

https://github.com/energy-domain/edo

### Explore the Ontology

The primary ontology file is:

[core/energy-domain-ontology.ttl](core/energy-domain-ontology.ttl)

The repository also includes associated semantic resources, governance artifacts, documentation, and version-specific directories.

### Review the Documentation

Begin with the repository's [documentation index](docs/index.md).

Additional resources are available in:

- [Core ontology](core/)
- [Governance resources](governance/)
- [Release directories](release/)
- [Transitional ontologies](transitional/)
- [Documentation](docs/)

### Inspect Ontology Resources

RDF and OWL-compatible tools, including [Protégé](https://protege.stanford.edu/), can be used to inspect ontology definitions and relationships.

Interpretation of ontology content should account for its version, governance status, and intended domain scope.

## Contributions and Review

Changes to ontology content should preserve semantic consistency, traceability, and alignment with the project's governance procedures.

Proposed changes should identify the affected concepts, provide a technical rationale, and distinguish semantic modifications from documentation or editorial corrections.

Contributions intended for integration into the core ontology require the appropriate review and approval.

Transitional semantic artifacts must remain subject to their defined restrictions and must not be treated as approved core ontology content.

## Related Resources

- [EDO Repository](https://github.com/energy-domain/edo)
- [EDO Documentation](docs/index.md)
- [buildingSMART International](https://www.buildingsmart.org/)
- [W3C Semantic Web Standards](https://www.w3.org/standards/semanticweb/)

## License

EDO is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

See the repository's license file for the applicable terms and attribution requirements.
