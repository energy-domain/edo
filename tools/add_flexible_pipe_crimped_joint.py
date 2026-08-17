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


joint = U("FlexiblePipeCrimpedJoint")
g.add((joint, RDF.type, OWL.Class))
g.add((joint, RDFS.subClassOf, U("PhysicalConnection")))
g.add((joint, DCT.identifier, Literal("FlexiblePipeCrimpedJoint")))
g.add((joint, SKOS.prefLabel, Literal("Flexible Pipe Crimped Joint", lang="en")))
g.add((joint, SKOS.prefLabel, Literal("Junta Crimpada de Duto Flexível", lang="pt-br")))
g.add((joint, SKOS.definition, Literal(
    "Permanent structural and pressure-containing physical connection formed by crimping an end fitting onto a flexible pipe segment.",
    lang="en",
)))
g.add((joint, SKOS.definition, Literal(
    "Conexão física permanente, estrutural e de contenção de pressão, formada pela crimpagem de um end fitting em um tramo de duto flexível.",
    lang="pt-br",
)))

# A flexible-pipe crimped joint is categorically different from a flanged joint.
g.add((joint, OWL.disjointWith, U("FlangedJoint")))

# Exactly two role-specific endpoints: one pipe-side crimped point and one end-fitting-side point.
qcard("FlexiblePipeCrimpedJoint", "connectsPoint", "FlexiblePipeCrimpedConnection", 1)
qcard("FlexiblePipeCrimpedJoint", "connectsPoint", "EndFittingCrimpedConnection", 1)
all_values_union(
    "FlexiblePipeCrimpedJoint",
    "connectsPoint",
    ["FlexiblePipeCrimpedConnection", "EndFittingCrimpedConnection"],
)

# Guard against accidentally broadening this joint to generic crimped endpoints.
assert (joint, RDFS.subClassOf, U("PhysicalConnection")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added FlexiblePipeCrimpedJoint; ontology now has {len(g)} triples")
