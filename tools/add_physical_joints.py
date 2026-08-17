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


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
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


def add_joint(name, label_en, label_pt, def_en, def_pt):
    joint = U(name)
    g.add((joint, RDF.type, OWL.Class))
    g.add((joint, RDFS.subClassOf, U("PhysicalConnection")))
    g.add((joint, DCT.identifier, Literal(name)))
    g.add((joint, SKOS.prefLabel, Literal(label_en, lang="en")))
    g.add((joint, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    g.add((joint, SKOS.definition, Literal(def_en, lang="en")))
    g.add((joint, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return joint


# Flexible-pipe crimped joint: two different endpoint roles.
crimped = add_joint(
    "FlexiblePipeCrimpedJoint",
    "Flexible Pipe Crimped Joint",
    "Junta Crimpada de Duto Flexível",
    "Permanent structural and pressure-containing physical connection formed by crimping an end fitting onto a flexible pipe segment.",
    "Conexão física permanente, estrutural e de contenção de pressão, formada pela crimpagem de um end fitting em um tramo de duto flexível.",
)
qcard("FlexiblePipeCrimpedJoint", "connectsPoint", "FlexiblePipeCrimpedConnection", 1)
qcard("FlexiblePipeCrimpedJoint", "connectsPoint", "EndFittingCrimpedConnection", 1)
all_values_union(
    "FlexiblePipeCrimpedJoint",
    "connectsPoint",
    ["FlexiblePipeCrimpedConnection", "EndFittingCrimpedConnection"],
)

# Welded joint: both endpoints are weldable fluid ports of the same semantic type.
welded = add_joint(
    "WeldedJoint",
    "Welded Joint",
    "Junta Soldada",
    "Permanent physical connection formed by welding two welded fluid-port connection points.",
    "Conexão física permanente formada pela soldagem de dois pontos de conexão de porta de fluido do tipo soldado.",
)
qcard("WeldedJoint", "connectsPoint", "WeldedConnection", 2)
all_values("WeldedJoint", "connectsPoint", "WeldedConnection")

# The modeled joint categories are mutually distinct.
for a, b in (
    ("FlangedJoint", "FlexiblePipeCrimpedJoint"),
    ("FlangedJoint", "WeldedJoint"),
    ("FlexiblePipeCrimpedJoint", "WeldedJoint"),
):
    g.add((U(a), OWL.disjointWith, U(b)))

for joint in (crimped, welded):
    assert (joint, RDFS.subClassOf, U("PhysicalConnection")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added physical joints; ontology now has {len(g)} triples")
