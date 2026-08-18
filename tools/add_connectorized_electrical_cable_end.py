from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


def add_class(name, parent, label_en, label_pt, def_en, def_pt):
    c=U(name)
    g.add((c,RDF.type,OWL.Class))
    g.add((c,RDFS.subClassOf,U(parent)))
    g.add((c,DCT.identifier,Literal(name)))
    g.add((c,SKOS.prefLabel,Literal(label_en,lang="en")))
    g.add((c,SKOS.prefLabel,Literal(label_pt,lang="pt-br")))
    g.add((c,SKOS.definition,Literal(def_en,lang="en")))
    g.add((c,SKOS.definition,Literal(def_pt,lang="pt-br")))
    return c


def all_values(cls, prop, target):
    for r in g.objects(U(cls),RDFS.subClassOf):
        if (r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U(prop)) in g and (r,OWL.allValuesFrom,U(target)) in g:
            return r
    r=BNode()
    g.add((r,RDF.type,OWL.Restriction)); g.add((r,OWL.onProperty,U(prop))); g.add((r,OWL.allValuesFrom,U(target)))
    g.add((U(cls),RDFS.subClassOf,r)); return r


def min_qcard(cls, prop, target, n):
    for r in g.objects(U(cls),RDFS.subClassOf):
        if ((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U(prop)) in g and
            (r,OWL.onClass,U(target)) in g and
            (r,OWL.minQualifiedCardinality,Literal(n,datatype=XSD.nonNegativeInteger)) in g):
            return r
    r=BNode()
    g.add((r,RDF.type,OWL.Restriction)); g.add((r,OWL.onProperty,U(prop))); g.add((r,OWL.onClass,U(target)))
    g.add((r,OWL.minQualifiedCardinality,Literal(n,datatype=XSD.nonNegativeInteger)))
    g.add((U(cls),RDFS.subClassOf,r)); return r


def has_only(cls, prop, target):
    return any((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U(prop)) in g and (r,OWL.allValuesFrom,U(target)) in g for r in g.objects(U(cls),RDFS.subClassOf))


def has_min(cls, prop, target, n):
    return any((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U(prop)) in g and (r,OWL.onClass,U(target)) in g and (r,OWL.minQualifiedCardinality,Literal(n,datatype=XSD.nonNegativeInteger)) in g for r in g.objects(U(cls),RDFS.subClassOf))


add_class(
    "ConnectorizedElectricalCableEnd", "ElectricalCableEnd",
    "Connectorized Electrical Cable End", "Extremidade de Cabo Elétrico com Conector",
    "Electrical cable end whose exposed service interface is provided through connector-based electrical mating hardware. It is a specialization for connectorized termination and does not imply that every electrical cable end is connectorized.",
    "Extremidade de cabo elétrico cuja interface de serviço exposta é fornecida por hardware de acoplamento elétrico baseado em conector. É uma especialização para terminação com conector e não implica que toda extremidade de cabo elétrico seja connectorizada.",
)

all_values("ConnectorizedElectricalCableEnd", "hasEndInterface", "ElectricalConnectorPort")
min_qcard("ConnectorizedElectricalCableEnd", "isTerminatedBy", "Connector", 1)

assert (U("ConnectorizedElectricalCableEnd"),RDFS.subClassOf,U("ElectricalCableEnd")) in g
assert has_only("ConnectorizedElectricalCableEnd","hasEndInterface","ElectricalConnectorPort")
assert has_min("ConnectorizedElectricalCableEnd","isTerminatedBy","Connector",1)
assert (U("ConnectorizedElectricalCableEnd"),RDF.type,OWL.NamedIndividual) not in g

# Generic electrical cable ends remain open to non-connector termination patterns such as
# splice boxes, direct terminations or future penetrator/feedthrough modelling.
assert not has_only("ElectricalCableEnd","hasEndInterface","ElectricalConnectorPort")
assert not has_min("ElectricalCableEnd","isTerminatedBy","Connector",1)

# Functional service and connectorization remain orthogonal. A connectorized end may also
# be typed as a control or power end; no disjointness is introduced.
for functional in ("ElectricalControlCableEnd","ElectricalPowerCableEnd"):
    assert (U("ConnectorizedElectricalCableEnd"),OWL.disjointWith,U(functional)) not in g
    assert (U(functional),OWL.disjointWith,U("ConnectorizedElectricalCableEnd")) not in g

# No UTA/UTM composition is forced here; terminal assemblies aggregate whichever hardware
# is required by the actual project architecture.
for cls in ("UTA","UTM"):
    for r in g.objects(U(cls),RDFS.subClassOf):
        if (r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U("hasTerminalHardware")) in g:
            assert (r,OWL.onClass,U("Connector")) not in g
            assert (r,OWL.allValuesFrom,U("Connector")) not in g

for r in set(g.subjects(RDF.type,OWL.Restriction)):
    assert len(list(g.objects(r,OWL.onProperty)))==1


g.bind("edo",EDO); g.bind("skos",SKOS); g.bind("dcterms",DCT)
g.serialize(destination=PATH,format="turtle")
print(f"Added connectorized electrical cable-end model; ontology now has {len(g)} triples")
