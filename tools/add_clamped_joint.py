from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def qcard(cls, prop, target, n):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))


def all_values_union(cls, prop, names):
    union = BNode()
    head = BNode()
    g.add((union, RDF.type, OWL.Class))
    Collection(g, head, [U(name) for name in names])
    g.add((union, OWL.unionOf, head))

    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, union))
    g.add((U(cls), RDFS.subClassOf, r))


joint = U("ClampedJoint")
g.add((joint, RDF.type, OWL.Class))
g.add((joint, RDFS.subClassOf, U("PhysicalConnection")))
g.add((joint, DCT.identifier, Literal("ClampedJoint")))
g.add((joint, SKOS.prefLabel, Literal("Clamped Joint", lang="en")))
g.add((joint, SKOS.prefLabel, Literal("Junta por Abraçadeira", lang="pt-br")))
g.add((joint, SKOS.definition, Literal(
    "Mechanical physical connection formed by distributed clamping contact between a collar clamping surface and a local external clamping surface of a pipe segment.",
    lang="en")))
g.add((joint, SKOS.definition, Literal(
    "Conexão física mecânica formada por contato distribuído de aperto entre a superfície de aperto de um colar e uma região local da superfície externa de um tramo de duto.",
    lang="pt-br")))

qcard("ClampedJoint", "connectsInterface", "CollarClampingSurface", 1)
qcard("ClampedJoint", "connectsInterface", "PipeClampingSurface", 1)
all_values_union(
    "ClampedJoint", "connectsInterface",
    ["CollarClampingSurface", "PipeClampingSurface"],
)

for other in ("FlangedJoint", "FlexiblePipeCrimpedJoint", "WeldedJoint"):
    g.add((joint, OWL.disjointWith, U(other)))

assert (joint, RDFS.subClassOf, U("PhysicalConnection")) in g
assert (U("CollarClampingSurface"), OWL.disjointWith, U("PipeClampingSurface")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added clamped joint; ontology now has {len(g)} triples")
