```markdown
# Energy Domain Ontology (EDO)

[![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

The **Energy Domain Ontology (EDO)** is a structured, semantic representation of concepts, entities, and relationships within the energy sector. Its primary goal is to support consistent data integration, knowledge sharing, and interoperability across engineering disciplines, particularly in subsea oil and gas projects.

EDO follows **Open BIM principles** and uses **IFC-based modelling standards**, extended with semantic web technologies and ontologies.

## Repository Structure

```

edo/                                   # root repo
 ├─ core/                              # live version of the EDO core
 │    └─ energy-domain-ontology.ttl    # main file, always evolving
 │
 ├─ edo-sandbox/          # edo sandbox for testing
 │    └─ edo-sandbox.ttl
 │
 ├─ release/                # static versions (releases) of the core and subontologies
 │    └─ x.y/               # specific version
 │         ├─ core/         # serialisations of version x.y of the core
 │         │    ├─ energy-domain-ontology.ttl
 │         │    ├─ energy-domain-ontology.rdf
 │         │    └─ ...
 │         ├─ <subontology_name>/   # specific subontology of version x.y
 │         │    ├─ subontology.ttl
 │         │    ├─ subontology.rdf
 │         │    └─ ...
 │         └─ README.md     # describes what is included in release x.y
 │
 ├─ governance/             # EDO governance ontologies
 │    ├─ maintenance/       # maintenance, scripts, patches
 │    │    └─ edo-gov-maintenance.ttl
 │    └─ review/            # comments, issues, proposals for evolution
 │         └─ edo-gov-review.ttl
 └─ docs/                   # general documentation, explaining structure, standards, etc.
      └─ index.md

````

## Core Features

- Semantic representation of energy domain entities, systems, and processes  
- Sub-ontologies for specialised areas such as subsea pipelines, flexible risers, and equipment engineering  
- Versioned releases for stable deployments while keeping a live, evolving core ontology  
- Interoperability with IFC and Open BIM standards  
- Extensible for additional disciplines and attributes  

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/energy-domain/edo.git
cd edo
````

2. **Explore the core ontology**
   The live core is located in `core/energy-domain-ontology.ttl`. Sub-ontologies are under `subontologies/`.

3. **Use a Turtle/OWL editor**
   Recommended tools: [Protégé](https://protege.stanford.edu/) or any RDF/Turtle-compatible editor.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Make your changes and commit (`git commit -am 'Add feature'`).
4. Push to your branch (`git push origin feature/my-feature`).
5. Open a Pull Request with a clear description of your changes.

Ensure all ontology updates comply with existing EDO standards and naming conventions.

## License

This project is licensed under **Attribution 4.0 International (CC BY 4.0)**. See the [LICENSE](LICENSE) file for details.

```

Se você quiser, posso também **remover a seção de Contact** completamente e deixar o README mais enxuto para GitHub. Quer que eu faça isso?
```
