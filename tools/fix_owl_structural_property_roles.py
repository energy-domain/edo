from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")

HAS_ATTRIBUTE = EDO.hasAttribute

# hasAttribute is used by OWL restrictions to relate domain-element individuals to
# DomainAttribute individuals. It therefore cannot remain an AnnotationProperty.
g.remove((HAS_ATTRIBUTE, RDF.type, OWL.AnnotationProperty))
g.remove((HAS_ATTRIBUTE, RDFS.subProperty