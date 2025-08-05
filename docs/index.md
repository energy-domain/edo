# Energy Domain Ontology (EDO)

Welcome to the official documentation of the **Energy Domain Ontology (EDO)**. This ontology serves as a semantic framework for the structured representation, exchange, and validation of information across the full lifecycle of assets in the energy sector.

**Namespace:** [`https://w3id.org/energy-domain/edo`](https://w3id.org/energy-domain/edo)  
**Prefix:** `edo:`  
**Stable Releases:** Hosted on GitHub and Zenodo with permanent URLs via [w3id.org](https://w3id.org)

---

## 🔷 Executive Overview

The Energy Domain Ontology is a collaborative, standards-driven initiative to support information interoperability in the energy sector. It is designed to serve the needs of clients (owners), engineering contractors, equipment and material suppliers, and software vendors.

EDO enables:

- Standardised information exchange across all lifecycle phases.
- Specification of data delivery requirements in open formats such as IFC.
- Support for project validation and compliance using SHACL and IDS.
- Foundation for extensions to the IFC standard for the energy sector.
- Alignment with global standards such as ISO 15926 and CFIHOS.

EDO is developed openly, with contributions and reviews from specialists across engineering disciplines and energy subdomains. A versioned, peer-reviewed core ontology is maintained, from which stable subontologies are derived for each sector and discipline.

---

## 🏗️ Scope and Domain Coverage

EDO covers information flows across all lifecycle phases:

- Conceptual Design  
- Basic Design  
- Detailed/Executive Design  
- Procurement  
- Installation/Construction  
- Commissioning  
- Operation  
- Maintenance  
- Decommissioning

### Subdomains Covered

#### 1. Oil & Gas  
- **Upstream:** Offshore platforms  
- **Downstream:** Refineries  
- **Subsea:** Subsea Wet Christmas Trees, Manifolds, Flexible and Rigid Risers and Flowlines, Umbilicals

#### 2. Other Energy Sectors  
- **Nuclear:** Power generation facilities  
- **Renewables:** Renewable energy plants

### Technical Disciplines Included

- Equipment (static and rotating)  
- Process Piping  
- Instrumentation and Control  
- Electrical  
- Civil and Structural  
- Subsea Systems  
- Others (as needed)

---

## 🧠 Ontology Modelling Strategy

EDO is modelled incrementally using [Protégé](https://protege.stanford.edu/), following best practices in OWL and Linked Data. It is structured as:

### Core Ontology

A centralised ontology representing all energy subdomains and disciplines, used as the authoritative source for:

- Data validation
- Subontology extraction
- Ontology-driven specification generation

### Subontologies

When a specific combination of **discipline** and **sector** achieves consensus maturity, a corresponding subontology is extracted. This subontology serves as the formal base for:

- Technical Specifications for information delivery
- IFC data modelling rules and diagrams
- SHACL and IDS validation templates

---

## 📦 Publication and Versioning

Each stable release of the core and subontologies is published in the following formats:

- `.ttl` (Turtle)
- `.jsonld` (JSON-LD)
- `.nt` (N-Triples)
- `.owl` (RDF/XML)
- `.html` (Human-readable rendering)

They are versioned using semantic versioning and hosted at:

- GitHub: [`github.com/your-org`](https://github.com/your-org)
- Zenodo (DOI for each release)
- Persistent URL via: [`https://w3id.org/energy-domain`](https://w3id.org/energy-domain)

---

## 🌐 Community Participation

All modelling and publication steps are transparent and open to stakeholder review. A collaborative workflow is implemented through **GitHub Issues**, where experts can:

- Comment on individual ontology entities (classes and properties)
- Suggest modifications
- Participate in approval workflows

Our team mediates the discussions to reach consensus before locking subontology versions.

---

## 📄 Technical Specifications

Once a subontology reaches maturity, a **Technical Specification** is generated including:

- Textual normative guidelines  
- Rules for modelling IFC-based data  
- Visual diagrams  
- Supporting spreadsheets derived from the ontology

These documents guide **clients** in contracting deliverables and **suppliers/contractors** in generating compliant models.

---

## ⚙️ Tooling and Applications

EDO supports various technical applications, including:

### IFC Interoperability

- Rule-based generation of IFC data using ontology-driven specifications
- Support for translators between IFC and other formats
- Guidance for extending IFC for energy-specific classes and attributes

### Project Validation

- Generation of [SHACL](https://www.w3.org/TR/shacl/) shapes from ontology classes and properties
- Creation of [buildingSMART IDS](https://technical.buildingsmart.org/standards/ids/) templates for requirement validation

### SPARQL and SHACL Examples

Examples and code snippets are available in the [Documentation Section](#documentation) to support:

- Data querying
- Consistency checking
- Automated validation

---

## 📚 Documentation

A complete documentation portal is provided, including:

### Executive Section

- Vision and roadmap
- Stakeholder benefits
- Governance model

### Technical Section

- Modelling conventions and methodology
- Procedures for creating, editing, and maintaining the core ontology
- Guidelines for subontology extraction
- SPARQL and SHACL usage examples
- Naming conventions, annotations, and versioning practices

---

## 📞 Contact and Contributions

We welcome collaboration from engineers, ontology experts, software developers, and stakeholders across the energy domain.

To contribute or get in touch:

- Visit: [`https://github.com/your-org`](https://github.com/your-org)
- Submit Issues or Pull Requests
- Join the discussion via GitHub Discussions

---

© [Your Organisation], under [Creative Commons CC0 1.0 Universal License](https://creativecommons.org/publicdomain/zero/1.0/)
