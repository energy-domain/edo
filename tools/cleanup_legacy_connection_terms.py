from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


# Replace the awkward legacy name ClampedConnection with a surface concept whose
# identifier matches its actual ontological nature.
clamping_surface = U("ClampingSurface")
g.add((clamping_surface, RDF.type, OWL.Class))
g.add((clamping_surface, RDFS.subClassOf, U("MechanicalConnectionSurface")))
g.add((clamping_surface, DCT.identifier, Literal("ClampingSurface")))
g.add((clamping_surface, SKOS.prefLabel, Literal("Clamping Surface", lang="en")))
g.add((clamping_surface, SKOS.prefLabel, Literal("Superfície de Aperto", lang="pt-br")))
g.add((clamping_surface, SKOS.definition, Literal(
    "Mechanical connection surface participating in a clamped attachment through distributed contact pressure.", lang="en")))
g.add((clamping_surface, SKOS.definition, Literal(
    "Superfície de conexão mecânica que participa de uma fixação por abraçadeira por meio de pressão de contato distribuída.", lang="pt-br")))

for child in ("CollarClampingSurface", "PipeClampingSurface"):
    g.remove((U(child), RDFS.subClassOf, U("ClampedConnection")))
    g.add((U(child), RDFS.subClassOf, clamping_surface))

# Retain the old term only as a deprecated compatibility bridge.
g.add((U("ClampedConnection"), OWL.deprecated, Literal(True, datatype=XSD.boolean)))
g.add((U("ClampedConnection"), DCT.isReplacedBy, clamping_surface))
g.remove((U("ClampedConnection"), RDFS.subClassOf, U("MechanicalConnectionSurface")))

# No active class should inherit from the deprecated term.
assert not list(g.subjects(RDFS.subClassOf, U("ClampedConnection")))
assert (U("CollarClampingSurface"), RDFS.subClassOf, clamping_surface) in g
assert (U("PipeClampingSurface"), RDFS.subClassOf, clamping_surface) in g

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Cleaned legacy connection terms; ontology now has {len(g)} triples")
