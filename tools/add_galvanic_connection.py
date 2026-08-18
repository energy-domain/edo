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


def add_class(name, parent, label_en, label_pt, def_en=None, def_pt=None):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return c


def qcard(cls, prop, target, n, pred=OWL.qualifiedCardinality):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, pred, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


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
    return r


# MetallicStrandSet is a physical part that realizes electrical continuity; it is
# not itself the physical connection. Keep it as a PartElement.
g.remove((U("MetallicStrandSet"), RDFS.subClassOf, U("PhysicalConnection")))
g.add((U("MetallicStrandSet"), RDFS.subClassOf, U("PartElement")))

for definition in list(g.objects(U("MetallicStrandSet"), SKOS.definition)):
    if getattr(definition, "language", None) == "en":
        g.remove((U("MetallicStrandSet"), SKOS.definition, definition))
g.add((U("MetallicStrandSet"), SKOS.definition, Literal(
    "Physical set of metallic strands used to establish electrical continuity between galvanically connected elements, such as sacrificial anodes and protected metallic infrastructure.",
    lang="en")))
g.add((U("MetallicStrandSet"), SKOS.definition, Literal(
    "Conjunto físico de cordoalhas metálicas usado para estabelecer continuidade elétrica entre elementos conectados galvanicamente, como anodos sacrificiais e infraestrutura metálica protegida.",
    lang="pt-br")))

# Galvanic interfaces are electrical connection points with distinct endpoint roles.
add_class(
    "GalvanicConnectionPoint", "ElectricPort",
    "Galvanic Connection Point", "Ponto de Conexão Galvânica",
    "Electrical connection point participating in a galvanic connection for intentional electrical continuity.",
    "Ponto de conexão elétrica que participa de uma conexão galvânica para continuidade elétrica intencional.",
)
add_class(
    "AnodeGalvanicConnectionPoint", "GalvanicConnectionPoint",
    "Anode Galvanic Connection Point", "Ponto de Conexão Galvânica do Anodo",
    "Galvanic connection point on the sacrificial-anode side of a cathodic-protection connection.",
    "Ponto de conexão galvânica no lado do anodo sacrificial de uma conexão de proteção catódica.",
)
add_class(
    "ProtectedStructureGalvanicConnectionPoint", "GalvanicConnectionPoint",
    "Protected Structure Galvanic Connection Point", "Ponto de Conexão Galvânica da Estrutura Protegida",
    "Galvanic connection point on the protected-metallic-structure side of a cathodic-protection connection.",
    "Ponto de conexão galvânica no lado da estrutura metálica protegida de uma conexão de proteção catódica.",
)
g.add((U("AnodeGalvanicConnectionPoint"), OWL.disjointWith, U("ProtectedStructureGalvanicConnectionPoint")))
all_values("AnodeGalvanicConnectionPoint", "isConnectedTo", "ProtectedStructureGalvanicConnectionPoint")
all_values("ProtectedStructureGalvanicConnectionPoint", "isConnectedTo", "AnodeGalvanicConnectionPoint")

# The connection itself is the physical joint. One endpoint is on the sacrificial
# anode side and one on the protected structure side. One or more strand sets may
# physically realize the electrical continuity; no owner-specific cardinality is
# asserted here because the current domain model does not establish how many such
# connections each AnodeCollarSet or EndFitting must have.
add_class(
    "GalvanicConnection", "PhysicalConnection",
    "Galvanic Connection", "Conexão Galvânica",
    "Physical electrical connection that intentionally establishes galvanic continuity between a sacrificial-anode side and a protected metallic structure for cathodic protection.",
    "Conexão elétrica física que estabelece intencionalmente continuidade galvânica entre o lado de um anodo sacrificial e uma estrutura metálica protegida para proteção catódica.",
)
qcard("GalvanicConnection", "connectsInterface", "AnodeGalvanicConnectionPoint", 1)
qcard("GalvanicConnection", "connectsInterface", "ProtectedStructureGalvanicConnectionPoint", 1)
all_values_union(
    "GalvanicConnection", "connectsInterface",
    ["AnodeGalvanicConnectionPoint", "ProtectedStructureGalvanicConnectionPoint"],
)
qcard("GalvanicConnection", "hasPart", "MetallicStrandSet", 1, OWL.minQualifiedCardinality)
all_values("GalvanicConnection", "hasPart", "MetallicStrandSet")

for other in ("FlangedJoint", "FlexiblePipeCrimpedJoint", "WeldedJoint", "ClampedJoint"):
    g.add((U("GalvanicConnection"), OWL.disjointWith, U(other)))

# Guardrails.
assert (U("MetallicStrandSet"), RDFS.subClassOf, U("PartElement")) in g
assert (U("MetallicStrandSet"), RDFS.subClassOf, U("PhysicalConnection")) not in g
assert (U("GalvanicConnection"), RDFS.subClassOf, U("PhysicalConnection")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added galvanic connection semantics; ontology now has {len(g)} triples")
