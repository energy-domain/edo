import json
from rdflib import Graph, URIRef, RDF, RDFS, OWL

def process_ontology(ttl_file):
    g = Graph()
    g.parse(ttl_file, format="turtle")
    
    EDO = "https://w3id.org/energy-domain/edo#"
    DomainElement = URIRef(EDO + "DomainElement")
    DomainAttribute = URIRef(EDO + "DomainAttribute")
    hasAttribute = URIRef(EDO + "hasAttribute")

    # Dicionário para armazenar todas as classes
    classes = {}

    # 1. Função recursiva para encontrar todas as subclasses
    def find_subclasses(class_uri):
        subclasses = []
        for s in g.subjects(RDFS.subClassOf, class_uri):
            s_uri = str(s)
            if s_uri not in classes:
                classes[s_uri] = {
                    "uri": s_uri,
                    "label": get_label(g, s),
                    "annotations": get_annotations(g, s),
                    "attributes": [],
                    "is_leaf": True  # Será atualizado se tiver subclasses
                }
                # Encontra subclasses desta classe recursivamente
                child_subclasses = find_subclasses(s)
                if child_subclasses:
                    classes[s_uri]["is_leaf"] = False
                subclasses.append({
                    "uri": s_uri,
                    "subclasses": child_subclasses
                })
        return subclasses

    # 2. Construir a hierarquia completa a partir de DomainElement
    hierarchy = find_subclasses(DomainElement)

    # 3. Processar atributos para todas as classes encontradas
    for class_uri, class_data in classes.items():
        # Atributos diretos
        for attr in g.objects(URIRef(class_uri), hasAttribute):
            if (attr, RDFS.subClassOf, DomainAttribute) in g:
                class_data["attributes"].append({
                    "uri": str(attr),
                    "label": get_label(g, attr),
                    "inherited": False,
                    "annotations": get_annotations(g, attr)
                })

        # Atributos herdados (para classes folha)
        if class_data["is_leaf"]:
            current = URIRef(class_uri)
            while True:
                # Pegar superclasse direta (que não seja DomainElement)
                superclasses = list(g.objects(current, RDFS.subClassOf))
                superclasses = [sc for sc in superclasses if str(sc) in classes]
                
                if not superclasses:
                    break
                
                super_uri = superclasses[0]
                for attr in g.objects(super_uri, hasAttribute):
                    if (attr, RDFS.subClassOf, DomainAttribute) in g:
                        attr_uri = str(attr)
                        if not any(a["uri"] == attr_uri for a in class_data["attributes"]):
                            class_data["attributes"].append({
                                "uri": attr_uri,
                                "label": get_label(g, attr),
                                "inherited": True,
                                "annotations": get_annotations(g, attr)
                            })
                current = super_uri

    # 4. Construir a estrutura final combinando hierarquia e atributos
    def build_final_hierarchy(hierarchy_nodes):
        final_nodes = []
        for node in hierarchy_nodes:
            class_data = classes[node["uri"]].copy()
            class_data["subclasses"] = build_final_hierarchy(node["subclasses"])
            final_nodes.append(class_data)
        return final_nodes

    taxonomy = build_final_hierarchy(hierarchy)
    return taxonomy

def get_label(g, uri):
    label = g.value(URIRef(uri), RDFS.label)
    if label:
        return str(label)
    return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]

def get_annotations(g, uri):
    annotations = {}
    for p, o in g.predicate_objects(URIRef(uri)):
        if str(p) in ["http://www.w3.org/2000/01/rdf-schema#label", 
                     "http://www.w3.org/2000/01/rdf-schema#comment",
                     "http://www.w3.org/2004/02/skos/core#definition"]:
            key = str(p).split("/")[-1].split("#")[-1]
            annotations[key] = str(o)
        elif str(p).startswith("https://w3id.org/energy-domain/edo#"):
            key = str(p).split("#")[-1]
            annotations[key] = str(o)
    return annotations

# Processar e gerar JSON
taxonomy = process_ontology("energy-domain-ontology.ttl")
with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, indent=2, ensure_ascii=False)
print("JSON gerado com sucesso!")