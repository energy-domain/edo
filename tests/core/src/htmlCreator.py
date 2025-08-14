import json
from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL

def process_ontology(ttl_file):
    # Carrega a ontologia
    g = Graph()
    g.parse(ttl_file, format="turtle")
    
    # Namespace da ontologia
    EDO = "https://w3id.org/energy-domain/edo#"
    
    # Classes importantes
    DomainElement = URIRef(EDO + "DomainElement")
    DomainAttribute = URIRef(EDO + "DomainAttribute")
    hasAttribute = URIRef(EDO + "hasAttribute")
    
    # Dicionário para armazenar a taxonomia
    taxonomy = {}
    
    # 1. Encontrar todas as subclasses de DomainElement
    elements = {}
    for s in g.subjects(RDF.type, OWL.Class):
        if (s, RDFS.subClassOf, DomainElement) in g:
            elements[s] = {
                "uri": str(s),
                "label": get_label(g, s),
                "subclasses": [],
                "attributes": [],
                "annotations": get_annotations(g, s),
                "is_leaf": True  # Será atualizado depois
            }
    
    # 2. Construir a hierarquia
    for element in elements.values():
        # Verificar superclasses (apenas uma para simplificar)
        for superclass in g.objects(URIRef(element["uri"]), RDFS.subClassOf):
            if str(superclass) != str(DomainElement) and str(superclass) in elements:
                elements[superclass]["subclasses"].append(element["uri"])
                elements[superclass]["is_leaf"] = False
    
    # 3. Encontrar as classes folha (sem subclasses)
    leaf_classes = [uri for uri, data in elements.items() if data["is_leaf"]]
    
    # 4. Adicionar atributos
    for element_uri, element_data in elements.items():
        # Atributos diretos
        direct_attributes = list(g.objects(element_uri, hasAttribute))
        for attr in direct_attributes:
            if (attr, RDF.type, OWL.Class) in g and (attr, RDFS.subClassOf, DomainAttribute) in g:
                element_data["attributes"].append({
                    "uri": str(attr),
                    "label": get_label(g, attr),
                    "inherited": False,
                    "annotations": get_annotations(g, attr)
                })
        
        # Se for classe folha, adicionar atributos herdados
        if element_uri in leaf_classes:
            current = element_uri
            while True:
                # Encontrar superclasse (apenas uma para simplificar)
                superclasses = list(g.objects(current, RDFS.subClassOf))
                domain_superclasses = [sc for sc in superclasses if str(sc) in elements]
                
                if not domain_superclasses:
                    break
                    
                superclass = domain_superclasses[0]
                # Adicionar atributos da superclasse
                for attr in g.objects(superclass, hasAttribute):
                    if (attr, RDF.type, OWL.Class) in g and (attr, RDFS.subClassOf, DomainAttribute) in g:
                        # Verificar se o atributo já foi adicionado
                        attr_uri = str(attr)
                        if not any(a["uri"] == attr_uri for a in element_data["attributes"]):
                            element_data["attributes"].append({
                                "uri": attr_uri,
                                "label": get_label(g, attr),
                                "inherited": True,
                                "annotations": get_annotations(g, attr)
                            })
                current = superclass
    
    # 5. Encontrar a raiz da taxonomia (classes que são subclasses diretas de DomainElement)
    root_elements = [uri for uri in elements if (URIRef(uri), RDFS.subClassOf, DomainElement) in g]
    
    # 6. Construir a estrutura hierárquica
    def build_hierarchy(uri):
        element = elements[uri]
        node = {
            "uri": element["uri"],
            "label": element["label"],
            "annotations": element["annotations"],
            "attributes": element["attributes"],
            "subclasses": [build_hierarchy(sub_uri) for sub_uri in element["subclasses"]]
        }
        return node
    
    taxonomy = [build_hierarchy(root) for root in root_elements]
    
    return taxonomy

def get_label(g, uri):
    # Tenta obter o label, senão retorna o nome local do URI
    label = g.value(uri, RDFS.label)
    if label:
        return str(label)
    else:
        return str(uri).split("#")[-1] if "#" in str(uri) else str(uri).split("/")[-1]

def get_annotations(g, uri):
    annotations = {}
    for p, o in g.predicate_objects(uri):
        if str(p) in ["http://www.w3.org/2000/01/rdf-schema#label", 
                     "http://www.w3.org/2000/01/rdf-schema#comment",
                     "http://www.w3.org/2004/02/skos/core#definition"]:
            key = str(p).split("/")[-1].split("#")[-1]
            annotations[key] = str(o)
        elif str(p).startswith("https://w3id.org/energy-domain/edo#"):
            key = str(p).split("#")[-1]
            annotations[key] = str(o)
    return annotations

# Processar a ontologia e gerar o JSON
taxonomy = process_ontology("energy-domain-ontology.ttl")
with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, indent=2, ensure_ascii=False)

print("JSON gerado com sucesso: taxonomy.json")