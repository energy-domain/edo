from rdflib import Graph, URIRef, RDF, RDFS, OWL

# Carrega a ontologia do arquivo TTL
input_file = "energy-domain-ontology copy.ttl"  # Substitua pelo seu arquivo
output_file = "ontologia_modificada.ttl"  # Arquivo de saída

g = Graph()
g.parse(input_file, format="turtle")

# Define os namespaces (ajuste conforme sua ontologia)
DOMAIN_ATTRIBUTE = URIRef("https://w3id.org/energy-domain/edo#DomainAttribute")  # Substitua pelo URI correto
OWL_Class = URIRef(str(RDF.type), OWL.Class)
OWL_DatatypeProperty = URIRef(str(RDF.type), OWL.DatatypeProperty)

# Encontra todas as subclasses folha de :DomainAttribute
subclasses_folha = set()

# Primeiro, encontra todas as subclasses (diretas e indiretas)
all_subclasses = set()
for s in g.subjects(RDFS.subClassOf, DOMAIN_ATTRIBUTE):
    all_subclasses.add(s)
    for ss in g.transitive_subjects(RDFS.subClassOf, s):  # Subclasses indiretas
        all_subclasses.add(ss)

# Depois, filtra apenas as folhas (que não são superclasses de nada)
for subclass in all_subclasses:
    is_folha = True
    for s in g.subjects(RDFS.subClassOf, subclass):
        if s != subclass:  # Ignora autorreferências
            is_folha = False
            break
    if is_folha:
        subclasses_folha.add(subclass)

# Modifica o rdf:type para owl:DatatypeProperty
for classe in subclasses_folha:
    # Remove a declaração como owl:Class
    g.remove((classe, RDF.type, OWL.Class))
    # Adiciona como owl:DatatypeProperty
    g.add((classe, RDF.type, OWL.DatatypeProperty))

# Salva a ontologia modificada
g.serialize(destination=output_file, format="turtle")
print(f"Ontologia modificada salva em {output_file}")
print(f"Classes modificadas: {len(subclasses_folha)}")