### General Ontology Schematic

#### Objectives / Use Cases  
1) **Serve as an information source** for generating technical specifications for clients (text with definitions, supplemented by spreadsheets and diagrams)  
2) **Provide verification data** for client project validation (via SHACL or IDS)  
3) **Support translators** (IFC STEP parser and future standards like CFIHOS)  
4) **Facilitate community discussions** as a communication framework  

---

#### Artifacts  
1) **Core Ontology**  
   - Primary TTL file (created/edited in Protégé + team scripts)  
   - Generated files: JSON-LD, N-Triples (via Protégé), OWL HTML (via script)  

2) **Sub-ontologies**  
   - TTL files generated via SPARQL queries and auxiliary scripts  
   - Represent subdomains, disciplines, lifecycle phases, and all derived outputs  

3) **Documentation Page**  
   - HTML page describing the core ontology and sub-ontologies  

---

#### Workflows  

1) **Core Ontology Creation/Editing/Maintenance**  
   - Clone repository  
   - Follow branch procedure  
   - Consult ontology standards document  
   - Edit via Protégé or scripts  
   - Commit → Pull Request → Merge  
   - Generate JSON-LD, N-Triples, and OWL HTML  
   - Update sub-ontologies  

2) **New Sub-ontology Creation**  
   - Add new repository folders  
   - Develop SPARQL queries + auxiliary scripts  
   - Set up w3id redirection  
   - Generate all derivative files  

--- 

### Key Improvements:  
- **Hierarchical organization** with clear sections  
- **Concise phrasing** while preserving technical details  
- **Consistent terminology** (e.g., "generate" instead of mixed verbs)  
- **Action-oriented workflow steps**  
- **Standardized file format references** (TTL, JSON-LD, etc.)  

Would you like to expand any section (e.g., add examples for SPARQL queries or Protégé steps)?

