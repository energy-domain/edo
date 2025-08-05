# Energy Domain Ontology (EDO)

## Overview
The **Energy Domain Ontology (EDO)** is an open, collaborative framework designed to standardise and model data exchanges across stakeholders in the energy sector. It spans the entire project lifecycle—from conceptual design to decommissioning—and covers all disciplines (e.g., equipment, piping, instrumentation, electrical, civil) across the following subdomains:
1. **Oil & Gas**:  
   - Upstream (e.g., oil platforms),  
   - Downstream (e.g., refineries),  
   - Subsea (e.g., ANMs, manifolds, risers, flowlines, umbilicals).  
2. **Nuclear & Renewables**:  
   - Energy production plants.  

EDO serves as the foundation for generating **Technical Specifications** to ensure interoperability via Industry Foundation Classes (IFC), with future extensions to ISO15926 and CFIHOS.

---

## Objectives
- **Standardisation**: Define a unified data model for energy assets and processes.  
- **Interoperability**: Enable seamless data exchange between stakeholders (owners, contractors, suppliers) using IFC.  
- **Verification**: Support project validation via IDS and SHACL rules.  
- **Extension**: Facilitate future IFC expansions for the energy domain.  

---

## Technical Implementation
### Ontology Structure
- **Core Ontology**: Central model encompassing all energy subdomains and disciplines.  
- **Sub-ontologies**: Modular extracts for mature disciplines/sectors, used to generate Technical Specifications.  

### Workflow
1. **Collaborative Development**:  
   - Ontology modelled incrementally in Protégé.  
   - Published on GitHub (`https://w3id.org/energy-domain/edo`) with versions archived in Zenodo (permanent W3ID URLs).  
2. **Expert Review**:  
   - Stakeholders review HTML documentation (GitHub Pages) and submit feedback via GitHub Issues.  
   - Consensus-driven approval workflow mediated by the EDO team.  
3. **Outputs**:  
   - Technical Specifications (normative text, IFC rules, diagrams, spreadsheets).  
   - Validation tools (SPARQL queries, SHACL/IDS rules).  
   - Translators for IFC ↔ other formats.  

### Deliverables
- **Formats**: TTL, JSON-LD, NTriples, OWL/HTML.  
- **Documentation**:  
  - **Executive**: High-level goals, use cases.  
  - **Technical**: Modelling standards, SPARQL/SHACL examples, procedures for ontology maintenance/sub-ontology extraction.  

---

## For Stakeholders
### Clients (Owners)
- Specify IFC-compliant data delivery from contractors using EDO-based Technical Specifications.  

### Designers & Engineers
- Contribute domain expertise via GitHub Issues.  
- Use specifications to ensure project compliance.  

### Software Developers
- Leverage EDO to build IFC-compliant tools or translators.  
- Integrate validation (SHACL/IDS) into workflows.  

### Ontology Engineers
- Participate in modelling via GitHub (issues, pull requests).  
- Follow documented procedures for edits/extractions.  

---

## Roadmap
- **Phase 1**: Core ontology stabilisation (oil & gas focus).  
- **Phase 2**: Expansion to nuclear/renewables.  
- **Phase 3**: Interoperability hub (ISO15926, CFIHOS integration).  

---

## License & Access
- **Repository**: [GitHub](https://github.com/[your-repo])  
- **Permanent URI**: [https://w3id.org/energy-domain/edo](https://w3id.org/energy-domain/edo)  
- **License**: Open-source (specify license, e.g., MIT).  

---

## Get Involved
- **Review**: Access HTML docs via [GitHub Pages](https://[your-org].github.io/[repo]).  
- **Contribute**: Submit feedback via [GitHub Issues](https://github.com/[your-repo]/issues).  
- **Contact**: [Your team email/contact form].  
